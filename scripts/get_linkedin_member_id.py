#!/usr/bin/env python3
"""
Get LinkedIn Member ID
This script helps you find your LinkedIn member ID for proper API calls
"""

import os
import requests
import json

def load_env_vars():
    """Load environment variables from .env file"""
    env_vars = {}
    
    try:
        with open('.env', 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    except FileNotFoundError:
        print("❌ .env file not found!")
        return None
    
    return env_vars

def get_member_id(access_token):
    """Try different approaches to get the LinkedIn member ID"""
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    
    print("🔍 Trying to find your LinkedIn member ID...")
    
    # Method 1: Try the basic profile endpoint with minimal fields
    endpoints_to_try = [
        ('https://api.linkedin.com/v2/people/~:(id)', 'Basic profile with ID only'),
        ('https://api.linkedin.com/v2/me', 'Me endpoint'),
        ('https://api.linkedin.com/v2/people/~', 'Full profile endpoint'),
        ('https://api.linkedin.com/v2/people/~:(id,firstName,lastName)', 'Profile with basic fields'),
    ]
    
    for endpoint, description in endpoints_to_try:
        try:
            print(f"\n🧪 Trying: {description}")
            print(f"   URL: {endpoint}")
            
            response = requests.get(endpoint, headers=headers)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Success! Response: {json.dumps(data, indent=2)}")
                
                member_id = data.get('id')
                if member_id:
                    print(f"\n🎯 Found your LinkedIn Member ID: {member_id}")
                    return member_id
            else:
                print(f"   ❌ Failed: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Method 2: Try to extract from error messages
    print("\n🔄 Trying to extract member ID from UGC posts endpoint...")
    try:
        # Make a deliberately malformed request to see if we get useful error info
        test_post = {
            "author": "urn:li:person:~",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": "test"},
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
        }
        
        response = requests.post(
            'https://api.linkedin.com/v2/ugcPosts',
            headers=headers,
            json=test_post
        )
        
        print(f"UGC Posts Status: {response.status_code}")
        print(f"UGC Posts Response: {response.text}")
        
        # Sometimes the error message contains hints about the correct format
        
    except Exception as e:
        print(f"UGC Posts Error: {e}")
    
    return None

def test_with_member_id(access_token, member_id):
    """Test posting with the correct member ID"""
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }
    
    print(f"\n🧪 Testing post creation with member ID: {member_id}")
    
    try:
        test_post = {
            "author": f"urn:li:member:{member_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": "🧪 Testing SME Analytica LinkedIn integration! This automated post confirms our social media system is working. #SMEAnalytica #TestPost #Automation"
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        print(f"📝 Using author URN: urn:li:member:{member_id}")
        
        response = requests.post(
            'https://api.linkedin.com/v2/ugcPosts',
            headers=headers,
            json=test_post
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            post_data = response.json()
            post_id = post_data.get('id')
            print(f"🎉 SUCCESS! Created LinkedIn post: {post_id}")
            print("✅ Your LinkedIn integration is working!")
            return True
        else:
            print(f"❌ Failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def update_env_file(member_id):
    """Update .env file with the member ID"""
    try:
        # Read current .env file
        with open('.env', 'r') as f:
            lines = f.readlines()
        
        # Add member ID
        with open('.env', 'a') as f:
            f.write(f"\nLINKEDIN_MEMBER_ID={member_id}\n")
        
        print(f"✅ Added LINKEDIN_MEMBER_ID={member_id} to .env file")
        
    except Exception as e:
        print(f"❌ Error updating .env file: {e}")

def main():
    print("SME Analytica LinkedIn Member ID Finder")
    print("=" * 50)
    
    # Load environment variables
    env_vars = load_env_vars()
    if not env_vars:
        return
    
    access_token = env_vars.get('LINKEDIN_ACCESS_TOKEN')
    if not access_token:
        print("❌ LINKEDIN_ACCESS_TOKEN not found in .env file!")
        return
    
    print(f"✅ Found access token: {access_token[:20]}...")
    
    # Try to get member ID
    member_id = get_member_id(access_token)
    
    if member_id:
        print(f"\n🎯 Your LinkedIn Member ID: {member_id}")
        
        # Test posting with this member ID
        success = test_with_member_id(access_token, member_id)
        
        if success:
            # Update .env file
            update_env_file(member_id)
            
            print("\n" + "="*50)
            print("🎉 LINKEDIN INTEGRATION COMPLETE!")
            print("="*50)
            print(f"✅ Member ID: {member_id}")
            print("✅ Posting test: Successful")
            print("✅ Configuration: Updated")
            print("\n🚀 Your LinkedIn automation is ready!")
        else:
            print("\n❌ Posting test failed, but we have your member ID")
            print(f"Add this to your .env file: LINKEDIN_MEMBER_ID={member_id}")
    else:
        print("\n❌ Could not determine your LinkedIn member ID")
        print("\n💡 Manual steps:")
        print("1. Check your LinkedIn app permissions")
        print("2. Ensure you have 'r_liteprofile' or 'r_basicprofile' scope")
        print("3. Try regenerating your access token")

if __name__ == "__main__":
    main()
