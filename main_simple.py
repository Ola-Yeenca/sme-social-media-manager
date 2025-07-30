#!/usr/bin/env python3
"""
SME Social Media Manager - Simplified Version
Single entry point for daily social media automation

Usage:
    python main.py                    # Run full daily automation
    python main.py --mode=content     # Generate and post content only  
    python main.py --mode=monitor     # Check mentions and engage only
    python main.py --mode=analytics   # Show analytics only
    python main.py --status           # Show system status
"""

import os
import sys
import argparse
from datetime import datetime
from typing import Dict, List

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Manual .env loading as fallback
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#') and '=' in line:
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value.strip('"').strip("'")

# Import our simple modules
from config import Config
from content_generator import ContentGenerator
from social_manager import SocialManager
from monitor import Monitor
from analytics import Analytics

def main():
    """Main orchestration function"""
    print(f"🚀 SME Social Media Manager - Simple Version")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    
    # Parse arguments
    parser = argparse.ArgumentParser(description='SME Social Media Manager')
    parser.add_argument('--mode', choices=['full', 'content', 'monitor', 'analytics'], 
                       default='full', help='Operation mode')
    parser.add_argument('--status', action='store_true', help='Show system status')
    args = parser.parse_args()
    
    # Initialize configuration
    config = Config()
    is_valid, missing = config.validate()
    
    if args.status:
        show_status(config, is_valid, missing)
        return
    
    if not is_valid:
        print("❌ Configuration Error:")
        for item in missing:
            print(f"   - Missing: {item}")
        print("\n💡 Please check your environment variables or .env file")
        sys.exit(1)
    
    # Initialize components
    try:
        content_generator = ContentGenerator(config)
        social_manager = SocialManager(config)
        monitor = Monitor(config, social_manager, content_generator)
        analytics = Analytics(config)
        
        print("✅ All components initialized successfully")
        
    except Exception as e:
        print(f"❌ Initialization error: {e}")
        sys.exit(1)
    
    # Run based on mode
    if args.mode == 'content':
        run_content_mode(content_generator, social_manager, analytics)
    elif args.mode == 'monitor':
        run_monitor_mode(monitor, analytics)
    elif args.mode == 'analytics':
        run_analytics_mode(analytics)
    else:  # full mode
        run_full_automation(content_generator, social_manager, monitor, analytics)
    
    print(f"✅ Automation complete at {datetime.now().strftime('%H:%M:%S UTC')}")

def run_full_automation(content_generator: ContentGenerator, social_manager: SocialManager, 
                       monitor: Monitor, analytics: Analytics):
    """Run complete daily automation"""
    print("\n🎯 Running Full Daily Automation")
    
    all_posts = []
    engagement_results = {}
    
    # 1. Generate and post content
    print("\n📝 Phase 1: Content Generation & Posting")
    posts = content_generator.generate_daily_posts(num_posts=3)
    
    for post in posts:
        if post:
            print(f"📄 Generated: {post['content'][:50]}...")
            
            # Post to all platforms
            post_results = social_manager.post_to_all_platforms(post['content'])
            
            # Log each successful post
            for result in post_results:
                analytics.log_post(result)
                all_posts.append(result)
    
    # 2. Monitor and engage
    print("\n👀 Phase 2: Monitoring & Engagement")
    engagement_results = monitor.basic_engagement()
    analytics.log_engagement(engagement_results)
    
    # 3. Generate summary
    print("\n📊 Phase 3: Analytics Summary")
    summary = analytics.daily_summary(all_posts, engagement_results)
    
    print(f"\n🎉 Daily automation complete!")
    print(f"   Posts created: {len(all_posts)}")
    print(f"   Mentions handled: {engagement_results.get('mentions_checked', 0)}")
    print(f"   Engagement actions: {engagement_results.get('likes_given', 0)}")

def run_content_mode(content_generator: ContentGenerator, social_manager: SocialManager, 
                    analytics: Analytics):
    """Run content generation and posting only"""
    print("\n📝 Content Generation Mode")
    
    posts = content_generator.generate_daily_posts(num_posts=3)
    posted_count = 0
    
    for post in posts:
        if post:
            print(f"📄 Content: {post['content']}")
            
            # Post to platforms
            results = social_manager.post_to_all_platforms(post['content'])
            
            for result in results:
                if result.get('success'):
                    analytics.log_post(result)
                    posted_count += 1
    
    print(f"✅ Posted {posted_count} pieces of content")

def run_monitor_mode(monitor: Monitor, analytics: Analytics):
    """Run monitoring and engagement only"""
    print("\n👀 Monitoring Mode")
    
    engagement_results = monitor.basic_engagement()
    analytics.log_engagement(engagement_results)
    
    print(f"✅ Monitoring complete: {engagement_results}")

def run_analytics_mode(analytics: Analytics):
    """Show analytics only"""
    print("\n📊 Analytics Mode")
    
    stats = analytics.get_basic_stats()
    print(f"📈 Current Stats: {stats}")

def show_status(config: Config, is_valid: bool, missing: List[str]):
    """Show system status"""
    print("\n🔍 System Status Check")
    print("=" * 50)
    
    # Configuration status
    print(f"Config Valid: {'✅ Yes' if is_valid else '❌ No'}")
    if missing:
        print("Missing Configuration:")
        for item in missing:
            print(f"  - {item}")
    
    # API status
    print(f"\nAPI Providers:")
    print(f"  Twitter: {'✅ Configured' if config.twitter_api_key else '❌ Missing'}")
    print(f"  LinkedIn: {'✅ Configured' if config.linkedin_access_token else '⚠️ Optional'}")
    print(f"  AI Provider: {'✅ ' + config.get_ai_provider() if config.get_ai_provider() else '❌ Missing'}")
    print(f"  Notion: {'✅ Configured' if config.notion_api_key else '⚠️ Optional'}")
    
    # File status
    print(f"\nCore Files:")
    required_files = ['config.py', 'content_generator.py', 'social_manager.py', 
                     'monitor.py', 'analytics.py']
    for file in required_files:
        exists = os.path.exists(file)
        print(f"  {file}: {'✅ Found' if exists else '❌ Missing'}")
    
    print("\n" + "=" * 50)
    
    if is_valid:
        print("✅ System ready for automation")
    else:
        print("❌ System not ready - fix configuration issues")

if __name__ == "__main__":
    main()