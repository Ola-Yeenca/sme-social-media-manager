#!/usr/bin/env python3
"""
Enhanced Content Strategy for SME Analytica Growth
Implements aggressive growth tactics and engagement strategies
"""

import os
import sys
import asyncio
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Load environment variables
load_dotenv()

# Unset the shell environment variable to use .env file
if 'SOCIAL_MEDIA_DB_ID' in os.environ:
    del os.environ['SOCIAL_MEDIA_DB_ID']

class EnhancedContentStrategy:
    """Enhanced content strategy for aggressive growth"""
    
    def __init__(self):
        self.content_pillars = {
            "educational": 0.40,  # Teaching business analytics
            "promotional": 0.20,  # SME Analytica features
            "community": 0.25,    # Engaging with audience
            "industry": 0.15      # Market trends and insights
        }
        
        self.posting_schedule = {
            "daily_posts": 6,  # Increased from 3 to 6
            "optimal_times": [
                {"hour": 8, "minute": 0},   # Morning commute
                {"hour": 10, "minute": 30}, # Mid-morning break
                {"hour": 12, "minute": 0},  # Lunch break
                {"hour": 15, "minute": 0},  # Afternoon break
                {"hour": 17, "minute": 30}, # End of workday
                {"hour": 19, "minute": 0}   # Evening engagement
            ]
        }
        
        self.content_types = {
            "educational_threads": [
                "🧵 THREAD: 5 Ways to Increase Restaurant Revenue with Data Analytics",
                "🧵 THREAD: How to Read Your Business Analytics Dashboard",
                "🧵 THREAD: Dynamic Pricing Strategies for Small Businesses",
                "🧵 THREAD: Customer Behavior Analytics 101",
                "🧵 THREAD: Inventory Management with AI"
            ],
            "quick_tips": [
                "💡 Quick Tip: Track your peak hours to optimize staffing costs",
                "💡 Quick Tip: Use customer data to create targeted promotions",
                "💡 Quick Tip: Monitor competitor pricing for better positioning",
                "💡 Quick Tip: Analyze seasonal trends to plan inventory",
                "💡 Quick Tip: Track customer lifetime value to focus retention"
            ],
            "industry_stats": [
                "📊 STAT: 73% of restaurants that use data analytics see 15%+ revenue growth",
                "📊 STAT: Small businesses using dynamic pricing increase profits by 25%",
                "📊 STAT: 68% of customers prefer businesses that personalize their experience",
                "📊 STAT: Data-driven restaurants reduce food waste by 30%",
                "📊 STAT: 82% of successful SMEs use analytics for decision making"
            ],
            "engagement_posts": [
                "🤔 QUESTION: What's your biggest challenge with business analytics?",
                "🗳️ POLL: Which metric do you track most? Revenue | Customers | Inventory | Other",
                "💬 DISCUSSION: How do you currently track customer preferences?",
                "🎯 CHALLENGE: Share your best data-driven business decision!",
                "🤝 COMMUNITY: Tag a fellow business owner who needs better analytics!"
            ],
            "success_stories": [
                "🏆 SUCCESS: Local café increased revenue 40% using our analytics insights",
                "🏆 SUCCESS: Restaurant chain optimized menu pricing, saved $50K annually",
                "🏆 SUCCESS: Retail store improved inventory turnover by 60%",
                "🏆 SUCCESS: Hotel increased occupancy rates by 25% with dynamic pricing",
                "🏆 SUCCESS: Food truck doubled profits using location analytics"
            ],
            "feature_highlights": [
                "⚡ FEATURE: Real-time dashboard shows live business metrics",
                "⚡ FEATURE: AI-powered pricing recommendations update hourly",
                "⚡ FEATURE: Customer segmentation identifies your best clients",
                "⚡ FEATURE: Predictive analytics forecasts demand trends",
                "⚡ FEATURE: Automated reports save 10+ hours weekly"
            ]
        }
        
        self.hashtag_sets = {
            "primary": ["#SMEAnalytica", "#BusinessAnalytics", "#SmallBusiness"],
            "restaurant": ["#RestaurantTech", "#MenuFlow", "#HospitalityAI", "#FoodService"],
            "retail": ["#RetailAnalytics", "#InventoryManagement", "#RetailTech"],
            "general": ["#DataDriven", "#BusinessGrowth", "#Entrepreneurship", "#StartupLife"],
            "trending": ["#AI", "#MachineLearning", "#DigitalTransformation", "#Innovation"]
        }

    def generate_enhanced_content(self, content_type, vertical="general"):
        """Generate enhanced content based on type and vertical"""
        
        content_templates = {
            "educational_thread": {
                "restaurant": [
                    "🧵 THREAD: How to use analytics to optimize your restaurant menu\n\n1/ Start by tracking which dishes sell best during different times\n2/ Analyze profit margins per dish\n3/ Use customer feedback data\n4/ Implement dynamic pricing\n5/ Monitor competitor pricing\n\n#RestaurantTech #MenuOptimization",
                    "🧵 THREAD: 5 Restaurant Analytics Metrics That Actually Matter\n\n1/ Table turnover rate\n2/ Average order value\n3/ Customer lifetime value\n4/ Food cost percentage\n5/ Peak hour efficiency\n\nTrack these to grow your business! #RestaurantAnalytics"
                ],
                "retail": [
                    "🧵 THREAD: Retail Analytics That Drive Sales\n\n1/ Track inventory turnover rates\n2/ Monitor customer purchase patterns\n3/ Analyze seasonal trends\n4/ Optimize pricing strategies\n5/ Measure marketing ROI\n\n#RetailAnalytics #BusinessGrowth",
                    "🧵 THREAD: How to Use Data to Reduce Retail Waste\n\n1/ Predict demand accurately\n2/ Optimize inventory levels\n3/ Track expiration dates\n4/ Analyze customer preferences\n5/ Implement dynamic discounting\n\n#RetailTech #Sustainability"
                ]
            },
            "engagement_question": [
                "🤔 Restaurant owners: What's your biggest challenge with managing inventory? Share below! 👇",
                "💬 Small business owners: How do you currently track your best customers?",
                "🗳️ POLL: Which business metric do you check first each morning?",
                "🎯 What's one business decision you wish you had more data for?",
                "🤝 Tag a fellow entrepreneur who could benefit from better business analytics!"
            ],
            "value_tip": [
                "💡 PRO TIP: Your slowest-selling items might be your most profitable. Check your margins, not just volume! #BusinessTip",
                "💡 INSIGHT: Customers who visit during off-peak hours often have higher lifetime value. Target them! #CustomerAnalytics",
                "💡 STRATEGY: Use weather data to predict demand. Rainy days = more delivery orders! #PredictiveAnalytics",
                "💡 HACK: Track customer complaints by category. The most common issue is your biggest growth opportunity! #CustomerService"
            ],
            "industry_insight": [
                "📊 INDUSTRY INSIGHT: 67% of restaurants that use analytics see 20%+ profit increases within 6 months. Are you part of the 67%? #RestaurantAnalytics",
                "📈 MARKET TREND: Dynamic pricing is becoming standard in hospitality. Early adopters see 15-30% revenue boosts! #DynamicPricing",
                "🔍 RESEARCH: Small businesses using AI analytics are 3x more likely to survive economic downturns. #AIforBusiness",
                "📊 DATA POINT: The average restaurant loses $50K annually due to poor inventory management. Analytics can fix this! #InventoryManagement"
            ]
        }
        
        # Select appropriate content based on type and vertical
        if content_type in content_templates:
            if vertical in content_templates[content_type]:
                return random.choice(content_templates[content_type][vertical])
            else:
                # Fallback to general content
                return random.choice(content_templates[content_type])
        
        return None

    def get_optimal_hashtags(self, content_type, vertical="general"):
        """Get optimal hashtags for content type and vertical"""
        
        hashtags = self.hashtag_sets["primary"].copy()
        
        if vertical == "restaurant":
            hashtags.extend(self.hashtag_sets["restaurant"][:2])
        elif vertical == "retail":
            hashtags.extend(self.hashtag_sets["retail"][:2])
        else:
            hashtags.extend(self.hashtag_sets["general"][:2])
        
        # Add trending hashtags occasionally
        if random.random() < 0.3:  # 30% chance
            hashtags.extend(random.sample(self.hashtag_sets["trending"], 1))
        
        return hashtags[:8]  # Limit to 8 hashtags

    def create_daily_content_plan(self):
        """Create a comprehensive daily content plan"""
        
        today = datetime.now()
        content_plan = []
        
        # Determine content distribution based on pillars
        content_distribution = [
            ("educational", 2),  # 2 educational posts
            ("community", 2),    # 2 engagement posts  
            ("promotional", 1),  # 1 promotional post
            ("industry", 1)      # 1 industry insight
        ]
        
        post_index = 0
        for category, count in content_distribution:
            for i in range(count):
                if post_index < len(self.posting_schedule["optimal_times"]):
                    time_slot = self.posting_schedule["optimal_times"][post_index]
                    
                    # Determine vertical (restaurant focus for now)
                    vertical = random.choice(["restaurant", "retail", "general"])
                    
                    # Generate content based on category
                    if category == "educational":
                        content_type = random.choice(["educational_thread", "value_tip"])
                    elif category == "community":
                        content_type = "engagement_question"
                    elif category == "promotional":
                        content_type = "feature_highlight"
                    else:  # industry
                        content_type = "industry_insight"
                    
                    content = self.generate_enhanced_content(content_type, vertical)
                    hashtags = self.get_optimal_hashtags(content_type, vertical)
                    
                    scheduled_time = today.replace(
                        hour=time_slot["hour"],
                        minute=time_slot["minute"],
                        second=0,
                        microsecond=0
                    )
                    
                    # If time has passed, schedule for tomorrow
                    if scheduled_time <= datetime.now():
                        scheduled_time += timedelta(days=1)
                    
                    content_plan.append({
                        "content": content,
                        "hashtags": hashtags,
                        "scheduled_time": scheduled_time,
                        "category": category,
                        "content_type": content_type,
                        "vertical": vertical
                    })
                    
                    post_index += 1
        
        return content_plan


