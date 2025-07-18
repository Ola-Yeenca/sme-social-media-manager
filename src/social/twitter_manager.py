"""
Twitter/X API integration for SME Analytica Social Media Manager
"""

import tweepy
import asyncio
import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import logging
from dataclasses import dataclass

@dataclass
class Tweet:
    """Tweet data structure"""
    id: str
    text: str
    author_id: str
    author_username: str
    created_at: datetime
    public_metrics: Dict[str, int]
    context_annotations: Optional[List[Dict]] = None
    referenced_tweets: Optional[List[Dict]] = None

@dataclass
class TwitterUser:
    """Twitter user data structure"""
    id: str
    username: str
    name: str
    description: str
    public_metrics: Dict[str, int]
    verified: bool = False
    profile_image_url: Optional[str] = None

class TwitterManager:
    """Manages Twitter API interactions for SME Analytica"""
    
    def __init__(self, api_credentials: Dict[str, str]):
        self.api_key = api_credentials["api_key"]
        self.api_secret = api_credentials["api_secret"]
        self.access_token = api_credentials["access_token"]
        self.access_token_secret = api_credentials["access_token_secret"]
        self.bearer_token = api_credentials["bearer_token"]

        # Initialize logger first
        self.logger = logging.getLogger(__name__)

        # Initialize Tweepy clients
        self._initialize_clients()

        # Rate limiting
        self.last_tweet_time = None
        self.min_interval_between_tweets = 300  # 5 minutes

        # Engagement tracking
        self.daily_engagement_count = 0
        self.daily_engagement_limit = 50
        self.last_engagement_reset = datetime.now().date()
    
    def _initialize_clients(self):
        """Initialize Twitter API clients"""
        try:
            # V2 Client for modern features
            self.client = tweepy.Client(
                bearer_token=self.bearer_token,
                consumer_key=self.api_key,
                consumer_secret=self.api_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret,
                wait_on_rate_limit=True
            )
            
            # V1.1 API for legacy features if needed
            auth = tweepy.OAuth1UserHandler(
                self.api_key,
                self.api_secret,
                self.access_token,
                self.access_token_secret
            )
            self.api_v1 = tweepy.API(auth, wait_on_rate_limit=True)
            
            self.logger.info("Twitter API clients initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Twitter clients: {e}")
            raise
    
    async def post_tweet(self, content: str, reply_to_tweet_id: Optional[str] = None,
                        media_ids: Optional[List[str]] = None) -> Optional[str]:
        """Post a tweet with content validation and rate limiting"""

        # Validate content
        if not self._validate_tweet_content(content):
            self.logger.error(f"Invalid tweet content: {content}")
            return None

        # Twitter subscription allows longer posts - use full content
        truncated_content = content
        self.logger.info(f"Posting full content ({len(content)} characters) - Twitter subscription active")
        
        # Check rate limiting
        if not self._can_tweet():
            self.logger.warning("Rate limit reached, skipping tweet")
            return None
        
        try:
            # Post tweet using v2 API
            response = self.client.create_tweet(
                text=truncated_content,
                in_reply_to_tweet_id=reply_to_tweet_id,
                media_ids=media_ids
            )
            
            if response.data:
                tweet_id = response.data['id']
                self.last_tweet_time = datetime.now()
                self.logger.info(f"Tweet posted successfully: {tweet_id}")
                return tweet_id
            else:
                self.logger.error("Tweet posting failed - no response data")
                return None
                
        except tweepy.TooManyRequests:
            self.logger.warning("Rate limit exceeded while posting tweet")
            return None
        except tweepy.Forbidden as e:
            self.logger.error(f"Tweet posting forbidden: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error posting tweet: {e}")
            return None
    
    async def reply_to_tweet(self, tweet_id: str, reply_content: str) -> Optional[str]:
        """Reply to a specific tweet"""
        
        if not self._can_engage():
            self.logger.warning("Daily engagement limit reached")
            return None
        
        try:
            response = self.client.create_tweet(
                text=reply_content,
                in_reply_to_tweet_id=tweet_id
            )
            
            if response.data:
                reply_id = response.data['id']
                self._increment_engagement_count()
                self.logger.info(f"Reply posted successfully: {reply_id}")
                return reply_id
            else:
                self.logger.error("Reply posting failed")
                return None
                
        except Exception as e:
            self.logger.error(f"Error posting reply: {e}")
            return None
    
    async def like_tweet(self, tweet_id: str) -> bool:
        """Like a tweet"""
        
        if not self._can_engage():
            return False
        
        try:
            response = self.client.like(tweet_id)
            if response:
                self._increment_engagement_count()
                self.logger.info(f"Liked tweet: {tweet_id}")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Error liking tweet: {e}")
            return False
    
    async def retweet_with_comment(self, tweet_id: str, comment: str) -> Optional[str]:
        """Retweet with a comment (quote tweet)"""
        
        if not self._can_engage():
            return None
        
        try:
            # Get the original tweet URL for quote tweeting
            original_tweet = self.client.get_tweet(tweet_id, 
                                                 tweet_fields=["author_id"],
                                                 user_fields=["username"])
            
            if original_tweet.data and original_tweet.includes:
                author_username = original_tweet.includes['users'][0].username
                tweet_url = f"https://twitter.com/{author_username}/status/{tweet_id}"
                
                # Create quote tweet
                quote_text = f"{comment} {tweet_url}"
                
                response = self.client.create_tweet(text=quote_text)
                
                if response.data:
                    quote_id = response.data['id']
                    self._increment_engagement_count()
                    self.logger.info(f"Quote tweet posted: {quote_id}")
                    return quote_id
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error quote tweeting: {e}")
            return None
    
    async def search_tweets(self, query: str, max_results: int = 10, 
                          exclude_retweets: bool = True) -> List[Tweet]:
        """Search for tweets matching a query"""
        
        try:
            # Build search query
            search_query = query
            if exclude_retweets:
                search_query += " -is:retweet"
            
            # Add language filter (remove min_faves as it requires premium access)
            search_query += " lang:en"
            
            tweets = tweepy.Paginator(
                self.client.search_recent_tweets,
                query=search_query,
                max_results=max_results,
                tweet_fields=['author_id', 'created_at', 'public_metrics', 'context_annotations'],
                user_fields=['username', 'name', 'description', 'public_metrics'],
                expansions=['author_id']
            ).flatten(limit=max_results)
            
            tweet_objects = []
            for tweet in tweets:
                # Find author info
                author_info = None
                if hasattr(self.client.get_tweet(tweet.id, expansions=['author_id']), 'includes'):
                    includes = self.client.get_tweet(tweet.id, expansions=['author_id']).includes
                    if includes and 'users' in includes:
                        author_info = includes['users'][0]
                
                tweet_obj = Tweet(
                    id=tweet.id,
                    text=tweet.text,
                    author_id=tweet.author_id,
                    author_username=author_info.username if author_info else "unknown",
                    created_at=tweet.created_at,
                    public_metrics=tweet.public_metrics,
                    context_annotations=getattr(tweet, 'context_annotations', None)
                )
                tweet_objects.append(tweet_obj)
            
            return tweet_objects
            
        except Exception as e:
            self.logger.error(f"Error searching tweets: {e}")
            return []
    
    async def get_mentions(self, max_results: int = 20, since_time: Optional[datetime] = None) -> List[Tweet]:
        """Get recent mentions of SME Analytica with optional time filtering"""

        try:
            # Build parameters for mentions request
            params = {
                'id': self.client.get_me().data.id,
                'max_results': max_results,
                'tweet_fields': ['author_id', 'created_at', 'public_metrics', 'context_annotations', 'in_reply_to_user_id'],
                'user_fields': ['username', 'name', 'description', 'public_metrics'],
                'expansions': ['author_id']
            }

            # Add time filter if provided (RFC3339 format)
            if since_time:
                params['start_time'] = since_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

            mentions = self.client.get_users_mentions(**params)

            mention_objects = []
            if mentions.data:
                for mention in mentions.data:
                    # Find author info
                    author_info = None
                    if mentions.includes and 'users' in mentions.includes:
                        author_info = next((user for user in mentions.includes['users']
                                          if user.id == mention.author_id), None)

                    mention_obj = Tweet(
                        id=mention.id,
                        text=mention.text,
                        author_id=mention.author_id,
                        author_username=author_info.username if author_info else "unknown",
                        created_at=mention.created_at,
                        public_metrics=mention.public_metrics,
                        context_annotations=getattr(mention, 'context_annotations', None)
                    )
                    mention_objects.append(mention_obj)

            return mention_objects

        except Exception as e:
            self.logger.error(f"Error getting mentions: {e}")
            return []

    async def get_notifications(self, since_time: Optional[datetime] = None, max_results: int = 50) -> List[Dict[str, Any]]:
        """Get comprehensive notifications including mentions, replies, and interactions"""

        try:
            notifications = []

            # Get mentions
            mentions = await self.get_mentions(max_results=max_results//2, since_time=since_time)
            for mention in mentions:
                notifications.append({
                    'type': 'mention',
                    'tweet': mention,
                    'timestamp': mention.created_at,
                    'author': mention.author_username,
                    'content': mention.text
                })

            # Get replies to our tweets (search for replies)
            if since_time:
                time_filter = f" since:{since_time.strftime('%Y-%m-%d')}"
            else:
                time_filter = ""

            # Search for replies to our account
            reply_query = f"to:smeanalytica{time_filter}"
            reply_tweets = await self.search_tweets(reply_query, max_results=max_results//2)

            for reply in reply_tweets:
                notifications.append({
                    'type': 'reply',
                    'tweet': reply,
                    'timestamp': reply.created_at,
                    'author': reply.author_username,
                    'content': reply.text
                })

            # Sort by timestamp (newest first)
            notifications.sort(key=lambda x: x['timestamp'], reverse=True)

            return notifications[:max_results]

        except Exception as e:
            self.logger.error(f"Error getting notifications: {e}")
            return []

    async def retweet(self, tweet_id: str) -> bool:
        """Retweet a specific tweet"""
        try:
            response = self.client.retweet(tweet_id)
            if response.data:
                self.logger.info(f"Successfully retweeted: {tweet_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error retweeting {tweet_id}: {e}")
            return False

    async def like_tweet(self, tweet_id: str) -> bool:
        """Like a specific tweet"""
        try:
            response = self.client.like(tweet_id)
            if response.data:
                self.logger.info(f"Successfully liked: {tweet_id}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error liking {tweet_id}: {e}")
            return False

    async def reply_to_tweet(self, tweet_id: str, content: str) -> Optional[str]:
        """Reply to a specific tweet"""
        return await self.post_tweet(content=content, reply_to_tweet_id=tweet_id)

    async def get_conversation_thread(self, tweet_id: str, max_depth: int = 5) -> List[Dict[str, Any]]:
        """Get conversation thread for a tweet"""
        try:
            thread = []
            current_id = tweet_id

            for _ in range(max_depth):
                tweet = self.client.get_tweet(
                    current_id,
                    tweet_fields=['author_id', 'created_at', 'in_reply_to_user_id', 'conversation_id'],
                    user_fields=['username', 'name'],
                    expansions=['author_id']
                )

                if tweet.data:
                    author_info = None
                    if tweet.includes and 'users' in tweet.includes:
                        author_info = tweet.includes['users'][0]

                    thread.append({
                        'id': tweet.data.id,
                        'text': tweet.data.text,
                        'author': author_info.username if author_info else 'unknown',
                        'created_at': tweet.data.created_at,
                        'in_reply_to_user_id': getattr(tweet.data, 'in_reply_to_user_id', None)
                    })

                    # Get the tweet this is replying to
                    if hasattr(tweet.data, 'in_reply_to_user_id'):
                        # This would require additional API calls to get the parent tweet
                        # For now, we'll stop here
                        break
                else:
                    break

            return thread

        except Exception as e:
            self.logger.error(f"Error getting conversation thread for {tweet_id}: {e}")
            return []

    async def get_user_profile(self, username: str) -> Dict[str, Any]:
        """Get detailed user profile information"""
        try:
            user = self.client.get_user(
                username=username,
                user_fields=['public_metrics', 'description', 'created_at', 'verified', 'location']
            )

            if user.data:
                return {
                    'username': user.data.username,
                    'name': user.data.name,
                    'description': user.data.description,
                    'followers': user.data.public_metrics['followers_count'],
                    'following': user.data.public_metrics['following_count'],
                    'tweet_count': user.data.public_metrics['tweet_count'],
                    'verified': getattr(user.data, 'verified', False),
                    'created_at': user.data.created_at,
                    'location': getattr(user.data, 'location', None),
                    'account_type': self._classify_account_type(user.data)
                }

            return {}

        except Exception as e:
            self.logger.error(f"Error getting user profile for {username}: {e}")
            return {}

    def _classify_account_type(self, user_data) -> str:
        """Classify account type based on profile data"""
        description = getattr(user_data, 'description', '').lower()
        followers = user_data.public_metrics['followers_count']

        # Business indicators
        business_keywords = ['restaurant', 'hotel', 'business', 'owner', 'ceo', 'founder', 'manager']
        if any(keyword in description for keyword in business_keywords):
            return 'business'

        # Influencer indicators
        if followers > 10000:
            return 'influencer'
        elif followers > 1000:
            return 'micro_influencer'

        # Tech/industry indicators
        tech_keywords = ['tech', 'developer', 'analytics', 'data', 'ai', 'software']
        if any(keyword in description for keyword in tech_keywords):
            return 'tech_professional'

        return 'individual'
    
    async def get_trending_hashtags(self, location_id: int = 1) -> List[str]:
        """Get trending hashtags (using v1.1 API)"""
        
        try:
            trends = self.api_v1.get_place_trends(location_id)
            if trends:
                trend_names = [trend['name'] for trend in trends[0]['trends'] 
                             if trend['name'].startswith('#')]
                return trend_names[:10]  # Return top 10 hashtag trends
            return []
            
        except Exception as e:
            self.logger.error(f"Error getting trending hashtags: {e}")
            return []
    
    async def get_user_info(self, username: str) -> Optional[TwitterUser]:
        """Get information about a Twitter user"""
        
        try:
            user = self.client.get_user(
                username=username,
                user_fields=['description', 'public_metrics', 'verified', 'profile_image_url']
            )
            
            if user.data:
                return TwitterUser(
                    id=user.data.id,
                    username=user.data.username,
                    name=user.data.name,
                    description=user.data.description or "",
                    public_metrics=user.data.public_metrics,
                    verified=getattr(user.data, 'verified', False),
                    profile_image_url=getattr(user.data, 'profile_image_url', None)
                )
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting user info for {username}: {e}")
            return None
    
    async def get_engagement_opportunities(self) -> List[Dict[str, Any]]:
        """Find engagement opportunities by searching relevant hashtags and keywords"""
        
        # Keywords related to SME Analytica's domain
        search_terms = [
            "#RestaurantTech",
            "#SmallBusiness analytics",
            "#AIforSMEs",
            "restaurant pricing strategy",
            "#HospitalityTech",
            "small business data",
            "#MenuTech",
            "#RestaurantAnalytics"
        ]
        
        opportunities = []
        
        for term in search_terms:
            tweets = await self.search_tweets(term, max_results=10)
            
            for tweet in tweets:
                # Calculate engagement score
                engagement_score = self._calculate_engagement_score(tweet)
                
                if engagement_score > 5:  # Minimum threshold
                    opportunities.append({
                        "tweet": tweet,
                        "search_term": term,
                        "engagement_score": engagement_score,
                        "opportunity_type": self._classify_opportunity(tweet, term)
                    })
        
        # Sort by engagement score
        opportunities.sort(key=lambda x: x["engagement_score"], reverse=True)
        
        return opportunities[:10]  # Return top 10 opportunities
    
    def _validate_tweet_content(self, content: str) -> bool:
        """Validate tweet content before posting"""

        if not content or len(content.strip()) == 0:
            return False

        # Check for spam indicators
        spam_indicators = ['buy now', 'click here', 'limited time', 'free money']
        content_lower = content.lower()
        if any(indicator in content_lower for indicator in spam_indicators):
            return False

        return True

    def _truncate_tweet_content(self, content: str) -> str:
        """Intelligently truncate tweet content to fit within 280 characters"""

        if len(content) <= 280:
            return content

        # Extract hashtags from the end
        import re
        hashtag_pattern = r'(#\w+(?:\s+#\w+)*)\s*$'
        hashtag_match = re.search(hashtag_pattern, content)
        hashtags = hashtag_match.group(1) if hashtag_match else ""

        # Calculate available space for main content
        available_chars = 280 - len(hashtags) - (1 if hashtags else 0)  # -1 for space before hashtags

        # Remove hashtags from content for truncation
        main_content = re.sub(hashtag_pattern, '', content).strip()

        if len(main_content) <= available_chars:
            return f"{main_content} {hashtags}".strip()

        # Truncate main content, trying to end at a word boundary
        truncated = main_content[:available_chars-3]  # -3 for "..."

        # Try to end at a word boundary
        last_space = truncated.rfind(' ')
        if last_space > available_chars * 0.8:  # Only use word boundary if it's not too short
            truncated = truncated[:last_space]

        # Add ellipsis and hashtags
        result = f"{truncated}... {hashtags}".strip()

        # Final safety check
        if len(result) > 280:
            # Emergency truncation
            excess = len(result) - 280
            truncated = truncated[:-excess-3]
            result = f"{truncated}... {hashtags}".strip()

        return result
    
    def _can_tweet(self) -> bool:
        """Check if we can post a new tweet based on rate limiting"""
        
        if self.last_tweet_time is None:
            return True
        
        time_since_last = datetime.now() - self.last_tweet_time
        return time_since_last.total_seconds() >= self.min_interval_between_tweets
    
    def _can_engage(self) -> bool:
        """Check if we can perform engagement actions"""
        
        # Reset daily counter if it's a new day
        if self.last_engagement_reset != datetime.now().date():
            self.daily_engagement_count = 0
            self.last_engagement_reset = datetime.now().date()
        
        return self.daily_engagement_count < self.daily_engagement_limit
    
    def _increment_engagement_count(self):
        """Increment the daily engagement counter"""
        self.daily_engagement_count += 1
    
    def _calculate_engagement_score(self, tweet: Tweet) -> float:
        """Calculate engagement score for a tweet"""
        
        metrics = tweet.public_metrics
        
        # Base score from engagement metrics
        likes = metrics.get('like_count', 0)
        retweets = metrics.get('retweet_count', 0)
        replies = metrics.get('reply_count', 0)
        
        # Weight different types of engagement
        score = (likes * 1) + (retweets * 3) + (replies * 2)
        
        # Boost score for SME-relevant keywords
        sme_keywords = ['restaurant', 'small business', 'analytics', 'pricing', 'hotel', 'retail']
        keyword_bonus = sum(2 for keyword in sme_keywords if keyword.lower() in tweet.text.lower())
        
        # Recency bonus (prefer recent tweets)
        hours_old = (datetime.now() - tweet.created_at.replace(tzinfo=None)).total_seconds() / 3600
        recency_bonus = max(0, 10 - hours_old)  # Bonus decreases with age
        
        return score + keyword_bonus + recency_bonus
    
    def _classify_opportunity(self, tweet: Tweet, search_term: str) -> str:
        """Classify the type of engagement opportunity"""
        
        text_lower = tweet.text.lower()
        
        if any(word in text_lower for word in ['help', 'advice', 'how to', 'question']):
            return "help_request"
        elif any(word in text_lower for word in ['problem', 'issue', 'struggling', 'difficult']):
            return "problem_solving"
        elif any(word in text_lower for word in ['success', 'achievement', 'growth', 'improvement']):
            return "success_story"
        elif any(word in text_lower for word in ['news', 'announcement', 'launch', 'update']):
            return "industry_news"
        else:
            return "general_engagement"
    
    async def get_account_metrics(self) -> Dict[str, Any]:
        """Get metrics for our own Twitter account"""
        
        try:
            user = self.client.get_me(
                user_fields=['public_metrics', 'created_at', 'description']
            )
            
            if user.data:
                return {
                    "followers_count": user.data.public_metrics['followers_count'],
                    "following_count": user.data.public_metrics['following_count'],
                    "tweet_count": user.data.public_metrics['tweet_count'],
                    "listed_count": user.data.public_metrics['listed_count'],
                    "account_created": user.data.created_at,
                    "description": user.data.description
                }
            return {}
            
        except Exception as e:
            self.logger.error(f"Error getting account metrics: {e}")
            return {}
    
    def get_rate_limit_status(self) -> Dict[str, Any]:
        """Get current rate limit status"""
        
        try:
            # This is a simplified version - in reality you'd track various endpoints
            return {
                "tweets_remaining": "Available" if self._can_tweet() else "Rate limited",
                "engagements_remaining": self.daily_engagement_limit - self.daily_engagement_count,
                "last_tweet_time": self.last_tweet_time,
                "next_available_tweet_time": self.last_tweet_time + timedelta(seconds=self.min_interval_between_tweets) if self.last_tweet_time else datetime.now()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting rate limit status: {e}")
            return {}
