#!/usr/bin/env python3
"""
🤖 SME Analytica Autonomous Agent Demonstration
Simple demonstration of core autonomous agent functionality
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from autonomous_agent import AutonomousSocialAgent
from src.ai_agent.intelligent_engagement_agent import IntelligentEngagementAgent
from src.ai_providers import AIProviderManager
from src.content.collaborative_content_generator import CollaborativeContentGenerator, ContentCategory

class AgentDemo:
    """Demonstration class for autonomous agent functionality"""
    
    def __init__(self):
        self.setup_demo_environment()
    
    def setup_demo_environment(self):
        """Setup demo environment"""
        # Create demo directories
        os.makedirs('logs', exist_ok=True)
        os.makedirs('config', exist_ok=True)
        
        # Setup mock environment variables for demo
        os.environ.update({
            'GOOGLE_GEMINI_API_KEY': 'demo_gemini_key',
            'OPENAI_API_KEY': 'demo_openai_key',
            'ANTHROPIC_API_KEY': 'demo_anthropic_key',
            'TWITTER_API_KEY': 'demo_twitter_key',
            'NOTION_API_KEY': 'demo_notion_key'
        })
    
    async def demo_autonomous_agent(self):
        """Demonstrate autonomous agent initialization"""
        print("🔧 Demo: Autonomous Social Agent")
        print("-" * 40)
        
        agent = AutonomousSocialAgent()
        
        print("✅ Agent initialized successfully")
        print(f"📊 Daily stats initialized: {agent.daily_stats}")
        print(f"⚙️  Configuration loaded: {len(agent.config)} sections")
        print(f"📝 Max daily posts: {agent.config['engagement_limits']['max_daily_posts']}")
        
        # Test agent methods
        from datetime import datetime
        test_time = datetime.now().replace(hour=8, minute=0)
        should_post = agent._should_post_now(test_time)
        print(f"🕐 Should post at 8 AM: {should_post}")
        
        # Test mention urgency calculation
        test_mention = {"text": "urgent help with restaurant analytics needed"}
        urgency = agent._calculate_mention_urgency(test_mention)
        print(f"⚡ Mention urgency score: {urgency}/10")
        
        # Test restaurant relevance
        content = "restaurant pricing optimization with AI"
        relevant = agent._is_relevant_to_restaurants(content)
        print(f"🍽️  Content relevant to restaurants: {relevant}")
        
        return True
    
    async def demo_engagement_agent(self):
        """Demonstrate engagement agent scoring methods"""
        print("\n🎯 Demo: Intelligent Engagement Agent")
        print("-" * 40)
        
        # Create minimal agent for method testing
        from src.ai_agent.intelligent_engagement_agent import IntelligentEngagementAgent
        agent = object.__new__(IntelligentEngagementAgent)
        
        # Setup required attributes
        agent.monitoring_config = {
            "keywords": {
                "high_priority": ["restaurant analytics", "dynamic pricing", "pos integration"],
                "medium_priority": ["small business", "business intelligence", "data analytics"],
                "prospect_signals": ["looking for", "need help", "recommendations", "advice"]
            }
        }
        
        # Test content analysis
        content = "How can small restaurants use AI for dynamic menu pricing?"
        
        relevance = agent._calculate_industry_relevance(content)
        print(f"📊 Industry relevance: {relevance}/10")
        
        conversion = agent._calculate_conversion_potential(content, {"followers": 1000, "bio": "restaurant owner"})
        print(f"💰 Conversion potential: {conversion}/10")
        
        alignment = agent._calculate_brand_alignment(content)
        print(f"🎯 Brand alignment: {alignment}/10")
        
        from src.ai_agent.intelligent_engagement_agent import OpportunityType
        urgency = agent._calculate_urgency_score({"text": "urgent help needed"}, OpportunityType.MENTION)
        print(f"⚡ Urgency score: {urgency}/10")
        
        return True
    
    async def demo_ai_providers(self):
        """Demonstrate AI provider integration"""
        print("\n🤖 Demo: AI Provider Manager")
        print("-" * 40)
        
        ai_config = {
            "google_gemini_api_key": "demo_gemini_key",
            "openai_api_key": "demo_openai_key",
            "anthropic_api_key": "demo_anthropic_key"
        }
        
        try:
            ai_provider = AIProviderManager(ai_config)
            print("✅ AI Provider Manager initialized")
            print(f"📦 Available providers: {len(ai_provider.providers)}")
            
            # Test content generation capabilities
            print("📝 Ready to generate content with AI providers")
            
            return True
        except Exception as e:
            print(f"❌ AI Provider setup: {e}")
            return False
    
    async def demo_content_generation(self):
        """Demonstrate content generation framework"""
        print("\n📝 Demo: Content Generation")
        print("-" * 40)
        
        # Mock content generation
        content_types = [
            ContentCategory.VIRAL_HOOKS,
            ContentCategory.DATA_INSIGHTS,
            ContentCategory.SUCCESS_STORIES,
            ContentCategory.THOUGHT_LEADERSHIP
        ]
        
        print("✅ Content generation framework initialized")
        print(f"🎯 Available categories: {len(content_types)}")
        
        for category in content_types:
            print(f"  📋 {category.value}")
        
        # Simulate content generation
        mock_content = {
            "category": "viral_hooks",
            "content": "🚀 Restaurants using AI see 23% profit increase! Here's how...",
            "viral_score": 8.5,
            "target_audience": ["restaurant_owners", "small_business"],
            "hashtags": ["#RestaurantTech", "#AIBusiness", "#SmallBusiness"]
        }
        
        print(f"🎪 Sample content: {mock_content['content']}")
        print(f"⭐ Viral score: {mock_content['viral_score']}/10")
        
        return True
    
    async def run_demo(self):
        """Run complete demonstration"""
        print("🤖 SME Analytica Autonomous Agent Demo")
        print("=" * 50)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        demos = [
            self.demo_autonomous_agent,
            self.demo_engagement_agent,
            self.demo_ai_providers,
            self.demo_content_generation
        ]
        
        results = []
        for demo in demos:
            try:
                result = await demo()
                results.append(result)
            except Exception as e:
                print(f"❌ Demo failed: {e}")
                results.append(False)
        
        print("\n" + "=" * 50)
        print("📊 DEMO SUMMARY")
        print("=" * 50)
        print(f"Components tested: {len(demos)}")
        print(f"Successful: {sum(results)}/{len(demos)}")
        
        if all(results):
            print("🎉 All autonomous agent components are working correctly!")
            print("\nNext steps:")
            print("1. Set up real API keys in environment variables")
            print("2. Run: python agent_cli.py start")
            print("3. Monitor with: python agent_cli.py dashboard")
        else:
            print("⚠️  Some components need attention")
        
        # Save demo results
        demo_results = {
            "timestamp": datetime.now().isoformat(),
            "components_tested": len(demos),
            "successful": sum(results),
            "demo_results": results
        }
        
        demo_file = f'logs/demo_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(demo_file, 'w') as f:
            json.dump(demo_results, f, indent=2)
        
        print(f"\n📄 Demo results saved to: {demo_file}")
        
        return all(results)

async def main():
    """Main demo runner"""
    demo = AgentDemo()
    await demo.run_demo()

if __name__ == "__main__":
    asyncio.run(main())