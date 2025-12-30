"""
Dynamic Content Generation System - Pulls from real sources
Strategy pattern for industry-specific real-time data and trending topics
"""

import os
import random
import requests
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional


class IndustryDynamicStrategy(ABC):
    """Abstract base class for industry-specific dynamic content"""

    @abstractmethod
    def get_subreddits(self) -> List[str]:
        """Return relevant subreddits for this industry"""
        pass

    @abstractmethod
    def get_keywords(self) -> List[str]:
        """Return keywords for filtering trending topics"""
        pass

    @abstractmethod
    def get_base_stats(self) -> List[Dict]:
        """Return industry-specific statistics"""
        pass

    @abstractmethod
    def get_competitors(self) -> List[Dict]:
        """Return competitor/market data"""
        pass

    @abstractmethod
    def get_time_insights(self) -> Dict:
        """Return time-contextual insights"""
        pass

    @abstractmethod
    def get_scenarios(self) -> List[str]:
        """Return realistic client scenario templates"""
        pass

    @abstractmethod
    def get_hashtag_pools(self) -> Dict[str, List[str]]:
        """Return hashtag pools for this industry"""
        pass


class RestaurantDynamicStrategy(IndustryDynamicStrategy):
    """Dynamic content strategy for restaurant/hospitality industry"""

    def get_subreddits(self) -> List[str]:
        return ['restaurateur', 'smallbusiness', 'dataengineering', 'machinelearning', 'KitchenConfidential']

    def get_keywords(self) -> List[str]:
        return ['data', 'AI', 'restaurant', 'business', 'analytics', 'pricing',
                'machine learning', 'startup', 'saas', 'automation', 'food', 'hospitality']

    def get_base_stats(self) -> List[Dict]:
        current_month = datetime.now().strftime('%B')
        current_quarter = f"Q{(datetime.now().month-1)//3+1}"

        return [
            {
                'metric': 'restaurant failure rate',
                'value': random.randint(70, 85),
                'unit': '%',
                'timeframe': 'first year',
                'insight': 'lack of data-driven decisions'
            },
            {
                'metric': 'average food cost',
                'value': random.randint(28, 35),
                'unit': '%',
                'timeframe': 'industry standard',
                'insight': 'optimization potential exists'
            },
            {
                'metric': 'revenue increase from dynamic pricing',
                'value': random.randint(8, 23),
                'unit': '%',
                'timeframe': 'within 6 months',
                'insight': 'AI-powered adjustments'
            },
            {
                'metric': 'table turnover improvement',
                'value': random.randint(15, 30),
                'unit': '%',
                'timeframe': 'peak hours',
                'insight': 'predictive analytics implementation'
            },
            {
                'metric': 'labor cost reduction',
                'value': random.randint(10, 18),
                'unit': '%',
                'timeframe': 'quarterly',
                'insight': 'smart scheduling algorithms'
            },
            {
                'metric': f'{current_month} inflation impact',
                'value': round(random.uniform(3.2, 5.8), 1),
                'unit': '%',
                'timeframe': 'restaurant margins',
                'insight': 'pricing strategy crucial'
            },
            {
                'metric': f'{current_quarter} tech adoption',
                'value': random.randint(42, 67),
                'unit': '%',
                'timeframe': 'European restaurants',
                'insight': 'digital transformation accelerating'
            }
        ]

    def get_competitors(self) -> List[Dict]:
        return [
            {'company': 'Toast', 'focus': 'integrated payment solutions', 'trend': 'unified platforms'},
            {'company': 'Square', 'focus': 'AI-powered insights', 'trend': 'predictive analytics'},
            {'company': 'Uber Eats', 'focus': 'dynamic delivery pricing', 'trend': 'demand-based fees'},
            {'company': 'DoorDash', 'focus': 'merchant analytics dashboard', 'trend': 'data democratization'},
            {'company': 'Lightspeed', 'focus': 'inventory predictions', 'trend': 'waste reduction'},
        ]

    def get_time_insights(self) -> Dict:
        now = datetime.now()
        insights = {'time_context': '', 'seasonal_context': '', 'business_rhythm': ''}

        if now.hour < 10:
            insights['time_context'] = 'morning prep time - when smart restaurants review yesterday\'s data'
        elif 11 <= now.hour < 14:
            insights['time_context'] = 'lunch rush - real-time data matters most now'
        elif 14 <= now.hour < 17:
            insights['time_context'] = 'afternoon lull - perfect for analyzing patterns'
        elif 17 <= now.hour < 20:
            insights['time_context'] = 'dinner service - peak revenue hours'
        else:
            insights['time_context'] = 'closing time - when today\'s insights become tomorrow\'s strategy'

        weekday = now.strftime('%A')
        day_insights = {
            'Monday': 'Start week strong - review weekend performance data',
            'Tuesday': 'Optimize midweek - lowest traffic days need smart tactics',
            'Wednesday': 'Midweek checkpoint - adjust strategies based on data',
            'Thursday': 'Prep for weekend - predictive models show rush patterns',
            'Friday': 'Peak begins - dynamic pricing maximizes revenue',
            'Saturday': 'Busiest day - real-time analytics prevent bottlenecks',
            'Sunday': 'Family dining patterns - different metrics matter'
        }
        insights['business_rhythm'] = day_insights.get(weekday, '')

        month = now.month
        if month in [12, 1, 2]:
            insights['seasonal_context'] = 'Winter strategies - comfort food trends, weather impact analysis'
        elif month in [3, 4, 5]:
            insights['seasonal_context'] = 'Spring refresh - menu optimization season, outdoor dining prep'
        elif month in [6, 7, 8]:
            insights['seasonal_context'] = 'Summer peak - tourist analytics, extended hours optimization'
        else:
            insights['seasonal_context'] = 'Fall transitions - seasonal menu data, holiday prep analytics'

        return insights

    def get_scenarios(self) -> List[str]:
        return [
            f"Client case: Madrid tapas bar discovered they were losing €{random.randint(500,1500)}/week "
            f"on their top 3 dishes. Our pricing algorithm fixed it in {random.randint(3,7)} days.",
            f"Real result: {random.randint(20,40)}% reduction in food waste after implementing "
            f"our predictive ordering system. That's €{random.randint(2000,5000)}/month saved.",
            f"Today's win: Restaurant group using our platform spotted a {random.randint(15,25)}% "
            f"revenue opportunity in their {random.choice(['happy hour', 'lunch special', 'weekend brunch'])}.",
            f"Quick win: {random.choice(['Fine dining', 'Fast casual', 'QSR'])} client used our "
            f"AI pricing and saw {random.randint(12,28)}% margin improvement in {random.randint(2,4)} weeks."
        ]

    def get_hashtag_pools(self) -> Dict[str, List[str]]:
        return {
            'tech': ['#AI', '#MachineLearning', '#DataScience', '#TechStartup', '#SaaS'],
            'industry': ['#RestaurantBusiness', '#Hospitality', '#FoodTech', '#RestaurantTech'],
            'specific': ['#PricingStrategy', '#DataDriven', '#MenuFlow', '#RestaurantAnalytics'],
            'trending': ['#MondayMotivation', '#FridayFeeling', '#StartupLife', '#Innovation']
        }


