"""
LinkedIn Manager for SME Analytica
Handles LinkedIn API interactions for B2B social media automation
"""

import logging
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class LinkedInPost:
    """Represents a LinkedIn post"""
    id: str
    content: str
    author_id: str
    created_at: datetime
    engagement_metrics: Dict[str, int]
    post_url: str

class LinkedInManager:
    """Manages LinkedIn API interactions for SME Analytica B2B content"""
    
    def __init__(self, api_credentials: Dict[str, str]):
        self.access_token = api_credentials.get("access_token")
        self.organization_id = api_credentials.get("organization_id")  # LinkedIn Company Page ID
        
        # Initialize logger
        self.logger = logging.getLogger(__name__)
        
        # API endpoints
        self.base_url = "https://api.linkedin.com/v2"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        # Rate limiting
        self.last_post_time = None
        self.min_interval_between_posts = 3600  # 1 hour between posts (LinkedIn best practice)
        
        # Daily limits
        self.daily_post_count = 0
        self.daily_post_limit = 2  # Conservative limit for LinkedIn
        self.last_post_reset = datetime.now().date()
        
        self.logger.info("LinkedIn Manager initialized")
    
    def _can_post(self) -> bool:
        """Check if we can post based on rate limits"""
        
        # Reset daily count if new day
        today = datetime.now().date()
        if today > self.last_post_reset:
            self.daily_post_count = 0
            self.last_post_reset = today
        
        # Check daily limit
        if self.daily_post_count >= self.daily_post_limit:
            self.logger.warning(f"Daily LinkedIn post limit reached: {self.daily_post_count}")
            return False
        
        # Check time interval
        if self.last_post_time:
            time_since_last = datetime.now() - self.last_post_time
            if time_since_last.total_seconds() < self.min_interval_between_posts:
                self.logger.warning("LinkedIn post interval limit not met")
                return False
        
        return True
    
    def _validate_post_content(self, content: str) -> bool:
        """Validate LinkedIn post content"""
        
        if not content or not content.strip():
            return False
        
        # LinkedIn post character limit is 3000
        if len(content) > 3000:
            self.logger.error(f"LinkedIn post too long: {len(content)} characters")
            return False
        
        return True
    
    async def post_to_linkedin(self, content: str, image_url: Optional[str] = None) -> Optional[str]:
        """Post content to LinkedIn company page"""
        
        if not self._validate_post_content(content):
            self.logger.error(f"Invalid LinkedIn post content: {content}")
            return None
        
        if not self._can_post():
            self.logger.warning("Rate limit reached, skipping LinkedIn post")
            return None
        
        try:
            # Prepare post data
            post_data = {
                "author": f"urn:li:organization:{self.organization_id}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": content
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            # Add image if provided
            if image_url:
                post_data["specificContent"]["com.linkedin.ugc.ShareContent"]["shareMediaCategory"] = "IMAGE"
                post_data["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = [
                    {
                        "status": "READY",
                        "description": {
                            "text": "SME Analytica - Restaurant Analytics"
                        },
                        "media": image_url,
                        "title": {
                            "text": "MenuFlow Restaurant Technology"
                        }
                    }
                ]
            
            # Make API request
            response = requests.post(
                f"{self.base_url}/ugcPosts",
                headers=self.headers,
                json=post_data,
                timeout=30
            )
            
            if response.status_code == 201:
                post_id = response.headers.get('x-restli-id')
                self.last_post_time = datetime.now()
                self.daily_post_count += 1
                self.logger.info(f"LinkedIn post published successfully: {post_id}")
                return post_id
            else:
                self.logger.error(f"LinkedIn post failed: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Network error posting to LinkedIn: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error posting to LinkedIn: {e}")
            return None
    
    async def get_company_metrics(self) -> Optional[Dict[str, Any]]:
        """Get LinkedIn company page metrics"""
        
        try:
            # Get company info
            response = requests.get(
                f"{self.base_url}/organizations/{self.organization_id}",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                company_data = response.json()
                
                # Get follower statistics
                follower_response = requests.get(
                    f"{self.base_url}/organizationalEntityFollowerStatistics",
                    headers=self.headers,
                    params={
                        "q": "organizationalEntity",
                        "organizationalEntity": f"urn:li:organization:{self.organization_id}"
                    },
                    timeout=30
                )
                
                metrics = {
                    "company_name": company_data.get("localizedName", "Unknown"),
                    "follower_count": 0,
                    "connection_status": "connected"
                }
                
                if follower_response.status_code == 200:
                    follower_data = follower_response.json()
                    if follower_data.get("elements"):
                        metrics["follower_count"] = follower_data["elements"][0].get("followerGains", {}).get("organicFollowerGain", 0)
                
                return metrics
            else:
                self.logger.error(f"Failed to get LinkedIn metrics: {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting LinkedIn metrics: {e}")
            return None
    
    async def search_linkedin_content(self, keywords: List[str], max_results: int = 10) -> List[Dict[str, Any]]:
        """Search for LinkedIn content opportunities (limited by API access)"""
        
        # Note: LinkedIn's search API is very limited for organic content
        # This is a placeholder for potential future functionality
        self.logger.info(f"LinkedIn content search requested for: {keywords}")
        
        # For now, return empty list as LinkedIn search requires special permissions
        return []
    
    def format_content_for_linkedin(self, content: str, hashtags: List[str]) -> str:
        """Format content specifically for LinkedIn's professional audience"""
        
        # LinkedIn best practices:
        # - More professional tone
        # - Longer form content is acceptable
        # - Use line breaks for readability
        # - Hashtags at the end
        
        # Add professional context if not present
        if not any(word in content.lower() for word in ['business', 'restaurant', 'analytics', 'data']):
            content = f"🏢 {content}"
        
        # Format hashtags for LinkedIn (limit to 5 most relevant)
        linkedin_hashtags = hashtags[:5]
        hashtag_text = " ".join(linkedin_hashtags)
        
        # Combine content with hashtags
        if hashtag_text:
            formatted_content = f"{content}\n\n{hashtag_text}"
        else:
            formatted_content = content
        
        return formatted_content
    
    def get_optimal_posting_times(self) -> List[Dict[str, int]]:
        """Get optimal posting times for LinkedIn (B2B audience)"""
        
        # LinkedIn optimal times (business hours, weekdays)
        return [
            {"hour": 8, "minute": 0},   # 8:00 AM - Morning check
            {"hour": 12, "minute": 0},  # 12:00 PM - Lunch break
            {"hour": 17, "minute": 0},  # 5:00 PM - End of workday
        ]
    
    async def test_connection(self) -> bool:
        """Test LinkedIn API connection"""
        
        try:
            metrics = await self.get_company_metrics()
            return metrics is not None
        except Exception as e:
            self.logger.error(f"LinkedIn connection test failed: {e}")
            return False
