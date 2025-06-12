#!/usr/bin/env python3
"""
SME Analytica Community Engagement Demo
Demonstrates the intelligent community engagement system
"""

import asyncio
import sys
import os
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.community.influencer_targeting import (
    InfluencerTargeting,
    InfluencerProfile,
    CommunityType,
    RelationshipStatus
)
from src.community.community_automation import CommunityAutomation

async def demo_influencer_discovery():
    """Demo influencer discovery and targeting"""
    
    print("🔍 INFLUENCER DISCOVERY & TARGETING")
    print("=" * 50)
    
    targeting = InfluencerTargeting()
    
    # Discover influencers
    keywords = ["restaurant analytics", "dynamic pricing", "hospitality tech", "small business", "menuflow"]
    influencers = await targeting.discover_influencers(keywords, limit=15)
    
    print(f"✅ Discovered {len(influencers)} high-quality influencers")
    print("\n🎯 TOP TARGETS:")
    
    # Save to database
    await targeting.save_influencer_profiles(influencers)
    
    # Show top targets by category
    categories = {}
    for influencer in influencers:
        category = influencer.community_type.value
        if category not in categories:
            categories[category] = []
        categories[category].append(influencer)
    
    for category, profiles in categories.items():
        print(f"\n📊 {category.replace('_', ' ').title()} ({len(profiles)} profiles):")
        
        # Sort by business value score
        sorted_profiles = sorted(profiles, key=lambda x: x.business_value_score, reverse=True)
        
        for i, profile in enumerate(sorted_profiles[:3], 1):  # Show top 3 per category
            print(f"   {i}. @{profile.username} - {profile.display_name}")
            print(f"      👥 {profile.follower_count:,} followers | 📈 {profile.engagement_rate:.1%} engagement")
            print(f"      💰 Business Value: {profile.business_value_score:.1f}/10")
            print(f"      🎯 Conversion Potential: {profile.conversion_potential:.1f}/10")
            print(f"      📍 {profile.location} | 🏷️ {profile.tier.value}")
            print(f"      💡 Key Interests: {', '.join(profile.interests[:3])}")
            print()
    
    return targeting

async def demo_engagement_opportunities(targeting):
    """Demo engagement opportunity identification"""
    
    print("\n🎯 ENGAGEMENT OPPORTUNITY IDENTIFICATION")
    print("=" * 50)
    
    # Identify opportunities
    opportunities = await targeting.identify_engagement_opportunities(timeframe_hours=24)
    
    print(f"✅ Found {len(opportunities)} high-quality engagement opportunities")
    
    if opportunities:
        print("\n🔥 TOP 5 OPPORTUNITIES:")
        
        for i, opp in enumerate(opportunities[:5], 1):
            profile = opp.member.profile
            print(f"\n{i}. @{profile.username} ({profile.community_type.value})")
            print(f"   📊 Urgency: {opp.urgency_score:.1f}/10 | 💰 Conversion: {opp.conversion_potential:.1f}/10")
            print(f"   🎭 Relationship: {opp.member.lifecycle_stage.value}")
            print(f"   📝 Content: \"{opp.content_text[:100]}...\"")
            print(f"   💡 Context: {opp.engagement_context}")
            print(f"   ⚡ Action: {opp.opportunity_type}")
            print(f"   🎯 Response: \"{opp.suggested_response[:120]}...\"")
            print(f"   📈 Expected Outcome: {opp.expected_outcome}")
    
    return opportunities

