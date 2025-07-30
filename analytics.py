"""
SME Social Media Manager - Simple Analytics
Basic analytics tracking using Notion database
"""

import requests
from datetime import datetime, timezone
from typing import Dict, List, Optional
from config import Config

class Analytics:
    """Simple analytics tracking system"""
    
    def __init__(self, config: Config):
        self.config = config
        self.notion_headers = None
        
        if config.notion_api_key:
            self.notion_headers = {
                'Authorization': f'Bearer {config.notion_api_key}',
                'Content-Type': 'application/json',
                'Notion-Version': '2022-06-28'
            }
            print("✅ Analytics (Notion) initialized")
        else:
            print("⚠️ Analytics disabled - no Notion API key")
    
    def log_post(self, post_data: Dict) -> bool:
        """Log a social media post to analytics"""
        if not self.notion_headers or not self.config.notion_database_id:
            print("Analytics not configured - logging to console only")
            print(f"📊 POST: {post_data.get('platform')} - {post_data.get('content', '')[:50]}...")
            return False
        
        try:
            # Prepare Notion page data
            page_data = {
                "parent": {"database_id": self.config.notion_database_id},
                "properties": {
                    "Title": {
                        "title": [{"text": {"content": f"{post_data.get('platform', 'unknown').title()} Post"}}]
                    },
                    "Platform": {
                        "select": {"name": post_data.get('platform', 'unknown').title()}
                    },
                    "Content": {
                        "rich_text": [{"text": {"content": post_data.get('content', '')[:2000]}}]
                    },
                    "Post ID": {
                        "rich_text": [{"text": {"content": str(post_data.get('post_id', ''))}}]
                    },
                    "Date": {
                        "date": {"start": datetime.now(timezone.utc).isoformat()}
                    },
                    "Status": {
                        "select": {"name": "Published" if post_data.get('success') else "Failed"}
                    }
                }
            }
            
            response = requests.post(
                "https://api.notion.com/v1/pages",
                headers=self.notion_headers,
                json=page_data,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"✅ Analytics logged: {post_data.get('platform')} post")
                return True
            else:
                print(f"❌ Analytics error: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Analytics logging error: {e}")
            return False
    
    def log_engagement(self, engagement_data: Dict) -> bool:
        """Log engagement activity to analytics"""
        if not self.notion_headers or not self.config.notion_database_id:
            print(f"📊 ENGAGEMENT: {engagement_data}")
            return False
        
        try:
            page_data = {
                "parent": {"database_id": self.config.notion_database_id},
                "properties": {
                    "Title": {
                        "title": [{"text": {"content": "Daily Engagement Summary"}}]
                    },
                    "Platform": {
                        "select": {"name": "Multiple"}
                    },
                    "Content": {
                        "rich_text": [{"text": {"content": f"Mentions: {engagement_data.get('mentions_checked', 0)}, Likes: {engagement_data.get('likes_given', 0)}"}}]
                    },
                    "Date": {
                        "date": {"start": datetime.now(timezone.utc).isoformat()}
                    },
                    "Status": {
                        "select": {"name": "Completed"}
                    }
                }
            }
            
            response = requests.post(
                "https://api.notion.com/v1/pages",
                headers=self.notion_headers,
                json=page_data,
                timeout=30
            )
            
            if response.status_code == 200:
                print("✅ Engagement analytics logged")
                return True
            else:
                print(f"❌ Engagement analytics error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Engagement analytics error: {e}")
            return False
    
    def get_basic_stats(self) -> Dict:
        """Get basic statistics from Notion database"""
        if not self.notion_headers or not self.config.notion_database_id:
            return {"error": "Analytics not configured"}
        
        try:
            # Query recent posts from Notion
            query_data = {
                "filter": {
                    "property": "Date",
                    "date": {
                        "past_week": {}
                    }
                }
            }
            
            response = requests.post(
                f"https://api.notion.com/v1/databases/{self.config.notion_database_id}/query",
                headers=self.notion_headers,
                json=query_data,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                
                stats = {
                    "total_posts_week": len(results),
                    "twitter_posts": len([r for r in results if self._get_platform(r) == "Twitter"]),
                    "linkedin_posts": len([r for r in results if self._get_platform(r) == "LinkedIn"]),
                    "last_updated": datetime.now(timezone.utc).isoformat()
                }
                
                print(f"📊 Weekly stats: {stats}")
                return stats
            else:
                print(f"❌ Stats query error: {response.status_code}")
                return {"error": "Failed to fetch stats"}
                
        except Exception as e:
            print(f"❌ Stats error: {e}")
            return {"error": str(e)}
    
    def _get_platform(self, notion_page: Dict) -> str:
        """Extract platform from Notion page properties"""
        try:
            platform_prop = notion_page.get('properties', {}).get('Platform', {})
            select_value = platform_prop.get('select', {})
            return select_value.get('name', 'Unknown')
        except:
            return 'Unknown'
    
    def daily_summary(self, posts: List[Dict], engagement: Dict) -> Dict:
        """Generate and log daily summary"""
        summary = {
            "date": datetime.now(timezone.utc).date().isoformat(),
            "posts_created": len(posts),
            "posts_successful": len([p for p in posts if p.get('success')]),
            "platforms_used": list(set(p.get('platform') for p in posts if p.get('platform'))),
            "engagement_activity": engagement,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        print(f"📊 Daily Summary: {summary}")
        
        # Log summary to analytics if configured
        if self.notion_headers:
            self.log_engagement({
                "type": "daily_summary",
                "posts_count": summary["posts_created"],
                "success_rate": f"{summary['posts_successful']}/{summary['posts_created']}",
                "platforms": ", ".join(summary["platforms_used"])
            })
        
        return summary