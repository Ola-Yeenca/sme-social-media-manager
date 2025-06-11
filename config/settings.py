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

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Twitter/X API
    twitter_api_key: str = Field(..., env="TWITTER_API_KEY")
    twitter_api_secret: str = Field(..., env="TWITTER_API_SECRET")
    twitter_access_token: str = Field(..., env="TWITTER_ACCESS_TOKEN")
    twitter_access_token_secret: str = Field(..., env="TWITTER_ACCESS_TOKEN_SECRET")
    twitter_bearer_token: str = Field(..., env="TWITTER_BEARER_TOKEN")
    
    # AI Provider Keys
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    anthropic_api_key: str = Field(..., env="ANTHROPIC_API_KEY")
    perplexity_api_key: Optional[str] = Field(None, env="PERPLEXITY_API_KEY")
    grok_api_key: Optional[str] = Field(None, env="GROK_API_KEY")
    
    # Content Configuration
    posting_schedule: int = Field(3, env="POSTING_SCHEDULE")
    engagement_frequency: str = Field("hourly", env="ENGAGEMENT_FREQUENCY")
    primary_language: Language = Field(Language.ENGLISH, env="PRIMARY_LANGUAGE")
    secondary_language: Language = Field(Language.SPANISH, env="SECONDARY_LANGUAGE")
    timezone: str = Field("UTC", env="TIMEZONE")
    
    # Notion Configuration
    notion_api_key: str = Field(..., env="NOTION_API_KEY")
    social_media_db_id: str = Field("20f7ad8571fa80ea9fe3fa6ba3f484c7", env="SOCIAL_MEDIA_DB_ID")
    local_businesses_db_id: Optional[str] = Field("1cd7ad8571fa8040ba03e63fcd20872a", env="LOCAL_BUSINESSES_DB_ID")

    # Database (keeping for backward compatibility)
    db_path: str = Field("data/social_manager.db", env="DB_PATH")

    # Logging
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_file: str = Field("logs/social_manager.log", env="LOG_FILE")
    
    # SME Analytica URLs
    company_website: str = Field("https://smeanalytica.dev", env="COMPANY_WEBSITE")
    menuflow_url: str = Field("https://restaurants.smeanalytica.dev", env="MENUFLOW_URL")
    api_docs_url: str = Field("https://api.smeanalytica.dev/docs", env="API_DOCS_URL")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

class SMEAnalyticaContext:
    """SME Analytica business context and messaging"""
    
    COMPANY_NAME = "SME Analytica"
    TAGLINE = "AI-driven analytics for small and medium enterprises"
    
    VALUE_PROPOSITIONS = [
        "AI-powered dynamic pricing that boosts margins by ~10%",
        "Real-time analytics without complex tech setup",
        "Vertical-specific modules (MenuFlow for restaurants)",
        "Seamless integration with existing POS and booking systems",
        "User-friendly interface for non-technical business owners"
    ]
    
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
    
    HASHTAGS = {
        "primary": ["#SMEAnalytica", "#AIforSMEs", "#DataInsights", "#SmallBusiness"],
        "restaurant": ["#RestaurantTech", "#MenuFlow", "#HospitalityAI", "#DynamicPricing"],
        "retail": ["#RetailAnalytics", "#InventoryManagement", "#RetailTech"],
        "general": ["#BusinessIntelligence", "#Analytics", "#AI", "#SmartBusiness"]
    }
    
    TARGET_AUDIENCE = [
        "Restaurant owners and managers",
        "Hotel managers and hospitality professionals",
        "Retail store owners",
        "Small business entrepreneurs",
        "Technology adopters in SME sector"
    ]

# Global settings instance
settings = Settings()
sme_context = SMEAnalyticaContext()
