"""
Content templates and generation logic for SME Analytica social media
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
import random
import re
# Language detection with fallback
try:
    from langdetect import detect
except ImportError:
    def detect(text):
        """Simple language detection fallback"""
        spanish_keywords = ['restaurante', 'negocio', 'datos', 'análisis']
        text_lower = text.lower()
        if any(keyword in text_lower for keyword in spanish_keywords):
            return 'es'
        return 'en'  # Default to English
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config.settings import SMEAnalyticaContext, ContentTheme, Language

# Import viral optimization module
try:
    from src.content.viral_optimization import ViralOptimizationAgent, ViralContent, TrendingTopic
except ImportError:
    # Fallback if viral optimization not available
    ViralOptimizationAgent = None
    ViralContent = None
    TrendingTopic = None

class ContentCategory(str, Enum):
    EDUCATIONAL = "educational"
    PROMOTIONAL = "promotional" 
    INDUSTRY_NEWS = "industry_news"
    CASE_STUDY = "case_study"
    TIPS_AND_TRICKS = "tips_and_tricks"
    COMPANY_UPDATE = "company_update"
    ENGAGEMENT = "engagement"

class ContentTemplate:
    """Template for generating themed content"""
    
    def __init__(self, theme: ContentTheme, category: ContentCategory, language: Language):
        self.theme = theme
        self.category = category
        self.language = language
        self.templates = self._load_templates()
    
    def _load_templates(self) -> List[str]:
        """Load content templates based on theme and language"""
        
        if self.language == Language.SPANISH:
            return self._get_spanish_templates()
        elif self.language == Language.FRENCH:
            return self._get_french_templates()
        else:
            return self._get_english_templates()
    
    def _get_english_templates(self) -> List[str]:
        """English content templates"""
        
        templates = {
            ContentTheme.DATA_MONDAY: [
                "📊 Data Monday: {insight} At SME Analytica, we've seen {statistic}. {call_to_action} {hashtags}",
                "💡 Monday Insight: {data_tip} Our AI analytics help {target_audience} {benefit}. {hashtags}",
                "🎯 Data-Driven Monday: {business_insight} With MenuFlow, restaurants see {specific_result}. {hashtags}",
                "📈 Data Tip Monday: Did you know? {data_point} can {business_impact}. SME Analytica makes this simple for {target_audience}. {hashtags}",
                "🔍 Monday Analytics: {industry_insight} Our early tests show {proven_result}. {actionable_advice} {hashtags}",
                "💰 Revenue Monday: {pricing_insight} MenuFlow's AI-driven pricing helped restaurants boost margins ~10% during peak hours. {hashtags}"
            ],
            ContentTheme.TECH_THURSDAY: [
                "🚀 Tech Thursday: {tech_feature} SME Analytica's {solution} {integration_benefit}. {hashtags}",
                "⚡ Thursday Tech Tip: {technical_insight} Our platform {ease_of_use}. {hashtags}",
                "🔧 Technology Update: {innovation} Real-time analytics made simple for {target_market}. {hashtags}",
                "🛠️ Tech Thursday: {integration_feature} We integrate into your existing systems and turn your tools into super-tools. {hashtags}",
                "⚙️ Innovation Thursday: {ai_feature} No data science degree required - just actionable insights for your business. {hashtags}",
                "🔗 Integration Thursday: {seamless_integration} SME Analytica connects with your POS, booking, and accounting systems. {hashtags}"
            ],
            ContentTheme.CASE_WEDNESDAY: [
                "📈 Case Study Wednesday: {business_name} {challenge_solved} using {sme_solution}. Result: {outcome}. {hashtags}",
                "🏆 Success Story: {client_example} {problem_statement} With SME Analytica, they achieved {specific_improvement}. {hashtags}",
                "💼 Real Results: {case_study_intro} {data_driven_solution} {measurable_outcome}. {hashtags}",
                "🎯 Case Wednesday: Meet {restaurant_name}: {business_challenge} With MenuFlow's AI analytics: {transformation_result}. {hashtags}",
                "📊 Success Story: {small_business} struggled with {pricing_challenge}. MenuFlow's dynamic pricing delivered {margin_improvement}. {hashtags}",
                "🏪 Real Results Wednesday: {business_example} used SME Analytica to {business_improvement}. Outcome: {revenue_impact} in {timeframe}. {hashtags}"
            ],
            ContentTheme.FACT_FRIDAY: [
                "💡 Fun Fact Friday: {interesting_statistic} {industry_context} {sme_analytica_connection}. {hashtags}",
                "🎲 Friday Fact: Did you know {surprising_data}? {business_relevance} {how_we_help}. {hashtags}",
                "📚 Fact Check Friday: {data_point} {industry_trend} {actionable_insight}. {hashtags}",
                "🔢 Fact Friday: {restaurant_statistic} MenuFlow's AI pricing helps restaurants capture this opportunity automatically. {hashtags}",
                "📈 Data Friday: {business_insight} SME Analytica turns this challenge into competitive advantage for small businesses. {hashtags}",
                "💰 Friday Insight: {revenue_fact} Our dynamic pricing technology helps SMEs maximize these peak opportunities. {hashtags}"
            ],
            ContentTheme.TALK_TUESDAY: [
                "🗣️ Talk Tuesday: {industry_question} What's your experience with {relevant_topic}? {hashtags}",
                "💬 Tuesday Discussion: {poll_question} Share your thoughts on {business_challenge}! {hashtags}",
                "🤔 Let's Talk: {conversation_starter} How do you handle {common_problem}? {hashtags}",
                "🤝 Talk Tuesday: Restaurant owners - {restaurant_question} Share your pricing strategies! {hashtags}",
                "💭 Tuesday Chat: {sme_question} What's your biggest analytics challenge? Let's discuss solutions! {hashtags}",
                "🗨️ Community Tuesday: {business_discussion} How do you use data to make decisions? {hashtags}"
            ],
            ContentTheme.WEEKEND_INSIGHTS: [
                "🌟 Weekend Insight: {weekend_tip} Small changes, big impact with SME Analytica. {hashtags}",
                "☕ Saturday Thought: {business_wisdom} Data doesn't have to be complicated to be powerful. {hashtags}",
                "🎯 Sunday Strategy: {strategic_insight} Start your week with actionable analytics. {hashtags}",
                "🌅 Weekend Wisdom: {weekend_insight} SME Analytica makes enterprise-level analytics accessible to everyone. {hashtags}",
                "🍃 Relaxed Insight: {casual_tip} Sometimes the best business decisions come from simple data observations. {hashtags}"
            ]
        }
        
        return templates.get(self.theme, templates[ContentTheme.DATA_MONDAY])
    
    def _get_spanish_templates(self) -> List[str]:
        """Spanish content templates"""
        
        templates = {
            ContentTheme.DATA_MONDAY: [
                "📊 Lunes de Datos: {insight} En SME Analytica, hemos visto {statistic}. {call_to_action} {hashtags}",
                "💡 Insight del Lunes: {data_tip} Nuestros análisis IA ayudan {target_audience} {benefit}. {hashtags}",
                "🎯 Lunes Orientado a Datos: {business_insight} Con MenuFlow, restaurantes ven {specific_result}. {hashtags}"
            ],
            ContentTheme.TECH_THURSDAY: [
                "🚀 Jueves Tech: {tech_feature} {solution} de SME Analytica {integration_benefit}. {hashtags}",
                "⚡ Tip Tech del Jueves: {technical_insight} Nuestra plataforma {ease_of_use}. {hashtags}",
                "🔧 Actualización Tecnológica: {innovation} Análisis en tiempo real simplificado para {target_market}. {hashtags}"
            ],
            ContentTheme.FACT_FRIDAY: [
                "💡 Dato Curioso Viernes: {interesting_statistic} {industry_context} {sme_analytica_connection}. {hashtags}",
                "🎲 Dato del Viernes: ¿Sabías que {surprising_data}? {business_relevance} {how_we_help}. {hashtags}"
            ]
        }
        
        return templates.get(self.theme, templates[ContentTheme.DATA_MONDAY])
    
    def _get_french_templates(self) -> List[str]:
        """French content templates"""
        
        templates = {
            ContentTheme.DATA_MONDAY: [
                "📊 Lundi Data: {insight} Chez SME Analytica, nous avons vu {statistic}. {call_to_action} {hashtags}",
                "💡 Insight du Lundi: {data_tip} Nos analyses IA aident {target_audience} {benefit}. {hashtags}"
            ],
            ContentTheme.TECH_THURSDAY: [
                "🚀 Jeudi Tech: {tech_feature} {solution} de SME Analytica {integration_benefit}. {hashtags}",
                "⚡ Tip Tech du Jeudi: {technical_insight} Notre plateforme {ease_of_use}. {hashtags}"
            ]
        }
        
        return templates.get(self.theme, templates[ContentTheme.DATA_MONDAY])

class ContentGenerator:
    """Main content generation engine with viral optimization"""
    
    def __init__(self, twitter_manager=None):
        self.context = SMEAnalyticaContext()
        self.content_variables = self._initialize_content_variables()
        
        # Initialize viral optimization if available
        self.viral_agent = None
        if ViralOptimizationAgent and twitter_manager:
            try:
                self.viral_agent = ViralOptimizationAgent(twitter_manager)
            except Exception as e:
                print(f"Warning: Could not initialize viral optimization: {e}")
        
        # Viral enhancement flags
        self.use_viral_hooks = True
        self.monitor_trends = True
    
    def _initialize_content_variables(self) -> Dict[str, List[str]]:
        """Initialize content variables for template substitution"""
        
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
            ]
        }
    
    def generate_themed_content(self, theme: ContentTheme, language: Language = Language.ENGLISH, 
                              category: ContentCategory = ContentCategory.EDUCATIONAL) -> Dict[str, Any]:
        """Generate content for a specific theme"""
        
        template_gen = ContentTemplate(theme, category, language)
        templates = template_gen.templates
        
        if not templates:
            templates = ["SME Analytica: AI-driven analytics for small businesses. {hashtags}"]
        
        # Select random template
        template = random.choice(templates)
        
        # Generate content variables
        content_vars = self._generate_content_variables(theme, language)
        
        # Format template with variables
        try:
            formatted_content = template.format(**content_vars)
        except KeyError as e:
            # Fallback if template variable missing
            formatted_content = f"SME Analytica: {self._get_fallback_content(theme, language)}"
        
        # Generate hashtags
        hashtags = self._generate_hashtags(theme, language)
        
        return {
            "text": formatted_content,
            "hashtags": hashtags,
            "theme": theme,
            "language": language,
            "category": category,
            "variables_used": content_vars
        }
    
    def _generate_content_variables(self, theme: ContentTheme, language: Language) -> Dict[str, str]:
        """Generate variables for template substitution"""
        
        variables = {}
        
        # Core variables
        variables["insight"] = random.choice(self.content_variables["insights"])
        variables["statistic"] = random.choice(self.content_variables["statistics"])
        variables["data_tip"] = random.choice(self.content_variables["data_tips"])
        variables["tech_feature"] = random.choice(self.content_variables["tech_features"])
        variables["business_insight"] = random.choice(self.content_variables["business_insights"])
        variables["call_to_action"] = random.choice(self.content_variables["call_to_actions"])
        variables["target_audience"] = random.choice(self.content_variables["target_audiences"])
        variables["benefit"] = random.choice(self.content_variables["benefits"])
        
        # Add default variables for all themes
        variables["technical_insight"] = variables["insight"]
        variables["case_study_intro"] = "Small business success:"
        variables["data_driven_solution"] = "Using SME Analytica's analytics,"
        variables["measurable_outcome"] = "they increased revenue by 15%"
        variables["data_point"] = "Dynamic pricing technology"
        variables["industry_trend"] = "is becoming essential for competitive restaurants"
        variables["actionable_insight"] = "Start with peak hour optimization"
        
        # Theme-specific variables
        if theme == ContentTheme.DATA_MONDAY:
            variables["specific_result"] = "10% higher margins during peak hours"
            variables["solution"] = "MenuFlow"
            
        elif theme == ContentTheme.TECH_THURSDAY:
            variables["integration_benefit"] = "turns your existing tools into super-tools"
            variables["ease_of_use"] = "requires no technical expertise"
            variables["innovation"] = "AI-powered dynamic pricing"
            variables["target_market"] = "small and medium enterprises"
            
        elif theme == ContentTheme.CASE_WEDNESDAY:
            variables["business_name"] = "Local Café Luna"
            variables["challenge_solved"] = "increased table turnover by 15%"
            variables["sme_solution"] = "MenuFlow's AI analytics"
            variables["outcome"] = "25% revenue boost in 3 months"
            variables["client_example"] = "Restaurant Bella Vista"
            variables["problem_statement"] = "struggled with peak-hour pricing"
            variables["specific_improvement"] = "10% margin increase"
            variables["restaurant_name"] = random.choice(["Café Luna", "Bistro Verde", "Restaurant Bella Vista", "Local Tapas Bar"])
            variables["business_challenge"] = random.choice(["struggled with fluctuating demand", "needed better pricing strategy", "wanted to optimize table turnover"])
            variables["transformation_result"] = random.choice(["10% higher margins during peak hours", "15% faster table turns", "25% revenue boost in 3 months"])
            variables["small_business"] = random.choice(["Local restaurant owner Maria", "Café owner Carlos", "Small hotel manager Ana"])
            variables["pricing_challenge"] = random.choice(["peak-hour demand management", "competitive pricing strategy", "seasonal pricing optimization"])
            variables["margin_improvement"] = random.choice(["10% margin increase", "15% revenue boost", "20% efficiency improvement"])
            variables["business_example"] = random.choice(["Family restaurant Casa Blanca", "Boutique Hotel Vista", "Corner Café Express"])
            variables["business_improvement"] = random.choice(["optimize their pricing strategy", "increase table turnover", "boost peak-hour revenue"])
            variables["revenue_impact"] = random.choice(["25% revenue increase", "30% margin improvement", "20% efficiency boost"])
            variables["timeframe"] = random.choice(["3 months", "6 weeks", "2 months"])
            
        elif theme == ContentTheme.FACT_FRIDAY:
            variables["interesting_statistic"] = "87% of restaurants plan to invest in AI technology this year"
            variables["industry_context"] = "The hospitality sector is rapidly embracing digital transformation"
            variables["sme_analytica_connection"] = "SME Analytica is leading this revolution for small businesses"
            variables["surprising_data"] = "dynamic pricing can increase restaurant revenue by 15% during busy periods"
            variables["business_relevance"] = "This applies to any restaurant with varying demand"
            variables["how_we_help"] = "Our MenuFlow module automates this optimization"
            
        elif theme == ContentTheme.TALK_TUESDAY:
            variables["industry_question"] = "What's the biggest analytics challenge for your restaurant?"
            variables["relevant_topic"] = "data-driven pricing strategies"
            variables["poll_question"] = "Which metric matters most to your business?"
            variables["business_challenge"] = "peak-hour demand management"
            variables["conversation_starter"] = "Restaurant owners: what's your pricing strategy?"
            variables["common_problem"] = "fluctuating customer demand"
            variables["restaurant_question"] = random.choice([
                "How do you handle peak hour pricing?",
                "What's your biggest operational challenge?",
                "How do you track customer satisfaction?"
            ])
            variables["sme_question"] = random.choice([
                "What data do you wish you had access to?",
                "How do you make pricing decisions?",
                "What's your biggest business analytics pain point?"
            ])
            variables["business_discussion"] = random.choice([
                "Small business owners:",
                "Restaurant managers:",
                "Retail entrepreneurs:"
            ])

        elif theme == ContentTheme.WEEKEND_INSIGHTS:
            variables["weekend_tip"] = random.choice([
                "Track your weekend vs weekday performance patterns",
                "Use quiet moments to analyze your data trends",
                "Weekend planning starts with Monday's analytics"
            ])
            variables["business_wisdom"] = random.choice([
                "The best insights often come from simple observations",
                "Smart businesses use data, not just intuition",
                "Analytics should inform decisions, not complicate them"
            ])
            variables["strategic_insight"] = random.choice([
                "Plan your week with data-driven goals",
                "Review last week's performance to improve this week",
                "Set analytics-based targets for better results"
            ])
            variables["weekend_insight"] = random.choice([
                "Weekend downtime is perfect for reviewing your business data",
                "The most successful SMEs use analytics as their competitive edge",
                "Simple data insights can transform your business operations"
            ])
            variables["casual_tip"] = random.choice([
                "Your POS data tells a story - are you listening?",
                "Peak hours aren't just busy times, they're profit opportunities",
                "Customer patterns reveal hidden revenue potential"
            ])
        
        # Generate hashtags string
        hashtags = self._generate_hashtags(theme, language)
        variables["hashtags"] = " ".join(hashtags)
        
        return variables
    
    def _generate_hashtags(self, theme: ContentTheme, language: Language) -> List[str]:
        """Generate relevant hashtags for the content"""
        
        base_hashtags = ["#SMEAnalytica"]
        
        # Theme-specific hashtags
        theme_hashtags = {
            ContentTheme.DATA_MONDAY: ["#DataInsights", "#BusinessAnalytics", "#AIforSMEs"],
            ContentTheme.TECH_THURSDAY: ["#RestaurantTech", "#MenuFlow", "#HospitalityAI"],
            ContentTheme.CASE_WEDNESDAY: ["#SuccessStory", "#ROI", "#BusinessGrowth"],
            ContentTheme.FACT_FRIDAY: ["#DidYouKnow", "#IndustryInsights", "#SmallBusiness"],
            ContentTheme.TALK_TUESDAY: ["#Discussion", "#BusinessTips", "#Community"],
            ContentTheme.WEEKEND_INSIGHTS: ["#WeekendReads", "#BusinessIntelligence", "#Growth"]
        }
        
        # Industry hashtags
        industry_hashtags = ["#RestaurantAnalytics", "#RetailTech", "#HotelManagement", "#DynamicPricing"]
        
        # Combine hashtags
        selected_hashtags = base_hashtags + theme_hashtags.get(theme, [])
        selected_hashtags.append(random.choice(industry_hashtags))
        
        # Language-specific hashtags
        if language == Language.SPANISH:
            selected_hashtags.append("#TechEspañol")
        elif language == Language.FRENCH:
            selected_hashtags.append("#TechFrançais")
        
        return selected_hashtags[:4]  # Limit to 4 hashtags
    
    def _get_fallback_content(self, theme: ContentTheme, language: Language) -> str:
        """Generate fallback content if template fails"""
        
        fallbacks = {
            Language.ENGLISH: "AI-driven analytics that help small businesses grow. Real-time insights, dynamic pricing, seamless integration.",
            Language.SPANISH: "Análisis impulsados por IA que ayudan a las pequeñas empresas a crecer. Insights en tiempo real, precios dinámicos.",
            Language.FRENCH: "Analyses pilotées par IA qui aident les petites entreprises à croître. Insights en temps réel, prix dynamiques."
        }
        
        return fallbacks.get(language, fallbacks[Language.ENGLISH])
    
    def generate_engagement_content(self, topic: str, language: Language = Language.ENGLISH) -> Dict[str, Any]:
        """Generate content for engaging with specific topics"""
        
        engagement_templates = {
            "pricing": "Great point on pricing strategy! At SME Analytica, we've seen AI-driven dynamic pricing boost margins by ~10%. {hashtags}",
            "analytics": "Data analytics can be game-changing for SMEs! Our platform makes complex insights simple for business owners. {hashtags}",
            "restaurant_tech": "Restaurant technology is evolving fast! MenuFlow combines QR ordering with real-time analytics for complete optimization. {hashtags}",
            "small_business": "Small businesses deserve enterprise-level analytics! That's exactly what SME Analytica delivers - powerful insights, simple interface. {hashtags}"
        }
        
        template = engagement_templates.get(topic.lower(), 
            "Insightful perspective! SME Analytica helps businesses turn data into actionable growth strategies. {hashtags}")
        
        hashtags = self._generate_hashtags(ContentTheme.TALK_TUESDAY, language)
        content = template.format(hashtags=" ".join(hashtags))
        
        return {
            "text": content,
            "hashtags": hashtags,
            "topic": topic,
            "language": language,
            "type": "engagement"
        }
    
    def validate_content(self, content: str, max_length: int = 280) -> Dict[str, Any]:
        """Validate generated content"""
        
        validation = {
            "valid": True,
            "length": len(content),
            "max_length": max_length,
            "issues": []
        }
        
        # Check length
        if len(content) > max_length:
            validation["valid"] = False
            validation["issues"].append(f"Content too long: {len(content)} > {max_length}")
        
        # Check for essential elements
        if "SME Analytica" not in content and "#SMEAnalytica" not in content:
            validation["issues"].append("Missing brand mention")
        
        # Check hashtag count
        hashtag_count = len(re.findall(r'#\w+', content))
        if hashtag_count > 4:
            validation["issues"].append(f"Too many hashtags: {hashtag_count} > 4")
        
        # Detect language
        try:
            detected_lang = detect(content)
            validation["detected_language"] = detected_lang
        except:
            validation["detected_language"] = "unknown"
        
        return validation
    
    def get_content_calendar(self, days: int = 7) -> List[Dict[str, Any]]:
        """Generate a content calendar for the specified number of days"""
        
        calendar = []
        start_date = datetime.now()
        
        # Theme rotation by day of week
        theme_schedule = {
            0: ContentTheme.DATA_MONDAY,      # Monday
            1: ContentTheme.TALK_TUESDAY,     # Tuesday  
            2: ContentTheme.CASE_WEDNESDAY,   # Wednesday
            3: ContentTheme.TECH_THURSDAY,    # Thursday
            4: ContentTheme.FACT_FRIDAY,      # Friday
            5: ContentTheme.WEEKEND_INSIGHTS, # Saturday
            6: ContentTheme.WEEKEND_INSIGHTS  # Sunday
        }
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            day_of_week = current_date.weekday()
            
            theme = theme_schedule.get(day_of_week, ContentTheme.DATA_MONDAY)
            
            # Generate content for English and Spanish
            english_content = self.generate_themed_content(theme, Language.ENGLISH)
            spanish_content = self.generate_themed_content(theme, Language.SPANISH)
            
            calendar.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "day_of_week": current_date.strftime("%A"),
                "theme": theme,
                "english_content": english_content,
                "spanish_content": spanish_content,
                "posting_times": ["09:00", "13:00", "17:00"]  # Suggested posting times
            })
        
        return calendar
    
    async def generate_viral_optimized_content(self, theme: Optional[ContentTheme] = None, 
                                             language: Language = Language.ENGLISH,
                                             use_trending_topics: bool = True) -> Dict[str, Any]:
        """Generate content optimized for viral spread"""
        
        if not self.viral_agent:
            # Fallback to regular content generation
            return self.generate_themed_content(theme or ContentTheme.DATA_MONDAY, language)
        
        try:
            # Get trending topics if requested
            trending_topic = None
            if use_trending_topics and self.monitor_trends:
                trending_topics = await self.viral_agent.monitor_trending_topics()
                if trending_topics:
                    # Select best trending topic
                    # Calculate combined score for trending topic selection
                    def calculate_trend_score(t):
                        potential_scores = {"low": 1, "medium": 2, "high": 3, "viral": 4}
                        potential_score = potential_scores.get(str(t.viral_potential), 1)
                        return t.relevance_score * potential_score
                    
                    trending_topic = max(trending_topics, key=calculate_trend_score)
            
            # Generate viral content
            viral_content = await self.viral_agent.generate_viral_content(
                trend=trending_topic,
                content_type="general"
            )
            
            # Convert to standard format
            return {
                "text": viral_content.text,
                "hashtags": viral_content.hashtags,
                "theme": theme or ContentTheme.DATA_MONDAY,
                "language": language,
                "category": ContentCategory.EDUCATIONAL,
                "viral_optimized": True,
                "viral_score": viral_content.viral_score,
                "estimated_reach": viral_content.estimated_reach,
                "trending_topic": trending_topic.topic if trending_topic else None,
                "shareability_factors": viral_content.shareability_factors
            }
            
        except Exception as e:
            print(f"Error generating viral content, falling back to regular: {e}")
            return self.generate_themed_content(theme or ContentTheme.DATA_MONDAY, language)
    
    async def generate_viral_thread(self, topic: Optional[str] = None) -> Dict[str, Any]:
        """Generate a viral thread for maximum engagement"""
        
        if not self.viral_agent:
            return {"error": "Viral optimization not available"}
        
        try:
            # Get trending topic related to the requested topic
            trending_topic = None
            if topic and self.monitor_trends:
                trending_topics = await self.viral_agent.monitor_trending_topics()
                # Find best matching trend
                for trend in trending_topics:
                    if topic.lower() in trend.topic.lower() or trend.industry_connection == "direct":
                        trending_topic = trend
                        break
            
            # Generate viral thread
            viral_content = await self.viral_agent.generate_viral_content(
                trend=trending_topic,
                content_type="thread"
            )
            
            return {
                "thread_text": viral_content.text,
                "hashtags": viral_content.hashtags,
                "viral_score": viral_content.viral_score,
                "estimated_reach": viral_content.estimated_reach,
                "thread_potential": viral_content.thread_potential,
                "shareability_factors": viral_content.shareability_factors,
                "trending_topic": trending_topic.topic if trending_topic else None
            }
            
        except Exception as e:
            return {"error": f"Failed to generate viral thread: {e}"}
    
    def enhance_content_with_viral_hooks(self, content: str) -> str:
        """Enhance existing content with viral hooks"""
        
        if not self.viral_agent or not self.use_viral_hooks:
            return content
        
        try:
            # Select a viral hook that matches content theme
            relevant_hooks = [hook for hook in self.viral_agent.viral_hooks 
                            if hook.viral_score > 7.0]
            
            if relevant_hooks:
                # Use highest scoring hook
                best_hook = max(relevant_hooks, key=lambda h: h.viral_score)
                
                # Check if content already has a strong opening
                if not any(opener in content.lower() for opener in 
                          ["here's", "the secret", "why", "how", "what"]):
                    
                    # Prepend viral hook
                    enhanced_content = f"{best_hook.hook_text}\n\n{content}"
                    
                    # Ensure it fits Twitter limits
                    if len(enhanced_content) <= 280:
                        return enhanced_content
            
            return content
            
        except Exception as e:
            print(f"Error enhancing content with viral hooks: {e}")
            return content
    
    async def get_viral_opportunities_for_day(self, date: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Get viral content opportunities for a specific day"""
        
        if not self.viral_agent:
            return []
        
        try:
            opportunities = await self.viral_agent.get_daily_viral_opportunities(count=10)
            
            # Convert to standard format
            formatted_opportunities = []
            for opp in opportunities:
                formatted_opp = {
                    "type": opp["type"],
                    "priority": opp["priority"],
                    "posting_time": opp["optimal_posting_time"],
                    "content": {
                        "text": opp["content"].text,
                        "hashtags": opp["content"].hashtags,
                        "viral_score": opp["content"].viral_score,
                        "estimated_reach": opp["content"].estimated_reach
                    },
                    "expected_engagement": opp["expected_engagement"]
                }
                
                if opp["trend"]:
                    formatted_opp["trend"] = {
                        "topic": opp["trend"].topic,
                        "viral_potential": opp["trend"].viral_potential,
                        "relevance_score": opp["trend"].relevance_score
                    }
                
                formatted_opportunities.append(formatted_opp)
            
            return formatted_opportunities
            
        except Exception as e:
            print(f"Error getting viral opportunities: {e}")
            return []
    
    async def analyze_hashtag_performance(self, hashtags: List[str]) -> Dict[str, Any]:
        """Analyze hashtag viral potential"""
        
        if not self.viral_agent:
            return {"error": "Viral analysis not available"}
        
        try:
            analysis = await self.viral_agent.analyze_hashtag_viral_potential(hashtags)
            return {
                "analysis_timestamp": datetime.now(),
                "hashtag_analysis": analysis,
                "recommendations": self._generate_hashtag_recommendations(analysis)
            }
            
        except Exception as e:
            return {"error": f"Failed to analyze hashtags: {e}"}
    
    def _generate_hashtag_recommendations(self, analysis: Dict[str, Any]) -> List[str]:
        """Generate hashtag recommendations based on analysis"""
        
        recommendations = []
        
        for hashtag, data in analysis.items():
            if isinstance(data, dict) and "viral_potential" in data:
                if data["viral_potential"] == "viral":
                    recommendations.append(f"🔥 {hashtag}: High viral potential - use immediately!")
                elif data["viral_potential"] == "high":
                    recommendations.append(f"⚡ {hashtag}: Good potential - recommended for important posts")
                elif data["viral_potential"] == "low" and data.get("volume", 0) < 10:
                    recommendations.append(f"⚠️ {hashtag}: Low activity - consider alternatives")
        
        return recommendations
    
    def get_viral_analytics_summary(self) -> Dict[str, Any]:
        """Get summary of viral optimization performance"""
        
        if not self.viral_agent:
            return {"viral_optimization": "Not available"}
        
        try:
            return self.viral_agent.get_viral_analytics_dashboard()
        except Exception as e:
            return {"error": f"Failed to get viral analytics: {e}"}
    
    def toggle_viral_features(self, use_viral_hooks: Optional[bool] = None, monitor_trends: Optional[bool] = None):
        """Toggle viral optimization features"""
        
        if use_viral_hooks is not None:
            self.use_viral_hooks = use_viral_hooks
        
        if monitor_trends is not None:
            self.monitor_trends = monitor_trends
        
        print(f"Viral features updated: hooks={self.use_viral_hooks}, trends={self.monitor_trends}")
