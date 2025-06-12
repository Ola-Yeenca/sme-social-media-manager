#!/usr/bin/env python3
"""
Quick Community Engagement Demo - Without delays
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.community.influencer_targeting import InfluencerTargeting

async def main():
    print("🚀 SME Analytica Community Engagement System")
    print("=" * 60)
    
    targeting = InfluencerTargeting()
    
    # 1. Discover influencers
    print("🔍 Discovering influencers...")
    keywords = ["restaurant analytics", "dynamic pricing", "hospitality tech"]
    influencers = await targeting.discover_influencers(keywords, limit=10)
    await targeting.save_influencer_profiles(influencers)
    
    print(f"✅ Found {len(influencers)} targeted influencers")
    
    # Show top 3 targets
    print("\n🎯 TOP TARGETS:")
    top_targets = sorted(influencers, key=lambda x: x.business_value_score, reverse=True)[:3]
    
    for i, profile in enumerate(top_targets, 1):
        print(f"{i}. @{profile.username} ({profile.community_type.value})")
        print(f"   👥 {profile.follower_count:,} followers")
        print(f"   💰 Business Value: {profile.business_value_score:.1f}/10")
        print(f"   🎯 Conversion Potential: {profile.conversion_potential:.1f}/10")
        print(f"   📍 {profile.location}")
    
    # 2. Find engagement opportunities
    print(f"\n🎯 Finding engagement opportunities...")
    opportunities = await targeting.identify_engagement_opportunities()
    
    print(f"✅ Found {len(opportunities)} engagement opportunities")
    
    if opportunities:
        print(f"\n🔥 TOP 3 OPPORTUNITIES:")
        for i, opp in enumerate(opportunities[:3], 1):
            print(f"{i}. @{opp.member.profile.username}")
            print(f"   📊 Urgency: {opp.urgency_score:.1f}/10")
            print(f"   💰 Conversion: {opp.conversion_potential:.1f}/10")
            print(f"   📝 Content: \"{opp.content_text[:80]}...\"")
            print(f"   ⚡ Action: {opp.opportunity_type}")
    
    # 3. Community analytics
    print(f"\n📈 Community Analytics:")
    analytics = targeting.get_community_analytics()
    
    total_members = sum(item['count'] for item in analytics['community_composition'])
    print(f"   🏘️ Total Community: {total_members} members")
    
    funnel = analytics['conversion_funnel']
    print(f"   🎯 Conversion Funnel:")
    print(f"      • Prospects: {funnel['prospects']}")
    print(f"      • Engaged: {funnel['engaged']}")
    print(f"      • Active: {funnel['active']}")
    print(f"      • Advocates: {funnel['advocates']}")
    print(f"      • Customers: {funnel['customers']}")
    
    # 4. Growth projection
    print(f"\n🚀 GROWTH PROJECTION (4 weeks):")
    print(f"   📊 Week 1 Target: 50 followers, 350 engagements, 5 demos")
    print(f"   📈 Week 2 Target: 150 followers, 490 engagements, 10 demos") 
    print(f"   🎯 Week 3 Target: 300 followers, 630 engagements, 20 demos")
    print(f"   💰 Week 4 Target: 500 followers, 700 engagements, 30 demos")
    
    print(f"\n✅ SYSTEM READY - Key Features:")
    print(f"   🔍 Intelligent influencer discovery & scoring")
    print(f"   🎯 Automated engagement opportunity identification")
    print(f"   💬 Smart response generation")
    print(f"   📊 Relationship lifecycle management")
    print(f"   💰 Conversion-focused community building")
    print(f"   📈 Comprehensive analytics & reporting")
    
    print(f"\n🎉 Ready to build SME Analytica's community!")

if __name__ == "__main__":
    asyncio.run(main())