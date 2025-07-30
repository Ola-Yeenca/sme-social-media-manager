"""
SME Social Media Manager - Simple Social Media Manager
Handles posting to Twitter and LinkedIn with basic error handling
"""

import tweepy
import requests
from typing import Dict, List, Optional
from config import Config

class SocialManager:
    """Simple social media manager for Twitter and LinkedIn"""
    
    def __init__(self, config: Config):
        self.config = config
        self.twitter_client = None
        self.linkedin_headers = None
        
        # Initialize Twitter
        if all([config.twitter_api_key, config.twitter_api_secret, 
                config.twitter_access_token, config.twitter_access_token_secret]):
            try:
                self.twitter_client = tweepy.Client(
                    bearer_token=config.twitter_bearer_token,
                    consumer_key=config.twitter_api_key,
                    consumer_secret=config.twitter_api_secret,
                    access_token=config.twitter_access_token,
                    access_token_secret=config.twitter_access_token_secret,
                    wait_on_rate_limit=True
                )
                print("✅ Twitter client initialized")
            except Exception as e:
                print(f"❌ Twitter initialization failed: {e}")
        
        # Initialize LinkedIn
        if config.linkedin_access_token:
            self.linkedin_headers = {
                'Authorization': f'Bearer {config.linkedin_access_token}',
                'Content-Type': 'application/json',
                'X-Restli-Protocol-Version': '2.0.0'
            }
            print("✅ LinkedIn client initialized")
    
    def post_to_twitter(self, content: str) -> Optional[Dict]:
        """Post content to Twitter"""
        if not self.twitter_client:
            print("❌ Twitter client not available")
            return None
            
        try:
            # Ensure content fits Twitter's character limit
            if len(content) > 280:
                content = content[:277] + "..."
                
            response = self.twitter_client.create_tweet(text=content)
            
            if response.data:
                tweet_id = response.data['id']
                tweet_url = f"https://twitter.com/SMEAnalytica/status/{tweet_id}"
                print(f"✅ Posted to Twitter: {tweet_url}")
                
                return {
                    "platform": "twitter",
                    "post_id": tweet_id,
                    "url": tweet_url,
                    "content": content,
                    "success": True
                }
            else:
                print("❌ Twitter post failed - no response data")
                return None
                
        except Exception as e:
            print(f"❌ Twitter posting error: {e}")
            return None
    
    def post_to_linkedin(self, content: str) -> Optional[Dict]:
        """Post content to LinkedIn"""
        if not self.linkedin_headers or not self.config.linkedin_organization_id:
            print("❌ LinkedIn not configured")
            return None
            
        try:
            # LinkedIn post payload
            post_data = {
                "author": f"urn:li:organization:{self.config.linkedin_organization_id}",
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
            
            response = requests.post(
                "https://api.linkedin.com/v2/ugcPosts",
                headers=self.linkedin_headers,
                json=post_data,
                timeout=30
            )
            
            if response.status_code == 201:
                post_id = response.json().get('id', 'unknown')
                print(f"✅ Posted to LinkedIn: {post_id}")
                
                return {
                    "platform": "linkedin", 
                    "post_id": post_id,
                    "content": content,
                    "success": True
                }
            else:
                print(f"❌ LinkedIn post failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ LinkedIn posting error: {e}")
            return None
    
    def post_to_all_platforms(self, content: str) -> List[Dict]:
        """Post content to all configured platforms"""
        results = []
        
        # Post to Twitter
        twitter_result = self.post_to_twitter(content)
        if twitter_result:
            results.append(twitter_result)
        
        # Post to LinkedIn (modify content slightly for LinkedIn)
        linkedin_content = content.replace("#", "")  # Remove hashtags for LinkedIn
        linkedin_result = self.post_to_linkedin(linkedin_content)
        if linkedin_result:
            results.append(linkedin_result)
        
        return results
    
    def get_mentions(self, limit: int = 10) -> List[Dict]:
        """Get recent mentions from Twitter"""
        if not self.twitter_client:
            return []
            
        try:
            # Get mentions from Twitter API v2
            mentions = self.twitter_client.get_mentions(
                max_results=limit,
                tweet_fields=['created_at', 'author_id', 'public_metrics']
            )
            
            results = []
            if mentions.data:
                for mention in mentions.data:
                    results.append({
                        "id": mention.id,
                        "text": mention.text,
                        "author_id": mention.author_id,
                        "created_at": mention.created_at,
                        "platform": "twitter"
                    })
            
            return results
            
        except Exception as e:
            print(f"❌ Error getting mentions: {e}")
            return []
    
    def reply_to_tweet(self, tweet_id: str, content: str) -> Optional[Dict]:
        """Reply to a specific tweet"""
        if not self.twitter_client:
            return None
            
        try:
            response = self.twitter_client.create_tweet(
                text=content,
                in_reply_to_tweet_id=tweet_id
            )
            
            if response.data:
                reply_id = response.data['id']
                reply_url = f"https://twitter.com/SMEAnalytica/status/{reply_id}"
                print(f"✅ Replied to tweet: {reply_url}")
                
                return {
                    "platform": "twitter",
                    "reply_id": reply_id,
                    "original_tweet_id": tweet_id,
                    "url": reply_url,
                    "content": content,
                    "success": True
                }
            
        except Exception as e:
            print(f"❌ Reply error: {e}")
            return None