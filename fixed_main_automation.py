#!/usr/bin/env python3
"""
Fixed SME Analytica Social Media Growth Manager
Production-ready automated social media management system with enhanced error handling
"""

import os
import sys
import asyncio
import argparse
import logging
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables (with fallback)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Continue without .env file loading

# Configure logging
def setup_logging():
    """Setup production logging"""
    os.makedirs('logs', exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/sme_social_manager.log'),
            logging.StreamHandler()
        ]
    )
    
    # Reduce noise from external libraries
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('tweepy').setLevel(logging.WARNING)
    logging.getLogger('notion_client').setLevel(logging.WARNING)

def validate_environment():
    """Validate required environment variables"""
    
    required_vars = [
        'TWITTER_API_KEY',
        'TWITTER_API_SECRET', 
        'TWITTER_ACCESS_TOKEN',
        'TWITTER_ACCESS_TOKEN_SECRET',
        'TWITTER_BEARER_TOKEN',
        'NOTION_API_KEY',
        'SOCIAL_MEDIA_DB_ID'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file or run the comprehensive test to create a template")
        return False, missing_vars
    
    return True, []

async def run_enhanced_automation():
    """Run enhanced automation with all systems integrated"""
    
    logger = logging.getLogger(__name__)
    logger.info("🚀 Starting Enhanced SME Analytica Automation")
    
    try:
        # Import and initialize enhanced systems
        from src.content.growth_content_generator import (
            GrowthOptimizedContentGenerator, 
            GrowthStrategy, 
            ContentTheme
        )
        from src.strategy.hashtag_intelligence import HashtagIntelligenceAgent
        from src.content.viral_optimization import ViralOptimizationAgent
        from src.community.community_automation import CommunityAutomation
        from src.analytics.analytics_dashboard import AnalyticsDashboard
        from config.settings import Language, settings
        
        print("📦 Initializing Enhanced Systems...")
        
        # Initialize all systems
        content_generator = GrowthOptimizedContentGenerator()
        hashtag_agent = HashtagIntelligenceAgent()
        
        # Initialize viral optimization with mock Twitter manager if needed
        try:
            from src.social.twitter_manager import TwitterManager
            twitter_manager = TwitterManager()
        except Exception:
            # Create mock Twitter manager for testing
            class MockTwitterManager:
                async def get_trending_hashtags(self):
                    return ["#RestaurantTech", "#AIBusiness", "#SmallBusiness"]
                
                async def search_tweets(self, query, max_results=20):
                    class MockTweet:
                        def __init__(self, query):
                            self.text = f"Sample tweet about {query}"
                            self.created_at = datetime.now()
                            self.public_metrics = {'like_count': 10, 'retweet_count': 5, 'reply_count': 2}
                    return [MockTweet(query) for _ in range(min(max_results, 10))]
            
            twitter_manager = MockTwitterManager()
            print("   ⚠️  Using mock Twitter manager (configure API keys for full functionality)")
        
        viral_agent = ViralOptimizationAgent(twitter_manager)
        community_automation = CommunityAutomation()
        analytics_dashboard = AnalyticsDashboard()
        
        print("✅ All systems initialized successfully")
        
        # Phase 1: Generate Enhanced Content Strategy
        print("\n📝 Phase 1: Enhanced Content Generation")
        
        # Generate 4-week growth calendar
        growth_calendar = content_generator.generate_4_week_growth_calendar()
        print(f"   📅 Generated 4-week growth calendar with {len(growth_calendar['weeks'])} weeks")
        
        # Generate today's content with optimal hashtags
        today_content = content_generator.generate_viral_optimized_content(
            theme=ContentTheme.DATA_MONDAY,
            growth_strategy=GrowthStrategy.FOLLOWER_ACQUISITION,
            language=Language.ENGLISH
        )
        
        # Optimize hashtags for the content
        optimal_hashtags = await hashtag_agent.get_optimal_hashtags_for_content(
            content_type="educational",
            theme="data_insights",
            target_audience="restaurant_owners"
        )
        
        print(f"   🎯 Generated content with viral score: {today_content['predicted_metrics'].viral_score:.1f}/10")
        print(f"   #️⃣ Optimized hashtags: {', '.join(optimal_hashtags.get('primary_combination', {}).get('hashtags', [])[:4])}")
        
        # Phase 2: Viral Optimization
        print("\n🔥 Phase 2: Viral Optimization")
        
        # Monitor trending topics
        trending_topics = await viral_agent.monitor_trending_topics()
        print(f"   📈 Found {len(trending_topics)} trending opportunities")
        
        # Generate viral content
        viral_content = await viral_agent.generate_viral_content(
            trend=trending_topics[0] if trending_topics else None,
            content_type="general"
        )
        print(f"   ⚡ Viral content score: {viral_content.viral_score:.1f}/10")
        
        # Get daily viral opportunities
        daily_opportunities = await viral_agent.get_daily_viral_opportunities(count=5)
        print(f"   🎯 {len(daily_opportunities)} viral opportunities identified")
        
        # Phase 3: Community Engagement
        print("\n👥 Phase 3: Community Engagement Automation")
        
        # Run daily community automation
        community_results = await community_automation.run_daily_automation(current_week=1)
        execution_rate = community_results['daily_summary']['automation_efficiency']['execution_rate']
        total_engagements = community_results['daily_summary']['total_executed_engagements']
        
        print(f"   🎯 Executed {total_engagements:.0f} community engagements")
        print(f"   ⚡ Automation efficiency: {execution_rate:.1f}%")
        print(f"   📊 Projected followers: {community_results['growth_progress']['projected_final_followers']:.0f}")
        
        # Phase 4: Analytics and Insights
        print("\n📊 Phase 4: Analytics Dashboard")
        
        # Generate comprehensive analytics
        analytics_report = analytics_dashboard.generate_comprehensive_report(weeks=1)
        real_time_dashboard = analytics_dashboard.get_real_time_dashboard()
        
        print(f"   📈 Analytics report generated")
        print(f"   🎯 Strategic recommendations: {len(analytics_report.get('strategic_recommendations', []))}")
        
        # Phase 5: Integration Summary
        print("\n🔗 Phase 5: System Integration Summary")
        
        integration_summary = {
            "content_generated": bool(today_content["text"]),
            "viral_optimization": viral_content.viral_score > 7.0,
            "hashtag_intelligence": len(optimal_hashtags.get("primary_combination", {}).get("hashtags", [])) > 0,
            "community_engagement": execution_rate > 80.0,
            "analytics_tracking": bool(analytics_report.get("report_generated")),
            "total_viral_score": (today_content['predicted_metrics'].viral_score + viral_content.viral_score) / 2,
            "estimated_reach": optimal_hashtags.get("primary_combination", {}).get("metrics", {}).get("predicted_reach", 1000),
            "automation_efficiency": execution_rate
        }
        
        success_metrics = sum(1 for v in integration_summary.values() if isinstance(v, bool) and v)
        
        print(f"   ✅ {success_metrics}/5 systems fully operational")
        print(f"   🎯 Combined viral score: {integration_summary['total_viral_score']:.1f}/10")
        print(f"   📈 Estimated reach: {integration_summary['estimated_reach']:,}")
        print(f"   ⚡ Overall automation efficiency: {integration_summary['automation_efficiency']:.1f}%")
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"logs/automation_results_{timestamp}.json"
        
        automation_results = {
            "timestamp": datetime.now().isoformat(),
            "integration_summary": integration_summary,
            "growth_calendar": growth_calendar,
            "viral_opportunities": len(daily_opportunities),
            "community_results": community_results,
            "analytics_summary": {
                "report_available": bool(analytics_report.get("report_generated")),
                "recommendations_count": len(analytics_report.get("strategic_recommendations", []))
            },
            "next_steps": generate_next_steps(integration_summary)
        }
        
        # Write results to file
        import json
        with open(results_file, 'w') as f:
            json.dump(automation_results, f, indent=2, default=str)
        
        print(f"\n📄 Automation results saved: {results_file}")
        
        # Final Summary
        print("\n" + "="*60)
        print("🎉 Enhanced Automation Complete!")
        print(f"📊 Systems Integration: {success_metrics}/5")
        print(f"🎯 Viral Content Score: {integration_summary['total_viral_score']:.1f}/10")
        print(f"📈 Estimated Reach: {integration_summary['estimated_reach']:,}")
        print(f"👥 Community Engagements: {total_engagements:.0f}")
        print(f"⚡ Automation Efficiency: {integration_summary['automation_efficiency']:.1f}%")
        print("="*60)
        
        return automation_results
        
    except Exception as e:
        logger.error(f"❌ Enhanced automation failed: {e}")
        print(f"💥 Automation failed: {e}")
        raise

def generate_next_steps(integration_summary: dict) -> list:
    """Generate next steps based on automation results"""
    
    next_steps = []
    
    success_count = sum(1 for v in integration_summary.values() if isinstance(v, bool) and v)
    
    if success_count >= 4:
        next_steps.extend([
            "🚀 Systems are operational - ready for production deployment",
            "📊 Monitor viral scores and adjust content strategy accordingly",
            "📈 Scale up community engagement based on efficiency metrics",
            "🔄 Schedule regular automation runs (3x daily recommended)"
        ])
    elif success_count >= 3:
        next_steps.extend([
            "⚠️  Most systems working - investigate failing components",
            "🔧 Review error logs for failing systems",
            "📊 Focus on improving automation efficiency",
            "🧪 Run comprehensive system test to identify issues"
        ])
    else:
        next_steps.extend([
            "🚨 Multiple system failures - run comprehensive diagnostics",
            "🔍 Check environment variables and API configurations",
            "🛠️  Review system requirements and dependencies",
            "📞 Consider technical support for critical issues"
        ])
    
    # Performance-based recommendations
    if integration_summary.get("total_viral_score", 0) > 8.0:
        next_steps.append("🔥 High viral scores - amplify content distribution")
    
    if integration_summary.get("automation_efficiency", 0) > 85.0:
        next_steps.append("⚡ High efficiency - consider increasing engagement targets")
    
    return next_steps

async def run_basic_automation():
    """Run basic automation workflow (fallback)"""
    
    logger = logging.getLogger(__name__)
    logger.info("🔄 Running basic automation workflow")
    
    try:
        # Basic content generation
        from src.content.content_generator import ContentGenerator
        from config.settings import ContentTheme, Language
        
        content_generator = ContentGenerator()
        
        # Generate basic content
        content = content_generator.generate_themed_content(
            ContentTheme.DATA_MONDAY, 
            Language.ENGLISH
        )
        
        print("📝 Basic content generated:")
        print(f"   Content: {content.get('text', 'No content')[:100]}...")
        print(f"   Hashtags: {', '.join(content.get('hashtags', []))}")
        
        return {"basic_automation": True, "content_generated": bool(content.get('text'))}
        
    except Exception as e:
        logger.error(f"❌ Basic automation failed: {e}")
        print(f"💥 Basic automation failed: {e}")
        return {"basic_automation": False, "error": str(e)}

def print_status():
    """Print current system status"""
    
    print("🚀 SME Analytica Social Media Growth Manager")
    print("=" * 60)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"🕐 Time: {datetime.now().strftime('%H:%M:%S')}")
    print(f"🐦 Twitter Account: @smeanalytica")
    print(f"📊 Notion Database: SME Social Media Posts")
    print("=" * 60)

