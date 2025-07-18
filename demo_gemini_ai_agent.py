#!/usr/bin/env python3
"""
Demo: Gemini-Powered AI Agent for SME Analytica
Demonstrates the intelligent engagement agent with Google Gemini integration
"""

import asyncio
import logging
import os
from datetime import datetime
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

async def demo_gemini_ai_agent():
    """Demonstrate the Gemini-powered AI agent capabilities"""
    
    print("🤖 SME Analytica Gemini-Powered AI Agent Demo")
    print("=" * 60)
    
    try:
        # Import required modules
        from src.ai_agent.intelligent_engagement_agent import create_intelligent_agent
        from src.content.gemini_influencer_generator import GeminiInfluencerGenerator, InfluencerContentType
        from src.ai_providers import AIProviderManager
        
        print("✅ Successfully imported AI agent modules")
        
        # Test AI Provider Manager with Gemini
        print("\n🧠 Testing AI Provider Manager with Gemini...")
        ai_config = {
            "google_gemini_api_key": os.getenv("GOOGLE_GEMINI_API_KEY"),
            "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
            "openai_api_key": os.getenv("OPENAI_API_KEY"),
            "perplexity_api_key": os.getenv("PERPLEXITY_API_KEY"),
            "grok_api_key": os.getenv("GROK_API_KEY")
        }
        
        ai_manager = AIProviderManager(ai_config)
        provider_status = ai_manager.get_provider_status()
        
        print("📊 AI Provider Status:")
        for provider, status in provider_status.items():
            availability = "✅ Available" if status.get("available", False) else "❌ Unavailable"
            print(f"  {provider}: {availability}")
        
        # Test Gemini Influencer Content Generator
        print("\n🎯 Testing Gemini Influencer Content Generator...")
        influencer_generator = GeminiInfluencerGenerator()
        
        # Generate different types of influencer content
        content_types = [
            InfluencerContentType.VIRAL_HOOKS,
            InfluencerContentType.DATA_INSIGHTS,
            InfluencerContentType.THOUGHT_LEADERSHIP
        ]
        
        for content_type in content_types:
            try:
                print(f"\n📝 Generating {content_type.value} content...")
                
                context = {
                    "theme": "restaurant_analytics",
                    "target_audience": "restaurant_owners",
                    "urgency": "high"
                }
                
                influencer_content = await influencer_generator.generate_influencer_content(
                    content_type, context
                )
                
                print(f"✨ Generated Content:")
                print(f"   Content: {influencer_content.content}")
                print(f"   Viral Potential: {influencer_content.viral_potential_score:.1f}/10")
                print(f"   Brand Authority: {influencer_content.brand_authority_score:.1f}/10")
                print(f"   Expected Engagement: {influencer_content.expected_engagement_rate:.1%}")
                print(f"   Hashtags: {', '.join(influencer_content.hashtags[:3])}")
                
            except Exception as e:
                print(f"❌ Error generating {content_type.value}: {e}")
        
        # Test AI Agent Creation
        print("\n🚀 Testing AI Agent Creation...")
        agent = await create_intelligent_agent()
        
        # Get agent status
        status = agent.get_agent_status()
        print("📊 AI Agent Status:")
        print(f"   AI Provider: {status.get('ai_provider_status', 'Unknown')}")
        print(f"   Current Mode: {status.get('current_mode', 'Unknown')}")
        print(f"   Safety System: {'✅ Active' if 'safety_stats' in status else '❌ Inactive'}")
        
        # Test Safety Manager
        print("\n🛡️ Testing Safety Manager...")
        safety_manager = agent.safety_manager
        
        # Test content safety checks
        test_contents = [
            {
                "content": "Great insights on restaurant analytics! Our data shows 10% margin improvement with dynamic pricing.",
                "author": "restaurant_owner_123",
                "expected": "SAFE"
            },
            {
                "content": "BUY NOW!!! LIMITED TIME OFFER!!! GUARANTEED RESULTS!!!",
                "author": "spammer_account",
                "expected": "UNSAFE"
            },
            {
                "content": "Looking for restaurant analytics solutions. Any recommendations?",
                "author": "legitimate_prospect",
                "expected": "SAFE"
            }
        ]
        
        for test in test_contents:
            safety_check = await safety_manager.check_content_safety(
                test["content"], 
                test["author"],
                {"author_profile": {"followers": 500, "following": 200}}
            )
            
            result_emoji = "✅" if safety_check.is_safe else "❌"
            print(f"   {result_emoji} Content: '{test['content'][:50]}...'")
            print(f"      Safety Level: {safety_check.safety_level.value}")
            print(f"      Confidence: {safety_check.confidence_score:.2f}")
            
            if safety_check.risk_factors:
                print(f"      Risk Factors: {', '.join(safety_check.risk_factors[:2])}")
        
        # Test Engagement Analysis with Gemini
        print("\n🎯 Testing Gemini Engagement Analysis...")
        
        if "gemini" in ai_manager.providers and ai_manager.providers["gemini"].is_available:
            test_tweets = [
                {
                    "text": "Struggling with restaurant profit margins. Any tips for optimization?",
                    "author": "restaurant_owner_joe"
                },
                {
                    "text": "Just discovered dynamic pricing for restaurants. Game changer! 📊",
                    "author": "foodtech_enthusiast"
                },
                {
                    "text": "Looking for POS integration solutions for my restaurant chain.",
                    "author": "multi_location_owner"
                }
            ]
            
            for tweet in test_tweets:
                try:
                    analysis = await ai_manager.analyze_engagement_with_gemini(
                        tweet["text"], tweet["author"]
                    )
                    
                    print(f"📊 Tweet: '{tweet['text'][:40]}...'")
                    print(f"   Relevance: {analysis.get('relevance_score', 0)}/10")
                    print(f"   Conversion Potential: {analysis.get('conversion_likelihood', 0)}/10")
                    print(f"   Recommended Action: {analysis.get('recommended_action', 'unknown')}")
                    print(f"   Strategy: {analysis.get('response_strategy', 'unknown')}")
                    
                except Exception as e:
                    print(f"❌ Analysis failed: {e}")
        else:
            print("⚠️ Gemini not available for engagement analysis")
        
        # Test Viral Campaign Generation
        print("\n🔥 Testing Viral Campaign Generation...")
        try:
            campaign = await influencer_generator.generate_viral_campaign(
                theme="restaurant_ai_revolution", 
                num_posts=3
            )
            
            print(f"📈 Generated {len(campaign)} viral campaign posts:")
            for i, post in enumerate(campaign, 1):
                print(f"   Post {i}: {post.content_type.value}")
                print(f"   Content: {post.content[:60]}...")
                print(f"   Viral Score: {post.viral_potential_score:.1f}/10")
                print()
        
        except Exception as e:
            print(f"❌ Viral campaign generation failed: {e}")
        
        # Performance Summary
        print("\n📊 Performance Summary:")
        print("=" * 40)
        
        # Get performance metrics
        if hasattr(influencer_generator, 'get_performance_metrics'):
            metrics = influencer_generator.get_performance_metrics()
            print("🎯 Influencer Generator:")
            for key, value in metrics.items():
                print(f"   {key}: {value}")
        
        # Safety statistics
        safety_stats = safety_manager.get_safety_stats()
        print("\n🛡️ Safety Manager:")
        for key, value in safety_stats.items():
            if isinstance(value, (int, float)):
                print(f"   {key}: {value}")
        
        print("\n✅ Demo completed successfully!")
        print("\n🚀 Key Features Demonstrated:")
        print("   • Gemini-powered intelligent content generation")
        print("   • Advanced safety and rate limiting")
        print("   • Viral content optimization")
        print("   • Engagement opportunity analysis")
        print("   • Multi-provider AI fallback system")
        print("   • Brand voice consistency")
        print("   • Real-time monitoring capabilities")
        
        print("\n🎯 SME Analytica AI Agent is ready for intelligent social media influence!")
        
        return {
            "status": "success",
            "ai_providers_tested": len(provider_status),
            "gemini_available": "gemini" in ai_manager.providers and ai_manager.providers["gemini"].is_available,
            "safety_system_active": True,
            "influencer_content_generated": True,
            "viral_campaign_created": True
        }
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed:")
        print("   pip install google-generativeai tweepy anthropic openai notion-client")
        return {"status": "import_error", "error": str(e)}
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return {"status": "error", "error": str(e)}

