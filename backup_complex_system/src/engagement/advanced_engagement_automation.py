"""
Advanced engagement automation system with growth intelligence
"""

import asyncio
import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass
import random
import re
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class EngagementStrategy(str, Enum):
    INFLUENCER_TARGETING = "influencer_targeting"
    COMMUNITY_BUILDING = "community_building"
    TREND_RIDING = "trend_riding"
    CONVERSION_FOCUSED = "conversion_focused"
    BRAND_AWARENESS = "brand_awareness"
    VIRAL_AMPLIFICATION = "viral_amplification"

class EngagementType(str, Enum):
    LIKE = "like"
    RETWEET = "retweet"
    REPLY = "reply"
    QUOTE_TWEET = "quote_tweet"
    FOLLOW = "follow"
    UNFOLLOW = "unfollow"
    THREAD_REPLY = "thread_reply"

@dataclass
class EngagementTarget:
    """Target for engagement activities"""
    username: str
    follower_count: int
    engagement_rate: float
    relevance_score: float
    influence_level: str
    target_type: str  # influencer, competitor, customer, prospect
    last_engagement: Optional[datetime] = None
    engagement_history: List[str] = None

@dataclass
class EngagementOpportunity:
    """Engagement opportunity with scoring"""
    tweet_id: str
    author: str
    content: str
    engagement_score: float
    strategy: EngagementStrategy
    action_type: EngagementType
    urgency: int  # 1-10
    potential_reach: int
    brand_alignment: float
    conversion_potential: float

