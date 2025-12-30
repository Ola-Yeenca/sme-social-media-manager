"""
Advanced Content Generation System for SME Analytica
Strategy pattern for multi-product content generation:
- MenuFlow (restaurant)
- RealEstate (real_estate)
- Regula AI (compliance)
- Conversa (conversa)
- SME Analytica (general)
"""

import os
import random
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Tuple


class IndustryStrategy(ABC):
    """Abstract base class for industry-specific content strategies"""

    @abstractmethod
    def get_templates(self) -> Dict[str, List[str]]:
        """Return content templates for this industry"""
        pass

    @abstractmethod
    def get_variables(self) -> Dict[str, any]:
        """Return variable substitutions for this industry"""
        pass

    @abstractmethod
    def get_hashtag_strategies(self) -> List[str]:
        """Return hashtag strategies for this industry"""
        pass

    @abstractmethod
    def get_style_instructions(self) -> Dict[str, str]:
        """Return style instructions per content category"""
        pass


class RestaurantStrategy(IndustryStrategy):
    """Content strategy for MenuFlow - Restaurant analytics product"""

    def get_templates(self) -> Dict[str, List[str]]:
        return {
            'data_insights': [
                "Share a surprising data insight about {metric} in the restaurant industry that shows {trend}. Include specific percentages. Make it eye-opening.",
                "Create a data visualization description showing how {feature} impacts {outcome}. Use numbers and comparisons.",
                "Explain how our ML algorithms detected {pattern} that saved restaurants {amount}. Be specific with data.",
                "Share a counterintuitive finding from analyzing {number}K restaurant transactions about {topic}.",
                "Present a before/after comparison of a client's {metric} using our analytics platform.",
            ],
            'tech_updates': [
                "Announce a new AI feature we're developing for {use_case}. Explain the tech stack briefly.",
                "Share how we're using {technology} to solve {problem} for restaurants. Be technical but accessible.",
                "Explain our latest algorithm update that improves {metric} by {percentage}. Include tech details.",
                "Discuss how we integrated with {system} to provide {benefit}. Technical but exciting.",
                "Share a behind-the-scenes look at our data pipeline processing {volume} daily transactions.",
            ],
            'case_studies': [
                "Tell a mini case study: '{business_name}' increased {metric} by {percentage} using our {feature}. Real results.",
                "Share how a client went from {problem} to {solution} in {timeframe} using our platform.",
                "Quick win story: Restaurant saved {amount}/month by optimizing {area} with our analytics.",
                "Client spotlight: How {business_type} uses real-time data to {achievement}.",
                "Success metric: {number} restaurants now using our {feature} with average {result}.",
            ],
            'tips_tricks': [
                "Pro tip for restaurant data analysis: {specific_technique}. Here's why it works...",
                "Hidden feature alert: Did you know you can {action} in our platform? Game-changer for {benefit}.",
                "Quick hack: Use {method} to instantly see {insight} in your restaurant data.",
                "Monday motivation: Set up {automation} to save {time} weekly on {task}.",
                "Data tip: Always compare {metric1} with {metric2} to spot {opportunity}.",
            ],
            'industry_trends': [
                "2025 prediction: {industry_trend} will reshape how restaurants {action}. Here's the data backing it.",
                "Industry shift: {percentage}% of restaurants now use {technology}. Are you ahead or behind?",
                "Breaking: New study shows {finding} about restaurant {topic}. What this means for you...",
                "Trend alert: {pattern} emerging in {region} restaurants. Data inside.",
                "Market analysis: Why {factor} is driving {change} in hospitality tech adoption.",
            ],
            'thought_leadership': [
                "Unpopular opinion: {controversial_take} about restaurant analytics. Here's the data...",
                "Hot take: {bold_statement} and I have the numbers to prove it.",
                "Let's talk about why {common_practice} is actually hurting restaurant profits.",
                "Controversial: {assumption} is wrong. Our data from {number} restaurants shows {reality}.",
                "Time to rethink {concept}. The data tells a different story...",
            ],
            'engagement_posts': [
                "Poll: What's your biggest data challenge? A) {option1} B) {option2} C) {option3}",
                "Quick question: How often do you check your {metric}? Reply below",
                "Fill in the blank: The most underutilized restaurant data is ____",
                "True or False: {statement}? Drop your answer + reasoning below.",
                "What's one metric you wish you could track better? We're listening",
            ]
        }

    def get_variables(self) -> Dict[str, any]:
        return {
            '{metric}': ['revenue per seat', 'table turnover rate', 'average order value',
                        'labor cost percentage', 'food cost ratio', 'customer lifetime value'],
            '{metric1}': ['weekday revenue', 'lunch sales', 'delivery orders'],
            '{metric2}': ['weekend patterns', 'dinner performance', 'dine-in metrics'],
            '{trend}': ['30% increase in off-peak profitability', '47% reduction in waste',
                       '23% improvement in staff efficiency', '18% boost in repeat customers'],
            '{pattern}': ['seasonal pricing opportunities', 'hidden profit leaks',
                         'optimal staffing patterns', 'menu performance gaps'],
            '{feature}': ['predictive analytics', 'dynamic pricing engine', 'real-time dashboards',
                        'automated alerts', 'competitor tracking', 'demand forecasting'],
            '{technology}': ['GPT-4 integration', 'computer vision', 'predictive ML models',
                           'real-time streaming', 'edge computing'],
            '{system}': ['Square POS', 'Toast', 'Lightspeed', 'Clover', 'Shopify POS'],
            '{outcome}': ['profit margins', 'customer satisfaction', 'operational efficiency',
                         'inventory turnover', 'staff productivity'],
            '{benefit}': ['real-time insights', 'automated pricing', 'predictive alerts',
                        'seamless workflows', 'data-driven decisions'],
            '{achievement}': ['reduce waste by 40%', 'increase profits 23%',
                            'save 10 hours weekly', 'boost ratings 0.5 stars'],
            '{amount}': ['€2,400', '€1,850', '€3,200', '€975', '€4,500'],
            '{number}': ['50', '127', '200+', '73', '95'],
            '{percentage}': ['34%', '28%', '45%', '19%', '52%', '67%'],
            '{volume}': ['1M+', '500K', '2.3M', '750K', '3M+'],
            '{time}': ['3 hours', '5 hours', '8 hours', '2 days'],
            '{timeframe}': ['3 weeks', '1 month', '45 days', '2 months'],
            '{business_name}': ['Bella Vista', 'The Corner Bistro', 'Sakura Sushi',
                               'El Mariachi', 'The Green Table'],
            '{business_type}': ['QSR chains', 'Fine dining', 'Fast casual',
                               'Food trucks', 'Hotel restaurants'],
            '{region}': ['Madrid', 'European', 'Spanish', 'Mediterranean', 'Iberian'],
            '{problem}': ['guessing prices', 'Excel chaos', 'no visibility',
                        'manual tracking', 'reactive decisions'],
            '{solution}': ['AI-powered insights', 'automated optimization',
                         'predictive analytics', 'real-time monitoring'],
            '{use_case}': ['predicting busy periods', 'optimizing staff schedules',
                         'menu engineering', 'waste reduction', 'dynamic pricing'],
            '{specific_technique}': [
                'segment lunch vs dinner metrics separately',
                'track item-level profit margins, not just revenue',
                'correlate weather data with sales patterns',
                'monitor competitor pricing weekly'
            ],
            '{action}': ['set up automated reports', 'configure price rules',
                       'analyze customer segments', 'track competitor moves'],
            '{method}': ['cohort analysis', 'A/B testing', 'regression analysis',
                       'clustering algorithms'],
            '{task}': ['inventory tracking', 'performance reports', 'price updates',
                     'competitor analysis'],
            '{area}': ['menu pricing', 'labor scheduling', 'inventory management',
                     'marketing spend'],
            '{topic}': ['customer behavior', 'pricing psychology', 'peak hours',
                      'seasonal trends'],
            '{concept}': ['static pricing', 'gut-feel decisions', 'one-size-fits-all menus',
                        'annual price reviews'],
            '{assumption}': ['"Lower prices mean more customers"', '"Busier is always better"',
                           '"All revenue is good revenue"', '"Tech is too complex"'],
            '{common_practice}': ['copying competitor prices', 'never changing prices',
                                'ignoring data', 'pricing by food cost alone'],
            '{controversial_take}': [
                'Most restaurants are leaving 20% profit on the table',
                'Daily pricing changes should be normal',
                'Your POS data is your most valuable asset',
                '90% of menu items shouldn\'t exist'
            ],
            '{bold_statement}': [
                'Static menus are dead',
                'Every restaurant needs a data scientist',
                'Gut feelings kill restaurants',
                'AI should set your prices'
            ],
            '{option1}': ['Lack of time', 'Too many tools', 'No clear ROI'],
            '{option2}': ['Too much data', 'Staff resistance', 'Integration issues'],
            '{option3}': ['No clear insights', 'Cost concerns', 'Complexity'],
            '{statement}': [
                'More data always means better decisions',
                'Real-time analytics are essential for restaurants',
                'Historical data predicts future perfectly'
            ],
            '{industry_trend}': ['AI-powered pricing', 'predictive inventory', 'automated scheduling'],
            '{factor}': ['labor shortages', 'inflation', 'delivery apps', 'sustainability demands'],
            '{change}': ['consolidation', 'tech adoption', 'pricing strategies', 'customer expectations'],
            '{automation}': ['daily reports', 'price alerts', 'inventory warnings', 'performance summaries'],
            '{insight}': ['profit leaks', 'growth opportunities', 'efficiency gaps', 'customer patterns'],
            '{opportunity}': ['upselling moments', 'pricing windows', 'cost savings', 'revenue potential'],
            '{finding}': ['data-driven restaurants outperform by 23%', 'real-time analytics reduce waste 40%'],
            '{result}': ['15% margin improvement', '20% efficiency gain', '25% less waste'],
            '{reality}': ['the opposite is true', 'data shows different patterns', 'margins tell another story']
        }

    def get_hashtag_strategies(self) -> List[str]:
        return [
            "Use 2-3 specific hashtags like #RestaurantAnalytics #DataDriven #MenuFlow",
            "Mix general and niche hashtags: #Tech #RestaurantData #FoodTech",
            "Focus on trending tags: #AI #MachineLearning #Hospitality",
            "Use branded hashtag: #SMEAnalytica #MenuFlow plus 1-2 relevant ones",
            "Question format, minimal hashtags at the end"
        ]

    def get_style_instructions(self) -> Dict[str, str]:
        return {
            'data_insights': "Be specific with numbers. Sound analytical and authoritative.",
            'tech_updates': "Be excited about the technology. Balance technical and accessible.",
            'case_studies': "Make it feel real and achievable. Include specific results.",
            'tips_tricks': "Be helpful and actionable. Share insider knowledge.",
            'industry_trends': "Be forward-thinking. Back claims with data.",
            'thought_leadership': "Be bold but back it up. Challenge conventional thinking.",
            'engagement_posts': "Be conversational and inviting. Encourage responses."
        }


