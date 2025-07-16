"""
Enhanced content generator with 4-week growth strategy optimization
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import random
import re
import sys
# Language detection with fallback
LANGDETECT_AVAILABLE = False
def detect(text):
    """Simple language detection fallback"""
    # Basic heuristic: if text contains Spanish keywords, return 'es'
    spanish_keywords = ['restaurantes', 'negocio', 'precios', 'datos', 'análisis']
    text_lower = text.lower()
    if any(keyword in text_lower for keyword in spanish_keywords):
        return 'es'
    return 'en'  # Default to English
import os
import asyncio
import json
from dataclasses import dataclass
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config.settings import SMEAnalyticaContext, ContentTheme, Language

class ContentCategory(str, Enum):
    EDUCATIONAL = "educational"
    PROMOTIONAL = "promotional" 
    INDUSTRY_NEWS = "industry_news"
    CASE_STUDY = "case_study"
    TIPS_AND_TRICKS = "tips_and_tricks"
    COMPANY_UPDATE = "company_update"
    ENGAGEMENT = "engagement"
    VIRAL_OPTIMIZED = "viral_optimized"
    GROWTH_FOCUSED = "growth_focused"
    INFLUENCER_TARGETED = "influencer_targeted"

class GrowthStrategy(str, Enum):
    FOLLOWER_ACQUISITION = "follower_acquisition"
    ENGAGEMENT_BOOST = "engagement_boost"
    BRAND_AWARENESS = "brand_awareness"
    CONVERSION_FOCUSED = "conversion_focused"
    VIRAL_POTENTIAL = "viral_potential"
    COMMUNITY_BUILDING = "community_building"

@dataclass
class ViralElements:
    """Elements that increase viral potential"""
    hooks: List[str]
    surprise_factors: List[str]
    emotional_triggers: List[str]
    shareability_factors: List[str]
    trending_angles: List[str]

@dataclass
class GrowthMetrics:
    """Track content performance for growth optimization"""
    engagement_rate: float
    virality_score: float
    conversion_potential: float
    brand_alignment: float
    growth_contribution: float

class GrowthOptimizedContentGenerator:
    """Advanced content generation engine with 4-week growth strategy"""
    
    def __init__(self):
        self.context = SMEAnalyticaContext()
        self.content_variables = self._initialize_content_variables()
        self.viral_elements = self._initialize_viral_elements()
        self.growth_strategies = self._initialize_growth_strategies()
        self.performance_tracker = {}
        self.trending_keywords = []
        self.optimal_posting_times = self._calculate_optimal_times()
    
    def _initialize_viral_elements(self) -> ViralElements:
        """Initialize viral content elements for maximum engagement"""
        return ViralElements(
            hooks=[
                "🚨 This will change how you think about restaurant pricing",
                "📊 The 10% secret that restaurant owners don't want you to know",
                "⚡ Why 87% of successful restaurants use AI pricing (and you should too)",
                "🔥 This one data insight increased a small café's revenue by 25%",
                "💡 The simple analytics trick that's saving restaurants thousands",
                "🎯 Stop guessing, start growing: The AI revolution for SMEs is here",
                "📈 From struggling to thriving: How data analytics transforms small businesses"
            ],
            surprise_factors=[
                "Your competitors are already using AI pricing (here's how to catch up)",
                "The hidden patterns in your POS data that reveal profit opportunities",
                "Why weekend data might be lying to you about your business performance",
                "The counterintuitive pricing strategy that boosts both volume AND margins",
                "3 restaurant analytics myths that are costing you money"
            ],
            emotional_triggers=[
                "fear_of_missing_out",
                "curiosity_gap",
                "success_aspiration",
                "problem_recognition",
                "competitive_advantage",
                "transformation_story"
            ],
            shareability_factors=[
                "practical_tips",
                "surprising_statistics",
                "relatable_struggles",
                "quick_wins",
                "industry_secrets",
                "success_stories"
            ],
            trending_angles=[
                "#AIRevolution in hospitality",
                "#SmallBusinessSuccess stories",
                "#DataDriven decision making",
                "#RestaurantTech innovation",
                "#BusinessIntelligence for SMEs"
            ]
        )
    
    def _initialize_growth_strategies(self) -> Dict[GrowthStrategy, Dict[str, Any]]:
        """Initialize 4-week growth strategies with specific tactics"""
        return {
            GrowthStrategy.FOLLOWER_ACQUISITION: {
                "week_1_target": 50,
                "week_2_target": 150,
                "week_3_target": 300,
                "week_4_target": 500,
                "tactics": [
                    "hashtag_optimization",
                    "influencer_engagement",
                    "community_participation",
                    "value_driven_content"
                ],
                "content_frequency": 4,  # posts per day
                "optimal_hashtags": [
                    "#SmallBusiness", "#RestaurantTech", "#AIforSMEs", "#BusinessIntelligence",
                    "#HospitalityTech", "#RetailAnalytics", "#DataInsights", "#MenuTech",
                    "#DynamicPricing", "#RestaurantAnalytics", "#SMEAnalytica"
                ]
            },
            GrowthStrategy.ENGAGEMENT_BOOST: {
                "engagement_target": 15,  # min engagement rate %
                "tactics": [
                    "questions_and_polls",
                    "controversial_takes",
                    "behind_the_scenes",
                    "user_generated_content",
                    "interactive_content"
                ],
                "response_time_target": 30,  # minutes
                "community_engagement_quota": 20  # engagements per day
            },
            GrowthStrategy.VIRAL_POTENTIAL: {
                "virality_score_target": 8,  # out of 10
                "tactics": [
                    "trending_topic_integration",
                    "surprise_statistics",
                    "counterintuitive_insights",
                    "shareworthy_graphics",
                    "thread_content"
                ],
                "optimal_timing": ["09:00", "13:00", "17:30", "21:00"]
            },
            GrowthStrategy.CONVERSION_FOCUSED: {
                "conversion_rate_target": 5,  # website visits per 100 views
                "tactics": [
                    "call_to_action_optimization",
                    "value_proposition_highlighting",
                    "social_proof_integration",
                    "urgency_creation",
                    "demo_invitations"
                ],
                "landing_page_mentions": True,
                "demo_requests_target": 10  # per week
            }
        }
    
    def _calculate_optimal_times(self) -> Dict[str, List[str]]:
        """Calculate optimal posting times for different audiences"""
        return {
            "restaurant_owners": ["08:30", "12:30", "17:00", "20:30"],  # Before/after service
            "hotel_managers": ["09:00", "14:00", "18:30"],  # Check-in/out times
            "retail_entrepreneurs": ["10:00", "15:00", "19:00"],  # Store operation hours
            "general_business": ["09:00", "13:00", "17:30", "21:00"],  # Standard business
            "international": ["06:00", "12:00", "15:00", "22:00"]  # Multiple timezones
        }
    
    def _initialize_content_variables(self) -> Dict[str, List[str]]:
        """Initialize enhanced content variables for growth-optimized templates"""
        
        return {
            "insights": [
                "AI-powered dynamic pricing can boost restaurant margins by ~10% during peak hours",
                "Real-time analytics help small businesses make data-driven decisions without complexity",
                "Vertical-specific modules deliver industry-tailored insights out of the box",
                "Seamless integration means no vendor switching, just supercharged analytics"
            ],
            "statistics": [
                "restaurants increase revenue 10% with dynamic pricing",
                "SMEs boost efficiency 25% with real-time analytics", 
                "business owners save 5 hours weekly with automated insights",
                "table turnover improve 15% with AI-driven recommendations"
            ],
            "data_tips": [
                "Track your busiest hours to optimize staffing and pricing",
                "Use customer feedback data to guide menu decisions",
                "Monitor competitor pricing to stay competitive",
                "Analyze seasonal trends to plan promotions"
            ],
            "tech_features": [
                "MenuFlow integrates seamlessly with existing POS systems",
                "Real-time dashboard updates without manual data entry",
                "AI pricing adjusts automatically based on demand patterns",
                "QR ordering system with built-in analytics tracking"
            ],
            "business_insights": [
                "Peak hour pricing optimization drives profitability",
                "Customer traffic patterns reveal hidden opportunities", 
                "Menu analytics identify top-performing items",
                "Real-time feedback helps improve service quality"
            ],
            "call_to_actions": [
                "Ready to boost your margins?",
                "Want to see how it works?",
                "Curious about your restaurant's potential?",
                "Transform your data into profits today"
            ],
            "target_audiences": [
                "restaurant owners",
                "hotel managers", 
                "retail store owners",
                "small business entrepreneurs",
                "hospitality professionals"
            ],
            "benefits": [
                "increase profitability",
                "optimize operations",
                "improve customer satisfaction",
                "make data-driven decisions",
                "boost efficiency"
            ],
            "viral_hooks": [
                "🚨 Restaurant owners: Your competitors are already using this",
                "📊 The $50,000 mistake 90% of restaurants make (and how to avoid it)",
                "⚡ This AI trick increased café revenue 25% in 60 days",
                "🔥 Why smart restaurants are ditching manual pricing forever",
                "💡 The hidden profit leak in your restaurant (check your POS data)"
            ],
            "growth_triggers": [
                "Ready to 10x your restaurant analytics?",
                "Join 500+ successful restaurant owners using AI pricing",
                "Stop leaving money on the table - optimize now",
                "Transform your data into profit today",
                "See why MenuFlow users increase margins by 10%"
            ],
            "social_proof": [
                "Join 500+ restaurants using MenuFlow",
                "Trusted by successful SME owners worldwide",
                "Proven results: 10% margin boost in peak hours",
                "Used by top-performing restaurants globally",
                "The analytics platform restaurant owners love"
            ],
            "urgency_creators": [
                "Limited beta access available",
                "Early adopter pricing ends soon",
                "Join the AI revolution before your competitors",
                "Don't wait - start optimizing today",
                "The future of restaurant pricing is here"
            ],
            "question_starters": [
                "What if you could increase margins by 10% without raising menu prices?",
                "How much revenue are you losing to poor pricing strategy?",
                "Ready to see what your data is really telling you?",
                "Want to know the secret to peak-hour profitability?",
                "Curious how AI can transform your restaurant operations?"
            ]
        }
    
    def generate_viral_optimized_content(self, theme: ContentTheme, growth_strategy: GrowthStrategy, 
                                       language: Language = Language.ENGLISH) -> Dict[str, Any]:
        """Generate content optimized for viral potential and growth"""
        
        # Select viral elements based on strategy
        viral_hook = random.choice(self.viral_elements.hooks)
        surprise_factor = random.choice(self.viral_elements.surprise_factors)
        
        # Growth strategy specific content
        strategy_config = self.growth_strategies[growth_strategy]
        
        if growth_strategy == GrowthStrategy.FOLLOWER_ACQUISITION:
            content_template = self._get_follower_acquisition_template(theme, language)
        elif growth_strategy == GrowthStrategy.ENGAGEMENT_BOOST:
            content_template = self._get_engagement_boost_template(theme, language)
        elif growth_strategy == GrowthStrategy.VIRAL_POTENTIAL:
            content_template = self._get_viral_potential_template(theme, language)
        else:
            content_template = self._get_conversion_focused_template(theme, language)
        
        # Generate enhanced variables
        variables = self._generate_growth_variables(theme, growth_strategy, language)
        
        # Format content
        content = content_template.format(**variables)
        
        # Calculate metrics
        metrics = self._calculate_growth_metrics(content, growth_strategy)
        
        # Generate hashtags and remove duplicates
        hashtags = self._generate_growth_hashtags(theme, growth_strategy, language)
        unique_hashtags = list(dict.fromkeys(hashtags))  # Remove duplicates while preserving order

        return {
            "text": content,
            "hashtags": unique_hashtags,
            "theme": theme,
            "language": language,
            "growth_strategy": growth_strategy,
            "viral_elements_used": {
                "hook": viral_hook,
                "surprise_factor": surprise_factor
            },
            "predicted_metrics": metrics,
            "optimal_posting_time": self._get_optimal_posting_time(growth_strategy),
            "target_audience": self._identify_target_audience(growth_strategy),
            "engagement_tactics": strategy_config.get("tactics", [])
        }
    
    def _get_follower_acquisition_template(self, theme: ContentTheme, language: Language) -> str:
        """Templates optimized for follower growth"""
        templates = {
            Language.ENGLISH: {
                ContentTheme.DATA_MONDAY: "🚨 {viral_hook} 📊 SME Analytica's AI pricing helped restaurants boost margins by {percentage}% during peak hours. {social_proof} Ready to transform your business? {growth_trigger} {hashtags}",
                ContentTheme.TECH_THURSDAY: "⚡ {tech_innovation} MenuFlow seamlessly integrates with your existing POS system - no vendor switching required! {social_proof} {growth_trigger} {hashtags}",
                ContentTheme.CASE_WEDNESDAY: "🏆 CASE STUDY: {restaurant_name} was struggling with {business_challenge}. After implementing MenuFlow: ✅ {result_1} ✅ {result_2} ✅ {result_3} {social_proof} Want similar results? {growth_trigger} {hashtags}",
                ContentTheme.FACT_FRIDAY: "💡 FACT: {surprising_statistic} Most restaurant owners don't realize this opportunity exists. {social_proof} Don't get left behind! {growth_trigger} {hashtags}"
            },
            Language.SPANISH: {
                ContentTheme.DATA_MONDAY: "🚨 {viral_hook} 📊 Los precios dinámicos de SME Analytica ayudaron a restaurantes a aumentar márgenes {percentage}% en horas pico. {social_proof} ¿Listo para transformar tu negocio? {growth_trigger} {hashtags}"
            }
        }
        
        lang_templates = templates.get(language, templates[Language.ENGLISH])
        return lang_templates.get(theme, lang_templates[ContentTheme.DATA_MONDAY])
    
    def _get_engagement_boost_template(self, theme: ContentTheme, language: Language) -> str:
        """Templates optimized for engagement"""
        templates = {
            Language.ENGLISH: {
                ContentTheme.TALK_TUESDAY: "🤔 {question_starter} We've seen restaurants increase revenue by {percentage}% with simple analytics changes. What's YOUR biggest pricing challenge? Drop a comment below! 👇 {social_proof} {hashtags}",
                ContentTheme.DATA_MONDAY: "📊 MONDAY POLL: What matters most for your restaurant? A) Higher margins B) Faster service C) Better analytics D) All of the above Comment your choice + why! {social_proof} {hashtags}",
                ContentTheme.FACT_FRIDAY: "💡 Fun fact: {surprising_fact} What's the most surprising data insight you've discovered about your business? Share below! 👇 {hashtags}"
            }
        }
        
        lang_templates = templates.get(language, templates[Language.ENGLISH])
        return lang_templates.get(theme, lang_templates[ContentTheme.TALK_TUESDAY])
    
    def _get_viral_potential_template(self, theme: ContentTheme, language: Language) -> str:
        """Templates optimized for viral spread"""
        templates = {
            Language.ENGLISH: {
                ContentTheme.DATA_MONDAY: "🔥 VIRAL THREAD 1/5: The {amount} secret that transformed a struggling café into the neighborhood's busiest spot... MenuFlow's AI pricing identified their profit leak: {specific_insight}. Result? {transformation_result} 🧵👇",
                ContentTheme.TECH_THURSDAY: "⚡ BREAKING: Restaurant tech that actually WORKS. Unlike complex systems that need IT teams, MenuFlow plugs into your existing POS and starts optimizing immediately. {social_proof} Retweet if you're tired of complicated restaurant tech! {hashtags}",
                ContentTheme.CASE_WEDNESDAY: "🚨 This will shock you: {restaurant_name} thought they needed to RAISE prices to increase profit. MenuFlow's AI found they could make MORE money by lowering some prices and raising others. Result: {percentage}% revenue boost! {hashtags}"
            }
        }
        
        lang_templates = templates.get(language, templates[Language.ENGLISH])
        return lang_templates.get(theme, lang_templates[ContentTheme.DATA_MONDAY])
    
    def _get_conversion_focused_template(self, theme: ContentTheme, language: Language) -> str:
        """Templates optimized for conversions"""
        templates = {
            Language.ENGLISH: {
                ContentTheme.DATA_MONDAY: "📊 {proven_result} {social_proof} Ready to see what MenuFlow can do for YOUR restaurant? Book a free 15-minute demo: [link] {urgency_creator} {hashtags}",
                ContentTheme.TECH_THURSDAY: "⚡ See MenuFlow in action: {demo_description} Watch how it integrates with your POS system and starts optimizing prices in real-time. Free demo available: [link] {hashtags}",
                ContentTheme.CASE_WEDNESDAY: "🏆 Want results like {restaurant_name}? They saw {specific_results} in just {timeframe}. Your restaurant could be next. Schedule your free consultation: [link] {hashtags}"
            }
        }
        
        lang_templates = templates.get(language, templates[Language.ENGLISH])
        return lang_templates.get(theme, lang_templates[ContentTheme.DATA_MONDAY])
    
    def _generate_growth_variables(self, theme: ContentTheme, growth_strategy: GrowthStrategy, 
                                 language: Language) -> Dict[str, str]:
        """Generate variables optimized for growth strategies"""
        
        base_variables = {
            "insight": random.choice(self.content_variables["insights"]),
            "statistic": random.choice(self.content_variables["statistics"]),
            "data_tip": random.choice(self.content_variables["data_tips"]),
            "tech_feature": random.choice(self.content_variables["tech_features"]),
            "business_insight": random.choice(self.content_variables["business_insights"]),
            "call_to_action": random.choice(self.content_variables["call_to_actions"]),
            "target_audience": random.choice(self.content_variables["target_audiences"]),
            "benefit": random.choice(self.content_variables["benefits"])
        }
        
        # Add growth-specific variables
        growth_variables = {
            "viral_hook": random.choice(self.content_variables["viral_hooks"]),
            "growth_trigger": random.choice(self.content_variables["growth_triggers"]),
            "social_proof": random.choice(self.content_variables["social_proof"]),
            "urgency_creator": random.choice(self.content_variables["urgency_creators"]),
            "question_starter": random.choice(self.content_variables["question_starters"]),
            "percentage": random.choice(["10", "15", "20", "25"]),
            "amount": random.choice(["$50K", "$10K", "simple", "hidden"]),
            "tech_innovation": "Revolutionary restaurant AI that actually works!",
            "transformation_result": random.choice([
                "25% revenue increase in 8 weeks",
                "$3,000 extra monthly profit",
                "15% faster table turnover",
                "10% higher margins during peak hours"
            ]),
            "specific_insight": random.choice([
                "they were underpricing their popular lunch items",
                "peak hour demand was 3x higher than they realized",
                "weekend breakfast had 40% hidden profit potential",
                "their happy hour pricing was leaving money on the table"
            ]),
            "demo_description": "Live integration with your POS system in under 5 minutes",
            "proven_result": "MenuFlow users report average 10% margin increase in peak hours.",
            "specific_results": random.choice([
                "$4,200 additional monthly revenue",
                "18% improvement in table turnover",
                "12% increase in average check size",
                "25% boost in weekend profitability"
            ]),
            "timeframe": random.choice(["6 weeks", "2 months", "90 days", "3 months"]),
            "surprising_fact": random.choice([
                "87% of restaurants underutilize their POS data",
                "Dynamic pricing can increase revenue 15% without losing customers",
                "AI analytics help restaurants discover hidden profit opportunities"
            ]),
            "surprising_statistic": random.choice([
                "73% of restaurants are underpricing their most popular items",
                "Dynamic pricing can boost revenue 20% during peak hours",
                "Small restaurants leave $15,000+ on the table annually from poor pricing"
            ]),
            "restaurant_name": random.choice(["Café Luna", "Bistro Verde", "Restaurant Bella Vista", "Local Tapas Bar"]),
            "business_challenge": random.choice(["fluctuating demand", "pricing strategy optimization", "table turnover improvement"]),
            "result_1": "10% higher margins",
            "result_2": "15% faster turnover", 
            "result_3": "$2,800 monthly boost"
        }
        
        # Generate hashtags string (remove duplicates)
        hashtags = self._generate_growth_hashtags(theme, growth_strategy, language)
        unique_hashtags = list(dict.fromkeys(hashtags))  # Remove duplicates while preserving order
        growth_variables["hashtags"] = " ".join(unique_hashtags)
        
        # Merge base and growth variables
        return {**base_variables, **growth_variables}
    
    def _generate_growth_hashtags(self, theme: ContentTheme, growth_strategy: GrowthStrategy, 
                                language: Language) -> List[str]:
        """Generate hashtags optimized for growth strategies"""
        
        base_hashtags = ["#SMEAnalytica"]
        strategy_config = self.growth_strategies[growth_strategy]
        
        if growth_strategy == GrowthStrategy.FOLLOWER_ACQUISITION:
            trending_hashtags = strategy_config["optimal_hashtags"]
            selected = random.sample(trending_hashtags, 3)
        elif growth_strategy == GrowthStrategy.ENGAGEMENT_BOOST:
            engagement_hashtags = ["#RestaurantOwners", "#SmallBizTips", "#BusinessGrowth", "#AskTheExperts"]
            selected = random.sample(engagement_hashtags, 3)
        elif growth_strategy == GrowthStrategy.VIRAL_POTENTIAL:
            viral_hashtags = ["#ViralBusiness", "#GameChanger", "#RestaurantHacks", "#AIRevolution"]
            selected = random.sample(viral_hashtags, 3)
        else:  # CONVERSION_FOCUSED
            conversion_hashtags = ["#BookDemo", "#RestaurantTech", "#GetResults", "#MenuFlow"]
            selected = random.sample(conversion_hashtags, 3)
        
        return base_hashtags + selected
    
    def _calculate_growth_metrics(self, content: str, growth_strategy: GrowthStrategy) -> GrowthMetrics:
        """Calculate predicted growth metrics for content"""
        
        # Simplified scoring algorithm (in production, this would use ML)
        engagement_score = len(re.findall(r'[?!]', content)) * 2  # Questions and exclamations
        viral_score = len(re.findall(r'🔥|⚡|🚨|💡', content)) * 1.5  # Viral emojis
        conversion_score = len(re.findall(r'demo|book|free|results', content.lower())) * 2
        brand_score = 8 if "SME Analytica" in content or "MenuFlow" in content else 5
        
        return GrowthMetrics(
            engagement_rate=min(engagement_score + 5, 10),
            virality_score=min(viral_score + 6, 10),
            conversion_potential=min(conversion_score + 4, 10),
            brand_alignment=brand_score,
            growth_contribution=min((engagement_score + viral_score + conversion_score) / 3 + 5, 10)
        )
    
    def _get_optimal_posting_time(self, growth_strategy: GrowthStrategy) -> str:
        """Get optimal posting time for growth strategy"""
        strategy_config = self.growth_strategies[growth_strategy]
        
        if "optimal_timing" in strategy_config:
            return random.choice(strategy_config["optimal_timing"])
        
        return random.choice(self.optimal_posting_times["general_business"])
    
    def _identify_target_audience(self, growth_strategy: GrowthStrategy) -> str:
        """Identify target audience for growth strategy"""
        
        audiences = {
            GrowthStrategy.FOLLOWER_ACQUISITION: "restaurant_owners",
            GrowthStrategy.ENGAGEMENT_BOOST: "general_business",
            GrowthStrategy.VIRAL_POTENTIAL: "international",
            GrowthStrategy.CONVERSION_FOCUSED: "restaurant_owners"
        }
        
        return audiences.get(growth_strategy, "general_business")
    
    def generate_4_week_growth_calendar(self) -> Dict[str, Any]:
        """Generate comprehensive 4-week growth calendar"""
        
        calendar = {
            "overview": {
                "strategy": "SME Analytica 4-Week Growth Acceleration",
                "target_followers": {"week_1": 50, "week_2": 150, "week_3": 300, "week_4": 500},
                "content_frequency": 4,  # posts per day
                "engagement_target": 15,  # % engagement rate
                "conversion_goal": "40 demo requests in 4 weeks"
            },
            "weeks": {}
        }
        
        themes_cycle = [
            ContentTheme.DATA_MONDAY, ContentTheme.TALK_TUESDAY, ContentTheme.CASE_WEDNESDAY,
            ContentTheme.TECH_THURSDAY, ContentTheme.FACT_FRIDAY, ContentTheme.WEEKEND_INSIGHTS
        ]
        
        growth_strategies_cycle = [
            GrowthStrategy.FOLLOWER_ACQUISITION, GrowthStrategy.ENGAGEMENT_BOOST,
            GrowthStrategy.VIRAL_POTENTIAL, GrowthStrategy.CONVERSION_FOCUSED
        ]
        
        start_date = datetime.now()
        
        for week in range(1, 5):
            week_content = []
            
            for day in range(7):
                current_date = start_date + timedelta(days=(week-1)*7 + day)
                theme = themes_cycle[day % len(themes_cycle)]
                
                # 4 posts per day with different growth strategies
                for post_num in range(4):
                    growth_strategy = growth_strategies_cycle[post_num]
                    
                    content = self.generate_viral_optimized_content(
                        theme=theme,
                        growth_strategy=growth_strategy,
                        language=Language.ENGLISH if post_num < 3 else Language.SPANISH
                    )
                    
                    week_content.append({
                        "date": current_date.strftime("%Y-%m-%d"),
                        "day": current_date.strftime("%A"),
                        "post_number": post_num + 1,
                        "optimal_time": content["optimal_posting_time"],
                        "content": content,
                        "week_focus": f"Week {week} - {self._get_week_focus(week)}"
                    })
            
            calendar["weeks"][f"week_{week}"] = {
                "focus": self._get_week_focus(week),
                "target_followers": self.growth_strategies[GrowthStrategy.FOLLOWER_ACQUISITION][f"week_{week}_target"],
                "content": week_content,
                "key_metrics": self._get_week_metrics(week)
            }
        
        return calendar
    
    def _get_week_focus(self, week: int) -> str:
        """Get strategic focus for each week"""
        focuses = {
            1: "Foundation & Initial Reach",
            2: "Engagement & Community Building", 
            3: "Viral Content & Scale",
            4: "Conversion & Optimization"
        }
        return focuses.get(week, "Growth Acceleration")
    
    def _get_week_metrics(self, week: int) -> Dict[str, Any]:
        """Get target metrics for each week"""
        return {
            "follower_target": self.growth_strategies[GrowthStrategy.FOLLOWER_ACQUISITION][f"week_{week}_target"],
            "engagement_rate_target": f"{10 + week * 2}%",
            "demo_requests_target": week * 3,
            "viral_posts_target": week * 2,
            "community_engagements_target": week * 50
        }

# Test the content generator
if __name__ == "__main__":
    generator = GrowthOptimizedContentGenerator()
    
    # Test viral content generation
    content = generator.generate_viral_optimized_content(
        theme=ContentTheme.DATA_MONDAY,
        growth_strategy=GrowthStrategy.FOLLOWER_ACQUISITION,
        language=Language.ENGLISH
    )
    
    print("Generated Viral Content:")
    print(json.dumps(content, indent=2, default=str))
    
    # Test 4-week calendar generation
    calendar = generator.generate_4_week_growth_calendar()
    print("\n4-Week Growth Calendar Overview:")
    print(json.dumps(calendar["overview"], indent=2))