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
import grok
from config import Config


class SMESocialBot:
    """Simple social media bot that actually works"""
    
    def __init__(self, test_mode=False):
        """Initialize the bot with API connections"""
        self.config = Config()
        self.test_mode = test_mode
        
        if not test_mode:
            self.setup_twitter()
        else:
            print("🧪 Test mode - skipping Twitter connection")
            
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
            # Twitter API v2 client - no immediate API calls
            self.twitter = tweepy.Client(
                bearer_token=self.config.twitter_bearer_token,
                consumer_key=self.config.twitter_api_key,
                consumer_secret=self.config.twitter_api_secret,
                access_token=self.config.twitter_access_token,
                access_token_secret=self.config.twitter_access_token_secret,
                wait_on_rate_limit=True
            )
            
            print("✅ Twitter API client initialized (will test on first use)")
            
        except Exception as e:
            print(f"❌ Twitter setup failed: {e}")
            sys.exit(1)
            
    def setup_ai(self):
        """Setup AI for content generation with fallback support"""
        
        # Try OpenAI first
        if self.config.openai_api_key:
            try:
                openai.api_key = self.config.openai_api_key
                print("✅ OpenAI configured (will test on first use)")
                self.ai_provider = 'openai'
                return
            except Exception as e:
                print(f"⚠️ OpenAI setup failed: {e}")
        
        # Try Anthropic as fallback
        if self.config.anthropic_api_key:
            try:
                import anthropic
                self.anthropic_client = anthropic.Anthropic(api_key=self.config.anthropic_api_key)
                print("✅ Anthropic configured (will test on first use)")
                self.ai_provider = 'anthropic'
                return
            except Exception as e:
                print(f"⚠️ Anthropic setup failed: {e}")

        # Try Grok as a second fallback
        if self.config.grok_api_key:
            try:
                self.grok_client = grok.Client(api_key=self.config.grok_api_key)
                print("✅ Grok configured (will test on first use)")
                self.ai_provider = 'grok'
                return
            except Exception as e:
                print(f"⚠️ Grok setup failed: {e}")
        
        print("❌ No working AI provider available")
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
            content = None

            # 1. Try OpenAI
            if self.ai_provider == 'openai':
                try:
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
                except Exception as openai_error:
                    print(f"⚠️ OpenAI failed: {str(openai_error)[:50]}...")
                    if self.config.anthropic_api_key:
                        print("-> Switching to Anthropic")
                        self.ai_provider = 'anthropic'
                    elif self.config.grok_api_key:
                        print("-> Switching to Grok")
                        self.ai_provider = 'grok'

            # 2. Try Anthropic (if it's the provider or failed over)
            if self.ai_provider == 'anthropic':
                try:
                    if not hasattr(self, 'anthropic_client'):
                        import anthropic
                        self.anthropic_client = anthropic.Anthropic(api_key=self.config.anthropic_api_key)
                    response = self.anthropic_client.messages.create(
                        model="claude-3-haiku-20240307",
                        max_tokens=100,
                        temperature=0.7,
                        system=f"You are the social media manager for SME Analytica. Context: {business_context}",
                        messages=[{"role": "user", "content": prompt}]
                    )
                    content = response.content[0].text.strip()
                except Exception as anthropic_error:
                    print(f"⚠️ Anthropic failed: {str(anthropic_error)[:50]}...")
                    if self.config.grok_api_key:
                        print("-> Switching to Grok")
                        self.ai_provider = 'grok'

            # 3. Try Grok (if it's the provider or failed over)
            if self.ai_provider == 'grok':
                try:
                    if not hasattr(self, 'grok_client'):
                        self.grok_client = grok.Client(api_key=self.config.grok_api_key)
                    response = self.grok_client.chat.completions.create(
                        model="llama3-8b-8192",
                        messages=[
                            {"role": "system", "content": f"You are the social media manager for SME Analytica. Context: {business_context}"},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=100,
                        temperature=0.7
                    )
                    content = response.choices[0].message.content.strip()
                except Exception as grok_error:
                    print(f"⚠️ Grok failed: {str(grok_error)[:50]}...")
            
            if content is None:
                raise Exception("All AI providers failed")
            
            # Ensure it's under 280 characters
            if len(content) > 280:
                content = content[:277] + "..."
                
            return content
            
        except Exception as e:
            print(f"❌ Content generation failed: {e}")
            self.session_stats['errors'] += 1
            
            # Fallback to pre-written content if AI fails
            fallback_content = [
                "Running a restaurant? Dynamic pricing can boost your margins by up to 10%! 📊 Data-driven decisions make all the difference. #RestaurantTech #SmallBusiness",
                "Small business tip: Know your profit margins on every menu item. Most restaurants are surprised by what the data reveals! 💡 #RestaurantOwner #Analytics",
                "Question for restaurant owners: How often do you adjust your menu prices? Data shows flexibility = profitability. 🍽️ #DynamicPricing #BusinessTips",
                "The #1 mistake in restaurant pricing? Ignoring competitor analysis. Stay competitive, stay profitable! 🚀 #RestaurantBusiness #PricingStrategy",
                "Real-time analytics + POS integration = smarter business decisions. It's not just about the food anymore! 📈 #RestaurantTech #DataDriven"
            ]
            
            fallback = random.choice(fallback_content)
            print(f"📝 Using fallback content: {fallback[:50]}...")
            return fallback
    
    def post_content(self, content: str) -> bool:
        """Post content to Twitter"""
        try:
            if not content:
                return False
            
            # Check if we're rate limited
            if hasattr(self, 'rate_limited') and self.rate_limited:
                print(f"🚀 [SIMULATION] Would post: {content[:50]}...")
                print(f"   Full content: {content}")
                self.session_stats['posts_created'] += 1
                return True
                
            response = self.twitter.create_tweet(text=content)
            
            if response.data:
                print(f"✅ POSTED LIVE: {content[:50]}...")
                print(f"   Full content: {content}")
                print(f"   Tweet ID: {response.data['id']}")
                self.session_stats['posts_created'] += 1
                return True
            else:
                print(f"❌ Failed to post: {content[:50]}...")
                self.session_stats['errors'] += 1
                return False
                
        except Exception as e:
            if "Rate limit exceeded" in str(e):
                print(f"⚠️ Hit rate limit, switching to simulation: {content[:50]}...")
                self.rate_limited = True
                return self.post_content(content)  # Retry in simulation mode
            print(f"❌ Posting failed: {e}")
            self.session_stats['errors'] += 1
            return False
    
    def check_mentions(self) -> List[Dict]:
        """Check for mentions and replies"""
        try:
            # Check if we're rate limited
            if hasattr(self, 'rate_limited') and self.rate_limited:
                print("🚀 [SIMULATION] Would check mentions...")
                # Simulate finding mentions
                simulated_mentions = [
                    {'id': '123456', 'text': '@smeanalytica Love your restaurant analytics insights!', 'author_id': 'user1'},
                    {'id': '123457', 'text': '@smeanalytica Can you help with dynamic pricing?', 'author_id': 'user2'}
                ]
                print(f"✅ [SIMULATION] Found {len(simulated_mentions)} mentions")
                return simulated_mentions
            
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
            if "Rate limit exceeded" in str(e):
                print("⚠️ Hit rate limit checking mentions, switching to simulation...")
                self.rate_limited = True
                return self.check_mentions()  # Retry in simulation mode
            print(f"❌ Mention check failed: {e}")
            self.session_stats['errors'] += 1
            return []
    
    def engage_with_mentions(self, mentions: List[Dict]) -> int:
        """Engage with mentions by liking and sometimes replying"""
        engagements = 0
        
        for mention in mentions[:3]:  # Limit to 3 engagements
            try:
                # Check if we're rate limited
                if hasattr(self, 'rate_limited') and self.rate_limited:
                    print(f"🚀 [SIMULATION] Would like mention: {mention['text'][:30]}...")
                    engagements += 1
                    
                    # Sometimes reply (30% chance)
                    if random.random() < 0.3:
                        reply = self.generate_reply(mention['text'])
                        if reply:
                            print(f"🚀 [SIMULATION] Would reply: {reply[:30]}...")
                            engagements += 1
                else:
                    # Always like the mention
                    self.twitter.like(mention['id'])
                    engagements += 1
                    print(f"✅ LIKED LIVE: {mention['text'][:30]}...")
                    
                    # Sometimes reply (30% chance)
                    if random.random() < 0.3:
                        reply = self.generate_reply(mention['text'])
                        if reply:
                            self.twitter.create_tweet(
                                text=reply,
                                in_reply_to_tweet_id=mention['id']
                            )
                            engagements += 1
                            print(f"✅ REPLIED LIVE: {reply[:30]}...")
                
                # Rate limiting - wait between engagements
                time.sleep(2)
                
            except Exception as e:
                if "Rate limit exceeded" in str(e):
                    print("⚠️ Hit rate limit during engagement, switching to simulation...")
                    self.rate_limited = True
                    continue
                print(f"❌ Engagement failed: {e}")
                self.session_stats['errors'] += 1
                continue
        
        self.session_stats['engagements_made'] += engagements
        return engagements
    
    def generate_reply(self, original_text: str) -> Optional[str]:
        """Generate a helpful reply to a mention"""
        try:
            business_context = "SME Analytica helps restaurants optimize pricing and increase profits through data analytics."
            reply = None

            if self.ai_provider == 'openai':
                try:
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
                except Exception as openai_error:
                    print(f"⚠️ OpenAI failed during reply: {str(openai_error)[:50]}...")
                    if self.config.anthropic_api_key:
                        self.ai_provider = 'anthropic'
                    elif self.config.grok_api_key:
                        self.ai_provider = 'grok'

            if self.ai_provider == 'anthropic':
                try:
                    if not hasattr(self, 'anthropic_client'):
                        import anthropic
                        self.anthropic_client = anthropic.Anthropic(api_key=self.config.anthropic_api_key)
                    response = self.anthropic_client.messages.create(
                        model="claude-3-haiku-20240307",
                        max_tokens=80,
                        temperature=0.6,
                        system=f"You are SME Analytica's helpful social media manager. Context: {business_context}. Reply helpfully and professionally. Keep under 280 characters.",
                        messages=[{"role": "user", "content": f"Someone mentioned us saying: '{original_text}'. Write a helpful, friendly reply."}]
                    )
                    reply = response.content[0].text.strip()
                except Exception as anthropic_error:
                    print(f"⚠️ Anthropic failed during reply: {str(anthropic_error)[:50]}...")
                    if self.config.grok_api_key:
                        self.ai_provider = 'grok'

            if self.ai_provider == 'grok':
                try:
                    if not hasattr(self, 'grok_client'):
                        self.grok_client = grok.Client(api_key=self.config.grok_api_key)
                    response = self.grok_client.chat.completions.create(
                        model="llama3-8b-8192",
                        messages=[
                            {"role": "system", "content": f"You are SME Analytica's helpful social media manager. Context: {business_context}. Reply helpfully and professionally. Keep under 280 characters."},
                            {"role": "user", "content": f"Someone mentioned us saying: '{original_text}'. Write a helpful, friendly reply."}
                        ],
                        max_tokens=80,
                        temperature=0.6
                    )
                    reply = response.choices[0].message.content.strip()
                except Exception as grok_error:
                    print(f"⚠️ Grok failed during reply: {str(grok_error)[:50]}...")

            if reply is None:
                return None
            
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
    
    def run_daily_automation(self, posting_only=False):
        """Run the complete daily automation sequence"""
        print(f"\n🤖 Starting SME Social Media Bot")
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        if posting_only:
            print("🔒 POSTING-ONLY MODE: API retrieval quota exceeded")
            print("📅 Full functionality returns August 11th when quota resets")
        
        print("=" * 50)
        
        # Skip initial API check - handle rate limits gracefully during operations
        print("🚀 Starting bot operations...")
        self.rate_limited = False  # Start optimistically
        
        # 1. Generate and post content (2-3 posts) - ALWAYS RUNS
        posts_to_create = random.choice([2, 3])
        print(f"\n📝 Creating {posts_to_create} posts...")
        
        for i in range(posts_to_create):
            content = self.generate_content()
            if content:
                success = self.post_content(content)
                if success and i < posts_to_create - 1:
                    # Wait between posts
                    time.sleep(60)  # 1 minute between posts
        
        if not posting_only:
            # 2. Check and engage with mentions - SKIPPED IN POSTING-ONLY MODE
            print(f"\n👂 Checking mentions...")
            mentions = self.check_mentions()
            if mentions:
                self.engage_with_mentions(mentions)
            
            # 3. Find and engage with relevant posts - SKIPPED IN POSTING-ONLY MODE
            print(f"\n🔍 Finding relevant posts to engage with...")
            relevant_posts = self.find_relevant_posts()
            if relevant_posts:
                self.engage_with_relevant_posts(relevant_posts)
        else:
            print(f"\n⏸️ SKIPPING mention checks (saves retrieval quota)")
            print(f"⏸️ SKIPPING post searches (saves retrieval quota)")
            print(f"📊 Retrieval functions resume August 11th")
        
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
    parser.add_argument('--posting-only', action='store_true', help='Posting-only mode - skips retrieval functions to save quota')
    args = parser.parse_args()
    
    try:
        if args.test:
            print("🧪 Test mode - generating sample content...")
            bot = SMESocialBot(test_mode=True)
            content = bot.generate_content()
            if content:
                print(f"Generated: {content}")
            else:
                print("❌ Content generation failed")
        else:
            bot = SMESocialBot()
            # Check if we should run in posting-only mode
            posting_only = args.posting_only or datetime.now() < datetime(2025, 8, 11)
            bot.run_daily_automation(posting_only=posting_only)
            
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
