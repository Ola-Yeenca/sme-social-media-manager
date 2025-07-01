"""
GitHub Workflow troubleshooting and fixes for SME Analytica Social Media Manager
"""

import asyncio
import os
import sys
from datetime import datetime, timezone
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging for debugging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def debug_automation_issue():
    """Debug the automation that failed to trigger at 13:00"""
    
    logger.info("=== SME Analytica Automation Debug Session ===")
    logger.info(f"Current time: {datetime.now(timezone.utc)}")
    
    # Check 1: Environment variables
    logger.info("1. Checking environment variables...")
    required_env_vars = [
        'NOTION_TOKEN',
        'NOTION_DATABASE_ID', 
        'TWITTER_API_KEY',
        'TWITTER_API_SECRET',
        'TWITTER_ACCESS_TOKEN',
        'TWITTER_ACCESS_TOKEN_SECRET',
        'TWITTER_BEARER_TOKEN',
        'OPENAI_API_KEY',
        'ANTHROPIC_API_KEY'
    ]
    
    missing_vars = []
    for var in required_env_vars:
        if not os.getenv(var):
            missing_vars.append(var)
        else:
            logger.info(f"✅ {var} is set")
    
    if missing_vars:
        logger.error(f"❌ Missing environment variables: {missing_vars}")
        return False
    
    # Check 2: Notion connection
    logger.info("2. Testing Notion connection...")
    try:
        # Add both src and project root to Python path
        sys.path.insert(0, '/Users/olayinka/sme_social_manager')
        sys.path.insert(0, '/Users/olayinka/sme_social_manager/src')
        
        # Test Notion connection directly
        from notion_client import Client
        
        notion_client = Client(auth=os.getenv('NOTION_TOKEN'))
        database_id = os.getenv('NOTION_DATABASE_ID')
        
        # Test basic connection
        response = notion_client.databases.retrieve(database_id)
        if response:
            logger.info("✅ Notion connection successful")
            logger.info(f"Database: {response.get('title', [{}])[0].get('plain_text', 'N/A')}")
        else:
            logger.error("❌ Notion connection failed")
            return False
            
    except Exception as e:
        logger.error(f"❌ Notion connection error: {e}")
        return False
    
    # Check 3: Twitter connection
    logger.info("3. Testing Twitter connection...")
    try:
        from social.twitter_manager import TwitterManager
        
        twitter_manager = TwitterManager({
            "api_key": os.getenv('TWITTER_API_KEY'),
            "api_secret": os.getenv('TWITTER_API_SECRET'),
            "access_token": os.getenv('TWITTER_ACCESS_TOKEN'),
            "access_token_secret": os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
            "bearer_token": os.getenv('TWITTER_BEARER_TOKEN')
        })
        
        account_info = await twitter_manager.get_account_metrics()
        if account_info:
            logger.info("✅ Twitter connection successful")
            logger.info(f"Account: {account_info.get('followers_count', 'N/A')} followers")
        else:
            logger.error("❌ Twitter connection failed")
            return False
            
    except Exception as e:
        logger.error(f"❌ Twitter connection error: {e}")
        return False
    
    # Check 4: Content generation
    logger.info("4. Testing content generation...")
    try:
        from social_media_manager import SocialMediaManager
        
        manager = SocialMediaManager()
        
        # Test content generation
        await manager._generate_daily_content()
        logger.info("✅ Content generation successful")
        
    except Exception as e:
        logger.error(f"❌ Content generation error: {e}")
        return False
    
    logger.info("=== Debug complete - all systems operational ===")
    return True

if __name__ == "__main__":
    asyncio.run(debug_automation_issue())
