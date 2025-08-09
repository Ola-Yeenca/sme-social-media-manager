#!/usr/bin/env python3
"""
Simple configuration management for SME Social Media Bot
Loads environment variables and validates API keys
"""

import os
import sys
from typing import Optional


class Config:
    """Simple configuration class"""
    
    def __init__(self):
        """Load and validate configuration"""
        self.load_environment()
        self.validate_required_keys()
    
    def load_environment(self):
        """Load environment variables"""
        
        # Twitter API keys (required)
        self.twitter_api_key = os.getenv('TWITTER_API_KEY')
        self.twitter_api_secret = os.getenv('TWITTER_API_SECRET')
        self.twitter_access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.twitter_access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        self.twitter_bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        
        # AI provider keys (at least one required)
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
        self.grok_api_key = os.getenv('GROK_API_KEY')
        
        # Optional keys
        self.linkedin_access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        self.linkedin_organization_id = os.getenv('LINKEDIN_ORGANIZATION_ID')
        self.notion_api_key = os.getenv('NOTION_API_KEY')
    
    def validate_required_keys(self):
        """Validate that required API keys are present"""
        
        # Check Twitter keys
        twitter_keys = [
            self.twitter_api_key,
            self.twitter_api_secret,
            self.twitter_access_token,
            self.twitter_access_token_secret,
            self.twitter_bearer_token
        ]
        
        if not all(twitter_keys):
            print("❌ Missing Twitter API keys. Required:")
            print("  TWITTER_API_KEY")
            print("  TWITTER_API_SECRET")
            print("  TWITTER_ACCESS_TOKEN")
            print("  TWITTER_ACCESS_TOKEN_SECRET")
            print("  TWITTER_BEARER_TOKEN")
            sys.exit(1)
        
        # Check AI provider keys (at least one)
        if not self.openai_api_key and not self.anthropic_api_key and not self.grok_api_key:
            print("❌ Missing AI provider keys. Need at least one:")
            print("  OPENAI_API_KEY")
            print("  ANTHROPIC_API_KEY")
            print("  GROK_API_KEY")
            sys.exit(1)
        
        print("✅ Configuration validated")
    
    def get_status(self) -> dict:
        """Get configuration status"""
        return {
            'twitter_configured': bool(self.twitter_api_key),
            'openai_configured': bool(self.openai_api_key),
            'anthropic_configured': bool(self.anthropic_api_key),
            'grok_configured': bool(self.grok_api_key),
            'linkedin_configured': bool(self.linkedin_access_token),
            'notion_configured': bool(self.notion_api_key)
        }


def load_dotenv_manually():
    """Manually load .env file if present"""
    env_file = '.env'
    
    if os.path.exists(env_file):
        print("📝 Loading .env file...")
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    # Remove quotes if present
                    value = value.strip("\"").strip("'")
                    os.environ[key] = value
        print("✅ Environment variables loaded")
    else:
        print("ℹ️ No .env file found, using system environment variables")


# Load environment variables when imported
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    load_dotenv_manually()


if __name__ == "__main__":
    """Test configuration"""
    print("🧪 Testing configuration...")
    config = Config()
    status = config.get_status()
    
    print("\n📊 Configuration Status:")
    for service, configured in status.items():
        status_icon = "✅" if configured else "❌"
        print(f"  {service}: {status_icon}")
    
    print("\n✅ Configuration test complete!")