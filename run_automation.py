#!/usr/bin/env python3
"""
Complete SME Social Media Manager Automation
This script handles the full automation workflow
"""

import os
import sys
import asyncio
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

# Unset the shell environment variable to use .env file
if 'SOCIAL_MEDIA_DB_ID' in os.environ:
    del os.environ['SOCIAL_MEDIA_DB_ID']

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/automation.log'),
        logging.StreamHandler()
    ]
)

async def check_and_post_scheduled_content():
    """Check for scheduled content and post it"""
    
    print("📤 Checking for Scheduled Content to Post")
    print("-" * 50)
    
    try:
        from notion import NotionManager
        import tweepy
        from config.settings import settings
        
        # Initialize components
        notion_manager = NotionManager()
        
        # Initialize Twitter client directly
        twitter_client = tweepy.Client(
            bearer_token=settings.twitter_bearer_token,
            consumer_key=settings.twitter_api_key,
            consumer_secret=settings.twitter_api_secret,
            access_token=settings.twitter_access_token,
            access_token_secret=settings.twitter_access_token_secret,
            wait_on_rate_limit=True
        )
        
        print("✅ Components initialized")
        
        # Get scheduled posts ready to publish
        ready_posts = notion_manager.get_scheduled_posts()
        
        if not ready_posts:
            print("📋 No posts ready to publish at this time")
            return 0
        
        print(f"📋 Found {len(ready_posts)} posts ready to publish")
        
        posted_count = 0
        
        for post in ready_posts:
            try:
                print(f"\n📤 Posting: {post.content[:50]}...")
                
                # Validate content length
                if len(post.content) > 280:
                    print(f"⚠️  Content too long ({len(post.content)} chars), truncating...")
                    content = post.content[:277] + "..."
                else:
                    content = post.content
                
                # Post to Twitter
                response = twitter_client.create_tweet(text=content)
                
                if response.data:
                    tweet_id = response.data['id']
                    published_time = datetime.now()
                    
                    # Update post status in Notion
                    success = notion_manager.mark_as_published(
                        post.id,
                        tweet_id,
                        published_time
                    )
                    
                    if success:
                        print(f"✅ Posted successfully! Tweet ID: {tweet_id}")
                        print(f"🔗 https://twitter.com/smeanalytica/status/{tweet_id}")
                        posted_count += 1
                    else:
                        print(f"⚠️  Posted to Twitter but failed to update Notion")
                else:
                    print("❌ Failed to post to Twitter")
                    
            except Exception as e:
                print(f"❌ Error posting content: {e}")
        
        print(f"\n📊 Posted {posted_count} out of {len(ready_posts)} scheduled posts")
        return posted_count
        
    except Exception as e:
        print(f"❌ Error in posting workflow: {e}")
        return 0


async def generate_daily_content():
    """Generate new content for today"""
    
    print("\n📝 Generating Daily Content")
    print("-" * 50)
    
    try:
        from notion import NotionManager, SocialMediaPost, PostStatus, Platform, PostType
        from content.content_generator import ContentGenerator, ContentTheme, Language
        
        # Initialize components
        notion_manager = NotionManager()
        content_generator = ContentGenerator()
        
        print("✅ Components initialized")
        
        # Determine today's theme
        today = datetime.now()
        day_themes = {
            0: (ContentTheme.DATA_MONDAY, "Data Monday", "📊"),
            1: (ContentTheme.TALK_TUESDAY, "Talk Tuesday", "💬"),
            2: (ContentTheme.CASE_WEDNESDAY, "Case Wednesday", "🏆"),
            3: (ContentTheme.TECH_THURSDAY, "Tech Thursday", "⚡"),
            4: (ContentTheme.FACT_FRIDAY, "Fact Friday", "💡"),
            5: (ContentTheme.WEEKEND_INSIGHTS, "Weekend Insights", "🌟"),
            6: (ContentTheme.WEEKEND_INSIGHTS, "Weekend Insights", "🌟")
        }
        
        theme, theme_name, emoji = day_themes.get(today.weekday(), day_themes[0])
        
        print(f"📅 Today is {today.strftime('%A')} - Theme: {theme_name} {emoji}")
        
        # Optimal posting times
        posting_times = [
            {"hour": 9, "minute": 0},   # Morning business start
            {"hour": 13, "minute": 0},  # Lunch break
            {"hour": 17, "minute": 30}  # End of business day
        ]
        
        generated_count = 0
        
        for i, posting_time in enumerate(posting_times):
            print(f"\n{i+1}. Generating content for {posting_time['hour']:02d}:{posting_time['minute']:02d}...")
            
            # Generate content
            content = content_generator.generate_themed_content(theme, Language.ENGLISH)
            
            if content and content.get("text"):
                # Calculate scheduled time
                scheduled_time = today.replace(
                    hour=posting_time["hour"],
                    minute=posting_time["minute"],
                    second=0,
                    microsecond=0
                )
                
                # If time has passed, schedule for tomorrow
                if scheduled_time <= datetime.now():
                    scheduled_time += timedelta(days=1)
                
                # Create post
                post = SocialMediaPost(
                    name=f"SME Analytica - {theme_name} {today.strftime('%Y-%m-%d')} #{i+1}",
                    content=content["text"],
                    status=PostStatus.SCHEDULED,
                    platform=Platform.TWITTER,
                    post_type=PostType.INFORMATIONAL,
                    scheduled_time=scheduled_time,
                    language="English",
                    content_theme=theme_name,
                    ai_provider_used="Grok",
                    tags=content.get("hashtags", ["SMEAnalytica"])[:5]
                )
                
                # Save to Notion
                post_id = notion_manager.create_post(post)
                
                if post_id:
                    print(f"   ✅ Created: {content['text'][:50]}...")
                    print(f"   📅 Scheduled for: {scheduled_time.strftime('%Y-%m-%d %H:%M')}")
                    generated_count += 1
                else:
                    print(f"   ❌ Failed to save to Notion")
            else:
                print(f"   ❌ Failed to generate content")
        
        print(f"\n📊 Generated {generated_count} new posts for today")
        return generated_count
        
    except Exception as e:
        print(f"❌ Error generating daily content: {e}")
        return 0


