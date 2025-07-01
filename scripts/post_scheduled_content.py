#!/usr/bin/env python3
"""
Script specifically for posting scheduled content - fixes the 13:00 trigger issue
"""

import asyncio
import logging
import sys
import os
from datetime import datetime, timezone, timedelta

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from social_media_manager import SocialMediaManager
from notion.notion_manager import NotionManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def post_scheduled_content_now():
    """Force post any content scheduled for now (13:00 fix)"""
    
    logger.info("🚀 SME Analytica - Posting Scheduled Content")
    logger.info(f"Current time: {datetime.now(timezone.utc)}")
    
    try:
        # Initialize the social media manager
        manager = SocialMediaManager()
        
        # Check for scheduled content from Notion
        if hasattr(manager, 'notion_manager') and manager.notion_manager:
            logger.info("📋 Checking Notion for scheduled content...")
            
            # Get content scheduled for today
            today = datetime.now(timezone.utc).date()
            start_time = datetime.combine(today, datetime.min.time()).replace(tzinfo=timezone.utc)
            end_time = start_time + timedelta(days=1)
            
            # Query Notion for today's content
            scheduled_content = await manager.notion_manager.query_content_plans(
                status_filter="Scheduled",
                date_range={"start": start_time, "end": end_time}
            )
            
            logger.info(f"Found {len(scheduled_content)} scheduled content items")
            
            for content in scheduled_content:
                if content.status == "Scheduled" and content.generated_content:
                    logger.info(f"📤 Posting: {content.title}")
                    
                    # Post to Twitter
                    tweet_id = await manager.twitter_manager.post_tweet(content.generated_content)
                    
                    if tweet_id:
                        logger.info(f"✅ Posted successfully: {tweet_id}")
                        
                        # Update Notion with tweet ID and status
                        await manager.notion_manager.update_content_plan(
                            content.title,  # You might need to track page IDs differently
                            {
                                "status": "Published",
                                "tweet_id": tweet_id
                            }
                        )
                    else:
                        logger.error(f"❌ Failed to post: {content.title}")
        
        # Also check local database for scheduled posts
        logger.info("💾 Checking local database for scheduled content...")
        await manager._post_scheduled_content()
        
        # If no scheduled content, generate and post new content
        current_hour = datetime.now(timezone.utc).hour
        if current_hour == 13:  # 1 PM UTC
            logger.info("🕐 It's 13:00 UTC - generating and posting midday content...")
            
            # Generate content for midday posting
            theme = manager._get_theme_for_day(datetime.now().weekday())
            
            # Create content request for midday post
            from ai_providers import ContentRequest, ContentType
            from config.settings import sme_context, Language
            
            content_request = ContentRequest(
                content_type=ContentType.TWEET,
                language=Language.SPANISH.value,  # Spanish for midday post
                theme=theme.value,
                context={
                    "target_audience": "restaurant owners",
                    "focus": "practical business insights",
                    "tone": "conversational expert",
                    "time_of_day": "midday",
                    "include_cta": True
                },
                hashtags=sme_context.HASHTAGS["primary"]
            )
            
            # Generate content
            generated_content = await manager.ai_manager.generate_content(content_request)
            
            if generated_content and generated_content.text:
                logger.info(f"📝 Generated midday content: {generated_content.text[:100]}...")
                
                # Post immediately
                tweet_id = await manager.twitter_manager.post_tweet(generated_content.text)
                
                if tweet_id:
                    logger.info(f"✅ Posted midday content: {tweet_id}")
                    
                    # Save to local database
                    from social_media_manager import PostSchedule
                    post = PostSchedule(
                        id=f"midday_{datetime.now().strftime('%Y%m%d_%H%M')}",
                        content=generated_content.text,
                        scheduled_time=datetime.now(timezone.utc),
                        language="es",
                        theme=theme.value,
                        posted=True,
                        tweet_id=tweet_id
                    )
                    
                    manager._save_scheduled_post(post)
                    manager._update_posted_status(post)
                    
                    # Update Notion if available
                    if hasattr(manager, 'notion_manager') and manager.notion_manager:
                        await manager.notion_manager.create_sme_content_plan({
                            "title": f"Midday Post - {datetime.now().strftime('%Y-%m-%d')}",
                            "content_type": "Tweet",
                            "theme": theme.value,
                            "language": "Spanish",
                            "target_audience": "Restaurant Owners",
                            "scheduled_date": datetime.now(timezone.utc),
                            "status": "Published",
                            "generated_content": generated_content.text,
                            "tweet_id": tweet_id,
                            "ai_provider": generated_content.metadata.get("provider", "Unknown")
                        })
                else:
                    logger.error("❌ Failed to post midday content")
            else:
                logger.error("❌ Failed to generate midday content")
        
        logger.info("✅ Scheduled content posting completed")
        
    except Exception as e:
        logger.error(f"❌ Error in scheduled content posting: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

async def test_posting_system():
    """Test the posting system without actually posting"""
    
    logger.info("🧪 Testing posting system...")
    
    try:
        manager = SocialMediaManager()
        
        # Test system components
        test_results = await manager.test_system()
        
        logger.info("Test Results:")
        for component, status in test_results.items():
            status_str = "✅ PASS" if status else "❌ FAIL"
            logger.info(f"  {component}: {status_str}")
        
        # Test content generation
        logger.info("🧠 Testing content generation...")
        theme = manager._get_theme_for_day(datetime.now().weekday())
        
        from ai_providers import ContentRequest, ContentType
        from config.settings import Language
        
        content_request = ContentRequest(
            content_type=ContentType.TWEET,
            language=Language.ENGLISH.value,
            theme=theme.value,
            context={"test": True},
            hashtags=["#SMEAnalytica", "#Test"]
        )
        
        generated_content = await manager.ai_manager.generate_content(content_request)
        
        if generated_content:
            logger.info(f"✅ Generated test content: {generated_content.text}")
        else:
            logger.error("❌ Failed to generate test content")
        
        return all(test_results.values())
        
    except Exception as e:
        logger.error(f"❌ Testing failed: {e}")
        return False

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="SME Analytica Scheduled Content Poster")
    parser.add_argument(
        '--test', 
        action='store_true', 
        help='Run in test mode (no actual posting)'
    )
    
    args = parser.parse_args()
    
    if args.test:
        success = asyncio.run(test_posting_system())
        sys.exit(0 if success else 1)
    else:
        asyncio.run(post_scheduled_content_now())

if __name__ == "__main__":
    main()
