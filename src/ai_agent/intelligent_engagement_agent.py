#!/usr/bin/env python3
"""
Intelligent AI Engagement Agent for SME Analytica
Continuously monitors, analyzes, and responds to engagement opportunities
"""

import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import random
import re

from ..social.twitter_manager import TwitterManager
from ..notion.notion_manager import NotionManager
from ..ai_providers import AIProviderManager, ContentRequest, ContentType
from ..engagement.engagement_automation import EngagementAutomation
from .hashtag_tracker import IntelligentHashtagTracker
from .response_generator import IntelligentResponseGenerator, ResponseContext
from .engagement_strategy_engine import EngagementStrategyEngine, EngagementStrategy
from .safety_manager import SafetyManager
from ..ai_council import AICouncilManager, VoteType
from config.settings import sme_context

class AgentMode(str, Enum):
    MONITORING = "monitoring"
    ANALYZING = "analyzing"
    RESPONDING = "responding"
    LEARNING = "learning"

class OpportunityType(str, Enum):
    MENTION = "mention"
    HASHTAG_MATCH = "hashtag_match"
    INDUSTRY_CONVERSATION = "industry_conversation"
    COMPETITOR_ACTIVITY = "competitor_activity"
    PROSPECT_SIGNAL = "prospect_signal"
    TREND_OPPORTUNITY = "trend_opportunity"

@dataclass
class EngagementContext:
    """Rich context for AI-powered engagement decisions"""
    opportunity_type: OpportunityType
    content: str
    author: str
    author_profile: Dict[str, Any]
    conversation_thread: List[Dict[str, Any]]
    industry_relevance: float
    urgency_score: float
    conversion_potential: float
    brand_alignment: float
    competitive_context: Optional[str] = None
    trending_context: Optional[str] = None

@dataclass
class AIResponse:
    """AI-generated response with metadata"""
    content: str
    confidence_score: float
    response_type: str  # reply, quote_tweet, retweet_comment
    reasoning: str
    safety_score: float
    brand_voice_score: float