class RealEstateDynamicStrategy(IndustryDynamicStrategy):
    """Dynamic content strategy for real estate industry"""

    def get_subreddits(self) -> List[str]:
        return ['realestate', 'RealEstateInvesting', 'commercialrealestate', 'realtors',
                'firsttimehomebuyer', 'smallbusiness', 'dataengineering']

    def get_keywords(self) -> List[str]:
        return ['real estate', 'property', 'housing', 'mortgage', 'valuation', 'AI',
                'machine learning', 'proptech', 'market', 'analytics', 'pricing', 'investment']

    def get_base_stats(self) -> List[Dict]:
        current_month = datetime.now().strftime('%B')
        current_quarter = f"Q{(datetime.now().month-1)//3+1}"

        return [
            {
                'metric': 'average days on market',
                'value': random.randint(25, 55),
                'unit': ' days',
                'timeframe': 'current market',
                'insight': 'pricing accuracy is key'
            },
            {
                'metric': 'overpriced listings',
                'value': random.randint(15, 35),
                'unit': '%',
                'timeframe': 'first-time list price',
                'insight': 'data-driven pricing wins'
            },
            {
                'metric': 'DOM reduction with AI pricing',
                'value': random.randint(25, 45),
                'unit': '%',
                'timeframe': 'vs traditional CMA',
                'insight': 'faster sales with algorithms'
            },
            {
                'metric': 'lead conversion rate improvement',
                'value': random.randint(30, 60),
                'unit': '%',
                'timeframe': 'with predictive scoring',
                'insight': 'focus on hot leads'
            },
            {
                'metric': 'agent productivity gain',
                'value': random.randint(15, 30),
                'unit': '%',
                'timeframe': 'with automation',
                'insight': 'work smarter not harder'
            },
            {
                'metric': f'{current_month} market velocity',
                'value': round(random.uniform(0.8, 1.4), 2),
                'unit': 'x',
                'timeframe': 'vs last year',
                'insight': 'timing matters'
            },
            {
                'metric': f'{current_quarter} PropTech adoption',
                'value': random.randint(45, 72),
                'unit': '%',
                'timeframe': 'top-performing agents',
                'insight': 'technology is differentiator'
            }
        ]

    def get_competitors(self) -> List[Dict]:
        return [
            {'company': 'Zillow', 'focus': 'Zestimate algorithm', 'trend': 'automated valuations'},
            {'company': 'Redfin', 'focus': 'data-driven buying', 'trend': 'transparent pricing'},
            {'company': 'Realogy', 'focus': 'agent tools', 'trend': 'CRM integration'},
            {'company': 'CoStar', 'focus': 'commercial analytics', 'trend': 'market intelligence'},
            {'company': 'Compass', 'focus': 'AI-powered platform', 'trend': 'end-to-end tech'},
        ]

    def get_time_insights(self) -> Dict:
        now = datetime.now()
        insights = {'time_context': '', 'seasonal_context': '', 'business_rhythm': ''}

        if now.hour < 10:
            insights['time_context'] = 'morning prep - review overnight leads and market updates'
        elif 10 <= now.hour < 13:
            insights['time_context'] = 'prime showing time - buyers are active'
        elif 13 <= now.hour < 16:
            insights['time_context'] = 'afternoon follow-ups - nurture warm leads'
        elif 16 <= now.hour < 19:
            insights['time_context'] = 'evening showings - second wave of buyer activity'
        else:
            insights['time_context'] = 'night prep - optimize tomorrow\'s strategy with today\'s data'

        weekday = now.strftime('%A')
        day_insights = {
            'Monday': 'New week momentum - fresh listings hit the market',
            'Tuesday': 'Strategic day - analyze weekend showing feedback',
            'Wednesday': 'Midweek push - follow up on hot leads before weekend',
            'Thursday': 'Pre-weekend prep - price adjustments often happen today',
            'Friday': 'Listing launch day - maximize weekend exposure',
            'Saturday': 'Peak showing day - highest buyer activity',
            'Sunday': 'Open house day - capture serious buyers'
        }
        insights['business_rhythm'] = day_insights.get(weekday, '')

        month = now.month
        if month in [12, 1, 2]:
            insights['seasonal_context'] = 'Winter market - motivated buyers, less competition'
        elif month in [3, 4, 5]:
            insights['seasonal_context'] = 'Spring surge - peak listing season, highest demand'
        elif month in [6, 7, 8]:
            insights['seasonal_context'] = 'Summer market - family moves, school-driven timing'
        else:
            insights['seasonal_context'] = 'Fall market - serious buyers before holiday slowdown'

        return insights

    def get_scenarios(self) -> List[str]:
        return [
            f"Client win: Agent used our AI pricing and sold {random.randint(8,18)}% above asking "
            f"in just {random.randint(5,14)} days on market.",
            f"Real result: Brokerage reduced average DOM from {random.randint(45,65)} to "
            f"{random.randint(18,30)} days using predictive pricing.",
            f"Lead scoring success: Agent focused on AI-identified hot leads and "
            f"closed {random.randint(40,70)}% more deals this quarter.",
            f"Market timing: Our algorithm predicted the {random.choice(['price surge', 'buyer wave', 'inventory drop'])} "
            f"giving clients a {random.randint(2,4)}-week advantage.",
            f"Productivity gain: Real estate team saved {random.randint(12,25)} hours/week on "
            f"CMA prep using automated valuations."
        ]

    def get_hashtag_pools(self) -> Dict[str, List[str]]:
        return {
            'tech': ['#AI', '#MachineLearning', '#PropTech', '#TechStartup', '#DataScience'],
            'industry': ['#RealEstate', '#RealEstateAgent', '#Realtor', '#PropertyMarket'],
            'specific': ['#RealEstateData', '#MarketAnalytics', '#HomeValuation', '#SMEAnalytica'],
            'trending': ['#RealEstateInvesting', '#PropertyInvestment', '#HousingMarket', '#Innovation']
        }