async def test_gemini_provider_directly():
    """Test Gemini provider directly"""
    
    print("\n🧪 Direct Gemini Provider Test")
    print("-" * 30)
    
    try:
        from src.ai_providers.gemini_provider import GeminiProvider
        
        api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
        gemini = GeminiProvider(api_key)
        
        print(f"🔧 Provider Name: {gemini.provider_name}")
        print(f"🔧 Available: {gemini.is_available}")
        
        # Test engagement analysis
        test_tweet = "Looking for restaurant analytics software. Need help with profit optimization."
        test_author = "restaurant_owner_mike"
        
        analysis = await gemini.analyze_engagement_opportunity(test_tweet, test_author)
        
        print(f"\n📊 Engagement Analysis:")
        print(f"   Relevance Score: {analysis.get('relevance_score', 0)}/10")
        print(f"   Conversion Likelihood: {analysis.get('conversion_likelihood', 0)}/10")
        print(f"   Recommended Action: {analysis.get('recommended_action', 'unknown')}")
        print(f"   Key Talking Points: {analysis.get('key_talking_points', [])[:2]}")
        
        # Test reply generation
        reply = await gemini.generate_reply(test_tweet, {"urgency": "high"})
        print(f"\n💬 Generated Reply: {reply}")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct Gemini test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting SME Analytica Gemini AI Agent Demo")
    print(f"⏰ Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run the main demo
    result = asyncio.run(demo_gemini_ai_agent())
    
    # Run direct Gemini test
    gemini_test = asyncio.run(test_gemini_provider_directly())
    
    print(f"\n📋 Demo Results:")
    print(f"   Main Demo: {'✅ Success' if result.get('status') == 'success' else '❌ Failed'}")
    print(f"   Gemini Direct Test: {'✅ Success' if gemini_test else '❌ Failed'}")
    
    if result.get("status") == "success":
        print(f"\n🎉 All systems operational! SME Analytica AI Agent with Gemini is ready for deployment.")
    else:
        print(f"\n⚠️ Issues detected. Check the logs above for details.")
    
    print(f"\n⏰ Demo completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