class IntelligentEngagementAgent:
    """AI-powered engagement agent with continuous monitoring and intelligent responses"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)

        # Initialize Twitter manager with credentials
        import os
        twitter_credentials = {
            "api_key": os.getenv("TWITTER_API_KEY"),
            "api_secret": os.getenv("TWITTER_API_SECRET"),
            "access_token": os.getenv("TWITTER_ACCESS_TOKEN"),
            "access_token_secret": os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
            "bearer_token": os.getenv("TWITTER_BEARER_TOKEN")
        }

        # Validate Twitter credentials
        if not all(twitter_credentials.values()):
            raise ValueError("Missing Twitter API credentials. Please check your environment variables.")

        self.twitter_manager = TwitterManager(twitter_credentials)
        self.notion_manager = NotionManager()

        # Initialize AI provider manager with Gemini support
        ai_config = {
            "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
            "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY", ""),
            "perplexity_api_key": os.getenv("PERPLEXITY_API_KEY", ""),
            "grok_api_key": os.getenv("GROK_API_KEY", ""),
            "google_gemini_api_key": os.getenv("GOOGLE_GEMINI_API_KEY", "")
        }
        self.ai_provider = AIProviderManager(ai_config)

        self.hashtag_tracker = IntelligentHashtagTracker(self.twitter_manager, self.ai_provider)
        self.response_generator = IntelligentResponseGenerator(self.ai_provider)
        self.strategy_engine = EngagementStrategyEngine()
        self.safety_manager = SafetyManager()
        self.ai_council = AICouncilManager(self.ai_provider)
        
        # Agent state
        self.is_running = False
        self.current_mode = AgentMode.MONITORING
        self.last_check_time = datetime.now()
        
        # Configuration
        self.monitoring_config = self._initialize_monitoring_config()
        self.response_templates = self._initialize_response_templates()
        self.safety_filters = self._initialize_safety_filters()
        self.brand_voice_guidelines = self._initialize_brand_voice()
        
        # Analytics
        self.session_stats = {
            "opportunities_found": 0,
            "responses_generated": 0,
            "engagements_executed": 0,
            "safety_blocks": 0,
            "start_time": datetime.now()
        }

    def _initialize_monitoring_config(self) -> Dict[str, Any]:
        """Initialize monitoring configuration"""
        return {
            "hashtags": {
                "primary": [
                    "#RestaurantTech", "#SMEAnalytics", "#MenuOptimization", 
                    "#RestaurantData", "#HospitalityAI", "#DynamicPricing",
                    "#POSIntegration", "#RestaurantAnalytics", "#MenuFlow"
                ],
                "secondary": [
                    "#SmallBusiness", "#BusinessIntelligence", "#DataDriven",
                    "#RestaurantOwner", "#HotelTech", "#RetailAnalytics",
                    "#AIForBusiness", "#DigitalTransformation"
                ],
                "trending": [
                    "#AIRevolution", "#TechTrends", "#BusinessGrowth",
                    "#Innovation", "#StartupLife", "#Entrepreneurship"
                ]
            },
            "keywords": {
                "high_priority": [
                    "restaurant analytics", "dynamic pricing", "pos integration",
                    "menu optimization", "hospitality ai", "restaurant data"
                ],
                "medium_priority": [
                    "small business", "business intelligence", "data analytics",
                    "restaurant owner", "hotel management", "retail tech"
                ],
                "prospect_signals": [
                    "looking for", "need help", "recommendations", "advice",
                    "struggling with", "how to", "best practices", "solutions"
                ]
            },
            "monitoring_intervals": {
                "mentions": 900,   # 15 minutes (was 5 minutes)
                "hashtags": 1800,  # 30 minutes (was 10 minutes)
                "trends": 3600,    # 1 hour (was 30 minutes)
                "competitors": 7200 # 2 hours (was 1 hour)
            },
            "engagement_limits": {
                "hourly_responses": 5,
                "daily_responses": 25,
                "weekly_responses": 150
            }
        }

    def _initialize_response_templates(self) -> Dict[str, List[str]]:
        """Initialize AI response templates for different scenarios"""
        return {
            "helpful_expert": [
                "Great question! In our experience with 500+ restaurants, {insight}. Happy to share more insights if helpful! 📊",
                "This resonates with many restaurant owners we work with. {solution_hint}. Feel free to reach out if you'd like to discuss further! 🤝",
                "Excellent point! We've seen similar challenges across the hospitality industry. {data_insight}. Would love to share what we've learned! 💡"
            ],
            "thought_leadership": [
                "This trend is exactly what we're seeing in restaurant analytics! {industry_insight}. The data tells a compelling story about {trend}. 📈",
                "💯 This! Our research with SME restaurants shows {statistic}. The opportunity for optimization is massive with the right approach. 🚀",
                "Spot on analysis! At SME Analytica, we've documented similar patterns. {supporting_data}. The future is definitely data-driven! 🔥"
            ],
            "community_support": [
                "The restaurant community is incredible! We're always happy to share insights from our analytics work. {helpful_tip}. Keep pushing forward! 💪",
                "Love seeing restaurant owners support each other! If analytics insights would be helpful for your situation, we're here to help. {offer}. 🤝",
                "This is why the hospitality community is so strong! {encouraging_insight}. Data can definitely help with challenges like this. 📊"
            ],
            "prospect_engagement": [
                "This sounds like exactly the type of challenge MenuFlow helps solve! {specific_solution}. Would be happy to show you how it works. DM us! 📩",
                "We help restaurants tackle this exact issue! {value_proposition}. Our analytics platform has helped similar establishments {result}. Interested in learning more? 🎯",
                "Perfect timing! This is precisely what SME Analytica specializes in. {capability_highlight}. Free consultation available if you'd like to explore solutions! 💡"
            ]
        }

    def _initialize_safety_filters(self) -> Dict[str, List[str]]:
        """Initialize safety filters to prevent inappropriate engagement"""
        return {
            "avoid_topics": [
                "politics", "religion", "personal attacks", "controversial",
                "spam", "scam", "illegal", "harassment", "discrimination"
            ],
            "avoid_accounts": [
                "spam", "bot", "fake", "suspended", "private"
            ],
            "content_flags": [
                "offensive", "inappropriate", "misleading", "promotional spam"
            ],
            "minimum_thresholds": {
                "account_age_days": 30,
                "follower_count": 10,
                "engagement_rate": 0.01
            }
        }

    def _initialize_brand_voice(self) -> Dict[str, Any]:
        """Initialize SME Analytica brand voice guidelines"""
        return {
            "tone": "professional yet approachable",
            "personality": "data-driven expert, helpful mentor, industry thought leader",
            "values": ["authenticity", "helpfulness", "expertise", "community"],
            "avoid": ["overly promotional", "pushy sales", "jargon-heavy", "impersonal"],
            "signature_elements": [
                "data-driven insights", "specific statistics", "helpful offers",
                "community focus", "restaurant expertise", "AI/analytics authority"
            ],
            "emoji_style": "strategic and professional (📊📈🚀💡🎯🤝💪🔥)",
            "hashtag_strategy": "relevant industry tags, avoid hashtag spam"
        }

    async def start_monitoring(self) -> None:
        """Start continuous monitoring and engagement"""
        self.logger.info("🤖 Starting Intelligent Engagement Agent")
        self.is_running = True
        self.session_stats["start_time"] = datetime.now()
        
        # Add initial delay to prevent immediate rate limiting
        initial_delay = random.randint(30, 120)  # 30 seconds to 2 minutes
        self.logger.info(f"⏱️ Initial delay: {initial_delay} seconds to prevent rate limiting")
        await asyncio.sleep(initial_delay)
        
        # Start monitoring tasks with staggered starts
        monitoring_tasks = []
        
        # Start mentions monitoring immediately
        monitoring_tasks.append(self._monitor_mentions())
        
        # Stagger other monitoring tasks to spread API calls
        await asyncio.sleep(30)  # 30 second delay
        monitoring_tasks.append(self._monitor_industry_conversations())
        
        await asyncio.sleep(30)  # Another 30 second delay  
        monitoring_tasks.append(self._monitor_trends())
        
        await asyncio.sleep(30)  # Another 30 second delay
        monitoring_tasks.append(self.hashtag_tracker.start_hashtag_monitoring())
        
        await asyncio.sleep(30)  # Another 30 second delay
        monitoring_tasks.append(self._analytics_reporter())
        
        try:
            await asyncio.gather(*monitoring_tasks)
        except Exception as e:
            self.logger.error(f"Agent monitoring error: {e}")
        finally:
            self.is_running = False

    async def _monitor_mentions(self) -> None:
        """Continuously monitor mentions and replies with enhanced rate limiting"""
        consecutive_errors = 0
        max_consecutive_errors = 3
        
        while self.is_running:
            try:
                self.current_mode = AgentMode.MONITORING
                
                # Add jitter to prevent synchronized requests
                jitter = random.uniform(0, 60)  # 0-60 seconds jitter
                await asyncio.sleep(jitter)
                
                self.logger.info("🔍 Checking mentions and notifications...")
                
                # Get recent mentions and notifications with error handling
                notifications = []
                try:
                    notifications = await self.twitter_manager.get_notifications(
                        since_time=self.last_check_time,
                        max_results=15  # Reduced from 30 to be more conservative
                    )
                except Exception as api_error:
                    self.logger.warning(f"API error getting notifications: {api_error}")
                    # Don't break the loop, just continue with empty notifications
                    notifications = []
                
                # Process notifications if we got any
                if notifications:
                    self.logger.info(f"📨 Processing {len(notifications)} notifications")
                    for notification in notifications[:5]:  # Limit to 5 most recent
                        try:
                            # Convert notification to tweet format for context building
                            tweet_data = {
                                'id': notification['tweet'].id,
                                'text': notification['content'],
                                'author': {'username': notification['author']},
                                'created_at': notification['timestamp'],
                                'public_metrics': notification['tweet'].public_metrics
                            }

                            context = await self._build_engagement_context(
                                tweet_data, OpportunityType.MENTION
                            )

                            if await self._should_engage(context):
                                await self._process_engagement_opportunity(context)
                                
                            # Add delay between processing notifications
                            await asyncio.sleep(5)
                            
                        except Exception as process_error:
                            self.logger.error(f"Error processing notification: {process_error}")
                            continue
                else:
                    self.logger.info("📭 No new notifications")
                
                # Reset consecutive errors on successful cycle
                consecutive_errors = 0
                
                self.last_check_time = datetime.now()
                
                # Use the configured interval with some jitter
                interval = self.monitoring_config["monitoring_intervals"]["mentions"]
                sleep_time = interval + random.uniform(-60, 60)  # ±1 minute jitter
                self.logger.info(f"⏰ Next mention check in {sleep_time/60:.1f} minutes")
                await asyncio.sleep(sleep_time)
                
            except Exception as e:
                consecutive_errors += 1
                self.logger.error(f"Mention monitoring error ({consecutive_errors}/{max_consecutive_errors}): {e}")
                
                if consecutive_errors >= max_consecutive_errors:
                    self.logger.error("Max consecutive errors reached. Pausing mention monitoring for 30 minutes.")
                    await asyncio.sleep(1800)  # 30 minutes
                    consecutive_errors = 0
                else:
                    # Exponential backoff
                    backoff_time = min(300 * (2 ** consecutive_errors), 900)  # Max 15 minutes
                    self.logger.info(f"⏱️ Backing off for {backoff_time} seconds")
                    await asyncio.sleep(backoff_time)

    async def _process_hashtag_opportunities(self) -> None:
        """Process opportunities found by hashtag tracker"""
        while self.is_running:
            try:
                # Get high-value opportunities from hashtag tracker
                opportunities = self.hashtag_tracker.get_hashtag_opportunities(min_score=7.0)

                for opportunity in opportunities[-10:]:  # Process last 10 opportunities
                    # Convert hashtag opportunity to engagement context
                    tweet_data = {
                        'id': opportunity.tweet_id,
                        'text': opportunity.content,
                        'author': {'username': opportunity.author},
                        'created_at': opportunity.discovered_at
                    }

                    context = await self._build_engagement_context(
                        tweet_data, OpportunityType.HASHTAG_MATCH
                    )

                    if await self._should_engage(context):
                        await self._process_engagement_opportunity(context)

                await asyncio.sleep(600)  # Check every 10 minutes

            except Exception as e:
                self.logger.error(f"Hashtag opportunity processing error: {e}")
                await asyncio.sleep(300)

    async def _monitor_industry_conversations(self) -> None:
        """Monitor industry conversations and discussions with rate limiting"""
        consecutive_errors = 0
        max_consecutive_errors = 3
        
        while self.is_running:
            try:
                # Add jitter to prevent synchronized requests
                jitter = random.uniform(0, 120)  # 0-2 minutes jitter
                await asyncio.sleep(jitter)
                
                self.logger.info("🔍 Monitoring industry conversations...")
                
                # Reduced and more conservative queries
                industry_queries = [
                    "restaurant analytics -from:smeanalytica",
                    "menu optimization -from:smeanalytica"
                ]
                
                for i, query in enumerate(industry_queries):
                    try:
                        self.logger.info(f"🔎 Searching: {query}")
                        tweets = await self.twitter_manager.search_tweets(
                            query=query,
                            max_results=8  # Reduced from 15 to be more conservative
                        )
                        
                        if tweets:
                            self.logger.info(f"📊 Found {len(tweets)} industry tweets")
                            for tweet in tweets[:3]:  # Limit to 3 most relevant
                                try:
                                    context = await self._build_engagement_context(
                                        tweet, OpportunityType.INDUSTRY_CONVERSATION
                                    )
                                    
                                    if await self._should_engage(context):
                                        await self._process_engagement_opportunity(context)
                                        
                                    # Add delay between processing tweets
                                    await asyncio.sleep(10)
                                    
                                except Exception as tweet_error:
                                    self.logger.error(f"Error processing industry tweet: {tweet_error}")
                                    continue
                        else:
                            self.logger.info("📭 No industry conversations found")
                        
                        # Add delay between queries to prevent rapid API calls
                        if i < len(industry_queries) - 1:
                            await asyncio.sleep(60)  # 1 minute between queries
                            
                    except Exception as query_error:
                        self.logger.warning(f"Error with query '{query}': {query_error}")
                        continue
                
                # Reset consecutive errors on successful cycle
                consecutive_errors = 0
                
                # Use the configured interval with jitter
                interval = self.monitoring_config["monitoring_intervals"]["trends"]
                sleep_time = interval + random.uniform(-300, 300)  # ±5 minutes jitter
                self.logger.info(f"⏰ Next industry conversation check in {sleep_time/60:.1f} minutes")
                await asyncio.sleep(sleep_time)
                
            except Exception as e:
                consecutive_errors += 1
                self.logger.error(f"Industry conversation monitoring error ({consecutive_errors}/{max_consecutive_errors}): {e}")
                
                if consecutive_errors >= max_consecutive_errors:
                    self.logger.error("Max consecutive errors reached. Pausing industry monitoring for 1 hour.")
                    await asyncio.sleep(3600)  # 1 hour
                    consecutive_errors = 0
                else:
                    # Exponential backoff
                    backoff_time = min(600 * (2 ** consecutive_errors), 1800)  # Max 30 minutes
                    self.logger.info(f"⏱️ Backing off for {backoff_time} seconds")
                    await asyncio.sleep(backoff_time)

    async def _monitor_trends(self) -> None:
        """Monitor trending topics for engagement opportunities with rate limiting"""
        consecutive_errors = 0
        max_consecutive_errors = 3
        
        while self.is_running:
            try:
                # Add jitter to prevent synchronized requests
                jitter = random.uniform(0, 180)  # 0-3 minutes jitter
                await asyncio.sleep(jitter)
                
                self.logger.info("🔍 Monitoring trending topics...")
                
                # Get trending topics - reduced and more conservative
                trending_hashtags = self.monitoring_config["hashtags"]["trending"][:2]  # Only first 2
                
                for i, hashtag in enumerate(trending_hashtags):
                    try:
                        # More conservative search query
                        query = f"{hashtag} restaurant -from:smeanalytica"
                        self.logger.info(f"🔎 Searching trending: {query}")
                        
                        tweets = await self.twitter_manager.search_tweets(
                            query=query,
                            max_results=5  # Reduced from 10 to be more conservative
                        )
                        
                        if tweets:
                            self.logger.info(f"📈 Found {len(tweets)} trending tweets for {hashtag}")
                            for tweet in tweets[:2]:  # Limit to 2 most relevant
                                try:
                                    context = await self._build_engagement_context(
                                        tweet, OpportunityType.TREND_OPPORTUNITY
                                    )
                                    
                                    if await self._should_engage(context):
                                        await self._process_engagement_opportunity(context)
                                        
                                    # Add delay between processing tweets
                                    await asyncio.sleep(15)
                                    
                                except Exception as tweet_error:
                                    self.logger.error(f"Error processing trending tweet: {tweet_error}")
                                    continue
                        else:
                            self.logger.info(f"📭 No trending tweets found for {hashtag}")
                        
                        # Add delay between hashtag searches
                        if i < len(trending_hashtags) - 1:
                            await asyncio.sleep(120)  # 2 minutes between hashtags
                            
                    except Exception as hashtag_error:
                        self.logger.warning(f"Error with hashtag '{hashtag}': {hashtag_error}")
                        continue
                
                # Reset consecutive errors on successful cycle
                consecutive_errors = 0
                
                # Use the configured interval with jitter
                interval = self.monitoring_config["monitoring_intervals"]["trends"]
                sleep_time = interval + random.uniform(-600, 600)  # ±10 minutes jitter
                self.logger.info(f"⏰ Next trend check in {sleep_time/60:.1f} minutes")
                await asyncio.sleep(sleep_time)
                
            except Exception as e:
                consecutive_errors += 1
                self.logger.error(f"Trend monitoring error ({consecutive_errors}/{max_consecutive_errors}): {e}")
                
                if consecutive_errors >= max_consecutive_errors:
                    self.logger.error("Max consecutive errors reached. Pausing trend monitoring for 2 hours.")
                    await asyncio.sleep(7200)  # 2 hours
                    consecutive_errors = 0
                else:
                    # Exponential backoff
                    backoff_time = min(900 * (2 ** consecutive_errors), 3600)  # Max 1 hour
                    self.logger.info(f"⏱️ Backing off for {backoff_time} seconds")
                    await asyncio.sleep(backoff_time)

    async def _analytics_reporter(self) -> None:
        """Periodic analytics reporting"""
        while self.is_running:
            try:
                # Report analytics every hour
                await asyncio.sleep(3600)
                
                runtime = datetime.now() - self.session_stats["start_time"]
                self.logger.info(
                    f"🤖 Agent Runtime: {runtime} | "
                    f"Opportunities: {self.session_stats['opportunities_found']} | "
                    f"Responses: {self.session_stats['responses_generated']} | "
                    f"Engagements: {self.session_stats['engagements_executed']}"
                )
                
                # Save analytics to Notion
                await self._save_session_analytics()
                
            except Exception as e:
                self.logger.error(f"Analytics reporting error: {e}")

    async def _build_engagement_context(self, content_data: Dict[str, Any],
                                      opportunity_type: OpportunityType) -> EngagementContext:
        """Build rich context for AI engagement decisions"""

        # Extract basic information
        content = content_data.get('text', '')
        author = content_data.get('author', {}).get('username', '')

        # Get author profile information
        author_profile = await self._get_author_profile(author)

        # Get conversation thread if this is a reply
        conversation_thread = []
        if content_data.get('in_reply_to_tweet_id'):
            conversation_thread = await self._get_conversation_thread(
                content_data['in_reply_to_tweet_id']
            )

        # Calculate relevance scores
        industry_relevance = self._calculate_industry_relevance(content)
        urgency_score = self._calculate_urgency_score(content_data, opportunity_type)
        conversion_potential = self._calculate_conversion_potential(content, author_profile)
        brand_alignment = self._calculate_brand_alignment(content)

        # Get competitive and trending context
        competitive_context = await self._analyze_competitive_context(content)
        trending_context = await self._analyze_trending_context(content)

        return EngagementContext(
            opportunity_type=opportunity_type,
            content=content,
            author=author,
            author_profile=author_profile,
            conversation_thread=conversation_thread,
            industry_relevance=industry_relevance,
            urgency_score=urgency_score,
            conversion_potential=conversion_potential,
            brand_alignment=brand_alignment,
            competitive_context=competitive_context,
            trending_context=trending_context
        )

    async def _should_engage(self, context: EngagementContext) -> bool:
        """Determine if we should engage using AI Council collaborative decision-making"""

        # First, basic safety and rate limit check
        is_safe, reason = await self.safety_manager.is_engagement_safe(
            content=context.content,
            author=context.author,
            engagement_type="response",
            context={
                "author_profile": context.author_profile,
                "opportunity_type": context.opportunity_type.value,
                "competitive_context": context.competitive_context,
                "trending_context": context.trending_context
            }
        )

        if not is_safe:
            self.logger.info(f"Engagement blocked by safety manager: {reason}")
            return False

        # Minimum quality thresholds (pre-council screening)
        if context.industry_relevance < 3.0:
            return False

        if context.brand_alignment < 5.0:
            return False

        # AI Council Decision for engagement
        try:
            council_decision = await self.ai_council.evaluate_engagement_opportunity(
                tweet_text=context.content,
                author=context.author,
                context={
                    "author_profile": context.author_profile,
                    "opportunity_type": context.opportunity_type.value,
                    "industry_relevance": context.industry_relevance,
                    "conversion_potential": context.conversion_potential,
                    "urgency_score": context.urgency_score,
                    "competitive_context": context.competitive_context,
                    "trending_context": context.trending_context
                }
            )

            # Log council decision
            self.logger.info(
                f"AI Council Decision: {council_decision.final_decision.value} "
                f"(Consensus: {council_decision.consensus_score:.1f}/10) "
                f"for @{context.author}: {context.content[:50]}..."
            )

            # Store council decision for analytics
            context.council_decision = council_decision

            # Return based on council decision
            return council_decision.final_decision in [VoteType.APPROVE, VoteType.MODIFY]

        except Exception as e:
            self.logger.error(f"AI Council evaluation failed: {e}")

            # Fallback to original logic if council fails
            if context.opportunity_type == OpportunityType.MENTION:
                return True  # Always respond to mentions (if they pass safety)

            if context.opportunity_type == OpportunityType.PROSPECT_SIGNAL:
                return context.conversion_potential > 6.0

            # General engagement threshold
            engagement_score = (
                context.industry_relevance * 0.3 +
                context.conversion_potential * 0.3 +
                context.urgency_score * 0.2 +
                context.brand_alignment * 0.2
            )

            return engagement_score > 6.5

    async def _process_engagement_opportunity(self, context: EngagementContext) -> None:
        """Process an engagement opportunity with AI-generated response"""

        try:
            self.current_mode = AgentMode.ANALYZING
            self.session_stats["opportunities_found"] += 1

            # Generate AI response
            ai_response = await self._generate_ai_response(context)

            if ai_response and ai_response.confidence_score > 0.7:
                self.current_mode = AgentMode.RESPONDING

                # Execute engagement
                success = await self._execute_engagement(context, ai_response)

                if success:
                    self.session_stats["engagements_executed"] += 1

                    # Record engagement in safety manager
                    self.safety_manager.record_engagement(
                        engagement_type="response",
                        author=context.author,
                        content=ai_response.content,
                        success=success
                    )

                    # Log to Notion
                    await self._log_engagement_to_notion(context, ai_response, success)

                self.session_stats["responses_generated"] += 1

        except Exception as e:
            self.logger.error(f"Error processing engagement opportunity: {e}")

    async def _generate_ai_response(self, context: EngagementContext) -> Optional[AIResponse]:
        """Generate AI-powered response using AI Council collaborative approach"""

        try:
            # Check if we have a council decision with modifications
            council_decision = getattr(context, 'council_decision', None)

            if council_decision and council_decision.final_decision == VoteType.MODIFY:
                # Use council suggestions to guide response generation
                self.logger.info(f"Generating response with AI Council modifications: {council_decision.modifications_required[:2]}")

            # Use collaborative content creation for high-value opportunities
            if context.conversion_potential > 7.0 or context.industry_relevance > 8.0:
                try:
                    collaboration_result = await self.ai_council.collaborative_content_creation(
                        theme=f"response_to_{context.opportunity_type.value}",
                        context={
                            "original_content": context.content,
                            "author": context.author,
                            "author_profile": context.author_profile,
                            "opportunity_type": context.opportunity_type.value,
                            "council_suggestions": council_decision.modifications_required if council_decision else []
                        }
                    )

                    if collaboration_result["collaboration_success"]:
                        response_content = collaboration_result["selected_content"]["content"]

                        return AIResponse(
                            content=response_content,
                            confidence_score=collaboration_result["selected_content"]["score"],
                            response_type="collaborative_response",
                            reasoning=f"AI Council collaborative response (Score: {collaboration_result['selected_content']['score']:.1f})",
                            safety_score=9.0,  # High safety from council validation
                            brand_voice_score=collaboration_result["selected_content"]["score"]
                        )

                except Exception as e:
                    self.logger.warning(f"Collaborative content creation failed, falling back: {e}")

            # Fallback to enhanced response generator
            response_context = ResponseContext(
                content=context.content,
                author=context.author,
                author_profile=context.author_profile,
                conversation_thread=context.conversation_thread,
                opportunity_type=context.opportunity_type.value,
                industry_relevance=context.industry_relevance,
                conversion_potential=context.conversion_potential,
                brand_alignment=context.brand_alignment,
                urgency=context.urgency_score,
                competitive_context=context.competitive_context,
                trending_context=context.trending_context
            )

            # Generate response using enhanced generator
            generated_response = await self.response_generator.generate_response(response_context)

            if not generated_response:
                return None

            # Validate response with AI Council if it's high-stakes
            if context.conversion_potential > 6.0:
                try:
                    validation_decision = await self.ai_council.evaluate_content_for_posting(
                        generated_response.content,
                        {"response_context": "engagement_reply", "original_tweet": context.content}
                    )

                    if validation_decision.final_decision == VoteType.REJECT:
                        self.logger.warning(f"AI Council rejected generated response: {validation_decision.reasoning}")
                        return None
                    elif validation_decision.final_decision == VoteType.MODIFY:
                        self.logger.info(f"AI Council suggests modifications: {validation_decision.modifications_required[:2]}")
                        # Could implement response modification here

                except Exception as e:
                    self.logger.warning(f"AI Council validation failed: {e}")

            # Convert to AIResponse format
            return AIResponse(
                content=generated_response.content,
                confidence_score=generated_response.confidence_score,
                response_type=generated_response.engagement_strategy,
                reasoning=generated_response.reasoning,
                safety_score=generated_response.safety_score,
                brand_voice_score=generated_response.brand_voice_score
            )

        except Exception as e:
            self.logger.error(f"Error generating AI response: {e}")
            return None

    def _build_response_prompt(self, context: EngagementContext) -> str:
        """Build comprehensive prompt for AI response generation"""

        prompt = f"""
