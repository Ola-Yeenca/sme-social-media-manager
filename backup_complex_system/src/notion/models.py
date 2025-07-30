"""
Data models for Notion integration
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum


class PostStatus(str, Enum):
    """Post status options"""
    DRAFT = "Draft"
    SCHEDULED = "Scheduled"
    PUBLISHED = "Published"
    ARCHIVED = "Archived"


class Platform(str, Enum):
    """Social media platform options"""
    TWITTER = "Twitter"
    LINKEDIN = "LinkedIn"
    FACEBOOK = "Facebook"
    INSTAGRAM = "Instagram"


class PostType(str, Enum):
    """Post type options"""
    PROMOTIONAL = "Promotional"
    INFORMATIONAL = "Informational"
    ENGAGEMENT = "Engagement"
    ANNOUNCEMENT = "Announcement"


@dataclass
class BusinessInfo:
    """Business information from Local Businesses database"""
    id: str
    name: str
    category: str
    city: str
    email: Optional[str] = None
    address: Optional[str] = None
    status: Optional[str] = None


@dataclass
class EngagementMetrics:
    """Engagement metrics for a post"""
    likes: int = 0
    retweets: int = 0
    replies: int = 0
    impressions: int = 0
    clicks: int = 0
    engagement_rate: float = 0.0
    last_updated: Optional[datetime] = None


@dataclass
class SocialMediaPost:
    """Complete social media post data structure"""
    # Basic post information
    name: str
    content: str
    status: PostStatus = PostStatus.DRAFT
    platform: Platform = Platform.TWITTER
    post_type: PostType = PostType.INFORMATIONAL
    
    # Timing
    scheduled_time: Optional[datetime] = None
    published_time: Optional[datetime] = None
    created_at: Optional[datetime] = None
    
    # Relationships and metadata
    business_id: Optional[str] = None
    business_info: Optional[BusinessInfo] = None
    tags: List[str] = field(default_factory=list)
    
    # Social media specific
    tweet_id: Optional[str] = None
    engagement_metrics: Optional[EngagementMetrics] = None
    engagement_status: str = "Pending"
    
    # Internal tracking
    notion_id: Optional[str] = None
    ai_provider_used: Optional[str] = None
    content_theme: Optional[str] = None
    language: str = "en"
    
    def __post_init__(self):
        """Post-initialization processing"""
        if self.created_at is None:
            self.created_at = datetime.now()
        
        if self.engagement_metrics is None:
            self.engagement_metrics = EngagementMetrics()
    
    @property
    def is_scheduled(self) -> bool:
        """Check if post is scheduled for future publishing"""
        return (
            self.status == PostStatus.SCHEDULED and 
            self.scheduled_time is not None and 
            self.scheduled_time > datetime.now()
        )
    
    @property
    def is_ready_to_publish(self) -> bool:
        """Check if post is ready to be published"""
        return (
            self.status == PostStatus.SCHEDULED and 
            self.scheduled_time is not None and 
            self.scheduled_time <= datetime.now()
        )
    
    @property
    def is_published(self) -> bool:
        """Check if post has been published"""
        return self.status == PostStatus.PUBLISHED
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API calls"""
        return {
            'name': self.name,
            'content': self.content,
            'status': self.status.value,
            'platform': self.platform.value,
            'post_type': self.post_type.value,
            'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else None,
            'published_time': self.published_time.isoformat() if self.published_time else None,
            'business_id': self.business_id,
            'tags': self.tags,
            'tweet_id': self.tweet_id,
            'engagement_status': self.engagement_status,
            'notion_id': self.notion_id,
            'ai_provider_used': self.ai_provider_used,
            'content_theme': self.content_theme,
            'language': self.language
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SocialMediaPost':
        """Create instance from dictionary"""
        # Parse datetime fields
        scheduled_time = None
        if data.get('scheduled_time'):
            scheduled_time = datetime.fromisoformat(data['scheduled_time'])
        
        published_time = None
        if data.get('published_time'):
            published_time = datetime.fromisoformat(data['published_time'])
        
        created_at = None
        if data.get('created_at'):
            created_at = datetime.fromisoformat(data['created_at'])
        
        return cls(
            name=data.get('name', ''),
            content=data.get('content', ''),
            status=PostStatus(data.get('status', PostStatus.DRAFT.value)),
            platform=Platform(data.get('platform', Platform.TWITTER.value)),
            post_type=PostType(data.get('post_type', PostType.INFORMATIONAL.value)),
            scheduled_time=scheduled_time,
            published_time=published_time,
            created_at=created_at,
            business_id=data.get('business_id'),
            tags=data.get('tags', []),
            tweet_id=data.get('tweet_id'),
            engagement_status=data.get('engagement_status', 'Pending'),
            notion_id=data.get('notion_id'),
            ai_provider_used=data.get('ai_provider_used'),
            content_theme=data.get('content_theme'),
            language=data.get('language', 'en')
        )


@dataclass
class ContentRequest:
    """Request for content generation"""
    theme: str
    language: str = "en"
    platform: Platform = Platform.TWITTER
    post_type: PostType = PostType.INFORMATIONAL
    business_context: Optional[BusinessInfo] = None
    target_audience: Optional[List[str]] = None
    hashtags: Optional[List[str]] = None
    max_length: int = 280
    include_call_to_action: bool = True


@dataclass
class AnalyticsData:
    """Analytics data structure"""
    date: datetime
    posts_created: int = 0
    posts_published: int = 0
    total_engagement: int = 0
    total_impressions: int = 0
    follower_growth: int = 0
    top_performing_post_id: Optional[str] = None
    engagement_rate: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'date': self.date.isoformat(),
            'posts_created': self.posts_created,
            'posts_published': self.posts_published,
            'total_engagement': self.total_engagement,
            'total_impressions': self.total_impressions,
            'follower_growth': self.follower_growth,
            'top_performing_post_id': self.top_performing_post_id,
            'engagement_rate': self.engagement_rate
        }


