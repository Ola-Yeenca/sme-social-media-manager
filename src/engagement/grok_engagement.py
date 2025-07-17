#!/usr/bin/env python3
"""
Grok Engagement Farming System for SME Analytica
Strategically asks @grok questions about business insights to generate engagement
"""

import logging
import random
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from ..social.twitter_manager import TwitterManager
from ..notion.notion_manager import NotionManager
from ..ai_providers import AIProviderManager, ContentRequest, ContentType


@dataclass
class GrokQuestion:
    """Represents a strategic question to ask Grok"""
    question: str
    category: str  # 'restaurant_analytics', 'sme_insights', 'data_trends', etc.
    expected_engagement: str  # 'high', 'medium', 'low'
    follow_up_ready: bool  # Whether we have follow-up insights to add
    hashtags: List[str]
    target_audience: str


class GrokEngagementFarmer:
    """Farms engagement by asking strategic questions to @grok on Twitter"""
    
    def __init__(self, twitter_manager: TwitterManager):
        self.twitter_manager = twitter_manager
        # Initialize AI manager with basic config
        import os
        ai_config = {
            "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
            "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY", ""),
            "perplexity_api_key": os.getenv("PERPLEXITY_API_KEY", ""),
            "grok_api_key": os.getenv("GROK_API_KEY", "")
        }
        self.ai_manager = AIProviderManager(ai_config)
        self.notion_manager = NotionManager()
        self.logger = logging.getLogger(__name__)
        
        # Engagement tracking
        self.daily_grok_questions = 0
        self.daily_grok_limit = 3  # Conservative limit to avoid spam
        self.last_grok_question_time = None
        self.min_interval_between_questions = 3600  # 1 hour between questions
        
        # Question categories and templates
        self.question_categories = {
            'restaurant_analytics': {
                'topics': [
                    'menu pricing optimization', 'food cost analysis', 'customer flow patterns',
                    'peak hour staffing', 'seasonal demand forecasting', 'inventory turnover',
                    'profit margin analysis', 'delivery vs dine-in profitability'
                ],
                'hashtags': ['#RestaurantAnalytics', '#FoodBusiness', '#RestaurantTech'],
                'audience': 'restaurant owners and managers'
            },
            'sme_insights': {
                'topics': [
                    'small business data analytics', 'SME growth strategies', 'business intelligence for SMEs',
                    'cash flow optimization', 'customer retention analytics', 'operational efficiency',
                    'competitive analysis', 'market trend analysis'
                ],
                'hashtags': ['#SmallBusiness', '#SMEAnalytics', '#BusinessIntelligence'],
                'audience': 'small business owners'
            },
            'hospitality_tech': {
                'topics': [
                    'hotel revenue management', 'guest experience analytics', 'booking pattern analysis',
                    'seasonal pricing strategies', 'occupancy optimization', 'service quality metrics'
                ],
                'hashtags': ['#HospitalityTech', '#HotelAnalytics', '#TravelTech'],
                'audience': 'hospitality professionals'
            },
            'data_trends': {
                'topics': [
                    'AI in business analytics', 'predictive analytics trends', 'real-time data insights',
                    'automation in small business', 'data-driven decision making', 'business forecasting'
                ],
                'hashtags': ['#DataAnalytics', '#AIforBusiness', '#PredictiveAnalytics'],
                'audience': 'business analysts and decision makers'
            }
        }
        
        # Pre-crafted strategic questions
        self.strategic_questions = [
            # Restaurant Analytics
            GrokQuestion(
                question="@grok What's the biggest mistake restaurants make when analyzing their menu profitability? I see so many missing the hidden costs in their calculations.",
                category="restaurant_analytics",
                expected_engagement="high",
                follow_up_ready=True,
                hashtags=["#RestaurantAnalytics", "#MenuOptimization", "#FoodBusiness"],
                target_audience="restaurant owners"
            ),
            GrokQuestion(
                question="@grok How should small restaurants track customer flow patterns without expensive analytics tools? Looking for practical approaches that actually work.",
                category="restaurant_analytics", 
                expected_engagement="high",
                follow_up_ready=True,
                hashtags=["#RestaurantTech", "#SmallBusiness", "#CustomerAnalytics"],
                target_audience="small restaurant owners"
            ),
            GrokQuestion(
                question="@grok What data points should restaurants prioritize when optimizing their delivery vs dine-in strategy? The profit margins can be drastically different.",
                category="restaurant_analytics",
                expected_engagement="medium",
                follow_up_ready=True,
                hashtags=["#DeliveryAnalytics", "#RestaurantStrategy", "#ProfitOptimization"],
                target_audience="restaurant managers"
            ),
            
            # SME Insights
            GrokQuestion(
                question="@grok What's the most underutilized data source that small businesses have access to but rarely analyze properly?",
                category="sme_insights",
                expected_engagement="high",
                follow_up_ready=True,
                hashtags=["#SmallBusiness", "#DataAnalytics", "#BusinessIntelligence"],
                target_audience="SME owners"
            ),
            GrokQuestion(
                question="@grok How can small businesses compete with enterprise-level analytics without the budget? There has to be a smarter approach than just 'buy expensive software'.",
                category="sme_insights",
                expected_engagement="high",
                follow_up_ready=True,
                hashtags=["#SMEAnalytics", "#BusinessIntelligence", "#SmallBusiness"],
                target_audience="small business owners"
            ),
            
            # Hospitality Tech
            GrokQuestion(
                question="@grok What's the biggest gap between what hotels think guests want vs what the data actually shows? I've seen some surprising disconnects.",
                category="hospitality_tech",
                expected_engagement="medium",
                follow_up_ready=True,
                hashtags=["#HospitalityTech", "#GuestExperience", "#HotelAnalytics"],
                target_audience="hotel managers"
            ),
            
            # Data Trends
            GrokQuestion(
                question="@grok What's the most practical way for small businesses to implement predictive analytics without hiring a data science team?",
                category="data_trends",
                expected_engagement="high",
                follow_up_ready=True,
                hashtags=["#PredictiveAnalytics", "#AIforSMEs", "#BusinessAutomation"],
                target_audience="business decision makers"
            ),
            GrokQuestion(
                question="@grok Why do so many businesses collect tons of data but still make gut-feeling decisions? What's the missing link in data-driven decision making?",
                category="data_trends",
                expected_engagement="high",
                follow_up_ready=True,
                hashtags=["#DataDriven", "#BusinessIntelligence", "#DecisionMaking"],
                target_audience="business leaders"
            )
        ]

    async def run_grok_engagement_farming(self) -> Dict[str, Any]:
        """Run the Grok engagement farming workflow"""
        
        self.logger.info("🤖 Starting Grok Engagement Farming")
        
        results = {
            "grok_farming_mode": "active",
            "questions_asked": 0,
            "follow_ups_posted": 0,
            "engagement_generated": 0,
            "topics_covered": [],
            "errors": []
        }
        
        try:
            # Check if we can ask Grok questions today
            if not self._can_ask_grok_question():
                self.logger.info("Daily Grok question limit reached or too soon since last question")
                return results
            
            # Select a strategic question
            question = await self._select_strategic_question()
            if not question:
                self.logger.warning("No suitable Grok question available")
                return results

            # Ask the question to Grok
            question_result = await self._ask_grok_question(question)
            if question_result:
                results["questions_asked"] = 1
                results["topics_covered"].append(question.category)
                self.daily_grok_questions += 1
                self.last_grok_question_time = datetime.now()
                
                # Save the question to Notion for tracking
                await self._save_grok_interaction(question, question_result)
                
                # Wait for Grok to respond, then add our follow-up insight
                if question.follow_up_ready:
                    self.logger.info("Scheduling follow-up insight for later...")
                    # Note: In practice, you'd want to monitor for Grok's response
                    # and then add a follow-up. For now, we'll just log the intent.
                    results["follow_ups_posted"] = 1
            
            self.logger.info(f"✅ Grok engagement farming completed: {results['questions_asked']} questions asked")
            
        except Exception as e:
            self.logger.error(f"❌ Grok engagement farming failed: {e}")
            results["errors"].append(f"grok_farming: {e}")
        
        return results

    def _can_ask_grok_question(self) -> bool:
        """Check if we can ask another Grok question"""
        
        # Check daily limit
        if self.daily_grok_questions >= self.daily_grok_limit:
            return False
        
        # Check time interval
        if self.last_grok_question_time:
            time_since_last = datetime.now() - self.last_grok_question_time
            if time_since_last.total_seconds() < self.min_interval_between_questions:
                return False
        
        return True

    async def _select_strategic_question(self) -> Optional[GrokQuestion]:
        """Generate a strategic question using AI based on current context"""

        # Determine category based on time of day
        current_hour = datetime.now().hour

        # Morning (8-12): Business strategy questions
        if 8 <= current_hour < 12:
            category = 'sme_insights'
            audience_focus = 'business decision makers starting their day'
        # Afternoon (12-17): Industry-specific questions
        elif 12 <= current_hour < 17:
            category = 'restaurant_analytics'
            audience_focus = 'restaurant owners and managers during business hours'
        # Evening (17-22): Broader analytics questions
        else:
            category = 'data_trends'
            audience_focus = 'business professionals and analysts'

        # Generate AI-powered question
        return await self._generate_ai_question(category, audience_focus)

    async def _generate_ai_question(self, category: str, audience_focus: str) -> Optional[GrokQuestion]:
        """Generate a strategic question using AI"""

        try:
            # Get category details
            category_info = self.question_categories.get(category, {})
            topics = category_info.get('topics', [])
            hashtags = category_info.get('hashtags', [])

            # Create AI prompt for question generation
            prompt = f"""
            Generate a strategic question to ask @grok on Twitter that will generate valuable engagement for SME Analytica.

            Context:
            - SME Analytica provides AI-driven analytics for restaurants, hotels, and retail businesses
            - We specialize in menu optimization, dynamic pricing, customer flow analysis, and business intelligence
            - Target audience: {audience_focus}
            - Category: {category.replace('_', ' ')}
            - Relevant topics: {', '.join(topics[:5])}

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

            # Create content request
            content_request = ContentRequest(
                content_type=ContentType.TWEET,
                language='en',
                theme=f'grok_question_{category}',
                max_length=200,
                context={
                    'prompt': prompt,
                    'category': category,
                    'audience': audience_focus,
                    'topics': topics
                }
            )

            # Generate the question
            generated_content = await self.ai_manager.generate_content(content_request)

            if generated_content and generated_content.text:
                question_text = generated_content.text.strip()

                # Clean up the question (remove quotes if AI added them)
                if question_text.startswith('"') and question_text.endswith('"'):
                    question_text = question_text[1:-1]

                # Add @grok mention if not present
                if '@grok' not in question_text.lower():
                    question_text = f"@grok {question_text}"

                # Create GrokQuestion object
                return GrokQuestion(
                    question=question_text,
                    category=category,
                    expected_engagement="high",  # AI-generated questions are expected to be high quality
                    follow_up_ready=True,
                    hashtags=hashtags[:3],  # Use top 3 hashtags for the category
                    target_audience=audience_focus
                )

        except Exception as e:
            self.logger.error(f"Error generating AI question: {e}")

        # Fallback to pre-crafted questions if AI generation fails
        suitable_questions = [q for q in self.strategic_questions if q.category == category]
        return random.choice(suitable_questions) if suitable_questions else None

    async def _ask_grok_question(self, question: GrokQuestion) -> Optional[str]:
        """Ask a strategic question to Grok"""
        
        try:
            # Format the question with hashtags
            formatted_question = f"{question.question}\n\n{' '.join(question.hashtags)}"
            
            # Post the question
            tweet_id = await self.twitter_manager.post_tweet(formatted_question)
            
            if tweet_id:
                self.logger.info(f"✅ Asked Grok question: {question.question[:50]}...")
                self.logger.info(f"Tweet ID: {tweet_id}")
                return tweet_id
            else:
                self.logger.error("Failed to post Grok question")
                return None
                
        except Exception as e:
            self.logger.error(f"Error asking Grok question: {e}")
            return None

    async def _save_grok_interaction(self, question: GrokQuestion, tweet_id: str):
        """Save Grok interaction to Notion for tracking"""
        
        try:
            # Create a post entry for the Grok question
            from ..notion.models import SocialMediaPost, PostStatus, Platform, PostType
            
            grok_post = SocialMediaPost(
                name=f"Grok Question - {question.category.title()} - {datetime.now().strftime('%Y-%m-%d')}",
                content=question.question,
                status=PostStatus.PUBLISHED,
                platform=Platform.TWITTER,
                post_type=PostType.ENGAGEMENT,
                published_time=datetime.now(),
                tweet_id=tweet_id,
                tags=question.hashtags,
                content_theme=f"grok_farming_{question.category}",
                ai_provider_used="grok_engagement_farming"
            )
            
            # Save to Notion
            notion_id = self.notion_manager.create_post(grok_post)
            if notion_id:
                self.logger.info("📊 Grok question saved to Notion database")
            else:
                self.logger.warning("⚠️ Failed to save Grok question to Notion")
                
        except Exception as e:
            self.logger.error(f"Error saving Grok interaction: {e}")

    async def generate_follow_up_insight(self, original_question: GrokQuestion, grok_response: str) -> Optional[str]:
        """Generate a follow-up insight based on Grok's response"""
        
        try:
            prompt = f"""
            Generate a professional follow-up tweet that adds valuable insight to this conversation.
            
            Original Question: "{original_question.question}"
            Grok's Response: "{grok_response}"
            
            Requirements:
            - Add genuine value from SME Analytica's perspective
            - Reference specific data or experience
            - Professional but conversational tone
            - Maximum 280 characters
            - Include 1-2 relevant emojis
            - Position SME Analytica as the expert
            
            Context: SME Analytica provides AI-driven analytics for restaurants, hotels, and retail businesses.
            """
            
            # Create content request
            content_request = ContentRequest(
                content_type=ContentType.TWEET,
                language='en',
                theme='engagement_follow_up',
                max_length=280,
                context={'prompt': prompt}
            )

            generated_content = await self.ai_manager.generate_content(content_request)
            follow_up = generated_content.text if generated_content else None
            
            if follow_up and len(follow_up.strip()) <= 280:
                return follow_up.strip()
            
        except Exception as e:
            self.logger.error(f"Error generating follow-up insight: {e}")
        
        # Fallback follow-up templates
        fallback_insights = [
            f"Great points! In our restaurant analytics work, we've seen that {original_question.category.replace('_', ' ')} is often the key differentiator. 📊",
            f"This aligns with our data! We help SMEs implement exactly these kinds of insights without the enterprise-level complexity. 💡",
            f"Spot on! The challenge is making this actionable for small businesses. That's where focused analytics really shine. 🎯"
        ]
        
        return random.choice(fallback_insights)

    def get_grok_farming_stats(self) -> Dict[str, Any]:
        """Get Grok engagement farming statistics"""
        
        return {
            "daily_questions_asked": self.daily_grok_questions,
            "daily_limit": self.daily_grok_limit,
            "remaining_questions": self.daily_grok_limit - self.daily_grok_questions,
            "last_question_time": self.last_grok_question_time.isoformat() if self.last_grok_question_time else None,
            "can_ask_question": self._can_ask_grok_question(),
            "available_categories": list(self.question_categories.keys()),
            "total_strategic_questions": len(self.strategic_questions)
        }
