"""
Intelligent Community Engagement System for SME Analytica
Builds relationships with influencers, creates community, and drives business growth
"""

import asyncio
import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass, asdict
import random
import re
import logging
from pathlib import Path

class InfluencerTier(str, Enum):
    """Influencer tiers based on follower count and influence"""
    NANO = "nano"           # 1K-10K followers
    MICRO = "micro"         # 10K-100K followers  
    MACRO = "macro"         # 100K-1M followers
    MEGA = "mega"           # 1M+ followers

class RelationshipStatus(str, Enum):
    """Relationship status with community members"""
    PROSPECT = "prospect"           # Identified but no engagement
    ENGAGED = "engaged"             # Initial engagement started
    ACTIVE = "active"               # Regular interaction
    ADVOCATE = "advocate"           # Promotes SME Analytica
    CUSTOMER = "customer"           # Business customer
    PARTNER = "partner"             # Strategic partner

class EngagementStrategy(str, Enum):
    """Engagement strategies for community building"""
    INFLUENCER_TARGETING = "influencer_targeting"
    COMMUNITY_BUILDING = "community_building"
    CONVERSION_FOCUSED = "conversion_focused"
    BRAND_AWARENESS = "brand_awareness"
    VIRAL_AMPLIFICATION = "viral_amplification"
    THOUGHT_LEADERSHIP = "thought_leadership"

class EngagementPriority(str, Enum):
    """Engagement priority levels"""
    CRITICAL = "critical"           # Immediate response needed
    HIGH = "high"                   # Respond within 2 hours
    MEDIUM = "medium"               # Respond within 24 hours
    LOW = "low"                     # Respond when convenient

class CommunityType(str, Enum):
    """Types of community members"""
    RESTAURANT_OWNER = "restaurant_owner"
    CHEF = "chef"
    HOTEL_MANAGER = "hotel_manager"
    RETAIL_OWNER = "retail_owner"
    INDUSTRY_EXPERT = "industry_expert"
    TECH_INFLUENCER = "tech_influencer"
    MEDIA_CONTACT = "media_contact"
    POTENTIAL_PARTNER = "potential_partner"
    COMPETITOR = "competitor"

@dataclass
class InfluencerProfile:
    """Complete influencer profile with scoring and relationship data"""
    username: str
    display_name: str
    follower_count: int
    following_count: int
    tweet_count: int
    bio: str
    location: str
    website: str
    tier: InfluencerTier
    community_type: CommunityType
    relevance_score: float          # 1-10 relevance to SME Analytica
    influence_score: float          # 1-10 influence in their niche
    engagement_rate: float          # Average engagement rate
    response_rate: float            # How often they respond to replies
    optimal_engagement_times: List[str]  # Best times to engage
    interests: List[str]
    recent_topics: List[str]
    relationship_status: RelationshipStatus
    first_contact_date: Optional[datetime] = None
    last_engagement_date: Optional[datetime] = None
    engagement_history: List[Dict] = None
    conversion_potential: float = 0.0    # 1-10 likelihood to convert
    business_value_score: float = 0.0    # 1-10 potential business value
    notes: str = ""

@dataclass  
class CommunityMember:
    """Community member with lifecycle tracking"""
    profile: InfluencerProfile
    lifecycle_stage: RelationshipStatus
    engagement_count: int = 0
    positive_interactions: int = 0
    negative_interactions: int = 0
    business_inquiries: int = 0
    demo_requests: int = 0
    referrals_made: int = 0
    lifetime_value: float = 0.0
    acquisition_cost: float = 0.0
    roi: float = 0.0
    next_engagement_action: str = ""
    priority_level: EngagementPriority = EngagementPriority.MEDIUM

@dataclass
class EngagementOpportunity:
    """Specific engagement opportunity with context"""
    member: CommunityMember
    content_id: str
    content_text: str
    opportunity_type: str           # reply, quote_tweet, retweet, like
    urgency_score: float           # 1-10
    conversion_potential: float    # 1-10
    engagement_context: str        # Why this is a good opportunity
    suggested_response: str
    optimal_timing: datetime
    expected_outcome: str
    success_metrics: Dict[str, float]

