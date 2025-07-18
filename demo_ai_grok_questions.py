#!/usr/bin/env python3
"""
Demo of AI-Generated Grok Questions
Shows how the system generates dynamic questions without hitting Twitter API
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add the project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

async def demo_ai_grok_questions():
    """Demo the AI-generated Grok questions"""
    
    print("🤖 SME Analytica AI-Generated Grok Questions Demo")
    print("=" * 55)
    
    try:
        # Import required modules
        from src.ai_providers import AIProviderManager, ContentRequest, ContentType
        import os
        
        print("✅ Successfully imported AI providers")
        
        # Initialize AI manager
        ai_config = {
            "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
            "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY", ""),
            "perplexity_api_key": os.getenv("PERPLEXITY_API_KEY", ""),
            "grok_api_key": os.getenv("GROK_API_KEY", ""),
            "google_gemini_api_key": os.getenv("GOOGLE_GEMINI_API_KEY", "")
        }
        
        ai_manager = AIProviderManager(ai_config)
        print("✅ AI manager initialized")
        
        # Demo question categories and contexts
        question_scenarios = [
            {
                "category": "restaurant_analytics",
                "audience": "restaurant owners during lunch rush",
                "time": "2:00 PM",
                "topics": ["menu pricing", "customer flow", "profit margins"],
                "hashtags": ["#RestaurantAnalytics", "#FoodBusiness", "#RestaurantTech"]
            },
            {
                "category": "sme_insights", 
                "audience": "small business owners starting their day",
                "time": "9:00 AM",
                "topics": ["business intelligence", "growth strategies", "data analytics"],
                "hashtags": ["#SmallBusiness", "#SMEAnalytics", "#BusinessIntelligence"]
            },
            {
                "category": "data_trends",
                "audience": "business professionals and analysts",
                "time": "7:00 PM", 
                "topics": ["AI in business", "predictive analytics", "automation"],
                "hashtags": ["#DataAnalytics", "#AIforBusiness", "#PredictiveAnalytics"]
            }
        ]
        
        print("\n🧠 Generating AI-Powered Grok Questions:")
        print("(These would be posted to Twitter mentioning @grok)")
        
        for i, scenario in enumerate(question_scenarios, 1):
            print(f"\n📅 Scenario {i}: {scenario['time']} - {scenario['category'].replace('_', ' ').title()}")
            print(f"   Target Audience: {scenario['audience']}")
            
            # Create AI prompt for question generation
            prompt = f"""
            Generate a strategic question to ask @grok on Twitter that will generate valuable engagement for SME Analytica.

            Context:
            - SME Analytica provides AI-driven analytics for restaurants, hotels, and retail businesses
            - We specialize in menu optimization, dynamic pricing, customer flow analysis, and business intelligence
            - Target audience: {scenario['audience']}
            - Category: {scenario['category'].replace('_', ' ')}
            - Relevant topics: {', '.join(scenario['topics'])}

            IMPORTANT STYLE REQUIREMENTS:
            - Acknowledge that @grok is an AI (e.g., "if you were a restaurant owner", "from an AI perspective")
            - Structure as: Question to @grok + Our solution/expertise + Follow-up question to @grok
            - Be conversational and natural
            - Position SME Analytica as the helpful expert with solutions
            - Make it feel like a genuine conversation between AIs about helping businesses

            PERFECT EXAMPLE FORMAT:
            "@grok do Restaurant owners ever wonder how much profit they're leaving on the table during their busiest hours?

            Wanna help them explain how with our dynamic menu pricing and flow analytics, they could be capturing 10%+ higher margins when demand peaks.

            Also, @grok what is your strategy for maximizing revenue when things get hectic, if you were a restaurant owner?"

            Generate a question following this EXACT conversational style and structure:
            1. "@grok do [target audience] ever [question about their challenge]?"
            2. "Wanna help them explain how with our [SME Analytica solution], they could [benefit]."
            3. "Also, @grok what is your [related question], if you were a [target role]?"

            Keep it natural, conversational, and helpful. Maximum 280 characters total.
            """
            
            try:
                # Create content request
                content_request = ContentRequest(
                    content_type=ContentType.TWEET,
                    language='en',
                    theme=f'grok_question_{scenario["category"]}',
                    max_length=200,
                    context={
                        'prompt': prompt,
                        'category': scenario['category'],
                        'audience': scenario['audience'],
                        'topics': scenario['topics']
                    }
                )
                
                # Generate the question
                print("   🤖 Generating AI question...")
                generated_content = await ai_manager.generate_content(content_request)
                
                if generated_content and generated_content.text:
                    question_text = generated_content.text.strip()
                    
                    # Clean up the question
                    if question_text.startswith('"') and question_text.endswith('"'):
                        question_text = question_text[1:-1]
                    
                    # Add @grok mention if not present
                    if '@grok' not in question_text.lower():
                        question_text = f"@grok {question_text}"
                    
                    # Show the complete tweet
                    hashtags_text = " ".join(scenario['hashtags'])
                    full_tweet = f"{question_text}\n\n{hashtags_text}"
                    
                    print(f"   ✅ Generated Question:")
                    print(f"      {question_text}")
                    print(f"   📝 Full Tweet ({len(full_tweet)} chars):")
                    print(f"      {full_tweet}")
                    print(f"   🎯 Expected Result:")
                    print(f"      • Grok responds with insights")
                    print(f"      • SME Analytica adds expert follow-up")
                    print(f"      • Community joins discussion")
                    print(f"      • Organic engagement and follower growth")
                    
                else:
                    print(f"   ❌ Failed to generate question")
                    
            except Exception as e:
                print(f"   ❌ Error generating question: {e}")
                # Show fallback approach
                fallback_questions = {
                    "restaurant_analytics": "What's the one restaurant metric that always surprises new owners?",
                    "sme_insights": "What's the biggest analytics mistake small businesses make?", 
                    "data_trends": "Why do businesses collect data but still make gut decisions?"
                }
                fallback = fallback_questions.get(scenario['category'], "What's your biggest business analytics challenge?")
                print(f"   🔄 Fallback question: @grok {fallback}")
        
        print("\n🎯 Key Benefits of AI-Generated Questions:")
        print("  ✅ Dynamic and contextual (not repetitive)")
        print("  ✅ Adapts to time of day and audience")
        print("  ✅ Maintains SME Analytica's expertise focus")
        print("  ✅ Professional yet engaging tone")
        print("  ✅ Optimized for Twitter engagement")
        print("  ✅ Generates valuable business discussions")
        
        print("\n🚀 How It Works in Production:")
        print("  1. System determines optimal question category based on time")
        print("  2. AI generates strategic question about SME Analytica's expertise")
        print("  3. Posts to Twitter mentioning @grok with relevant hashtags")
        print("  4. Grok (Twitter's AI) responds automatically")
        print("  5. SME Analytica adds expert follow-up insights")
        print("  6. Community engages, creating organic growth")
        print("  7. All interactions tracked in Notion database")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Note: This demo requires AI provider modules to be available")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print(f"🕐 Starting demo at {datetime.now()}")
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("Note: dotenv not available, using system environment variables")
    
    # Run demo
    asyncio.run(demo_ai_grok_questions())
    
    print(f"\n🕐 Demo completed at {datetime.now()}")
    print("\n🎉 AI-Generated Grok Questions are ready!")
    print("Run the full system with: python main.py --mode=engagement")
