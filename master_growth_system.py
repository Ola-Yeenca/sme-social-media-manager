#!/usr/bin/env python3
"""
Master Growth System for SME Analytica
Orchestrates all growth activities for maximum impact
"""

import os
import sys
import asyncio
import schedule
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

# Unset the shell environment variable to use .env file
if 'SOCIAL_MEDIA_DB_ID' in os.environ:
    del os.environ['SOCIAL_MEDIA_DB_ID']

class MasterGrowthSystem:
    """Master orchestrator for all growth activities"""
    
    def __init__(self):
        self.growth_targets = {
            "week_1": {"followers": 25, "engagement_rate": 3.0, "posts_per_day": 6},
            "week_2": {"followers": 50, "engagement_rate": 4.0, "posts_per_day": 7},
            "week_3": {"followers": 100, "engagement_rate": 5.0, "posts_per_day": 8},
            "month_1": {"followers": 200, "engagement_rate": 6.0, "posts_per_day": 8},
            "month_2": {"followers": 500, "engagement_rate": 7.0, "posts_per_day": 10},
            "month_3": {"followers": 1000, "engagement_rate": 8.0, "posts_per_day": 12}
        }
        
        self.daily_schedule = {
            "07:00": "generate_morning_content",
            "09:00": "post_scheduled_content",
            "11:00": "engagement_activities",
            "13:00": "post_scheduled_content", 
            "15:00": "growth_activities",
            "17:00": "post_scheduled_content",
            "19:00": "evening_engagement",
            "21:00": "analytics_review"
        }

    async def run_morning_routine(self):
        """Morning content generation and planning"""
        
        print("🌅 Morning Growth Routine")
        print("=" * 50)
        
        try:
            # Import required modules
            from enhanced_content_strategy import generate_enhanced_daily_content
            from advanced_analytics import run_advanced_analytics
            
            # Generate enhanced daily content
            print("📝 Generating enhanced daily content...")
            posts_created = await generate_enhanced_daily_content()
            
            # Quick analytics check
            print("\n📊 Running morning analytics...")
            await run_advanced_analytics()
            
            print(f"\n✅ Morning routine complete: {posts_created} posts scheduled")
            return {"posts_created": posts_created, "analytics_run": True}
            
        except Exception as e:
            print(f"❌ Error in morning routine: {e}")
            return {"posts_created": 0, "analytics_run": False}

    async def run_engagement_burst(self):
        """Intensive engagement activities"""
        
        print("💬 Engagement Burst Activity")
        print("=" * 50)
        
        try:
            from growth_automation import GrowthAutomation
            
            automation = GrowthAutomation()
            
            # Run engagement activities
            activities = [
                automation.monitor_mentions(),
                automation.engage_with_target_content(),
                automation.analyze_trending_topics()
            ]
            
            results = await asyncio.gather(*activities, return_exceptions=True)
            
            success_count = sum(1 for r in results if r and not isinstance(r, Exception))
            
            print(f"✅ Engagement burst complete: {success_count}/3 activities successful")
            return {"engagement_activities": success_count}
            
        except Exception as e:
            print(f"❌ Error in engagement burst: {e}")
            return {"engagement_activities": 0}

    async def run_growth_sprint(self):
        """Focused growth activities"""
        
        print("🚀 Growth Sprint")
        print("=" * 50)
        
        try:
            from growth_automation import GrowthAutomation
            
            automation = GrowthAutomation()
            
            # Run growth-focused activities
            follow_result = await automation.follow_target_accounts()
            trend_result = await automation.analyze_trending_topics()
            
            print(f"✅ Growth sprint complete")
            return {"follow_activity": follow_result, "trend_analysis": trend_result}
            
        except Exception as e:
            print(f"❌ Error in growth sprint: {e}")
            return {"follow_activity": False, "trend_analysis": False}

    async def run_posting_cycle(self):
        """Post scheduled content and immediate engagement"""
        
        print("📤 Posting Cycle")
        print("=" * 50)
        
        try:
            from run_automation import check_and_post_scheduled_content
            
            # Post scheduled content
            posted_count = await check_and_post_scheduled_content()
            
            # If we posted something, do immediate engagement
            if posted_count > 0:
                print("🔄 Running immediate post-posting engagement...")
                await self.run_engagement_burst()
            
            print(f"✅ Posting cycle complete: {posted_count} posts published")
            return {"posts_published": posted_count}
            
        except Exception as e:
            print(f"❌ Error in posting cycle: {e}")
            return {"posts_published": 0}

    async def run_evening_review(self):
        """Evening analytics and planning"""
        
        print("🌙 Evening Review & Planning")
        print("=" * 50)
        
        try:
            from advanced_analytics import AdvancedAnalytics
            
            analytics = AdvancedAnalytics()
            
            # Comprehensive analytics
            account_metrics = await analytics.collect_account_metrics()
            content_performance = await analytics.analyze_content_performance()
            insights = await analytics.generate_insights_report()
            
            # Print daily summary
            if account_metrics:
                print(f"\n📊 Daily Summary:")
                print(f"   👥 Followers: {account_metrics['followers_count']}")
                print(f"   📈 Growth (7d): {account_metrics.get('growth_rate_followers_7d', 0)}%")
                print(f"   📝 Total Tweets: {account_metrics['tweet_count']}")
            
            if content_performance:
                print(f"   💬 Avg Engagement: {content_performance.get('avg_engagement_rate', 0):.1f}")
                print(f"   📊 Posts Analyzed: {content_performance.get('posts_analyzed', 0)}")
            
            print(f"✅ Evening review complete")
            return {"analytics_complete": True, "insights_generated": insights is not None}
            
        except Exception as e:
            print(f"❌ Error in evening review: {e}")
            return {"analytics_complete": False, "insights_generated": False}

    async def run_full_day_automation(self):
        """Run complete day automation cycle"""
        
        print("🚀 SME Analytica - Full Day Growth Automation")
        print("=" * 70)
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d')}")
        print(f"🕐 Started: {datetime.now().strftime('%H:%M:%S')}")
        
        daily_results = {
            "date": datetime.now().strftime('%Y-%m-%d'),
            "start_time": datetime.now().strftime('%H:%M:%S'),
            "activities": {}
        }
        
        # Morning routine
        print(f"\n{'='*20} MORNING ROUTINE {'='*20}")
        morning_results = await self.run_morning_routine()
        daily_results["activities"]["morning"] = morning_results
        
        # Midday posting and engagement
        print(f"\n{'='*20} MIDDAY ACTIVITIES {'='*20}")
        posting_results = await self.run_posting_cycle()
        daily_results["activities"]["midday_posting"] = posting_results
        
        # Afternoon growth activities
        print(f"\n{'='*20} AFTERNOON GROWTH {'='*20}")
        growth_results = await self.run_growth_sprint()
        daily_results["activities"]["afternoon_growth"] = growth_results
        
        # Evening posting
        print(f"\n{'='*20} EVENING POSTING {'='*20}")
        evening_posting = await self.run_posting_cycle()
        daily_results["activities"]["evening_posting"] = evening_posting
        
        # Evening review
        print(f"\n{'='*20} EVENING REVIEW {'='*20}")
        review_results = await self.run_evening_review()
        daily_results["activities"]["evening_review"] = review_results
        
        # Final summary
        daily_results["end_time"] = datetime.now().strftime('%H:%M:%S')
        
        print(f"\n{'='*70}")
        print("🎉 DAILY AUTOMATION COMPLETE!")
        print("=" * 70)
        
        # Calculate totals
        total_posts_created = morning_results.get("posts_created", 0)
        total_posts_published = (posting_results.get("posts_published", 0) + 
                               evening_posting.get("posts_published", 0))
        
        print(f"📊 Daily Summary:")
        print(f"   📝 Posts Created: {total_posts_created}")
        print(f"   📤 Posts Published: {total_posts_published}")
        print(f"   💬 Engagement Activities: Multiple cycles")
        print(f"   🚀 Growth Activities: Completed")
        print(f"   📈 Analytics: {'✅' if review_results.get('analytics_complete') else '❌'}")
        
        print(f"\n🕐 Total Runtime: {daily_results['start_time']} - {daily_results['end_time']}")
        print(f"🎯 Next automation: Tomorrow at 07:00")
        
        # Save daily results
        await self.save_daily_results(daily_results)
        
        return daily_results

    async def save_daily_results(self, results):
        """Save daily automation results"""
        
        try:
            import json
            
            os.makedirs('automation_logs', exist_ok=True)
            filename = f"automation_logs/daily_results_{results['date']}.json"
            
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            
            print(f"💾 Daily results saved to: {filename}")
            
        except Exception as e:
            print(f"⚠️ Error saving daily results: {e}")

    def setup_automated_schedule(self):
        """Setup automated daily schedule"""
        
        print("⏰ Setting up automated growth schedule...")
        
        # Schedule daily automation
        schedule.every().day.at("07:00").do(lambda: asyncio.run(self.run_full_day_automation()))
        
        # Schedule individual activities throughout the day
        schedule.every().day.at("09:00").do(lambda: asyncio.run(self.run_posting_cycle()))
        schedule.every().day.at("11:00").do(lambda: asyncio.run(self.run_engagement_burst()))
        schedule.every().day.at("13:00").do(lambda: asyncio.run(self.run_posting_cycle()))
        schedule.every().day.at("15:00").do(lambda: asyncio.run(self.run_growth_sprint()))
        schedule.every().day.at("17:00").do(lambda: asyncio.run(self.run_posting_cycle()))
        schedule.every().day.at("19:00").do(lambda: asyncio.run(self.run_engagement_burst()))
        schedule.every().day.at("21:00").do(lambda: asyncio.run(self.run_evening_review()))
        
        print("✅ Automated schedule configured!")
        print("\n📅 Daily Schedule:")
        print("   07:00 - Full day automation start")
        print("   09:00 - Morning posting cycle")
        print("   11:00 - Engagement burst")
        print("   13:00 - Lunch posting cycle")
        print("   15:00 - Growth sprint")
        print("   17:00 - Evening posting cycle")
        print("   19:00 - Evening engagement")
        print("   21:00 - Analytics review")

    def run_scheduler(self):
        """Run the automated scheduler"""
        
        print("🤖 Starting automated growth scheduler...")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\n⏹️ Scheduler stopped by user")


