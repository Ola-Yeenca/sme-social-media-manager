#!/usr/bin/env python3
"""
LinkedIn Organization ID Helper
This script helps you find your LinkedIn organization ID using different methods.
"""

import requests
import json
import sys
from urllib.parse import quote

def test_access_token(access_token):
    """Test if the access token works by getting user profile"""
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    
    try:
        # Test with user profile
        response = requests.get(
            'https://api.linkedin.com/v2/people/~',
            headers=headers
        )
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Access token works! User: {user_data.get('localizedFirstName', 'Unknown')} {user_data.get('localizedLastName', 'Unknown')}")
            return True
        else:
            print(f"❌ Access token test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing access token: {e}")
        return False

def test_posting_capability(access_token):
    """Test if we can create posts and extract organization info"""
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    
    print("\n🧪 Testing posting capabilities...")
    
    # Test creating a simple text post (we'll delete it immediately)
    test_post_data = {
        "author": "urn:li:person:~",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": "Test post - will be deleted immediately"
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    try:
        response = requests.post(
            'https://api.linkedin.com/v2/ugcPosts',
            headers=headers,
            json=test_post_data
        )
        
        if response.status_code == 201:
            post_data = response.json()
            post_id = post_data.get('id')
            print(f"✅ Successfully created test post: {post_id}")
            
            # Try to delete the test post immediately
            delete_response = requests.delete(
                f'https://api.linkedin.com/v2/ugcPosts/{post_id}',
                headers=headers
            )
            
            if delete_response.status_code == 204:
                print("✅ Test post deleted successfully")
            else:
                print(f"⚠️ Could not delete test post (status: {delete_response.status_code})")
                print("Please manually delete the test post from your LinkedIn profile")
            
            return True
        else:
            print(f"❌ Failed to create test post: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing post creation: {e}")
        return False

def get_organization_id_methods(access_token):
    """Try different methods to get organization ID"""
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    
    print("\n🔍 Trying different methods to get organization ID...")
    
    # Method 1: Try organizationAcls (might fail)
    print("\n1️⃣ Method 1: organizationAcls")
    try:
        response = requests.get(
            'https://api.linkedin.com/v2/organizationAcls?q=roleAssignee',
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Response: {json.dumps(data, indent=2)}")
            if 'elements' in data and data['elements']:
                for element in data['elements']:
                    if 'organization' in element:
                        org_id = element['organization'].split(':')[-1]
                        print(f"🎯 Found Organization ID: {org_id}")
                        return org_id
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Method 2: Try organizations endpoint
    print("\n2️⃣ Method 2: organizations")
    try:
        response = requests.get(
            'https://api.linkedin.com/v2/organizations',
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Response: {json.dumps(data, indent=2)}")
            if 'elements' in data and data['elements']:
                org_id = str(data['elements'][0]['id'])
                print(f"🎯 Found Organization ID: {org_id}")
                return org_id
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Method 3: Try company pages endpoint
    print("\n3️⃣ Method 3: company pages")
    try:
        response = requests.get(
            'https://api.linkedin.com/v2/organizationalEntityAcls?q=roleAssignee',
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Response: {json.dumps(data, indent=2)}")
            if 'elements' in data and data['elements']:
                for element in data['elements']:
                    if 'organizationalTarget' in element:
                        org_id = element['organizationalTarget'].split(':')[-1]
                        print(f"🎯 Found Organization ID: {org_id}")
                        return org_id
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return None

def manual_instructions():
    """Provide manual instructions for finding organization ID"""
    print("\n" + "="*60)
    print("📋 MANUAL METHOD TO FIND YOUR ORGANIZATION ID")
    print("="*60)
    print("""
Since the API methods didn't work, here's how to find it manually:

🔍 METHOD 1: LinkedIn Company Page URL
1. Go to your LinkedIn company page
2. Look at the URL: https://www.linkedin.com/company/YOUR-COMPANY-NAME/
3. The organization ID is often in the page source or can be found by:
   - Right-click → View Page Source
   - Search for "organizationId" or "companyId"

🔍 METHOD 2: LinkedIn Developer Tools
1. Go to https://www.linkedin.com/company/YOUR-COMPANY-NAME/
2. Open browser Developer Tools (F12)
3. Go to Network tab
4. Refresh the page
5. Look for API calls containing organization IDs

🔍 METHOD 3: Use a Placeholder for Now
For testing purposes, you can use a placeholder:
LINKEDIN_ORGANIZATION_ID=placeholder

Then test personal posts first, and we'll figure out the org ID later.

🔍 METHOD 4: Contact LinkedIn Support
If you're still having trouble, LinkedIn Developer Support can help
identify your organization ID.

Once you have your organization ID, add it to your .env file as:
LINKEDIN_ORGANIZATION_ID=your_org_id_here
""")

def generate_env_config(access_token, org_id=None):
    """Generate the .env configuration"""
    print("\n" + "="*60)
    print("📝 GENERATING YOUR .ENV CONFIGURATION")
    print("="*60)
    
    config = f"""
# LinkedIn API Configuration
LINKEDIN_CLIENT_ID=7707x12iau05l8
LINKEDIN_ACCESS_TOKEN={access_token}
LINKEDIN_ORGANIZATION_ID={org_id or 'placeholder'}

# Add these to your existing .env file
"""
    
    print(config)
    
    if not org_id:
        print("⚠️ Note: Organization ID is set to 'placeholder'")
        print("You can test personal posts first, then update the org ID later.")

def main():
    print("SME Analytica LinkedIn Organization ID Helper")
    print("=" * 50)
    
    # Get access token from the previous script
    print("Please paste your LinkedIn access token from the previous script:")
    access_token = input("Access token: ").strip()
    
    if not access_token:
        print("❌ No access token provided!")
        return
    
    # Test access token
    if not test_access_token(access_token):
        print("❌ Access token is not working. Please check your token.")
        return
    
    # Test posting capability
    can_post = test_posting_capability(access_token)
    
    if can_post:
        print("✅ Great! You can create posts with this token.")
    
    # Try to get organization ID
    org_id = get_organization_id_methods(access_token)
    
    if org_id:
        print(f"\n🎉 SUCCESS! Your organization ID is: {org_id}")
    else:
        print("\n❌ Could not automatically determine organization ID")
        manual_instructions()
    
    # Generate .env configuration regardless
    generate_env_config(access_token, org_id)

if __name__ == "__main__":
    main()