You are the social media AI agent for SME Analytica, an AI-driven analytics platform for restaurants, hotels, and retail businesses.

BRAND CONTEXT:
- SME Analytica offers MenuFlow dynamic pricing that boosts restaurant margins ~10%
- We provide real-time analytics and easy POS integration
- We make enterprise-level BI accessible to non-technical small business owners
- We've helped 500+ restaurants optimize their operations

ENGAGEMENT CONTEXT:
- Opportunity Type: {context.opportunity_type.value}
- Author: {context.author}
- Content: "{context.content}"
- Industry Relevance: {context.industry_relevance}/10
- Conversion Potential: {context.conversion_potential}/10

AUTHOR PROFILE:
- Followers: {context.author_profile.get('followers', 0)}
- Bio: {context.author_profile.get('description', 'N/A')}
- Account Type: {context.author_profile.get('account_type', 'unknown')}

RESPONSE GUIDELINES:
1. Be helpful and authentic, never pushy or overly promotional
2. Share specific data insights when relevant (e.g., "10% margin improvement")
3. Position SME Analytica as a thought leader and helpful expert
4. Use professional but approachable tone
5. Include relevant emojis strategically (📊📈🚀💡🎯🤝)
6. Keep under 280 characters for Twitter
7. Offer value first, promotion second