async def main():
    """Main function with command options"""
    
    command = sys.argv[1] if len(sys.argv) > 1 else 'full'
    
    growth_system = MasterGrowthSystem()
    
    if command == 'full':
        await growth_system.run_full_day_automation()
    elif command == 'morning':
        await growth_system.run_morning_routine()
    elif command == 'engagement':
        await growth_system.run_engagement_burst()
    elif command == 'growth':
        await growth_system.run_growth_sprint()
    elif command == 'posting':
        await growth_system.run_posting_cycle()
    elif command == 'evening':
        await growth_system.run_evening_review()
    elif command == 'schedule':
        growth_system.setup_automated_schedule()
        growth_system.run_scheduler()
    else:
        print("🚀 SME Analytica Master Growth System")
        print("=" * 50)
        print("Usage: python master_growth_system.py [command]")
        print("\nCommands:")
        print("  full       - Run complete daily automation")
        print("  morning    - Morning content generation")
        print("  engagement - Engagement burst activities")
        print("  growth     - Growth sprint activities")
        print("  posting    - Posting cycle")
        print("  evening    - Evening review & analytics")
        print("  schedule   - Start automated scheduler")
        print("\nExamples:")
        print("  python master_growth_system.py full")
        print("  python master_growth_system.py schedule")


if __name__ == "__main__":
    asyncio.run(main())
