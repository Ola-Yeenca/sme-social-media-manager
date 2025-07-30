"""
SME Social Media Manager - Simple Configuration
Minimal configuration management for essential APIs only
"""

import os
from typing import Optional

class Config:
    """Simple configuration class for essential environment variables"""
    
    def __init__(self):
        # Essential Twitter API credentials
        self.twitter_api_key = os.getenv('TWITTER_API_KEY')
        self.twitter_api_secret = os.getenv('TWITTER_API_SECRET')
        self.twitter_access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.twitter_access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        self.twitter_bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        
        # LinkedIn credentials (optional)
        self.linkedin_access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        self.linkedin_organization_id = os.getenv('LINKEDIN_ORGANIZATION_ID')
        
        # AI Provider (choose one)
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        
        # Notion for analytics
        self.notion_api_key = os.getenv('NOTION_API_KEY')
        self.notion_database_id = os.getenv('SOCIAL_MEDIA_DB_ID')
        
        # Business context
        self.company_name = "SME Analytica"
        self.target_audience = "restaurant owners, hospitality managers, small business entrepreneurs"
        self.posting_schedule = ["08:00", "12:00", "17:00", "20:00"]  # UTC times
        
    def validate(self) -> tuple[bool, list[str]]:
        """Validate essential configuration"""
        missing = []
        
        # Check Twitter credentials
        if not all([self.twitter_api_key, self.twitter_api_secret, 
                   self.twitter_access_token, self.twitter_access_token_secret]):
            missing.append("Twitter API credentials")
            
        # Check AI provider
        if not (self.openai_api_key or self.anthropic_api_key):
            missing.append("AI provider API key (OpenAI or Anthropic)")
            
        return len(missing) == 0, missing
    
    def get_ai_provider(self) -> str:
        """Return which AI provider to use"""
        if self.openai_api_key:
            return "openai"
        elif self.anthropic_api_key:
            return "anthropic"
        return None