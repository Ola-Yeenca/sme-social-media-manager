"""
Configuration management for SME Analytica Social Media Manager
"""

import os
from typing import Dict, List, Optional
from enum import Enum

try:
    from pydantic_settings import BaseSettings
    from pydantic import Field
except ImportError:
    try:
        # Try pydantic v2 location
        from pydantic.v1 import BaseSettings, Field
    except ImportError:
        # Fallback for older pydantic versions
        from pydantic import BaseSettings, Field

class Language(str, Enum):
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"

class ContentTheme(str, Enum):
    DATA_MONDAY = "data_monday"
    TALK_TUESDAY = "talk_tuesday"
    CASE_WEDNESDAY = "case_wednesday"
    TECH_THURSDAY = "tech_thursday"
    FACT_FRIDAY = "fact_friday"
    WEEKEND_INSIGHTS = "weekend_insights"

class AIProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    PERPLEXITY = "perplexity"
    GROK = "grok"
    GEMINI = "gemini"

class Settings:
    """Application settings with fallback defaults"""
    
    def __init__(self):
        # Twitter/X API
        self.twitter_api_key = os.getenv("TWITTER_API_KEY", "your_twitter_api_key_here")
        self.twitter_api_secret = os.getenv("TWITTER_API_SECRET", "your_twitter_api_secret_here")
        self.twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN", "your_twitter_access_token_here")
        self.twitter_access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "your_twitter_access_token_secret_here")
        self.twitter_bearer_token = os.getenv("TWITTER_BEARER_TOKEN", "your_twitter_bearer_token_here")

        # LinkedIn API (optional)
        self.linkedin_access_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        self.linkedin_organization_id = os.getenv("LINKEDIN_ORGANIZATION_ID")
        
        # AI Provider Keys
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "your_openai_api_key_here")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "your_anthropic_api_key_here")
        self.perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")
        self.grok_api_key = os.getenv("GROK_API_KEY")
        self.google_gemini_api_key = os.getenv("GOOGLE_GEMINI_API_KEY", "AIzaSyChtpXZLiYpDFnY7fyMqWZ7S_Rp396QL60")
        
        # Content Configuration
        self.posting_schedule = int(os.getenv("POSTING_SCHEDULE", "3"))
        self.engagement_frequency = os.getenv("ENGAGEMENT_FREQUENCY", "hourly")
        self.primary_language = Language.ENGLISH
        self.secondary_language = Language.SPANISH
        self.timezone = os.getenv("TIMEZONE", "UTC")
        
        # Notion Configuration (support both naming conventions)
        self.notion_api_key = os.getenv("NOTION_API_KEY") or os.getenv("NOTION_TOKEN", "your_notion_api_key_here")
        self.social_media_db_id = os.getenv("SOCIAL_MEDIA_DB_ID") or os.getenv("NOTION_DATABASE_ID", "20f7ad8571fa80ea9fe3fa6ba3f484c7")
        self.local_businesses_db_id = os.getenv("LOCAL_BUSINESSES_DB_ID", "1cd7ad8571fa8040ba03e63fcd20872a")

        # Database (keeping for backward compatibility)
        self.db_path = os.getenv("DB_PATH", "data/social_manager.db")
        self.community_db_path = os.getenv("COMMUNITY_DB_PATH", "data/community_database.db")

        # Community Engagement Settings
        self.community_daily_engagement_target = int(os.getenv("COMMUNITY_DAILY_ENGAGEMENT_TARGET", "50"))
        self.community_max_daily_follows = int(os.getenv("COMMUNITY_MAX_DAILY_FOLLOWS", "20"))
        self.community_max_daily_replies = int(os.getenv("COMMUNITY_MAX_DAILY_REPLIES", "30"))
        self.community_response_time_hours = int(os.getenv("COMMUNITY_RESPONSE_TIME_HOURS", "2"))
        self.community_automation_enabled = os.getenv("COMMUNITY_AUTOMATION_ENABLED", "True").lower() == "true"

        # Logging
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_file = os.getenv("LOG_FILE", "logs/social_manager.log")
        
        # SME Analytica URLs
        self.company_website = os.getenv("COMPANY_WEBSITE", "https://smeanalytica.dev")
        self.menuflow_url = os.getenv("MENUFLOW_URL", "https://restaurants.smeanalytica.dev")
        self.api_docs_url = os.getenv("API_DOCS_URL", "https://api.smeanalytica.dev/docs")

