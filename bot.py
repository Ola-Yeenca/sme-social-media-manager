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
import groq
from config import Config
from viral_predictor import ViralTweetPredictor, ViralScore
from linkedin_manager import LinkedInManager


class SMESocialBot:
    """Simple social media bot that actually works"""
    
    def __init__(self, test_mode=False, multi_platform=True):
        """Initialize the bot with API connections"""
        self.config = Config()
        self.test_mode = test_mode
        self.multi_platform = multi_platform
        
        if not test_mode:
            self.setup_twitter()
            if multi_platform:
                self.setup_linkedin()
        else:
            print("🧪 Test mode - skipping API connections")
            
        self.setup_ai()
        
        # Initialize viral predictor
        self.viral_predictor = ViralTweetPredictor()
        print("✅ Viral prediction system initialized")
        
        # Simple tracking
        self.session_stats = {
            'posts_created': 0,
            'linkedin_posts': 0,
            'mentions_checked': 0,
            'engagements_made': 0,
            'errors': 0,
            'viral_predictions': 0
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
    
    def setup_linkedin(self):
        """Setup LinkedIn API connection"""
        try:
            if self.config.linkedin_access_token:
                self.linkedin = LinkedInManager(
                    access_token=self.config.linkedin_access_token,
                    organization_id=getattr(self.config, 'linkedin_organization_id', None)
                )
                print("✅ LinkedIn API client initialized")
            else:
                print("⚠️ LinkedIn token not found - LinkedIn posting disabled")
                self.linkedin = None
                
        except Exception as e:
            print(f"⚠️ LinkedIn setup failed: {e}")
            self.linkedin = None
            
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
                self.grok_client = groq.Groq(api_key=self.config.grok_api_key)
                print("✅ Grok configured (will test on first use)")
                self.ai_provider = 'grok'
                return
            except Exception as e:
                print(f"⚠️ Grok setup failed: {e}")
        
        print("❌ No working AI provider available")
        sys.exit(1)
    
    def generate_content(self) -> str:
        """Generate social media content using dynamic data sources"""
        
        # Try dynamic content generation first
        try:
            from dynamic_content import DynamicContentEngine
            engine = DynamicContentEngine()
            
            # Generate dynamic content from real sources
            dynamic_content = engine.generate_dynamic_content()
            
            # If we got good dynamic content, use it directly
            if dynamic_content and len(dynamic_content) > 50:
                print("🎯 Using dynamic real-time content")
                return dynamic_content
                
        except Exception as e:
            print(f"⚠️ Dynamic content generation failed: {e}")
        
        # Fallback to AI generation with better prompts
        business_context = """
        You are the head of data analytics at SME Analytica, a cutting-edge restaurant tech company.
        You're passionate about data, obsessed with helping restaurants thrive, and you speak like a tech founder.
        Be specific, use real numbers, share insider knowledge. You're building the future of restaurant analytics.
        Sometimes contrarian, always data-driven. Mix technical insights with business impact.
        """
        
        # Import advanced content generator for better prompts
        try:
            from content_generator import get_dynamic_content_prompt
            prompt = get_dynamic_content_prompt()
        except:
            # Ultimate fallback
            prompt = "Write a data-driven insight about restaurant analytics. Be specific, technical, and engaging. Under 280 chars."
        
        try:
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
                        self.grok_client = groq.Groq(api_key=self.config.grok_api_key)
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
        """Post content to Twitter with viral prediction"""
        try:
            if not content:
                return False
            
            # Predict viral potential before posting
            viral_score = self.viral_predictor.predict_viral_potential(content)
            self.session_stats['viral_predictions'] += 1
            
            print(f"\n📊 Viral Prediction Score: {viral_score.total_score}/100")
            print(f"   Predicted Likes: {viral_score.predicted_engagement['likes']}")
            print(f"   Predicted Retweets: {viral_score.predicted_engagement['retweets']}")
            print(f"   Confidence: {viral_score.confidence}%")
            
            # If score is low, try to optimize
            if viral_score.total_score < 70:
                print("🔧 Score below 70, optimizing tweet...")
                optimized_content, new_score = self.viral_predictor.optimize_tweet(content)
                if new_score.total_score > viral_score.total_score:
                    print(f"✨ Optimization improved score: {viral_score.total_score} → {new_score.total_score}")
                    content = optimized_content
                    viral_score = new_score
            
            # Show recommendations if any
            if viral_score.recommendations:
                print("💡 Recommendations for next time:")
                for rec in viral_score.recommendations[:3]:
                    print(f"   - {rec}")
            
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
                print(f"   Viral Score: {viral_score.total_score}/100")
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
    
    def generate_viral_content(self, base_idea: str = None) -> List[tuple]:
        """Generate multiple viral tweet variations"""
        if not base_idea:
            base_idea = "SME Analytica helps restaurants increase revenue with data-driven insights"
        
        print("\n🚀 Generating viral tweet variations...")
        variations = self.viral_predictor.generate_viral_variations(base_idea, count=3)
        
        print(f"\n📊 Generated {len(variations)} viral variations:")
        for i, (tweet, score) in enumerate(variations, 1):
            print(f"\nVariation {i} (Score: {score.total_score}/100):")
            print(f"   {tweet[:100]}..." if len(tweet) > 100 else f"   {tweet}")
            print(f"   Predicted: {score.predicted_engagement['likes']} likes, {score.predicted_engagement['retweets']} RTs")
        
        return variations
    
    def post_best_viral_content(self, multi_platform=False) -> bool:
        """Generate viral variations and post the best one"""
        try:
            # Generate base content first
            base_content = self.generate_content()
            
            # Generate viral variations
            variations = self.generate_viral_content(base_content)
            
            if variations:
                # Post the best one (first in sorted list)
                best_tweet, best_score = variations[0]
                print(f"\n🎯 Posting best variation with score {best_score.total_score}/100")
                return self.post_multi_platform(best_tweet) if multi_platform else self.post_content(best_tweet)
            else:
                # Fallback to regular posting
                return self.post_multi_platform(base_content) if multi_platform else self.post_content(base_content)
                
        except Exception as e:
            print(f"❌ Viral content generation failed: {e}")
            # Fallback to regular content
            content = self.generate_content()
            return self.post_multi_platform(content) if multi_platform else self.post_content(content)
    
    def post_multi_platform(self, content: str) -> bool:
        """Post content to both Twitter and LinkedIn"""
        twitter_success = False
        linkedin_success = False
        
        # Post to Twitter
        print("\n🐦 Posting to Twitter...")
        twitter_success = self.post_content(content)
        
        # Post to LinkedIn if configured
        if self.linkedin and hasattr(self, 'linkedin'):
            print("\n🔗 Posting to LinkedIn...")
            try:
                linkedin_success, response = self.linkedin.post_to_linkedin(content, optimize_viral=True)
                if linkedin_success:
                    self.session_stats['linkedin_posts'] += 1
                else:
                    print(f"   LinkedIn error: {response.get('error', 'Unknown error')}")
            except Exception as e:
                print(f"   LinkedIn posting failed: {e}")
        else:
            print("\n⚠️ LinkedIn not configured - skipping LinkedIn post")
        
        return twitter_success or linkedin_success
    
    def check_mentions(self, days_back: int = 1) -> List[Dict]:
        """Check for mentions and replies with configurable lookback period"""
        try:
            # Check if we're rate limited
            if hasattr(self, 'rate_limited') and self.rate_limited:
                print("🚀 [SIMULATION] Would check mentions...")
                # Simulate finding mentions based on days back
                simulated_mentions = [
                    {'id': '123456', 'text': '@smeanalytica Love your restaurant analytics insights!', 'author_id': 'user1'},
                    {'id': '123457', 'text': '@smeanalytica Can you help with dynamic pricing?', 'author_id': 'user2'},
                    {'id': '123458', 'text': '@smeanalytica Interesting data on profit margins!', 'author_id': 'user3'},
                ]
                # More mentions for weekly mode
                if days_back > 1:
                    simulated_mentions.extend([
                        {'id': '123459', 'text': '@smeanalytica How do you handle seasonal pricing?', 'author_id': 'user4'},
                        {'id': '123460', 'text': '@smeanalytica Great insights on menu optimization!', 'author_id': 'user5'}
                    ])
                
                print(f"✅ [SIMULATION] Found {len(simulated_mentions)} mentions from last {days_back} days")
                return simulated_mentions
            
            # Get mentions from specified time period
            since_time = datetime.now() - timedelta(days=days_back)
            
            mentions = self.twitter.get_users_mentions(
                id=self.twitter.get_me().data.id,
                max_results=min(100, days_back * 10),  # More results for longer periods
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
            print(f"✅ Found {len(mention_list)} mentions from last {days_back} days")
            return mention_list
            
        except Exception as e:
            if "Rate limit exceeded" in str(e):
                print("⚠️ Hit rate limit checking mentions, switching to simulation...")
                self.rate_limited = True
                return self.check_mentions(days_back)  # Retry in simulation mode
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
                        self.grok_client = groq.Groq(api_key=self.config.grok_api_key)
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
    
    def run_daily_automation(self, posting_only=False, weekly_engagement=False, multi_platform=True):
        """Run the complete daily automation sequence"""
        print(f"\n🤖 Starting SME Social Media Bot")
        print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print(f"🌍 Platforms: {'Twitter + LinkedIn' if multi_platform and self.linkedin else 'Twitter only'}")
        
        mode_description = "WEEKLY FULL ENGAGEMENT" if weekly_engagement else ("POSTING-ONLY" if posting_only else "FULL AUTOMATION")
        print(f"💯 Mode: {mode_description}")
        
        if posting_only and not weekly_engagement:
            print("🔒 API retrieval quota management active")
            print("📅 Full engagement available on Sundays or after Aug 11th")
        
        print("=" * 50)
        
        # Skip initial API check - handle rate limits gracefully during operations
        print("🚀 Starting bot operations...")
        self.rate_limited = False  # Start optimistically
        
        # 1. Generate and post ONE unique content piece - Natural posting frequency
        print(f"\n📝 Creating one dynamic post with viral optimization...")
        
        # Always use viral prediction for single post
        print("\n🎯 Using viral prediction and dynamic content generation...")
        success = self.post_best_viral_content(multi_platform=multi_platform)
        
        if not posting_only or weekly_engagement:
            # 2. Check and engage with mentions
            days_back = 7 if weekly_engagement else 1
            print(f"\n👂 Checking mentions from last {days_back} days...")
            mentions = self.check_mentions(days_back=days_back)
            if mentions:
                self.engage_with_mentions(mentions)
            
            # 3. Find and engage with relevant posts (only if not weekly mode to avoid overuse)
            if not weekly_engagement:
                print(f"\n🔍 Finding relevant posts to engage with...")
                relevant_posts = self.find_relevant_posts()
                if relevant_posts:
                    self.engage_with_relevant_posts(relevant_posts)
            else:
                print(f"\n⏭️ Skipping post search in weekly mode (focus on mentions)")
        else:
            print(f"\n⏸️ SKIPPING mention checks (saves retrieval quota)")
            print(f"⏸️ SKIPPING post searches (saves retrieval quota)")
            print(f"📊 Full engagement available on Sundays")
        
        # 4. Show results
        print(f"\n📊 Session Results:")
        print(f"  Posts created: {self.session_stats['posts_created']}")
        if multi_platform and self.linkedin:
            print(f"  LinkedIn posts: {self.session_stats['linkedin_posts']}")
        print(f"  Viral predictions: {self.session_stats['viral_predictions']}")
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
    parser.add_argument('--weekly-engagement', action='store_true', help='Weekly full engagement mode - processes mentions from past 7 days')
    parser.add_argument('--multi-platform', action='store_true', default=True, help='Post to both Twitter and LinkedIn')
    parser.add_argument('--viral-test', action='store_true', help='Test viral prediction system')
    parser.add_argument('--viral-analyze', type=str, help='Analyze viral potential of a specific tweet')
    args = parser.parse_args()
    
    try:
        if args.viral_test:
            print("🧪 Testing Viral Prediction System...")
            from viral_predictor import ViralTweetPredictor
            predictor = ViralTweetPredictor()
            
            test_tweets = [
                "Just launched our new analytics dashboard for SMEs!",
                "🚀 Game-changer: AI-powered analytics that boost revenue by 47% on average. Who's ready to transform their business? #AI #Business #Growth",
                "Unpopular opinion: Most businesses waste 80% of their data. Here's how to fix it: 🧵"
            ]
            
            for tweet in test_tweets:
                print(f"\n📝 Tweet: {tweet[:80]}...")
                score = predictor.predict_viral_potential(tweet)
                print(f"📊 Viral Score: {score.total_score}/100")
                print(f"👍 Predicted: {score.predicted_engagement['likes']} likes, {score.predicted_engagement['retweets']} RTs")
                
        elif args.viral_analyze:
            print(f"🔬 Analyzing viral potential...")
            from viral_predictor import ViralTweetPredictor
            predictor = ViralTweetPredictor()
            score = predictor.predict_viral_potential(args.viral_analyze)
            
            print(f"\n📊 Viral Score: {score.total_score}/100")
            print(f"\nBreakdown:")
            print(f"  Content: {score.content_score}/100")
            print(f"  Timing: {score.timing_score}/100")
            print(f"  Hashtags: {score.hashtag_score}/100")
            print(f"  Engagement: {score.engagement_score}/100")
            print(f"  Trends: {score.trend_score}/100")
            print(f"\nPredicted Engagement:")
            print(f"  Likes: {score.predicted_engagement['likes']}")
            print(f"  Retweets: {score.predicted_engagement['retweets']}")
            print(f"  Replies: {score.predicted_engagement['replies']}")
            print(f"  Impressions: {score.predicted_engagement['impressions']}")
            
            if score.recommendations:
                print(f"\n💡 Recommendations:")
                for rec in score.recommendations:
                    print(f"  - {rec}")
                    
        elif args.test:
            print("🧪 Test mode - generating sample content...")
            bot = SMESocialBot(test_mode=True)
            content = bot.generate_content()
            if content:
                print(f"Generated: {content}")
            else:
                print("❌ Content generation failed")
        else:
            bot = SMESocialBot(multi_platform=args.multi_platform)
            
            # Determine mode
            if args.weekly_engagement:
                print("📅 Weekly engagement mode - processing all mentions from past week")
                bot.run_daily_automation(posting_only=False, weekly_engagement=True, multi_platform=args.multi_platform)
            else:
                # Check if we should run in posting-only mode (until Aug 11 or manual override)
                posting_only = args.posting_only or datetime.now() < datetime(2025, 8, 11)
                bot.run_daily_automation(posting_only=posting_only, multi_platform=args.multi_platform)
            
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
