"""
Base AI provider interface for consistent integration
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

class ContentType(str, Enum):
    TWEET = "tweet"
    REPLY = "reply"
    THREAD = "thread"
    RETWEET_COMMENT = "retweet_comment"
    SOCIAL_MEDIA_POST = "social_media_post"
    ANALYSIS = "analysis"
    CONTENT_EVALUATION = "content_evaluation"
    ENGAGEMENT_ANALYSIS = "engagement_analysis"

@dataclass
class ContentRequest:
    """Standardized content generation request"""
    content_type: ContentType
    language: str = "en"
    theme: str = ""
    context: Dict[str, Any] = None
    max_length: int = 1000  # Flexible length for Twitter subscription and LinkedIn
    hashtags: Optional[List[str]] = None
    tone: str = "conversational_expert"
    platform: str = "twitter"

    def __post_init__(self):
        if self.context is None:
            self.context = {}

@dataclass
class GeneratedContent:
    """Standardized content response"""
    text: str
    language: str
    hashtags: List[str]
    confidence_score: float
    metadata: Dict[str, Any]

class BaseAIProvider(ABC):
    """Abstract base class for AI providers"""
    
    def __init__(self, api_key: str, model_name: str = None):
        self.api_key = api_key
        self.model_name = model_name
    
    @abstractmethod
    async def generate_content(self, request: ContentRequest) -> GeneratedContent:
        """Generate content based on request parameters"""
        pass
    
    @abstractmethod
    async def analyze_engagement_opportunity(self, tweet_text: str, author: str) -> Dict[str, Any]:
        """Analyze if a tweet presents a good engagement opportunity"""
        pass
    
    @abstractmethod
    async def generate_reply(self, original_tweet: str, context: Dict[str, Any]) -> str:
        """Generate a contextual reply to a tweet"""
        pass
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider name"""
        pass
    
    @property
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available and properly configured"""
        pass

class AIProviderError(Exception):
    """Custom exception for AI provider errors"""
    pass

class RateLimitError(AIProviderError):
    """Raised when rate limits are exceeded"""
    pass

class APIError(AIProviderError):
    """Raised when API calls fail"""
    pass
