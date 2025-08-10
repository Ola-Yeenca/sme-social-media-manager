"""
Advanced Content Generation System for SME Analytica
A tech/data analytics company focused on restaurant & hospitality data insights
"""

import random
from datetime import datetime
from typing import Dict, List, Tuple

class ContentGenerator:
    """Generate diverse, engaging content for a data analytics company"""
    
    def __init__(self):
        self.used_templates = []  # Track recently used templates to avoid repetition
        self.max_history = 20  # Remember last 20 templates
        
    def get_content_strategy(self) -> Dict:
        """Get a diverse content strategy based on time and context"""
        
        # Content categories with weights
        categories = {
            'data_insights': 0.25,      # Data-driven insights and statistics
            'tech_updates': 0.15,        # Technology and AI updates
            'case_studies': 0.15,        # Success stories and case studies
            'tips_tricks': 0.15,         # Practical tips and tricks
            'industry_trends': 0.10,     # Industry trends and predictions
            'thought_leadership': 0.10,  # Controversial or thought-provoking
            'engagement_posts': 0.10     # Questions and polls
        }
        
        # Time-based content adjustments
        hour = datetime.now().hour
        if 8 <= hour < 10:  # Morning - motivational/tips
            categories['tips_tricks'] += 0.1
        elif 12 <= hour < 14:  # Lunch - light content
            categories['engagement_posts'] += 0.1
        elif 17 <= hour < 19:  # Evening - insights
            categories['data_insights'] += 0.1
            
        return categories
    
    def generate_prompts(self) -> List[str]:
        """Generate diverse, non-repetitive prompts"""
        
        # Data Insights Templates
        data_insights = [
            "Share a surprising data insight about {metric} in the restaurant industry that shows {trend}. Include specific percentages. Make it eye-opening.",
            "Create a data visualization description showing how {feature} impacts {outcome}. Use numbers and comparisons.",
            "Explain how our ML algorithms detected {pattern} that saved restaurants {amount}. Be specific with data.",
            "Share a counterintuitive finding from analyzing {number}K restaurant transactions about {topic}.",
            "Present a before/after comparison of a client's {metric} using our analytics platform.",
        ]
        
        # Tech Updates Templates
        tech_updates = [
            "Announce a new AI feature we're developing for {use_case}. Explain the tech stack briefly.",
            "Share how we're using {technology} to solve {problem} for restaurants. Be technical but accessible.",
            "Explain our latest algorithm update that improves {metric} by {percentage}. Include tech details.",
            "Discuss how we integrated with {system} to provide {benefit}. Technical but exciting.",
            "Share a behind-the-scenes look at our data pipeline processing {volume} daily transactions.",
        ]
        
        # Case Studies Templates
        case_studies = [
            "Tell a mini case study: '{Restaurant}' increased {metric} by {percentage} using our {feature}. Real results.",
            "Share how a client went from {problem} to {solution} in {timeframe} using our platform.",
            "Quick win story: Restaurant saved €{amount}/month by optimizing {area} with our analytics.",
            "Client spotlight: How {business_type} uses real-time data to {achievement}.",
            "Success metric: {number} restaurants now using our {feature} with average {result}.",
        ]
        
        # Tips & Tricks Templates
        tips_tricks = [
            "Pro tip for restaurant data analysis: {specific_technique}. Here's why it works...",
            "Hidden feature alert: Did you know you can {action} in our platform? Game-changer for {benefit}.",
            "Quick hack: Use {method} to instantly see {insight} in your restaurant data.",
            "Monday motivation: Set up {automation} to save {time} weekly on {task}.",
            "Data tip: Always compare {metric1} with {metric2} to spot {opportunity}.",
        ]
        
        # Industry Trends Templates
        industry_trends = [
            "🔮 2025 prediction: {trend} will reshape how restaurants {action}. Here's the data backing it.",
            "Industry shift: {percentage}% of restaurants now use {technology}. Are you ahead or behind?",
            "Breaking: New study shows {finding} about restaurant {topic}. What this means for you...",
            "Trend alert: {pattern} emerging in {region} restaurants. Data inside.",
            "Market analysis: Why {factor} is driving {change} in hospitality tech adoption.",
        ]
        
        # Thought Leadership Templates
        thought_leadership = [
            "Unpopular opinion: {controversial_take} about restaurant analytics. Here's the data...",
            "Hot take: {bold_statement} and I have the numbers to prove it.",
            "Let's talk about why {common_practice} is actually hurting restaurant profits.",
            "Controversial: {assumption} is wrong. Our data from {number} restaurants shows {reality}.",
            "Time to rethink {concept}. The data tells a different story...",
        ]
        
        # Engagement Posts Templates
        engagement_posts = [
            "Poll: What's your biggest data challenge? A) {option1} B) {option2} C) {option3}",
            "Quick question: How often do you check your {metric}? Reply below 👇",
            "Fill in the blank: The most underutilized restaurant data is ____",
            "True or False: {statement_about_data}? Drop your answer + reasoning below.",
            "What's one metric you wish you could track better? We're listening 👂",
        ]
        
        # Combine all templates
        all_templates = {
            'data_insights': data_insights,
            'tech_updates': tech_updates,
            'case_studies': case_studies,
            'tips_tricks': tips_tricks,
            'industry_trends': industry_trends,
            'thought_leadership': thought_leadership,
            'engagement_posts': engagement_posts
        }
        
        return all_templates
    
    def fill_template_variables(self, template: str) -> str:
        """Fill in template variables with relevant content"""
        
        variables = {
            # Metrics
            '{metric}': random.choice(['revenue per seat', 'table turnover rate', 'average order value', 
                                      'labor cost percentage', 'food cost ratio', 'customer lifetime value']),
            '{metric1}': 'weekday revenue',
            '{metric2}': 'weekend patterns',
            
            # Trends and patterns
            '{trend}': random.choice(['30% increase in off-peak profitability', '47% reduction in waste',
                                    '23% improvement in staff efficiency', '18% boost in repeat customers']),
            '{pattern}': random.choice(['seasonal pricing opportunities', 'hidden profit leaks',
                                       'optimal staffing patterns', 'menu performance gaps']),
            
            # Features and technology
            '{feature}': random.choice(['predictive analytics', 'dynamic pricing engine', 'real-time dashboards',
                                      'automated alerts', 'competitor tracking', 'demand forecasting']),
            '{technology}': random.choice(['GPT-4 integration', 'computer vision', 'predictive ML models',
                                         'real-time streaming', 'edge computing', 'blockchain verification']),
            '{system}': random.choice(['Square POS', 'Toast', 'Lightspeed', 'Clover', 'Shopify POS']),
            
            # Outcomes and benefits
            '{outcome}': random.choice(['profit margins', 'customer satisfaction', 'operational efficiency',
                                       'inventory turnover', 'staff productivity']),
            '{benefit}': random.choice(['real-time insights', 'automated pricing', 'predictive alerts',
                                      'seamless workflows', 'data-driven decisions']),
            '{achievement}': random.choice(['reduce waste by 40%', 'increase profits 23%', 
                                          'save 10 hours weekly', 'boost ratings 0.5 stars']),
            
            # Specific values
            '{amount}': random.choice(['€2,400', '€1,850', '€3,200', '€975', '€4,500']),
            '{number}': random.choice(['50', '127', '200+', '73', '95']),
            '{percentage}': random.choice(['34%', '28%', '45%', '19%', '52%', '67%']),
            '{volume}': random.choice(['1M+', '500K', '2.3M', '750K', '3M+']),
            '{time}': random.choice(['3 hours', '5 hours', '8 hours', '2 days']),
            '{timeframe}': random.choice(['3 weeks', '1 month', '45 days', '2 months']),
            
            # Business context
            '{Restaurant}': random.choice(['Bella Vista', 'The Corner Bistro', 'Sakura Sushi', 
                                         'El Mariachi', 'The Green Table']),
            '{business_type}': random.choice(['QSR chains', 'Fine dining', 'Fast casual', 
                                            'Food trucks', 'Hotel restaurants']),
            '{region}': random.choice(['Madrid', 'European', 'Spanish', 'Mediterranean', 'Iberian']),
            
            # Problems and solutions
            '{problem}': random.choice(['guessing prices', 'Excel chaos', 'no visibility', 
                                      'manual tracking', 'reactive decisions']),
            '{solution}': random.choice(['AI-powered insights', 'automated optimization', 
                                       'predictive analytics', 'real-time monitoring']),
            '{use_case}': random.choice(['predicting busy periods', 'optimizing staff schedules',
                                        'menu engineering', 'waste reduction', 'dynamic pricing']),
            
            # Specific techniques
            '{specific_technique}': random.choice([
                'segment lunch vs dinner metrics separately',
                'track item-level profit margins, not just revenue',
                'correlate weather data with sales patterns',
                'monitor competitor pricing weekly'
            ]),
            
            # Actions and methods
            '{action}': random.choice(['set up automated reports', 'configure price rules',
                                     'analyze customer segments', 'track competitor moves']),
            '{method}': random.choice(['cohort analysis', 'A/B testing', 'regression analysis',
                                      'clustering algorithms']),
            
            # Tasks and areas
            '{task}': random.choice(['inventory tracking', 'performance reports', 'price updates',
                                    'competitor analysis']),
            '{area}': random.choice(['menu pricing', 'labor scheduling', 'inventory management',
                                   'marketing spend']),
            '{topic}': random.choice(['customer behavior', 'pricing psychology', 'peak hours',
                                    'seasonal trends']),
            
            # Concepts and assumptions
            '{concept}': random.choice(['static pricing', 'gut-feel decisions', 'one-size-fits-all menus',
                                       'annual price reviews']),
            '{assumption}': random.choice(['"Lower prices mean more customers"', '"Busier is always better"',
                                         '"All revenue is good revenue"', '"Tech is too complex"']),
            '{common_practice}': random.choice(['copying competitor prices', 'never changing prices',
                                              'ignoring data', 'pricing by food cost alone']),
            
            # Controversial takes
            '{controversial_take}': random.choice([
                'Most restaurants are leaving 20% profit on the table',
                'Daily pricing changes should be normal',
                'Your POS data is your most valuable asset',
                '90% of menu items shouldn\'t exist'
            ]),
            '{bold_statement}': random.choice([
                'Static menus are dead',
                'Every restaurant needs a data scientist',
                'Gut feelings kill restaurants',
                'AI should set your prices'
            ]),
            
            # Engagement options
            '{option1}': 'Lack of time',
            '{option2}': 'Too much data',
            '{option3}': 'No clear insights',
            
            # Statements
            '{statement_about_data}': random.choice([
                'More data always means better decisions',
                'Real-time analytics are essential for restaurants',
                'Historical data predicts future perfectly'
            ]),
            
            # Factors and changes
            '{factor}': random.choice(['labor shortages', 'inflation', 'delivery apps', 
                                     'sustainability demands']),
            '{change}': random.choice(['consolidation', 'tech adoption', 'pricing strategies',
                                     'customer expectations']),
            
            # Automation
            '{automation}': random.choice(['daily reports', 'price alerts', 'inventory warnings',
                                         'performance summaries']),
            
            # Insights and opportunities  
            '{insight}': random.choice(['profit leaks', 'growth opportunities', 'efficiency gaps',
                                      'customer patterns']),
            '{opportunity}': random.choice(['upselling moments', 'pricing windows', 'cost savings',
                                          'revenue potential'])
        }
        
        # Replace all variables in template
        for var, value in variables.items():
            if var in template:
                template = template.replace(var, value)
                
        return template
    
    def select_template(self, templates: Dict[str, List[str]]) -> Tuple[str, str]:
        """Select a template ensuring variety"""
        
        strategy = self.get_content_strategy()
        
        # Weight-based selection of category
        categories = list(strategy.keys())
        weights = list(strategy.values())
        selected_category = random.choices(categories, weights=weights)[0]
        
        # Get templates for selected category
        category_templates = templates[selected_category]
        
        # Filter out recently used templates
        available = [t for t in category_templates if t not in self.used_templates[-10:]]
        if not available:
            available = category_templates
            
        selected_template = random.choice(available)
        
        # Track usage
        self.used_templates.append(selected_template)
        if len(self.used_templates) > self.max_history:
            self.used_templates.pop(0)
            
        return selected_category, selected_template
    
    def generate_content_prompt(self) -> Tuple[str, str]:
        """Generate a complete, varied content prompt"""
        
        templates = self.generate_prompts()
        category, template = self.select_template(templates)
        filled_template = self.fill_template_variables(template)
        
        # Add category-specific instructions
        instructions = {
            'data_insights': "Be specific with numbers. Sound analytical and authoritative.",
            'tech_updates': "Be excited about the technology. Balance technical and accessible.",
            'case_studies': "Make it feel real and achievable. Include specific results.",
            'tips_tricks': "Be helpful and actionable. Share insider knowledge.",
            'industry_trends': "Be forward-thinking. Back claims with data.",
            'thought_leadership': "Be bold but back it up. Challenge conventional thinking.",
            'engagement_posts': "Be conversational and inviting. Encourage responses."
        }
        
        # Add variety in hashtag strategies
        hashtag_strategies = [
            "Use 2-3 specific hashtags like #RestaurantAnalytics #DataDriven",
            "Mix general and niche hashtags: #Tech #RestaurantData",
            "Focus on trending tags: #AI #MachineLearning #Hospitality",
            "Use branded hashtag: #SMEAnalytica plus 1-2 relevant ones",
            "Question format, minimal hashtags at the end"
        ]
        
        # Build final prompt
        final_prompt = f"""
        Category: {category.replace('_', ' ').title()}
        
        Task: {filled_template}
        
        Style: {instructions.get(category, 'Be engaging and informative.')}
        Hashtag strategy: {random.choice(hashtag_strategies)}
        
        Requirements:
        - Under 280 characters total
        - Sound like a data-driven tech company, not a generic business account
        - Vary sentence structure and length
        - Sometimes use data viz emojis: 📊📈📉 or tech emojis: 🤖⚡💡
        - Occasionally include a call-to-action
        
        Write the tweet:
        """
        
        return category, final_prompt

# Integration function for backward compatibility
def get_dynamic_content_prompt() -> str:
    """Get a dynamic, non-repetitive content prompt"""
    generator = ContentGenerator()
    category, prompt = generator.generate_content_prompt()
    print(f"📝 Content category: {category}")
    return prompt