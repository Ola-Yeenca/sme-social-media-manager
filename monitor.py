"""
SME Social Media Manager - Simple Monitor
Basic mention monitoring and engagement automation
"""

from typing import List, Dict, Optional
from social_manager import SocialManager
from content_generator import ContentGenerator
from config import Config

class Monitor:
    """Simple monitoring and engagement system"""
    
    def __init__(self, config: Config, social_manager: SocialManager, content_generator: ContentGenerator):
        self.config = config
        self.social_manager = social_manager
        self.content_generator = content_generator
        self.processed_mentions = set()  # Simple in-memory tracking
    
    def check_mentions(self) -> List[Dict]:
        """Check for new mentions and respond appropriately"""
        print("🔍 Checking for mentions...")
        
        mentions = self.social_manager.get_mentions(limit=10)
        new_mentions = []
        
        for mention in mentions:
            mention_id = mention.get('id')
            
            # Skip if already processed
            if mention_id in self.processed_mentions:
                continue
                
            # Skip if it's our own tweet
            if self._is_our_tweet(mention.get('text', '')):
                continue
            
            print(f"📩 New mention found: {mention.get('text', '')[:50]}...")
            
            # Generate and send response
            response = self._handle_mention(mention)
            if response:
                new_mentions.append({
                    "mention": mention,
                    "response": response
                })
            
            # Mark as processed
            self.processed_mentions.add(mention_id)
        
        return new_mentions
    
    def _handle_mention(self, mention: Dict) -> Optional[Dict]:
        """Handle a single mention"""
        mention_text = mention.get('text', '')
        mention_id = mention.get('id')
        author_id = mention.get('author_id', 'unknown')
        
        # Generate AI response
        response_text = self.content_generator.generate_response_to_mention(
            mention_text, 
            author_id
        )
        
        if not response_text:
            print("❌ Could not generate response")
            return None
        
        # Post reply
        reply_result = self.social_manager.reply_to_tweet(mention_id, response_text)
        
        if reply_result:
            print(f"✅ Responded to mention: {response_text[:50]}...")
            return reply_result
        else:
            print("❌ Failed to post reply")
            return None
    
    def _is_our_tweet(self, text: str) -> bool:
        """Check if this is our own tweet (simple heuristic)"""
        our_indicators = [
            self.config.company_name.lower(),
            "sme analytica",
            "@smeanalytica"
        ]
        
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in our_indicators)
    
    def basic_engagement(self) -> Dict:
        """Perform basic engagement activities"""
        print("🤝 Running basic engagement...")
        
        engagement_results = {
            "likes_given": 0,
            "follows_attempted": 0,
            "mentions_checked": 0
        }
        
        try:
            # Check mentions (main engagement activity)
            mentions = self.check_mentions()
            engagement_results["mentions_checked"] = len(mentions)
            
            # Simple engagement with relevant tweets (very basic)
            relevant_tweets = self._find_relevant_tweets()
            for tweet in relevant_tweets[:3]:  # Limit to 3 per run
                if self._like_tweet(tweet.get('id')):
                    engagement_results["likes_given"] += 1
            
            print(f"✅ Engagement complete: {engagement_results}")
            return engagement_results
            
        except Exception as e:
            print(f"❌ Engagement error: {e}")
            return engagement_results
    
    def _find_relevant_tweets(self) -> List[Dict]:
        """Find tweets relevant to our industry (simple search)"""
        if not self.social_manager.twitter_client:
            return []
            
        try:
            # Search for recent tweets about restaurant/hospitality
            search_terms = [
                "restaurant management",
                "hospitality business",
                "small business owner"
            ]
            
            tweets = []
            for term in search_terms[:1]:  # Limit API calls
                try:
                    results = self.social_manager.twitter_client.search_recent_tweets(
                        query=f"{term} -is:retweet",
                        max_results=10,
                        tweet_fields=['created_at', 'author_id', 'public_metrics']
                    )
                    
                    if results.data:
                        tweets.extend([{
                            "id": tweet.id,
                            "text": tweet.text,
                            "author_id": tweet.author_id
                        } for tweet in results.data])
                        
                except Exception as e:
                    print(f"Search error for '{term}': {e}")
                    continue
            
            return tweets
            
        except Exception as e:
            print(f"❌ Error finding relevant tweets: {e}")
            return []
    
    def _like_tweet(self, tweet_id: str) -> bool:
        """Like a specific tweet"""
        if not self.social_manager.twitter_client:
            return False
            
        try:
            self.social_manager.twitter_client.like(tweet_id)
            print(f"👍 Liked tweet: {tweet_id}")
            return True
        except Exception as e:
            print(f"❌ Like error: {e}")
            return False