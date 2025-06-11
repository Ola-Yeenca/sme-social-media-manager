#!/usr/bin/env python3
"""
Advanced Analytics and Performance Tracking for SME Analytica
Tracks growth metrics, engagement rates, and optimization opportunities
"""

import os
import sys
import asyncio
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

# Unset the shell environment variable to use .env file
if 'SOCIAL_MEDIA_DB_ID' in os.environ:
    del os.environ['SOCIAL_MEDIA_DB_ID']

class AdvancedAnalytics:
    """Advanced analytics and performance tracking"""
    
    def __init__(self):
        self.metrics_to_track = [
            'follower_count', 'following_count', 'tweet_count',
            'likes_received', 'retweets_received', 'replies_received',
            'impressions', 'engagement_rate', 'reach'
        ]
        
        self.content_performance_metrics = [
            'likes_per_post', 'retweets_per_post', 'replies_per_post',
            'engagement_rate_by_type', 'best_posting_times', 'top_hashtags'
        ]

    async def collect_account_metrics(self):
        """Collect comprehensive account metrics"""
        
        print("📊 Collecting Account Metrics")
        print("-" * 40)
        
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
            
            # Get account info with metrics
            user = client.get_me(user_fields=['public_metrics', 'created_at'])
            
            if user and user.data:
                metrics = user.data.public_metrics
                
                account_data = {
                    'timestamp': datetime.now().isoformat(),
                    'username': user.data.username,
                    'followers_count': metrics['followers_count'],
                    'following_count': metrics['following_count'],
                    'tweet_count': metrics['tweet_count'],
                    'listed_count': metrics['listed_count'],
                    'account_age_days': (datetime.now() - user.data.created_at.replace(tzinfo=None)).days
                }
                
                print(f"👤 Account: @{account_data['username']}")
                print(f"👥 Followers: {account_data['followers_count']}")
                print(f"📝 Tweets: {account_data['tweet_count']}")
                print(f"📅 Account Age: {account_data['account_age_days']} days")
                
                # Calculate growth rates if we have historical data
                growth_metrics = await self.calculate_growth_rates(account_data)
                account_data.update(growth_metrics)
                
                # Save metrics to file
                await self.save_metrics(account_data, 'account_metrics')
                
                return account_data
            
        except Exception as e:
            print(f"❌ Error collecting account metrics: {e}")
            return None

    async def analyze_content_performance(self):
        """Analyze performance of recent content"""
        
        print("\n📈 Analyzing Content Performance")
        print("-" * 40)
        
        try:
            import tweepy
            from config.settings import settings
            from notion import NotionManager
            
            # Initialize clients
            twitter_client = tweepy.Client(bearer_token=settings.twitter_bearer_token)
            notion_manager = NotionManager()
            
            # Get published posts from Notion
            published_posts = notion_manager.get_posts_by_status("Published", limit=50)
            
            if not published_posts:
                print("📭 No published posts found for analysis")
                return None
            
            print(f"📊 Analyzing {len(published_posts)} published posts")
            
            content_analytics = {
                'total_posts': len(published_posts),
                'posts_analyzed': 0,
                'total_engagement': 0,
                'avg_engagement_rate': 0,
                'best_performing_post': None,
                'worst_performing_post': None,
                'content_type_performance': {},
                'hashtag_performance': {},
                'posting_time_performance': {}
            }
            
            post_performances = []
            
            for post in published_posts:
                if hasattr(post, 'tweet_id') and post.tweet_id:
                    try:
                        # Get tweet metrics
                        tweet = twitter_client.get_tweet(
                            post.tweet_id,
                            tweet_fields=['public_metrics', 'created_at']
                        )
                        
                        if tweet.data:
                            metrics = tweet.data.public_metrics
                            
                            engagement = metrics['like_count'] + metrics['retweet_count'] + metrics['reply_count']
                            
                            post_performance = {
                                'post_id': post.id,
                                'tweet_id': post.tweet_id,
                                'content': post.content[:100],
                                'likes': metrics['like_count'],
                                'retweets': metrics['retweet_count'],
                                'replies': metrics['reply_count'],
                                'total_engagement': engagement,
                                'impressions': metrics.get('impression_count', 0),
                                'content_theme': getattr(post, 'content_theme', 'unknown'),
                                'post_type': getattr(post, 'post_type', 'unknown'),
                                'hashtags': getattr(post, 'tags', []),
                                'posted_time': tweet.data.created_at
                            }
                            
                            post_performances.append(post_performance)
                            content_analytics['posts_analyzed'] += 1
                            content_analytics['total_engagement'] += engagement
                            
                            print(f"   📝 Post: {post.content[:30]}... | Engagement: {engagement}")
                            
                    except Exception as e:
                        print(f"   ⚠️ Error analyzing tweet {post.tweet_id}: {e}")
            
            if post_performances:
                # Calculate analytics
                content_analytics['avg_engagement_rate'] = content_analytics['total_engagement'] / len(post_performances)
                
                # Find best and worst performing posts
                best_post = max(post_performances, key=lambda x: x['total_engagement'])
                worst_post = min(post_performances, key=lambda x: x['total_engagement'])
                
                content_analytics['best_performing_post'] = {
                    'content': best_post['content'],
                    'engagement': best_post['total_engagement'],
                    'tweet_url': f"https://twitter.com/smeanalytica/status/{best_post['tweet_id']}"
                }
                
                content_analytics['worst_performing_post'] = {
                    'content': worst_post['content'],
                    'engagement': worst_post['total_engagement']
                }
                
                # Analyze content type performance
                content_type_performance = {}
                for post in post_performances:
                    content_type = post['content_theme']
                    if content_type not in content_type_performance:
                        content_type_performance[content_type] = {'total_engagement': 0, 'count': 0}
                    
                    content_type_performance[content_type]['total_engagement'] += post['total_engagement']
                    content_type_performance[content_type]['count'] += 1
                
                # Calculate averages
                for content_type in content_type_performance:
                    data = content_type_performance[content_type]
                    data['avg_engagement'] = data['total_engagement'] / data['count']
                
                content_analytics['content_type_performance'] = content_type_performance
                
                # Analyze posting time performance
                time_performance = {}
                for post in post_performances:
                    hour = post['posted_time'].hour
                    if hour not in time_performance:
                        time_performance[hour] = {'total_engagement': 0, 'count': 0}
                    
                    time_performance[hour]['total_engagement'] += post['total_engagement']
                    time_performance[hour]['count'] += 1
                
                # Calculate averages
                for hour in time_performance:
                    data = time_performance[hour]
                    data['avg_engagement'] = data['total_engagement'] / data['count']
                
                content_analytics['posting_time_performance'] = time_performance
                
                # Save analytics
                await self.save_metrics(content_analytics, 'content_performance')
                
                # Print insights
                print(f"\n📊 Content Performance Insights:")
                print(f"   • Average engagement per post: {content_analytics['avg_engagement_rate']:.1f}")
                print(f"   • Best performing post: {best_post['total_engagement']} engagement")
                print(f"   • Best content type: {max(content_type_performance.items(), key=lambda x: x[1]['avg_engagement'])[0]}")
                
                # Find best posting time
                if time_performance:
                    best_hour = max(time_performance.items(), key=lambda x: x[1]['avg_engagement'])
                    print(f"   • Best posting time: {best_hour[0]:02d}:00 ({best_hour[1]['avg_engagement']:.1f} avg engagement)")
                
                return content_analytics
            
        except Exception as e:
            print(f"❌ Error analyzing content performance: {e}")
            return None

    async def calculate_growth_rates(self, current_metrics):
        """Calculate growth rates compared to historical data"""
        
        try:
            # Load historical data
            historical_data = await self.load_historical_metrics('account_metrics')
            
            if not historical_data:
                return {'growth_rate_followers': 0, 'growth_rate_tweets': 0}
            
            # Get last week's data
            last_week = datetime.now() - timedelta(days=7)
            last_week_data = None
            
            for record in reversed(historical_data):
                record_date = datetime.fromisoformat(record['timestamp'])
                if record_date <= last_week:
                    last_week_data = record
                    break
            
            if last_week_data:
                # Calculate growth rates
                follower_growth = ((current_metrics['followers_count'] - last_week_data['followers_count']) / 
                                 max(last_week_data['followers_count'], 1)) * 100
                
                tweet_growth = ((current_metrics['tweet_count'] - last_week_data['tweet_count']) / 
                              max(last_week_data['tweet_count'], 1)) * 100
                
                return {
                    'growth_rate_followers_7d': round(follower_growth, 2),
                    'growth_rate_tweets_7d': round(tweet_growth, 2),
                    'followers_gained_7d': current_metrics['followers_count'] - last_week_data['followers_count']
                }
            
        except Exception as e:
            print(f"⚠️ Error calculating growth rates: {e}")
        
        return {'growth_rate_followers_7d': 0, 'growth_rate_tweets_7d': 0, 'followers_gained_7d': 0}

    async def generate_insights_report(self):
        """Generate actionable insights report"""
        
        print("\n🔍 Generating Insights Report")
        print("-" * 40)
        
        try:
            # Load recent analytics data
            account_metrics = await self.load_historical_metrics('account_metrics')
            content_performance = await self.load_historical_metrics('content_performance')
            
            insights = {
                'timestamp': datetime.now().isoformat(),
                'recommendations': [],
                'growth_opportunities': [],
                'content_optimization': [],
                'engagement_strategies': []
            }
            
            # Analyze account growth
            if account_metrics and len(account_metrics) > 0:
                latest_metrics = account_metrics[-1]
                
                if latest_metrics.get('growth_rate_followers_7d', 0) < 5:
                    insights['growth_opportunities'].append(
                        "Follower growth is below 5% weekly. Consider increasing engagement activities and following relevant accounts."
                    )
                
                if latest_metrics.get('followers_count', 0) < 100:
                    insights['growth_opportunities'].append(
                        "Focus on reaching 100 followers milestone. Increase posting frequency and engage with industry conversations."
                    )
            
            # Analyze content performance
            if content_performance and len(content_performance) > 0:
                latest_content = content_performance[-1]
                
                if latest_content.get('avg_engagement_rate', 0) < 5:
                    insights['content_optimization'].append(
                        "Average engagement rate is low. Try more interactive content like polls and questions."
                    )
                
                # Best content type recommendations
                content_types = latest_content.get('content_type_performance', {})
                if content_types:
                    best_type = max(content_types.items(), key=lambda x: x[1].get('avg_engagement', 0))
                    insights['content_optimization'].append(
                        f"'{best_type[0]}' content performs best. Consider creating more of this type."
                    )
                
                # Best posting time recommendations
                time_performance = latest_content.get('posting_time_performance', {})
                if time_performance:
                    best_times = sorted(time_performance.items(), key=lambda x: x[1].get('avg_engagement', 0), reverse=True)[:3]
                    best_hours = [f"{hour:02d}:00" for hour, _ in best_times]
                    insights['content_optimization'].append(
                        f"Best posting times: {', '.join(best_hours)}. Schedule more content during these hours."
                    )
            
            # General engagement strategies
            insights['engagement_strategies'].extend([
                "Respond to all mentions and comments within 2 hours",
                "Share behind-the-scenes content about SME Analytica development",
                "Create weekly Twitter threads about business analytics topics",
                "Engage with 10-15 relevant tweets daily in your industry",
                "Use trending hashtags when relevant to your content"
            ])
            
            # Save insights
            await self.save_metrics(insights, 'insights_report')
            
            # Print report
            print("📋 Insights Report Generated:")
            
            if insights['growth_opportunities']:
                print("\n🚀 Growth Opportunities:")
                for opportunity in insights['growth_opportunities']:
                    print(f"   • {opportunity}")
            
            if insights['content_optimization']:
                print("\n📈 Content Optimization:")
                for optimization in insights['content_optimization']:
                    print(f"   • {optimization}")
            
            if insights['engagement_strategies']:
                print("\n💬 Engagement Strategies:")
                for strategy in insights['engagement_strategies'][:3]:  # Show top 3
                    print(f"   • {strategy}")
            
            return insights
            
        except Exception as e:
            print(f"❌ Error generating insights: {e}")
            return None

    async def save_metrics(self, data, metric_type):
        """Save metrics to JSON file"""
        
        try:
            os.makedirs('analytics_data', exist_ok=True)
            filename = f'analytics_data/{metric_type}.json'
            
            # Load existing data
            existing_data = []
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    existing_data = json.load(f)
            
            # Append new data
            existing_data.append(data)
            
            # Keep only last 100 records
            if len(existing_data) > 100:
                existing_data = existing_data[-100:]
            
            # Save updated data
            with open(filename, 'w') as f:
                json.dump(existing_data, f, indent=2, default=str)
            
            print(f"💾 Saved {metric_type} metrics")
            
        except Exception as e:
            print(f"❌ Error saving metrics: {e}")

    async def load_historical_metrics(self, metric_type):
        """Load historical metrics from JSON file"""
        
        try:
            filename = f'analytics_data/{metric_type}.json'
            
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    return json.load(f)
            
        except Exception as e:
            print(f"⚠️ Error loading historical metrics: {e}")
        
        return []


async def run_advanced_analytics():
    """Run comprehensive analytics suite"""
    
    print("📊 SME Analytica Advanced Analytics")
    print("=" * 60)
    print(f"🕐 Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    analytics = AdvancedAnalytics()
    
    # Run analytics
    results = {}
    
    # Collect account metrics
    account_data = await analytics.collect_account_metrics()
    results['account_metrics'] = account_data is not None
    
    # Analyze content performance
    content_data = await analytics.analyze_content_performance()
    results['content_analysis'] = content_data is not None
    
    # Generate insights
    insights = await analytics.generate_insights_report()
    results['insights_generated'] = insights is not None
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Analytics Summary:")
    for analysis, success in results.items():
        status = "✅ Complete" if success else "❌ Failed"
        print(f"   • {analysis.replace('_', ' ').title()}: {status}")
    
    print(f"\n💾 Data saved to: ./analytics_data/")
    print(f"🕐 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return results


if __name__ == "__main__":
    asyncio.run(run_advanced_analytics())
