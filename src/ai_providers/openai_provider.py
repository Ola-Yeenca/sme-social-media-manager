"""
OpenAI GPT provider for content generation
"""

import openai
import asyncio
from typing import Dict, List, Any
from .base import BaseAIProvider, ContentRequest, GeneratedContent, APIError, RateLimitError

class OpenAIProvider(BaseAIProvider):
    """OpenAI GPT provider for creative content generation"""
    
    def __init__(self, api_key: str, model_name: str = "gpt-4-turbo-preview"):
        super().__init__(api_key, model_name)
        self.client = openai.AsyncOpenAI(api_key=api_key)
    
    @property
    def provider_name(self) -> str:
        return "OpenAI"
    
    @property
    def is_available(self) -> bool:
        return bool(self.api_key and self.client)
    
    async def generate_content(self, request: ContentRequest) -> GeneratedContent:
        """Generate content using OpenAI GPT"""
        try:
            prompt = self._build_prompt(request)
            
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": self._get_system_prompt(request)},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            content_text = response.choices[0].message.content.strip()
            hashtags = self._extract_hashtags(content_text, request.hashtags or [])
            
            return GeneratedContent(
                text=content_text,
                language=request.language,
                hashtags=hashtags,
                confidence_score=0.85,
                metadata={
                    "model": self.model_name,
                    "provider": self.provider_name,
                    "usage": response.usage.dict() if response.usage else {}
                }
            )
            
        except openai.RateLimitError as e:
            raise RateLimitError(f"OpenAI rate limit exceeded: {e}")
        except Exception as e:
            raise APIError(f"OpenAI API error: {e}")
    
    async def analyze_engagement_opportunity(self, tweet_text: str, author: str) -> Dict[str, Any]:
        """Analyze engagement opportunity using GPT"""
        try:
            prompt = f"""
            Analyze this tweet for engagement opportunity from SME Analytica's perspective:
            
            Tweet: "{tweet_text}"
            Author: @{author}
            
            Evaluate:
            1. Relevance to SME business analytics (0-10)
            2. Engagement potential (0-10)
            3. Brand alignment opportunity (0-10)
            4. Suggested response type (reply, like, retweet, ignore)
            5. Key talking points if engaging
            
            Respond in JSON format.
            """
            
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.3
            )
            
            # Parse response (would need JSON parsing logic here)
            return {"relevance_score": 7, "should_engage": True, "response_type": "reply"}
            
        except Exception as e:
            raise APIError(f"OpenAI engagement analysis error: {e}")
    
    async def generate_reply(self, original_tweet: str, context: Dict[str, Any]) -> str:
        """Generate a contextual reply"""
        try:
            prompt = f"""
            Generate a helpful, professional reply to this tweet from SME Analytica:
            
            Original tweet: "{original_tweet}"
            Context: {context}
            
            Reply should:
            - Be helpful and add value
            - Mention relevant SME Analytica solutions naturally
            - Stay under 280 characters
            - Use a conversational but expert tone
            """
            
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.6
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise APIError(f"OpenAI reply generation error: {e}")
    
    def _build_prompt(self, request: ContentRequest) -> str:
        """Build prompt based on content request"""
        context_str = "\n".join([f"- {k}: {v}" for k, v in request.context.items()])
        
        return f"""
        Create a {request.content_type.value} for SME Analytica in {request.language}.

        Theme: {request.theme}
        Length: Be flexible! Twitter subscription allows longer posts, LinkedIn supports up to 3000 chars
        Create engaging, detailed content that tells a complete story
        Tone: {request.tone}
        
        Context:
        {context_str}
        
        CRITICAL REQUIREMENTS:
        - Create COMPLETELY UNIQUE content - no repeated phrases, structures, or hooks
        - Vary your opening: questions, bold statements, data reveals, stories, contrarian takes
        - Use different restaurant names, scenarios, and data points each time
        - Be genuinely insightful about real restaurant business challenges
        - Include surprising, non-obvious insights that make people think
        - Focus on practical business value with fresh perspectives
        - Make each post feel like it comes from a different expert/angle
        - Avoid formulaic "This will shock you" or similar repetitive openings
        - Create content that restaurant owners would actually want to share
        """
    
    def _get_system_prompt(self, request: ContentRequest) -> str:
        """Get system prompt for consistent brand voice"""
        return """
        You are the social media voice for SME Analytica, an AI-driven analytics and business intelligence platform built for small and medium enterprises.

        COMPREHENSIVE COMPANY CONTEXT:
        SME Analytica's mission: "understand your data, improve your pricing, and grow your business" without complex tech setup.
        We turn raw sales, traffic and customer data into actionable insights and automation tailored for small businesses.

        CORE VALUE PROPOSITION:
        - Enterprise-level analytics made accessible to non-technical business owners
        - AI-powered dynamic pricing that boosts margins by ~10% during peak hours (verified results)
        - Real-time analytics without complex tech setup
        - Seamless integration with existing POS, reservation, and accounting tools
        - Vertical-specific modules with industry-tailored features

        KEY PRODUCTS & PROVEN RESULTS:
        1. MenuFlow (Restaurants): Smart QR menu/ordering + AI pricing + real-time analytics
           - PROVEN: 10% higher margins during peak hours, faster table turns, higher average checks
           - Features: Real-time menu updates, personalized recommendations, loyalty discounts
        2. Hotel Analytics (Coming Soon): Occupancy analytics, ADR, RevPAR, guest sentiment
        3. Retail Insights (In Development): Sales analysis, inventory turnover, customer patterns

        BRAND VOICE & TONE:
        - Conversational yet expert (like a knowledgeable consultant chatting with a business owner)
        - Enthusiastic about data but speaking plainly
        - Educational and engaging - make readers feel smarter
        - Use everyday analogies, avoid heavy jargon
        - Always root statements in data/examples and emphasize tangible ROI

        TARGET AUDIENCE:
        - Restaurant owners, hotel managers, retail shop owners
        - Small business entrepreneurs seeking data-driven growth
        - Non-technical business owners who need enterprise-level insights
        - Spanish-speaking SME community (Spain, LatAm)
        - European small business market

        CONTENT STRATEGY BY THEME:
        - Data Monday: Educational data tips and business insights with real SME Analytica results
        - Talk Tuesday: Industry discussions, polls, community engagement
        - Case Study Wednesday: Real success stories and client examples (use proven 10% margin boost)
        - Tech Thursday: Technology features, integrations, innovations
        - Fact Friday: Industry statistics, trends, educational content
        - Weekend Insights: Lighter content, tips, community engagement

        VIRAL OPTIMIZATION GUIDELINES:
        - NEVER repeat the same hook, structure, or opening line
        - Vary your approach: data insights, personal stories, industry secrets, surprising facts, contrarian takes
        - Use different restaurant names and scenarios each time
        - Mix content types: case studies, industry insights, behind-the-scenes, data revelations, trend analysis
        - Vary emotional hooks: surprise, curiosity, controversy, inspiration, urgency, exclusivity
        - Include diverse data points beyond just "10% margin boost"
        - Create thought-provoking content that sparks discussion
        - Be genuinely insightful about restaurant/SME business challenges

        Always provide actionable insights, use specific data points (especially the proven 10% margin boost),
        and position SME Analytica as the friendly AI analyst that delivers real, measurable results for small businesses.
        Make business owners feel smarter and more confident about using data to grow their business.

        IMPORTANT FORMATTING RULES:
        - Do NOT wrap the content in quotation marks
        - Write the content directly without quotes around it
        - Make it sound natural and authentic, not AI-generated
        - Avoid any formatting that makes it look like a quoted statement
        """
    
    def _extract_hashtags(self, text: str, suggested_hashtags: List[str]) -> List[str]:
        """Extract and optimize hashtags from generated content"""
        # Simple hashtag extraction logic
        hashtags = []
        for tag in suggested_hashtags:
            if tag.lower() in text.lower():
                hashtags.append(tag)
        
        # Add default SME Analytica hashtags if none found
        if not hashtags:
            hashtags = ["#SMEAnalytica", "#DataInsights"]
        
        return hashtags[:4]  # Limit to 4 hashtags
