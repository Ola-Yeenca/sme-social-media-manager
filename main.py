#!/usr/bin/env python3
"""
SME Analytica Social Media Growth Manager
Production-ready automated social media management system

Usage:
    python main.py              # Run full daily automation
    python main.py --mode=post  # Just post scheduled content
    python main.py --mode=grow  # Just run growth activities
    python main.py --help       # Show help
"""

import os
import sys
import asyncio
import argparse
import logging
from datetime import datetime
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

# Unset shell environment variable to use .env file
if 'SOCIAL_MEDIA_DB_ID' in os.environ:
    del os.environ['SOCIAL_MEDIA_DB_ID']

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

async def run_full_automation():
    """Run complete daily automation"""
    
    logger = logging.getLogger(__name__)
    logger.info("🚀 Starting SME Analytica Daily Automation")
    
    try:
        from master_growth_system import MasterGrowthSystem
        
        growth_system = MasterGrowthSystem()
        results = await growth_system.run_full_day_automation()
        
        logger.info("✅ Daily automation completed successfully")
        return results
        
    except Exception as e:
        logger.error(f"❌ Daily automation failed: {e}")
        raise

async def run_posting_only():
    """Run posting cycle only"""
    
    logger = logging.getLogger(__name__)
    logger.info("📤 Starting posting cycle")
    
    try:
        from run_automation import check_and_post_scheduled_content
        
        posted_count = await check_and_post_scheduled_content()
        
        logger.info(f"✅ Posting cycle completed: {posted_count} posts published")
        return {"posts_published": posted_count}
        
    except Exception as e:
        logger.error(f"❌ Posting cycle failed: {e}")
        raise

async def run_growth_only():
    """Run growth activities only"""
    
    logger = logging.getLogger(__name__)
    logger.info("🚀 Starting growth activities")
    
    try:
        from growth_automation import run_growth_automation
        
        results = await run_growth_automation()
        
        logger.info("✅ Growth activities completed")
        return results
        
    except Exception as e:
        logger.error(f"❌ Growth activities failed: {e}")
        raise

async def run_content_generation():
    """Run AI-powered SME Analytica content generation"""

    logger = logging.getLogger(__name__)
    logger.info("🤖 Starting AI-powered SME Analytica content generation")

    try:
        from ai_content_generator import generate_ai_content

        posts_created = await generate_ai_content()

        logger.info(f"✅ AI content generation completed: {posts_created} posts created")
        return {"posts_created": posts_created}

    except Exception as e:
        logger.error(f"❌ AI content generation failed: {e}")
        raise

async def run_analytics():
    """Run analytics only"""
    
    logger = logging.getLogger(__name__)
    logger.info("📊 Starting analytics")
    
    try:
        from advanced_analytics import run_advanced_analytics
        
        results = await run_advanced_analytics()
        
        logger.info("✅ Analytics completed")
        return results
        
    except Exception as e:
        logger.error(f"❌ Analytics failed: {e}")
        raise

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
        print("Please check your .env file")
        return False
    
    return True

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
    """Main function"""
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='SME Analytica Social Media Growth Manager',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Run full daily automation
  python main.py --mode=post        # Just post scheduled content
  python main.py --mode=grow        # Just run growth activities
  python main.py --mode=content     # Just generate content
  python main.py --mode=analytics   # Just run analytics
  python main.py --status           # Show system status
        """
    )
    
    parser.add_argument(
        '--mode',
        choices=['full', 'post', 'grow', 'content', 'analytics'],
        default='full',
        help='Operation mode (default: full)'
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
    
    # Validate environment
    if not validate_environment():
        sys.exit(1)
    
    # Print status unless quiet
    if not args.quiet:
        print_status()
    
    try:
        # Run based on mode
        if args.mode == 'full':
            results = await run_full_automation()
        elif args.mode == 'post':
            results = await run_posting_only()
        elif args.mode == 'grow':
            results = await run_growth_only()
        elif args.mode == 'content':
            results = await run_content_generation()
        elif args.mode == 'analytics':
            results = await run_analytics()
        
        if not args.quiet:
            print(f"\n✅ Operation '{args.mode}' completed successfully!")
            
        logger.info(f"Operation '{args.mode}' completed successfully")
        
    except KeyboardInterrupt:
        logger.info("⏹️ Operation stopped by user")
        if not args.quiet:
            print("\n⏹️ Operation stopped by user")
        
    except Exception as e:
        logger.error(f"❌ Operation failed: {e}")
        if not args.quiet:
            print(f"\n❌ Operation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
