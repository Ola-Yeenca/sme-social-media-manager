"""
Anthropic Claude provider for analytical content
"""

import anthropic
import asyncio
from typing import Dict, List, Any
from .base import BaseAIProvider, ContentRequest, GeneratedContent, APIError, RateLimitError

class AnthropicProvider(BaseAIProvider):
    """Anthropic Claude provider for analytical and insight-driven content"""
    
    def __init__(self, api_key: str, model_name: str = "claude-3-sonnet-20240229"):
        super().__init__(api_key, model_name)
        self.client = anthropic.AsyncAnthropic(api_key=api_key)
    
    @property
    def provider_name(self) -> str:
        return "Anthropic"
    
    @property
    def is_available(self) -> bool:
        return bool(self.api_key and self.client)
    
    async def generate_content(self, request: ContentRequest) -> GeneratedContent:
        """Generate analytical content using Claude"""
        try:
            prompt = self._build_analytical_prompt(request)
            
            response = await self.client.messages.create(
                model=self.model_name,
                max_tokens=200,
                temperature=0.6,
                messages=[{"role": "user", "content": prompt}]
            )
            
            content_text = response.content[0].text.strip()
            hashtags = self._extract_hashtags(content_text, request.hashtags or [])
            
            return GeneratedContent(
                text=content_text,
                language=request.language,
                hashtags=hashtags,
                confidence_score=0.90,  # Claude is great for analytical content
                metadata={
                    "model": self.model_name,
                    "provider": self.provider_name,
                    "usage": response.usage.dict() if hasattr(response, 'usage') else {}
                }
            )
            
        except anthropic.RateLimitError as e:
            raise RateLimitError(f"Anthropic rate limit exceeded: {e}")
        except Exception as e:
            raise APIError(f"Anthropic API error: {e}")
    
    async def analyze_engagement_opportunity(self, tweet_text: str, author: str) -> Dict[str, Any]:
        """Analyze engagement opportunity using Claude's analytical capabilities"""
        try:
            prompt = f"""
            As an AI analyst for SME Analytica, evaluate this tweet for engagement potential:
            
            Tweet: "{tweet_text}"
            Author: @{author}
            
            SME Analytica context:
            - AI-driven analytics for small/medium enterprises
            - Specializes in restaurant analytics (MenuFlow), retail insights, hotel analytics
            - Focus on dynamic pricing, real-time analytics, business intelligence
            
            Please analyze:
            1. Business relevance (0-10): How relevant is this to SME business analytics?
            2. Engagement value (0-10): Would engaging add value to both parties?
            3. Brand fit (0-10): How well does this align with our expertise?
            4. Recommended action: reply, like, retweet, or ignore
            5. If replying, what key value could we add?
            
            Provide a structured assessment.
            """
            
            response = await self.client.messages.create(
                model=self.model_name,
                max_tokens=300,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # For now, return a structured response (you'd parse the actual response)
            return {
                "relevance_score": 8,
                "engagement_value": 7,
                "brand_fit": 9,
                "should_engage": True,
                "response_type": "reply",
                "key_value": "AI-driven pricing insights"
            }
            
        except Exception as e:
            raise APIError(f"Anthropic engagement analysis error: {e}")
    
    async def generate_reply(self, original_tweet: str, context: Dict[str, Any]) -> str:
        """Generate insightful reply using Claude"""
        try:
            prompt = f"""
            Generate a helpful reply to this tweet from SME Analytica's perspective:
            
            Original tweet: "{original_tweet}"
            Context: {context}
            
            SME Analytica expertise:
            - AI-powered dynamic pricing (10% margin boost proven)
            - Real-time analytics for restaurants, hotels, retail
            - MenuFlow: QR ordering + analytics for restaurants
            - Business intelligence made simple for SME owners
            
            Reply requirements:
            - Add genuine value to the conversation
            - Share a relevant insight or tip
            - Mention SME Analytica solutions naturally (not sales-y)
            - Keep under 280 characters
            - Use friendly expert tone
            
            Focus on being helpful first, promotional second.
            """
            
            response = await self.client.messages.create(
                model=self.model_name,
                max_tokens=150,
                temperature=0.5,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            raise APIError(f"Anthropic reply generation error: {e}")
    
    def _build_analytical_prompt(self, request: ContentRequest) -> str:
        """Build analytical prompt for Claude"""
        context_str = "\n".join([f"- {k}: {v}" for k, v in request.context.items()])
        
        language_instruction = {
            "en": "Generate content in English",
            "es": "Generate content in Spanish",
            "fr": "Generate content in French"
        }.get(request.language, "Generate content in English")
        
        return f"""
        You are creating social media content for SME Analytica, an AI-driven analytics and business intelligence platform built for small and medium enterprises.

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

        Task: Create a {request.content_type.value} with these specifications:
        - Theme: {request.theme}
        - Language: {language_instruction}
        - Max length: {request.max_length} characters
        - Tone: Expert but conversational, like a friendly data consultant

        Context for this post:
        {context_str}

        CONTENT STRATEGY BY THEME:
        - Data Monday: Educational data tips and business insights with real SME Analytica results
        - Talk Tuesday: Industry discussions, polls, community engagement
        - Case Study Wednesday: Real success stories and client examples (use proven 10% margin boost)
        - Tech Thursday: Technology features, integrations, innovations
        - Fact Friday: Industry statistics, trends, educational content
        - Weekend Insights: Lighter content, tips, community engagement

        Content guidelines:
        - Focus on practical business value and actionable insights
        - Use specific data points (especially the proven 10% margin boost)
        - Reference real SME Analytica capabilities and results
        - Avoid heavy jargon - explain concepts simply
        - Include relevant hashtags naturally
        - Position SME Analytica as the helpful AI analyst that delivers real results
        - Make business owners feel smarter and more confident about using data

        Create engaging content that educates, inspires, and showcases SME Analytica's proven value.
        """
    
    def _extract_hashtags(self, text: str, suggested_hashtags: List[str]) -> List[str]:
        """Extract and optimize hashtags for analytical content"""
        hashtags = []
        
        # Check for suggested hashtags in content
        for tag in suggested_hashtags:
            if tag.lower().replace('#', '') in text.lower():
                hashtags.append(tag)
        
        # Add analytical content specific hashtags
        analytical_tags = ["#DataInsights", "#BusinessIntelligence", "#SMEAnalytica"]
        for tag in analytical_tags:
            if tag not in hashtags and len(hashtags) < 4:
                hashtags.append(tag)
        
        return hashtags[:4]
