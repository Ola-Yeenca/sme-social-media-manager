#!/usr/bin/env python3
"""
LinkedIn OAuth2 Authentication Helper
Generates access token for SME Analytica LinkedIn integration
"""

import requests
import urllib.parse
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

# Your LinkedIn App Credentials - Load from environment variables
CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID", "7707x12iau05l8")
CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")  # NEVER hardcode secrets!
REDIRECT_URI = "http://localhost:8080/callback"

if not CLIENT_SECRET:
    print("❌ ERROR: LINKEDIN_CLIENT_SECRET environment variable not set!")
    print("Please add LINKEDIN_CLIENT_SECRET to your .env file")
    exit(1)

# LinkedIn OAuth2 URLs
AUTHORIZATION_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"

# Required scopes for posting to company page
SCOPES = [
    "w_member_social",      # Post on behalf of members
    "w_organization_social", # Post to company page
    "r_organization_social"  # Read company metrics
]

class CallbackHandler(BaseHTTPRequestHandler):
    """Handle OAuth callback"""
    
    def do_GET(self):
        if self.path.startswith('/callback'):
            # Parse authorization code from callback
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            
            if 'code' in params:
                self.server.auth_code = params['code'][0]
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                html_response = """
                <html>
                <body>
                <h1>Authorization Successful!</h1>
                <p>You can close this window and return to the terminal.</p>
                <script>setTimeout(() => window.close(), 3000);</script>
                </body>
                </html>
                """
                self.wfile.write(html_response.encode('utf-8'))
            else:
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                error_response = """
                <html>
                <body>
                <h1>Authorization Failed</h1>
                <p>No authorization code received.</p>
                </body>
                </html>
                """
                self.wfile.write(error_response.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress default logging
        pass

def get_authorization_url():
    """Generate LinkedIn authorization URL"""
    
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': ' '.join(SCOPES),
        'state': 'sme_analytica_auth'
    }
    
    url = f"{AUTHORIZATION_URL}?{urllib.parse.urlencode(params)}"
    return url

def exchange_code_for_token(auth_code):
    """Exchange authorization code for access token"""
    
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    
    response = requests.post(TOKEN_URL, data=data)
    
    if response.status_code == 200:
        token_data = response.json()
        return token_data.get('access_token')
    else:
        print(f"Token exchange failed: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def get_organization_id(access_token):
    """Get organization ID for SME Analytica company page"""
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Search for organizations the user can manage
    response = requests.get(
        'https://api.linkedin.com/v2/organizationAcls',
        headers=headers,
        params={'q': 'roleAssignee'}
    )
    
    if response.status_code == 200:
        data = response.json()
        organizations = data.get('elements', [])
        
        print(f"\nFound {len(organizations)} organization(s):")
        for org in organizations:
            org_urn = org.get('organization')
            if org_urn:
                org_id = org_urn.split(':')[-1]
                print(f"  - Organization ID: {org_id}")
                return org_id
        
        return None
    else:
        print(f"Failed to get organizations: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def main():
    """Main authentication flow"""
    
    print("SME Analytica LinkedIn Authentication Helper")
    print("=" * 50)
    
    # Step 1: Start local server for callback
    print("1. Starting local callback server...")
    server = HTTPServer(('localhost', 8080), CallbackHandler)
    server.auth_code = None
    
    # Run server in background
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    # Step 2: Open authorization URL
    auth_url = get_authorization_url()
    print(f"2. Opening LinkedIn authorization page...")
    print(f"   URL: {auth_url}")
    
    webbrowser.open(auth_url)
    
    # Step 3: Wait for callback
    print("3. Waiting for authorization (please complete in browser)...")
    
    timeout = 120  # 2 minutes timeout
    start_time = time.time()
    
    while server.auth_code is None and (time.time() - start_time) < timeout:
        time.sleep(1)
    
    server.shutdown()
    
    if server.auth_code is None:
        print("Authorization timed out or failed")
        return
    
    print("Authorization code received!")
    
    # Step 4: Exchange code for token
    print("4. Exchanging code for access token...")
    access_token = exchange_code_for_token(server.auth_code)
    
    if not access_token:
        print("Failed to get access token")
        return
    
    print("Access token obtained!")
    
    # Step 5: Get organization ID
    print("5. Getting organization ID...")
    org_id = get_organization_id(access_token)
    
    if not org_id:
        print("Failed to get organization ID")
        return
    
    # Step 6: Display results
    print("\nLinkedIn Integration Setup Complete!")
    print("=" * 50)
    print("Add these to your .env file:")
    print()
    print(f"LINKEDIN_ACCESS_TOKEN={access_token}")
    print(f"LINKEDIN_ORGANIZATION_ID={org_id}")
    print()
    print("Add these to GitHub Secrets:")
    print(f"  LINKEDIN_ACCESS_TOKEN: {access_token}")
    print(f"  LINKEDIN_ORGANIZATION_ID: {org_id}")
    print()
    print("Your SME Analytica automation can now post to LinkedIn!")

if __name__ == "__main__":
    main()
