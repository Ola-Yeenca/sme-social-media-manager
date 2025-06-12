"""
Hashtag Intelligence Agent for SME Analytica's social media growth system
Builds intelligent hashtag optimization system that maximizes reach and engagement
"""

import json
import sqlite3
from typing import Dict, List, Tuple, Optional, Any, Set
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import random
import asyncio
import re
import logging
from collections import defaultdict, Counter
import statistics
import math

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HashtagLifecycle(str, Enum):
    """Hashtag lifecycle stages"""
    EMERGING = "emerging"
    TRENDING = "trending"
    PEAK = "peak"
    SATURATED = "saturated"
    DECLINING = "declining"

class HashtagCategory(str, Enum):
    """Hashtag categories for classification"""
    BRAND = "brand"
    INDUSTRY = "industry"
    TECHNOLOGY = "technology"
    BUSINESS = "business"
    GEOGRAPHIC = "geographic"
    EVENT = "event"
    TRENDING = "trending"
    COMMUNITY = "community"

class PerformanceMetric(str, Enum):
    """Performance metrics for hashtag tracking"""
    REACH = "reach"
    ENGAGEMENT = "engagement"
    FOLLOWERS = "followers"
    CONVERSIONS = "conversions"
    VIRAL_SCORE = "viral_score"

@dataclass
class HashtagPerformance:
    """Individual hashtag performance data"""
    hashtag: str
    reach: int = 0
    impressions: int = 0
    engagement_rate: float = 0.0
    likes: int = 0
    shares: int = 0
    comments: int = 0
    follower_growth: int = 0
    click_through_rate: float = 0.0
    conversion_rate: float = 0.0
    viral_score: float = 0.0
    usage_frequency: int = 0
    last_used: Optional[datetime] = None
    lifecycle_stage: HashtagLifecycle = HashtagLifecycle.EMERGING
    category: HashtagCategory = HashtagCategory.INDUSTRY
    
    def calculate_performance_score(self) -> float:
        """Calculate overall performance score"""
        # Weighted scoring system
        weights = {
            'engagement': 0.3,
            'reach': 0.25,
            'viral': 0.2,
            'conversion': 0.15,
            'growth': 0.1
        }
        
        # Normalize metrics (0-10 scale)
        normalized_engagement = min(self.engagement_rate * 100, 10)
        normalized_reach = min(self.reach / 1000, 10)
        normalized_viral = min(self.viral_score, 10)
        normalized_conversion = min(self.conversion_rate * 1000, 10)
        normalized_growth = min(self.follower_growth / 10, 10)
        
        score = (
            normalized_engagement * weights['engagement'] +
            normalized_reach * weights['reach'] +
            normalized_viral * weights['viral'] +
            normalized_conversion * weights['conversion'] +
            normalized_growth * weights['growth']
        )
        
        return round(score, 2)
    
    def is_overused(self, max_usage_per_week: int = 3) -> bool:
        """Check if hashtag is being overused"""
        if not self.last_used:
            return False
        
        week_ago = datetime.now() - timedelta(days=7)
        return self.usage_frequency > max_usage_per_week and self.last_used > week_ago

@dataclass
class HashtagCombination:
    """Optimal hashtag combination for content"""
    hashtags: List[str]
    predicted_reach: int
    predicted_engagement: float
    synergy_score: float
    diversity_score: float
    total_score: float
    content_type: str
    target_audience: str
    optimal_posting_time: str
    
    def get_combination_analysis(self) -> Dict[str, Any]:
        """Get detailed analysis of this combination"""
        return {
            "hashtags": self.hashtags,
            "metrics": {
                "predicted_reach": self.predicted_reach,
                "predicted_engagement": self.predicted_engagement,
                "synergy_score": self.synergy_score,
                "diversity_score": self.diversity_score,
                "total_score": self.total_score
            },
            "optimization": {
                "content_type": self.content_type,
                "target_audience": self.target_audience,
                "optimal_posting_time": self.optimal_posting_time
            }
        }

@dataclass
class TrendingHashtag:
    """Trending hashtag discovery result"""
    hashtag: str
    trend_score: float
    growth_rate: float
    current_volume: int
    predicted_peak: datetime
    industry_relevance: float
    geographic_focus: List[str]
    related_hashtags: List[str]
    opportunity_window: int  # days until saturation
    
    def is_worth_using(self, min_trend_score: float = 7.0) -> bool:
        """Determine if this trending hashtag is worth using"""
        return (
            self.trend_score >= min_trend_score and
            self.opportunity_window > 2 and
            self.industry_relevance > 0.6
        )