class RealEstateStrategy(IndustryStrategy):
    """Content strategy for Real Estate analytics product"""

    def get_templates(self) -> Dict[str, List[str]]:
        return {
            'data_insights': [
                "Market data alert: {metric} in {region} shows {trend}. Here's what smart agents are doing with this insight.",
                "Our AI analyzed {number}K property listings. {finding}. This changes everything for pricing strategy.",
                "Surprising stat: {metric} is {percentage} different from what most agents assume. The data doesn't lie.",
                "Before/after: Agent used our valuation algorithm and {achievement}. Data-driven pricing wins.",
                "Hidden pattern detected: {pattern} in {region} market. Early movers have {timeframe} advantage.",
            ],
            'tech_updates': [
                "New feature: {feature} now live for {use_case}. Early adopters seeing {percentage} improvement.",
                "Behind the scenes: Our {technology} processes {volume} property data points daily for accurate valuations.",
                "Just integrated with {system}. Now you can {benefit} seamlessly.",
                "Algorithm update: {metric} predictions now {percentage} more accurate. Tech details inside.",
                "We're using {technology} to solve {problem} in real estate. Here's how it works.",
            ],
            'case_studies': [
                "Case study: {business_name} closed {number} more deals using our {feature}. ROI in {timeframe}.",
                "Client win: Agent went from {problem} to {solution} in {timeframe}. Data made the difference.",
                "Success story: Brokerage reduced {metric} by {percentage} with predictive analytics.",
                "Real result: {business_type} using our platform achieved {achievement}.",
                "From struggling to thriving: How {business_name} used data to {achievement}.",
            ],
            'tips_tricks': [
                "Pro tip: {specific_technique}. Top agents already do this.",
                "Quick win: Use {method} to identify {insight} in your listings.",
                "Hidden feature: {action} in our platform gives you {benefit} instantly.",
                "Data hack: Compare {metric1} with {metric2} to spot {opportunity} before competitors.",
                "Time saver: Set up {automation} and save {time} weekly on {task}.",
            ],
            'industry_trends': [
                "2025 real estate prediction: {industry_trend} will separate winners from the rest.",
                "Market shift: {percentage}% of top agents now use {technology}. Where do you stand?",
                "Trend alert: {pattern} emerging in {region}. Smart money is paying attention.",
                "The data is clear: {factor} is driving {change} in property markets.",
                "Industry insight: {finding}. Time to adjust your strategy?",
            ],
            'thought_leadership': [
                "Hot take: {bold_statement}. Fight me in the comments.",
                "Unpopular opinion: {controversial_take}. Here's the market data.",
                "Why {common_practice} is costing agents deals. Data inside.",
                "Controversial: {assumption} is a myth. {number} transactions prove otherwise.",
                "Time to rethink {concept}. The market has changed.",
            ],
            'engagement_posts': [
                "Poll: Biggest challenge in today's market? A) {option1} B) {option2} C) {option3}",
                "Quick question: How do you price listings? Data or gut feeling?",
                "Fill in the blank: The most overlooked metric in real estate is ____",
                "Agents: What's one tech tool you can't live without? Drop it below",
                "True or False: {statement}? Let's debate.",
            ]
        }

    def get_variables(self) -> Dict[str, any]:
        return {
            '{metric}': ['days on market', 'price per sqft', 'list-to-sale ratio',
                        'buyer conversion rate', 'avg sale price', 'inventory levels',
                        'time to close', 'commission rates', 'lead response time'],
            '{metric1}': ['listing price', 'neighborhood comps', 'market velocity'],
            '{metric2}': ['final sale price', 'broader market trends', 'buyer demand'],
            '{trend}': ['15% faster closings', '23% better pricing accuracy',
                       '40% reduction in days on market', '30% more qualified leads'],
            '{pattern}': ['pricing sweet spots', 'buyer behavior shifts',
                         'seasonal demand curves', 'neighborhood value acceleration'],
            '{feature}': ['automated valuations (AVM)', 'predictive pricing', 'lead scoring',
                        'market analytics dashboard', 'comp analysis engine', 'buyer matching AI'],
            '{technology}': ['machine learning models', 'real-time market feeds', 'predictive AI',
                           'natural language processing', 'computer vision for property analysis'],
            '{system}': ['MLS systems', 'Zillow API', 'CRM platforms', 'DocuSign',
                        'showing management tools', 'transaction management'],
            '{outcome}': ['faster sales', 'higher sale prices', 'better lead conversion',
                         'reduced time on market', 'improved client satisfaction'],
            '{benefit}': ['instant valuations', 'market insights', 'automated follow-ups',
                        'competitive intelligence', 'data-driven pricing'],
            '{achievement}': ['close 30% more deals', 'reduce DOM by 40%',
                            'increase average sale price 8%', 'double lead conversion'],
            '{amount}': ['$15,000', '$8,500', '$25,000', '$12,000', '$50,000'],
            '{number}': ['50', '127', '300+', '85', '200'],
            '{percentage}': ['34%', '28%', '45%', '19%', '52%', '67%'],
            '{volume}': ['1M+', '500K', '2.5M', '750K', '5M+'],
            '{time}': ['5 hours', '10 hours', '2 days', '1 week'],
            '{timeframe}': ['30 days', '60 days', '90 days', 'one quarter'],
            '{business_name}': ['Prime Realty Group', 'Coastal Properties', 'Urban Edge Realty',
                               'Summit Real Estate', 'NextGen Properties'],
            '{business_type}': ['luxury agents', 'commercial brokers', 'residential teams',
                               'property investors', 'new construction specialists'],
            '{region}': ['urban markets', 'suburban areas', 'coastal regions',
                        'high-growth metros', 'emerging neighborhoods'],
            '{problem}': ['guessing prices', 'slow lead response', 'missed opportunities',
                        'manual CMA prep', 'reactive marketing'],
            '{solution}': ['AI-powered pricing', 'automated insights',
                         'predictive lead scoring', 'real-time market data'],
            '{use_case}': ['pricing new listings', 'identifying hot leads',
                         'predicting market shifts', 'optimizing showing schedules'],
            '{specific_technique}': [
                'analyze days-on-market patterns by price band',
                'track neighborhood velocity before pricing',
                'use predictive models for offer strategy',
                'monitor inventory levels weekly by zip code'
            ],
            '{action}': ['set up market alerts', 'configure lead scoring',
                       'build automated CMAs', 'track competitor listings'],
            '{method}': ['comparative market analysis', 'trend forecasting',
                       'buyer persona clustering', 'pricing optimization'],
            '{task}': ['CMA preparation', 'lead qualification', 'market research',
                     'listing updates'],
            '{area}': ['pricing strategy', 'lead nurturing', 'market positioning',
                     'listing optimization'],
            '{topic}': ['buyer behavior', 'market timing', 'price sensitivity',
                      'inventory trends'],
            '{concept}': ['static pricing', 'gut-feel valuations', 'one-price-fits-all',
                        'waiting for the market'],
            '{assumption}': ['"Price high, negotiate down"', '"Spring is the only time to sell"',
                           '"All leads are equal"', '"More listings = more success"'],
            '{common_practice}': ['overpricing to leave room', 'ignoring data signals',
                                'treating all buyers the same', 'manual everything'],
            '{controversial_take}': [
                'Most agents overprice by 5-10%',
                'Zillow estimates are more accurate than most CMAs',
                'The best time to list varies by neighborhood, not season',
                'AI will handle 50% of agent tasks by 2026'
            ],
            '{bold_statement}': [
                'Traditional CMAs are obsolete',
                'Data beats experience in pricing',
                'Gut feeling costs agents deals',
                'Every agent needs AI tools now'
            ],
            '{option1}': ['Finding leads', 'Market uncertainty', 'Tech overwhelm'],
            '{option2}': ['Pricing accuracy', 'Competition', 'Time management'],
            '{option3}': ['Client expectations', 'Inventory shortage', 'Conversion rates'],
            '{statement}': [
                'AI will replace agents within 10 years',
                'Data-driven pricing always wins',
                'Open houses are outdated'
            ],
            '{industry_trend}': ['AI-powered valuations', 'predictive market analytics',
                                'automated lead nurturing', 'virtual everything'],
            '{factor}': ['interest rates', 'inventory levels', 'remote work trends',
                        'investor activity'],
            '{change}': ['pricing strategies', 'buyer expectations', 'agent workflows',
                        'market timing'],
            '{automation}': ['lead alerts', 'market updates', 'price change notifications',
                           'showing feedback'],
            '{insight}': ['pricing opportunities', 'hot buyer leads', 'market timing signals',
                        'competitive gaps'],
            '{opportunity}': ['underpriced inventory', 'motivated sellers', 'buyer demand spikes',
                            'market inefficiencies'],
            '{finding}': ['data-driven agents close 30% more', 'AI pricing reduces DOM 40%',
                        'predictive lead scoring doubles conversion'],
            '{result}': ['faster closings', 'higher sale prices', 'more referrals'],
            '{reality}': ['the data shows otherwise', 'top performers do the opposite',
                        'market trends disagree']
        }

    def get_hashtag_strategies(self) -> List[str]:
        return [
            "Use 2-3 specific hashtags like #RealEstateData #PropTech #SMEAnalytica",
            "Mix general and niche hashtags: #RealEstate #AIinRealEstate #MarketData",
            "Focus on trending tags: #AI #MachineLearning #PropertyMarket",
            "Use branded hashtag: #SMEAnalytica plus #RealEstateAgent #PropTech",
            "Engagement style with minimal hashtags"
        ]

    def get_style_instructions(self) -> Dict[str, str]:
        return {
            'data_insights': "Lead with surprising market data. Be authoritative but accessible.",
            'tech_updates': "Show how tech solves real agent problems. Avoid jargon.",
            'case_studies': "Focus on ROI and tangible results. Make it relatable.",
            'tips_tricks': "Actionable advice agents can use today. Be practical.",
            'industry_trends': "Forward-thinking with data backing. Be bold.",
            'thought_leadership': "Challenge industry norms. Back it with evidence.",
            'engagement_posts': "Spark debate. Ask questions agents care about."
        }


