#!/usr/bin/env python3
"""
Manual Grok Engagement Script
Post strategic questions to @grok immediately for viral engagement
"""

import asyncio
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def post_grok_question():
    """Post a strategic question to @grok immediately"""
    
    logger = logging.getLogger(__name__)
    logger.info("🚀 Manual Grok Engagement - Posting Strategic Question...")
    
    try:
        # Import required modules
        from src.social.twitter_manager import TwitterManager
        from src.engagement.grok_engagement import GrokEngagementFarmer
        
        # Initialize Twitter manager
        twitter_credentials = {
            "api_key": os.getenv("TWITTER_API_KEY"),
            "api_secret": os.getenv("TWITTER_API_SECRET"),
            "access_token": os.getenv("TWITTER_ACCESS_TOKEN"),
            "access_token_secret": os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
            "bearer_token": os.getenv("TWITTER_BEARER_TOKEN")
        }
        
        # Check credentials
        missing_creds = [k for k, v in twitter_credentials.items() if not v]
        if missing_creds:
            logger.error(f"❌ Missing Twitter credentials: {missing_creds}")
            return
        
        # Initialize Twitter manager
        twitter_manager = TwitterManager(twitter_credentials)
        logger.info("✅ Twitter manager initialized")
        
        # Initialize Grok engagement farmer
        grok_farmer = GrokEngagementFarmer(twitter_manager)
        logger.info("✅ Grok farmer initialized")
        
        # Override rate limiting for manual posting
        grok_farmer.daily_grok_questions = 0  # Reset count
        grok_farmer.last_grok_question_time = None  # Reset time
        
        logger.info("🎯 Rate limiting bypassed for manual posting")
        
        # Run Grok engagement
        logger.info("🚀 Posting strategic Grok question...")
        results = await grok_farmer.run_grok_engagement_farming()
        
        if results.get("questions_asked", 0) > 0:
            logger.info("✅ SUCCESS! Grok question posted successfully!")
            logger.info(f"📊 Results: {results}")
            logger.info("🔥 Check your Twitter for the new viral engagement!")
        else:
            logger.warning("⚠️ No question was posted. Check the logs above for details.")
            if results.get("errors"):
                logger.error(f"❌ Errors: {results['errors']}")
        
        return results
        
    except Exception as e:
        logger.error(f"❌ Manual posting failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("🤖 SME Analytica - AI-Driven Grok Engagement")
    print("=" * 55)
    print("This will generate and post a strategic AI-powered question")
    print("to @grok for viral engagement and business influence.")
    print()
    print("🧠 Features:")
    print("  • Dynamic AI question generation")
    print("  • Strategic business positioning")
    print("  • Thought leadership content")
    print("  • Viral engagement optimization")
    print()

    confirm = input("Do you want to post an AI-generated Grok question now? (y/N): ")
    if confirm.lower() in ['y', 'yes']:
        print("\n🚀 Generating and posting strategic Grok question...")
        asyncio.run(post_grok_question())
    else:
        print("❌ Cancelled. No question posted.")