class InfluencerTargeting:
    """Advanced influencer targeting and community engagement system"""
    
    def __init__(self, db_path: str = "data/community_database.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(exist_ok=True)
        self.logger = logging.getLogger(__name__)
        
        # Initialize database
        self._init_database()
        
        # Load configuration
        self.industry_keywords = self._load_industry_keywords()
        self.engagement_templates = self._load_engagement_templates()
        self.scoring_weights = self._load_scoring_weights()
        
        # Track daily limits and performance
        self.daily_limits = {
            "total_engagements": 100,
            "new_follows": 20,
            "replies": 30,
            "quote_tweets": 10,
            "direct_outreach": 5
        }
        
        self.performance_metrics = {
            "engagement_rate": 0.0,
            "response_rate": 0.0,
            "conversion_rate": 0.0,
            "follower_growth_rate": 0.0
        }
    
    def _init_database(self):
        """Initialize SQLite database for community management"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS influencer_profiles (
                    username TEXT PRIMARY KEY,
                    display_name TEXT,
                    follower_count INTEGER,
                    following_count INTEGER,
                    tweet_count INTEGER,
                    bio TEXT,
                    location TEXT,
                    website TEXT,
                    tier TEXT,
                    community_type TEXT,
                    relevance_score REAL,
                    influence_score REAL,
                    engagement_rate REAL,
                    response_rate REAL,
                    optimal_engagement_times TEXT,
                    interests TEXT,
                    recent_topics TEXT,
                    relationship_status TEXT,
                    first_contact_date TEXT,
                    last_engagement_date TEXT,
                    conversion_potential REAL,
                    business_value_score REAL,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS engagement_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    engagement_type TEXT,
                    content_id TEXT,
                    content_text TEXT,
                    our_response TEXT,
                    engagement_date TIMESTAMP,
                    response_received BOOLEAN,
                    sentiment_score REAL,
                    conversion_outcome TEXT,
                    business_value REAL,
                    FOREIGN KEY (username) REFERENCES influencer_profiles (username)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS community_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    metric_date DATE,
                    follower_count INTEGER,
                    engagement_count INTEGER,
                    positive_interactions INTEGER,
                    negative_interactions INTEGER,
                    business_inquiries INTEGER,
                    demo_requests INTEGER,
                    referrals_made INTEGER,
                    lifetime_value REAL,
                    FOREIGN KEY (username) REFERENCES influencer_profiles (username)
                )
            """)
            
            conn.execute("""
                CREATE TABLE IF NOT EXISTS engagement_opportunities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    content_id TEXT,
                    opportunity_type TEXT,
                    urgency_score REAL,
                    conversion_potential REAL,
                    suggested_response TEXT,
                    optimal_timing TIMESTAMP,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (username) REFERENCES influencer_profiles (username)
                )
            """)
    
    def _load_industry_keywords(self) -> Dict[str, Dict[str, Any]]:
        """Load industry-specific keywords for targeting"""
        return {
            "restaurant_primary": {
                "restaurant analytics": {"weight": 10, "conversion_potential": 9},
                "dynamic pricing": {"weight": 10, "conversion_potential": 9},
                "menuflow": {"weight": 9, "conversion_potential": 8},
                "pos integration": {"weight": 8, "conversion_potential": 8},
                "restaurant technology": {"weight": 8, "conversion_potential": 7},
                "hospitality ai": {"weight": 7, "conversion_potential": 7},
                "restaurant data": {"weight": 7, "conversion_potential": 6},
                "menu optimization": {"weight": 6, "conversion_potential": 6}
            },
            "business_intelligence": {
                "business analytics": {"weight": 8, "conversion_potential": 6},
                "small business data": {"weight": 7, "conversion_potential": 7},
                "business intelligence": {"weight": 7, "conversion_potential": 5},
                "data driven decisions": {"weight": 6, "conversion_potential": 5},
                "retail analytics": {"weight": 6, "conversion_potential": 6},
                "hotel analytics": {"weight": 8, "conversion_potential": 8}
            },
            "pain_points": {
                "pricing struggles": {"weight": 9, "conversion_potential": 9},
                "profit margins": {"weight": 8, "conversion_potential": 8},
                "inventory management": {"weight": 7, "conversion_potential": 7},
                "customer insights": {"weight": 6, "conversion_potential": 6},
                "operational efficiency": {"weight": 6, "conversion_potential": 6},
                "competition analysis": {"weight": 5, "conversion_potential": 5}
            },
            "buying_signals": {
                "looking for solution": {"weight": 10, "conversion_potential": 10},
                "need recommendations": {"weight": 9, "conversion_potential": 9},
                "evaluating options": {"weight": 8, "conversion_potential": 8},
                "budget approved": {"weight": 10, "conversion_potential": 10},
                "demo request": {"weight": 10, "conversion_potential": 10},
                "free trial": {"weight": 8, "conversion_potential": 8}
            }
        }
    
    def _load_engagement_templates(self) -> Dict[str, Dict[str, List[str]]]:
        """Load engagement templates for different scenarios"""
        return {
            "initial_contact": {
                "restaurant_owner": [
                    "Hi {name}! Love your insights on restaurant operations. We help restaurant owners like you boost margins ~10% through AI-powered analytics. Would be happy to share some industry data that might interest you! 📊",
                    "Great point about {topic}! At SME Analytica, we've seen this challenge across 500+ restaurants. Our MenuFlow solution addresses exactly this through dynamic pricing. Happy to discuss the approach! 🚀",
                    "Your experience resonates with many restaurant owners we work with. We've developed analytics tools specifically for this challenge - would love to share what we've learned from the data! 💡"
                ],
                "industry_expert": [
                    "Excellent analysis on {topic}! This aligns perfectly with the trends we're seeing in restaurant analytics. Would love to exchange insights on how AI is transforming hospitality operations 🤝",
                    "Your expertise in {area} is impressive! We're building AI analytics specifically for restaurants/hotels and would value your perspective on industry needs. Happy to share our research findings! 📈",
                    "Spot on about {insight}! This is exactly why we built MenuFlow - to address these gaps in restaurant analytics. Would be great to discuss the technical approaches with someone of your expertise! 🎯"
                ],
                "media_contact": [
                    "Great coverage of {topic}! We're seeing similar trends in our restaurant analytics research. Would be happy to share data/insights that might be valuable for future stories 📰",
                    "Your article on {subject} was insightful! SME Analytica has unique data on this topic from 500+ restaurants. Would love to be a resource for industry insights! 📊",
                    "Excellent journalism on {topic}! We have some interesting case studies on AI in restaurants that might complement your coverage. Happy to share! 🎤"
                ],
                "potential_partner": [
                    "Interesting approach to {topic}! We're always looking for integration opportunities that benefit restaurant owners. Would love to explore potential synergies! 🤝",
                    "Your solutions complement what we're building at SME Analytica. There might be great partnership opportunities to serve restaurant owners better. Open to discussion! 💡",
                    "Love the focus on {area}! We're seeing demand for integrated solutions from restaurant owners. Perhaps there are collaboration opportunities worth exploring! 🚀"
                ],
                "hotel_manager": [
                    "Great insights on hotel operations! We're building similar analytics solutions for hospitality. Would love to share what we've learned from the restaurant side! 🏨",
                    "Your experience with {topic} mirrors what we see in restaurant analytics. The hospitality industry has such similar challenges across segments! 📊",
                    "Excellent point about {insight}! We're developing hotel analytics solutions and would value your perspective on industry needs. Happy to exchange ideas! 💡"
                ],
                "retail_owner": [
                    "Your retail insights are spot-on! Many of the analytics challenges are similar to what we solve for restaurants. Happy to share cross-industry learnings! 🛍️",
                    "Great point about {topic}! We're seeing similar patterns in restaurant analytics. The small business journey has so many parallels across sectors! 📈",
                    "Love your approach to {area}! We help restaurants with similar challenges through AI analytics. Would be interesting to compare notes! 💡"
                ],
                "chef": [
                    "Amazing culinary insights! We help restaurant owners optimize operations and pricing. Your chef perspective would be invaluable for our product development! 👨‍🍳",
                    "Your expertise in {area} is impressive! We're building analytics tools for restaurants and would love a chef's perspective on operational challenges! 📊",
                    "Great content about {topic}! We work with restaurant owners on data-driven decisions. A chef's operational insights would be incredibly valuable! 🍴"
                ],
                "tech_influencer": [
                    "Excellent analysis of {topic}! This aligns with what we're seeing in SME technology adoption. Would love to share insights from the restaurant analytics space! 💻",
                    "Your tech insights are valuable! We're building AI analytics for small businesses and would love to exchange thoughts on technology trends! 🚀",
                    "Great perspective on {area}! The intersection of AI and small business operations is fascinating. Happy to share what we've learned in hospitality! 📱"
                ]
            },
            "relationship_building": {
                "value_first": [
                    "Saw your question about {topic}. Here's a free insight from our restaurant analytics: [specific data point]. Hope it helps! Always happy to share industry knowledge 💡",
                    "Your challenge with {issue} is common. We analyzed this across 500+ restaurants and found [insight]. Happy to share the full research if useful! 📊",
                    "Great discussion on {topic}! Our data shows [specific finding]. This might add to the conversation - no agenda, just sharing knowledge! 🤝"
                ],
                "thought_leadership": [
                    "Building on your point about {topic}: Our restaurant analytics research reveals [insight]. The implications for the industry are significant 📈",
                    "Your analysis of {trend} is spot-on. We're seeing this accelerate in restaurant data - the convergence of AI and hospitality is creating huge opportunities 🚀",
                    "Agree completely on {point}. The restaurant industry is at an inflection point with AI analytics. The early adopters are seeing 10%+ margin improvements 💪"
                ]
            },
            "conversion_focused": {
                "soft_pitch": [
                    "This challenge you mentioned is exactly what MenuFlow solves for restaurants. We've helped similar establishments boost margins 10%+ through AI pricing. Happy to share a quick case study! 📈",
                    "Your pain point resonates! We built SME Analytica specifically for this. Would love to show you a 15-min demo of how other restaurants solved this exact issue 🎯",
                    "Sounds like you're dealing with what we call the 'data visibility gap.' We have a solution that's helped 500+ restaurants turn their POS data into profit. Worth a quick chat? ☕"
                ],
                "direct_cta": [
                    "Based on your posts about {challenge}, I think MenuFlow could save you significant time and increase profits. Free 15-min demo available - interested? 🚀",
                    "Your restaurant seems perfect for our analytics platform. We're helping similar establishments boost margins ~10%. Would a brief demo be valuable? 📊",
                    "Given your interest in {topic}, you might find SME Analytica interesting. We offer free consultations for restaurant owners. Worth 15 minutes? 💡"
                ]
            }
        }
    
    def _load_scoring_weights(self) -> Dict[str, float]:
        """Load scoring weights for influencer evaluation"""
        return {
            "follower_count": 0.15,
            "engagement_rate": 0.25,
            "relevance_score": 0.30,
            "response_rate": 0.10,
            "business_potential": 0.20
        }
    
    async def discover_influencers(self, keywords: List[str], limit: int = 50) -> List[InfluencerProfile]:
        """Discover new influencers based on keywords and criteria"""
        discovered_profiles = []
        
        # This would integrate with Twitter API to search for users
        # For now, we'll return the curated database
        curated_influencers = self._get_curated_influencer_database()
        
        for profile in curated_influencers:
            # Score relevance based on keywords
            relevance = self._calculate_keyword_relevance(profile, keywords)
            if relevance >= 3.0:  # Lower threshold to include more profiles
                profile.relevance_score = max(relevance, profile.relevance_score)
                discovered_profiles.append(profile)
        
        # Sort by composite score
        scored_profiles = []
        for profile in discovered_profiles:
            composite_score = self._calculate_composite_score(profile)
            scored_profiles.append((profile, composite_score))
        
        scored_profiles.sort(key=lambda x: x[1], reverse=True)
        return [profile for profile, score in scored_profiles[:limit]]
    
    def _get_curated_influencer_database(self) -> List[InfluencerProfile]:
        """Return curated database of restaurant industry influencers"""
        return [
            # Restaurant Owners & Operators
            InfluencerProfile(
                username="ChefMarcusRestaurant",
                display_name="Chef Marcus Rodriguez",
                follower_count=15000,
                following_count=2500,
                tweet_count=8500,
                bio="Award-winning chef & restaurant owner. 3 locations in Miami. Sharing industry insights & growth strategies.",
                location="Miami, FL",
                website="marcusrestaurants.com",
                tier=InfluencerTier.MICRO,
                community_type=CommunityType.RESTAURANT_OWNER,
                relevance_score=9.2,
                influence_score=8.5,
                engagement_rate=0.085,
                response_rate=0.65,
                optimal_engagement_times=["9:00", "13:00", "19:00"],
                interests=["restaurant operations", "staff management", "customer experience", "food costs"],
                recent_topics=["rising food costs", "labor shortage", "technology adoption"],
                relationship_status=RelationshipStatus.PROSPECT,
                conversion_potential=8.5,
                business_value_score=9.0,
                engagement_history=[]
            ),
            
            InfluencerProfile(
                username="SarahsRestaurantGroup",
                display_name="Sarah Chen - Restaurant Group Owner",
                follower_count=22000,
                following_count=1800,
                tweet_count=12000,
                bio="Owner of 5 restaurants in NYC. Helping other restaurant owners succeed. Analytics & operations focused.",
                location="New York, NY",
                website="sarahsrestaurants.com",
                tier=InfluencerTier.MICRO,
                community_type=CommunityType.RESTAURANT_OWNER,
                relevance_score=9.8,
                influence_score=9.0,
                engagement_rate=0.092,
                response_rate=0.78,
                optimal_engagement_times=["8:00", "12:00", "17:00"],
                interests=["restaurant analytics", "multi-unit operations", "profitability", "technology"],
                recent_topics=["restaurant analytics", "POS integration", "margin optimization"],
                relationship_status=RelationshipStatus.PROSPECT,
                conversion_potential=9.5,
                business_value_score=9.8,
                engagement_history=[]
            ),
            
            # Industry Experts & Consultants
            InfluencerProfile(
                username="RestaurantTechGuru",
                display_name="David Kim - Restaurant Tech Consultant",
                follower_count=35000,
                following_count=4200,
                tweet_count=18500,
                bio="Restaurant technology consultant. Helping restaurants optimize operations through smart tech integration.",
                location="San Francisco, CA",
                website="restauranttech.consulting",
                tier=InfluencerTier.MACRO,
                community_type=CommunityType.INDUSTRY_EXPERT,
                relevance_score=9.5,
                influence_score=8.8,
                engagement_rate=0.068,
                response_rate=0.55,
                optimal_engagement_times=["10:00", "14:00", "16:00"],
                interests=["restaurant technology", "POS systems", "analytics", "automation"],
                recent_topics=["AI in restaurants", "data analytics", "operational efficiency"],
                relationship_status=RelationshipStatus.PROSPECT,
                conversion_potential=7.5,
                business_value_score=8.2,
                engagement_history=[]
            ),
            
            InfluencerProfile(
                username="HospitalityDataPro",
                display_name="Maria Gonzalez - Hospitality Analytics",
                follower_count=18500,
                following_count=2100,
                tweet_count=9800,
                bio="15 years in hospitality analytics. Helping hotels & restaurants make data-driven decisions.",
                location="Las Vegas, NV",
                website="hospitalityanalytics.com",
                tier=InfluencerTier.MICRO,
                community_type=CommunityType.INDUSTRY_EXPERT,
                relevance_score=9.7,
                influence_score=8.9,
                engagement_rate=0.095,
                response_rate=0.72,
                optimal_engagement_times=["9:00", "15:00", "18:00"],
                interests=["hospitality analytics", "revenue management", "customer insights", "AI"],
                recent_topics=["predictive analytics", "dynamic pricing", "customer behavior"],
                relationship_status=RelationshipStatus.PROSPECT,
                conversion_potential=8.0,
                business_value_score=8.5,
                engagement_history=[]
            ),
            
            # Media & Publications
            InfluencerProfile(
                username="RestaurantBizMag",
                display_name="Restaurant Business Magazine",
                follower_count=125000,
                following_count=5500,
                tweet_count=35000,
                bio="Leading source for restaurant industry news, trends, and insights. Covering technology, operations & growth.",
                location="New York, NY",
                website="restaurantbusinessonline.com",
                tier=InfluencerTier.MACRO,
                community_type=CommunityType.MEDIA_CONTACT,
                relevance_score=8.5,
                influence_score=9.5,
                engagement_rate=0.035,
                response_rate=0.25,
                optimal_engagement_times=["11:00", "14:00", "16:00"],
                interests=["restaurant news", "industry trends", "technology", "business insights"],
                recent_topics=["restaurant technology", "industry challenges", "growth strategies"],
                relationship_status=RelationshipStatus.PROSPECT,
                conversion_potential=6.0,
                business_value_score=8.8,
                engagement_history=[]
            ),
            
            InfluencerProfile(
                username="NationsRestaurantNews",
                display_name="Nation's Restaurant News",
                follower_count=185000,
                following_count=8200,
                tweet_count=42000,
                bio="The premier source of news and information for the restaurant industry since 1967.",
                location="New York, NY",
                website="nrn.com",
                tier=InfluencerTier.MACRO,
                community_type=CommunityType.MEDIA_CONTACT,
                relevance_score=8.8,
                influence_score=9.8,
                engagement_rate=0.028,
                response_rate=0.20,
                optimal_engagement_times=["10:00", "13:00", "15:00"],
                interests=["restaurant industry", "business news", "technology trends", "market analysis"],
                recent_topics=["restaurant innovation", "technology adoption", "industry growth"],
                relationship_status=RelationshipStatus.PROSPECT,
                conversion_potential=5.5,
                business_value_score=9.2,
                engagement_history=[]
            ),
            
            # Hotel Industry  
            InfluencerProfile(
                username="BoutiqueHotelOwner",
                display_name="Alex Thompson - Boutique Hotel Owner",
                follower_count=12500,
                following_count=1900,
                tweet_count=6800,
                bio="Owner of 3 boutique hotels in Austin. Passionate about guest experience & operational efficiency.",
                location="Austin, TX",
                website="austinboutiquehotels.com",
                tier=InfluencerTier.MICRO,
                community_type=CommunityType.HOTEL_MANAGER,
                relevance_score=8.5,
                influence_score=7.8,
                engagement_rate=0.105,
                response_rate=0.68,
                optimal_engagement_times=["8:00", "16:00", "20:00"],
                interests=["hotel management", "guest experience", "revenue optimization", "technology"],
                recent_topics=["occupancy optimization", "guest satisfaction", "hotel technology"],
                relationship_status=RelationshipStatus.PROSPECT,
                conversion_potential=8.2,
                business_value_score=7.8,
                engagement_history=[]
            ),
            
            # Retail Business Owners
            InfluencerProfile(
                username="RetailSuccessStory",
                display_name="Jennifer Liu - Retail Business Coach",
                follower_count=28000,
                following_count=3200,
                tweet_count=14500,
                bio="Helping retail business owners optimize operations & increase profits. Former multi-store owner.",
                location="Chicago, IL",
                website="retailsuccess.coach",
                tier=InfluencerTier.MICRO,
                community_type=CommunityType.RETAIL_OWNER,
                relevance_score=7.8,
                influence_score=8.2,
                engagement_rate=0.078,
                response_rate=0.62,
                optimal_engagement_times=["9:00", "13:00", "17:00"],
                interests=["retail operations", "inventory management", "customer analytics", "profitability"],
                recent_topics=["retail analytics", "inventory optimization", "customer insights"],
                relationship_status=RelationshipStatus.PROSPECT,
                conversion_potential=7.5,
                business_value_score=7.2,
                engagement_history=[]
            ),
            
            # Tech Influencers in SME Space
            InfluencerProfile(
                username="SmallBizTechTrends",
                display_name="Michael Roberts - SME Technology Analyst",
                follower_count=45000,
                following_count=4800,
                tweet_count=22000,
                bio="Technology analyst focused on small business solutions. Covering AI, analytics & automation for SMEs.",
                location="Austin, TX",
                website="smebiztech.com",
                tier=InfluencerTier.MACRO,
                community_type=CommunityType.TECH_INFLUENCER,
                relevance_score=8.2,
                influence_score=8.5,
                engagement_rate=0.058,
                response_rate=0.45,
                optimal_engagement_times=["10:00", "14:00", "16:00"],
                interests=["SME technology", "business analytics", "AI for small business", "automation"],
                recent_topics=["AI adoption in SMEs", "business intelligence tools", "automation trends"],
                relationship_status=RelationshipStatus.PROSPECT,
                conversion_potential=6.8,
                business_value_score=7.5,
                engagement_history=[]
            ),
            
            # Potential Partners
            InfluencerProfile(
                username="POSSystemsPro",
                display_name="POS Systems Professional",
                follower_count=15800,
                following_count=2400,
                tweet_count=11200,
                bio="POS systems consultant & integrator. Helping restaurants choose the right technology stack.",
                location="Orlando, FL",
                website="possystemspro.com",
                tier=InfluencerTier.MICRO,
                community_type=CommunityType.POTENTIAL_PARTNER,
                relevance_score=8.8,
                influence_score=7.5,
                engagement_rate=0.082,
                response_rate=0.58,
                optimal_engagement_times=["9:00", "14:00", "17:00"],
                interests=["POS systems", "restaurant technology", "integrations", "analytics"],
                recent_topics=["POS integration", "restaurant tech stack", "data analytics"],
                relationship_status=RelationshipStatus.PROSPECT,
                conversion_potential=7.2,
                business_value_score=8.0,
                engagement_history=[]
            )
        ]
    
    def _calculate_keyword_relevance(self, profile: InfluencerProfile, keywords: List[str]) -> float:
        """Calculate relevance score based on profile content and keywords"""
        relevance_score = 0.0
        
        # Check bio for keywords
        bio_text = profile.bio.lower()
        for keyword in keywords:
            if keyword.lower() in bio_text:
                relevance_score += 2.0
        
        # Check interests
        for interest in profile.interests:
            for keyword in keywords:
                if keyword.lower() in interest.lower():
                    relevance_score += 1.5
        
        # Check recent topics
        for topic in profile.recent_topics:
            for keyword in keywords:
                if keyword.lower() in topic.lower():
                    relevance_score += 1.0
        
        # Industry-specific keyword matching
        for category, keyword_dict in self.industry_keywords.items():
            for keyword, data in keyword_dict.items():
                if keyword in bio_text or any(keyword in interest.lower() for interest in profile.interests):
                    relevance_score += data["weight"] * 0.5
        
        return min(relevance_score, 10.0)
    
    def _calculate_composite_score(self, profile: InfluencerProfile) -> float:
        """Calculate composite score for influencer ranking"""
        weights = self.scoring_weights
        
        # Normalize follower count (log scale)
        import math
        follower_score = min(math.log10(profile.follower_count + 1), 6.0)
        
        composite_score = (
            follower_score * weights["follower_count"] +
            profile.engagement_rate * 100 * weights["engagement_rate"] +
            profile.relevance_score * weights["relevance_score"] +
            profile.response_rate * 10 * weights["response_rate"] +
            profile.business_value_score * weights["business_potential"]
        )
        
        return composite_score
    
    async def analyze_community_sentiment(self, username: str, content_samples: List[str]) -> Dict[str, Any]:
        """Analyze community member's sentiment and communication style"""
        
        # Simple sentiment analysis (in production, use advanced NLP)
        positive_indicators = ["great", "excellent", "amazing", "love", "helpful", "successful", "growth"]
        negative_indicators = ["terrible", "awful", "hate", "problem", "issue", "struggle", "difficult"]
        
        sentiment_scores = []
        topics = []
        communication_style = {
            "formal": 0,
            "casual": 0,
            "technical": 0,
            "business_focused": 0
        }
        
        for content in content_samples:
            content_lower = content.lower()
            
            # Sentiment scoring
            pos_count = sum(1 for word in positive_indicators if word in content_lower)
            neg_count = sum(1 for word in negative_indicators if word in content_lower)
            sentiment_score = (pos_count - neg_count) / max(len(content.split()), 1)
            sentiment_scores.append(sentiment_score)
            
            # Communication style analysis
            if any(word in content_lower for word in ["please", "thank you", "sincerely", "regards"]):
                communication_style["formal"] += 1
            if any(word in content_lower for word in ["hey", "awesome", "cool", "lol", "btw"]):
                communication_style["casual"] += 1
            if any(word in content_lower for word in ["api", "integration", "analytics", "data", "algorithm"]):
                communication_style["technical"] += 1
            if any(word in content_lower for word in ["revenue", "profit", "roi", "business", "growth"]):
                communication_style["business_focused"] += 1
            
            # Topic extraction (simple keyword matching)
            for category, keyword_dict in self.industry_keywords.items():
                for keyword in keyword_dict.keys():
                    if keyword.replace('_', ' ') in content_lower:
                        topics.append(keyword)
        
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0
        dominant_style = max(communication_style.items(), key=lambda x: x[1])[0]
        
        return {
            "average_sentiment": avg_sentiment,
            "sentiment_category": "positive" if avg_sentiment > 0.1 else "negative" if avg_sentiment < -0.1 else "neutral",
            "communication_style": dominant_style,
            "style_scores": communication_style,
            "main_topics": list(set(topics)),
            "engagement_receptivity": self._calculate_engagement_receptivity(avg_sentiment, dominant_style)
        }
    
    def _calculate_engagement_receptivity(self, sentiment: float, style: str) -> float:
        """Calculate how receptive someone might be to engagement"""
        base_receptivity = 5.0
        
        # Sentiment adjustment
        if sentiment > 0.2:
            base_receptivity += 2.0
        elif sentiment < -0.2:
            base_receptivity -= 1.5
        
        # Style adjustment
        style_modifiers = {
            "business_focused": 1.5,
            "technical": 1.0,
            "formal": 0.5,
            "casual": 1.2
        }
        
        base_receptivity += style_modifiers.get(style, 0.0)
        
        return min(max(base_receptivity, 1.0), 10.0)
    
    async def identify_engagement_opportunities(self, timeframe_hours: int = 24) -> List[EngagementOpportunity]:
        """Identify current engagement opportunities across the community"""
        opportunities = []
        
        # Get active community members
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT * FROM influencer_profiles 
                WHERE relationship_status IN ('prospect', 'engaged', 'active')
                ORDER BY business_value_score DESC, relevance_score DESC
                LIMIT 50
            """)
            
            profiles_data = cursor.fetchall()
        
        for profile_data in profiles_data:
            # Convert to InfluencerProfile object
            profile = self._row_to_profile(profile_data)
            member = CommunityMember(
                profile=profile,
                lifecycle_stage=profile.relationship_status,
                priority_level=self._determine_priority_level(profile)
            )
            
            # Simulate finding recent content (in production, use Twitter API)
            recent_content = self._simulate_recent_content(profile)
            
            for content in recent_content:
                opportunity = await self._evaluate_content_opportunity(member, content)
                if opportunity and opportunity.urgency_score >= 4.0:
                    opportunities.append(opportunity)
        
        # Sort by urgency and conversion potential
        opportunities.sort(key=lambda x: (x.urgency_score, x.conversion_potential), reverse=True)
        
        return opportunities[:20]  # Return top 20 opportunities
    
    def _row_to_profile(self, row: tuple) -> InfluencerProfile:
        """Convert database row to InfluencerProfile object"""
        return InfluencerProfile(
            username=row[0],
            display_name=row[1],
            follower_count=row[2],
            following_count=row[3],
            tweet_count=row[4],
            bio=row[5],
            location=row[6],
            website=row[7],
            tier=InfluencerTier(row[8]),
            community_type=CommunityType(row[9]),
            relevance_score=row[10],
            influence_score=row[11],
            engagement_rate=row[12],
            response_rate=row[13],
            optimal_engagement_times=json.loads(row[14]) if row[14] else [],
            interests=json.loads(row[15]) if row[15] else [],
            recent_topics=json.loads(row[16]) if row[16] else [],
            relationship_status=RelationshipStatus(row[17]),
            first_contact_date=datetime.fromisoformat(row[18]) if row[18] else None,
            last_engagement_date=datetime.fromisoformat(row[19]) if row[19] else None,
            conversion_potential=row[20] or 0.0,
            business_value_score=row[21] or 0.0,
            notes=row[22] or "",
            engagement_history=[]
        )
    
    def _determine_priority_level(self, profile: InfluencerProfile) -> EngagementPriority:
        """Determine engagement priority for a profile"""
        if profile.business_value_score >= 9.0 and profile.conversion_potential >= 8.0:
            return EngagementPriority.CRITICAL
        elif profile.business_value_score >= 7.0 and profile.conversion_potential >= 6.0:
            return EngagementPriority.HIGH
        elif profile.relevance_score >= 7.0:
            return EngagementPriority.MEDIUM
        else:
            return EngagementPriority.LOW
    
    def _simulate_recent_content(self, profile: InfluencerProfile) -> List[Dict[str, Any]]:
        """Simulate recent content from a profile (in production, use Twitter API)"""
        content_templates = {
            CommunityType.RESTAURANT_OWNER: [
                "Struggling with food cost increases this quarter. Anyone else seeing 15%+ jumps in supplier prices? How are you managing margins?",
                "Just implemented a new POS system but the reporting is confusing. Need better analytics to understand peak hours and customer preferences.",
                "Looking for recommendations on restaurant management software. Need something that integrates with our current POS and helps with pricing decisions.",
                "Staff shortage is killing us. Anyone found good solutions for optimizing schedules and reducing labor costs without hurting service?"
            ],
            CommunityType.INDUSTRY_EXPERT: [
                "The future of restaurant technology is AI-driven analytics. Most operators are sitting on goldmines of data they're not using effectively.",
                "Seeing more restaurants adopt dynamic pricing strategies. The early adopters are reporting 8-12% margin improvements during peak periods.",
                "Restaurant industry needs to embrace data-driven decision making. Too many owners still operate on gut feeling instead of analytics.",
                "The convergence of POS systems and advanced analytics is creating unprecedented opportunities for operational optimization."
            ],
            CommunityType.HOTEL_MANAGER: [
                "Occupancy rates are recovering but ADR is still challenging. Looking for tools to optimize pricing based on demand patterns.",
                "Guest satisfaction scores improving but we need better insights into what drives repeat bookings and referrals.",
                "Revenue management is becoming more complex. Need analytics that go beyond basic occupancy tracking.",
                "The hotel industry needs better integration between booking systems and operational analytics."
            ]
        }
        
        templates = content_templates.get(profile.community_type, content_templates[CommunityType.RESTAURANT_OWNER])
        
        # Return 1-3 pieces of recent content
        num_content = random.randint(2, 3)  # Ensure we always have some content
        selected_content = random.sample(templates, min(num_content, len(templates)))
        
        return [
            {
                "id": f"tweet_{i}_{profile.username}",
                "text": content,
                "author": profile.username,
                "timestamp": datetime.now() - timedelta(hours=random.randint(1, 24)),
                "likes": random.randint(5, int(profile.follower_count * 0.02)),
                "retweets": random.randint(1, int(profile.follower_count * 0.005)),
                "replies": random.randint(2, int(profile.follower_count * 0.01))
            }
            for i, content in enumerate(selected_content)
        ]
    
    async def _evaluate_content_opportunity(self, member: CommunityMember, content: Dict[str, Any]) -> Optional[EngagementOpportunity]:
        """Evaluate if content presents a good engagement opportunity"""
        
        content_text = content["text"].lower()
        
        # Calculate urgency based on content type and timing
        urgency_score = 5.0  # Base urgency
        
        # High urgency indicators
        if any(phrase in content_text for phrase in ["looking for", "need help", "recommendations", "anyone know"]):
            urgency_score += 3.0
        
        if any(phrase in content_text for phrase in ["urgent", "asap", "immediately", "today"]):
            urgency_score += 2.0
        
        # Content relevance to SME Analytica
        relevance_boost = 0.0
        for category, keyword_dict in self.industry_keywords.items():
            for keyword, data in keyword_dict.items():
                if keyword.replace('_', ' ') in content_text:
                    relevance_boost += data["conversion_potential"] * 0.3
        
        urgency_score += relevance_boost
        
        # Time sensitivity (newer content = higher urgency)
        hours_old = (datetime.now() - content["timestamp"]).total_seconds() / 3600
        time_factor = max(1.0 - (hours_old / 24), 0.2)  # Decay over 24 hours
        urgency_score *= time_factor
        
        # Don't engage with very low-urgency opportunities
        if urgency_score < 3.0:
            return None
        
        # Calculate conversion potential
        conversion_potential = member.profile.conversion_potential
        
        # Boost conversion potential based on content
        if any(phrase in content_text for phrase in ["budget", "looking to buy", "evaluating", "demo"]):
            conversion_potential = min(conversion_potential + 2.0, 10.0)
        
        # Determine engagement type and generate response
        engagement_type, response = await self._determine_engagement_approach(member, content)
        
        # Calculate expected outcomes
        success_metrics = self._calculate_success_metrics(member, engagement_type, urgency_score)
        
        return EngagementOpportunity(
            member=member,
            content_id=content["id"],
            content_text=content["text"],
            opportunity_type=engagement_type,
            urgency_score=min(urgency_score, 10.0),
            conversion_potential=conversion_potential,
            engagement_context=self._generate_engagement_context(content_text, member.profile),
            suggested_response=response,
            optimal_timing=self._calculate_optimal_timing(member.profile),
            expected_outcome=self._predict_engagement_outcome(member, urgency_score, conversion_potential),
            success_metrics=success_metrics
        )
    
    async def _determine_engagement_approach(self, member: CommunityMember, content: Dict[str, Any]) -> Tuple[str, str]:
        """Determine the best engagement approach and generate response"""
        
        content_text = content["text"].lower()
        profile = member.profile
        
        # Determine engagement type based on content and relationship status
        if member.lifecycle_stage == RelationshipStatus.PROSPECT:
            # First contact - be helpful, not promotional
            if "?" in content["text"]:
                engagement_type = "helpful_reply"
                templates = self.engagement_templates["initial_contact"][profile.community_type.value]
            else:
                engagement_type = "value_comment"
                templates = self.engagement_templates["relationship_building"]["value_first"]
        
        elif member.lifecycle_stage == RelationshipStatus.ENGAGED:
            # Build relationship with thought leadership
            engagement_type = "thought_leadership"
            templates = self.engagement_templates["relationship_building"]["thought_leadership"]
        
        elif member.lifecycle_stage == RelationshipStatus.ACTIVE:
            # Can be more direct with conversion opportunities
            if any(phrase in content_text for phrase in ["looking for", "need solution", "recommendations"]):
                engagement_type = "soft_pitch"
                templates = self.engagement_templates["conversion_focused"]["soft_pitch"]
            else:
                engagement_type = "relationship_building"
                templates = self.engagement_templates["relationship_building"]["value_first"]
        
        else:
            engagement_type = "general_engagement"
            templates = self.engagement_templates["relationship_building"]["value_first"]
        
        # Select and customize template
        base_response = random.choice(templates)
        
        # Customize response with content-specific information
        customized_response = self._customize_response(base_response, content, profile)
        
        return engagement_type, customized_response
    
    def _customize_response(self, template: str, content: Dict[str, Any], profile: InfluencerProfile) -> str:
        """Customize response template with specific context"""
        
        response = template
        
        # Replace placeholders
        response = response.replace("{name}", profile.display_name.split()[0])
        
        # Extract topic from content for contextualization
        content_text = content["text"].lower()
        
        # Identify main topic
        topic = "restaurant operations"  # Default
        if "pricing" in content_text:
            topic = "pricing strategies"
        elif "analytics" in content_text or "data" in content_text:
            topic = "analytics and data insights"
        elif "pos" in content_text:
            topic = "POS system integration"
        elif "staff" in content_text or "labor" in content_text:
            topic = "staff management"
        elif "cost" in content_text or "margin" in content_text:
            topic = "cost management"
        
        response = response.replace("{topic}", topic)
        
        # Add specific insights based on content
        if "struggling" in content_text or "problem" in content_text:
            insight = "This is a common challenge we see across the industry"
        elif "looking for" in content_text:
            insight = "We have experience helping with exactly this type of situation"
        else:
            insight = "Your perspective on this aligns with industry trends we're tracking"
        
        response = response.replace("{insight}", insight)
        
        return response
    
    def _generate_engagement_context(self, content_text: str, profile: InfluencerProfile) -> str:
        """Generate context explaining why this is a good engagement opportunity"""
        
        contexts = []
        
        # Profile-based context
        if profile.business_value_score >= 8.0:
            contexts.append("High-value target with strong business potential")
        
        if profile.conversion_potential >= 8.0:
            contexts.append("High conversion likelihood based on profile analysis")
        
        # Content-based context
        if any(phrase in content_text.lower() for phrase in ["looking for", "need help", "recommendations"]):
            contexts.append("Direct request for help/recommendations - high engagement opportunity")
        
        if any(keyword in content_text.lower() for keyword in ["analytics", "pricing", "pos", "data"]):
            contexts.append("Content directly relevant to SME Analytica solutions")
        
        if "?" in content_text:
            contexts.append("Question format provides natural engagement opportunity")
        
        return "; ".join(contexts) if contexts else "General engagement opportunity"
    
    def _calculate_optimal_timing(self, profile: InfluencerProfile) -> datetime:
        """Calculate optimal timing for engagement based on profile"""
        
        now = datetime.now()
        
        # Use profile's optimal engagement times if available
        if profile.optimal_engagement_times:
            next_optimal_time = None
            for time_str in profile.optimal_engagement_times:
                hour = int(time_str.split(':')[0])
                
                # Find next occurrence of this hour
                target_time = now.replace(hour=hour, minute=0, second=0, microsecond=0)
                if target_time <= now:
                    target_time += timedelta(days=1)
                
                if next_optimal_time is None or target_time < next_optimal_time:
                    next_optimal_time = target_time
            
            return next_optimal_time or now + timedelta(hours=1)
        
        # Default to business hours
        if now.hour < 9:
            return now.replace(hour=9, minute=0, second=0, microsecond=0)
        elif now.hour >= 17:
            return (now + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
        else:
            return now + timedelta(minutes=30)  # Engage within 30 minutes during business hours
    
    def _predict_engagement_outcome(self, member: CommunityMember, urgency: float, conversion_potential: float) -> str:
        """Predict likely outcome of engagement"""
        
        if conversion_potential >= 8.0 and urgency >= 7.0:
            return "High likelihood of meaningful conversation leading to business inquiry"
        elif conversion_potential >= 6.0 and urgency >= 6.0:
            return "Good chance of positive response and relationship building"
        elif member.profile.response_rate >= 0.6:
            return "Likely to receive response based on historical engagement patterns"
        elif urgency >= 7.0:
            return "Timely help provided, building brand awareness and trust"
        else:
            return "General brand awareness and community building"
    
    def _calculate_success_metrics(self, member: CommunityMember, engagement_type: str, urgency: float) -> Dict[str, float]:
        """Calculate expected success metrics for engagement"""
        
        base_response_rate = member.profile.response_rate
        
        # Adjust based on engagement type
        type_multipliers = {
            "helpful_reply": 1.5,
            "value_comment": 1.2,
            "thought_leadership": 1.1,
            "soft_pitch": 0.8,
            "general_engagement": 1.0
        }
        
        multiplier = type_multipliers.get(engagement_type, 1.0)
        
        return {
            "response_probability": min(base_response_rate * multiplier, 1.0),
            "positive_sentiment_probability": 0.75 * multiplier,
            "conversion_probability": member.profile.conversion_potential / 100,
            "relationship_advancement_probability": 0.6 * multiplier,
            "business_value_score": urgency * member.profile.business_value_score / 10
        }
    
    async def execute_engagement_plan(self, opportunities: List[EngagementOpportunity], daily_limit: int = 20) -> Dict[str, Any]:
        """Execute engagement plan with tracking and analytics"""
        
        executed_engagements = []
        skipped_count = 0
        
        # Sort opportunities by priority
        sorted_opportunities = sorted(opportunities, 
                                    key=lambda x: (x.urgency_score, x.conversion_potential), 
                                    reverse=True)
        
        for i, opportunity in enumerate(sorted_opportunities):
            if i >= daily_limit:
                skipped_count += 1
                continue
            
            # Check if we've already engaged with this member today
            if await self._recently_engaged(opportunity.member.profile.username):
                skipped_count += 1
                continue
            
            # Execute engagement (in production, this would use Twitter API)
            success = await self._execute_engagement(opportunity)
            
            if success:
                executed_engagements.append({
                    "opportunity": opportunity,
                    "execution_time": datetime.now(),
                    "status": "success",
                    "expected_metrics": opportunity.success_metrics
                })
                
                # Update member relationship status if needed
                await self._update_member_status(opportunity.member)
                
                # Log engagement in database
                await self._log_engagement(opportunity)
            
            # Add delay between engagements to appear natural
            await asyncio.sleep(random.uniform(60, 300))  # 1-5 minutes between engagements
        
        # Calculate execution summary
        execution_summary = {
            "total_opportunities": len(opportunities),
            "executed_count": len(executed_engagements),
            "skipped_count": skipped_count,
            "execution_rate": (len(executed_engagements) / len(opportunities) * 100) if len(opportunities) > 0 else 0,
            "expected_responses": sum(e["expected_metrics"]["response_probability"] for e in executed_engagements),
            "expected_conversions": sum(e["expected_metrics"]["conversion_probability"] for e in executed_engagements),
            "total_business_value_score": sum(e["expected_metrics"]["business_value_score"] for e in executed_engagements),
            "engagements": executed_engagements
        }
        
        return execution_summary
    
    async def _recently_engaged(self, username: str, hours: int = 24) -> bool:
        """Check if we've recently engaged with a user"""
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT COUNT(*) FROM engagement_history 
                WHERE username = ? AND engagement_date > ?
            """, (username, cutoff_time.isoformat()))
            
            count = cursor.fetchone()[0]
        
        return count > 0
    
    async def _execute_engagement(self, opportunity: EngagementOpportunity) -> bool:
        """Execute the actual engagement (simulate for now)"""
        
        # In production, this would:
        # 1. Use Twitter API to post reply/retweet/etc.
        # 2. Handle rate limits and errors
        # 3. Track success/failure
        
        # For now, simulate success based on opportunity score
        success_probability = min(opportunity.urgency_score / 10, 0.9)
        return random.random() < success_probability
    
    async def _update_member_status(self, member: CommunityMember):
        """Update member relationship status based on engagement"""
        
        # Advance relationship status if appropriate
        if member.lifecycle_stage == RelationshipStatus.PROSPECT:
            new_status = RelationshipStatus.ENGAGED
        elif member.lifecycle_stage == RelationshipStatus.ENGAGED:
            # Don't automatically advance - wait for response
            new_status = member.lifecycle_stage
        else:
            new_status = member.lifecycle_stage
        
        # Update in database
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE influencer_profiles 
                SET relationship_status = ?, last_engagement_date = ?, updated_at = CURRENT_TIMESTAMP
                WHERE username = ?
            """, (new_status.value, datetime.now().isoformat(), member.profile.username))
    
    async def _log_engagement(self, opportunity: EngagementOpportunity):
        """Log engagement in database for analytics"""
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO engagement_history 
                (username, engagement_type, content_id, content_text, our_response, 
                 engagement_date, response_received, sentiment_score, business_value)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                opportunity.member.profile.username,
                opportunity.opportunity_type,
                opportunity.content_id,
                opportunity.content_text,
                opportunity.suggested_response,
                datetime.now().isoformat(),
                False,  # Will be updated when response is received
                0.0,    # Will be calculated when response is analyzed
                opportunity.success_metrics["business_value_score"]
            ))
    
    async def save_influencer_profiles(self, profiles: List[InfluencerProfile]):
        """Save influencer profiles to database"""
        
        with sqlite3.connect(self.db_path) as conn:
            for profile in profiles:
                conn.execute("""
                    INSERT OR REPLACE INTO influencer_profiles 
                    (username, display_name, follower_count, following_count, tweet_count,
                     bio, location, website, tier, community_type, relevance_score,
                     influence_score, engagement_rate, response_rate, optimal_engagement_times,
                     interests, recent_topics, relationship_status, first_contact_date,
                     last_engagement_date, conversion_potential, business_value_score, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    profile.username, profile.display_name, profile.follower_count,
                    profile.following_count, profile.tweet_count, profile.bio,
                    profile.location, profile.website, profile.tier.value,
                    profile.community_type.value, profile.relevance_score,
                    profile.influence_score, profile.engagement_rate, profile.response_rate,
                    json.dumps(profile.optimal_engagement_times), json.dumps(profile.interests),
                    json.dumps(profile.recent_topics), profile.relationship_status.value,
                    profile.first_contact_date.isoformat() if profile.first_contact_date else None,
                    profile.last_engagement_date.isoformat() if profile.last_engagement_date else None,
                    profile.conversion_potential, profile.business_value_score, profile.notes
                ))
    
    def get_community_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive community analytics"""
        
        with sqlite3.connect(self.db_path) as conn:
            # Community size and composition
            cursor = conn.execute("""
                SELECT community_type, COUNT(*) as count,
                       AVG(business_value_score) as avg_value,
                       AVG(conversion_potential) as avg_conversion
                FROM influencer_profiles 
                GROUP BY community_type
            """)
            community_composition = cursor.fetchall()
            
            # Relationship status distribution
            cursor = conn.execute("""
                SELECT relationship_status, COUNT(*) as count
                FROM influencer_profiles 
                GROUP BY relationship_status
            """)
            relationship_distribution = cursor.fetchall()
            
            # Recent engagement activity
            cursor = conn.execute("""
                SELECT DATE(engagement_date) as date, COUNT(*) as engagements,
                       AVG(business_value) as avg_value
                FROM engagement_history 
                WHERE engagement_date > datetime('now', '-{} days')
                GROUP BY DATE(engagement_date)
                ORDER BY date
            """.format(days))
            daily_activity = cursor.fetchall()
            
            # Conversion funnel
            cursor = conn.execute("""
                SELECT 
                    SUM(CASE WHEN relationship_status = 'prospect' THEN 1 ELSE 0 END) as prospects,
                    SUM(CASE WHEN relationship_status = 'engaged' THEN 1 ELSE 0 END) as engaged,
                    SUM(CASE WHEN relationship_status = 'active' THEN 1 ELSE 0 END) as active,
                    SUM(CASE WHEN relationship_status = 'advocate' THEN 1 ELSE 0 END) as advocates,
                    SUM(CASE WHEN relationship_status = 'customer' THEN 1 ELSE 0 END) as customers
                FROM influencer_profiles
            """)
            funnel_data = cursor.fetchone()
            
            # High-value targets
            cursor = conn.execute("""
                SELECT username, display_name, business_value_score, conversion_potential,
                       relationship_status
                FROM influencer_profiles 
                WHERE business_value_score >= 8.0 
                ORDER BY business_value_score DESC, conversion_potential DESC
                LIMIT 10
            """)
            high_value_targets = cursor.fetchall()
        
        return {
            "community_composition": [
                {"type": row[0], "count": row[1], "avg_value": row[2], "avg_conversion": row[3]}
                for row in community_composition
            ],
            "relationship_distribution": [
                {"status": row[0], "count": row[1]} for row in relationship_distribution
            ],
            "daily_activity": [
                {"date": row[0], "engagements": row[1], "avg_value": row[2]}
                for row in daily_activity
            ],
            "conversion_funnel": {
                "prospects": funnel_data[0] or 0,
                "engaged": funnel_data[1] or 0,
                "active": funnel_data[2] or 0,
                "advocates": funnel_data[3] or 0,
                "customers": funnel_data[4] or 0
            },
            "high_value_targets": [
                {
                    "username": row[0], "name": row[1], "value_score": row[2],
                    "conversion_potential": row[3], "status": row[4]
                }
                for row in high_value_targets
            ],
            "performance_metrics": self.performance_metrics
        }

# Example usage and testing
if __name__ == "__main__":
    async def main():
        # Initialize targeting system
        targeting = InfluencerTargeting()
        
        # Discover and save influencers
        print("🔍 Discovering influencers...")
        keywords = ["restaurant analytics", "dynamic pricing", "hospitality tech", "small business"]
        influencers = await targeting.discover_influencers(keywords, limit=20)
        await targeting.save_influencer_profiles(influencers)
        print(f"✅ Discovered and saved {len(influencers)} influencer profiles")
        
        # Identify engagement opportunities
        print("\n🎯 Identifying engagement opportunities...")
        opportunities = await targeting.identify_engagement_opportunities()
        print(f"✅ Found {len(opportunities)} high-quality engagement opportunities")
        
        # Display top opportunities
        print("\n🔥 Top 5 Engagement Opportunities:")
        for i, opp in enumerate(opportunities[:5], 1):
            print(f"{i}. @{opp.member.profile.username} ({opp.member.profile.community_type.value})")
            print(f"   Urgency: {opp.urgency_score:.1f}/10 | Conversion: {opp.conversion_potential:.1f}/10")
            print(f"   Context: {opp.engagement_context}")
            print(f"   Response: {opp.suggested_response[:100]}...")
            print()
        
        # Execute engagement plan (simulation)
        print("🚀 Executing engagement plan...")
        execution_results = await targeting.execute_engagement_plan(opportunities[:10])
        print(f"✅ Executed {execution_results['executed_count']} engagements")
        print(f"📊 Expected responses: {execution_results['expected_responses']:.1f}")
        print(f"💰 Expected conversions: {execution_results['expected_conversions']:.2f}")
        
        # Show community analytics
        print("\n📈 Community Analytics:")
        analytics = targeting.get_community_analytics()
        print(f"Total Community Members: {sum(item['count'] for item in analytics['community_composition'])}")
        print("Relationship Distribution:")
        for item in analytics['relationship_distribution']:
            print(f"  {item['status']}: {item['count']}")
        
        print("\nHigh-Value Targets:")
        for target in analytics['high_value_targets'][:5]:
            print(f"  @{target['username']} - Value: {target['value_score']:.1f} | Status: {target['status']}")
    
    asyncio.run(main())