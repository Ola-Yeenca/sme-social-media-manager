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
from content.growth_content_generator import GrowthOptimizedContentGenerator, ContentTheme, Language, GrowthStrategy
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
        self.content_generator = GrowthOptimizedContentGenerator()
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
            
            # Use AI for dynamic content generation with viral optimization
            growth_strategy = GrowthStrategy.VIRAL_POTENTIAL if i == 0 else GrowthStrategy.ENGAGEMENT_BOOST

            # Get viral optimization insights from our growth generator
            viral_insights = self.content_generator.generate_viral_optimized_content(
                theme=theme,
                growth_strategy=growth_strategy,
                language=language
            )

            # Create diverse context for each post to force variety
            import random

            content_angles = [
                # MenuFlow Feature Stories
                "collaborative_ordering_breakthrough", "qr_code_revolution", "ai_recommendation_success",
                "multilingual_expansion", "kitchen_integration_win", "bill_splitting_magic",
                "real_time_sync_power", "zero_wait_achievement", "order_accuracy_perfection",
                "table_turnover_optimization", "staff_efficiency_boost", "customer_satisfaction_surge",

                # Business Transformation Angles
                "digital_transformation", "operational_excellence", "revenue_optimization",
                "customer_experience_revolution", "technology_integration", "competitive_advantage",
                "scalability_success", "efficiency_breakthrough", "profit_maximization",

                # Industry Insights
                "restaurant_tech_evolution", "future_of_dining", "pos_integration_mastery",
                "analytics_driven_decisions", "predictive_intelligence", "automation_benefits",
                "mobile_first_strategy", "contactless_dining_trend", "data_driven_growth",

                # Problem-Solution Stories
                "chaos_to_order", "confusion_to_clarity", "manual_to_automated",
                "slow_to_instant", "error_prone_to_perfect", "complex_to_simple"
            ]

            restaurant_scenarios = [
                # MenuFlow Success Stories with Real Features
                {"name": "Bistro Verde", "challenge": "40% slower table turnover during lunch rush", "insight": "MenuFlow's collaborative ordering cut wait times", "result": "40% faster table turnover", "feature": "QR code instant ordering"},
                {"name": "Café Luna", "challenge": "customers confused by multilingual menu", "insight": "automatic language detection and translation", "result": "90% customer satisfaction boost", "feature": "real-time menu translation"},
                {"name": "Restaurant Bella Vista", "challenge": "25% revenue loss from order errors", "insight": "digital ordering eliminated miscommunication", "result": "60% reduction in order errors", "feature": "collaborative cart system"},
                {"name": "The Corner Deli", "challenge": "staff overwhelmed taking group orders", "insight": "customers self-order via shared cart", "result": "staff efficiency increased 3x", "feature": "real-time group ordering"},
                {"name": "Local Tapas Bar", "challenge": "losing customers who couldn't split bills", "insight": "automatic bill splitting by person", "result": "25% increase in group dining", "feature": "smart bill splitting"},

                # AI-Powered Optimization Stories
                {"name": "Harvest Kitchen", "challenge": "unpredictable daily revenue swings", "insight": "AI recommendations boosted average orders", "result": "25% increase in average order value", "feature": "AI-powered menu recommendations"},
                {"name": "Urban Spoon", "challenge": "popular items running out early", "insight": "demand prediction and inventory alerts", "result": "eliminated stockouts completely", "feature": "inventory prediction system"},
                {"name": "The Daily Grind", "challenge": "morning rush creating 15-min waits", "insight": "pre-ordering and table status tracking", "result": "zero wait time for menu access", "feature": "instant QR code access"},
                {"name": "Fusion Table", "challenge": "couldn't identify profitable menu items", "insight": "real-time analytics on dish performance", "result": "identified top 20% profit drivers", "feature": "performance analytics dashboard"},
                {"name": "Artisan Eatery", "challenge": "customers leaving due to language barriers", "insight": "browser language auto-detection", "result": "expanded to 5 language markets", "feature": "multilingual accessibility"},

                # Operational Excellence Stories
                {"name": "Sakura Sushi", "challenge": "kitchen overwhelmed with complex orders", "insight": "digital orders flow directly to kitchen displays", "result": "streamlined kitchen operations", "feature": "kitchen integration system"},
                {"name": "Mama Rosa's", "challenge": "large families struggled to coordinate orders", "insight": "real-time collaborative ordering for groups", "result": "became family dining destination", "feature": "seamless group ordering"},
                {"name": "El Corazón", "challenge": "happy hour pricing changes caused confusion", "insight": "dynamic pricing updates in real-time", "result": "optimized happy hour revenue", "feature": "dynamic pricing engine"},
                {"name": "Bangkok Street", "challenge": "customers couldn't communicate spice preferences", "insight": "detailed customization options in app", "result": "perfect spice levels every time", "feature": "customization interface"},
                {"name": "Le Petit Café", "challenge": "breakfast crowd left due to slow service", "insight": "sub-second menu loading and ordering", "result": "captured morning rush market", "feature": "instant menu loading"},

                # Technology Integration Success
                {"name": "Burger Junction", "challenge": "POS system couldn't handle digital orders", "insight": "seamless integration with existing POS", "result": "unified order management", "feature": "POS system integration"},
                {"name": "Pizza Corner", "challenge": "complex topping orders led to mistakes", "insight": "visual order confirmation system", "result": "100% order accuracy", "feature": "order verification system"},
                {"name": "Sandwich Co.", "challenge": "peak lunch hour chaos", "insight": "real-time order status tracking", "result": "organized lunch service", "feature": "order tracking system"},
                {"name": "Taco Libre", "challenge": "couldn't track customer preferences", "insight": "AI learning from order patterns", "result": "personalized recommendations", "feature": "AI recommendation engine"},
                {"name": "Noodle House", "challenge": "seasonal menu changes were manual nightmare", "insight": "one-click menu updates across all tables", "result": "instant seasonal transitions", "feature": "real-time menu management"},

                # Enterprise Analytics Success
                {"name": "The Golden Fork", "challenge": "no visibility into customer behavior", "insight": "comprehensive analytics dashboard", "result": "data-driven menu optimization", "feature": "business intelligence suite"},
                {"name": "Meridian Restaurant", "challenge": "couldn't predict busy periods", "insight": "traffic heatmap and pattern analysis", "result": "perfect staff scheduling", "feature": "predictive analytics"},
                {"name": "Chef's Table", "challenge": "premium items weren't selling", "insight": "AI-suggested upselling at optimal moments", "result": "doubled premium item sales", "feature": "intelligent upselling"},
                {"name": "The Copper Pot", "challenge": "lost revenue from no-shows", "insight": "reservation integration with ordering system", "result": "reduced no-shows by 30%", "feature": "reservation management"},
                {"name": "Starlight Bistro", "challenge": "customers skipping dessert", "insight": "strategic dessert recommendations during meal", "result": "dessert sales up 40%", "feature": "contextual recommendations"}
            ]

            data_insights = [
                # MenuFlow Proven Results
                "MenuFlow delivers 40% faster table turnover through streamlined digital ordering",
                "AI recommendations increase average order value by 25% automatically",
                "Digital ordering reduces order errors by 60% compared to traditional methods",
                "Collaborative ordering enables seamless group dining for 4+ people",
                "Sub-second menu loading eliminates customer wait times completely",
                "Real-time synchronization keeps all devices updated instantly",
                "Automatic bill splitting increases group dining revenue by 25%",
                "99.9% uptime ensures ordering system never fails during service",
                "Zero app downloads required - works instantly via QR code scanning",
                "Multilingual menus expand customer base to international diners",

                # Restaurant Operations Insights
                "QR code ordering eliminates need for servers to take orders manually",
                "Kitchen integration displays orders directly on kitchen screens",
                "Real-time inventory tracking prevents stockouts during peak hours",
                "Dynamic pricing adjusts automatically based on demand patterns",
                "Staff efficiency increases 3x when customers self-order digitally",
                "Order accuracy reaches 100% with digital confirmation systems",
                "Peak hour chaos disappears with organized digital order queues",
                "Table status tracking optimizes seating and turnover rates",
                "Predictive analytics enable perfect staff scheduling decisions",
                "One-click menu updates instantly change pricing across all tables",

                # Customer Experience Metrics
                "90% customer satisfaction achieved with digital ordering experience",
                "Group ordering coordination hassles eliminated completely",
                "Language barriers removed with automatic translation features",
                "Order tracking provides real-time status updates to customers",
                "Special dietary requests handled perfectly through digital customization",
                "Payment processing becomes seamless with integrated systems",
                "Customer feedback collection improves service quality continuously",
                "Personalized recommendations learn from individual preferences",
                "Mobile-first design works perfectly on any smartphone",
                "Accessibility features serve customers with diverse needs"
            ]

            scenario = random.choice(restaurant_scenarios)
            angle = random.choice(content_angles)
            insight = random.choice(data_insights)

            # Enhance the AI prompt with diverse, randomized context
            enhanced_context = {
                **content_request.context,
                "content_angle": angle,
                "restaurant_name": scenario["name"],
                "business_challenge": scenario["challenge"],
                "key_insight": scenario["insight"],
                "surprising_statistic": insight,
                "post_number": i + 1,  # Help AI understand this is post X of the day
                "uniqueness_requirement": f"This is post #{i+1} today - make it completely different from previous posts"
            }

            # Update content request with enhanced context
            content_request.context = enhanced_context

            # Generate content using AI with viral optimization
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
            content = self.content_generator.generate_viral_optimized_content(
                ContentTheme.DATA_MONDAY,
                GrowthStrategy.VIRAL_POTENTIAL,
                Language.ENGLISH
            )
            results["content_generation"] = bool(content["text"])
        except Exception as e:
            self.logger.error(f"Content generation test failed: {e}")
        
        return results