CONVERSATION THREAD:
{self._format_conversation_thread(context.conversation_thread)}

Generate a response that provides value, demonstrates expertise, and naturally positions SME Analytica as a helpful industry leader. Focus on being genuinely helpful rather than promotional.
"""

        return prompt.strip()

    def _format_conversation_thread(self, thread: List[Dict[str, Any]]) -> str:
        """Format conversation thread for AI context"""
        if not thread:
            return "No previous conversation context."

        formatted = []
        for tweet in thread[-3:]:  # Last 3 tweets for context
            author = tweet.get('author', 'Unknown')
            content = tweet.get('text', '')
            formatted.append(f"@{author}: {content}")

        return "\n".join(formatted)

    async def _execute_engagement(self, context: EngagementContext,
                                ai_response: AIResponse) -> bool:
        """Execute the engagement action"""

        try:
            if ai_response.response_type == "reply":
                # Extract tweet ID from context
                tweet_id = self._extract_tweet_id(context)
                if tweet_id:
                    result = await self.twitter_manager.post_tweet(
                        content=ai_response.content,
                        reply_to_tweet_id=tweet_id
                    )
                    return result is not None

            elif ai_response.response_type == "quote_tweet":
                # Quote tweet functionality
                tweet_id = self._extract_tweet_id(context)
                if tweet_id:
                    quote_content = f"{ai_response.content} https://twitter.com/i/web/status/{tweet_id}"
                    result = await self.twitter_manager.post_tweet(content=quote_content)
                    return result is not None

            elif ai_response.response_type == "retweet_comment":
                # Retweet with comment
                tweet_id = self._extract_tweet_id(context)
                if tweet_id:
                    # First retweet
                    await self.twitter_manager.retweet(tweet_id)
                    # Then add comment
                    result = await self.twitter_manager.post_tweet(content=ai_response.content)
                    return result is not None

            return False

        except Exception as e:
            self.logger.error(f"Error executing engagement: {e}")
            return False

    # Helper methods for analysis and scoring

    async def _get_author_profile(self, username: str) -> Dict[str, Any]:
        """Get author profile information with rate limiting protection"""
        try:
            profile = await self.twitter_manager.get_user_profile(username)
            return profile if profile else {"username": username}
        except Exception as e:
            self.logger.warning(f"Could not get profile for @{username}: {e}")
            return {"username": username}

    async def _get_conversation_thread(self, tweet_id: str) -> List[Dict[str, Any]]:
        """Get conversation thread for context with rate limiting protection"""
        try:
            return await self.twitter_manager.get_conversation_thread(tweet_id)
        except Exception as e:
            self.logger.warning(f"Could not get conversation thread for {tweet_id}: {e}")
            return []

    def _calculate_industry_relevance(self, content: str) -> float:
        """Calculate how relevant content is to our industry"""
        content_lower = content.lower()
        score = 0.0

        # Primary keywords (high weight)
        primary_keywords = self.monitoring_config["keywords"]["high_priority"]
        for keyword in primary_keywords:
            if keyword in content_lower:
                score += 2.0

        # Secondary keywords (medium weight)
        secondary_keywords = self.monitoring_config["keywords"]["medium_priority"]
        for keyword in secondary_keywords:
            if keyword in content_lower:
                score += 1.0

        # Prospect signals (high weight)
        prospect_signals = self.monitoring_config["keywords"]["prospect_signals"]
        for signal in prospect_signals:
            if signal in content_lower:
                score += 1.5

        return min(score, 10.0)

    def _calculate_urgency_score(self, content_data: Dict[str, Any],
                               opportunity_type: OpportunityType) -> float:
        """Calculate urgency score for engagement"""
        score = 5.0  # Base urgency

        content = content_data.get('text', '').lower()

        # Time-sensitive indicators
        urgent_words = ['urgent', 'asap', 'immediately', 'now', 'today', 'breaking']
        for word in urgent_words:
            if word in content:
                score += 2.0

        # Question indicators (need response)
        if '?' in content:
            score += 1.5

        # Opportunity type urgency
        type_urgency = {
            OpportunityType.MENTION: 9.0,
            OpportunityType.PROSPECT_SIGNAL: 8.0,
            OpportunityType.INDUSTRY_CONVERSATION: 6.0,
            OpportunityType.HASHTAG_MATCH: 5.0,
            OpportunityType.TREND_OPPORTUNITY: 7.0,
            OpportunityType.COMPETITOR_ACTIVITY: 4.0
        }

        score = max(score, type_urgency.get(opportunity_type, 5.0))

        return min(score, 10.0)

    def _calculate_conversion_potential(self, content: str,
                                     author_profile: Dict[str, Any]) -> float:
        """Calculate potential for converting engagement to business value"""
        score = 3.0  # Base potential
        content_lower = content.lower()

        # High conversion indicators
        high_conversion_signals = [
            'looking for', 'need help', 'recommendations', 'advice',
            'struggling with', 'how to', 'best solution', 'which platform'
        ]

        for signal in high_conversion_signals:
            if signal in content_lower:
                score += 2.0

        # Target customer indicators
        target_indicators = [
            'restaurant owner', 'small business', 'pos system', 'analytics',
            'hotel manager', 'retail business', 'menu pricing'
        ]

        for indicator in target_indicators:
            if indicator in content_lower:
                score += 1.5

        # Author profile factors
        followers = author_profile.get('followers', 0)
        if followers > 1000:  # Potential influencer
            score += 1.0

        bio = author_profile.get('description', '').lower()
        if any(word in bio for word in ['restaurant', 'business', 'owner', 'manager']):
            score += 2.0

        return min(score, 10.0)

    def _calculate_brand_alignment(self, content: str) -> float:
        """Calculate how well content aligns with SME Analytica brand"""
        score = 5.0  # Neutral baseline
        content_lower = content.lower()

        # Positive alignment
        positive_keywords = [
            'restaurant', 'analytics', 'data', 'pricing', 'ai', 'automation',
            'small business', 'hospitality', 'pos', 'integration', 'revenue',
            'profit', 'optimization', 'efficiency', 'growth', 'technology'
        ]

        for keyword in positive_keywords:
            if keyword in content_lower:
                score += 0.5

        # Negative alignment
        negative_keywords = [
            'spam', 'scam', 'fake', 'illegal', 'controversial', 'politics',
            'religion', 'personal attack', 'harassment', 'offensive'
        ]

        for keyword in negative_keywords:
            if keyword in content_lower:
                score -= 3.0

        return max(min(score, 10.0), 0.0)

    async def _analyze_competitive_context(self, content: str) -> Optional[str]:
        """Analyze competitive context in content"""
        competitors = ['toast', 'square', 'opentable', 'resy', 'yelp']
        content_lower = content.lower()

        mentioned_competitors = [comp for comp in competitors if comp in content_lower]

        if mentioned_competitors:
            return f"Mentions competitors: {', '.join(mentioned_competitors)}"

        return None

    async def _analyze_trending_context(self, content: str) -> Optional[str]:
        """Analyze trending context in content"""
        trending_topics = ['ai revolution', 'digital transformation', 'automation']
        content_lower = content.lower()

        mentioned_trends = [trend for trend in trending_topics if trend in content_lower]

        if mentioned_trends:
            return f"Trending topics: {', '.join(mentioned_trends)}"

        return None

    def _passes_safety_filters(self, context: EngagementContext) -> bool:
        """Check if content passes safety filters"""
        content_lower = context.content.lower()

        # Check for inappropriate topics
        avoid_topics = self.safety_filters["avoid_topics"]
        for topic in avoid_topics:
            if topic in content_lower:
                self.session_stats["safety_blocks"] += 1
                return False

        # Check author profile
        author_profile = context.author_profile

        # Minimum follower threshold
        if author_profile.get('followers', 0) < self.safety_filters["minimum_thresholds"]["follower_count"]:
            return False

        return True

    def _within_rate_limits(self) -> bool:
        """Check if we're within engagement rate limits"""
        # This would check against actual engagement counts
        # For now, return True (implement proper rate limiting)
        return True

    def _analyze_response_confidence(self, response: str, context: EngagementContext) -> float:
        """Analyze confidence in AI response quality"""
        score = 7.0  # Base confidence

        # Length check
        if len(response) < 20:
            score -= 2.0
        elif len(response) > 280:
            score -= 1.0

        # Relevance to context
        if any(keyword in response.lower() for keyword in ['restaurant', 'analytics', 'data']):
            score += 1.0

        # Professional tone indicators
        if any(phrase in response for phrase in ['happy to', 'feel free', 'would love']):
            score += 0.5

        return min(score, 10.0)

    def _analyze_response_safety(self, response: str) -> float:
        """Analyze safety score of response"""
        score = 9.0  # High safety baseline

        # Check for promotional language
        promotional_words = ['buy now', 'limited time', 'act fast', 'exclusive offer']
        for word in promotional_words:
            if word in response.lower():
                score -= 2.0

        return max(score, 0.0)

    def _analyze_brand_voice_alignment(self, response: str) -> float:
        """Analyze how well response aligns with brand voice"""
        score = 7.0  # Good baseline

        # Check for brand voice elements
        brand_elements = ['data', 'analytics', 'insights', 'optimization', 'restaurant']
        for element in brand_elements:
            if element in response.lower():
                score += 0.5

        # Check for helpful tone
        helpful_phrases = ['happy to help', 'feel free', 'would love to share']
        for phrase in helpful_phrases:
            if phrase in response.lower():
                score += 0.5

        return min(score, 10.0)

    def _determine_response_type(self, context: EngagementContext) -> str:
        """Determine the best response type for the context"""

        # Mentions always get replies
        if context.opportunity_type == OpportunityType.MENTION:
            return "reply"

        # High conversion potential gets direct replies
        if context.conversion_potential > 7.0:
            return "reply"

        # Industry conversations get thoughtful replies
        if context.opportunity_type == OpportunityType.INDUSTRY_CONVERSATION:
            return "reply"

        # Trending content gets quote tweets for amplification
        if context.opportunity_type == OpportunityType.TREND_OPPORTUNITY:
            return "quote_tweet"

        # Default to reply for engagement
        return "reply"

    def _extract_tweet_id(self, context: EngagementContext) -> Optional[str]:
        """Extract tweet ID from context"""
        # This would extract the actual tweet ID from the context
        # Implementation depends on how tweet data is structured
        return "123456789"  # Placeholder

    async def _log_engagement_to_notion(self, context: EngagementContext,
                                      ai_response: AIResponse, success: bool) -> None:
        """Log engagement activity to Notion database"""
        try:
            engagement_data = {
                "timestamp": datetime.now().isoformat(),
                "opportunity_type": context.opportunity_type.value,
                "author": context.author,
                "content_preview": context.content[:100] + "..." if len(context.content) > 100 else context.content,
                "response": ai_response.content,
                "response_type": ai_response.response_type,
                "confidence_score": ai_response.confidence_score,
                "industry_relevance": context.industry_relevance,
                "conversion_potential": context.conversion_potential,
                "success": success
            }

            # Save to Notion (implement based on your Notion schema)
            self.notion_manager.save_engagement_analytics(engagement_data)

        except Exception as e:
            self.logger.error(f"Error logging engagement to Notion: {e}")

    async def _save_session_analytics(self) -> None:
        """Save session analytics to Notion"""
        try:
            session_data = {
                "session_start": self.session_stats["start_time"].isoformat(),
                "session_duration": str(datetime.now() - self.session_stats["start_time"]),
                "opportunities_found": self.session_stats["opportunities_found"],
                "responses_generated": self.session_stats["responses_generated"],
                "engagements_executed": self.session_stats["engagements_executed"],
                "safety_blocks": self.session_stats["safety_blocks"],
                "success_rate": (
                    self.session_stats["engagements_executed"] /
                    max(self.session_stats["responses_generated"], 1) * 100
                )
            }

            self.notion_manager.save_engagement_analytics(session_data)

        except Exception as e:
            self.logger.error(f"Error saving session analytics: {e}")

    async def stop_monitoring(self) -> Dict[str, Any]:
        """Stop monitoring and return final statistics"""
        self.is_running = False

        final_stats = {
            "session_duration": str(datetime.now() - self.session_stats["start_time"]),
            "total_opportunities": self.session_stats["opportunities_found"],
            "total_responses": self.session_stats["responses_generated"],
            "total_engagements": self.session_stats["engagements_executed"],
            "safety_blocks": self.session_stats["safety_blocks"],
            "success_rate": (
                self.session_stats["engagements_executed"] /
                max(self.session_stats["responses_generated"], 1) * 100
            )
        }

        self.logger.info(f"🤖 Agent stopped. Final stats: {final_stats}")
        return final_stats

    def get_agent_status(self) -> Dict[str, Any]:
        """Get current agent status and statistics"""
        runtime = datetime.now() - self.session_stats["start_time"]

        # Get safety statistics
        safety_stats = self.safety_manager.get_safety_stats()

        # Get AI provider status
        ai_provider_status = "Unknown"
        if hasattr(self.ai_provider, 'providers'):
            if "gemini" in self.ai_provider.providers and self.ai_provider.providers["gemini"].is_available:
                ai_provider_status = "Gemini-powered (Enhanced Intelligence)"
            elif "anthropic" in self.ai_provider.providers and self.ai_provider.providers["anthropic"].is_available:
                ai_provider_status = "Anthropic-powered"
            elif "openai" in self.ai_provider.providers and self.ai_provider.providers["openai"].is_available:
                ai_provider_status = "OpenAI-powered"

        return {
            "is_running": self.is_running,
            "current_mode": self.current_mode.value,
            "runtime": str(runtime),
            "ai_provider_status": ai_provider_status,
            "opportunities_found": self.session_stats["opportunities_found"],
            "responses_generated": self.session_stats["responses_generated"],
            "engagements_executed": self.session_stats["engagements_executed"],
            "safety_blocks": self.session_stats["safety_blocks"],
            "last_check": self.last_check_time.isoformat(),
            "safety_stats": safety_stats,
            "hashtag_tracker_stats": self.hashtag_tracker.get_tracking_stats() if hasattr(self.hashtag_tracker, 'get_tracking_stats') else {},
            "response_generator_stats": self.response_generator.get_generation_stats() if hasattr(self.response_generator, 'get_generation_stats') else {}
        }

# Factory function for easy agent creation
async def create_intelligent_agent() -> IntelligentEngagementAgent:
    """Create and initialize an intelligent engagement agent"""
    agent = IntelligentEngagementAgent()
    return agent

# CLI interface for testing
if __name__ == "__main__":
    import sys

    async def main():
        agent = await create_intelligent_agent()

        if len(sys.argv) > 1 and sys.argv[1] == "start":
            print("🤖 Starting Intelligent Engagement Agent...")
            try:
                await agent.start_monitoring()
            except KeyboardInterrupt:
                print("\n🛑 Stopping agent...")
                stats = await agent.stop_monitoring()
                print(f"Final statistics: {stats}")
        else:
            print("Usage: python intelligent_engagement_agent.py start")

    asyncio.run(main())
