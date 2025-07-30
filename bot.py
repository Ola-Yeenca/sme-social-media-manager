#!/usr/bin/env python3
"""
SME Social Media Bot - Simple & Working
Posts 3-4 times daily, monitors mentions, engages with relevant posts
"""

import os
import sys
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional

import tweepy
import openai
from config import Config


class SMESocialBot:
    """Simple social media bot that actually works"""
    
    def __init__(self):
        """Initialize the bot with API connections"""
        self.config = Config()
        self.setup_twitter()
        self.setup_ai()
        
        # Simple tracking
        self.session_stats = {
            'posts_created': 0,
            'mentions_checked': 0,
            'engagements_made': 0,
            'errors': 0
        }
        
    def setup_twitter(self):
        """Setup Twitter API connection"""
        try:
            # Twitter API v2 client
            self.twitter = tweepy.Client(
                bearer_token=self.config.twitter_bearer_token,
                consumer_key=self.config.twitter_api_key,
                consumer_secret=self.config.twitter_api_secret,
                access_token=self.config.twitter_access_token,
                access_token_secret=self.config.twitter_access_token_secret,
                wait_on_rate_limit=True
            )
            
            # Test connection
            me = self.twitter.get_me()
            print(f"✅ Connected to Twitter as @{me.data.username}")
            
        except Exception as e:
            print(f"❌ Twitter setup failed: {e}")
            sys.exit(1)
            
    def setup_ai(self):
        """Setup AI for content generation"""
        try:
            if self.config.openai_api_key:
                openai.api_key = self.config.openai_api_key
                # Test connection
                openai.models.list()
                print("✅ OpenAI connected")
                self.ai_provider = 'openai'
            else:
                print("❌ No AI provider configured")
                sys.exit(1)
                
        except Exception as e:
            print(f"❌ AI setup failed: {e}")
            sys.exit(1)
    
    def generate_content(self) -> str:
        """Generate social media content using AI"""
        
        business_context = """
        SME Analytica provides MenuFlow dynamic pricing for restaurants, hotels, and retail businesses.
        We help small businesses optimize pricing, increase margins (~10%), and make data-driven decisions.
        Our platform integrates with POS systems and provides real-time analytics.
        Target audience: Restaurant owners, hotel managers, small business entrepreneurs in Europe.
        """
        
        content_prompts = [
            "Write a helpful tip for restaurant owners about pricing strategy. Include a practical insight. Keep it under 280 characters. End with 1-2 relevant emojis.",
            "Share an interesting statistic about how dynamic pricing helps restaurants increase profits. Make it engaging and educational. Under 280 characters with emojis.",
            "Create a short post about the importance of data-driven decisions for small businesses. Include a question to encourage engagement. Under 280 characters.",
            "Write about a common mistake restaurant owners make with menu pricing and how to avoid it. Helpful and informative tone. Under 280 characters with emojis."
        ]
        
        try:
            prompt = random.choice(content_prompts)
            
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are the social media manager for SME Analytica. Context: {business_context}"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            
            # Ensure it's under 280 characters
            if len(content) > 280:
                content = content[:277] + "..."
                
            return content
            
        except Exception as e:
            print(f"❌ Content generation failed: {e}")
            self.session_stats['errors'] += 1
            return None
    
    def post_content(self, content: str) -> bool:
        """Post content to Twitter"""
        try:
            if not content:
                return False
                
            response = self.twitter.create_tweet(text=content)
            
            if response.data:
                print(f"✅ Posted: {content[:50]}...")
                self.session_stats['posts_created'] += 1
                return True
            else:
                print(f"❌ Failed to post: {content[:50]}...")
                self.session_stats['errors'] += 1
                return False
                
        except Exception as e:
            print(f"❌ Posting failed: {e}")
            self.session_stats['errors'] += 1
            return False
    
    def check_mentions(self) -> List[Dict]:
        """Check for mentions and replies"""
        try:
            # Get mentions from last 24 hours
            since_time = datetime.now() - timedelta(hours=24)
            
            mentions = self.twitter.get_users_mentions(
                id=self.twitter.get_me().data.id,
                max_results=10,
                start_time=since_time.isoformat()
            )
            
            mention_list = []
            if mentions.data:
                for mention in mentions.data:
                    mention_list.append({
                        'id': mention.id,
                        'text': mention.text,
                        'author_id': mention.author_id,
                        'created_at': mention.created_at
                    })
                    
            self.session_stats['mentions_checked'] += len(mention_list)
            print(f"✅ Found {len(mention_list)} mentions")
            return mention_list
            
        except Exception as e:
            print(f"❌ Mention check failed: {e}")
            self.session_stats['errors'] += 1
            return []
    
    def engage_with_mentions(self, mentions: List[Dict]) -> int:
        """Engage with mentions by liking and sometimes replying"""
        engagements = 0
        
        for mention in mentions[:3]:  # Limit to 3 engagements
            try:
                # Always like the mention
                self.twitter.like(mention['id'])
                engagements += 1
                print(f"✅ Liked mention: {mention['text'][:30]}...")
                
                # Sometimes reply (30% chance)
                if random.random() < 0.3:
                    reply = self.generate_reply(mention['text'])
                    if reply:
                        self.twitter.create_tweet(
                            text=reply,
                            in_reply_to_tweet_id=mention['id']
                        )
                        engagements += 1
                        print(f"✅ Replied: {reply[:30]}...")
                
                # Rate limiting - wait between engagements
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ Engagement failed: {e}")
                self.session_stats['errors'] += 1
                continue
        
        self.session_stats['engagements_made'] += engagements
        return engagements
    
    def generate_reply(self, original_text: str) -> Optional[str]:
        """Generate a helpful reply to a mention"""
        try:
            business_context = "SME Analytica helps restaurants optimize pricing and increase profits through data analytics."
            
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"You are SME Analytica's helpful social media manager. Context: {business_context}. Reply helpfully and professionally. Keep under 280 characters."},
                    {"role": "user", "content": f"Someone mentioned us saying: '{original_text}'. Write a helpful, friendly reply."}
                ],
                max_tokens=80,
                temperature=0.6
            )
            
            reply = response.choices[0].message.content.strip()
            
            # Ensure it's under 280 characters
            if len(reply) > 280:
                reply = reply[:277] + "..."
                
            return reply
            
        except Exception as e:
            print(f"❌ Reply generation failed: {e}")
            return None
    
    def find_relevant_posts(self) -> List[Dict]:
        """Find posts related to our business to engage with"""
        keywords = [
            "restaurant pricing",
            "restaurant owner",
            "menu optimization", 
            "small business analytics",
            "POS system",
            "restaurant margins"
        ]
        
        relevant_posts = []
        
        try:
            # Search for one keyword at a time to avoid rate limits
            keyword = random.choice(keywords)
            
            tweets = self.twitter.search_recent_tweets(
                query=f"{keyword} -is:retweet -from:smeanalytica",
                max_results=5,
                tweet_fields=['public_metrics', 'created_at']
            )
            
            if tweets.data:
                for tweet in tweets.data:
                    # Only engage with tweets that have some engagement already
                    if tweet.public_metrics['like_count'] > 0:
                        relevant_posts.append({
                            'id': tweet.id,
                            'text': tweet.text,
                            'likes': tweet.public_metrics['like_count'],
                            'created_at': tweet.created_at
                        })
            
            print(f"✅ Found {len(relevant_posts)} relevant posts for '{keyword}'")
            return relevant_posts
            
        except Exception as e:
            print(f"❌ Post search failed: {e}")
            self.session_stats['errors'] += 1
            return []
    
    def engage_with_relevant_posts(self, posts: List[Dict]) -> int:
        """Like relevant posts from potential customers"""
        engagements = 0
        
        for post in posts[:2]:  # Limit to 2 engagements
            try:
                self.twitter.like(post['id'])
                engagements += 1
                print(f"✅ Liked relevant post: {post['text'][:30]}...")
                
                # Wait between engagements
                time.sleep(3)
                
            except Exception as e:
                print(f"❌ Like failed: {e}")
                self.session_stats['errors'] += 1
                continue
        
        self.session_stats['engagements_made'] += engagements
        return engagements
    
    def run_daily_automation(self):
        """Run the complete daily automation sequence"""
        print(f"\n🤖 Starting SME Social Media Bot")
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print("=" * 50)
        
        # 1. Generate and post content (2-3 posts)
        posts_to_create = random.choice([2, 3])
        print(f"\n📝 Creating {posts_to_create} posts...")
        
        for i in range(posts_to_create):
            content = self.generate_content()
            if content:
                success = self.post_content(content)
                if success and i < posts_to_create - 1:
                    # Wait between posts
                    time.sleep(60)  # 1 minute between posts
        
        # 2. Check and engage with mentions
        print(f"\n👂 Checking mentions...")
        mentions = self.check_mentions()
        if mentions:
            self.engage_with_mentions(mentions)
        
        # 3. Find and engage with relevant posts
        print(f"\n🔍 Finding relevant posts to engage with...")
        relevant_posts = self.find_relevant_posts()
        if relevant_posts:
            self.engage_with_relevant_posts(relevant_posts)
        
        # 4. Show results
        print(f"\n📊 Session Results:")
        print(f"  Posts created: {self.session_stats['posts_created']}")
        print(f"  Mentions checked: {self.session_stats['mentions_checked']}")
        print(f"  Engagements made: {self.session_stats['engagements_made']}")
        print(f"  Errors: {self.session_stats['errors']}")
        print("=" * 50)
        print("✅ Bot run complete!")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='SME Social Media Bot')
    parser.add_argument('--test', action='store_true', help='Test mode - generate content only')
    args = parser.parse_args()
    
    try:
        bot = SMESocialBot()
        
        if args.test:
            print("🧪 Test mode - generating sample content...")
            content = bot.generate_content()
            if content:
                print(f"Generated: {content}")
            else:
                print("❌ Content generation failed")
        else:
            bot.run_daily_automation()
            
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()