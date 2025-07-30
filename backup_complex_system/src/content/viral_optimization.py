"""
Viral Content Optimization Agent for SME Analytica
Real-time trending topic integration and viral content generation
"""

import asyncio
import json
import re
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import random
import logging
from collections import defaultdict, Counter
import math

# Import existing modules
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config.settings import SMEAnalyticaContext
from src.social.twitter_manager import TwitterManager, Tweet

class ViralPotential(str, Enum):
    """Viral potential scoring levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VIRAL = "viral"

class TrendType(str, Enum):
    """Types of trending topics"""
    HASHTAG = "hashtag"
    KEYWORD = "keyword"
    CONVERSATION = "conversation"
    EVENT = "event"
    INDUSTRY_NEWS = "industry_news"

@dataclass
class ViralHook:
    """Structure for viral content hooks"""
    hook_text: str
    hook_type: str
    emotional_trigger: str
    expected_engagement: str
    use_cases: List[str]
    viral_score: float

@dataclass
class TrendingTopic:
    """Structure for trending topics"""
    topic: str
    trend_type: TrendType
    volume: int
    growth_rate: float
    viral_potential: ViralPotential
    relevance_score: float
    industry_connection: str
    optimal_timing: datetime
    hashtags: List[str]
    context: str
    discovered_at: datetime
    expires_at: Optional[datetime] = None

@dataclass
class ViralContent:
    """Generated viral content structure"""
    text: str
    hooks: List[str]
    hashtags: List[str]
    viral_score: float
    trend_context: Optional[TrendingTopic]
    timing_score: float
    shareability_factors: List[str]
    thread_potential: bool
    estimated_reach: int

class ViralOptimizationAgent:
    """Main viral optimization engine for SME Analytica"""
    
    def __init__(self, twitter_manager: TwitterManager):
        self.twitter_manager = twitter_manager
        self.context = SMEAnalyticaContext()
        self.logger = logging.getLogger(__name__)
        
        # Viral content components
        self.viral_hooks = self._initialize_viral_hooks()
        self.thread_templates = self._initialize_thread_templates()
        self.trending_topics_cache = {}
        self.viral_patterns = self._initialize_viral_patterns()
        
        # Tracking and analytics
        self.content_performance_history = []
        self.trend_tracking_history = []
        
        # Business-specific keywords for trend monitoring
        self.business_keywords = [
            "restaurant", "small business", "analytics", "pricing", "AI", "automation",
            "hospitality", "hotel", "retail", "POS", "revenue", "profit", "margins",
            "customer data", "business intelligence", "SME", "entrepreneur", "startup",
            "MenuFlow", "dynamic pricing", "table turnover", "peak hours", "QR menu"
        ]
        
        # Viral success patterns from top performing accounts
        self.viral_success_patterns = {
            "thread_starters": [
                "🧵 THREAD: Why",
                "Here's what nobody tells you about",
                "I analyzed 1000+ businesses and found",
                "The #1 mistake I see restaurants make:",
                "Data doesn't lie. Here's what we discovered:",
                "🔥 This will change how you think about"
            ],
            "engagement_triggers": [
                "What's your experience with",
                "Agree or disagree:",
                "Hot take:",
                "Unpopular opinion:",
                "Let's settle this debate:",
                "Am I the only one who thinks"
            ],
            "value_propositions": [
                "10% margin boost with one simple change",
                "From struggling to thriving in 3 months",
                "Why 87% of restaurants fail at pricing",
                "The AI hack every small business needs",
                "Turn your POS data into profit",
                "Real-time insights that actually work"
            ]
        }

    def _initialize_viral_hooks(self) -> List[ViralHook]:
        """Initialize viral hook templates optimized for SME Analytica"""
        
        hooks = [
            # Problem-agitation hooks
            ViralHook(
                hook_text="87% of restaurants are leaving money on the table with pricing. Here's the simple fix:",
                hook_type="problem_agitation",
                emotional_trigger="fear_of_missing_out",
                expected_engagement="high",
                use_cases=["pricing", "restaurant"],
                viral_score=8.5
            ),
            ViralHook(
                hook_text="I analyzed 1000+ small businesses. The successful ones all do this ONE thing:",
                hook_type="data_revelation",
                emotional_trigger="curiosity",
                expected_engagement="viral",
                use_cases=["general", "case_study"],
                viral_score=9.2
            ),
            ViralHook(
                hook_text="Your POS system is collecting gold, but you're throwing it away. Here's why:",
                hook_type="missed_opportunity",
                emotional_trigger="regret_avoidance",
                expected_engagement="high",
                use_cases=["analytics", "data"],
                viral_score=8.8
            ),
            ViralHook(
                hook_text="The #1 mistake killing small business profits (and it's not what you think):",
                hook_type="contrarian",
                emotional_trigger="curiosity",
                expected_engagement="high",
                use_cases=["profit", "mistakes"],
                viral_score=8.7
            ),
            ViralHook(
                hook_text="🔥 HOT TAKE: Manual pricing is costing restaurants 15% of potential revenue:",
                hook_type="hot_take",
                emotional_trigger="urgency",
                expected_engagement="high",
                use_cases=["pricing", "controversy"],
                viral_score=8.3
            ),
            ViralHook(
                hook_text="Plot twist: The data you need to 10x your business is already in your hands:",
                hook_type="plot_twist",
                emotional_trigger="surprise",
                expected_engagement="medium_high",
                use_cases=["data", "growth"],
                viral_score=8.1
            ),
            # Success story hooks
            ViralHook(
                hook_text="From 8 followers to helping restaurants boost margins 10%. Here's the journey:",
                hook_type="transformation",
                emotional_trigger="inspiration",
                expected_engagement="high",
                use_cases=["success_story", "growth"],
                viral_score=8.9
            ),
            ViralHook(
                hook_text="This cafe owner increased revenue 25% with one simple change. The secret:",
                hook_type="case_study_teaser",
                emotional_trigger="curiosity",
                expected_engagement="high",
                use_cases=["case_study", "revenue"],
                viral_score=8.6
            ),
            # Educational hooks
            ViralHook(
                hook_text="🧵 THREAD: 7 AI-powered pricing strategies that actually work for small businesses:",
                hook_type="educational_thread",
                emotional_trigger="value_seeking",
                expected_engagement="high",
                use_cases=["education", "thread"],
                viral_score=8.4
            ),
            ViralHook(
                hook_text="Nobody teaches small business owners this, but peak-hour optimization can change everything:",
                hook_type="secret_knowledge",
                emotional_trigger="exclusivity",
                expected_engagement="medium_high",
                use_cases=["education", "insider"],
                viral_score=8.2
            ),
            # Industry insight hooks
            ViralHook(
                hook_text="The restaurant industry is changing fast. Here's what's coming next:",
                hook_type="industry_prediction",
                emotional_trigger="fomo",
                expected_engagement="medium_high",
                use_cases=["industry", "future"],
                viral_score=7.9
            ),
            ViralHook(
                hook_text="Unpopular opinion: Most 'analytics' solutions are actually making businesses dumber:",
                hook_type="controversial_take",
                emotional_trigger="debate",
                expected_engagement="high",
                use_cases=["controversy", "industry"],
                viral_score=8.5
            )
        ]
        
        return hooks

    def _initialize_thread_templates(self) -> Dict[str, List[str]]:
        """Initialize viral thread templates for different scenarios"""
        
        return {
            "case_study_thread": [
                "{hook}",
                "2/ The Challenge: {business_name} was struggling with {specific_problem}. Sound familiar?",
                "3/ The numbers were brutal: {negative_metrics}",
                "4/ Then we implemented {solution_name}. Here's what happened:",
                "5/ Results after {timeframe}: {positive_results}",
                "6/ But here's the real kicker: {unexpected_benefit}",
                "7/ The lesson: {key_takeaway}",
                "8/ Want similar results? Here's how to start: {call_to_action}"
            ],
            "industry_insight_thread": [
                "{hook}",
                "2/ I've been tracking {data_point} across {sample_size} businesses. The pattern is clear:",
                "3/ The top 10% all do this: {key_behavior}",
                "4/ Meanwhile, the bottom 50% are still: {outdated_behavior}",
                "5/ The gap is widening. Here's why: {explanation}",
                "6/ Real example: {case_example}",
                "7/ The takeaway for your business: {actionable_advice}",
                "8/ Ready to level up? Start here: {next_steps}"
            ],
            "problem_solution_thread": [
                "{hook}",
                "2/ Here's the problem: {problem_description}",
                "3/ Most businesses try to fix this by: {common_wrong_solution}",
                "4/ But that actually makes it worse because: {why_it_fails}",
                "5/ The real solution is counter-intuitive: {actual_solution}",
                "6/ Here's how it works: {solution_explanation}",
                "7/ Case in point: {example}",
                "8/ Try this: {specific_action_step}"
            ],
            "trend_analysis_thread": [
                "{hook}",
                "2/ The data is clear: {trend_statement}",
                "3/ What this means for {target_audience}: {implications}",
                "4/ Smart businesses are already: {early_adopter_behavior}",
                "5/ But most are still: {laggard_behavior}",
                "6/ The opportunity window: {timing_element}",
                "7/ How to capitalize: {strategy}",
                "8/ Don't wait. Start with: {immediate_action}"
            ]
        }

    def _initialize_viral_patterns(self) -> Dict[str, Any]:
        """Initialize patterns that tend to go viral in business/tech space"""
        
        return {
            "emotional_triggers": {
                "curiosity": ["Here's what nobody tells you", "The secret", "What we discovered"],
                "urgency": ["Before it's too late", "Window closing", "Act now"],
                "fear": ["Biggest mistake", "Killing your profits", "Costing you"],
                "aspiration": ["Level up", "Transform", "10x your business"],
                "validation": ["You're not alone", "Everyone struggles with", "Common problem"],
                "exclusivity": ["Insider secret", "What top performers do", "Hidden strategy"]
            },
            "engagement_drivers": {
                "numbers": ["87%", "10x", "2.5x revenue", "$50k saved"],
                "timeframes": ["in 30 days", "this quarter", "overnight", "in 3 months"],
                "superlatives": ["#1 mistake", "biggest opportunity", "best strategy"],
                "controversy": ["Unpopular opinion", "Hot take", "Contrarian view"],
                "storytelling": ["Plot twist", "Here's what happened", "The journey"]
            },
            "shareability_factors": [
                "practical_value",
                "emotional_resonance", 
                "social_currency",
                "triggering_debates",
                "surprising_insights",
                "actionable_advice"
            ]
        }

    async def monitor_trending_topics(self) -> List[TrendingTopic]:
        """Monitor and analyze trending topics for viral opportunities"""
        
        self.logger.info("Starting trending topic monitoring...")
        
        trending_topics = []
        
        try:
            # Get hashtag trends
            hashtag_trends = await self.twitter_manager.get_trending_hashtags()
            
            # Analyze each trend for relevance
            for hashtag in hashtag_trends:
                relevance_score = self._calculate_relevance_score(hashtag)
                
                if relevance_score > 3.0:  # Threshold for relevant trends
                    # Get sample tweets to understand context
                    sample_tweets = await self.twitter_manager.search_tweets(
                        hashtag, max_results=20
                    )
                    
                    trend_analysis = self._analyze_trend_context(hashtag, sample_tweets)
                    
                    trending_topic = TrendingTopic(
                        topic=hashtag,
                        trend_type=TrendType.HASHTAG,
                        volume=len(sample_tweets),
                        growth_rate=trend_analysis["growth_rate"],
                        viral_potential=trend_analysis["viral_potential"],
                        relevance_score=relevance_score,
                        industry_connection=trend_analysis["industry_connection"],
                        optimal_timing=self._calculate_optimal_timing(trend_analysis),
                        hashtags=[hashtag],
                        context=trend_analysis["context"],
                        discovered_at=datetime.now()
                    )
                    
                    trending_topics.append(trending_topic)
            
            # Monitor keyword trends
            keyword_trends = await self._monitor_keyword_trends()
            trending_topics.extend(keyword_trends)
            
            # Cache results
            self.trending_topics_cache = {
                "last_updated": datetime.now(),
                "topics": trending_topics
            }
            
            # Track for analytics
            self.trend_tracking_history.append({
                "timestamp": datetime.now(),
                "topics_found": len(trending_topics),
                "high_potential_count": len([t for t in trending_topics if t.viral_potential in [ViralPotential.HIGH, ViralPotential.VIRAL]])
            })
            
            self.logger.info(f"Found {len(trending_topics)} relevant trending topics")
            return trending_topics
            
        except Exception as e:
            self.logger.error(f"Error monitoring trending topics: {e}")
            return []

    async def _monitor_keyword_trends(self) -> List[TrendingTopic]:
        """Monitor specific business keywords for emerging trends"""
        
        keyword_trends = []
        
        for keyword in self.business_keywords:
            try:
                # Search for recent activity around keyword
                tweets = await self.twitter_manager.search_tweets(
                    f"{keyword} -is:retweet", max_results=50
                )
                
                if len(tweets) > 10:  # Minimum threshold for trend consideration
                    trend_analysis = self._analyze_keyword_trend(keyword, tweets)
                    
                    if trend_analysis["is_trending"]:
                        trending_topic = TrendingTopic(
                            topic=keyword,
                            trend_type=TrendType.KEYWORD,
                            volume=len(tweets),
                            growth_rate=trend_analysis["growth_rate"],
                            viral_potential=trend_analysis["viral_potential"],
                            relevance_score=10.0,  # Always highly relevant
                            industry_connection=trend_analysis["industry_connection"],
                            optimal_timing=datetime.now() + timedelta(hours=2),
                            hashtags=trend_analysis["related_hashtags"],
                            context=trend_analysis["context"],
                            discovered_at=datetime.now()
                        )
                        
                        keyword_trends.append(trending_topic)
                
                # Rate limiting
                await asyncio.sleep(0.5)
                
            except Exception as e:
                self.logger.error(f"Error monitoring keyword {keyword}: {e}")
                continue
        
        return keyword_trends

    def _calculate_relevance_score(self, topic: str) -> float:
        """Calculate how relevant a trending topic is to SME Analytica"""
        
        score = 0.0
        topic_lower = topic.lower()
        
        # Direct business keywords
        business_matches = sum(1 for keyword in self.business_keywords 
                             if keyword.lower() in topic_lower)
        score += business_matches * 2.0
        
        # Industry-adjacent terms
        adjacent_terms = [
            "tech", "data", "ai", "startup", "business", "growth", "profit",
            "revenue", "innovation", "digital", "automation", "saas"
        ]
        adjacent_matches = sum(1 for term in adjacent_terms 
                             if term in topic_lower)
        score += adjacent_matches * 1.0
        
        # Trending business topics
        trending_business = [
            "inflation", "economy", "recession", "recovery", "funding",
            "investment", "ipo", "acquisition", "merger", "layoffs"
        ]
        business_trend_matches = sum(1 for term in trending_business 
                                   if term in topic_lower)
        score += business_trend_matches * 1.5
        
        return score

    def _analyze_trend_context(self, hashtag: str, tweets: List[Tweet]) -> Dict[str, Any]:
        """Analyze the context and potential of a trending topic"""
        
        if not tweets:
            return {
                "growth_rate": 0.0,
                "viral_potential": ViralPotential.LOW,
                "industry_connection": "none",
                "context": "No context available"
            }
        
        # Analyze tweet engagement
        total_engagement = sum(
            tweet.public_metrics.get('like_count', 0) +
            tweet.public_metrics.get('retweet_count', 0) +
            tweet.public_metrics.get('reply_count', 0)
            for tweet in tweets
        )
        
        avg_engagement = total_engagement / len(tweets) if tweets else 0
        
        # Analyze content themes
        all_text = " ".join(tweet.text for tweet in tweets).lower()
        
        # Determine industry connection
        industry_connection = "general"
        if any(word in all_text for word in ["restaurant", "hotel", "retail"]):
            industry_connection = "direct"
        elif any(word in all_text for word in ["business", "startup", "entrepreneur"]):
            industry_connection = "business"
        elif any(word in all_text for word in ["tech", "ai", "data", "analytics"]):
            industry_connection = "tech"
        
        # Calculate viral potential
        viral_potential = ViralPotential.LOW
        if avg_engagement > 100:
            viral_potential = ViralPotential.HIGH
        elif avg_engagement > 50:
            viral_potential = ViralPotential.MEDIUM
        
        # Estimate growth rate based on recency and engagement
        recent_tweets = [t for t in tweets if 
                        (datetime.now() - t.created_at.replace(tzinfo=None)).total_seconds() < 3600]
        growth_rate = len(recent_tweets) / len(tweets) if tweets else 0
        
        return {
            "growth_rate": growth_rate,
            "viral_potential": viral_potential,
            "industry_connection": industry_connection,
            "context": f"Trending with {len(tweets)} mentions, avg engagement: {avg_engagement:.1f}",
            "avg_engagement": avg_engagement
        }

    def _analyze_keyword_trend(self, keyword: str, tweets: List[Tweet]) -> Dict[str, Any]:
        """Analyze if a keyword is trending and its viral potential"""
        
        # Check recency - more recent tweets indicate trending
        recent_hours = 6
        recent_cutoff = datetime.now() - timedelta(hours=recent_hours)
        recent_tweets = [t for t in tweets if 
                        t.created_at.replace(tzinfo=None) > recent_cutoff]
        
        # Calculate if trending based on recent activity
        recent_ratio = len(recent_tweets) / len(tweets) if tweets else 0
        is_trending = recent_ratio > 0.3 and len(recent_tweets) > 5
        
        # Extract related hashtags
        all_text = " ".join(tweet.text for tweet in tweets)
        hashtag_pattern = r'#\w+'
        hashtags = list(set(re.findall(hashtag_pattern, all_text)))
        
        # Calculate engagement
        total_engagement = sum(
            tweet.public_metrics.get('like_count', 0) +
            tweet.public_metrics.get('retweet_count', 0) +
            tweet.public_metrics.get('reply_count', 0)
            for tweet in tweets
        )
        avg_engagement = total_engagement / len(tweets) if tweets else 0
        
        # Determine viral potential
        viral_potential = ViralPotential.LOW
        if avg_engagement > 50 and is_trending:
            viral_potential = ViralPotential.HIGH
        elif avg_engagement > 20 or is_trending:
            viral_potential = ViralPotential.MEDIUM
        
        return {
            "is_trending": is_trending,
            "growth_rate": recent_ratio,
            "viral_potential": viral_potential,
            "industry_connection": "direct",  # Our keywords are always directly relevant
            "context": f"Keyword trending with {len(recent_tweets)} recent mentions",
            "related_hashtags": hashtags[:5]  # Top 5 related hashtags
        }

    def _calculate_optimal_timing(self, trend_analysis: Dict[str, Any]) -> datetime:
        """Calculate the optimal time to post content about this trend"""
        
        # Generally, optimal timing is 1-3 hours after trend detection
        # but before it peaks (to ride the wave up)
        
        base_delay = 1  # Start with 1 hour delay
        
        # Adjust based on viral potential
        if trend_analysis["viral_potential"] == ViralPotential.HIGH:
            base_delay = 0.5  # Post quickly for high potential
        elif trend_analysis["viral_potential"] == ViralPotential.VIRAL:
            base_delay = 0.25  # Post very quickly for viral potential
        
        # Adjust based on growth rate
        if trend_analysis["growth_rate"] > 0.7:
            base_delay *= 0.5  # Fast-growing trends need quick response
        
        return datetime.now() + timedelta(hours=base_delay)

    async def generate_viral_content(self, trend: Optional[TrendingTopic] = None, 
                                   content_type: str = "general") -> ViralContent:
        """Generate viral content optimized for engagement"""
        
        self.logger.info(f"Generating viral content for type: {content_type}")
        
        # Select appropriate viral hook
        hook = self._select_optimal_hook(trend, content_type)
        
        # Generate base content
        if content_type == "thread":
            content = await self._generate_viral_thread(hook, trend)
        else:
            content = await self._generate_viral_post(hook, trend)
        
        # Calculate viral score
        viral_score = self._calculate_viral_score(content, hook, trend)
        
        # Generate hashtags
        hashtags = self._generate_viral_hashtags(trend, content_type)
        
        # Calculate timing score
        timing_score = self._calculate_timing_score(trend)
        
        # Identify shareability factors
        shareability_factors = self._identify_shareability_factors(content, hook)
        
        # Estimate reach
        estimated_reach = self._estimate_reach(viral_score, timing_score, trend)
        
        viral_content = ViralContent(
            text=content["text"],
            hooks=[hook.hook_text],
            hashtags=hashtags,
            viral_score=viral_score,
            trend_context=trend,
            timing_score=timing_score,
            shareability_factors=shareability_factors,
            thread_potential=content.get("is_thread", False),
            estimated_reach=estimated_reach
        )
        
        # Track for performance analysis
        self.content_performance_history.append({
            "generated_at": datetime.now(),
            "viral_score": viral_score,
            "trend_used": trend.topic if trend else None,
            "content_type": content_type
        })
        
        return viral_content

    def _select_optimal_hook(self, trend: Optional[TrendingTopic], 
                           content_type: str) -> ViralHook:
        """Select the best viral hook for the given context"""
        
        # Filter hooks by relevance
        relevant_hooks = []
        
        for hook in self.viral_hooks:
            if content_type in hook.use_cases or "general" in hook.use_cases:
                relevance_score = hook.viral_score
                
                # Boost score if hook matches trend context
                if trend and trend.industry_connection in hook.hook_text.lower():
                    relevance_score += 1.0
                
                # Boost score for high-potential trends
                if trend and trend.viral_potential in [ViralPotential.HIGH, ViralPotential.VIRAL]:
                    relevance_score += 0.5
                
                relevant_hooks.append((hook, relevance_score))
        
        # Select hook with highest relevance score
        if relevant_hooks:
            relevant_hooks.sort(key=lambda x: x[1], reverse=True)
            return relevant_hooks[0][0]
        
        # Fallback to highest-scoring general hook
        return max(self.viral_hooks, key=lambda h: h.viral_score)

    async def _generate_viral_post(self, hook: ViralHook, 
                                  trend: Optional[TrendingTopic]) -> Dict[str, Any]:
        """Generate a single viral post"""
        
        # Start with the hook
        content_parts = [hook.hook_text]
        
        # Add trend-specific context if available
        if trend:
            context_line = self._generate_trend_context_line(trend)
            if context_line:
                content_parts.append(context_line)
        
        # Add SME Analytica value proposition
        value_prop = random.choice([
            "MenuFlow's AI pricing delivers 10% margin boosts during peak hours.",
            "Real-time analytics that actually drive revenue, not just reports.",
            "Turn your POS data into profit with AI that speaks restaurant.",
            "Dynamic pricing + real-time insights = competitive advantage."
        ])
        content_parts.append(value_prop)
        
        # Add engagement driver
        engagement_line = random.choice([
            "What's your biggest pricing challenge?",
            "Ready to see your data differently?",
            "Your experience with dynamic pricing?",
            "Time to level up your analytics game?"
        ])
        content_parts.append(engagement_line)
        
        # Combine with proper spacing
        full_text = "\n\n".join(content_parts)
        
        return {
            "text": full_text,
            "is_thread": False
        }

    async def _generate_viral_thread(self, hook: ViralHook, 
                                   trend: Optional[TrendingTopic]) -> Dict[str, Any]:
        """Generate a viral thread"""
        
        # Select thread template based on hook type
        template_key = "case_study_thread"
        if "industry" in hook.hook_type or "prediction" in hook.hook_type:
            template_key = "industry_insight_thread"
        elif "problem" in hook.hook_type or "mistake" in hook.hook_type:
            template_key = "problem_solution_thread"
        elif trend and trend.trend_type == TrendType.INDUSTRY_NEWS:
            template_key = "trend_analysis_thread"
        
        template = self.thread_templates[template_key]
        
        # Generate thread variables
        thread_vars = self._generate_thread_variables(hook, trend)
        
        # Format each tweet in the thread
        thread_tweets = []
        for tweet_template in template:
            try:
                formatted_tweet = tweet_template.format(**thread_vars)
                thread_tweets.append(formatted_tweet)
            except KeyError:
                # Skip tweets with missing variables
                continue
        
        # Combine into thread format
        thread_text = "\n\n".join([f"{i+1}/ {tweet}" for i, tweet in enumerate(thread_tweets)])
        
        return {
            "text": thread_text,
            "is_thread": True,
            "tweet_count": len(thread_tweets)
        }

    def _generate_thread_variables(self, hook: ViralHook, 
                                 trend: Optional[TrendingTopic]) -> Dict[str, str]:
        """Generate variables for thread templates"""
        
        base_vars = {
            "hook": hook.hook_text,
            "business_name": random.choice(["Cafe Luna", "Bistro Verde", "Local Tapas", "Corner Deli"]),
            "specific_problem": random.choice([
                "inconsistent pricing during rush hours",
                "low table turnover rates", 
                "manual pricing decisions",
                "lack of customer insights"
            ]),
            "negative_metrics": random.choice([
                "20% lower margins during peak times",
                "Average table turnover: 45 minutes",
                "Pricing guesswork costing $2k/month",
                "Zero visibility into customer patterns"
            ]),
            "solution_name": "MenuFlow's AI pricing system",
            "timeframe": random.choice(["3 months", "6 weeks", "90 days"]),
            "positive_results": random.choice([
                "10% margin increase during peak hours",
                "25% faster table turnover",
                "15% revenue boost",
                "Real-time pricing optimization"
            ]),
            "unexpected_benefit": random.choice([
                "Staff stress reduced by 30%",
                "Customer satisfaction up 20%",
                "Decision-making time cut by 80%",
                "Competitive advantage in local market"
            ]),
            "key_takeaway": "Data-driven pricing beats guesswork every time",
            "call_to_action": "Start with peak-hour optimization"
        }
        
        # Add trend-specific variables
        if trend:
            base_vars.update({
                "data_point": f"trending topic: {trend.topic}",
                "sample_size": f"{trend.volume}+ businesses",
                "trend_statement": f"{trend.topic} is reshaping how businesses operate"
            })
        
        return base_vars

    def _generate_trend_context_line(self, trend: TrendingTopic) -> str:
        """Generate a line that connects SME Analytica to the trending topic"""
        
        if trend.trend_type == TrendType.HASHTAG:
            if "restaurant" in trend.topic.lower():
                return f"With {trend.topic} trending, restaurants need smarter pricing more than ever."
            elif "business" in trend.topic.lower():
                return f"Perfect timing - {trend.topic} highlights why SMEs need better analytics."
            elif "ai" in trend.topic.lower() or "tech" in trend.topic.lower():
                return f"{trend.topic} is exactly why we built AI-powered analytics for small businesses."
        
        return f"Jumping on {trend.topic} because this affects every small business owner."

    def _calculate_viral_score(self, content: Dict[str, Any], hook: ViralHook, 
                             trend: Optional[TrendingTopic]) -> float:
        """Calculate the viral potential score for generated content"""
        
        base_score = hook.viral_score
        
        # Content quality multipliers
        text = content["text"]
        
        # Length optimization (Twitter sweet spot: 71-100 characters get most engagement)
        length_score = 1.0
        if content.get("is_thread"):
            length_score = 1.2  # Threads often perform better
        elif 70 <= len(text) <= 100:
            length_score = 1.3
        elif 100 <= len(text) <= 280:
            length_score = 1.1
        elif len(text) > 280:
            length_score = 0.8  # Too long for optimal engagement
        
        # Emotional trigger presence
        emotion_score = 1.0
        emotion_words = {
            "urgency": ["now", "immediately", "before", "deadline", "limited"],
            "curiosity": ["secret", "hidden", "reveal", "discover", "why"],
            "social_proof": ["successful", "top", "proven", "results", "case"],
            "controversy": ["unpopular", "hot take", "disagree", "debate", "wrong"]
        }
        
        text_lower = text.lower()
        for emotion_type, words in emotion_words.items():
            if any(word in text_lower for word in words):
                emotion_score += 0.2
        
        # Trend relevance bonus
        trend_score = 1.0
        if trend:
            if trend.viral_potential == ViralPotential.VIRAL:
                trend_score = 1.5
            elif trend.viral_potential == ViralPotential.HIGH:
                trend_score = 1.3
            elif trend.viral_potential == ViralPotential.MEDIUM:
                trend_score = 1.1
        
        # Numbers and specificity bonus
        numbers_score = 1.0
        if re.search(r'\b\d+%\b', text):  # Percentages
            numbers_score += 0.2
        if re.search(r'\b\$\d+\b', text):  # Dollar amounts
            numbers_score += 0.2
        if re.search(r'\b\d+x\b', text):  # Multipliers
            numbers_score += 0.2
        
        final_score = base_score * length_score * emotion_score * trend_score * numbers_score
        return min(final_score, 10.0)  # Cap at 10.0

    def _generate_viral_hashtags(self, trend: Optional[TrendingTopic], 
                               content_type: str) -> List[str]:
        """Generate hashtags optimized for viral spread"""
        
        hashtags = ["#SMEAnalytica"]
        
        # Add trend hashtags if available
        if trend and trend.hashtags:
            hashtags.extend(trend.hashtags[:2])  # Max 2 trend hashtags
        
        # Content-type specific hashtags
        type_hashtags = {
            "thread": ["#Thread", "#BusinessTips"],
            "case_study": ["#CaseStudy", "#ROI"],
            "general": ["#AI", "#SmallBusiness"],
            "pricing": ["#DynamicPricing", "#RestaurantTech"],
            "analytics": ["#DataInsights", "#BusinessIntelligence"]
        }
        
        if content_type in type_hashtags:
            hashtags.extend(type_hashtags[content_type])
        
        # Add high-performing business hashtags
        viral_hashtags = [
            "#BusinessGrowth", "#Entrepreneur", "#RestaurantOwner", 
            "#AIforBusiness", "#SmartPricing", "#DataDriven"
        ]
        
        # Add one random viral hashtag
        hashtags.append(random.choice(viral_hashtags))
        
        # Ensure uniqueness and limit
        unique_hashtags = list(dict.fromkeys(hashtags))  # Preserve order, remove duplicates
        return unique_hashtags[:4]  # Twitter optimal: 1-2 hashtags, max 4

    def _calculate_timing_score(self, trend: Optional[TrendingTopic]) -> float:
        """Calculate how good the timing is for posting about this trend"""
        
        if not trend:
            return 5.0  # Neutral score for non-trend content
        
        # Time since trend discovery
        hours_since_discovery = (datetime.now() - trend.discovered_at).total_seconds() / 3600
        
        # Optimal window: 0.5-3 hours after discovery
        if 0.5 <= hours_since_discovery <= 3:
            timing_score = 9.0
        elif hours_since_discovery <= 6:
            timing_score = 7.0
        elif hours_since_discovery <= 12:
            timing_score = 5.0
        else:
            timing_score = 3.0  # Trend might be getting stale
        
        # Boost for high viral potential trends
        if trend.viral_potential == ViralPotential.VIRAL:
            timing_score += 1.0
        elif trend.viral_potential == ViralPotential.HIGH:
            timing_score += 0.5
        
        return min(timing_score, 10.0)

    def _identify_shareability_factors(self, content: Dict[str, Any], 
                                     hook: ViralHook) -> List[str]:
        """Identify what makes this content shareable"""
        
        factors = []
        text = content["text"].lower()
        
        # Practical value
        if any(word in text for word in ["how to", "tip", "strategy", "guide"]):
            factors.append("practical_value")
        
        # Emotional resonance
        if hook.emotional_trigger in ["curiosity", "fear", "aspiration"]:
            factors.append("emotional_resonance")
        
        # Social currency (makes sharer look good/smart)
        if any(word in text for word in ["insight", "secret", "data", "analysis"]):
            factors.append("social_currency")
        
        # Debate triggering
        if any(word in text for word in ["opinion", "take", "disagree", "debate"]):
            factors.append("triggering_debates")
        
        # Surprising insights
        if any(word in text for word in ["surprising", "unexpected", "plot twist"]):
            factors.append("surprising_insights")
        
        # Actionable advice
        if any(word in text for word in ["start", "try", "implement", "action"]):
            factors.append("actionable_advice")
        
        # Data-driven content
        if re.search(r'\b\d+%', text) or "analysis" in text:
            factors.append("data_driven")
        
        return factors

    def _estimate_reach(self, viral_score: float, timing_score: float, 
                       trend: Optional[TrendingTopic]) -> int:
        """Estimate potential reach based on various factors"""
        
        # Base reach (current follower count + typical amplification)
        base_reach = 50  # Current small following
        
        # Viral score multiplier
        viral_multiplier = viral_score / 5.0  # Normalize to reasonable range
        
        # Timing multiplier
        timing_multiplier = timing_score / 10.0
        
        # Trend amplification
        trend_multiplier = 1.0
        if trend:
            if trend.viral_potential == ViralPotential.VIRAL:
                trend_multiplier = 5.0
            elif trend.viral_potential == ViralPotential.HIGH:
                trend_multiplier = 3.0
            elif trend.viral_potential == ViralPotential.MEDIUM:
                trend_multiplier = 2.0
        
        estimated_reach = int(base_reach * viral_multiplier * timing_multiplier * trend_multiplier)
        
        # Add some randomness for realism
        variance = random.uniform(0.8, 1.2)
        return int(estimated_reach * variance)

    async def analyze_hashtag_viral_potential(self, hashtags: List[str]) -> Dict[str, Dict[str, Any]]:
        """Analyze the viral potential of specific hashtags"""
        
        analysis_results = {}
        
        for hashtag in hashtags:
            try:
                # Get recent tweets with this hashtag
                tweets = await self.twitter_manager.search_tweets(
                    hashtag, max_results=100
                )
                
                if tweets:
                    analysis = self._analyze_hashtag_performance(hashtag, tweets)
                    analysis_results[hashtag] = analysis
                else:
                    analysis_results[hashtag] = {
                        "viral_potential": ViralPotential.LOW,
                        "volume": 0,
                        "engagement_rate": 0,
                        "recommendation": "Low activity - consider alternatives"
                    }
                
                # Rate limiting
                await asyncio.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Error analyzing hashtag {hashtag}: {e}")
                analysis_results[hashtag] = {
                    "error": str(e),
                    "viral_potential": ViralPotential.LOW
                }
        
        return analysis_results

    def _analyze_hashtag_performance(self, hashtag: str, tweets: List[Tweet]) -> Dict[str, Any]:
        """Analyze performance metrics for a specific hashtag"""
        
        if not tweets:
            return {
                "viral_potential": ViralPotential.LOW,
                "volume": 0,
                "engagement_rate": 0,
                "recommendation": "No recent activity"
            }
        
        # Calculate metrics
        total_engagement = sum(
            tweet.public_metrics.get('like_count', 0) +
            tweet.public_metrics.get('retweet_count', 0) +
            tweet.public_metrics.get('reply_count', 0)
            for tweet in tweets
        )
        
        avg_engagement = total_engagement / len(tweets)
        volume = len(tweets)
        
        # Recent activity (last 24 hours)
        recent_cutoff = datetime.now() - timedelta(hours=24)
        recent_tweets = [t for t in tweets if 
                        t.created_at.replace(tzinfo=None) > recent_cutoff]
        recent_ratio = len(recent_tweets) / len(tweets)
        
        # Determine viral potential
        viral_potential = ViralPotential.LOW
        if avg_engagement > 100 and recent_ratio > 0.3:
            viral_potential = ViralPotential.VIRAL
        elif avg_engagement > 50 and recent_ratio > 0.2:
            viral_potential = ViralPotential.HIGH
        elif avg_engagement > 20 or recent_ratio > 0.4:
            viral_potential = ViralPotential.MEDIUM
        
        # Generate recommendation
        recommendation = f"Use if targeting {viral_potential} engagement"
        if viral_potential == ViralPotential.VIRAL:
            recommendation = "🔥 High viral potential - use immediately!"
        elif viral_potential == ViralPotential.HIGH:
            recommendation = "⚡ Good potential - recommended for important posts"
        elif viral_potential == ViralPotential.LOW and volume < 10:
            recommendation = "Consider more popular alternatives"
        
        return {
            "viral_potential": viral_potential,
            "volume": volume,
            "avg_engagement": avg_engagement,
            "recent_activity_ratio": recent_ratio,
            "engagement_rate": avg_engagement / max(volume, 1),
            "recommendation": recommendation,
            "top_performing_tweets": sorted(tweets, 
                                          key=lambda t: sum(t.public_metrics.values()), 
                                          reverse=True)[:3]
        }

    async def get_daily_viral_opportunities(self, count: int = 10) -> List[Dict[str, Any]]:
        """Get top viral opportunities for the day"""
        
        # Monitor current trends
        trending_topics = await self.monitor_trending_topics()
        
        opportunities = []
        
        # Generate opportunities from trends
        for trend in trending_topics[:5]:  # Top 5 trends
            if trend.viral_potential in [ViralPotential.HIGH, ViralPotential.VIRAL]:
                viral_content = await self.generate_viral_content(trend, "general")
                
                opportunity = {
                    "type": "trend_opportunity",
                    "trend": trend,
                    "content": viral_content,
                    "priority": self._calculate_opportunity_priority(trend, viral_content),
                    "optimal_posting_time": trend.optimal_timing,
                    "expected_engagement": self._estimate_engagement(viral_content)
                }
                opportunities.append(opportunity)
        
        # Generate thread opportunities
        thread_content = await self.generate_viral_content(None, "thread")
        thread_opportunity = {
            "type": "thread_opportunity",
            "trend": None,
            "content": thread_content,
            "priority": 7.0,  # Threads generally perform well
            "optimal_posting_time": datetime.now() + timedelta(hours=2),
            "expected_engagement": self._estimate_engagement(thread_content)
        }
        opportunities.append(thread_opportunity)
        
        # Sort by priority
        opportunities.sort(key=lambda x: x["priority"], reverse=True)
        
        return opportunities[:count]

    def _calculate_opportunity_priority(self, trend: TrendingTopic, 
                                      content: ViralContent) -> float:
        """Calculate priority score for an opportunity"""
        
        # Base score from trend viral potential
        base_score = {
            ViralPotential.VIRAL: 9.0,
            ViralPotential.HIGH: 7.0,
            ViralPotential.MEDIUM: 5.0,
            ViralPotential.LOW: 3.0
        }[trend.viral_potential]
        
        # Content quality bonus
        content_bonus = (content.viral_score - 5.0) * 0.5
        
        # Timing bonus
        timing_bonus = content.timing_score / 10.0
        
        # Relevance bonus
        relevance_bonus = trend.relevance_score / 10.0
        
        return base_score + content_bonus + timing_bonus + relevance_bonus

    def _estimate_engagement(self, content: ViralContent) -> Dict[str, int]:
        """Estimate expected engagement metrics"""
        
        base_engagement = content.estimated_reach * 0.1  # 10% engagement rate
        
        # Distribute across engagement types
        likes = int(base_engagement * 0.7)  # 70% likes
        retweets = int(base_engagement * 0.2)  # 20% retweets  
        replies = int(base_engagement * 0.1)  # 10% replies
        
        return {
            "likes": likes,
            "retweets": retweets, 
            "replies": replies,
            "total": likes + retweets + replies
        }

    def get_viral_analytics_dashboard(self) -> Dict[str, Any]:
        """Generate analytics dashboard for viral content performance"""
        
        current_time = datetime.now()
        
        # Recent performance
        recent_content = [c for c in self.content_performance_history 
                         if (current_time - c["generated_at"]).days <= 7]
        
        recent_trends = [t for t in self.trend_tracking_history 
                        if (current_time - t["timestamp"]).days <= 7]
        
        # Calculate metrics
        avg_viral_score = sum(c["viral_score"] for c in recent_content) / len(recent_content) if recent_content else 0
        trends_monitored = sum(t["topics_found"] for t in recent_trends) if recent_trends else 0
        high_potential_trends = sum(t["high_potential_count"] for t in recent_trends) if recent_trends else 0
        
        # Get current cache status
        cache_status = "Fresh" if (
            self.trending_topics_cache and 
            (current_time - self.trending_topics_cache["last_updated"]).total_seconds() < 3600
        ) else "Stale"
        
        return {
            "viral_content_metrics": {
                "content_generated_last_7_days": len(recent_content),
                "average_viral_score": round(avg_viral_score, 2),
                "high_scoring_content": len([c for c in recent_content if c["viral_score"] > 8.0])
            },
            "trend_monitoring": {
                "trends_monitored_last_7_days": trends_monitored,
                "high_potential_trends_found": high_potential_trends,
                "cache_status": cache_status,
                "last_monitoring_update": self.trending_topics_cache.get("last_updated") if self.trending_topics_cache else None
            },
            "viral_hooks_available": len(self.viral_hooks),
            "thread_templates_available": len(self.thread_templates),
            "success_rate": f"{(high_potential_trends / max(trends_monitored, 1)) * 100:.1f}%" if trends_monitored > 0 else "0%"
        }