async def show_analytics():
    """Show current analytics and status"""
    
    print("\n📊 Analytics & Status")
    print("-" * 50)
    
    try:
        from notion import NotionManager
        from config.settings import settings
        import tweepy
        
        # Initialize components
        notion_manager = NotionManager()
        
        # Get post counts by status
        draft_posts = notion_manager.get_posts_by_status("Draft", limit=100)
        scheduled_posts = notion_manager.get_posts_by_status("Scheduled", limit=100)
        published_posts = notion_manager.get_posts_by_status("Published", limit=100)
        
        print(f"📋 Content Status:")
        print(f"   • Draft: {len(draft_posts)} posts")
        print(f"   • Scheduled: {len(scheduled_posts)} posts")
        print(f"   • Published: {len(published_posts)} posts")
        
        # Twitter account info
        try:
            twitter_client = tweepy.Client(bearer_token=settings.twitter_bearer_token)
            user = twitter_client.get_me(user_fields=['public_metrics'])
            
            if user and user.data:
                metrics = user.data.public_metrics
                print(f"\n🐦 Twitter Account (@{user.data.username}):")
                print(f"   • Followers: {metrics['followers_count']}")
                print(f"   • Following: {metrics['following_count']}")
                print(f"   • Tweets: {metrics['tweet_count']}")
        except Exception as e:
            print(f"⚠️  Could not fetch Twitter metrics: {e}")
        
        # Database info
        db_id = settings.social_media_db_id
        print(f"\n🔗 Notion Database: https://www.notion.so/{db_id.replace('-', '')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error showing analytics: {e}")
        return False


async def run_full_automation():
    """Run the complete automation workflow"""
    
    print("🚀 SME Social Media Manager - Full Automation")
    print("=" * 60)
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # 1. Check and post scheduled content
    posted_count = await check_and_post_scheduled_content()
    
    # 2. Generate new daily content
    generated_count = await generate_daily_content()
    
    # 3. Show analytics
    await show_analytics()
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 Automation Complete!")
    print(f"📤 Posted: {posted_count} tweets")
    print(f"📝 Generated: {generated_count} new posts")
    print(f"🕐 Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return {"posted": posted_count, "generated": generated_count}


async def main():
    """Main function with command handling"""
    
    command = sys.argv[1] if len(sys.argv) > 1 else 'full'
    
    if command == 'post':
        await check_and_post_scheduled_content()
    elif command == 'generate':
        await generate_daily_content()
    elif command == 'analytics':
        await show_analytics()
    elif command == 'full':
        await run_full_automation()
    else:
        print("Usage: python run_automation.py [post|generate|analytics|full]")
        print("  post      - Check and post scheduled content")
        print("  generate  - Generate new daily content")
        print("  analytics - Show current analytics")
        print("  full      - Run complete automation (default)")


if __name__ == "__main__":
    asyncio.run(main())