class AdvancedEngagementAutomation:
    """Advanced engagement automation with AI-driven targeting"""
    
    def __init__(self):
        self.engagement_targets = {}
        self.engagement_history = []
        self.daily_limits = self._initialize_daily_limits()
        self.strategy_weights = self._initialize_strategy_weights()
        self.keyword_targets = self._initialize_keyword_targets()
        self.influencer_database = self._initialize_influencer_database()
        self.engagement_templates = self._initialize_engagement_templates()
        self.growth_targets = self._initialize_growth_targets()
    
    def _initialize_daily_limits(self) -> Dict[str, int]:
        """Initialize daily engagement limits to avoid spam detection"""
        return {
            "total_engagements": 100,
            "likes": 50,
            "retweets": 25,
            "replies": 20,
            "follows": 20,
            "unfollows": 10,
            "quote_tweets": 5
        }
    
    def _initialize_strategy_weights(self) -> Dict[EngagementStrategy, float]:
        """Initialize strategy weights for balanced growth"""
        return {
            EngagementStrategy.INFLUENCER_TARGETING: 0.25,
            EngagementStrategy.COMMUNITY_BUILDING: 0.20,
            EngagementStrategy.TREND_RIDING: 0.20,
            EngagementStrategy.CONVERSION_FOCUSED: 0.15,
            EngagementStrategy.BRAND_AWARENESS: 0.10,
            EngagementStrategy.VIRAL_AMPLIFICATION: 0.10
        }
    
    def _initialize_keyword_targets(self) -> Dict[str, Dict[str, Any]]:
        """Initialize keyword targeting for SME Analytica"""
        return {
            "primary_keywords": {
                "restaurant_analytics": {"weight": 10, "urgency": 9},
                "dynamic_pricing": {"weight": 10, "urgency": 9},
                "menuflow": {"weight": 9, "urgency": 8},
                "restaurant_tech": {"weight": 8, "urgency": 7},
                "pos_integration": {"weight": 8, "urgency": 7},
                "hospitality_ai": {"weight": 7, "urgency": 6}
            },
            "secondary_keywords": {
                "small_business": {"weight": 6, "urgency": 5},
                "business_analytics": {"weight": 6, "urgency": 5},
                "restaurant_owner": {"weight": 5, "urgency": 4},
                "hotel_management": {"weight": 5, "urgency": 4},
                "retail_analytics": {"weight": 4, "urgency": 3}
            },
            "trending_keywords": {
                "ai_revolution": {"weight": 8, "urgency": 8},
                "business_intelligence": {"weight": 7, "urgency": 7},
                "digital_transformation": {"weight": 6, "urgency": 6},
                "data_driven": {"weight": 6, "urgency": 5}
            }
        }
    
    def _initialize_influencer_database(self) -> List[EngagementTarget]:
        """Initialize database of target influencers and accounts"""
        return [
            # Restaurant Industry Influencers
            EngagementTarget("RestaurantOwner", 15000, 0.08, 9.0, "micro", "influencer"),
            EngagementTarget("ChefTalk", 25000, 0.06, 8.5, "micro", "influencer"),
            EngagementTarget("HospitalityTech", 12000, 0.12, 9.5, "micro", "influencer"),
            EngagementTarget("RestaurantBiz", 35000, 0.05, 8.0, "macro", "influencer"),
            
            # Business & Tech Influencers
            EngagementTarget("SmallBizTips", 45000, 0.04, 7.5, "macro", "influencer"),
            EngagementTarget("BusinessAI", 20000, 0.07, 8.5, "micro", "influencer"),
            EngagementTarget("RetailTech", 18000, 0.09, 8.0, "micro", "influencer"),
            
            # Industry Publications & Communities
            EngagementTarget("RestaurantNews", 55000, 0.03, 9.0, "macro", "media"),
            EngagementTarget("HospitalityNet", 30000, 0.05, 8.5, "macro", "media"),
            EngagementTarget("NationRestNews", 85000, 0.02, 9.5, "macro", "media"),
            
            # Competitors (for competitive intelligence)
            EngagementTarget("ToastPOS", 75000, 0.04, 6.0, "macro", "competitor"),
            EngagementTarget("SquareUp", 250000, 0.02, 5.5, "mega", "competitor"),
            EngagementTarget("OpenTable", 180000, 0.03, 6.5, "mega", "competitor"),
            
            # Target Customers
            EngagementTarget("RestaurantOwners", 8000, 0.15, 9.5, "micro", "customer"),
            EngagementTarget("HotelManagers", 6000, 0.18, 9.0, "micro", "customer"),
            EngagementTarget("RetailBusiness", 12000, 0.12, 8.5, "micro", "customer")
        ]
    
    def _initialize_engagement_templates(self) -> Dict[EngagementStrategy, Dict[str, List[str]]]:
        """Initialize engagement templates for different strategies"""
        return {
            EngagementStrategy.INFLUENCER_TARGETING: {
                "replies": [
                    "Great insight! At SME Analytica, we've seen similar trends with AI-powered analytics helping restaurants optimize pricing in real-time. Would love to share some data on this! 📊",
                    "This aligns perfectly with what we're seeing in the restaurant analytics space. MenuFlow's dynamic pricing has helped establishments boost margins by ~10% during peak hours. 🚀",
                    "Fantastic point! Our AI analytics platform has helped 500+ restaurants discover these exact opportunities through data-driven insights. Happy to discuss further! 💡",
                    "Absolutely agree! Data analytics transforms restaurant operations. We've documented similar results with MenuFlow - would be interesting to compare insights! 📈"
                ],
                "quote_tweets": [
                    "💯 This! Real-time analytics are game-changing for restaurants. MenuFlow users report 10% margin improvements during peak hours through AI-powered dynamic pricing.",
                    "Spot on! 📊 SME Analytica's research shows 73% of restaurants underutilize their POS data. The opportunity for growth is massive with the right analytics tools.",
                    "This is exactly why we built MenuFlow! 🎯 Seamless POS integration + AI pricing = competitive advantage for restaurant owners."
                ]
            },
            EngagementStrategy.COMMUNITY_BUILDING: {
                "replies": [
                    "We'd love to help with that! SME Analytica specializes in making complex analytics simple for restaurant owners. Feel free to reach out if you have specific questions! 🤝",
                    "The restaurant community is amazing! We're passionate about helping owners succeed with data-driven insights. Always happy to share what we've learned! 💪",
                    "Great question from the community! In our experience with 500+ restaurants, the key is starting simple - track peak hours, then optimize pricing. Want to share more insights! 📊",
                    "Love seeing restaurant owners support each other! We're here to provide analytics insights whenever the community needs them. Growth through collaboration! 🚀"
                ]
            },
            EngagementStrategy.TREND_RIDING: {
                "replies": [
                    "The AI revolution in hospitality is just getting started! 🔥 MenuFlow's dynamic pricing shows how AI can immediately boost restaurant profitability. Exciting times ahead!",
                    "This trend is reshaping the industry! 📈 We're seeing restaurants embrace AI analytics for pricing optimization, inventory management, and customer insights. The future is data-driven!",
                    "Riding this wave with restaurant owners! 🌊 AI-powered analytics are no longer luxury - they're necessity for competitive restaurants. MenuFlow makes it accessible to all."
                ]
            },
            EngagementStrategy.CONVERSION_FOCUSED: {
                "replies": [
                    "This resonates with many restaurant owners we work with! If you're interested in seeing how AI analytics can transform operations, we offer free 15-min demos of MenuFlow. DM us! 📩",
                    "Sounds like you're dealing with the exact challenges MenuFlow solves! 🎯 We've helped similar restaurants boost margins 10%+ through dynamic pricing. Happy to show you how!",
                    "We help restaurants solve this exact problem! 💡 MenuFlow's real-time analytics + AI pricing optimization has transformed 500+ establishments. Free consultation available!"
                ]
            },
            EngagementStrategy.VIRAL_AMPLIFICATION: {
                "retweets_with_comment": [
                    "🚨 This! Every restaurant owner should read this thread. The data insights are spot-on with what we see through MenuFlow analytics.",
                    "💯 FACTS! This is exactly why AI-powered restaurant analytics are becoming essential. Retweet if you agree! 🔄",
                    "🔥 This thread is pure gold for restaurant owners! The analytics opportunities mentioned here align perfectly with MenuFlow's capabilities."
                ]
            }
        }
    
    def _initialize_growth_targets(self) -> Dict[str, Dict[str, int]]:
        """Initialize 4-week growth targets"""
        return {
            "week_1": {"follower_target": 50, "engagement_quota": 350, "conversion_target": 5},
            "week_2": {"follower_target": 150, "engagement_quota": 490, "conversion_target": 10},
            "week_3": {"follower_target": 300, "engagement_quota": 630, "conversion_target": 20},
            "week_4": {"follower_target": 500, "engagement_quota": 700, "conversion_target": 30}
        }
    
    async def identify_engagement_opportunities(self, tweets_data: List[Dict[str, Any]], 
                                              current_week: int = 1) -> List[EngagementOpportunity]:
        """Identify and score engagement opportunities using AI"""
        opportunities = []
        
        for tweet in tweets_data:
            opportunity = await self._analyze_tweet_opportunity(tweet, current_week)
            if opportunity and opportunity.engagement_score >= 6.0:
                opportunities.append(opportunity)
        
        # Sort by engagement score and urgency
        opportunities.sort(key=lambda x: (x.engagement_score, x.urgency), reverse=True)
        
        return opportunities[:50]  # Return top 50 opportunities
    
    async def _analyze_tweet_opportunity(self, tweet: Dict[str, Any], 
                                       current_week: int) -> Optional[EngagementOpportunity]:
        """Analyze individual tweet for engagement opportunity"""
        
        content = tweet.get('text', '').lower()
        author = tweet.get('author', '')
        tweet_id = tweet.get('id', '')
        
        # Calculate relevance score
        relevance_score = self._calculate_relevance_score(content)
        if relevance_score < 3.0:
            return None
        
        # Calculate engagement score
        engagement_score = self._calculate_engagement_score(tweet, relevance_score)
        
        # Determine strategy and action
        strategy = self._determine_engagement_strategy(tweet, current_week)
        action_type = self._determine_action_type(tweet, strategy)
        
        # Calculate metrics
        urgency = self._calculate_urgency(tweet, strategy)
        potential_reach = self._estimate_reach(tweet)
        brand_alignment = self._calculate_brand_alignment(content)
        conversion_potential = self._calculate_conversion_potential(tweet, strategy)
        
        return EngagementOpportunity(
            tweet_id=tweet_id,
            author=author,
            content=content,
            engagement_score=engagement_score,
            strategy=strategy,
            action_type=action_type,
            urgency=urgency,
            potential_reach=potential_reach,
            brand_alignment=brand_alignment,
            conversion_potential=conversion_potential
        )
    
    def _calculate_relevance_score(self, content: str) -> float:
        """Calculate relevance score based on keywords"""
        score = 0.0
        
        # Check primary keywords
        for keyword, data in self.keyword_targets["primary_keywords"].items():
            if keyword.replace('_', ' ') in content:
                score += data["weight"]
        
        # Check secondary keywords
        for keyword, data in self.keyword_targets["secondary_keywords"].items():
            if keyword.replace('_', ' ') in content:
                score += data["weight"] * 0.7
        
        # Check trending keywords
        for keyword, data in self.keyword_targets["trending_keywords"].items():
            if keyword.replace('_', ' ') in content:
                score += data["weight"] * 0.8
        
        return min(score, 10.0)
    
    def _calculate_engagement_score(self, tweet: Dict[str, Any], relevance_score: float) -> float:
        """Calculate overall engagement score"""
        
        # Base relevance score
        score = relevance_score
        
        # Author influence factor
        follower_count = tweet.get('author_followers', 0)
        influence_factor = min(follower_count / 10000, 2.0)  # Cap at 2x multiplier
        score += influence_factor
        
        # Engagement metrics
        likes = tweet.get('like_count', 0)
        retweets = tweet.get('retweet_count', 0)
        replies = tweet.get('reply_count', 0)
        
        engagement_rate = (likes + retweets * 2 + replies * 3) / max(follower_count, 1) * 1000
        score += min(engagement_rate, 3.0)
        
        # Timing factor (newer tweets get higher scores)
        tweet_age_hours = tweet.get('age_hours', 24)
        timing_factor = max(1.0 - (tweet_age_hours / 24), 0.2)
        score *= timing_factor
        
        return min(score, 10.0)
    
    def _determine_engagement_strategy(self, tweet: Dict[str, Any], current_week: int) -> EngagementStrategy:
        """Determine best engagement strategy for tweet"""
        
        author = tweet.get('author', '')
        content = tweet.get('text', '').lower()
        follower_count = tweet.get('author_followers', 0)
        
        # Check if author is in influencer database
        target = next((t for t in self.influencer_database if t.username.lower() in author.lower()), None)
        
        if target:
            if target.target_type == "influencer":
                return EngagementStrategy.INFLUENCER_TARGETING
            elif target.target_type == "competitor":
                return EngagementStrategy.BRAND_AWARENESS
            elif target.target_type == "customer":
                return EngagementStrategy.CONVERSION_FOCUSED
        
        # Strategy based on content type
        if any(word in content for word in ['trending', 'viral', 'breaking', 'news']):
            return EngagementStrategy.TREND_RIDING
        
        if any(word in content for word in ['question', 'help', 'advice', 'how to']):
            return EngagementStrategy.COMMUNITY_BUILDING
        
        # Week-based strategy weights
        week_strategies = {
            1: EngagementStrategy.FOLLOWER_ACQUISITION,
            2: EngagementStrategy.COMMUNITY_BUILDING,
            3: EngagementStrategy.VIRAL_AMPLIFICATION,
            4: EngagementStrategy.CONVERSION_FOCUSED
        }
        
        return week_strategies.get(current_week, EngagementStrategy.COMMUNITY_BUILDING)
    
    def _determine_action_type(self, tweet: Dict[str, Any], strategy: EngagementStrategy) -> EngagementType:
        """Determine best action type for engagement"""
        
        content = tweet.get('text', '').lower()
        
        # Strategy-based action preferences
        strategy_actions = {
            EngagementStrategy.INFLUENCER_TARGETING: [EngagementType.REPLY, EngagementType.QUOTE_TWEET],
            EngagementStrategy.COMMUNITY_BUILDING: [EngagementType.REPLY, EngagementType.LIKE],
            EngagementStrategy.TREND_RIDING: [EngagementType.RETWEET, EngagementType.QUOTE_TWEET],
            EngagementStrategy.CONVERSION_FOCUSED: [EngagementType.REPLY, EngagementType.QUOTE_TWEET],
            EngagementStrategy.VIRAL_AMPLIFICATION: [EngagementType.RETWEET, EngagementType.QUOTE_TWEET],
            EngagementStrategy.BRAND_AWARENESS: [EngagementType.LIKE, EngagementType.RETWEET]
        }
        
        preferred_actions = strategy_actions.get(strategy, [EngagementType.LIKE])
        
        # Content-based action selection
        if '?' in content:  # Questions deserve replies
            return EngagementType.REPLY
        elif any(word in content for word in ['great', 'amazing', 'excellent']):
            return EngagementType.LIKE
        elif any(word in content for word in ['share', 'retweet', 'spread']):
            return EngagementType.RETWEET
        
        return random.choice(preferred_actions)
    
    def _calculate_urgency(self, tweet: Dict[str, Any], strategy: EngagementStrategy) -> int:
        """Calculate engagement urgency (1-10)"""
        
        urgency = 5  # Base urgency
        
        # Time-sensitive content
        content = tweet.get('text', '').lower()
        if any(word in content for word in ['breaking', 'urgent', 'now', 'today']):
            urgency += 3
        
        # Strategy urgency
        if strategy == EngagementStrategy.TREND_RIDING:
            urgency += 2
        elif strategy == EngagementStrategy.INFLUENCER_TARGETING:
            urgency += 1
        
        # High engagement tweets need immediate response
        engagement_count = tweet.get('like_count', 0) + tweet.get('retweet_count', 0)
        if engagement_count > 100:
            urgency += 2
        
        return min(urgency, 10)
    
    def _estimate_reach(self, tweet: Dict[str, Any]) -> int:
        """Estimate potential reach of engagement"""
        
        author_followers = tweet.get('author_followers', 0)
        engagement_count = tweet.get('like_count', 0) + tweet.get('retweet_count', 0)
        
        # Base reach is author's followers
        reach = author_followers
        
        # Viral content multiplier
        if engagement_count > author_followers * 0.05:  # High engagement rate
            reach *= 2
        
        # Thread or popular content
        if tweet.get('reply_count', 0) > 20:
            reach *= 1.5
        
        return int(reach)
    
    def _calculate_brand_alignment(self, content: str) -> float:
        """Calculate how well content aligns with SME Analytica brand"""
        
        alignment_score = 5.0  # Neutral baseline
        
        # Positive brand alignment keywords
        positive_keywords = [
            'restaurant', 'analytics', 'data', 'pricing', 'ai', 'automation',
            'small business', 'hospitality', 'pos', 'integration', 'revenue',
            'profit', 'optimization', 'efficiency', 'growth'
        ]
        
        for keyword in positive_keywords:
            if keyword in content:
                alignment_score += 0.5
        
        # Negative brand alignment keywords
        negative_keywords = [
            'spam', 'scam', 'fake', 'illegal', 'controversial', 'politics',
            'religion', 'personal attack', 'harassment'
        ]
        
        for keyword in negative_keywords:
            if keyword in content:
                alignment_score -= 2.0
        
        return max(min(alignment_score, 10.0), 0.0)
    
    def _calculate_conversion_potential(self, tweet: Dict[str, Any], strategy: EngagementStrategy) -> float:
        """Calculate potential for converting engagement to business value"""
        
        potential = 3.0  # Base potential
        content = tweet.get('text', '').lower()
        
        # High conversion indicators
        if any(word in content for word in ['looking for', 'need help', 'recommendations', 'advice']):
            potential += 3.0
        
        if any(word in content for word in ['restaurant owner', 'small business', 'pos system']):
            potential += 2.0
        
        # Strategy-based conversion potential
        strategy_multipliers = {
            EngagementStrategy.CONVERSION_FOCUSED: 2.0,
            EngagementStrategy.INFLUENCER_TARGETING: 1.5,
            EngagementStrategy.COMMUNITY_BUILDING: 1.3,
            EngagementStrategy.BRAND_AWARENESS: 1.0,
            EngagementStrategy.VIRAL_AMPLIFICATION: 0.8,
            EngagementStrategy.TREND_RIDING: 0.7
        }
        
        potential *= strategy_multipliers.get(strategy, 1.0)
        
        return min(potential, 10.0)
    
    async def generate_engagement_response(self, opportunity: EngagementOpportunity) -> str:
        """Generate appropriate response for engagement opportunity"""
        
        strategy = opportunity.strategy
        action_type = opportunity.action_type
        
        if action_type == EngagementType.REPLY:
            templates = self.engagement_templates[strategy]["replies"]
            return random.choice(templates)
        elif action_type == EngagementType.QUOTE_TWEET:
            if "quote_tweets" in self.engagement_templates[strategy]:
                templates = self.engagement_templates[strategy]["quote_tweets"]
                return random.choice(templates)
            else:
                templates = self.engagement_templates[strategy]["replies"]
                return random.choice(templates)
        elif action_type == EngagementType.RETWEET:
            if "retweets_with_comment" in self.engagement_templates[strategy]:
                templates = self.engagement_templates[strategy]["retweets_with_comment"]
                return random.choice(templates)
        
        return ""  # No response needed for likes, follows, etc.
    
    async def execute_engagement_plan(self, opportunities: List[EngagementOpportunity], 
                                    current_week: int = 1) -> Dict[str, Any]:
        """Execute engagement plan with rate limiting and safety checks"""
        
        executed_engagements = []
        daily_counts = {action.value: 0 for action in EngagementType}
        
        # Week-based targets
        week_targets = self.growth_targets[f"week_{current_week}"]
        target_engagements = week_targets["engagement_quota"] // 7  # Daily target
        
        for opportunity in opportunities:
            # Check daily limits
            if daily_counts[opportunity.action_type.value] >= self.daily_limits.get(opportunity.action_type.value, 10):
                continue
            
            if sum(daily_counts.values()) >= target_engagements:
                break
            
            # Generate response if needed
            response = await self.generate_engagement_response(opportunity)
            
            # Record engagement (in production, this would execute the actual engagement)
            executed_engagements.append({
                "opportunity": opportunity,
                "response": response,
                "timestamp": datetime.now(),
                "status": "executed"
            })
            
            daily_counts[opportunity.action_type.value] += 1
            
            # Add realistic delay between engagements
            await asyncio.sleep(random.uniform(30, 180))  # 30 seconds to 3 minutes
        
        return {
            "executed_count": len(executed_engagements),
            "daily_counts": daily_counts,
            "target_engagements": target_engagements,
            "completion_rate": len(executed_engagements) / target_engagements * 100,
            "engagements": executed_engagements
        }
    
    def get_weekly_engagement_strategy(self, week: int) -> Dict[str, Any]:
        """Get comprehensive engagement strategy for specific week"""
        
        week_focuses = {
            1: {
                "primary_strategy": EngagementStrategy.COMMUNITY_BUILDING,
                "secondary_strategies": [EngagementStrategy.INFLUENCER_TARGETING, EngagementStrategy.BRAND_AWARENESS],
                "focus_description": "Foundation building and initial community engagement",
                "target_accounts": ["RestaurantOwners", "SmallBizTips", "HospitalityTech"],
                "content_themes": ["educational", "helpful", "non-promotional"],
                "daily_engagement_target": 50
            },
            2: {
                "primary_strategy": EngagementStrategy.INFLUENCER_TARGETING,
                "secondary_strategies": [EngagementStrategy.COMMUNITY_BUILDING, EngagementStrategy.TREND_RIDING],
                "focus_description": "Influencer outreach and industry relationship building",
                "target_accounts": ["RestaurantBiz", "ChefTalk", "BusinessAI"],
                "content_themes": ["industry_insights", "data_sharing", "thought_leadership"],
                "daily_engagement_target": 70
            },
            3: {
                "primary_strategy": EngagementStrategy.VIRAL_AMPLIFICATION,
                "secondary_strategies": [EngagementStrategy.TREND_RIDING, EngagementStrategy.COMMUNITY_BUILDING],
                "focus_description": "Viral content amplification and trend participation",
                "target_accounts": ["RestaurantNews", "HospitalityNet", "NationRestNews"],
                "content_themes": ["trending_topics", "viral_content", "shareworthy_insights"],
                "daily_engagement_target": 90
            },
            4: {
                "primary_strategy": EngagementStrategy.CONVERSION_FOCUSED,
                "secondary_strategies": [EngagementStrategy.INFLUENCER_TARGETING, EngagementStrategy.COMMUNITY_BUILDING],
                "focus_description": "Conversion optimization and business development",
                "target_accounts": ["RestaurantOwners", "HotelManagers", "RetailBusiness"],
                "content_themes": ["value_proposition", "case_studies", "demo_invitations"],
                "daily_engagement_target": 100
            }
        }
        
        return week_focuses.get(week, week_focuses[1])

# Test the engagement automation
if __name__ == "__main__":
    automation = AdvancedEngagementAutomation()
    
    # Test opportunity identification
    sample_tweets = [
        {
            "id": "123456789",
            "text": "Looking for the best restaurant analytics platform. Need something that integrates with our POS system and helps with pricing optimization. Any recommendations?",
            "author": "RestaurantOwnerJohn",
            "author_followers": 1200,
            "like_count": 5,
            "retweet_count": 2,
            "reply_count": 8,
            "age_hours": 2
        }
    ]
    
    async def test_automation():
        opportunities = await automation.identify_engagement_opportunities(sample_tweets, 1)
        for opp in opportunities:
            print(f"Opportunity: {opp.engagement_score:.2f} score - {opp.strategy.value} - {opp.action_type.value}")
            response = await automation.generate_engagement_response(opp)
            print(f"Response: {response}\n")
    
    asyncio.run(test_automation())