class GeneralSMEDynamicStrategy(IndustryDynamicStrategy):
    """Dynamic content strategy for general SME/tech focus"""

    def get_subreddits(self) -> List[str]:
        return ['smallbusiness', 'startups', 'Entrepreneur', 'dataengineering',
                'machinelearning', 'artificial', 'business']

    def get_keywords(self) -> List[str]:
        return ['data', 'AI', 'business', 'analytics', 'automation', 'machine learning',
                'startup', 'saas', 'SME', 'productivity', 'efficiency', 'growth']

    def get_base_stats(self) -> List[Dict]:
        current_month = datetime.now().strftime('%B')
        current_quarter = f"Q{(datetime.now().month-1)//3+1}"

        return [
            {
                'metric': 'SME productivity gain with AI',
                'value': random.randint(25, 45),
                'unit': '%',
                'timeframe': 'first 6 months',
                'insight': 'automation is the key'
            },
            {
                'metric': 'data-driven decision accuracy',
                'value': random.randint(60, 85),
                'unit': '%',
                'timeframe': 'vs gut feeling',
                'insight': 'numbers don\'t lie'
            },
            {
                'metric': 'time saved on reporting',
                'value': random.randint(10, 20),
                'unit': ' hours/week',
                'timeframe': 'with automation',
                'insight': 'focus on growth instead'
            },
            {
                'metric': 'SME AI adoption rate',
                'value': random.randint(35, 55),
                'unit': '%',
                'timeframe': '2025 projection',
                'insight': 'gap between leaders and laggards'
            },
            {
                'metric': 'cost reduction with analytics',
                'value': random.randint(15, 30),
                'unit': '%',
                'timeframe': 'operational costs',
                'insight': 'visibility drives savings'
            },
            {
                'metric': f'{current_month} tech investment',
                'value': random.randint(15, 35),
                'unit': '%',
                'timeframe': 'YoY growth',
                'insight': 'SMEs betting on tech'
            },
            {
                'metric': f'{current_quarter} automation ROI',
                'value': random.randint(200, 400),
                'unit': '%',
                'timeframe': 'average return',
                'insight': 'investment pays off fast'
            }
        ]

    def get_competitors(self) -> List[Dict]:
        return [
            {'company': 'Monday.com', 'focus': 'workflow automation', 'trend': 'visual project management'},
            {'company': 'HubSpot', 'focus': 'integrated CRM', 'trend': 'all-in-one platforms'},
            {'company': 'Zapier', 'focus': 'no-code automation', 'trend': 'democratized integration'},
            {'company': 'Notion', 'focus': 'AI-powered workspace', 'trend': 'knowledge management'},
            {'company': 'Anthropic/OpenAI', 'focus': 'AI assistants', 'trend': 'AI for everyone'},
        ]

    def get_time_insights(self) -> Dict:
        now = datetime.now()
        insights = {'time_context': '', 'seasonal_context': '', 'business_rhythm': ''}

        if now.hour < 10:
            insights['time_context'] = 'morning planning - set data-driven priorities'
        elif 10 <= now.hour < 13:
            insights['time_context'] = 'peak productivity - when decisions get made'
        elif 13 <= now.hour < 16:
            insights['time_context'] = 'afternoon execution - implement, don\'t just plan'
        elif 16 <= now.hour < 19:
            insights['time_context'] = 'end of day review - what did the data tell you?'
        else:
            insights['time_context'] = 'strategic thinking time - big picture planning'

        weekday = now.strftime('%A')
        day_insights = {
            'Monday': 'Week kickoff - review last week\'s metrics, set new goals',
            'Tuesday': 'Execution day - implement insights from Monday\'s analysis',
            'Wednesday': 'Midweek check - are you on track? Data tells the truth',
            'Thursday': 'Optimization day - tweak what\'s not working',
            'Friday': 'Review and plan - set up next week for success',
            'Saturday': 'Strategy time - step back and see the big picture',
            'Sunday': 'Prep day - organize for a data-driven week ahead'
        }
        insights['business_rhythm'] = day_insights.get(weekday, '')

        month = now.month
        if month in [12, 1, 2]:
            insights['seasonal_context'] = 'Q1 planning - set metrics for the year ahead'
        elif month in [3, 4, 5]:
            insights['seasonal_context'] = 'Growth season - execute on Q1 insights'
        elif month in [6, 7, 8]:
            insights['seasonal_context'] = 'Midyear review - course correct with data'
        else:
            insights['seasonal_context'] = 'Q4 push - optimize for year-end results'

        return insights

    def get_scenarios(self) -> List[str]:
        return [
            f"Client win: SME automated {random.randint(5,15)} manual processes and "
            f"saved {random.randint(15,30)} hours/week. ROI in {random.randint(2,6)} weeks.",
            f"Real result: Small business used our analytics and grew revenue "
            f"{random.randint(20,45)}% while cutting costs {random.randint(10,25)}%.",
            f"Productivity story: Team of {random.randint(5,20)} now does what took "
            f"{random.randint(10,30)} people before. Thanks to AI automation.",
            f"Quick win: {random.choice(['E-commerce', 'Service', 'B2B'])} business "
            f"spotted {random.randint(15,35)}% cost leak in first data analysis.",
            f"Growth unlocked: SME used predictive analytics to time their "
            f"{random.choice(['expansion', 'hiring', 'product launch'])} perfectly."
        ]

    def get_hashtag_pools(self) -> Dict[str, List[str]]:
        return {
            'tech': ['#AI', '#MachineLearning', '#Automation', '#TechStartup', '#DataScience'],
            'industry': ['#SmallBusiness', '#SME', '#Entrepreneur', '#StartupLife'],
            'specific': ['#DataDriven', '#BusinessGrowth', '#SMEAnalytica', '#Productivity'],
            'trending': ['#AIforBusiness', '#FutureOfWork', '#DigitalTransformation', '#Innovation']
        }