class SMEAnalyticaContext:
    """SME Analytica business context and messaging"""

    COMPANY_NAME = "SME Analytica"
    TAGLINE = "AI-driven analytics for small and medium enterprises"

    # Comprehensive Business Overview
    COMPANY_DESCRIPTION = """SME Analytica is an AI-driven analytics and business intelligence platform built for small and medium enterprises.
    Its tools help business owners "understand your data, improve your pricing, and grow your business" without complex tech setup.
    In practice, SME Analytica turns raw sales, traffic and customer data into actionable insights and automation
    (e.g. dynamic pricing and performance dashboards) tailored for small businesses."""

    VALUE_PROPOSITIONS = [
        "AI-powered dynamic pricing that boosts margins by ~10%",
        "Real-time analytics without complex tech setup",
        "Vertical-specific modules (MenuFlow for restaurants)",
        "Seamless integration with existing POS and booking systems",
        "User-friendly interface for non-technical business owners",
        "Enterprise-level analytics made accessible to non-technical owners",
        "Predictive insights for pricing and inventory optimization",
        "Real-time traffic and operations analytics",
        "Competitive benchmarking and customer sentiment analysis"
    ]

    # Key Differentiators
    DIFFERENTIATORS = [
        "Vertical Specialization: Dedicated modules for specific sectors with industry-specific features",
        "AI-Powered Dynamic Pricing: Automatically adjusts prices in real time based on demand",
        "Seamless Integration: Connects via APIs to existing POS, reservation, accounting tools",
        "Real-Time Analytics: Live customer traffic and operations insights",
        "User-Friendly Interface: Designed for non-technical users with actionable dashboards"
    ]

    # Core Modules
    CORE_MODULES = {
        "MenuFlow": {
            "description": "Smart restaurant module combining QR menu/order system with analytics and dynamic pricing",
            "features": ["Real-time menu updates", "QR-code ordering", "Personalized recommendations",
                        "Loyalty discounts", "Peak-time price optimization"],
            "results": "10% higher margins during peak hours, faster table turns, higher average checks"
        },
        "Hotel Analytics": {
            "description": "Hospitality module for occupancy analytics, ADR, RevPAR and guest sentiment",
            "features": ["Booking data integration", "Predictive forecasts", "Rate optimization", "Staffing insights"],
            "status": "Coming soon"
        },
        "Retail Insights": {
            "description": "For retail shops analyzing sales per hour, inventory turnover, customer visit patterns",
            "features": ["Promotion timing", "Stock reorder suggestions", "Footfall analysis"],
            "status": "In development"
        }
    }
    
    KEY_FEATURES = {
        "menuflow": {
            "name": "MenuFlow",
            "description": "Smart restaurant module with QR ordering and dynamic pricing",
            "benefits": ["10% higher margins during peak hours", "Faster table turns", "Real-time menu updates"]
        },
        "hotel_analytics": {
            "name": "Hotel Analytics",
            "description": "Occupancy optimization and revenue management for small hotels",
            "benefits": ["RevPAR optimization", "Predictive forecasting", "Guest sentiment analysis"]
        },
        "retail_insights": {
            "name": "Retail Insights",
            "description": "Sales analytics and inventory optimization for retail stores",
            "benefits": ["Inventory turnover analysis", "Promotion timing", "Customer visit patterns"]
        }
    }
    
    # Proven Results & Use Cases
    PROVEN_RESULTS = [
        "10% higher margins during peak hours with AI-driven dynamic pricing",
        "Faster table turns and higher average checks",
        "More guests served per hour with minimal wait time",
        "Real-time insights for immediate action",
        "No data science knowledge required"
    ]

    USE_CASES = [
        "Revenue uplift via dynamic pricing during peak traffic",
        "Inventory & demand forecasting to avoid stockouts",
        "Customer satisfaction tracking through review analysis",
        "Competitive benchmarking against local competitors",
        "Operational optimization for staffing and resource allocation"
    ]

    # Social Media Strategy
    CONTENT_THEMES = {
        "Data Monday": "Educational data tips and insights that matter to small businesses",
        "Talk Tuesday": "Industry discussions, polls, and engagement with community",
        "Case Study Wednesday": "Real success stories and client examples",
        "Tech Thursday": "Technology features, integrations, and innovations",
        "Fact Friday": "Industry statistics, trends, and educational content",
        "Weekend Insights": "Lighter content, tips, and community engagement"
    }

    BRAND_VOICE = {
        "tone": "Conversational yet expert - like a knowledgeable consultant chatting with a small business owner",
        "style": "Enthusiastic about data but speaking plainly, optimistic, helpful, playful with everyday analogies",
        "approach": "Educational and engaging, making SME owners feel smarter after reading",
        "languages": "Bilingual - English (70%) and Spanish (30%) for global reach, occasional French"
    }

    HASHTAGS = {
        "primary": ["#SMEAnalytica", "#AIforSMEs", "#DataInsights", "#SmallBusiness"],
        "restaurant": ["#RestaurantTech", "#MenuFlow", "#HospitalityAI", "#DynamicPricing"],
        "retail": ["#RetailAnalytics", "#InventoryManagement", "#RetailTech"],
        "general": ["#BusinessIntelligence", "#Analytics", "#AI", "#SmartBusiness"],
        "spanish": ["#PequeñasEmpresas", "#AnalíticaIA", "#RestauranteTech", "#DatosInteligentes"],
        "french": ["#PME", "#AnalyticsIA", "#TechRestaurant", "#DonnéesIntelligentes"]
    }

    TARGET_AUDIENCE = [
        "Restaurant owners and managers",
        "Hotel managers and hospitality professionals",
        "Retail store owners",
        "Small business entrepreneurs",
        "Technology adopters in SME sector",
        "Non-technical business owners seeking data insights",
        "Spanish-speaking SME community",
        "European small business market"
    ]

    # Community Engagement Strategy
    COMMUNITY_PRIORITIES = {
        "restaurant_owners": {
            "weight": 40,
            "conversion_potential": 9.0,
            "engagement_approach": "solution_focused",
            "key_pain_points": ["pricing optimization", "margin pressure", "operational efficiency"]
        },
        "industry_experts": {
            "weight": 25,
            "conversion_potential": 6.0,
            "engagement_approach": "thought_leadership",
            "key_pain_points": ["industry trends", "technology adoption", "best practices"]
        },
        "media_contacts": {
            "weight": 15,
            "conversion_potential": 5.0,
            "engagement_approach": "information_sharing",
            "key_pain_points": ["industry insights", "newsworthy developments", "expert commentary"]
        },
        "hotel_managers": {
            "weight": 10,
            "conversion_potential": 8.0,
            "engagement_approach": "solution_focused",
            "key_pain_points": ["revenue optimization", "occupancy management", "guest analytics"]
        },
        "potential_partners": {
            "weight": 10,
            "conversion_potential": 7.0,
            "engagement_approach": "collaboration_focused",
            "key_pain_points": ["integration opportunities", "mutual benefits", "market expansion"]
        }
    }

    # Conversion Tracking
    CONVERSION_FUNNEL = {
        "awareness": "Social media impression and engagement",
        "interest": "Profile visit and follow",
        "consideration": "Direct message or reply engagement",
        "intent": "Demo request or business inquiry",
        "evaluation": "Technical discussion or case study request",
        "purchase": "Signed customer or partnership agreement"
    }

    # Community Growth Targets (4-week campaign)
    GROWTH_TARGETS = {
        "week_1": {
            "followers": 50,
            "engagements": 350,
            "demo_requests": 5,
            "business_inquiries": 3,
            "focus": "Foundation building and initial community engagement"
        },
        "week_2": {
            "followers": 150,
            "engagements": 490,
            "demo_requests": 10,
            "business_inquiries": 7,
            "focus": "Influencer outreach and relationship building"
        },
        "week_3": {
            "followers": 300,
            "engagements": 630,
            "demo_requests": 20,
            "business_inquiries": 15,
            "focus": "Viral amplification and thought leadership"
        },
        "week_4": {
            "followers": 500,
            "engagements": 700,
            "demo_requests": 30,
            "business_inquiries": 25,
            "focus": "Conversion optimization and customer acquisition"
        }
    }

# Global settings instance
settings = Settings()
sme_context = SMEAnalyticaContext()
