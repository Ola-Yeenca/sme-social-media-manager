#!/usr/bin/env python3
"""
Intelligent Hashtag Tracking System for SME Analytica
Monitors hashtags, analyzes trends, and identifies engagement opportunities
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import json

class HashtagPriority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    TRENDING = "trending"

@dataclass
class HashtagMetrics:
    """Metrics for hashtag performance"""
    hashtag: str
    volume: int  # Number of posts
    engagement_rate: float
    reach_estimate: int
    sentiment_score: float
    relevance_score: float
    trending_velocity: float  # Rate of growth
    last_updated: datetime

@dataclass
class HashtagOpportunity:
    """Engagement opportunity from hashtag monitoring"""
    hashtag: str
    tweet_id: str
    author: str
    content: str
    opportunity_score: float
    engagement_potential: float
    conversion_likelihood: float
    urgency: int
    discovered_at: datetime

class IntelligentHashtagTracker:
    """Advanced hashtag tracking with AI-powered opportunity identification"""
    
    def __init__(self, twitter_manager, ai_provider):
        self.twitter_manager = twitter_manager
        self.ai_provider = ai_provider
        self.logger = logging.getLogger(__name__)
        
        # Hashtag configuration
        self.hashtag_config = self._initialize_hashtag_config()
        self.tracking_metrics = {}
        self.opportunity_history = []
        
        # Performance tracking
        self.session_stats = {
            "hashtags_monitored": 0,
            "opportunities_found": 0,
            "high_value_opportunities": 0,
            "trending_hashtags_discovered": 0,
            "start_time": datetime.now()
        }

    def _initialize_hashtag_config(self) -> Dict[str, Any]:
        """Initialize hashtag tracking configuration"""
        return {
            "primary_hashtags": {
                "#RestaurantTech": {"priority": HashtagPriority.HIGH, "weight": 10},
                "#SMEAnalytics": {"priority": HashtagPriority.HIGH, "weight": 10},
                "#MenuOptimization": {"priority": HashtagPriority.HIGH, "weight": 9},
                "#RestaurantData": {"priority": HashtagPriority.HIGH, "weight": 9},
                "#HospitalityAI": {"priority": HashtagPriority.HIGH, "weight": 8},
                "#DynamicPricing": {"priority": HashtagPriority.HIGH, "weight": 8},
                "#POSIntegration": {"priority": HashtagPriority.HIGH, "weight": 8},
                "#RestaurantAnalytics": {"priority": HashtagPriority.HIGH, "weight": 9},
                "#MenuFlow": {"priority": HashtagPriority.HIGH, "weight": 10}
            },
            "secondary_hashtags": {
                "#SmallBusiness": {"priority": HashtagPriority.MEDIUM, "weight": 6},
                "#BusinessIntelligence": {"priority": HashtagPriority.MEDIUM, "weight": 7},
                "#DataDriven": {"priority": HashtagPriority.MEDIUM, "weight": 6},
                "#RestaurantOwner": {"priority": HashtagPriority.MEDIUM, "weight": 7},
                "#HotelTech": {"priority": HashtagPriority.MEDIUM, "weight": 6},
                "#RetailAnalytics": {"priority": HashtagPriority.MEDIUM, "weight": 6},
                "#AIForBusiness": {"priority": HashtagPriority.MEDIUM, "weight": 7},
                "#DigitalTransformation": {"priority": HashtagPriority.MEDIUM, "weight": 5}
            },
            "trending_hashtags": {
                "#AIRevolution": {"priority": HashtagPriority.TRENDING, "weight": 8},
                "#TechTrends": {"priority": HashtagPriority.TRENDING, "weight": 6},
                "#BusinessGrowth": {"priority": HashtagPriority.TRENDING, "weight": 6},
                "#Innovation": {"priority": HashtagPriority.TRENDING, "weight": 5},
                "#StartupLife": {"priority": HashtagPriority.TRENDING, "weight": 5},
                "#Entrepreneurship": {"priority": HashtagPriority.TRENDING, "weight": 5}
            },
            "monitoring_intervals": {
                HashtagPriority.HIGH: 300,      # 5 minutes
                HashtagPriority.MEDIUM: 600,    # 10 minutes
                HashtagPriority.LOW: 1800,      # 30 minutes
                HashtagPriority.TRENDING: 900   # 15 minutes
            },
            "opportunity_thresholds": {
                "minimum_engagement": 5,
                "minimum_relevance": 4.0,
                "minimum_opportunity_score": 6.0,
                "high_value_threshold": 8.0
            }
        }

    async def start_hashtag_monitoring(self) -> None:
        """Start continuous hashtag monitoring"""
        self.logger.info("🏷️ Starting Intelligent Hashtag Tracking")
        
        # Start monitoring tasks for different priority levels
        monitoring_tasks = [
            self._monitor_hashtag_group("primary_hashtags"),
            self._monitor_hashtag_group("secondary_hashtags"),
            self._monitor_hashtag_group("trending_hashtags"),
            self._discover_new_trending_hashtags(),
            self._analyze_hashtag_performance(),
            self._cleanup_old_data()
        ]
        
        try:
            await asyncio.gather(*monitoring_tasks)
        except Exception as e:
            self.logger.error(f"Hashtag monitoring error: {e}")

    async def _monitor_hashtag_group(self, group_name: str) -> None:
        """Monitor a specific group of hashtags"""
        hashtags = self.hashtag_config[group_name]
        
        while True:
            try:
                for hashtag, config in hashtags.items():
                    await self._monitor_single_hashtag(hashtag, config)
                    
                    # Rate limiting between hashtags
                    await asyncio.sleep(30)
                
                # Wait based on priority
                priority = list(hashtags.values())[0]["priority"]
                interval = self.hashtag_config["monitoring_intervals"][priority]
                await asyncio.sleep(interval)
                
            except Exception as e:
                self.logger.error(f"Error monitoring {group_name}: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes before retrying

    async def _monitor_single_hashtag(self, hashtag: str, config: Dict[str, Any]) -> None:
        """Monitor a single hashtag for opportunities"""
        try:
            # Search for recent tweets with this hashtag
            query = f"{hashtag} -from:smeanalytica -is:retweet"
            tweets = await self.twitter_manager.search_tweets(
                query=query,
                max_results=20
            )
            
            opportunities = []
            total_engagement = 0
            total_reach = 0
            
            for tweet in tweets:
                # Calculate opportunity score
                opportunity = await self._analyze_tweet_opportunity(tweet, hashtag, config)
                
                if opportunity and opportunity.opportunity_score >= self.hashtag_config["opportunity_thresholds"]["minimum_opportunity_score"]:
                    opportunities.append(opportunity)
                    
                    if opportunity.opportunity_score >= self.hashtag_config["opportunity_thresholds"]["high_value_threshold"]:
                        self.session_stats["high_value_opportunities"] += 1
                
                # Aggregate metrics
                if tweet.public_metrics:
                    total_engagement += (
                        tweet.public_metrics.get('like_count', 0) +
                        tweet.public_metrics.get('retweet_count', 0) +
                        tweet.public_metrics.get('reply_count', 0)
                    )
                    total_reach += tweet.public_metrics.get('impression_count', 0)
            
            # Update hashtag metrics
            await self._update_hashtag_metrics(hashtag, len(tweets), total_engagement, total_reach)
            
            # Store opportunities
            self.opportunity_history.extend(opportunities)
            self.session_stats["opportunities_found"] += len(opportunities)
            
            if opportunities:
                self.logger.info(f"🏷️ Found {len(opportunities)} opportunities for {hashtag}")
            
        except Exception as e:
            self.logger.error(f"Error monitoring hashtag {hashtag}: {e}")

    async def _analyze_tweet_opportunity(self, tweet, hashtag: str, config: Dict[str, Any]) -> Optional[HashtagOpportunity]:
        """Analyze a tweet for engagement opportunity"""
        try:
            # Basic relevance scoring
            relevance_score = self._calculate_hashtag_relevance(tweet.text, hashtag)
            
            if relevance_score < self.hashtag_config["opportunity_thresholds"]["minimum_relevance"]:
                return None
            
            # Calculate engagement potential
            engagement_potential = self._calculate_engagement_potential(tweet)
            
            # Calculate conversion likelihood
            conversion_likelihood = self._calculate_conversion_likelihood(tweet.text, tweet.author_username)
            
            # Calculate overall opportunity score
            opportunity_score = (
                relevance_score * 0.3 +
                engagement_potential * 0.3 +
                conversion_likelihood * 0.2 +
                config["weight"] * 0.2
            )
            
            # Calculate urgency
            urgency = self._calculate_urgency(tweet, hashtag)
            
            return HashtagOpportunity(
                hashtag=hashtag,
                tweet_id=tweet.id,
                author=tweet.author_username,
                content=tweet.text,
                opportunity_score=opportunity_score,
                engagement_potential=engagement_potential,
                conversion_likelihood=conversion_likelihood,
                urgency=urgency,
                discovered_at=datetime.now()
            )
            
        except Exception as e:
            self.logger.error(f"Error analyzing tweet opportunity: {e}")
            return None

    def _calculate_hashtag_relevance(self, content: str, hashtag: str) -> float:
        """Calculate how relevant content is to our business"""
        content_lower = content.lower()
        score = 3.0  # Base score
        
        # Industry keywords
        industry_keywords = [
            'restaurant', 'analytics', 'data', 'pricing', 'ai', 'automation',
            'small business', 'hospitality', 'pos', 'integration', 'revenue',
            'profit', 'optimization', 'efficiency', 'growth', 'menu'
        ]
        
        for keyword in industry_keywords:
            if keyword in content_lower:
                score += 0.5
        
        # Prospect signals
        prospect_signals = [
            'looking for', 'need help', 'recommendations', 'advice',
            'struggling with', 'how to', 'best practices', 'solutions'
        ]
        
        for signal in prospect_signals:
            if signal in content_lower:
                score += 1.0
        
        # Question indicators
        if '?' in content:
            score += 0.5
        
        return min(score, 10.0)

    def _calculate_engagement_potential(self, tweet) -> float:
        """Calculate potential for engagement based on tweet metrics"""
        if not tweet.public_metrics:
            return 3.0
        
        likes = tweet.public_metrics.get('like_count', 0)
        retweets = tweet.public_metrics.get('retweet_count', 0)
        replies = tweet.public_metrics.get('reply_count', 0)
        
        # Calculate engagement rate (simplified)
        total_engagement = likes + retweets * 2 + replies * 3
        
        # Normalize to 0-10 scale
        if total_engagement < 5:
            return 2.0
        elif total_engagement < 20:
            return 5.0
        elif total_engagement < 50:
            return 7.0
        else:
            return 9.0

    def _calculate_conversion_likelihood(self, content: str, author: str) -> float:
        """Calculate likelihood of converting engagement to business value"""
        content_lower = content.lower()
        score = 3.0
        
        # High conversion signals
        high_conversion = [
            'restaurant owner', 'small business', 'pos system', 'analytics',
            'hotel manager', 'retail business', 'menu pricing', 'looking for solution'
        ]
        
        for signal in high_conversion:
            if signal in content_lower:
                score += 2.0
        
        # Author indicators (simplified - would need profile analysis)
        if 'restaurant' in author.lower() or 'business' in author.lower():
            score += 1.5
        
        return min(score, 10.0)

    def _calculate_urgency(self, tweet, hashtag: str) -> int:
        """Calculate urgency of engagement (1-10)"""
        urgency = 5  # Base urgency
        
        content_lower = tweet.text.lower()
        
        # Time-sensitive indicators
        if any(word in content_lower for word in ['urgent', 'asap', 'now', 'today']):
            urgency += 3
        
        # Question indicators
        if '?' in tweet.text:
            urgency += 2
        
        # High engagement tweets
        if tweet.public_metrics:
            total_engagement = sum(tweet.public_metrics.values())
            if total_engagement > 50:
                urgency += 2
        
        # Trending hashtags get higher urgency
        if hashtag in self.hashtag_config["trending_hashtags"]:
            urgency += 1
        
        return min(urgency, 10)

    async def _update_hashtag_metrics(self, hashtag: str, volume: int, 
                                    total_engagement: int, total_reach: int) -> None:
        """Update metrics for a hashtag"""
        try:
            current_time = datetime.now()
            
            # Calculate rates
            engagement_rate = total_engagement / max(volume, 1)
            reach_estimate = total_reach if total_reach > 0 else volume * 100  # Estimate if not available
            
            # Calculate trending velocity (simplified)
            trending_velocity = 0.0
            if hashtag in self.tracking_metrics:
                previous_volume = self.tracking_metrics[hashtag].volume
                time_diff = (current_time - self.tracking_metrics[hashtag].last_updated).total_seconds() / 3600
                if time_diff > 0:
                    trending_velocity = (volume - previous_volume) / time_diff
            
            # Update metrics
            self.tracking_metrics[hashtag] = HashtagMetrics(
                hashtag=hashtag,
                volume=volume,
                engagement_rate=engagement_rate,
                reach_estimate=reach_estimate,
                sentiment_score=7.0,  # Would integrate sentiment analysis
                relevance_score=8.0,  # Would calculate based on content analysis
                trending_velocity=trending_velocity,
                last_updated=current_time
            )
            
            self.session_stats["hashtags_monitored"] += 1
            
        except Exception as e:
            self.logger.error(f"Error updating metrics for {hashtag}: {e}")

    async def _discover_new_trending_hashtags(self) -> None:
        """Discover new trending hashtags relevant to our industry"""
        while True:
            try:
                # Get trending hashtags
                trending = await self.twitter_manager.get_trending_hashtags()
                
                for hashtag in trending:
                    if await self._is_relevant_hashtag(hashtag):
                        if hashtag not in self.hashtag_config["trending_hashtags"]:
                            # Add to trending hashtags
                            self.hashtag_config["trending_hashtags"][hashtag] = {
                                "priority": HashtagPriority.TRENDING,
                                "weight": 6
                            }
                            self.session_stats["trending_hashtags_discovered"] += 1
                            self.logger.info(f"🔥 Discovered new trending hashtag: {hashtag}")
                
                await asyncio.sleep(1800)  # Check every 30 minutes
                
            except Exception as e:
                self.logger.error(f"Error discovering trending hashtags: {e}")
                await asyncio.sleep(3600)  # Wait 1 hour before retrying

    async def _is_relevant_hashtag(self, hashtag: str) -> bool:
        """Check if a hashtag is relevant to our industry"""
        relevant_keywords = [
            'restaurant', 'business', 'analytics', 'data', 'ai', 'tech',
            'hospitality', 'retail', 'pos', 'pricing', 'optimization'
        ]
        
        hashtag_lower = hashtag.lower()
        return any(keyword in hashtag_lower for keyword in relevant_keywords)

    async def _analyze_hashtag_performance(self) -> None:
        """Analyze hashtag performance and optimize tracking"""
        while True:
            try:
                await asyncio.sleep(3600)  # Run every hour
                
                # Analyze performance and adjust weights
                for hashtag, metrics in self.tracking_metrics.items():
                    if metrics.engagement_rate > 10:  # High performing hashtag
                        # Increase monitoring frequency
                        pass
                    elif metrics.engagement_rate < 2:  # Low performing hashtag
                        # Decrease monitoring frequency
                        pass
                
            except Exception as e:
                self.logger.error(f"Error analyzing hashtag performance: {e}")

    async def _cleanup_old_data(self) -> None:
        """Clean up old opportunity data"""
        while True:
            try:
                await asyncio.sleep(86400)  # Run daily
                
                # Remove opportunities older than 7 days
                cutoff_time = datetime.now() - timedelta(days=7)
                self.opportunity_history = [
                    opp for opp in self.opportunity_history 
                    if opp.discovered_at > cutoff_time
                ]
                
            except Exception as e:
                self.logger.error(f"Error cleaning up old data: {e}")

    def get_hashtag_opportunities(self, min_score: float = 6.0) -> List[HashtagOpportunity]:
        """Get current hashtag opportunities above minimum score"""
        return [
            opp for opp in self.opportunity_history 
            if opp.opportunity_score >= min_score
        ]

    def get_hashtag_metrics(self) -> Dict[str, HashtagMetrics]:
        """Get current hashtag metrics"""
        return self.tracking_metrics.copy()

    def get_tracking_stats(self) -> Dict[str, Any]:
        """Get hashtag tracking statistics"""
        runtime = datetime.now() - self.session_stats["start_time"]
        
        return {
            "runtime": str(runtime),
            "hashtags_monitored": self.session_stats["hashtags_monitored"],
            "opportunities_found": self.session_stats["opportunities_found"],
            "high_value_opportunities": self.session_stats["high_value_opportunities"],
            "trending_hashtags_discovered": self.session_stats["trending_hashtags_discovered"],
            "active_hashtags": len(self.tracking_metrics),
            "recent_opportunities": len([
                opp for opp in self.opportunity_history 
                if opp.discovered_at > datetime.now() - timedelta(hours=24)
            ])
        }