class GeneralSMEStrategy(IndustryStrategy):
    """Content strategy for SME Analytica - General SME and tech focus"""

    def get_templates(self) -> Dict[str, List[str]]:
        return {
            'data_insights': [
                "SME insight: {metric} improved by {percentage} when businesses adopted {feature}. Data from {number} companies.",
                "Surprising finding: {finding}. Most SMEs don't realize this.",
                "New data shows {trend}. Are you leveraging this for your business?",
                "We analyzed {number}K SME transactions. Pattern detected: {pattern}.",
                "Before/after: SME used data analytics and {achievement}. Results speak.",
            ],
            'tech_updates': [
                "Tech that matters for SMEs: {feature} now helps with {use_case}.",
                "We're building {technology} specifically for small businesses. Here's why it matters.",
                "New integration: Connect {system} with our platform for {benefit}.",
                "Behind the scenes: How we use {technology} to help SMEs compete with enterprises.",
                "Feature drop: {feature} is live. Early adopters seeing {percentage} gains.",
            ],
            'case_studies': [
                "SME success: {business_type} went from {problem} to {solution} in {timeframe}.",
                "Client spotlight: How a {business_type} used data to {achievement}.",
                "Real result: Small business saved {amount}/month with analytics.",
                "Case study: {number} SMEs using our {feature}. Average result: {result}.",
                "From chaos to clarity: {business_type}'s data transformation story.",
            ],
            'tips_tricks': [
                "SME tip: {specific_technique}. Takes 10 minutes, saves hours.",
                "Quick win for small businesses: {action} to see {insight} instantly.",
                "Productivity hack: Set up {automation} and reclaim {time} weekly.",
                "Data tip: Track {metric1} against {metric2} to find {opportunity}.",
                "Free advice: {specific_technique}. Most businesses overlook this.",
            ],
            'industry_trends': [
                "2025 SME trend: {industry_trend} is becoming essential, not optional.",
                "{percentage}% of successful SMEs now use {technology}. The gap is widening.",
                "Market signal: {factor} is driving {change} for small businesses.",
                "Trend watch: {pattern} emerging. Smart SMEs are preparing now.",
                "Industry shift: {finding}. Time to adapt?",
            ],
            'thought_leadership': [
                "Unpopular SME opinion: {controversial_take}",
                "Hot take: {bold_statement}. Small businesses, listen up.",
                "Why {common_practice} is holding your business back.",
                "Myth busted: {assumption} - data says otherwise.",
                "Controversial: {concept} is outdated. Here's what works now.",
            ],
            'engagement_posts': [
                "SME owners: What's your biggest operational challenge? A) {option1} B) {option2} C) {option3}",
                "Quick poll: Do you use data for decisions? Always / Sometimes / Rarely",
                "Fill in the blank: The tool that changed my business is ____",
                "Business owners: What's one metric you wish you understood better?",
                "Debate time: {statement} - Agree or disagree?",
            ]
        }

    def get_variables(self) -> Dict[str, any]:
        return {
            '{metric}': ['operational efficiency', 'customer acquisition cost', 'revenue per employee',
                        'profit margins', 'customer retention', 'conversion rates',
                        'time to decision', 'process cycle time', 'cash flow'],
            '{metric1}': ['customer acquisition cost', 'revenue', 'operational costs'],
            '{metric2}': ['lifetime value', 'profit margins', 'efficiency gains'],
            '{trend}': ['25% efficiency gains with AI', '40% reduction in manual tasks',
                       '30% faster decision making', '35% cost savings with automation'],
            '{pattern}': ['automation adoption surge', 'data-first decision making',
                         'AI tool integration', 'process optimization opportunities'],
            '{feature}': ['predictive analytics', 'automated workflows', 'real-time dashboards',
                        'AI assistants', 'process automation', 'data integration'],
            '{technology}': ['machine learning', 'AI automation', 'cloud analytics',
                           'predictive modeling', 'natural language AI'],
            '{system}': ['accounting software', 'CRM platforms', 'ERP systems',
                        'project management tools', 'communication platforms'],
            '{outcome}': ['better decisions', 'faster growth', 'reduced costs',
                         'improved efficiency', 'competitive advantage'],
            '{benefit}': ['automated insights', 'real-time visibility', 'predictive alerts',
                        'data-driven decisions', 'process optimization'],
            '{achievement}': ['cut costs 30%', 'grow revenue 25%', 'save 15 hours weekly',
                            'double efficiency', 'scale without hiring'],
            '{amount}': ['$2,000', '$5,000', '$3,500', '$1,500', '$8,000'],
            '{number}': ['50', '100+', '250', '75', '150'],
            '{percentage}': ['34%', '28%', '45%', '22%', '50%', '67%'],
            '{volume}': ['100K+', '500K', '1M', '250K', '2M+'],
            '{time}': ['5 hours', '10 hours', '3 days', '1 week'],
            '{timeframe}': ['30 days', '60 days', '90 days', 'one quarter'],
            '{business_type}': ['e-commerce stores', 'service businesses', 'B2B companies',
                               'local businesses', 'tech startups', 'professional services'],
            '{region}': ['growing markets', 'competitive industries', 'traditional sectors'],
            '{problem}': ['spreadsheet chaos', 'no visibility', 'slow decisions',
                        'manual processes', 'data silos'],
            '{solution}': ['automated analytics', 'real-time insights',
                         'AI-powered decisions', 'integrated data'],
            '{use_case}': ['forecasting demand', 'optimizing operations',
                         'reducing costs', 'accelerating growth'],
            '{specific_technique}': [
                'automate your weekly reporting',
                'set up alerts for key metrics',
                'integrate your data sources',
                'use AI for routine decisions'
            ],
            '{action}': ['connect your tools', 'set up dashboards',
                       'automate workflows', 'enable AI features'],
            '{method}': ['data integration', 'process automation',
                       'predictive analysis', 'performance tracking'],
            '{task}': ['reporting', 'data entry', 'analysis', 'forecasting'],
            '{area}': ['operations', 'sales', 'marketing', 'finance'],
            '{topic}': ['business growth', 'efficiency', 'scaling', 'automation'],
            '{concept}': ['manual processes', 'spreadsheet management',
                        'gut-feel decisions', 'delayed reporting'],
            '{assumption}': ['"Data is only for big companies"', '"AI is too expensive"',
                           '"We\'re too small for analytics"', '"Tech slows us down"'],
            '{common_practice}': ['avoiding technology', 'manual data entry',
                                'delayed decision making', 'ignoring metrics'],
            '{controversial_take}': [
                'Most SMEs are drowning in data they don\'t use',
                'Spreadsheets are killing small businesses',
                'AI is now affordable for every SME',
                'Data-driven SMEs will dominate their markets'
            ],
            '{bold_statement}': [
                'Every SME needs AI tools now',
                'Manual processes are a competitive disadvantage',
                'Data literacy is the new business requirement',
                'Automation is survival, not luxury'
            ],
            '{option1}': ['Time constraints', 'Tech complexity', 'Budget limits'],
            '{option2}': ['Finding talent', 'Data chaos', 'Process inefficiency'],
            '{option3}': ['Competition', 'Scaling challenges', 'Decision delays'],
            '{statement}': [
                'AI will level the playing field for SMEs',
                'Data-driven beats experience-driven',
                'Automation is essential for growth'
            ],
            '{industry_trend}': ['AI adoption', 'process automation', 'data integration',
                                'predictive analytics'],
            '{factor}': ['technology access', 'competitive pressure', 'talent costs',
                        'market speed'],
            '{change}': ['operational models', 'growth strategies', 'hiring practices',
                        'decision making'],
            '{automation}': ['weekly reports', 'data syncs', 'alert systems',
                           'routine tasks'],
            '{insight}': ['efficiency gaps', 'growth opportunities', 'cost leaks',
                        'optimization potential'],
            '{opportunity}': ['process improvements', 'cost reductions', 'growth levers',
                            'competitive advantages'],
            '{finding}': ['data-driven SMEs grow 2x faster', 'automation saves 15+ hours weekly',
                        'AI adoption correlates with profitability'],
            '{result}': ['faster growth', 'better margins', 'reduced costs'],
            '{reality}': ['data proves otherwise', 'successful SMEs do the opposite',
                        'the numbers disagree']
        }

    def get_hashtag_strategies(self) -> List[str]:
        return [
            "Use 2-3 specific hashtags like #SMEAnalytics #DataDriven #SMEgrowth",
            "Mix general and niche hashtags: #SmallBusiness #AI #Automation",
            "Focus on trending tags: #AI #MachineLearning #BusinessGrowth",
            "Use branded hashtag: #SMEAnalytica plus #Entrepreneurship #TechForSMEs",
            "Engagement style with minimal hashtags"
        ]

    def get_style_instructions(self) -> Dict[str, str]:
        return {
            'data_insights': "Make data accessible and actionable for non-technical owners.",
            'tech_updates': "Show practical value. Avoid intimidating jargon.",
            'case_studies': "Relatable SME stories. Focus on realistic results.",
            'tips_tricks': "Immediately actionable. Low barrier to implement.",
            'industry_trends': "Forward-looking but practical. Relevant to small business.",
            'thought_leadership': "Challenge outdated SME practices. Be provocative.",
            'engagement_posts': "Connect with SME pain points. Build community."
        }


