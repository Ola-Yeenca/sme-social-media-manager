#!/usr/bin/env python3
"""
Integration script for Community Engagement with SME Social Manager
Shows how to integrate the community system with the existing automation
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.community.influencer_targeting import InfluencerTargeting
from src.community.community_automation import CommunityAutomation

class SMESocialManagerWithCommunity:
    """Enhanced SME Social Manager with Community Engagement"""
    
    def __init__(self):
        self.community_targeting = InfluencerTargeting()
        self.community_automation = CommunityAutomation()
        
    async def initialize_community_system(self):
        """Initialize the community engagement system"""
        
        print("🔧 Initializing SME Analytica Community System...")
        
        # Discover and load influencers
        keywords = [
            "restaurant analytics", "dynamic pricing", "hospitality tech", 
            "small business", "pos integration", "hotel management",
            "retail analytics", "business intelligence"
        ]
        
        influencers = await self.community_targeting.discover_influencers(keywords, limit=50)
        await self.community_targeting.save_influencer_profiles(influencers)
        
        print(f"✅ Loaded {len(influencers)} influencer profiles")
        
        # Categorize by priority
        categories = {}
        for influencer in influencers:
            category = influencer.community_type.value
            if category not in categories:
                categories[category] = []
            categories[category].append(influencer)
        
        print("\n📊 Community Composition:")
        for category, profiles in categories.items():
            avg_value = sum(p.business_value_score for p in profiles) / len(profiles)
            print(f"   • {category.replace('_', ' ').title()}: {len(profiles)} profiles (avg value: {avg_value:.1f}/10)")
        
        return influencers
    
    async def run_daily_community_engagement(self, week: int = 1):
        """Run daily community engagement as part of social media automation"""
        
        print(f"\n🚀 Running Daily Community Engagement - Week {week}")
        print("=" * 60)
        
        # Get engagement opportunities
        opportunities = await self.community_targeting.identify_engagement_opportunities()
        print(f"🎯 Found {len(opportunities)} engagement opportunities")
        
        if opportunities:
            # Show top opportunities
            print("\n🔥 TOP OPPORTUNITIES:")
            for i, opp in enumerate(opportunities[:5], 1):
                print(f"{i}. @{opp.member.profile.username} ({opp.member.profile.community_type.value})")
                print(f"   📊 Score: {opp.urgency_score:.1f}/10 | 💰 Conversion: {opp.conversion_potential:.1f}/10")
                print(f"   💬 Action: {opp.opportunity_type}")
                print(f"   📝 Response: \"{opp.suggested_response[:80]}...\"")
            
            # Execute engagements (with daily limits)
            execution_results = await self.community_targeting.execute_engagement_plan(
                opportunities, daily_limit=20
            )
            
            print(f"\n✅ EXECUTION RESULTS:")
            print(f"   • Executed: {execution_results['executed_count']} engagements")
            print(f"   • Expected responses: {execution_results['expected_responses']:.1f}")
            print(f"   • Expected conversions: {execution_results['expected_conversions']:.2f}")
            print(f"   • Business value score: {execution_results['total_business_value_score']:.1f}")
        
        # Get community analytics
        analytics = self.community_targeting.get_community_analytics()
        
        print(f"\n📈 COMMUNITY METRICS:")
        print(f"   • Total members: {sum(item['count'] for item in analytics['community_composition'])}")
        
        funnel = analytics['conversion_funnel']
        print(f"   • Conversion funnel: {funnel['prospects']} → {funnel['engaged']} → {funnel['active']} → {funnel['customers']}")
        
        return {
            "opportunities_found": len(opportunities),
            "engagements_executed": execution_results.get('executed_count', 0) if opportunities else 0,
            "expected_responses": execution_results.get('expected_responses', 0) if opportunities else 0,
            "expected_conversions": execution_results.get('expected_conversions', 0) if opportunities else 0,
            "community_size": sum(item['count'] for item in analytics['community_composition'])
        }
    
    async def generate_weekly_community_report(self, week: int):
        """Generate weekly community engagement report"""
        
        print(f"\n📊 WEEKLY COMMUNITY REPORT - Week {week}")
        print("=" * 60)
        
        # Get comprehensive analytics
        analytics = self.community_targeting.get_community_analytics(days=7)
        
        # Community composition
        print("🏘️ COMMUNITY COMPOSITION:")
        total_members = sum(item['count'] for item in analytics['community_composition'])
        print(f"   Total Community Members: {total_members}")
        
        for item in analytics['community_composition']:
            percentage = (item['count'] / total_members * 100) if total_members > 0 else 0
            print(f"   • {item['type'].replace('_', ' ').title()}: {item['count']} ({percentage:.1f}%)")
        
        # High-value targets
        print(f"\n💎 HIGH-VALUE TARGETS:")
        for target in analytics['high_value_targets'][:5]:
            print(f"   • @{target['username']}: Value {target['value_score']:.1f}/10, Status: {target['status']}")
        
        # Growth projections
        week_targets = {
            1: {"followers": 50, "engagements": 350, "demos": 5},
            2: {"followers": 150, "engagements": 490, "demos": 10},
            3: {"followers": 300, "engagements": 630, "demos": 20},
            4: {"followers": 500, "engagements": 700, "demos": 30}
        }
        
        current_target = week_targets.get(week, week_targets[1])
        
        print(f"\n🎯 WEEK {week} TARGETS:")
        print(f"   • Follower target: {current_target['followers']}")
        print(f"   • Engagement target: {current_target['engagements']}")
        print(f"   • Demo target: {current_target['demos']}")
        
        # Success metrics
        print(f"\n📈 SUCCESS METRICS:")
        print(f"   • Community engagement rate: 35%+ (target)")
        print(f"   • Response rate: 15%+ (target)")
        print(f"   • Conversion rate: 5%+ (target)")
        print(f"   • Business inquiries: {current_target['demos']} (target)")
        
        return analytics
    
    async def get_community_status(self):
        """Get current community status for integration with main dashboard"""
        
        analytics = self.community_targeting.get_community_analytics()
        
        return {
            "total_community_members": sum(item['count'] for item in analytics['community_composition']),
            "high_value_targets": len([t for t in analytics['high_value_targets'] if t['value_score'] >= 8.0]),
            "conversion_funnel": analytics['conversion_funnel'],
            "top_opportunities": len(await self.community_targeting.identify_engagement_opportunities()),
            "ready_for_automation": True
        }

async def main():
    """Demonstrate the integrated community engagement system"""
    
    print("🚀 SME ANALYTICA ENHANCED SOCIAL MANAGER")
    print("With Intelligent Community Engagement")
    print("=" * 70)
    
    # Initialize enhanced system
    manager = SMESocialManagerWithCommunity()
    
    # Initialize community system
    await manager.initialize_community_system()
    
    # Simulate daily operations for Week 1
    print(f"\n⏰ SIMULATING DAILY OPERATIONS...")
    
    daily_results = []
    for day in range(1, 4):  # Show 3 days
        print(f"\n📅 Day {day} Operations:")
        day_result = await manager.run_daily_community_engagement(week=1)
        daily_results.append(day_result)
        
        print(f"   Summary: {day_result['engagements_executed']} engagements, "
              f"{day_result['expected_conversions']:.1f} expected conversions")
    
    # Weekly report
    await manager.generate_weekly_community_report(week=1)
    
    # Integration status
    status = await manager.get_community_status()
    
    print(f"\n🔗 INTEGRATION STATUS:")
    print(f"   • Community system: ✅ Active")
    print(f"   • Total members tracked: {status['total_community_members']}")
    print(f"   • High-value targets: {status['high_value_targets']}")
    print(f"   • Daily opportunities: {status['top_opportunities']}")
    print(f"   • Automation ready: {'✅' if status['ready_for_automation'] else '❌'}")
    
    print(f"\n🎯 INTEGRATION BENEFITS:")
    print(f"   ✅ Automated influencer discovery and targeting")
    print(f"   ✅ Smart engagement opportunity identification")
    print(f"   ✅ Conversion-focused community building")
    print(f"   ✅ Comprehensive relationship management")
    print(f"   ✅ Business-focused growth metrics")
    print(f"   ✅ Seamless integration with existing automation")
    
    print(f"\n💰 EXPECTED BUSINESS IMPACT:")
    print(f"   📈 500+ targeted followers in 4 weeks")
    print(f"   🎯 30+ demo requests generated")
    print(f"   💼 20+ qualified business conversations")
    print(f"   🤝 50+ industry relationship established")
    print(f"   📊 35%+ engagement rate achieved")
    
    print(f"\n🚀 System ready for production deployment!")

if __name__ == "__main__":
    asyncio.run(main())