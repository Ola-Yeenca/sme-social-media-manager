#!/usr/bin/env python3
"""
Growth Automation for SME Analytica
Implements engagement tactics, follower growth, and community building
"""

import os
import sys
import asyncio
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

# Unset the shell environment variable to use .env file
if 'SOCIAL_MEDIA_DB_ID' in os.environ:
    del os.environ['SOCIAL_MEDIA_DB_ID']

class GrowthAutomation:
    """Automated growth and engagement strategies"""
    
    def __init__(self):
        self.target_keywords = [
            "restaurant analytics", "small business", "business intelligence",
            "restaurant tech", "hospitality analytics", "menu optimization",
            "dynamic pricing", "business data", "restaurant management",
            "small business owner", "entrepreneur", "startup", "business growth"
        ]
        
        self.target_accounts = [
            # Restaurant industry accounts
            "@RestaurantOwner", "@ChefsTalk", "@HospitalityNet",
            "@RestaurantNews", "@FoodServiceDir", "@QSRMagazine",
            # Small business accounts  
            "@SmallBizTrends", "@SCORE", "@SBAGov", "@EntMagazine",
            "@SmallBusiness", "@StartupGrind", "@Entrepreneur",
            # Analytics and tech accounts
            "@BusinessIntel", "@DataScience", "@TechCrunch", "@VentureBeat"
        ]
        
        self.engagement_responses = {
            "analytics_question": [
                "Great question! Analytics can definitely help with that. Have you considered tracking customer behavior patterns?",
                "This is exactly what we help restaurants solve! Dynamic pricing based on demand can increase revenue by 15-25%.",
                "Data-driven decisions are game changers! What specific metrics are you currently tracking?",
                "Love seeing business owners thinking analytically! Have you tried segmenting your customer data?"
            ],
            "business_challenge": [
                "Many restaurant owners face this challenge! Analytics can provide insights to optimize operations.",
                "This is a common pain point. Have you considered using predictive analytics to forecast demand?",
                "Great point! Data visualization can make complex business metrics much easier to understand.",
                "Exactly why we built SME Analytica! Small businesses need enterprise-level analytics made simple."
            ],
            "success_celebration": [
                "Congratulations! 🎉 Data-driven decisions really pay off. What metrics helped you achieve this?",
                "Amazing results! 🚀 This is exactly why we're passionate about analytics for small businesses.",
                "Love seeing success stories! 📈 Analytics-driven growth is the future of small business.",
                "Fantastic! 🎯 Would love to hear more about your data strategy that led to this success."
            ]
        }

    async def monitor_mentions(self):
        """Monitor and respond to mentions"""
        
        print("👂 Monitoring Mentions and Engagement Opportunities")
        print("-" * 50)
        
        try:
            import tweepy
            from config.settings import settings
            
            # Initialize Twitter client
            client = tweepy.Client(
                bearer_token=settings.twitter_bearer_token,
                consumer_key=settings.twitter_api_key,
                consumer_secret=settings.twitter_api_secret,
                access_token=settings.twitter_access_token,
                access_token_secret=settings.twitter_access_token_secret,
                wait_on_rate_limit=True
            )
            
            # Get mentions
            mentions = client.get_mentions(max_results=10)
            
            if mentions.data:
                print(f"📬 Found {len(mentions.data)} mentions")
                
                for mention in mentions.data:
                    print(f"📝 Mention: {mention.text[:50]}...")
                    
                    # Generate appropriate response
                    response = self.generate_mention_response(mention.text)
                    
                    if response:
                        print(f"💬 Response: {response[:50]}...")
                        
                        # Reply to mention (commented out for safety)
                        # client.create_tweet(text=response, in_reply_to_tweet_id=mention.id)
                        print("   ✅ (Response ready - enable in production)")
            else:
                print("📭 No new mentions found")
            
            return True
            
        except Exception as e:
            print(f"❌ Error monitoring mentions: {e}")
            return False

    def generate_mention_response(self, mention_text):
        """Generate appropriate response to mentions"""
        
        mention_lower = mention_text.lower()
        
        if any(word in mention_lower for word in ["analytics", "data", "metrics"]):
            return random.choice(self.engagement_responses["analytics_question"])
        elif any(word in mention_lower for word in ["challenge", "problem", "difficult", "struggle"]):
            return random.choice(self.engagement_responses["business_challenge"])
        elif any(word in mention_lower for word in ["success", "growth", "increased", "improved"]):
            return random.choice(self.engagement_responses["success_celebration"])
        else:
            return "Thanks for the mention! 🙏 Always happy to discuss business analytics and growth strategies."

    async def engage_with_target_content(self):
        """Find and engage with relevant content"""
        
        print("\n🎯 Engaging with Target Content")
        print("-" * 50)
        
        try:
            import tweepy
            from config.settings import settings
            
            client = tweepy.Client(
                bearer_token=settings.twitter_bearer_token,
                consumer_key=settings.twitter_api_key,
                consumer_secret=settings.twitter_api_secret,
                access_token=settings.twitter_access_token,
                access_token_secret=settings.twitter_access_token_secret,
                wait_on_rate_limit=True
            )
            
            engagement_count = 0
            
            # Search for relevant tweets
            for keyword in random.sample(self.target_keywords, 3):  # Sample 3 keywords
                print(f"🔍 Searching for: '{keyword}'")
                
                try:
                    tweets = client.search_recent_tweets(
                        query=f'"{keyword}" -is:retweet lang:en',
                        max_results=10,
                        tweet_fields=['author_id', 'public_metrics']
                    )
                    
                    if tweets.data:
                        for tweet in tweets.data[:2]:  # Engage with top 2 tweets
                            # Check if tweet has good engagement potential
                            metrics = tweet.public_metrics
                            if metrics['like_count'] > 5 and metrics['retweet_count'] > 1:
                                print(f"   💖 Liking tweet: {tweet.text[:40]}...")
                                
                                # Like the tweet (commented out for safety)
                                # client.like(tweet.id)
                                print("   ✅ (Like ready - enable in production)")
                                
                                engagement_count += 1
                                
                                # Occasionally retweet with comment
                                if random.random() < 0.3:  # 30% chance
                                    comment = self.generate_retweet_comment(tweet.text)
                                    print(f"   🔄 Retweet comment: {comment[:40]}...")
                                    # client.create_tweet(text=comment, quote_tweet_id=tweet.id)
                                    print("   ✅ (Retweet ready - enable in production)")
                    
                except Exception as e:
                    print(f"   ⚠️ Error searching '{keyword}': {e}")
            
            print(f"\n📊 Engagement Summary: {engagement_count} interactions planned")
            return engagement_count
            
        except Exception as e:
            print(f"❌ Error engaging with content: {e}")
            return 0

    def generate_retweet_comment(self, original_text):
        """Generate thoughtful comments for retweets"""
        
        comments = [
            "Exactly! This is why data-driven decision making is crucial for small businesses. 📊",
            "Great insight! We see this trend across many of our restaurant clients. 🍽️",
            "This aligns perfectly with what we're seeing in the analytics space. 📈",
            "Spot on! Small businesses that embrace analytics see 25%+ growth on average. 🚀",
            "Love this perspective! Data democratization is key for SME success. 💡"
        ]
        
        return random.choice(comments)

    async def follow_target_accounts(self):
        """Follow relevant accounts in target industries"""
        
        print("\n👥 Following Target Accounts")
        print("-" * 50)
        
        try:
            import tweepy
            from config.settings import settings
            
            client = tweepy.Client(
                bearer_token=settings.twitter_bearer_token,
                consumer_key=settings.twitter_api_key,
                consumer_secret=settings.twitter_api_secret,
                access_token=settings.twitter_access_token,
                access_token_secret=settings.twitter_access_token_secret,
                wait_on_rate_limit=True
            )
            
            # Get current following count to avoid hitting limits
            me = client.get_me(user_fields=['public_metrics'])
            current_following = me.data.public_metrics['following_count']
            
            print(f"📊 Currently following: {current_following} accounts")
            
            # Follow a few target accounts (limit to avoid spam)
            follow_limit = min(5, 100 - current_following)  # Conservative limit
            
            if follow_limit > 0:
                accounts_to_follow = random.sample(self.target_accounts, min(follow_limit, len(self.target_accounts)))
                
                for account in accounts_to_follow:
                    try:
                        # Get user info first
                        user = client.get_user(username=account.replace('@', ''))
                        
                        if user.data:
                            print(f"👤 Following: {account}")
                            # client.follow_user(user.data.id)
                            print("   ✅ (Follow ready - enable in production)")
                        
                    except Exception as e:
                        print(f"   ⚠️ Error following {account}: {e}")
            else:
                print("⚠️ Following limit reached for today")
            
            return True
            
        except Exception as e:
            print(f"❌ Error following accounts: {e}")
            return False

    async def analyze_trending_topics(self):
        """Analyze trending topics for content opportunities"""
        
        print("\n📈 Analyzing Trending Topics")
        print("-" * 50)
        
        try:
            import tweepy
            from config.settings import settings
            
            client = tweepy.Client(bearer_token=settings.twitter_bearer_token)
            
            # Get trending topics (requires location ID)
            # Using worldwide trends (WOEID: 1)
            trends = client.get_place_trends(id=1)
            
            if trends:
                business_related_trends = []
                
                for trend in trends[0]['trends'][:10]:  # Check top 10 trends
                    trend_name = trend['name'].lower()
                    
                    # Check if trend is business-related
                    if any(keyword in trend_name for keyword in ['business', 'restaurant', 'startup', 'entrepreneur', 'tech', 'ai', 'data']):
                        business_related_trends.append(trend['name'])
                
                if business_related_trends:
                    print(f"🔥 Business-related trends found:")
                    for trend in business_related_trends:
                        print(f"   • {trend}")
                        
                    # Generate content ideas based on trends
                    content_ideas = self.generate_trend_content(business_related_trends[0])
                    print(f"\n💡 Content idea: {content_ideas}")
                else:
                    print("📊 No business-related trends found in top 10")
            
            return True
            
        except Exception as e:
            print(f"❌ Error analyzing trends: {e}")
            return False

    def generate_trend_content(self, trend):
        """Generate content based on trending topics"""
        
        trend_templates = [
            f"🔥 {trend} is trending! Here's how small businesses can leverage this trend for growth...",
            f"📊 Seeing {trend} everywhere? Here's the data behind why this matters for restaurants...",
            f"💡 {trend} + Business Analytics = Growth Opportunity. Here's how to capitalize...",
            f"🚀 {trend} is more than just a trend - it's a business opportunity. Here's the analytics perspective..."
        ]
        
        return random.choice(trend_templates)


async def run_growth_automation():
    """Run the complete growth automation suite"""
    
    print("🚀 SME Analytica Growth Automation")
    print("=" * 60)
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    automation = GrowthAutomation()
    
    # Run all growth activities
    activities = [
        ("Monitor Mentions", automation.monitor_mentions),
        ("Engage with Content", automation.engage_with_target_content),
        ("Follow Target Accounts", automation.follow_target_accounts),
        ("Analyze Trends", automation.analyze_trending_topics)
    ]
    
    results = {}
    
    for activity_name, activity_func in activities:
        try:
            print(f"\n🎯 Running: {activity_name}")
            result = await activity_func()
            results[activity_name] = result
        except Exception as e:
            print(f"❌ Error in {activity_name}: {e}")
            results[activity_name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Growth Automation Summary:")
    for activity, result in results.items():
        status = "✅ Success" if result else "❌ Failed"
        print(f"   • {activity}: {status}")
    
    print(f"\n🕐 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return results


if __name__ == "__main__":
    asyncio.run(run_growth_automation())
