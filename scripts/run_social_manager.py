#!/usr/bin/env python3
"""
Main execution script for SME Analytica Social Media Manager
"""

import asyncio
import logging
import argparse
import sys
import os
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from social_media_manager import SocialMediaManager
from config.settings import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.log_file),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def run_daily_automation():
    """Run the complete daily automation workflow"""
    logger.info("Starting SME Analytica Social Media Manager - Daily Automation")
    
    try:
        manager = SocialMediaManager()
        await manager.run_daily_automation()
        logger.info("Daily automation completed successfully")
    except Exception as e:
        logger.error(f"Daily automation failed: {e}")
        sys.exit(1)

async def run_test():
    """Test all system components"""
    logger.info("Testing SME Analytica Social Media Manager")
    
    try:
        manager = SocialMediaManager()
        results = await manager.test_system()
        
        print("\\n=== System Test Results ===")
        for component, status in results.items():
            status_str = "✅ PASS" if status else "❌ FAIL"
            print(f"{component}: {status_str}")
            
            if isinstance(status, dict):
                for provider, provider_status in status.items():
                    provider_status_str = "✅ PASS" if provider_status else "❌ FAIL"
                    print(f"  {provider}: {provider_status_str}")
        
        print("\\n=== Test Complete ===")
        
    except Exception as e:
        logger.error(f"System test failed: {e}")
        sys.exit(1)

async def generate_content_only():
    """Generate content without posting"""
    logger.info("Generating content for SME Analytica")
    
    try:
        manager = SocialMediaManager()
        await manager._generate_daily_content()
        logger.info("Content generation completed")
    except Exception as e:
        logger.error(f"Content generation failed: {e}")
        sys.exit(1)

async def run_engagement_only():
    """Run engagement automation only"""
    logger.info("Running engagement automation")
    
    try:
        manager = SocialMediaManager()
        await manager._process_engagement_opportunities()
        await manager._respond_to_mentions()
        logger.info("Engagement automation completed")
    except Exception as e:
        logger.error(f"Engagement automation failed: {e}")
        sys.exit(1)

async def get_performance_report(days: int = 7):
    """Generate and display performance report"""
    logger.info(f"Generating {days}-day performance report")
    
    try:
        manager = SocialMediaManager()
        report = await manager.get_performance_report(days)
        
        print(f"\\n=== SME Analytica Social Media Performance Report ===")
        print(f"Period: {report['period']}")
        print(f"Posts Created: {report['posts_created']}")
        print(f"Posts Published: {report['posts_published']}")
        print(f"Engagements Made: {report['engagements_made']}")
        print(f"Average Daily Posts: {report['avg_daily_posts']}")
        print(f"Publishing Rate: {report['publishing_rate']}%")
        
        if report['account_metrics']:
            print(f"\\nAccount Metrics:")
            for metric, value in report['account_metrics'].items():
                print(f"  {metric}: {value}")
        
        print(f"\\nAI Provider Status:")
        for provider, status in report['ai_provider_status'].items():
            availability = "Available" if status['available'] else "Unavailable"
            print(f"  {provider}: {availability}")
        
        print("\\n=== Report Complete ===")
        
    except Exception as e:
        logger.error(f"Performance report failed: {e}")
        sys.exit(1)

def main():
    """Main entry point with command line arguments"""
    parser = argparse.ArgumentParser(description="SME Analytica Social Media Manager")
    parser.add_argument(
        'command', 
        choices=['daily', 'test', 'content', 'engagement', 'report'],
        help='Command to execute'
    )
    parser.add_argument(
        '--days', 
        type=int, 
        default=7,
        help='Number of days for performance report (default: 7)'
    )
    
    args = parser.parse_args()
    
    if args.command == 'daily':
        asyncio.run(run_daily_automation())
    elif args.command == 'test':
        asyncio.run(run_test())
    elif args.command == 'content':
        asyncio.run(generate_content_only())
    elif args.command == 'engagement':
        asyncio.run(run_engagement_only())
    elif args.command == 'report':
        asyncio.run(get_performance_report(args.days))

if __name__ == "__main__":
    main()