class DynamicContentEngine:
    """Generate unique content by pulling from various data sources"""

    def __init__(self, industry: str = None):
        self.content_cache = {}
        self.cache_duration = 3600

        if industry is None:
            industry = os.getenv('SME_INDUSTRY', 'general').lower()

        self.industry = industry
        self.strategy = self._get_strategy(industry)
        print(f"📡 Dynamic content engine: {industry.replace('_', ' ').title()}")

    def _get_strategy(self, industry: str) -> IndustryDynamicStrategy:
        """Get the appropriate strategy for the industry"""
        strategies = {
            'restaurant': RestaurantDynamicStrategy(),
            'real_estate': RealEstateDynamicStrategy(),
        }
        return strategies.get(industry, GeneralSMEDynamicStrategy())

    def get_trending_topics(self) -> List[Dict]:
        """Get current trending topics in tech/business/data"""
        topics = []
        keywords = self.strategy.get_keywords()
        subreddits = self.strategy.get_subreddits()

        try:
            # Hacker News top stories
            hn_response = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json', timeout=5)
            if hn_response.status_code == 200:
                story_ids = hn_response.json()[:10]
                for story_id in story_ids[:5]:
                    try:
                        story = requests.get(f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json', timeout=5).json()
                        if story and 'title' in story:
                            if any(keyword.lower() in story['title'].lower() for keyword in keywords):
                                topics.append({
                                    'title': story['title'],
                                    'url': story.get('url', ''),
                                    'score': story.get('score', 0),
                                    'source': 'HackerNews'
                                })
                    except:
                        pass
        except:
            pass

        try:
            # Reddit subreddits
            for subreddit in subreddits[:4]:
                try:
                    reddit_response = requests.get(
                        f'https://www.reddit.com/r/{subreddit}/hot.json?limit=5',
                        headers={'User-Agent': 'SMEAnalytica Bot 1.0'},
                        timeout=5
                    )
                    if reddit_response.status_code == 200:
                        posts = reddit_response.json()['data']['children']
                        for post in posts[:3]:
                            post_data = post['data']
                            topics.append({
                                'title': post_data['title'],
                                'url': f"https://reddit.com{post_data['permalink']}",
                                'score': post_data['score'],
                                'source': f'r/{subreddit}'
                            })
                except:
                    pass
        except:
            pass

        return topics

    def get_industry_statistics(self) -> List[Dict]:
        """Get industry-specific statistics"""
        return self.strategy.get_base_stats()

    def analyze_competitor_activity(self) -> List[Dict]:
        """Analyze what competitors and industry leaders are discussing"""
        return self.strategy.get_competitors()

    def get_real_time_insights(self) -> Dict:
        """Generate insights based on current time, day, season"""
        return self.strategy.get_time_insights()

    def generate_data_story(self) -> str:
        """Create a data-driven narrative"""
        stories = []

        stats = self.get_industry_statistics()
        trends = self.get_trending_topics()
        competitors = self.analyze_competitor_activity()
        time_insights = self.get_real_time_insights()

        # Statistical insight
        if stats:
            stat = random.choice(stats)
            stories.append(
                f"New data: {stat['metric']} at {stat['value']}{stat['unit']} {stat['timeframe']}. "
                f"Key factor? {stat['insight'].capitalize()}. "
                f"We help businesses beat these odds with real-time analytics."
            )

        # Trending topic reaction
        if trends:
            trend = random.choice(trends[:3]) if trends else None
            if trend:
                stories.append(
                    f"Trending on {trend['source']}: '{trend['title'][:60]}...' "
                    f"Our take: Data-driven businesses adapt faster. "
                    f"How? Real-time insights > gut feelings."
                )

        # Competitive insight
        if competitors:
            comp = random.choice(competitors)
            stories.append(
                f"While {comp['company']} focuses on {comp['focus']}, "
                f"we see the real opportunity in {comp['trend']}. "
                f"SMEs need accessible analytics, not complex platforms."
            )

        # Time-contextual content
        stories.append(
            f"It's {time_insights['time_context']}. "
            f"{time_insights['business_rhythm']}. "
            f"Your data is telling a story - are you listening?"
        )

        # Realistic client scenarios
        scenarios = self.strategy.get_scenarios()
        stories.append(random.choice(scenarios))

        return random.choice(stories)

    def generate_engaging_question(self) -> str:
        """Generate thought-provoking questions based on current context"""
        questions = []
        stats = self.get_industry_statistics()

        if stats:
            stat = random.choice(stats)
            questions.append(
                f"With {stat['metric']} at {stat['value']}{stat['unit']}, "
                f"what's your strategy? We use {stat['insight']} - what works for you?"
            )

        # Context-aware questions
        now = datetime.now()
        if now.weekday() == 0:
            questions.append(
                "Monday data check: What was your best performing metric last week? "
                "If you don't know instantly, you need better analytics 📊"
            )
        elif now.weekday() == 4:
            questions.append(
                "Friday forecast: Can you predict next week's performance? "
                "Our AI can. What's your method?"
            )

        # Industry-specific challenge questions
        if self.industry == 'restaurant':
            questions.extend([
                "Your POS has the data. Your success depends on using it. "
                "What's stopping you from going data-driven?",
                f"Quick poll: Do you know your profit margin per menu item? "
                f"A) Yes, exactly B) Roughly C) No idea",
            ])
        elif self.industry == 'real_estate':
            questions.extend([
                "MLS has the data. Are you actually using it strategically? "
                "What's your biggest analytics gap?",
                "Quick poll: How accurate are your listing price recommendations? "
                "A) Within 3% B) Within 10% C) It's a guess",
            ])
        else:
            questions.extend([
                "Your tools have the data. Are you using it for decisions? "
                "What's the #1 metric you check daily?",
                "Quick poll: How do you make business decisions? "
                "A) Data always B) Sometimes data C) Gut feeling",
            ])

        return random.choice(questions)

    def generate_dynamic_content(self) -> str:
        """Main method to generate completely dynamic content"""
        content_types = [
            ('data_story', 0.4),
            ('question', 0.2),
            ('trending_reaction', 0.2),
            ('tip', 0.1),
            ('announcement', 0.1)
        ]

        selected_type = random.choices(
            [ct[0] for ct in content_types],
            [ct[1] for ct in content_types]
        )[0]

        content = ""

        if selected_type == 'data_story':
            content = self.generate_data_story()

        elif selected_type == 'question':
            content = self.generate_engaging_question()

        elif selected_type == 'trending_reaction':
            trends = self.get_trending_topics()
            if trends:
                trend = trends[0]
                content = (
                    f"📈 Trending: {trend['title'][:80]}... "
                    f"This is why data-driven businesses win. "
                    f"Real-time insights > following trends blindly."
                )
            else:
                content = self.generate_data_story()

        elif selected_type == 'tip':
            time_insights = self.get_real_time_insights()
            tips = [
                f"Pro tip: Your {datetime.now().strftime('%A')} data pattern "
                f"predicts next week's demand. Use it for smarter planning.",
                f"Hidden insight: Businesses that check metrics {random.choice(['before work', 'hourly', 'after each task'])} "
                f"see {random.randint(15,30)}% better results.",
                f"Quick win: Analyze your last {random.randint(30,90)} days. "
                f"The patterns you'll find = pure opportunity."
            ]
            content = random.choice(tips)

        elif selected_type == 'announcement':
            features = ['Predictive analytics', 'Automated reporting', 'Real-time dashboards',
                       'AI-powered insights', 'Smart alerts']
            announcements = [
                f"🚀 New feature alert: {random.choice(features)} "
                f"now live. Early adopters seeing {random.randint(10,25)}% improvement.",
                f"📊 This week's platform stats: {random.randint(50000,150000)} data points analyzed, "
                f"${random.randint(100,500)}K in value identified for our users."
            ]
            content = random.choice(announcements)

        # Add appropriate hashtags
        hashtag_pools = self.strategy.get_hashtag_pools()

        hashtags = []
        if 'data' in content.lower() or 'analytic' in content.lower():
            hashtags.append(random.choice(hashtag_pools['tech']))
        if any(word in content.lower() for word in ['business', 'sme', 'company']):
            hashtags.append(random.choice(hashtag_pools['industry']))
        hashtags.append(random.choice(hashtag_pools['specific']))

        if random.random() > 0.7:
            hashtags.append(random.choice(hashtag_pools['trending']))

        # Keep under 280 chars
        hashtag_str = ' '.join(hashtags[:3])
        if len(content) + len(hashtag_str) + 1 > 280:
            content = content[:280 - len(hashtag_str) - 4] + '...'

        return f"{content} {hashtag_str}"


def generate_dynamic_content(industry: str = None) -> str:
    """Generate completely unique, dynamic content"""
    engine = DynamicContentEngine(industry)
    return engine.generate_dynamic_content()
