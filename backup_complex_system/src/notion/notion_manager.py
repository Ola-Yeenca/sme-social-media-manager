"""
Notion Database Manager for SME Social Media Manager
Handles all interactions with the Social Media Posts Notion database
"""

import os
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from notion_client import Client
from notion_client.errors import APIResponseError

from config.settings import settings


@dataclass
class NotionPost:
    """Data structure for Notion social media posts"""
    id: Optional[str] = None
    name: str = ""
    content: str = ""
    status: str = "Draft"  # Draft, Scheduled, Published, Archived
    platform: str = "Twitter"  # Twitter, LinkedIn, Facebook, Instagram
    scheduled_time: Optional[datetime] = None
    published_time: Optional[datetime] = None
    post_type: str = "Informational"  # Promotional, Informational, Engagement, Announcement
    business_id: Optional[str] = None
    engagement_status: str = "Pending"
    tags: List[str] = None
    tweet_id: Optional[str] = None
    engagement_metrics: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.engagement_metrics is None:
            self.engagement_metrics = {}


class NotionManager:
    """Manages all Notion database operations for social media posts"""
    
    def __init__(self):
        self.client = Client(auth=settings.notion_api_key)
        self.social_media_db_id = self._format_notion_id(settings.social_media_db_id)
        self.local_businesses_db_id = self._format_notion_id(settings.local_businesses_db_id) if settings.local_businesses_db_id else None
        self.logger = logging.getLogger(__name__)

        # Test connection on initialization
        self._test_connection()

    def _format_notion_id(self, notion_id: str) -> str:
        """Format Notion ID with proper hyphens for API calls"""
        if not notion_id:
            return notion_id

        # Remove any existing hyphens
        clean_id = notion_id.replace('-', '')

        # Add hyphens in the correct positions for Notion UUID format
        if len(clean_id) == 32:
            formatted_id = f"{clean_id[:8]}-{clean_id[8:12]}-{clean_id[12:16]}-{clean_id[16:20]}-{clean_id[20:]}"
            return formatted_id

        # Return as-is if not the expected length
        return notion_id
    
    def _test_connection(self):
        """Test the Notion API connection"""
        try:
            db_info = self.client.databases.retrieve(database_id=self.social_media_db_id)
            db_title = db_info.get('title', [{}])[0].get('plain_text', 'Unknown')
            self.logger.info(f"Connected to Notion database: {db_title}")
        except Exception as e:
            self.logger.error(f"Failed to connect to Notion database: {e}")
            # Don't raise the exception, just log it for now
            # raise
    
    def create_post(self, post) -> Optional[str]:  # Accept both NotionPost and SocialMediaPost
        """Create a new post in the Notion database"""
        try:
            # Convert SocialMediaPost to NotionPost if needed
            if hasattr(post, 'status') and hasattr(post, 'platform'):
                # This is a SocialMediaPost, convert it
                notion_post = self._convert_to_notion_post(post)
            else:
                notion_post = post

            properties = self._build_post_properties(notion_post)
            
            response = self.client.pages.create(
                parent={"database_id": self.social_media_db_id},
                properties=properties
            )
            
            post_id = response.get('id')
            self.logger.info(f"Created new post in Notion: {post_id}")
            return post_id
            
        except APIResponseError as e:
            self.logger.error(f"Notion API error creating post: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error creating post in Notion: {e}")
            return None
    
    def update_post(self, post_id: str, post) -> bool:  # Accept both NotionPost and SocialMediaPost
        """Update an existing post in the Notion database"""
        try:
            # Convert SocialMediaPost to NotionPost if needed
            if hasattr(post, 'status') and hasattr(post, 'platform'):
                notion_post = self._convert_to_notion_post(post)
            else:
                notion_post = post

            properties = self._build_post_properties(notion_post)
            
            self.client.pages.update(
                page_id=post_id,
                properties=properties
            )
            
            self.logger.info(f"Updated post in Notion: {post_id}")
            return True
            
        except APIResponseError as e:
            self.logger.error(f"Notion API error updating post: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error updating post in Notion: {e}")
            return False
    
    def get_post(self, post_id: str) -> Optional[NotionPost]:
        """Retrieve a specific post from Notion"""
        try:
            response = self.client.pages.retrieve(page_id=post_id)
            return self._parse_notion_post(response)
            
        except APIResponseError as e:
            self.logger.error(f"Notion API error retrieving post: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error retrieving post from Notion: {e}")
            return None
    
    def get_scheduled_posts(self, limit: int = 100) -> List[NotionPost]:
        """Get all scheduled posts that are ready to be published"""
        try:
            now = datetime.now(timezone.utc)
            
            response = self.client.databases.query(
                database_id=self.social_media_db_id,
                filter={
                    "and": [
                        {
                            "property": "Status",
                            "select": {
                                "equals": "Scheduled"
                            }
                        },
                        {
                            "property": "Scheduled Time",
                            "date": {
                                "on_or_before": now.isoformat()
                            }
                        }
                    ]
                },
                sorts=[
                    {
                        "property": "Scheduled Time",
                        "direction": "ascending"
                    }
                ],
                page_size=limit
            )
            
            posts = []
            for page in response.get('results', []):
                post = self._parse_notion_post(page)
                if post:
                    posts.append(post)
            
            self.logger.info(f"Retrieved {len(posts)} scheduled posts from Notion")
            return posts
            
        except Exception as e:
            self.logger.error(f"Error retrieving scheduled posts: {e}")
            return []
    
    def get_posts_by_status(self, status: str, limit: int = 100) -> List[NotionPost]:
        """Get posts by their status"""
        try:
            response = self.client.databases.query(
                database_id=self.social_media_db_id,
                filter={
                    "property": "Status",
                    "select": {
                        "equals": status
                    }
                },
                sorts=[
                    {
                        "property": "Scheduled Time",
                        "direction": "descending"
                    }
                ],
                page_size=limit
            )
            
            posts = []
            for page in response.get('results', []):
                post = self._parse_notion_post(page)
                if post:
                    posts.append(post)
            
            return posts
            
        except Exception as e:
            self.logger.error(f"Error retrieving posts by status {status}: {e}")
            return []
    
    def mark_as_published(self, post_id: str, tweet_id: str, published_time: datetime = None) -> bool:
        """Mark a post as published with tweet ID and timestamp"""
        if published_time is None:
            published_time = datetime.now(timezone.utc)
        
        try:
            properties = {
                "Status": {
                    "select": {
                        "name": "Published"
                    }
                },
                "Published Time": {
                    "date": {
                        "start": published_time.isoformat()
                    }
                }
            }

            # Add tweet ID to the Tweet ID field
            if tweet_id:
                properties["Tweet ID"] = {
                    "rich_text": [
                        {
                            "text": {
                                "content": tweet_id
                            }
                        }
                    ]
                }

                # Also update engagement metrics
                properties["Engagement Metrics"] = {
                    "rich_text": [
                        {
                            "text": {
                                "content": f"Published - Tweet ID: {tweet_id}"
                            }
                        }
                    ]
                }
            
            self.client.pages.update(
                page_id=post_id,
                properties=properties
            )
            
            self.logger.info(f"Marked post {post_id} as published with tweet ID {tweet_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error marking post as published: {e}")
            return False

    def save_engagement_analytics(self, engagement_data: Dict[str, Any]) -> bool:
        """Save engagement analytics data to Notion database"""

        try:
            # Create a new page in the social media database for engagement analytics
            properties = {
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": f"Engagement Analytics - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                            }
                        }
                    ]
                },
                "Content": {
                    "rich_text": [
                        {
                            "text": {
                                "content": f"Engagement Summary:\n"
                                          f"• Actions Taken: {engagement_data.get('actions_taken', 0)}\n"
                                          f"• Opportunities Found: {engagement_data.get('opportunities_found', 0)}\n"
                                          f"• Platforms: {', '.join(engagement_data.get('platforms_engaged', []))}\n"
                                          f"• Breakdown: {engagement_data.get('engagement_breakdown', {})}"
                            }
                        }
                    ]
                },
                "Status": {
                    "select": {
                        "name": "Published"
                    }
                },
                "Platform": {
                    "select": {
                        "name": "Analytics"
                    }
                },
                "Post Type": {
                    "select": {
                        "name": "Engagement"
                    }
                },
                "Published Time": {
                    "date": {
                        "start": datetime.now().isoformat()
                    }
                },
                "Engagement Metrics": {
                    "rich_text": [
                        {
                            "text": {
                                "content": f"Engagement Analytics: {engagement_data.get('actions_taken', 0)} actions, "
                                          f"{engagement_data.get('opportunities_found', 0)} opportunities"
                            }
                        }
                    ]
                }
            }

            response = self.client.pages.create(
                parent={"database_id": self.social_media_db_id},
                properties=properties
            )

            analytics_id = response.get('id')
            self.logger.info(f"Saved engagement analytics to Notion: {analytics_id}")
            return True

        except Exception as e:
            self.logger.error(f"Error saving engagement analytics to Notion: {e}")
            return False

    def get_engagement_analytics(self, days: int = 7) -> Dict[str, Any]:
        """Get engagement analytics from the last N days"""

        try:
            # Calculate date range
            from datetime import timedelta
            start_date = datetime.now() - timedelta(days=days)

            response = self.client.databases.query(
                database_id=self.social_media_db_id,
                filter={
                    "and": [
                        {
                            "property": "Post Type",
                            "select": {
                                "equals": "Engagement"
                            }
                        },
                        {
                            "property": "Published Time",
                            "date": {
                                "after": start_date.isoformat()
                            }
                        }
                    ]
                },
                sorts=[
                    {
                        "property": "Published Time",
                        "direction": "descending"
                    }
                ]
            )

            analytics_summary = {
                "total_engagement_sessions": len(response.get('results', [])),
                "date_range": f"{start_date.strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}",
                "sessions": []
            }

            for page in response.get('results', []):
                # Extract engagement data from the page
                content = self._extract_text_from_rich_text(page.get('properties', {}).get('Content', {}).get('rich_text', []))
                published_time = page.get('properties', {}).get('Published Time', {}).get('date', {}).get('start')

                analytics_summary["sessions"].append({
                    "id": page.get('id'),
                    "content": content,
                    "published_time": published_time
                })

            return analytics_summary

        except Exception as e:
            self.logger.error(f"Error retrieving engagement analytics: {e}")
            return {"error": str(e)}
    
    def _build_post_properties(self, post: NotionPost) -> Dict[str, Any]:
        """Build Notion properties from NotionPost object for Local Businesses database"""

        # Use the title field that exists in Local Businesses database
        # This will be the business name or post title
        properties = {
            "title": {  # This is the main title field in Local Businesses
                "title": [
                    {
                        "text": {
                            "content": post.name[:100]  # Notion title limit
                        }
                    }
                ]
            },
            "Content": {
                "rich_text": [
                    {
                        "text": {
                            "content": post.content
                        }
                    }
                ]
            },
            "Status": {
                "select": {
                    "name": post.status
                }
            },
            "Platform": {
                "select": {
                    "name": post.platform
                }
            },
            "Post Type": {
                "select": {
                    "name": post.post_type
                }
            }
        }
        
        # Add scheduled time if provided
        if post.scheduled_time:
            properties["Scheduled Time"] = {
                "date": {
                    "start": post.scheduled_time.isoformat()
                }
            }

        # Add published time if provided
        if post.published_time:
            properties["Published Time"] = {
                "date": {
                    "start": post.published_time.isoformat()
                }
            }

        # Add tags if provided
        if post.tags:
            properties["Tags"] = {
                "multi_select": [
                    {"name": tag} for tag in post.tags[:10]  # Limit to 10 tags
                ]
            }

        # Add tweet ID if provided
        if post.tweet_id:
            properties["Tweet ID"] = {
                "rich_text": [
                    {
                        "text": {
                            "content": post.tweet_id
                        }
                    }
                ]
            }

        # Add engagement status/metrics
        if post.engagement_status:
            properties["Engagement Metrics"] = {
                "rich_text": [
                    {
                        "text": {
                            "content": post.engagement_status
                        }
                    }
                ]
            }
        
        return properties
    
    def _parse_notion_post(self, page: Dict[str, Any]) -> Optional[NotionPost]:
        """Parse a Notion page into a NotionPost object from Local Businesses database"""
        try:
            properties = page.get('properties', {})

            # Extract basic properties - using new database structure
            name = self._extract_title(properties.get('title', {}))  # title field
            content = self._extract_rich_text(properties.get('Content', {}))
            status = self._extract_select(properties.get('Status', {})) or "Draft"
            platform = self._extract_select(properties.get('Platform', {})) or "Twitter"
            post_type = self._extract_select(properties.get('Post Type', {})) or "Informational"
            engagement_status = self._extract_rich_text(properties.get('Engagement Metrics', {}))

            # Extract dates
            scheduled_time = self._extract_date(properties.get('Scheduled Time', {}))
            published_time = self._extract_date(properties.get('Published Time', {}))

            # Extract tags
            tags = self._extract_multi_select(properties.get('Tags', {}))

            # Extract tweet ID
            tweet_id = self._extract_rich_text(properties.get('Tweet ID', {}))

            # This page IS the business, so business_id is the page ID itself
            business_id = page.get('id')
            
            return NotionPost(
                id=page.get('id'),
                name=name,
                content=content,
                status=status,
                platform=platform,
                scheduled_time=scheduled_time,
                published_time=published_time,
                post_type=post_type,
                business_id=business_id,
                engagement_status=engagement_status,
                tags=tags,
                tweet_id=tweet_id
            )
            
        except Exception as e:
            self.logger.error(f"Error parsing Notion post: {e}")
            return None
    
    def _extract_title(self, title_property: Dict) -> str:
        """Extract title from Notion title property"""
        title_list = title_property.get('title', [])
        return title_list[0].get('text', {}).get('content', '') if title_list else ''
    
    def _extract_rich_text(self, rich_text_property: Dict) -> str:
        """Extract text from Notion rich_text property"""
        rich_text_list = rich_text_property.get('rich_text', [])
        return ''.join([item.get('text', {}).get('content', '') for item in rich_text_list])
    
    def _extract_select(self, select_property: Dict) -> str:
        """Extract value from Notion select property"""
        select_obj = select_property.get('select')
        return select_obj.get('name', '') if select_obj else ''
    
    def _extract_multi_select(self, multi_select_property: Dict) -> List[str]:
        """Extract values from Notion multi_select property"""
        multi_select_list = multi_select_property.get('multi_select', [])
        return [item.get('name', '') for item in multi_select_list]
    
    def _extract_date(self, date_property: Dict) -> Optional[datetime]:
        """Extract datetime from Notion date property"""
        date_obj = date_property.get('date')
        if date_obj and date_obj.get('start'):
            try:
                return datetime.fromisoformat(date_obj['start'].replace('Z', '+00:00'))
            except ValueError:
                return None
        return None

    def _convert_to_notion_post(self, social_post):
        """Convert SocialMediaPost to NotionPost"""
        return NotionPost(
            name=social_post.name,
            content=social_post.content,
            status=social_post.status.value if hasattr(social_post.status, 'value') else str(social_post.status),
            platform=social_post.platform.value if hasattr(social_post.platform, 'value') else str(social_post.platform),
            post_type=social_post.post_type.value if hasattr(social_post.post_type, 'value') else str(social_post.post_type),
            scheduled_time=social_post.scheduled_time,
            published_time=social_post.published_time,
            tags=social_post.tags,
            tweet_id=getattr(social_post, 'tweet_id', None),
            engagement_status=getattr(social_post, 'engagement_status', 'Pending')
        )
