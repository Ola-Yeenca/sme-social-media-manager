"""
Content templates and generation logic for SME Analytica social media
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
import random
import re
from langdetect import detect
import sys
import os
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
                "🎯 Data-Driven Monday: {business_insight} With MenuFlow, restaurants see {specific_result}. {hashtags}"
            ],
            ContentTheme.TECH_THURSDAY: [
                "🚀 Tech Thursday: {tech_feature} SME Analytica's {solution} {integration_benefit}. {hashtags}",
                "⚡ Thursday Tech Tip: {technical_insight} Our platform {ease_of_use}. {hashtags}",
                "🔧 Technology Update: {innovation} Real-time analytics made simple for {target_market}. {hashtags}"
            ],
            ContentTheme.CASE_WEDNESDAY: [
                "📈 Case Study Wednesday: {business_name} {challenge_solved} using {sme_solution}. Result: {outcome}. {hashtags}",
                "🏆 Success Story: {client_example} {problem_statement} With SME Analytica, they achieved {specific_improvement}. {hashtags}",
                "💼 Real Results: {case_study_intro} {data_driven_solution} {measurable_outcome}. {hashtags}"
            ],
            ContentTheme.FACT_FRIDAY: [
                "💡 Fun Fact Friday: {interesting_statistic} {industry_context} {sme_analytica_connection}. {hashtags}",
                "🎲 Friday Fact: Did you know {surprising_data}? {business_relevance} {how_we_help}. {hashtags}",
                "📚 Fact Check Friday: {data_point} {industry_trend} {actionable_insight}. {hashtags}"
            ],
            ContentTheme.TALK_TUESDAY: [
                "🗣️ Talk Tuesday: {industry_question} What's your experience with {relevant_topic}? {hashtags}",
                "💬 Tuesday Discussion: {poll_question} Share your thoughts on {business_challenge}! {hashtags}",
                "🤔 Let's Talk: {conversation_starter} How do you handle {common_problem}? {hashtags}"
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
    """Main content generation engine"""
    
    def __init__(self):
        self.context = SMEAnalyticaContext()
        self.content_variables = self._initialize_content_variables()
    
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
