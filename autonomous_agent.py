#!/usr/bin/env python3
"""
🤖 SME Analytica Autonomous Social Media Agent
24/7 Intelligent Agent for Twitter (X) and LinkedIn Growth

Features:
- Autonomous @smeanalytica mention monitoring and responses
- Grok/Perplexity integration for intelligent replies
- Viral content generation and posting
- Real-time engagement automation
- AI-powered growth optimization
"""

import asyncio
import logging
import os
import sys
from datetime import datetime, timedelta
import signal
import json

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.ai_agent.intelligent_engagement_agent import IntelligentEngagementAgent
from src.social_media_manager import SocialMediaManager
from src.content.collaborative_content_generator import CollaborativeContentGenerator, ContentCategory
from src.ai_providers import AIProviderManager
from src.notion.notion_manager import NotionManager
from config.settings import sme_context

class AutonomousSocialAgent:
    """Fully autonomous social media agent for SME Analytica"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        
        # Initialize core components
        self.engagement_agent = None
        self.content_manager = None
        self.ai_provider = None
        
        # Agent state
        self.is_running = False
        self.start_time = None
        self.daily_stats = {
            "posts_created": 0,
            "posts_published": 0,
            "mentions_responded": 0,
            "engagements_made": 0,
            "viral_score_total": 0,
            "grok_interactions": 0
        }
        
        # Configuration
        self.config = {
            "posting_schedule": {
                "morning": {"time": "08:00", "timezone": "Europe/Madrid"},
                "afternoon": {"time": "13:00", "timezone": "Europe/Madrid"},
                "evening": {"time": "18:00", "timezone": "Europe/Madrid"},
                "night": {"time": "21:00", "timezone": "Europe/Madrid"}
            },
            "engagement_limits": {
                "max_daily_posts": 12,
                "max_mention_responses": 25,
                "max_hourly_engagements": 8
            },
            "viral_thresholds": {
                "minimum_viral_score": 7.5,
                "trending_hashtag_boost": 2.0,
                "optimal_length": 180
            }
        }
        
    def setup_logging(self):
        """Setup comprehensive logging for autonomous agent"""
        os.makedirs('logs', exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/autonomous_agent.log'),
                logging.StreamHandler()
            ]
        )
        
        # Reduce noise from external libraries
        logging.getLogger('httpx').setLevel(logging.WARNING)
        logging.getLogger('tweepy').setLevel(logging.WARNING)
        
    async def initialize(self):
        """Initialize all agent components"""
        try:
            self.logger.info("🚀 Initializing SME Analytica Autonomous Agent...")
            
            # Initialize AI providers
            ai_config = {
                "google_gemini_api_key": os.getenv("GOOGLE_GEMINI_API_KEY"),
                "openai_api_key": os.getenv("OPENAI_API_KEY"),
                "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
                "grok_api_key": os.getenv("GROK_API_KEY"),
                "perplexity_api_key": os.getenv("PERPLEXITY_API_KEY")
            }
            
            self.ai_provider = AIProviderManager(ai_config)
            
            # Initialize engagement agent for mentions and responses
            from src.ai_agent.intelligent_engagement_agent import create_intelligent_agent
            self.engagement_agent = await create_intelligent_agent()
            
            # Initialize content manager for viral content
            from src.notion.notion_manager import NotionManager
            notion_manager = NotionManager()
            self.content_manager = CollaborativeContentGenerator(self.ai_provider, notion_manager)
            
            self.logger.info("✅ All components initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize agent: {e}")
            return False
    
    async def start_autonomous_operation(self):
        """Start 24/7 autonomous operation"""
        self.logger.info("🤖 Starting 24/7 Autonomous Social Media Operation...")
        self.is_running = True
        self.start_time = datetime.now()
        
        # Setup graceful shutdown
        signal.signal(signal.SIGINT, self._graceful_shutdown)
        signal.signal(signal.SIGTERM, self._graceful_shutdown)
        
        # Start all autonomous tasks
        tasks = [
            self._daily_content_scheduler(),
            self._mention_monitoring_loop(),
            self._grok_integration_loop(),
            self._viral_content_optimizer(),
            self._engagement_automation(),
            self._analytics_reporter()
        ]
        
        try:
            await asyncio.gather(*tasks)
        except Exception as e:
            self.logger.error(f"🚨 Autonomous operation error: {e}")
        finally:
            await self._shutdown()
    
    async def _daily_content_scheduler(self):
        """Schedule and post viral content 4x daily"""
        while self.is_running:
            try:
                current_time = datetime.now()
                
                # Check if it's time to post
                if self._should_post_now(current_time):
                    await self._create_and_post_viral_content()
                    await asyncio.sleep(3600)  # Wait 1 hour between posts
                
                await asyncio.sleep(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"Daily scheduler error: {e}")
                await asyncio.sleep(300)
    
    async def _mention_monitoring_loop(self):
        """Continuous 24/7 monitoring for @smeanalytica mentions"""
        while self.is_running:
            try:
                # Check for mentions every 2 minutes
                mentions = await self._check_mentions()
                
                for mention in mentions:
                    await self._respond_to_mention(mention)
                
                await asyncio.sleep(120)  # 2-minute intervals
                
            except Exception as e:
                self.logger.error(f"Mention monitoring error: {e}")
                await asyncio.sleep(60)
    
    async def _grok_integration_loop(self):
        """Monitor and engage with Grok/Perplexity AI discussions"""
        while self.is_running:
            try:
                # Monitor AI-related discussions
                ai_discussions = await self._find_ai_discussions()
                
                for discussion in ai_discussions:
                    await self._engage_ai_discussion(discussion)
                
                await asyncio.sleep(1800)  # Check every 30 minutes
                
            except Exception as e:
                self.logger.error(f"Grok integration error: {e}")
                await asyncio.sleep(600)
    
    async def _viral_content_optimizer(self):
        """Optimize content for maximum viral potential"""
        while self.is_running:
            try:
                # Analyze trending topics every 15 minutes
                trending_data = await self._analyze_trending_topics()
                
                if trending_data:
                    await self._optimize_content_for_trends(trending_data)
                
                await asyncio.sleep(900)  # 15-minute intervals
                
            except Exception as e:
                self.logger.error(f"Viral optimizer error: {e}")
                await asyncio.sleep(300)
    
    async def _engagement_automation(self):
        """Automated engagement with target accounts"""
        while self.is_running:
            try:
                # Engage with restaurant owners and industry leaders
                target_accounts = await self._identify_target_accounts()
                
                for account in target_accounts[:5]:  # Max 5 per hour
                    await self._strategic_engagement(account)
                
                await asyncio.sleep(3600)  # Hourly engagement
                
            except Exception as e:
                self.logger.error(f"Engagement automation error: {e}")
                await asyncio.sleep(600)
    
    async def _analytics_reporter(self):
        """Report analytics every 6 hours"""
        while self.is_running:
            try:
                await asyncio.sleep(21600)  # 6 hours
                await self._generate_analytics_report()
                
            except Exception as e:
                self.logger.error(f"Analytics reporter error: {e}")
                await asyncio.sleep(3600)
    
    async def _create_and_post_viral_content(self):
        """Create and post viral content using AI Council"""
        try:
            self.logger.info("📝 Creating viral content...")
            
            # Generate multiple content types
            content_categories = [
                ContentCategory.VIRAL_HOOKS,
                ContentCategory.DATA_INSIGHTS,
                ContentCategory.SUCCESS_STORIES,
                ContentCategory.THOUGHT_LEADERSHIP
            ]
            
            best_content = None
            best_score = 0
            
            for category in content_categories:
                try:
                    content = await self.content_manager.generate_collaborative_content(category)
                    if content.final_score > best_score:
                        best_content = content
                        best_score = content.final_score
                except Exception as e:
                    self.logger.warning(f"Content generation failed for {category}: {e}")
            
            if best_content and best_score >= self.config["viral_thresholds"]["minimum_viral_score"]:
                # Post to both Twitter and LinkedIn
                success = await self._post_to_platforms(best_content)
                if success:
                    self.daily_stats["posts_published"] += 1
                    self.daily_stats["viral_score_total"] += best_score
                    self.logger.info(f"✅ Posted viral content (score: {best_score}/10)")
            
        except Exception as e:
            self.logger.error(f"Viral content creation error: {e}")
    
    async def _check_mentions(self):
        """Check for @smeanalytica mentions"""
        try:
            # This would use Twitter API to check mentions
            # For now, using the engagement agent's monitoring
            if hasattr(self.engagement_agent, 'twitter_manager'):
                mentions = await self.engagement_agent.twitter_manager.get_mentions(
                    since_time=datetime.now() - timedelta(minutes=5)
                )
                return mentions
            return []
        except Exception as e:
            self.logger.error(f"Mention check error: {e}")
            return []
    
    async def _respond_to_mention(self, mention):
        """Generate intelligent response to mentions"""
        try:
            # Use AI Council to generate contextual response
            response_context = {
                "original_content": mention.get('text', ''),
                "author": mention.get('author', ''),
                "mention_type": mention.get('type', ''),
                "urgency": self._calculate_mention_urgency(mention)
            }
            
            # Generate response using collaborative AI
            response = await self._generate_mention_response(response_context)
            
            if response:
                success = await self._post_response(response, mention)
                if success:
                    self.daily_stats["mentions_responded"] += 1
                    self.logger.info(f"💬 Responded to mention from @{mention.get('author', 'unknown')}")
            
        except Exception as e:
            self.logger.error(f"Mention response error: {e}")
    
    async def _find_ai_discussions(self):
        """Find discussions about AI, Grok, Perplexity"""
        try:
            search_queries = [
                "grok restaurant analytics",
                "perplexity business intelligence",
                "ai restaurant pricing",
                "grok vs chatgpt restaurant",
                "ai menu optimization"
            ]
            
            discussions = []
            for query in search_queries:
                # Search Twitter for relevant discussions
                if hasattr(self.engagement_agent, 'twitter_manager'):
                    tweets = await self.engagement_agent.twitter_manager.search_tweets(
                        query=query, max_results=10
                    )
                    discussions.extend(tweets)
            
            return discussions[:5]  # Limit to top 5
            
        except Exception as e:
            self.logger.error(f"AI discussion finding error: {e}")
            return []
    
    async def _engage_ai_discussion(self, discussion):
        """Engage with AI-related discussions strategically"""
        try:
            # Generate insightful response about AI in restaurants
            response = await self._generate_ai_insight_response(discussion)
            
            if response:
                success = await self._post_response(response, discussion)
                if success:
                    self.daily_stats["grok_interactions"] += 1
                    self.logger.info("🤖 Engaged with AI discussion")
            
        except Exception as e:
            self.logger.error(f"AI discussion engagement error: {e}")
    
    async def _analyze_trending_topics(self):
        """Analyze trending topics for content optimization"""
        try:
            # Get trending hashtags and topics
            trending_topics = await self._get_trending_data()
            
            # Analyze relevance to restaurant industry
            relevant_trends = []
            for topic in trending_topics:
                if self._is_relevant_to_restaurants(topic):
                    relevant_trends.append(topic)
            
            return relevant_trends[:3]
            
        except Exception as e:
            self.logger.error(f"Trending analysis error: {e}")
            return []
    
    async def _post_to_platforms(self, content):
        """Post content to both Twitter and LinkedIn"""
        try:
            # Post to Twitter
            twitter_success = await self._post_to_twitter(content)
            
            # Post to LinkedIn (adapted format)
            linkedin_success = await self._post_to_linkedin(content)
            
            return twitter_success or linkedin_success
            
        except Exception as e:
            self.logger.error(f"Multi-platform posting error: {e}")
            return False
    
    # Utility methods
    def _should_post_now(self, current_time):
        """Determine if it's optimal posting time"""
        schedule = self.config["posting_schedule"]
        current_hour = current_time.hour
        
        optimal_hours = [8, 13, 18, 21]  # Madrid timezone
        return current_hour in optimal_hours
    
    def _calculate_mention_urgency(self, mention):
        """Calculate urgency score for mention responses"""
        urgency_indicators = ['urgent', 'help', 'question', 'asap']
        text = mention.get('text', '').lower()
        
        score = 5  # Base urgency
        for indicator in urgency_indicators:
            if indicator in text:
                score += 2
        
        return min(score, 10)
    
    async def _generate_mention_response(self, context):
        """Generate contextual response to mentions"""
        try:
            prompt = f"""
            Generate a helpful, expert response to this mention about SME Analytica:
            
            Original mention: {context['original_content']}
            Author: {context['author']}
            Urgency: {context['urgency']}/10
            
            Be helpful, provide value, and naturally position SME Analytica as the expert in restaurant analytics.
            Include relevant data points and offer to help further.
            Keep under 280 characters for Twitter.
            """
            
            response = await self.ai_provider.generate_content(prompt)
            return response
            
        except Exception as e:
            self.logger.error(f"Mention response generation error: {e}")
            return None
    
    async def _generate_ai_insight_response(self, discussion):
        """Generate insightful response about AI in restaurants"""
        try:
            prompt = f"""
            Generate an insightful response to this AI discussion that positions SME Analytica as the expert:
            
            Discussion: {discussion.get('text', '')}
            
            Include specific insights about AI in restaurant operations, mention MenuFlow capabilities,
            and provide value. Keep professional but engaging.
            """
            
            response = await self.ai_provider.generate_content(prompt)
            return response
            
        except Exception as e:
            self.logger.error(f"AI insight generation error: {e}")
            return None
    
    async def _identify_target_accounts(self):
        """Identify high-value target accounts for engagement"""
        try:
            # Search for restaurant owners, industry leaders
            target_keywords = [
                "restaurant owner",
                "hospitality manager", 
                "small business owner",
                "food service director"
            ]
            
            accounts = []
            for keyword in target_keywords:
                # Find accounts to engage with
                found_accounts = await self._search_target_accounts(keyword)
                accounts.extend(found_accounts)
            
            return accounts[:10]  # Top 10 per cycle
            
        except Exception as e:
            self.logger.error(f"Target account identification error: {e}")
            return []
    
    async def _generate_analytics_report(self):
        """Generate comprehensive analytics report"""
        try:
            runtime = datetime.now() - self.start_time
            
            report = {
                "timestamp": datetime.now().isoformat(),
                "runtime": str(runtime),
                "daily_stats": self.daily_stats,
                "growth_metrics": {
                    "estimated_reach": self.daily_stats["posts_published"] * 100,
                    "engagement_rate": (self.daily_stats["engagements_made"] / max(self.daily_stats["posts_published"], 1)) * 100
                },
                "ai_performance": {
                    "viral_content_score": self.daily_stats["viral_score_total"] / max(self.daily_stats["posts_published"], 1),
                    "mention_response_rate": self.daily_stats["mentions_responded"]
                }
            }
            
            # Save to file and Notion
            await self._save_analytics(report)
            
            self.logger.info(f"📊 Analytics report generated: {json.dumps(report, indent=2)}")
            
        except Exception as e:
            self.logger.error(f"Analytics generation error: {e}")
    
    def _graceful_shutdown(self, signum, frame):
        """Handle graceful shutdown"""
        self.logger.info("🛑 Received shutdown signal, stopping gracefully...")
        self.is_running = False
    
    async def _shutdown(self):
        """Cleanup and shutdown"""
        self.logger.info("🧹 Shutting down autonomous agent...")
        
        # Generate final report
        await self._generate_analytics_report()
        
        # Save final state
        await self._save_final_state()
        
        self.logger.info("✅ Autonomous agent shutdown complete")
    
    # Placeholder methods for Twitter/LinkedIn API calls
    async def _post_to_twitter(self, content):
        """Post to Twitter (placeholder)"""
        # Implement actual Twitter posting
        return True
    
    async def _post_to_linkedin(self, content):
        """Post to LinkedIn (placeholder)"""
        # Implement actual LinkedIn posting  
        return True
    
    async def _get_trending_data(self):
        """Get trending topics (placeholder)"""
        return ["#RestaurantTech", "#AIFood", "#DigitalMenu"]
    
    def _is_relevant_to_restaurants(self, topic):
        """Check if trending topic is restaurant-relevant"""
        restaurant_keywords = ["restaurant", "food", "menu", "hospitality", "dining"]
        return any(keyword in topic.lower() for keyword in restaurant_keywords)
    
    async def _search_target_accounts(self, keyword):
        """Search for target accounts (placeholder)"""
        return [{"username": f"restaurant_owner_{i}", "followers": 1000+i} for i in range(3)]
    
    async def _save_analytics(self, report):
        """Save analytics (placeholder)"""
        with open('logs/analytics.json', 'w') as f:
            json.dump(report, f, indent=2)
    
    async def _save_final_state(self):
        """Save final agent state"""
        state = {
            "shutdown_time": datetime.now().isoformat(),
            "final_stats": self.daily_stats
        }
        with open('logs/final_state.json', 'w') as f:
            json.dump(state, f, indent=2)

async def main():
    """Main entry point for autonomous agent"""
    print("🤖 SME Analytica Autonomous Social Media Agent")
    print("=" * 50)
    print("Starting 24/7 intelligent social media operation...")
    print("- Monitoring @smeanalytica mentions")
    print("- Creating viral content")
    print("- Engaging with AI discussions")
    print("- Optimizing for growth")
    print("=" * 50)
    
    agent = AutonomousSocialAgent()
    
    # Initialize agent
    if await agent.initialize():
        # Start autonomous operation
        await agent.start_autonomous_operation()
    else:
        print("❌ Failed to initialize agent. Check API keys and configuration.")

if __name__ == "__main__":
    asyncio.run(main())