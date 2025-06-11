"""
Main Social Media Manager for SME Analytica
Orchestrates AI providers, content generation, and Twitter interactions
"""

import asyncio
import logging
import time
import sqlite3
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Import our modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from ai_providers import AIProviderManager, ContentRequest, ContentType, ProviderStrategy
from content.content_generator import ContentGenerator, ContentTheme, Language, ContentCategory
from social.twitter_manager import TwitterManager, Tweet
from config.settings import settings, sme_context
from notion import NotionManager, SocialMediaPost, PostStatus, Platform, PostType

@dataclass
class PostSchedule:
    """Scheduled post data structure"""
    id: str
    content: str
    scheduled_time: datetime
    language: str
    theme: str
    posted: bool = False
    tweet_id: Optional[str] = None

@dataclass
class EngagementAction:
    """Engagement action tracking"""
    id: str
    action_type: str  # like, reply, retweet, quote
    target_tweet_id: str
    target_author: str
    content: Optional[str]  # For replies and quotes
    executed: bool = False
    executed_at: Optional[datetime] = None
    success: bool = False

class SocialMediaManager:
    """Main orchestrator for SME Analytica's social media automation"""
    
    def __init__(self):
        # Initialize components
        self.ai_manager = self._initialize_ai_manager()
        self.content_generator = ContentGenerator()
        self.twitter_manager = self._initialize_twitter_manager()

        # Notion database manager
        self.notion_manager = NotionManager()

        # Keep SQLite for backward compatibility (optional)
        self.db_path = settings.db_path
        self._initialize_database()

        # Scheduling and state
        self.daily_post_count = 0
        self.daily_post_limit = settings.posting_schedule
        self.last_post_reset = datetime.now().date()

        self.logger = logging.getLogger(__name__)
        
    def _initialize_ai_manager(self) -> AIProviderManager:
        """Initialize AI provider manager with credentials"""
        
        config = {
            "openai_api_key": settings.openai_api_key,
            "anthropic_api_key": settings.anthropic_api_key,
            "perplexity_api_key": settings.perplexity_api_key,
            "grok_api_key": settings.grok_api_key
        }
        
        return AIProviderManager(config)
    
    def _initialize_twitter_manager(self) -> TwitterManager:
        """Initialize Twitter API manager"""
        
        credentials = {
            "api_key": settings.twitter_api_key,
            "api_secret": settings.twitter_api_secret,
            "access_token": settings.twitter_access_token,
            "access_token_secret": settings.twitter_access_token_secret,
            "bearer_token": settings.twitter_bearer_token
        }
        
        return TwitterManager(credentials)
    
    def _initialize_database(self):
        """Initialize SQLite database for tracking"""
        
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                scheduled_time TIMESTAMP NOT NULL,
                posted_time TIMESTAMP,
                language TEXT NOT NULL,
                theme TEXT NOT NULL,
                tweet_id TEXT,
                engagement_metrics TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS engagements (
                id TEXT PRIMARY KEY,
                action_type TEXT NOT NULL,
                target_tweet_id TEXT NOT NULL,
                target_author TEXT NOT NULL,
                content TEXT,
                executed_at TIMESTAMP,
                success BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                posts_created INTEGER DEFAULT 0,
                posts_published INTEGER DEFAULT 0,
                engagements_made INTEGER DEFAULT 0,
                followers_gained INTEGER DEFAULT 0,
                total_reach INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    async def run_daily_automation(self):
        """Run the complete daily automation workflow"""
        
        self.logger.info("Starting daily automation workflow")
        
        try:
            # 1. Generate and schedule content for the day
            await self._generate_daily_content()
            
            # 2. Find and execute engagement opportunities
            await self._process_engagement_opportunities()
            
            # 3. Respond to mentions and replies
            await self._respond_to_mentions()
            
            # 4. Post scheduled content
            await self._post_scheduled_content()
            
            # 5. Update analytics
            await self._update_daily_analytics()
            
            self.logger.info("Daily automation workflow completed successfully")
            
        except Exception as e:
            self.logger.error(f"Error in daily automation: {e}")
    
    async def _generate_daily_content(self):
        """Generate content for posting throughout the day"""
        
        self.logger.info("Generating daily content")
        
        # Determine today's theme based on day of week
        today = datetime.now()
        theme = self._get_theme_for_day(today.weekday())
        
        # Generate content in multiple languages
        languages = [Language.ENGLISH, Language.SPANISH]
        
        posting_times = self._get_optimal_posting_times()
        
        for i, posting_time in enumerate(posting_times[:settings.posting_schedule]):
            # Alternate between languages
            language = languages[i % len(languages)]
            
            # Use different AI providers for variety
            provider_strategy = ProviderStrategy.BEST_FOR_CONTENT if i == 0 else ProviderStrategy.ROUND_ROBIN
            
            # Create content request
            content_request = ContentRequest(
                content_type=ContentType.TWEET,
                language=language.value,
                theme=theme.value,
                context={
                    "target_audience": "small business owners",
                    "focus": "practical business value",
                    "tone": "expert but conversational",
                    "include_cta": i == 0  # Call to action on first post
                },
                hashtags=sme_context.HASHTAGS["primary"]
            )
            
            # Generate content
            generated_content = await self.ai_manager.generate_content(
                content_request, 
                provider_strategy
            )
            
            # Schedule the post
            schedule_time = today.replace(
                hour=posting_time["hour"],
                minute=posting_time["minute"],
                second=0,
                microsecond=0
            )

            # Create Notion post
            notion_post = SocialMediaPost(
                name=f"SME Analytica - {theme.value.title()} {today.strftime('%Y-%m-%d')} #{i+1}",
                content=generated_content.text,
                status=PostStatus.SCHEDULED,
                platform=Platform.TWITTER,
                post_type=PostType.INFORMATIONAL,
                scheduled_time=schedule_time,
                language=language.value,
                content_theme=theme.value,
                ai_provider_used=generated_content.provider if hasattr(generated_content, 'provider') else None,
                tags=sme_context.HASHTAGS["primary"][:5]  # Limit to 5 tags
            )

            # Save to Notion database
            post_id = self.notion_manager.create_post(notion_post)
            if post_id:
                notion_post.notion_id = post_id
                self.logger.info(f"Scheduled post for {schedule_time}: {generated_content.text[:50]}...")
            else:
                self.logger.error(f"Failed to save post to Notion for {schedule_time}")

            # Also save to SQLite for backward compatibility
            post_schedule = PostSchedule(
                id=f"post_{today.strftime('%Y%m%d')}_{i}",
                content=generated_content.text,
                scheduled_time=schedule_time,
                language=language.value,
                theme=theme.value
            )
            self._save_scheduled_post(post_schedule)

    def _get_theme_for_day(self, day_of_week: int) -> ContentTheme:
        """Get content theme based on day of week"""
        
        theme_schedule = {
            0: ContentTheme.DATA_MONDAY,
            1: ContentTheme.TALK_TUESDAY,
            2: ContentTheme.CASE_WEDNESDAY,
            3: ContentTheme.TECH_THURSDAY,
            4: ContentTheme.FACT_FRIDAY,
            5: ContentTheme.WEEKEND_INSIGHTS,
            6: ContentTheme.WEEKEND_INSIGHTS
        }
        
        return theme_schedule.get(day_of_week, ContentTheme.DATA_MONDAY)
    
    def _get_optimal_posting_times(self) -> List[Dict[str, int]]:
        """Get optimal posting times based on audience analysis"""
        
        # Optimal times for SME audience (business hours + lunch + evening)
        return [
            {"hour": 9, "minute": 0},   # Morning business start
            {"hour": 13, "minute": 0},  # Lunch break
            {"hour": 17, "minute": 30}  # End of business day
        ]
    
    # Database helper methods
    def _save_scheduled_post(self, post: PostSchedule):
        """Save scheduled post to database"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO posts (id, content, scheduled_time, language, theme)
            VALUES (?, ?, ?, ?, ?)
        """, (
            post.id,
            post.content,
            post.scheduled_time.isoformat(),
            post.language,
            post.theme
        ))
        
        conn.commit()
        conn.close()

    async def _post_scheduled_content(self):
        """Post content that is scheduled and ready to publish"""

        self.logger.info("Checking for scheduled content to post")

        # Get ready-to-publish posts from Notion
        ready_posts = self.notion_manager.get_scheduled_posts()

        for post in ready_posts:
            try:
                # Post to Twitter directly with content
                tweet_id = await self.twitter_manager.post_tweet(post.content)

                if tweet_id:
                    published_time = datetime.now()

                    # Update post status in Notion
                    success = self.notion_manager.mark_as_published(
                        post.id,  # Use post.id instead of post.notion_id
                        tweet_id,
                        published_time
                    )

                    if success:
                        self.logger.info(f"Successfully posted and updated: {tweet_id}")
                        self.daily_post_count += 1
                    else:
                        self.logger.error(f"Posted tweet {tweet_id} but failed to update Notion")
                else:
                    self.logger.error(f"Failed to post tweet: {post.content[:50]}...")

            except Exception as e:
                self.logger.error(f"Error posting scheduled content: {e}")

    async def _process_engagement_opportunities(self):
        """Find and process engagement opportunities"""
        # This method would implement engagement logic
        # For now, just log that it's being processed
        self.logger.info("Processing engagement opportunities")
        pass

    async def _respond_to_mentions(self):
        """Respond to mentions and replies"""
        # This method would implement mention response logic
        # For now, just log that it's being processed
        self.logger.info("Processing mentions and replies")
        pass

    async def _update_daily_analytics(self):
        """Update daily analytics"""
        # This method would implement analytics updates
        # For now, just log that it's being processed
        self.logger.info("Updating daily analytics")
        pass

    async def test_system(self) -> Dict[str, Any]:
        """Test all system components"""

        results = {
            "ai_providers": await self.ai_manager.test_providers(),
            "twitter_connection": False,
            "notion_database": False,
            "sqlite_database": False,
            "content_generation": False
        }
        
        # Test Twitter connection
        try:
            account_info = await self.twitter_manager.get_account_metrics()
            results["twitter_connection"] = bool(account_info)
        except Exception as e:
            self.logger.error(f"Twitter test failed: {e}")
        
        # Test Notion database
        try:
            # Try to get posts from Notion
            posts = self.notion_manager.get_posts_by_status("Draft", limit=1)
            results["notion_database"] = True
            self.logger.info("Notion database connection successful")
        except Exception as e:
            self.logger.error(f"Notion database test failed: {e}")

        # Test SQLite database
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM posts")
            conn.close()
            results["sqlite_database"] = True
        except Exception as e:
            self.logger.error(f"SQLite database test failed: {e}")
        
        # Test content generation
        try:
            content = self.content_generator.generate_themed_content(
                ContentTheme.DATA_MONDAY, 
                Language.ENGLISH
            )
            results["content_generation"] = bool(content["text"])
        except Exception as e:
            self.logger.error(f"Content generation test failed: {e}")
        
        return results