async def main():
    """Main function with enhanced error handling"""
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='SME Analytica Social Media Growth Manager',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python fixed_main_automation.py --mode=enhanced     # Run enhanced automation (recommended)
  python fixed_main_automation.py --mode=basic       # Run basic automation
  python fixed_main_automation.py --test             # Run system test
  python fixed_main_automation.py --status           # Show system status
        """
    )
    
    parser.add_argument(
        '--mode',
        choices=['enhanced', 'basic'],
        default='enhanced',
        help='Operation mode (default: enhanced)'
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Run comprehensive system test'
    )
    
    parser.add_argument(
        '--status',
        action='store_true',
        help='Show system status and exit'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress output (logs only)'
    )
    
    args = parser.parse_args()
    
    # Show status if requested
    if args.status:
        print_status()
        return
    
    # Run system test if requested
    if args.test:
        try:
            from comprehensive_system_test import ComprehensiveSystemTest
            test_suite = ComprehensiveSystemTest()
            results = await test_suite.run_comprehensive_test()
            return results
        except ImportError:
            print("❌ System test module not found. Please ensure comprehensive_system_test.py is available.")
            return
    
    # Validate environment
    env_valid, missing_vars = validate_environment()
    if not env_valid:
        print("\n🔧 Environment issues detected. Options:")
        print("   1. Run: python comprehensive_system_test.py  # Creates template .env")
        print("   2. Manually configure missing variables in .env file")
        print("   3. Run with --mode=basic for limited functionality")
        
        if args.mode == 'enhanced':
            print("\n⚠️  Switching to basic mode due to environment issues...")
            args.mode = 'basic'
    
    # Print status unless quiet
    if not args.quiet:
        print_status()
    
    try:
        # Run based on mode
        if args.mode == 'enhanced':
            if env_valid:
                results = await run_enhanced_automation()
            else:
                print("❌ Enhanced mode requires complete environment setup")
                results = await run_basic_automation()
        else:  # basic mode
            results = await run_basic_automation()
        
        if not args.quiet:
            print(f"\n✅ Operation '{args.mode}' completed successfully!")
            
        logger.info(f"Operation '{args.mode}' completed successfully")
        return results
        
    except KeyboardInterrupt:
        logger.info("⏹️ Operation stopped by user")
        if not args.quiet:
            print("\n⏹️ Operation stopped by user")
        
    except Exception as e:
        logger.error(f"❌ Operation failed: {e}")
        if not args.quiet:
            print(f"\n❌ Operation failed: {e}")
            print("\n🔧 Troubleshooting suggestions:")
            print("   1. Run: python fixed_main_automation.py --test")
            print("   2. Check environment variables in .env file")
            print("   3. Verify all dependencies are installed")
            print("   4. Check logs/sme_social_manager.log for details")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())