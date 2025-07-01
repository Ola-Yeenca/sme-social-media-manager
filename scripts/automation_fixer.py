#!/usr/bin/env python3
"""
SME Analytica Automation Fix Script
Diagnoses and fixes common issues with the 13:00 tweet automation
"""

import asyncio
import os
import sys
import json
from datetime import datetime, timezone, timedelta
import logging

# Setup detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('automation_debug.log')
    ]
)
logger = logging.getLogger(__name__)

class AutomationFixer:
    """Diagnoses and fixes SME Analytica automation issues"""
    
    def __init__(self):
        self.issues_found = []
        self.fixes_applied = []
    
    async def run_complete_diagnosis(self):
        """Run complete diagnosis and fix routine"""
        
        logger.info("🔧 SME Analytica Automation Diagnostics")
        logger.info("=" * 50)
        
        # Step 1: Check environment setup
        await self._check_environment()
        
        # Step 2: Verify API connections
        await self._verify_api_connections()
        
        # Step 3: Check GitHub workflow
        await self._check_github_workflow()
        
        # Step 4: Test Notion integration
        await self._test_notion_integration()
        
        # Step 5: Verify content generation
        await self._verify_content_generation()
        
        # Step 6: Test posting functionality
        await self._test_posting_functionality()
        
        # Summary and fixes
        await self._provide_summary_and_fixes()
    
    async def _check_environment(self):
        """Check environment variables and configuration"""
        
        logger.info("1️⃣ Checking Environment Configuration...")
        
        required_vars = {
            'NOTION_TOKEN': 'Notion integration token',
            'NOTION_DATABASE_ID': 'Notion database ID',
            'TWITTER_API_KEY': 'Twitter API key',
            'TWITTER_API_SECRET': 'Twitter API secret', 
            'TWITTER_ACCESS_TOKEN': 'Twitter access token',
            'TWITTER_ACCESS_TOKEN_SECRET': 'Twitter access token secret',
            'TWITTER_BEARER_TOKEN': 'Twitter bearer token',
            'OPENAI_API_KEY': 'OpenAI API key',
            'ANTHROPIC_API_KEY': 'Anthropic API key'
        }
        
        missing_vars = []
        for var, description in required_vars.items():
            value = os.getenv(var)
            if not value:
                missing_vars.append(f"{var} ({description})")
                logger.error(f"❌ Missing: {var}")
            else:
                # Show first/last few characters for security
                masked_value = f"{value[:4]}...{value[-4:]}" if len(value) > 8 else "***"
                logger.info(f"✅ {var}: {masked_value}")
        
        if missing_vars:
            self.issues_found.append({
                "type": "Missing Environment Variables",
                "details": missing_vars,
                "fix": "Add missing environment variables to your .env file and GitHub secrets"
            })

    async def _verify_api_connections(self):
        """Verify all API connections"""
        
        logger.info("2️⃣ Verifying API Connections...")
        
        # Test basic connectivity first
        try:
            import requests
            response = requests.get("https://api.twitter.com/2/tweets/search/recent?query=test&max_results=10", 
                                  headers={"Authorization": f"Bearer {os.getenv('TWITTER_BEARER_TOKEN')}"})
            if response.status_code == 200:
                logger.info("✅ Twitter API connection successful")
            else:
                logger.error(f"❌ Twitter API error: {response.status_code}")
                self.issues_found.append({
                    "type": "Twitter API Connection",
                    "details": f"HTTP {response.status_code}",
                    "fix": "Check Twitter API credentials"
                })
        except Exception as e:
            logger.error(f"❌ Twitter API error: {e}")
            self.issues_found.append({
                "type": "Twitter API Error", 
                "details": str(e),
                "fix": "Check internet connection and Twitter credentials"
            })

    async def _check_github_workflow(self):
        """Check GitHub workflow configuration"""
        
        logger.info("3️⃣ Checking GitHub Workflow...")
        
        workflow_path = ".github/workflows/social_automation.yml"
        if os.path.exists(workflow_path):
            logger.info("✅ GitHub workflow file exists")
        else:
            logger.error("❌ GitHub workflow file missing")
            self.issues_found.append({
                "type": "Missing GitHub Workflow",
                "details": "No workflow file found",
                "fix": "Create the GitHub Actions workflow file"
            })

    async def _test_notion_integration(self):
        """Test Notion integration"""
        
        logger.info("4️⃣ Testing Notion Integration...")
        
        try:
            import aiohttp
            headers = {
                "Authorization": f"Bearer {os.getenv('NOTION_TOKEN')}",
                "Notion-Version": "2022-06-28"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://api.notion.com/v1/databases/{os.getenv('NOTION_DATABASE_ID')}",
                    headers=headers
                ) as response:
                    if response.status == 200:
                        logger.info("✅ Notion API connection successful")
                    else:
                        logger.error(f"❌ Notion API error: {response.status}")
                        self.issues_found.append({
                            "type": "Notion API Connection",
                            "details": f"HTTP {response.status}",
                            "fix": "Check Notion token and database ID"
                        })
        except Exception as e:
            logger.error(f"❌ Notion error: {e}")

    async def _verify_content_generation(self):
        """Test content generation"""
        
        logger.info("5️⃣ Testing Content Generation...")
        
        try:
            # Simple OpenAI test
            import openai
            client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Generate a short tweet about AI for restaurants"}],
                max_tokens=50
            )
            
            if response.choices[0].message.content:
                logger.info("✅ Content generation working")
                logger.info(f"   Sample: {response.choices[0].message.content}")
            else:
                logger.error("❌ Content generation failed")
                
        except Exception as e:
            logger.error(f"❌ Content generation error: {e}")
            self.issues_found.append({
                "type": "Content Generation Error",
                "details": str(e),
                "fix": "Check OpenAI API key and credits"
            })

    async def _test_posting_functionality(self):
        """Test posting functionality"""
        
        logger.info("6️⃣ Testing Posting Functionality...")
        
        try:
            import tweepy
            
            auth = tweepy.OAuth1UserHandler(
                os.getenv('TWITTER_API_KEY'),
                os.getenv('TWITTER_API_SECRET'), 
                os.getenv('TWITTER_ACCESS_TOKEN'),
                os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
            )
            
            api = tweepy.API(auth)
            
            # Test authentication
            me = api.verify_credentials()
            if me:
                logger.info(f"✅ Twitter authentication successful: @{me.screen_name}")
            else:
                logger.error("❌ Twitter authentication failed")
                
        except Exception as e:
            logger.error(f"❌ Twitter auth error: {e}")
            self.issues_found.append({
                "type": "Twitter Authentication Error",
                "details": str(e), 
                "fix": "Check Twitter API credentials and permissions"
            })

    async def _provide_summary_and_fixes(self):
        """Provide summary and fixes"""
        
        logger.info("📋 DIAGNOSIS SUMMARY")
        logger.info("=" * 50)
        
        if not self.issues_found:
            logger.info("🎉 No major issues found!")
            logger.info("")
            logger.info("If 13:00 tweet still didn't post, try:")
            logger.info("1. Manual test: python scripts/post_scheduled_content.py --test")
            logger.info("2. Check GitHub Actions tab for workflow runs") 
            logger.info("3. Verify GitHub secrets are set correctly")
            logger.info("4. Run manual workflow dispatch")
        else:
            logger.error(f"❌ Found {len(self.issues_found)} issues:")
            logger.info("")
            
            for i, issue in enumerate(self.issues_found, 1):
                logger.error(f"{i}. {issue['type']}")
                logger.error(f"   Details: {issue['details']}")
                logger.info(f"   Fix: {issue['fix']}")
                logger.info("")
        
        logger.info("🔧 QUICK FIXES FOR 13:00 POSTING")
        logger.info("=" * 50)
        logger.info("")
        logger.info("1. Test posting manually:")
        logger.info("   python scripts/post_scheduled_content.py")
        logger.info("")
        logger.info("2. Check GitHub Actions:")
        logger.info("   - Go to your repo > Actions tab")
        logger.info("   - Look for 'Social Media Automation' workflow")
        logger.info("   - Check if it ran at 13:00 UTC")
        logger.info("")
        logger.info("3. Manual trigger:")
        logger.info("   - Actions > Social Media Automation > Run workflow")
        logger.info("   - Select 'post_now' action")
        logger.info("")
        logger.info("4. Check logs:")
        logger.info("   - Look at workflow run logs")
        logger.info("   - Check for error messages")

async def main():
    """Main function"""
    fixer = AutomationFixer()
    await fixer.run_complete_diagnosis()

if __name__ == "__main__":
    asyncio.run(main())