async def generate_enhanced_daily_content():
    """Generate enhanced daily content using the new strategy"""
    
    print("🚀 Enhanced SME Analytica Content Generation")
    print("=" * 60)
    
    try:
        from notion import NotionManager, SocialMediaPost, PostStatus, Platform, PostType
        
        # Initialize components
        notion_manager = NotionManager()
        strategy = EnhancedContentStrategy()
        
        print("✅ Components initialized")
        print(f"📊 Strategy: {strategy.posting_schedule['daily_posts']} posts/day")
        print(f"🎯 Content Pillars: Educational (40%), Community (25%), Promotional (20%), Industry (15%)")
        
        # Generate daily content plan
        content_plan = strategy.create_daily_content_plan()
        
        print(f"\n📋 Generating {len(content_plan)} enhanced posts...")
        
        created_posts = []
        
        for i, plan in enumerate(content_plan, 1):
            print(f"\n{i}. Creating {plan['category']} post...")
            print(f"   Type: {plan['content_type']}")
            print(f"   Vertical: {plan['vertical']}")
            print(f"   Time: {plan['scheduled_time'].strftime('%H:%M')}")
            
            # Create enhanced post
            post = SocialMediaPost(
                name=f"SME Analytica - {plan['category'].title()} {datetime.now().strftime('%Y-%m-%d')} #{i}",
                content=plan['content'],
                status=PostStatus.SCHEDULED,
                platform=Platform.TWITTER,
                post_type=PostType.INFORMATIONAL,
                scheduled_time=plan['scheduled_time'],
                language="English",
                content_theme=plan['category'],
                ai_provider_used="Enhanced Strategy",
                tags=plan['hashtags']
            )
            
            # Save to Notion
            post_id = notion_manager.create_post(post)
            
            if post_id:
                print(f"   ✅ Created: {plan['content'][:50]}...")
                created_posts.append({
                    "id": post_id,
                    "category": plan['category'],
                    "time": plan['scheduled_time']
                })
            else:
                print(f"   ❌ Failed to create post")
        
        # Summary
        print(f"\n" + "=" * 60)
        print(f"🎉 Enhanced Content Generation Complete!")
        print(f"📊 Created: {len(created_posts)} posts")
        print(f"📅 Scheduled over: {len(set(p['time'].hour for p in created_posts))} time slots")
        
        # Show breakdown by category
        categories = {}
        for post in created_posts:
            cat = post['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        print(f"\n📋 Content Breakdown:")
        for category, count in categories.items():
            print(f"   • {category.title()}: {count} posts")
        
        return len(created_posts)
        
    except Exception as e:
        print(f"❌ Error generating enhanced content: {e}")
        import traceback
        traceback.print_exc()
        return 0


if __name__ == "__main__":
    asyncio.run(generate_enhanced_daily_content())