async def demo_engagement_execution(targeting, opportunities):
    """Demo engagement execution and tracking"""
    
    print("\n🚀 ENGAGEMENT EXECUTION")
    print("=" * 50)
    
    if not opportunities:
        print("⚠️ No opportunities available for execution demo")
        return {}
    
    # Execute top 10 opportunities
    execution_results = await targeting.execute_engagement_plan(opportunities[:10])
    
    print(f"✅ Executed {execution_results['executed_count']} engagements")
    print(f"📊 Execution Rate: {execution_results['execution_rate']:.1f}%")
    print(f"💬 Expected Responses: {execution_results['expected_responses']:.1f}")
    print(f"💰 Expected Conversions: {execution_results['expected_conversions']:.2f}")
    print(f"📈 Total Business Value Score: {execution_results['total_business_value_score']:.1f}")
    
    if execution_results['engagements']:
        print("\n🎯 ENGAGEMENT HIGHLIGHTS:")
        
        high_value_engagements = [
            eng for eng in execution_results['engagements']
            if eng['expected_metrics']['business_value_score'] >= 8.0
        ]
        
        if high_value_engagements:
            print(f"   💎 {len(high_value_engagements)} high-value target engagements")
        
        high_conversion_engagements = [
            eng for eng in execution_results['engagements']
            if eng['expected_metrics']['conversion_probability'] >= 0.7
        ]
        
        if high_conversion_engagements:
            print(f"   🎯 {len(high_conversion_engagements)} high-conversion opportunities")
        
        quick_responses = [
            eng for eng in execution_results['engagements']
            if eng['expected_metrics']['response_probability'] >= 0.8
        ]
        
        if quick_responses:
            print(f"   ⚡ {len(quick_responses)} likely to get quick responses")
    
    return execution_results

async def demo_community_analytics(targeting):
    """Demo community analytics and insights"""
    
    print("\n📈 COMMUNITY ANALYTICS")
    print("=" * 50)
    
    analytics = targeting.get_community_analytics(days=7)
    
    # Community composition
    print("🏘️ COMMUNITY COMPOSITION:")
    total_members = sum(item['count'] for item in analytics['community_composition'])
    print(f"   Total Community Members: {total_members}")
    
    for item in analytics['community_composition']:
        percentage = (item['count'] / total_members * 100) if total_members > 0 else 0
        print(f"   • {item['type'].replace('_', ' ').title()}: {item['count']} ({percentage:.1f}%)")
        print(f"     └─ Avg Value Score: {item['avg_value']:.1f}/10")
    
    # Relationship funnel
    print("\n🎯 RELATIONSHIP FUNNEL:")
    funnel = analytics['conversion_funnel']
    total_relationships = sum(funnel.values())
    
    if total_relationships > 0:
        for stage, count in funnel.items():
            percentage = (count / total_relationships * 100) if total_relationships > 0 else 0
            print(f"   • {stage.replace('_', ' ').title()}: {count} ({percentage:.1f}%)")
    
    # High-value targets
    print("\n💎 HIGH-VALUE TARGETS:")
    for i, target in enumerate(analytics['high_value_targets'][:5], 1):
        print(f"   {i}. @{target['username']} - {target['name']}")
        print(f"      💰 Value: {target['value_score']:.1f}/10 | 🎯 Conversion: {target['conversion_potential']:.1f}/10")
        print(f"      📊 Status: {target['status']}")
    
    return analytics

async def demo_full_automation():
    """Demo the complete automation system"""
    
    print("\n🤖 FULL AUTOMATION SYSTEM")
    print("=" * 50)
    
    automation = CommunityAutomation()
    
    # Run daily automation (simulation)
    daily_results = await automation.run_daily_automation(current_week=1)
    
    print(f"📅 Daily Automation Results - {daily_results['date']}")
    print(f"📊 Week {daily_results['week']} of 4-week campaign")
    
    summary = daily_results['daily_summary']
    print(f"\n⚡ EXECUTION SUMMARY:")
    print(f"   🎯 Target Engagements: {summary['total_target_engagements']:.0f}")
    print(f"   ✅ Executed Engagements: {summary['total_executed_engagements']:.0f}")
    print(f"   📊 Execution Rate: {summary['execution_rate']:.1f}%")
    
    # Phase breakdown
    print(f"\n🕐 PHASE BREAKDOWN:")
    for phase_name, phase_data in summary['phase_breakdown'].items():
        phase_display = phase_name.replace('_', ' ').title()
        print(f"   • {phase_display}: {phase_data['executed']:.0f}/{phase_data['target']:.0f}")
        print(f"     Focus: {phase_data['focus']}")
        if phase_data['highlights']:
            print(f"     Highlights: {', '.join(phase_data['highlights'])}")
    
    # Growth progress
    progress = daily_results['growth_progress']
    print(f"\n📈 GROWTH PROGRESS:")
    print(f"   • Current Followers: {progress['estimated_followers']:.0f}")
    print(f"   • Week Target: {progress['week_target']}")
    print(f"   • Week Progress: {progress['progress_to_weekly_target']:.1f}%")
    print(f"   • Overall Progress: {progress['progress_to_overall_target']:.1f}%")
    print(f"   • Projected Final: {progress['projected_final_followers']:.0f} followers")
    print(f"   • Days Remaining: {progress['days_remaining']}")
    
    # Tomorrow's plan
    tomorrow = daily_results['tomorrow_plan']
    print(f"\n🔮 TOMORROW'S STRATEGY:")
    print(f"   • Priority Focus: {tomorrow['priority_focus_tomorrow'].replace('_', ' ').title()}")
    print(f"   • Successful Phases: {', '.join(tomorrow['successful_phases'])}")
    if tomorrow['areas_for_improvement']:
        print(f"   • Areas to Improve: {', '.join(tomorrow['areas_for_improvement'])}")
    if tomorrow['strategy_adjustments']:
        print(f"   • Strategy Adjustments: {tomorrow['strategy_adjustments']}")
    
    return daily_results

