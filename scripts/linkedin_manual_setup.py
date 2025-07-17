#!/usr/bin/env python3
"""
LinkedIn Manual Setup Helper
For when OAuth flow needs product approvals
"""

import requests

def test_linkedin_credentials():
    """Test LinkedIn credentials and provide setup guidance"""
    
    print("🔗 LinkedIn Manual Setup Helper")
    print("=" * 50)
    
    print("\n📋 Required LinkedIn App Products:")
    print("1. Share on LinkedIn")
    print("2. Marketing Developer Platform") 
    print("3. Sign In with LinkedIn using OpenID Connect")
    
    print("\n🔧 Manual Token Generation:")
    print("1. Go to: https://developer.linkedin.com/")
    print("2. Select your 'SME Analytica Social Manager' app")
    print("3. Click 'Auth' tab")
    print("4. Use 'OAuth 2.0 tools' to generate token")
    print("5. Select scopes: w_member_social, w_organization_social, r_organization_social")
    
    print("\n📝 Your App Details:")
    print(f"Client ID: 7707x12iau05l8")
    print(f"Company Page: https://www.linkedin.com/company/smeanalytica/")
    print(f"Organization ID: smeanalytica")
    
    # Get token from user input
    print("\n🔑 Enter your access token when ready:")
    access_token = input("Access Token: ").strip()
    
    if not access_token:
        print("❌ No access token provided")
        return
    
    # Test the token
    print("\n🧪 Testing access token...")
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Test basic profile access
    try:
        response = requests.get(
            'https://api.linkedin.com/v2/people/~',
            headers=headers
        )
        
        if response.status_code == 200:
            profile = response.json()
            print(f"✅ Token valid! Connected as: {profile.get('localizedFirstName', 'Unknown')} {profile.get('localizedLastName', '')}")
        else:
            print(f"❌ Token test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Error testing token: {e}")
        return
    
    # Test organization access
    try:
        response = requests.get(
            'https://api.linkedin.com/v2/organizationAcls',
            headers=headers,
            params={'q': 'roleAssignee'}
        )
        
        if response.status_code == 200:
            data = response.json()
            organizations = data.get('elements', [])
            
            if organizations:
                print(f"✅ Organization access confirmed! Found {len(organizations)} organization(s)")
                for org in organizations:
                    org_urn = org.get('organization', '')
                    if 'smeanalytica' in org_urn.lower() or org_urn:
                        org_id = org_urn.split(':')[-1] if ':' in org_urn else 'smeanalytica'
                        print(f"  - Organization ID: {org_id}")
            else:
                print("⚠️ No organizations found. You may need 'Marketing Developer Platform' product approval")
                
        else:
            print(f"⚠️ Organization access limited: {response.status_code}")
            print("This is normal if 'Marketing Developer Platform' isn't approved yet")
            
    except Exception as e:
        print(f"⚠️ Organization test error: {e}")
    
    # Provide final setup instructions
    print("\n🎉 Setup Instructions:")
    print("=" * 30)
    print("Add these to your .env file:")
    print()
    print(f"LINKEDIN_ACCESS_TOKEN={access_token}")
    print(f"LINKEDIN_ORGANIZATION_ID=smeanalytica")
    print()
    print("Add these to GitHub Secrets:")
    print(f"  LINKEDIN_ACCESS_TOKEN: {access_token}")
    print(f"  LINKEDIN_ORGANIZATION_ID: smeanalytica")
    print()
    print("🚀 Your LinkedIn integration is ready!")
    print("Note: Company page posting requires 'Marketing Developer Platform' approval")

if __name__ == "__main__":
    test_linkedin_credentials()