class ContentGenerator:
    """Generate diverse, engaging content using industry-specific strategies"""

    def __init__(self, industry: str = None):
        self.used_templates = []
        self.max_history = 20

        # Get industry from parameter or environment
        if industry is None:
            industry = os.getenv('SME_INDUSTRY', 'general').lower()

        # Select strategy based on industry
        self.industry = industry
        self.strategy = self._get_strategy(industry)
        print(f"📊 Content strategy: {industry.replace('_', ' ').title()}")

    def _get_strategy(self, industry: str) -> IndustryStrategy:
        """Get the appropriate strategy for the industry"""
        strategies = {
            'restaurant': RestaurantStrategy(),
            'real_estate': RealEstateStrategy(),
            # Future strategies can be added here:
            # 'compliance': ComplianceStrategy(),
            # 'conversa': ConversaStrategy(),
        }
        return strategies.get(industry, GeneralSMEStrategy())

    def get_content_strategy(self) -> Dict:
        """Get a diverse content strategy based on time and context"""
        categories = {
            'data_insights': 0.25,
            'tech_updates': 0.15,
            'case_studies': 0.15,
            'tips_tricks': 0.15,
            'industry_trends': 0.10,
            'thought_leadership': 0.10,
            'engagement_posts': 0.10
        }

        hour = datetime.now().hour
        if 8 <= hour < 10:
            categories['tips_tricks'] += 0.1
        elif 12 <= hour < 14:
            categories['engagement_posts'] += 0.1
        elif 17 <= hour < 19:
            categories['data_insights'] += 0.1

        return categories

    def fill_template_variables(self, template: str) -> str:
        """Fill in template variables with industry-specific content"""
        variables = self.strategy.get_variables()

        for var, values in variables.items():
            if var in template:
                value = random.choice(values) if isinstance(values, list) else values
                template = template.replace(var, str(value))

        return template

    def select_template(self, templates: Dict[str, List[str]]) -> Tuple[str, str]:
        """Select a template ensuring variety"""
        strategy = self.get_content_strategy()

        categories = list(strategy.keys())
        weights = list(strategy.values())
        selected_category = random.choices(categories, weights=weights)[0]

        category_templates = templates.get(selected_category, templates['data_insights'])

        available = [t for t in category_templates if t not in self.used_templates[-10:]]
        if not available:
            available = category_templates

        selected_template = random.choice(available)

        self.used_templates.append(selected_template)
        if len(self.used_templates) > self.max_history:
            self.used_templates.pop(0)

        return selected_category, selected_template

    def generate_content_prompt(self) -> Tuple[str, str]:
        """Generate a complete, varied content prompt"""
        templates = self.strategy.get_templates()
        category, template = self.select_template(templates)
        filled_template = self.fill_template_variables(template)

        instructions = self.strategy.get_style_instructions()
        hashtag_strategies = self.strategy.get_hashtag_strategies()

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


def get_dynamic_content_prompt(industry: str = None) -> str:
    """Get a dynamic, non-repetitive content prompt"""
    generator = ContentGenerator(industry)
    category, prompt = generator.generate_content_prompt()
    print(f"📝 Content category: {category}")
    return prompt