async def demo_weekly_report():
    """Demo weekly reporting"""
    
    print("\n📊 WEEKLY REPORT")
    print("=" * 50)
    
    automation = CommunityAutomation()
    weekly_report = await automation.generate_weekly_report(week_number=1)
    
    print(f"📅 {weekly_report['period']}")
    
    targets = weekly_report['targets']
    performance = weekly_report['performance']
    
    print(f"\n🎯 TARGETS vs PERFORMANCE:")
    print(f"   • Followers: {performance['new_followers']:.0f} / {targets['followers']} ({performance['new_followers']/targets['followers']*100:.1f}%)")
    print(f"   • Engagements: {performance['engagements_executed']:.0f} / {targets['engagements']} ({performance['engagements_executed']/targets['engagements']*100:.1f}%)")
    print(f"   • Conversions: {performance['conversions_achieved']:.0f} / {targets['conversions']} ({performance['conversions_achieved']/targets['conversions']*100:.1f}%)")
    
    print(f"\n🌟 KEY ACHIEVEMENTS:")
    for achievement in weekly_report['key_achievements']:
        print(f"   {achievement}")
    
    if weekly_report['areas_for_improvement']:
        print(f"\n🔧 AREAS FOR IMPROVEMENT:")
        for improvement in weekly_report['areas_for_improvement']:
            print(f"   {improvement}")
    
    print(f"\n💡 NEXT WEEK RECOMMENDATIONS:")
    for recommendation in weekly_report['next_week_recommendations']:
        print(f"   {recommendation}")
    
    return weekly_report

async def main():
    """Run complete community engagement demo"""
    
    print("🚀 SME ANALYTICA COMMUNITY ENGAGEMENT SYSTEM")
    print("Building relationships that drive business growth")
    print("=" * 60)
    
    try:
        # Demo 1: Influencer Discovery
        targeting = await demo_influencer_discovery()
        
        # Demo 2: Engagement Opportunities  
        opportunities = await demo_engagement_opportunities(targeting)
        
        # Demo 3: Engagement Execution
        execution_results = await demo_engagement_execution(targeting, opportunities)
        
        # Demo 4: Community Analytics
        analytics = await demo_community_analytics(targeting)
        
        # Demo 5: Full Automation
        automation_results = await demo_full_automation()
        
        # Demo 6: Weekly Report
        weekly_report = await demo_weekly_report()
        
        # Final Summary
        print("\n🎉 DEMO COMPLETE - SYSTEM CAPABILITIES")
        print("=" * 60)
        print("✅ Intelligent influencer discovery and scoring")
        print("✅ Automated engagement opportunity identification")
        print("✅ Smart response generation and timing optimization")
        print("✅ Relationship lifecycle management")
        print("✅ Conversion-focused community building")
        print("✅ Comprehensive analytics and reporting")
        print("✅ Full automation with growth tracking")
        
        print(f"\n🎯 BUSINESS IMPACT PROJECTION:")
        print(f"   • 50+ high-value influencers targeted")
        print(f"   • 20+ potential customers engaged")  
        print(f"   • 30%+ engagement rate expected")
        print(f"   • 15+ demo requests projected")
        print(f"   • 500+ followers in 4 weeks")
        
        print(f"\n🚀 READY TO GROW SME ANALYTICA'S COMMUNITY!")
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())