class HashtagAnalytics:
    """Core hashtag analytics and scoring engine"""
    
    def __init__(self, database_path: str = "data/hashtag_analytics.db"):
        self.database_path = database_path
        self.initialize_database()
        
        # SME Analytica specific hashtag groups
        self.brand_hashtags = {
            "#SMEAnalytica", "#MenuFlow", "#DynamicPricing", "#RestaurantAI",
            "#SMEAnalyticaSuccess", "#MenuFlowMagic", "#RestaurantData"
        }
        
        self.industry_hashtags = {
            # Restaurant & Food Service
            "#RestaurantTech", "#FoodTech", "#RestaurantAnalytics", "#MenuOptimization",
            "#RestaurantPOS", "#QROrdering", "#FoodBusiness", "#RestaurantOwner",
            "#CafeBusiness", "#RestaurantRevenue", "#FoodServiceTech", "#DiningTech",
            
            # Hotel & Hospitality  
            "#HotelTech", "#HospitalityTech", "#HotelManagement", "#HospitalityAI",
            "#HotelAnalytics", "#RevPar", "#HotelRevenue", "#BookingOptimization",
            
            # Retail
            "#RetailTech", "#RetailAnalytics", "#SmallRetail", "#RetailPOS",
            "#InventoryTech", "#RetailAI", "#EcommerceTech",
            
            # Business & Analytics
            "#BusinessIntelligence", "#DataAnalytics", "#BusinessAnalytics", "#AIforBusiness",
            "#SmallBusiness", "#SME", "#BusinessGrowth", "#RevenueOptimization",
            "#PricingStrategy", "#BusinessInsights", "#DataDriven"
        }
        
        self.geographic_hashtags = {
            # Major Markets
            "#LondonRestaurants", "#NYCFood", "#TorontoEats", "#SydneyDining",
            "#ParisRestaurants", "#TokyoFood", "#LAEats", "#ChicagoFood",
            "#BerlinFood", "#AmsterdamEats", "#SingaporeFood", "#DubaiDining",
            "#MiamiEats", "#SeattleFood", "#VancouverDining", "#MelbourneCafe",
            
            # Regional
            "#UKRestaurants", "#CanadianFood", "#AustralianFood", "#EuropeanDining",
            "#AsianFood", "#NorthAmericaEats", "#GlobalRestaurants",
            "#EuropeEats", "#AsiaRestaurants", "#PacificDining",
            
            # Business regions
            "#LondonBusiness", "#NYCBusiness", "#TorontoBusiness", "#SydneyBusiness",
            "#EuropeBusiness", "#GlobalSME", "#InternationalBusiness"
        }
        
        self.event_hashtags = {
            # Industry Events
            "#NRF2024", "#RestaurantShow", "#FoodTechWeek", "#HospitalityTech",
            "#RetailTechShow", "#FoodInnovation", "#RestaurantInnovation",
            
            # Seasonal
            "#Q1Business", "#Q2Growth", "#Q3Results", "#Q4Planning",
            "#NewYearBusiness", "#SpringLaunch", "#SummerBoost", "#HolidayRush"
        }
    
    def initialize_database(self):
        """Initialize hashtag analytics database"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            # Hashtag performance table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS hashtag_performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hashtag TEXT UNIQUE NOT NULL,
                    reach INTEGER DEFAULT 0,
                    impressions INTEGER DEFAULT 0,
                    engagement_rate REAL DEFAULT 0.0,
                    likes INTEGER DEFAULT 0,
                    shares INTEGER DEFAULT 0,
                    comments INTEGER DEFAULT 0,
                    follower_growth INTEGER DEFAULT 0,
                    click_through_rate REAL DEFAULT 0.0,
                    conversion_rate REAL DEFAULT 0.0,
                    viral_score REAL DEFAULT 0.0,
                    usage_frequency INTEGER DEFAULT 0,
                    last_used TEXT,
                    lifecycle_stage TEXT DEFAULT 'emerging',
                    category TEXT DEFAULT 'industry',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Hashtag combinations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS hashtag_combinations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    combination_hash TEXT UNIQUE NOT NULL,
                    hashtags TEXT NOT NULL,
                    predicted_reach INTEGER DEFAULT 0,
                    predicted_engagement REAL DEFAULT 0.0,
                    actual_reach INTEGER DEFAULT 0,
                    actual_engagement REAL DEFAULT 0.0,
                    synergy_score REAL DEFAULT 0.0,
                    diversity_score REAL DEFAULT 0.0,
                    total_score REAL DEFAULT 0.0,
                    content_type TEXT,
                    target_audience TEXT,
                    optimal_posting_time TEXT,
                    times_used INTEGER DEFAULT 0,
                    success_rate REAL DEFAULT 0.0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    last_used TEXT
                )
            ''')
            
            # Trending hashtags table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS trending_hashtags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hashtag TEXT NOT NULL,
                    trend_score REAL DEFAULT 0.0,
                    growth_rate REAL DEFAULT 0.0,
                    current_volume INTEGER DEFAULT 0,
                    predicted_peak TEXT,
                    industry_relevance REAL DEFAULT 0.0,
                    geographic_focus TEXT,
                    related_hashtags TEXT,
                    opportunity_window INTEGER DEFAULT 0,
                    discovered_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'active'
                )
            ''')
            
            # A/B test results table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ab_test_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    test_id TEXT NOT NULL,
                    hashtag_set_a TEXT NOT NULL,
                    hashtag_set_b TEXT NOT NULL,
                    reach_a INTEGER DEFAULT 0,
                    reach_b INTEGER DEFAULT 0,
                    engagement_a REAL DEFAULT 0.0,
                    engagement_b REAL DEFAULT 0.0,
                    winner TEXT,
                    confidence_level REAL DEFAULT 0.0,
                    test_start TEXT,
                    test_end TEXT,
                    content_type TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Hashtag analytics database initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
    
    def update_hashtag_performance(self, performance: HashtagPerformance):
        """Update hashtag performance data"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO hashtag_performance 
                (hashtag, reach, impressions, engagement_rate, likes, shares, comments,
                 follower_growth, click_through_rate, conversion_rate, viral_score,
                 usage_frequency, last_used, lifecycle_stage, category, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                performance.hashtag, performance.reach, performance.impressions,
                performance.engagement_rate, performance.likes, performance.shares,
                performance.comments, performance.follower_growth,
                performance.click_through_rate, performance.conversion_rate,
                performance.viral_score, performance.usage_frequency,
                performance.last_used.isoformat() if performance.last_used else None,
                performance.lifecycle_stage.value, performance.category.value
            ))
            
            conn.commit()
            conn.close()
            logger.info(f"Updated performance for {performance.hashtag}")
            
        except Exception as e:
            logger.error(f"Error updating hashtag performance: {e}")
    
    def get_hashtag_performance(self, hashtag: str) -> Optional[HashtagPerformance]:
        """Get performance data for a specific hashtag"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT hashtag, reach, impressions, engagement_rate, likes, shares,
                       comments, follower_growth, click_through_rate, conversion_rate,
                       viral_score, usage_frequency, last_used, lifecycle_stage, category
                FROM hashtag_performance WHERE hashtag = ?
            ''', (hashtag,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return HashtagPerformance(
                    hashtag=row[0], reach=row[1], impressions=row[2],
                    engagement_rate=row[3], likes=row[4], shares=row[5],
                    comments=row[6], follower_growth=row[7],
                    click_through_rate=row[8], conversion_rate=row[9],
                    viral_score=row[10], usage_frequency=row[11],
                    last_used=datetime.fromisoformat(row[12]) if row[12] else None,
                    lifecycle_stage=HashtagLifecycle(row[13]),
                    category=HashtagCategory(row[14])
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting hashtag performance: {e}")
            return None
    
    def get_top_performing_hashtags(self, limit: int = 20, 
                                  category: Optional[HashtagCategory] = None,
                                  min_score: float = 5.0) -> List[HashtagPerformance]:
        """Get top performing hashtags"""
        try:
            conn = sqlite3.connect(self.database_path)
            cursor = conn.cursor()
            
            query = '''
                SELECT hashtag, reach, impressions, engagement_rate, likes, shares,
                       comments, follower_growth, click_through_rate, conversion_rate,
                       viral_score, usage_frequency, last_used, lifecycle_stage, category
                FROM hashtag_performance 
                WHERE 1=1
            '''
            params = []
            
            if category:
                query += ' AND category = ?'
                params.append(category.value)
            
            query += ' ORDER BY viral_score DESC, engagement_rate DESC LIMIT ?'
            params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()
            
            hashtags = []
            for row in rows:
                performance = HashtagPerformance(
                    hashtag=row[0], reach=row[1], impressions=row[2],
                    engagement_rate=row[3], likes=row[4], shares=row[5],
                    comments=row[6], follower_growth=row[7],
                    click_through_rate=row[8], conversion_rate=row[9],
                    viral_score=row[10], usage_frequency=row[11],
                    last_used=datetime.fromisoformat(row[12]) if row[12] else None,
                    lifecycle_stage=HashtagLifecycle(row[13]),
                    category=HashtagCategory(row[14])
                )
                
                if performance.calculate_performance_score() >= min_score:
                    hashtags.append(performance)
            
            return hashtags
            
        except Exception as e:
            logger.error(f"Error getting top performing hashtags: {e}")
            return []
    
    def calculate_hashtag_synergy(self, hashtags: List[str]) -> float:
        """Calculate synergy score for hashtag combination"""
        if len(hashtags) < 2:
            return 0.0
        
        # Check for category diversity
        categories = set()
        for hashtag in hashtags:
            if hashtag in self.brand_hashtags:
                categories.add("brand")
            elif hashtag in self.industry_hashtags:
                categories.add("industry")
            elif hashtag in self.geographic_hashtags:
                categories.add("geographic")
            elif hashtag in self.event_hashtags:
                categories.add("event")
            else:
                categories.add("other")
        
        diversity_score = len(categories) / 5.0  # Max 5 categories
        
        # Check for complementary combinations
        synergy_bonus = 0.0
        
        # Brand + Industry synergy
        if any(h in self.brand_hashtags for h in hashtags) and \
           any(h in self.industry_hashtags for h in hashtags):
            synergy_bonus += 0.3
        
        # Geographic + Industry synergy
        if any(h in self.geographic_hashtags for h in hashtags) and \
           any(h in self.industry_hashtags for h in hashtags):
            synergy_bonus += 0.2
        
        # Event + Industry synergy
        if any(h in self.event_hashtags for h in hashtags) and \
           any(h in self.industry_hashtags for h in hashtags):
            synergy_bonus += 0.25
        
        total_synergy = (diversity_score + synergy_bonus) * 10
        return min(total_synergy, 10.0)

class TrendingHashtagDiscovery:
    """Discover trending and emerging hashtags in restaurant/hospitality tech space"""
    
    def __init__(self, analytics: HashtagAnalytics):
        self.analytics = analytics
        
        # Seed hashtags for discovery
        self.seed_hashtags = [
            "#RestaurantTech", "#FoodTech", "#HospitalityAI", "#MenuTech",
            "#RestaurantAnalytics", "#DynamicPricing", "#QROrdering",
            "#POS", "#TableTech", "#FoodDelivery", "#RestaurantPos"
        ]
        
        # Keywords for trend detection
        self.trend_keywords = [
            "AI", "automation", "digital", "smart", "analytics", "data",
            "optimization", "revenue", "margin", "efficiency", "tech",
            "innovation", "transformation", "future", "2024", "2025"
        ]
    
    async def discover_trending_hashtags(self, count: int = 10) -> List[TrendingHashtag]:
        """Discover trending hashtags using multiple detection methods"""
        discovered_hashtags = []
        
        # Method 1: Related hashtag discovery
        related_trends = await self._discover_related_hashtags()
        discovered_hashtags.extend(related_trends)
        
        # Method 2: Keyword-based trend detection
        keyword_trends = await self._discover_keyword_trends()
        discovered_hashtags.extend(keyword_trends)
        
        # Method 3: Industry event hashtags
        event_trends = await self._discover_event_hashtags()
        discovered_hashtags.extend(event_trends)
        
        # Sort by trend score and return top results
        discovered_hashtags.sort(key=lambda x: x.trend_score, reverse=True)
        return discovered_hashtags[:count]
    
    async def _discover_related_hashtags(self) -> List[TrendingHashtag]:
        """Discover trending hashtags related to our seed hashtags"""
        trends = []
        
        for seed in self.seed_hashtags:
            # Simulate related hashtag discovery
            related = self._generate_related_hashtags(seed)
            
            for hashtag in related:
                trend_score = self._calculate_trend_score(hashtag)
                if trend_score > 6.0:
                    trends.append(TrendingHashtag(
                        hashtag=hashtag,
                        trend_score=trend_score,
                        growth_rate=random.uniform(0.1, 0.8),
                        current_volume=random.randint(100, 50000),
                        predicted_peak=datetime.now() + timedelta(days=random.randint(3, 21)),
                        industry_relevance=random.uniform(0.6, 1.0),
                        geographic_focus=["Global", "North America", "Europe"],
                        related_hashtags=[seed],
                        opportunity_window=random.randint(5, 30)
                    ))
        
        return trends
    
    def _generate_related_hashtags(self, seed: str) -> List[str]:
        """Generate related hashtags based on seed"""
        base = seed.replace("#", "")
        
        related_patterns = [
            f"#{base}2024", f"#{base}AI", f"#{base}Tech", f"#{base}Innovation",
            f"#{base}Future", f"#{base}Analytics", f"#{base}Automation",
            f"#Smart{base}", f"#AI{base}", f"#Digital{base}", f"#Next{base}"
        ]
        
        # Industry-specific variations
        if "Restaurant" in base:
            related_patterns.extend([
                "#RestaurantRevolution", "#FoodTechTrends", "#DiningInnovation",
                "#RestaurantAutomation", "#SmartRestaurants", "#FutureOfDining"
            ])
        elif "Hotel" in base or "Hospitality" in base:
            related_patterns.extend([
                "#HotelInnovation", "#SmartHotels", "#HospitalityRevolution",
                "#TravelTech", "#HotelAutomation", "#DigitalHospitality"
            ])
        
        return related_patterns[:5]  # Return top 5 related hashtags
    
    def _calculate_trend_score(self, hashtag: str) -> float:
        """Calculate trend score for hashtag"""
        score = 5.0  # Base score
        
        # Check for trending indicators
        trend_indicators = ["2024", "2025", "AI", "Smart", "Future", "Next", "Innovation"]
        for indicator in trend_indicators:
            if indicator.lower() in hashtag.lower():
                score += 1.5
        
        # Industry relevance boost
        industry_terms = ["Restaurant", "Hotel", "Hospitality", "Food", "Tech", "Analytics"]
        for term in industry_terms:
            if term.lower() in hashtag.lower():
                score += 1.0
        
        # Limit to 10.0 max score
        return min(score, 10.0)
    
    async def _discover_keyword_trends(self) -> List[TrendingHashtag]:
        """Discover trends based on trending keywords"""
        trends = []
        
        # Generate hashtags from trending keywords
        for keyword in self.trend_keywords:
            hashtag_variations = [
                f"#{keyword}Restaurant", f"#{keyword}Food", f"#{keyword}Hospitality",
                f"#{keyword}Business", f"#{keyword}Tech", f"#{keyword}2024"
            ]
            
            for hashtag in hashtag_variations:
                if self._is_viable_hashtag(hashtag):
                    trend_score = self._calculate_keyword_trend_score(keyword, hashtag)
                    if trend_score > 7.0:
                        trends.append(TrendingHashtag(
                            hashtag=hashtag,
                            trend_score=trend_score,
                            growth_rate=random.uniform(0.2, 0.9),
                            current_volume=random.randint(500, 25000),
                            predicted_peak=datetime.now() + timedelta(days=random.randint(5, 14)),
                            industry_relevance=random.uniform(0.7, 1.0),
                            geographic_focus=["Global"],
                            related_hashtags=[f"#{keyword}"],
                            opportunity_window=random.randint(7, 21)
                        ))
        
        return trends
    
    def _is_viable_hashtag(self, hashtag: str) -> bool:
        """Check if hashtag is viable for trending"""
        # Must be reasonable length
        if len(hashtag) > 30 or len(hashtag) < 5:
            return False
        
        # Must contain letters
        if not re.search(r'[a-zA-Z]', hashtag):
            return False
        
        # No spaces or special characters (except #)
        if re.search(r'[^a-zA-Z0-9#]', hashtag):
            return False
        
        return True
    
    def _calculate_keyword_trend_score(self, keyword: str, hashtag: str) -> float:
        """Calculate trend score for keyword-based hashtag"""
        base_score = 6.0
        
        # High-value keywords get boost
        high_value_keywords = ["AI", "Analytics", "Smart", "Future", "Innovation"]
        if keyword in high_value_keywords:
            base_score += 2.0
        
        # Industry alignment boost
        if any(term in hashtag for term in ["Restaurant", "Food", "Hospitality", "Business"]):
            base_score += 1.5
        
        return min(base_score, 10.0)
    
    async def _discover_event_hashtags(self) -> List[TrendingHashtag]:
        """Discover hashtags related to upcoming industry events"""
        events = [
            "RestaurantShow2024", "FoodTechWeek", "HospitalityTech2024",
            "NRF2024", "RetailTechShow", "FoodInnovationSummit",
            "RestaurantInnovation", "HotelTechConf", "FoodServiceExpo"
        ]
        
        trends = []
        for event in events:
            hashtag = f"#{event}"
            trends.append(TrendingHashtag(
                hashtag=hashtag,
                trend_score=random.uniform(7.5, 9.5),
                growth_rate=random.uniform(0.5, 1.0),
                current_volume=random.randint(1000, 15000),
                predicted_peak=datetime.now() + timedelta(days=random.randint(10, 60)),
                industry_relevance=0.95,
                geographic_focus=["Global", "North America"],
                related_hashtags=["#FoodTech", "#RestaurantTech"],
                opportunity_window=random.randint(14, 45)
            ))
        
        return trends

class HashtagCombinationOptimizer:
    """Optimize hashtag combinations for maximum reach and engagement"""
    
    def __init__(self, analytics: HashtagAnalytics):
        self.analytics = analytics
        
        # Content type specific weights
        self.content_weights = {
            "educational": {
                "industry": 0.4,
                "brand": 0.2,
                "business": 0.3,
                "geographic": 0.1
            },
            "promotional": {
                "brand": 0.5,
                "industry": 0.3,
                "geographic": 0.2,
                "business": 0.0
            },
            "case_study": {
                "brand": 0.3,
                "industry": 0.3,
                "business": 0.4,
                "geographic": 0.0
            },
            "engagement": {
                "community": 0.4,
                "industry": 0.3,
                "trending": 0.3,
                "brand": 0.0
            }
        }
    
    def generate_optimal_combinations(self, content_type: str = "educational",
                                    target_audience: str = "restaurant_owners",
                                    max_hashtags: int = 4,
                                    count: int = 5) -> List[HashtagCombination]:
        """Generate optimal hashtag combinations"""
        combinations = []
        
        # Get available hashtags by category
        available_hashtags = self._get_categorized_hashtags()
        
        # Get content type weights
        weights = self.content_weights.get(content_type, self.content_weights["educational"])
        
        for _ in range(count * 3):  # Generate more than needed for filtering
            combination = self._create_combination(
                available_hashtags, weights, max_hashtags, content_type, target_audience
            )
            
            if combination and combination.total_score > 6.0:
                combinations.append(combination)
        
        # Sort by total score and return top results
        combinations.sort(key=lambda x: x.total_score, reverse=True)
        return combinations[:count]
    
    def _get_categorized_hashtags(self) -> Dict[str, List[str]]:
        """Get hashtags organized by category"""
        return {
            "brand": list(self.analytics.brand_hashtags),
            "industry": list(self.analytics.industry_hashtags)[:20],  # Limit for performance
            "geographic": list(self.analytics.geographic_hashtags)[:15],
            "business": [
                "#SmallBusiness", "#BusinessGrowth", "#Entrepreneur",
                "#BusinessIntelligence", "#DataDriven", "#RevenueOptimization",
                "#SME", "#BusinessAnalytics", "#AIforBusiness"
            ],
            "community": [
                "#RestaurantCommunity", "#FoodieNetwork", "#BusinessNetworking",
                "#SmallBizCommunity", "#TechCommunity", "#SMECommunity"
            ],
            "trending": [
                "#TechTrends2024", "#AIBusiness", "#FutureOfFood",
                "#DigitalTransformation", "#Innovation2024", "#AI2024",
                "#RestaurantAI", "#SmartBusiness", "#TechInnovation"
            ]
        }
    
    def _create_combination(self, available_hashtags: Dict[str, List[str]],
                          weights: Dict[str, float], max_hashtags: int,
                          content_type: str, target_audience: str) -> Optional[HashtagCombination]:
        """Create a single optimized hashtag combination"""
        selected_hashtags = []
        
        # Select hashtags based on weights
        for category, weight in weights.items():
            if category in available_hashtags and weight > 0:
                count = max(1, int(max_hashtags * weight))
                available = available_hashtags[category]
                
                if available:
                    selected = random.sample(available, min(count, len(available)))
                    selected_hashtags.extend(selected)
        
        # Trim to max hashtags
        if len(selected_hashtags) > max_hashtags:
            selected_hashtags = random.sample(selected_hashtags, max_hashtags)
        
        if not selected_hashtags:
            return None
        
        # Calculate metrics
        predicted_reach = self._predict_reach(selected_hashtags)
        predicted_engagement = self._predict_engagement(selected_hashtags)
        synergy_score = self.analytics.calculate_hashtag_synergy(selected_hashtags)
        diversity_score = self._calculate_diversity_score(selected_hashtags)
        
        # Calculate total score
        total_score = (
            (predicted_reach / 10000) * 0.3 +
            predicted_engagement * 30 * 0.3 +
            synergy_score * 0.2 +
            diversity_score * 0.2
        )
        
        return HashtagCombination(
            hashtags=selected_hashtags,
            predicted_reach=predicted_reach,
            predicted_engagement=predicted_engagement,
            synergy_score=synergy_score,
            diversity_score=diversity_score,
            total_score=min(total_score, 10.0),
            content_type=content_type,
            target_audience=target_audience,
            optimal_posting_time=self._get_optimal_posting_time(content_type)
        )
    
    def _predict_reach(self, hashtags: List[str]) -> int:
        """Predict reach for hashtag combination"""
        base_reach = 1000
        
        for hashtag in hashtags:
            # Brand hashtags have lower reach but higher engagement
            if hashtag in self.analytics.brand_hashtags:
                base_reach += random.randint(500, 2000)
            # Industry hashtags have good reach
            elif hashtag in self.analytics.industry_hashtags:
                base_reach += random.randint(2000, 8000)
            # Geographic hashtags vary widely
            elif hashtag in self.analytics.geographic_hashtags:
                base_reach += random.randint(1000, 15000)
            else:
                base_reach += random.randint(1000, 5000)
        
        # Combination bonus
        if len(hashtags) > 2:
            base_reach = int(base_reach * 1.2)
        
        return base_reach
    
    def _predict_engagement(self, hashtags: List[str]) -> float:
        """Predict engagement rate for hashtag combination"""
        base_rate = 0.02  # 2%
        
        for hashtag in hashtags:
            if hashtag in self.analytics.brand_hashtags:
                base_rate += random.uniform(0.005, 0.02)  # Brand hashtags get higher engagement
            elif hashtag in self.analytics.industry_hashtags:
                base_rate += random.uniform(0.002, 0.01)
            else:
                base_rate += random.uniform(0.001, 0.005)
        
        return min(base_rate, 0.1)  # Cap at 10%
    
    def _calculate_diversity_score(self, hashtags: List[str]) -> float:
        """Calculate diversity score for hashtag combination"""
        categories = set()
        
        for hashtag in hashtags:
            if hashtag in self.analytics.brand_hashtags:
                categories.add("brand")
            elif hashtag in self.analytics.industry_hashtags:
                categories.add("industry")
            elif hashtag in self.analytics.geographic_hashtags:
                categories.add("geographic")
            else:
                categories.add("other")
        
        return (len(categories) / 4.0) * 10  # Max 4 categories, scale to 10
    
    def _get_optimal_posting_time(self, content_type: str) -> str:
        """Get optimal posting time based on content type"""
        optimal_times = {
            "educational": ["09:00", "13:00", "17:00"],
            "promotional": ["12:00", "18:00", "20:00"],
            "case_study": ["10:00", "14:00", "16:00"],
            "engagement": ["11:00", "15:00", "19:00"]
        }
        
        times = optimal_times.get(content_type, optimal_times["educational"])
        return random.choice(times)

class HashtagABTester:
    """A/B testing framework for hashtag combinations"""
    
    def __init__(self, analytics: HashtagAnalytics):
        self.analytics = analytics
    
    def create_ab_test(self, content_type: str, target_audience: str) -> Dict[str, Any]:
        """Create A/B test for hashtag combinations"""
        optimizer = HashtagCombinationOptimizer(self.analytics)
        
        # Generate two different combinations
        combinations = optimizer.generate_optimal_combinations(
            content_type=content_type,
            target_audience=target_audience,
            count=10  # Generate more options
        )
        
        if len(combinations) < 2:
            return {"error": "Not enough combinations for A/B test"}
        
        # Select A and B sets with different strategies
        set_a = combinations[0]  # Highest scored combination
        
        # Find a different combination for set B
        set_b = combinations[1]
        for combo in combinations[1:]:
            # Ensure B is sufficiently different from A
            overlap = len(set(combo.hashtags) & set(set_a.hashtags))
            if overlap <= len(set_a.hashtags) // 2:  # Less than 50% overlap
                set_b = combo
                break
        
        test_id = f"abtest_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return {
            "test_id": test_id,
            "set_a": {
                "hashtags": set_a.hashtags,
                "predicted_metrics": {
                    "reach": set_a.predicted_reach,
                    "engagement": set_a.predicted_engagement,
                    "total_score": set_a.total_score
                }
            },
            "set_b": {
                "hashtags": set_b.hashtags,
                "predicted_metrics": {
                    "reach": set_b.predicted_reach,
                    "engagement": set_b.predicted_engagement,
                    "total_score": set_b.total_score
                }
            },
            "test_duration_days": 7,
            "content_type": content_type,
            "target_audience": target_audience,
            "success_metrics": ["reach", "engagement_rate", "follower_growth"]
        }
    
    def analyze_ab_test_results(self, test_id: str, results_a: Dict[str, Any],
                               results_b: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze A/B test results and determine winner"""
        
        # Calculate performance scores
        score_a = self._calculate_test_score(results_a)
        score_b = self._calculate_test_score(results_b)
        
        # Determine winner and confidence
        winner = "A" if score_a > score_b else "B"
        confidence = abs(score_a - score_b) / max(score_a, score_b)
        
        # Statistical significance (simplified)
        is_significant = confidence > 0.1  # 10% difference threshold
        
        analysis = {
            "test_id": test_id,
            "winner": winner,
            "confidence_level": round(confidence, 3),
            "is_statistically_significant": is_significant,
            "performance_a": {
                "score": round(score_a, 2),
                "metrics": results_a
            },
            "performance_b": {
                "score": round(score_b, 2),
                "metrics": results_b
            },
            "recommendations": self._generate_test_recommendations(winner, confidence, results_a, results_b)
        }
        
        # Save results to database
        self._save_ab_test_results(analysis)
        
        return analysis
    
    def _calculate_test_score(self, results: Dict[str, Any]) -> float:
        """Calculate overall performance score for test results"""
        weights = {
            "reach": 0.3,
            "engagement_rate": 0.4,
            "follower_growth": 0.2,
            "click_through_rate": 0.1
        }
        
        score = 0.0
        for metric, weight in weights.items():
            value = results.get(metric, 0)
            if metric == "engagement_rate":
                normalized_value = min(value * 100, 10)  # Scale to 0-10
            elif metric == "click_through_rate":
                normalized_value = min(value * 1000, 10)  # Scale to 0-10
            else:
                normalized_value = min(value / 1000, 10)  # Scale to 0-10
            
            score += normalized_value * weight
        
        return score
    
    def _generate_test_recommendations(self, winner: str, confidence: float,
                                     results_a: Dict[str, Any], results_b: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on test results"""
        recommendations = []
        
        if confidence > 0.2:
            recommendations.append(f"Set {winner} is the clear winner with {confidence:.1%} better performance")
        elif confidence > 0.1:
            recommendations.append(f"Set {winner} shows moderate advantage - consider using for important posts")
        else:
            recommendations.append("Results are inconclusive - both sets perform similarly")
        
        # Specific metric recommendations
        if results_a.get("engagement_rate", 0) > results_b.get("engagement_rate", 0) * 1.2:
            recommendations.append("Set A shows superior engagement - good for community building")
        elif results_b.get("engagement_rate", 0) > results_a.get("engagement_rate", 0) * 1.2:
            recommendations.append("Set B shows superior engagement - good for community building")
        
        if results_a.get("reach", 0) > results_b.get("reach", 0) * 1.2:
            recommendations.append("Set A achieves better reach - use for awareness campaigns")
        elif results_b.get("reach", 0) > results_a.get("reach", 0) * 1.2:
            recommendations.append("Set B achieves better reach - use for awareness campaigns")
        
        return recommendations
    
    def _save_ab_test_results(self, analysis: Dict[str, Any]):
        """Save A/B test results to database"""
        try:
            conn = sqlite3.connect(self.analytics.database_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO ab_test_results 
                (test_id, hashtag_set_a, hashtag_set_b, reach_a, reach_b,
                 engagement_a, engagement_b, winner, confidence_level,
                 test_start, test_end, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            ''', (
                analysis["test_id"],
                json.dumps(analysis["performance_a"]["metrics"]),
                json.dumps(analysis["performance_b"]["metrics"]),
                analysis["performance_a"]["metrics"].get("reach", 0),
                analysis["performance_b"]["metrics"].get("reach", 0),
                analysis["performance_a"]["metrics"].get("engagement_rate", 0),
                analysis["performance_b"]["metrics"].get("engagement_rate", 0),
                analysis["winner"],
                analysis["confidence_level"],
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error saving A/B test results: {e}")

class HashtagIntelligenceAgent:
    """Main hashtag intelligence agent orchestrating all hashtag optimization"""
    
    def __init__(self, database_path: str = "data/hashtag_analytics.db"):
        self.analytics = HashtagAnalytics(database_path)
        self.discovery = TrendingHashtagDiscovery(self.analytics)
        self.optimizer = HashtagCombinationOptimizer(self.analytics)
        self.ab_tester = HashtagABTester(self.analytics)
        
        # SME Analytica context
        self.context = {
            "brand": "SME Analytica",
            "products": ["MenuFlow", "DynamicPricing", "RestaurantAI"],
            "target_audiences": ["restaurant_owners", "hotel_managers", "retail_owners"],
            "value_props": ["10% margin boost", "real-time analytics", "seamless integration"],
            "geographic_focus": ["North America", "Europe", "Global"]
        }
        
        # Multilingual hashtag support
        self.multilingual_hashtags = {
            "spanish": {
                "#PequeñasEmpresas", "#RestauranteTech", "#AnalíticaIA", "#DatosInteligentes",
                "#EmpresasInteligentes", "#TecnologíaRestaurante", "#AnalíticaDatos",
                "#NegociosInteligentes", "#IAparaPYME", "#OptimizaciónPrecios"
            },
            "french": {
                "#PME", "#TechRestaurant", "#AnalyticsIA", "#DonnéesIntelligentes",
                "#EntreprisesIntelligentes", "#TechnologieRestaurant", "#AnalyseDonnées",
                "#IAEntreprise", "#OptimisationPrix", "#BusinessIntelligent"
            },
            "german": {
                "#KMU", "#RestaurantTech", "#KIAnalytik", "#DatenIntelligenz",
                "#SmarteBetriebe", "#RestaurantTechnologie", "#DatenAnalyse",
                "#KIUnternehmen", "#PreisOptimierung", "#BusinessIntelligenz"
            }
        }
    
    async def get_optimal_hashtags_for_content(self, content_type: str = "educational",
                                             theme: str = "data_insights",
                                             target_audience: str = "restaurant_owners",
                                             max_hashtags: int = 4) -> Dict[str, Any]:
        """Get optimal hashtag combination for specific content"""
        
        # Generate optimal combinations
        combinations = self.optimizer.generate_optimal_combinations(
            content_type=content_type,
            target_audience=target_audience,
            max_hashtags=max_hashtags,
            count=3
        )
        
        if not combinations:
            return {"error": "No optimal combinations found"}
        
        best_combination = combinations[0]
        
        # Get trending hashtags that could enhance the combination
        trending = await self.discovery.discover_trending_hashtags(count=5)
        
        # Filter trending hashtags that would work with this content
        relevant_trending = [
            t for t in trending 
            if t.is_worth_using() and t.industry_relevance > 0.7
        ]
        
        return {
            "primary_combination": best_combination.get_combination_analysis(),
            "alternative_combinations": [combo.get_combination_analysis() for combo in combinations[1:]],
            "trending_opportunities": [
                {
                    "hashtag": t.hashtag,
                    "trend_score": t.trend_score,
                    "opportunity_window": t.opportunity_window,
                    "why_trending": f"Growing at {t.growth_rate:.1%} with {t.current_volume:,} current volume"
                }
                for t in relevant_trending[:3]
            ],
            "performance_prediction": {
                "estimated_reach": best_combination.predicted_reach,
                "estimated_engagement_rate": f"{best_combination.predicted_engagement:.2%}",
                "viral_potential": "High" if best_combination.total_score > 8.0 else "Medium" if best_combination.total_score > 6.0 else "Low"
            }
        }
    
    async def analyze_competitor_hashtags(self, competitor_hashtags: List[str]) -> Dict[str, Any]:
        """Analyze competitor hashtag strategies and find opportunities"""
        
        analysis = {
            "competitor_analysis": {
                "hashtags_analyzed": len(competitor_hashtags),
                "category_breakdown": self._analyze_hashtag_categories(competitor_hashtags),
                "performance_estimates": {}
            },
            "opportunity_gaps": [],
            "optimization_suggestions": []
        }
        
        # Analyze performance potential of competitor hashtags
        for hashtag in competitor_hashtags:
            performance = self.analytics.get_hashtag_performance(hashtag)
            if performance:
                analysis["competitor_analysis"]["performance_estimates"][hashtag] = {
                    "performance_score": performance.calculate_performance_score(),
                    "lifecycle_stage": performance.lifecycle_stage.value,
                    "usage_recommendation": "Use" if performance.calculate_performance_score() > 6.0 else "Avoid"
                }
        
        # Find hashtags competitors are missing
        all_industry_hashtags = (
            self.analytics.industry_hashtags | 
            self.analytics.geographic_hashtags | 
            self.analytics.event_hashtags
        )
        
        competitor_set = set(competitor_hashtags)
        missing_hashtags = all_industry_hashtags - competitor_set
        
        # Score missing hashtags as opportunities
        for hashtag in list(missing_hashtags)[:10]:  # Limit to top 10
            performance = self.analytics.get_hashtag_performance(hashtag)
            if performance and performance.calculate_performance_score() > 7.0:
                analysis["opportunity_gaps"].append({
                    "hashtag": hashtag,
                    "opportunity_score": performance.calculate_performance_score(),
                    "reason": "High-performing hashtag unused by competitor"
                })
        
        # Generate trending hashtags competitors might not know about
        trending = await self.discovery.discover_trending_hashtags(count=5)
        for trend in trending:
            if trend.hashtag not in competitor_set and trend.is_worth_using():
                analysis["opportunity_gaps"].append({
                    "hashtag": trend.hashtag,
                    "opportunity_score": trend.trend_score,
                    "reason": f"Emerging trend with {trend.opportunity_window} day window"
                })
        
        # Generate optimization suggestions
        analysis["optimization_suggestions"] = self._generate_competitor_insights(
            competitor_hashtags, analysis["opportunity_gaps"]
        )
        
        return analysis
    
    def _analyze_hashtag_categories(self, hashtags: List[str]) -> Dict[str, int]:
        """Analyze hashtag distribution across categories"""
        categories = {"brand": 0, "industry": 0, "geographic": 0, "event": 0, "other": 0}
        
        for hashtag in hashtags:
            if hashtag in self.analytics.brand_hashtags:
                categories["brand"] += 1
            elif hashtag in self.analytics.industry_hashtags:
                categories["industry"] += 1
            elif hashtag in self.analytics.geographic_hashtags:
                categories["geographic"] += 1
            elif hashtag in self.analytics.event_hashtags:
                categories["event"] += 1
            else:
                categories["other"] += 1
        
        return categories
    
    def _generate_competitor_insights(self, competitor_hashtags: List[str], 
                                    opportunities: List[Dict[str, Any]]) -> List[str]:
        """Generate insights and recommendations from competitor analysis"""
        insights = []
        
        # Category analysis
        categories = self._analyze_hashtag_categories(competitor_hashtags)
        total_hashtags = len(competitor_hashtags)
        
        if categories["brand"] / total_hashtags > 0.4:
            insights.append("Competitor overuses brand hashtags - opportunity for more industry/trending hashtags")
        
        if categories["geographic"] / total_hashtags < 0.1:
            insights.append("Competitor underutilizes geographic hashtags - opportunity for location-based targeting")
        
        if categories["event"] / total_hashtags < 0.05:
            insights.append("Competitor misses event-based hashtags - opportunity for timely trend participation")
        
        # Opportunity insights
        high_opportunity_count = len([opp for opp in opportunities if opp["opportunity_score"] > 8.0])
        if high_opportunity_count > 3:
            insights.append(f"Found {high_opportunity_count} high-value hashtag opportunities competitor is missing")
        
        # Trending insights
        trending_opportunities = [opp for opp in opportunities if "Emerging trend" in opp["reason"]]
        if trending_opportunities:
            insights.append(f"Identified {len(trending_opportunities)} emerging trends for early adoption advantage")
        
        return insights
    
    async def create_hashtag_rotation_strategy(self, content_themes: List[str],
                                             posting_frequency: int = 7) -> Dict[str, Any]:
        """Create a hashtag rotation strategy to avoid overuse"""
        
        strategy = {
            "rotation_schedule": {},
            "hashtag_pools": {},
            "usage_limits": {},
            "performance_tracking": {}
        }
        
        # Create hashtag pools for each theme
        for theme in content_themes:
            combinations = self.optimizer.generate_optimal_combinations(
                content_type=theme,
                count=posting_frequency * 2  # 2x posts for rotation
            )
            
            strategy["hashtag_pools"][theme] = [
                combo.hashtags for combo in combinations
            ]
        
        # Create rotation schedule
        for day in range(7):  # Weekly schedule
            theme = content_themes[day % len(content_themes)]
            pool = strategy["hashtag_pools"][theme]
            
            if pool:
                strategy["rotation_schedule"][f"day_{day + 1}"] = {
                    "theme": theme,
                    "hashtag_set": pool[day % len(pool)],
                    "backup_set": pool[(day + 1) % len(pool)] if len(pool) > 1 else pool[0]
                }
        
        # Set usage limits
        all_hashtags = set()
        for pools in strategy["hashtag_pools"].values():
            for hashtag_set in pools:
                all_hashtags.update(hashtag_set)
        
        for hashtag in all_hashtags:
            performance = self.analytics.get_hashtag_performance(hashtag)
            if performance and performance.is_overused():
                strategy["usage_limits"][hashtag] = 1  # Limit overused hashtags
            else:
                strategy["usage_limits"][hashtag] = 3  # Normal usage limit per week
        
        return strategy
    
    async def get_daily_hashtag_recommendations(self, date: Optional[datetime] = None) -> Dict[str, Any]:
        """Get daily hashtag recommendations based on trends and performance"""
        
        if not date:
            date = datetime.now()
        
        # Get trending hashtags
        trending = await self.discovery.discover_trending_hashtags(count=10)
        
        # Get top performing hashtags
        top_performing = self.analytics.get_top_performing_hashtags(limit=15)
        
        # Create recommendations by time of day
        recommendations = {
            "date": date.strftime("%Y-%m-%d"),
            "morning_post": self._create_time_based_recommendation("morning", trending, top_performing),
            "afternoon_post": self._create_time_based_recommendation("afternoon", trending, top_performing),
            "evening_post": self._create_time_based_recommendation("evening", trending, top_performing),
            "trending_alerts": [
                {
                    "hashtag": t.hashtag,
                    "alert": f"Trending with {t.growth_rate:.1%} growth - {t.opportunity_window} days left",
                    "action": "Use immediately" if t.trend_score > 8.5 else "Monitor closely"
                }
                for t in trending[:3] if t.is_worth_using()
            ]
        }
        
        return recommendations
    
    def _create_time_based_recommendation(self, time_period: str, 
                                        trending: List[TrendingHashtag],
                                        top_performing: List[HashtagPerformance]) -> Dict[str, Any]:
        """Create hashtag recommendation for specific time period"""
        
        # Time-specific hashtag preferences
        time_preferences = {
            "morning": {"business": 0.4, "industry": 0.3, "brand": 0.2, "trending": 0.1},
            "afternoon": {"industry": 0.4, "trending": 0.3, "business": 0.2, "brand": 0.1},
            "evening": {"trending": 0.4, "community": 0.3, "brand": 0.2, "industry": 0.1}
        }
        
        weights = time_preferences.get(time_period, time_preferences["afternoon"])
        
        # Select hashtags based on weights
        selected_hashtags = []
        
        # Add brand hashtag
        selected_hashtags.append("#SMEAnalytica")
        
        # Add trending if high weight
        if weights.get("trending", 0) > 0.3 and trending:
            best_trend = max(trending, key=lambda t: t.trend_score)
            if best_trend.is_worth_using():
                selected_hashtags.append(best_trend.hashtag)
        
        # Add industry hashtags
        industry_count = max(1, int(3 * weights.get("industry", 0.3)))
        industry_hashtags = random.sample(
            list(self.analytics.industry_hashtags), 
            min(industry_count, len(self.analytics.industry_hashtags))
        )
        selected_hashtags.extend(industry_hashtags[:industry_count])
        
        # Limit to 4 hashtags total
        selected_hashtags = selected_hashtags[:4]
        
        return {
            "hashtags": selected_hashtags,
            "time_period": time_period,
            "strategy": f"Optimized for {time_period} engagement patterns",
            "expected_performance": "Medium to High"
        }
    
    async def get_geographic_hashtag_strategy(self, target_regions: List[str]) -> Dict[str, Any]:
        """Create geographic-specific hashtag strategy for international reach"""
        
        strategy = {
            "regional_strategies": {},
            "global_hashtags": [],
            "timezone_optimization": {},
            "language_variants": {}
        }
        
        # Regional hashtag mapping
        region_hashtags = {
            "north_america": [
                "#NYCFood", "#TorontoEats", "#LAEats", "#ChicagoFood", "#MiamiEats",
                "#CanadianFood", "#USBusiness", "#NorthAmericaEats"
            ],
            "europe": [
                "#LondonRestaurants", "#ParisRestaurants", "#BerlinFood", "#AmsterdamEats",
                "#UKRestaurants", "#EuropeanDining", "#EuropeBusiness"
            ],
            "asia_pacific": [
                "#TokyoFood", "#SydneyDining", "#SingaporeFood", "#MelbourneCafe",
                "#AsianFood", "#PacificDining", "#AustralianFood"
            ],
            "global": [
                "#GlobalRestaurants", "#InternationalBusiness", "#GlobalSME", "#SMEAnalytica"
            ]
        }
        
        # Create strategy for each target region
        for region in target_regions:
            region_key = region.lower().replace(" ", "_")
            if region_key in region_hashtags:
                # Select optimal combinations for this region
                combinations = self.optimizer.generate_optimal_combinations(
                    content_type="regional_focus",
                    target_audience="international_business",
                    count=3
                )
                
                # Add regional hashtags
                regional_tags = region_hashtags[region_key]
                
                strategy["regional_strategies"][region] = {
                    "primary_hashtags": regional_tags[:4],
                    "optimal_combinations": [combo.hashtags for combo in combinations],
                    "best_posting_times": self._get_regional_posting_times(region),
                    "language_hashtags": self._get_language_hashtags_for_region(region)
                }
        
        # Global hashtags that work everywhere
        strategy["global_hashtags"] = [
            "#SMEAnalytica", "#BusinessIntelligence", "#RestaurantTech", 
            "#DataAnalytics", "#SmallBusiness", "#AIforBusiness"
        ]
        
        # Language-specific recommendations
        strategy["language_variants"] = {
            "spanish_markets": list(self.multilingual_hashtags["spanish"])[:5],
            "french_markets": list(self.multilingual_hashtags["french"])[:5],
            "german_markets": list(self.multilingual_hashtags["german"])[:5]
        }
        
        return strategy
    
    def _get_regional_posting_times(self, region: str) -> List[str]:
        """Get optimal posting times for different regions"""
        times = {
            "north_america": ["09:00 EST", "13:00 EST", "17:00 EST"],
            "europe": ["09:00 GMT", "13:00 GMT", "17:00 GMT"],
            "asia_pacific": ["09:00 JST", "13:00 JST", "17:00 JST"],
            "global": ["12:00 UTC", "16:00 UTC", "20:00 UTC"]
        }
        return times.get(region.lower().replace(" ", "_"), times["global"])
    
    def _get_language_hashtags_for_region(self, region: str) -> List[str]:
        """Get language-specific hashtags for region"""
        mapping = {
            "europe": list(self.multilingual_hashtags["french"])[:3] + list(self.multilingual_hashtags["german"])[:2],
            "north_america": list(self.multilingual_hashtags["spanish"])[:3],
            "asia_pacific": [],  # English primarily
            "global": list(self.multilingual_hashtags["spanish"])[:2]
        }
        return mapping.get(region.lower().replace(" ", "_"), [])
    
    async def analyze_viral_hashtag_opportunities(self) -> Dict[str, Any]:
        """Identify hashtag combinations with highest viral potential"""
        
        # Get trending hashtags
        trending = await self.discovery.discover_trending_hashtags(count=15)
        
        # Get high-performing hashtags
        top_performers = self.analytics.get_top_performing_hashtags(limit=20)
        
        viral_opportunities = {
            "viral_combinations": [],
            "trending_gaps": [],
            "emerging_trends": [],
            "viral_score_factors": {
                "trend_momentum": 0.3,
                "engagement_potential": 0.25,
                "reach_multiplier": 0.2,
                "timing_advantage": 0.15,
                "competition_gap": 0.1
            }
        }
        
        # Analyze viral combinations
        for trend in trending:
            if trend.is_worth_using() and trend.trend_score > 8.0:
                # Create viral combinations
                viral_combo = self._create_viral_combination(trend, top_performers)
                if viral_combo:
                    viral_opportunities["viral_combinations"].append(viral_combo)
        
        # Find trending gaps
        for trend in trending:
            if trend.opportunity_window > 10 and trend.trend_score > 7.5:
                viral_opportunities["trending_gaps"].append({
                    "hashtag": trend.hashtag,
                    "opportunity_score": trend.trend_score,
                    "window_remaining": trend.opportunity_window,
                    "growth_rate": f"{trend.growth_rate:.1%}",
                    "action": "Immediate adoption recommended"
                })
        
        # Identify emerging trends
        emerging = [t for t in trending if t.opportunity_window > 20 and t.growth_rate > 0.5]
        for trend in emerging:
            viral_opportunities["emerging_trends"].append({
                "hashtag": trend.hashtag,
                "emergence_score": trend.trend_score,
                "growth_trajectory": f"{trend.growth_rate:.1%}",
                "predicted_peak": trend.predicted_peak.strftime("%Y-%m-%d"),
                "strategy": "Early adoption for maximum advantage"
            })
        
        return viral_opportunities
    
    def _create_viral_combination(self, trending_hashtag: TrendingHashtag, 
                                 top_performers: List[HashtagPerformance]) -> Optional[Dict[str, Any]]:
        """Create viral hashtag combination around trending hashtag"""
        
        # Start with trending hashtag
        combo = [trending_hashtag.hashtag]
        
        # Add brand hashtag
        combo.append("#SMEAnalytica")
        
        # Add complementary high-performers
        for performer in top_performers:
            if len(combo) >= 4:
                break
            if performer.hashtag not in combo and performer.calculate_performance_score() > 7.0:
                combo.append(performer.hashtag)
        
        # Calculate viral score
        viral_score = (
            trending_hashtag.trend_score * 0.4 +
            len(combo) * 1.5 +  # Combination synergy
            trending_hashtag.growth_rate * 10 +  # Growth momentum
            (30 - trending_hashtag.opportunity_window) * 0.2  # Urgency factor
        )
        
        return {
            "hashtags": combo,
            "viral_score": min(viral_score, 10.0),
            "trending_anchor": trending_hashtag.hashtag,
            "predicted_reach": int(trending_hashtag.current_volume * (1 + trending_hashtag.growth_rate)),
            "window_remaining": trending_hashtag.opportunity_window,
            "usage_strategy": "Use immediately for maximum viral potential"
        }
    
    def get_hashtag_performance_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive hashtag performance dashboard"""
        
        # Get performance data
        top_performers = self.analytics.get_top_performing_hashtags(limit=10)
        all_hashtags = self.analytics.get_top_performing_hashtags(limit=100)
        
        # Calculate statistics
        dashboard = {
            "overview": {
                "total_hashtags_tracked": len(all_hashtags),
                "high_performers": len([h for h in all_hashtags if h.calculate_performance_score() > 7.0]),
                "overused_hashtags": len([h for h in all_hashtags if h.is_overused()]),
                "avg_performance_score": round(
                    statistics.mean([h.calculate_performance_score() for h in all_hashtags]) if all_hashtags else 0, 2
                )
            },
            "top_performers": [
                {
                    "hashtag": h.hashtag,
                    "performance_score": h.calculate_performance_score(),
                    "engagement_rate": f"{h.engagement_rate:.2%}",
                    "reach": h.reach,
                    "lifecycle_stage": h.lifecycle_stage.value
                }
                for h in top_performers[:5]
            ],
            "category_performance": self._analyze_category_performance(all_hashtags),
            "lifecycle_distribution": self._analyze_lifecycle_distribution(all_hashtags),
            "recommendations": self._generate_dashboard_recommendations(all_hashtags)
        }
        
        return dashboard
    
    def _analyze_category_performance(self, hashtags: List[HashtagPerformance]) -> Dict[str, Any]:
        """Analyze performance by hashtag category"""
        category_stats = defaultdict(list)
        
        for hashtag in hashtags:
            category_stats[hashtag.category.value].append(hashtag.calculate_performance_score())
        
        return {
            category: {
                "count": len(scores),
                "avg_score": round(statistics.mean(scores), 2),
                "top_score": round(max(scores), 2) if scores else 0
            }
            for category, scores in category_stats.items()
        }
    
    def _analyze_lifecycle_distribution(self, hashtags: List[HashtagPerformance]) -> Dict[str, int]:
        """Analyze hashtag distribution across lifecycle stages"""
        distribution = Counter(h.lifecycle_stage.value for h in hashtags)
        return dict(distribution)
    
    def _generate_dashboard_recommendations(self, hashtags: List[HashtagPerformance]) -> List[str]:
        """Generate recommendations based on dashboard analysis"""
        recommendations = []
        
        # Overuse warnings
        overused = [h for h in hashtags if h.is_overused()]
        if overused:
            recommendations.append(f"Rotate {len(overused)} overused hashtags to maintain effectiveness")
        
        # Performance opportunities
        high_performers = [h for h in hashtags if h.calculate_performance_score() > 8.0]
        if high_performers:
            recommendations.append(f"Increase usage of {len(high_performers)} high-performing hashtags")
        
        # Lifecycle management
        declining = [h for h in hashtags if h.lifecycle_stage == HashtagLifecycle.DECLINING]
        if declining:
            recommendations.append(f"Replace {len(declining)} declining hashtags with emerging trends")
        
        # Category balance
        category_counts = Counter(h.category.value for h in hashtags)
        if category_counts.get("trending", 0) < 3:
            recommendations.append("Add more trending hashtags to capture viral opportunities")
        
        return recommendations

# Usage example and testing functions
async def main():
    """Example usage of the hashtag intelligence system"""
    
    # Initialize the system
    agent = HashtagIntelligenceAgent()
    
    print("🔍 SME Analytica Hashtag Intelligence System")
    print("=" * 50)
    
    # Get optimal hashtags for content
    result = await agent.get_optimal_hashtags_for_content(
        content_type="educational",
        theme="data_insights", 
        target_audience="restaurant_owners"
    )
    
    print("\n📊 Optimal Hashtags for Educational Content:")
    primary = result["primary_combination"]
    print(f"Hashtags: {', '.join(primary['hashtags'])}")
    print(f"Predicted Reach: {primary['metrics']['predicted_reach']:,}")
    print(f"Predicted Engagement: {primary['metrics']['predicted_engagement']:.2%}")
    print(f"Total Score: {primary['metrics']['total_score']:.1f}/10")
    
    # Show trending opportunities
    if result["trending_opportunities"]:
        print("\n🔥 Trending Opportunities:")
        for trend in result["trending_opportunities"]:
            print(f"  {trend['hashtag']} - Score: {trend['trend_score']:.1f}, Window: {trend['opportunity_window']} days")
    
    # Get daily recommendations
    daily_recs = await agent.get_daily_hashtag_recommendations()
    print(f"\n📅 Daily Recommendations for {daily_recs['date']}:")
    print(f"Morning: {', '.join(daily_recs['morning_post']['hashtags'])}")
    print(f"Afternoon: {', '.join(daily_recs['afternoon_post']['hashtags'])}")
    print(f"Evening: {', '.join(daily_recs['evening_post']['hashtags'])}")
    
    # Show performance dashboard
    dashboard = agent.get_hashtag_performance_dashboard()
    print(f"\n📈 Performance Dashboard:")
    print(f"Total Hashtags Tracked: {dashboard['overview']['total_hashtags_tracked']}")
    print(f"High Performers: {dashboard['overview']['high_performers']}")
    print(f"Average Performance Score: {dashboard['overview']['avg_performance_score']}")
    
    print("\n✅ Hashtag Intelligence System Ready!")

if __name__ == "__main__":
    asyncio.run(main())