@dataclass
class SchedulingRule:
    """Rules for post scheduling"""
    hour: int
    minute: int = 0
    days_of_week: Optional[List[int]] = None  # 0=Monday, 6=Sunday
    timezone: str = "UTC"
    
    def __post_init__(self):
        if self.days_of_week is None:
            self.days_of_week = list(range(7))  # All days by default


# Common hashtag sets for different content types
HASHTAG_SETS = {
    'sme_analytica': ['#SMEAnalytica', '#AIforSMEs', '#DataInsights', '#SmallBusiness'],
    'restaurant': ['#RestaurantTech', '#MenuFlow', '#HospitalityAI', '#DynamicPricing'],
    'retail': ['#RetailAnalytics', '#InventoryManagement', '#RetailTech'],
    'hotel': ['#HotelTech', '#HospitalityAI', '#RevenueManagement'],
    'general_business': ['#BusinessIntelligence', '#Analytics', '#AI', '#SmartBusiness'],
    'data_monday': ['#DataMonday', '#Analytics', '#BusinessData', '#SMEAnalytica'],
    'tech_thursday': ['#TechThursday', '#Innovation', '#AITech', '#BusinessTech'],
    'fact_friday': ['#FactFriday', '#BusinessFacts', '#IndustryInsights']
}

# Content themes for different days
CONTENT_THEMES = {
    'monday': 'data_monday',
    'tuesday': 'talk_tuesday', 
    'wednesday': 'case_wednesday',
    'thursday': 'tech_thursday',
    'friday': 'fact_friday',
    'saturday': 'weekend_insights',
    'sunday': 'weekend_insights'
}

# Optimal posting times (in UTC)
OPTIMAL_POSTING_TIMES = [
    {'hour': 9, 'minute': 0},   # Morning business start
    {'hour': 13, 'minute': 0},  # Lunch break
    {'hour': 17, 'minute': 30}  # End of business day
]
