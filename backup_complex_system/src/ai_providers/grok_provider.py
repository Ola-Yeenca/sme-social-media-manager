"""
Grok AI provider for trending topics and engagement
"""

import aiohttp
import asyncio
from typing import Dict, List, Any
from .base import BaseAIProvider, ContentRequest, GeneratedContent, APIError, RateLimitError

class GrokProvider(BaseAIProvider):
    """Grok AI provider for trending topics and viral engagement content"""
    
    def __init__(self, api_key: str, model_name: str = "grok-beta"):
        super().__init__(api_key, model_name)
        self.base_url = "https://api.x.ai/v1"
    
    @property
    def provider_name(self) -> str:
        return "Grok"
    
    @property
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    async def generate_content(self, request: ContentRequest) -> GeneratedContent:
        """Generate trending, engaging content using Grok"""
        try:
            prompt = self._build_trending_prompt(request)
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are Grok, creating engaging social media content that captures current trends while being informative about business analytics."
                        },
                        {"role": "user", "content": prompt}
                    ],
                    "model": self.model_name,
                    "max_tokens": 200,
                    "temperature": 0.8,  # Higher creativity for engagement
                    "stream": False
                }
                
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 429:
                        raise RateLimitError("Grok rate limit exceeded")
                    
                    response.raise_for_status()
                    data = await response.json()
                    
                    content_text = data["choices"][0]["message"]["content"].strip()
                    hashtags = self._extract_trending_hashtags(content_text, request.hashtags or [])
                    
                    return GeneratedContent(
                        text=content_text,
                        language=request.language,
                        hashtags=hashtags,
                        confidence_score=0.85,  # High for engagement potential
                        metadata={
                            "model": self.model_name,
                            "provider": self.provider_name,
                            "trending_focus": True,
                            "usage": data.get("usage", {})
                        }
                    )
                    
        except aiohttp.ClientResponseError as e:
            if e.status == 429:
                raise RateLimitError(f"Grok rate limit: {e}")
            raise APIError(f"Grok API error: {e}")
        except Exception as e:
            raise APIError(f"Grok error: {e}")
    
    async def analyze_engagement_opportunity(self, tweet_text: str, author: str) -> Dict[str, Any]:
        """Analyze using Grok's understanding of trending topics"""
        try:
            prompt = f"""
            Analyze this tweet for viral engagement potential and trending topic relevance:
            
            Tweet: "{tweet_text}"
            Author: @{author}
            
            Consider:
            - Current trending topics on X/Twitter
            - Viral content patterns
            - SME business context
            - Engagement timing
            
            Should SME Analytica engage? How can we add value while riding trends?
            """
            
            # Simplified response for now
            return {
                "viral_potential": 7,
                "trend_alignment": 8,
                "should_engage": True,
                "engagement_style": "witty_informative",
                "trending_angle": "AI business trends"
            }
            
        except Exception as e:
            raise APIError(f"Grok engagement analysis error: {e}")
    
    async def generate_reply(self, original_tweet: str, context: Dict[str, Any]) -> str:
        """Generate witty, engaging reply using Grok's style"""
        try:
            prompt = f"""
            Create a witty but informative reply that will get good engagement:
            
            Original tweet: "{original_tweet}"
            Context: {context}
            
            Style requirements:
            - Clever and engaging (Grok style)
            - Informative about SME analytics
            - Not overly promotional
            - Likely to get likes/retweets
            - Under 280 characters
            
            Add value while being memorable and shareable.
            """
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "messages": [{"role": "user", "content": prompt}],
                    "model": self.model_name,
                    "max_tokens": 100,
                    "temperature": 0.9
                }
                
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return data["choices"][0]["message"]["content"].strip()
                    
        except Exception as e:
            raise APIError(f"Grok reply generation error: {e}")
    
    def _build_trending_prompt(self, request: ContentRequest) -> str:
        """Build prompt optimized for trending, engaging content"""
        context_str = "\n".join([f"- {k}: {v}" for k, v in request.context.items()])
        
        return f"""
        Create a {request.content_type.value} for SME Analytica that's likely to go viral:
        
        Theme: {request.theme}
        Language: {request.language}
        Max length: {request.max_length} characters
        
        Context:
        {context_str}
        
        Make it:
        - Highly engaging and shareable
        - Tap into current trends when relevant
        - Educational but entertaining
        - Include surprising statistics or insights
        - Use hooks that make people want to read more
        
        SME Analytica focus:
        - AI-powered business analytics
        - Dynamic pricing success stories
        - Real-time data insights
        - Small business empowerment
        
        Create content that business owners will want to share with their networks.
        """
    
    def _extract_trending_hashtags(self, text: str, suggested_hashtags: List[str]) -> List[str]:
        """Extract hashtags optimized for viral potential"""
        hashtags = []
        
        # Trending business hashtags
        viral_tags = ["#SmallBizTech", "#AIRevolution", "#DataWins", "#BusinessTips"]
        
        # Mix suggested with viral potential tags
        all_tags = suggested_hashtags + viral_tags
        
        for tag in all_tags:
            if len(hashtags) < 4 and tag not in hashtags:
                hashtags.append(tag)
        
        # Ensure SME Analytica is included
        if "#SMEAnalytica" not in hashtags:
            hashtags[0] = "#SMEAnalytica"
        
        return hashtags[:4]


class MockGrokProvider(BaseAIProvider):
    """Mock Grok provider for when Grok API is not available"""
    
    def __init__(self, api_key: str = "mock", model_name: str = "mock-grok"):
        super().__init__(api_key, model_name)
    
    @property
    def provider_name(self) -> str:
        return "MockGrok"
    
    @property
    def is_available(self) -> bool:
        return True
    
    async def generate_content(self, request: ContentRequest) -> GeneratedContent:
        """Generate mock trending content"""
        trending_templates = {
            "data_monday": "📊 Monday Data Tip: AI-powered pricing can boost your restaurant margins by ~10% during peak hours. It's like having a revenue consultant working 24/7! #SMEAnalytica #DataInsights #RestaurantTech #AI",
            "tech_thursday": "🚀 Tech Thursday: MenuFlow integrates seamlessly with your existing POS system. No vendor switching, just supercharged analytics! Transform your restaurant data into profit. #MenuFlow #SMEAnalytica #HospitalityTech",
            "fact_friday": "💡 Fun Fact Friday: Small restaurants using dynamic pricing see 15% faster table turns during busy periods. Data + AI = happier customers and higher revenue! #SMEAnalytica #RestaurantAI #BusinessTips"
        }
        
        # Simple template selection based on theme
        template_key = request.theme.lower().replace(' ', '_')
        content_text = trending_templates.get(template_key, 
            "🎯 SME Analytica turns your business data into actionable insights. Real-time analytics made simple for restaurant, hotel, and retail owners. #SMEAnalytica #DataInsights #SmallBusiness")
        
        if request.language == "es":
            content_text = "📊 Consejo de datos: La IA puede aumentar los márgenes de tu restaurante ~10% en horas pico. ¡Como tener un consultor de ingresos 24/7! #SMEAnalytica #DatosInteligentes #RestauranteTech"
        
        return GeneratedContent(
            text=content_text,
            language=request.language,
            hashtags=["#SMEAnalytica", "#DataInsights", "#AI", "#SmallBusiness"],
            confidence_score=0.75,
            metadata={"provider": "MockGrok", "template_used": template_key}
        )
    
    async def analyze_engagement_opportunity(self, tweet_text: str, author: str) -> Dict[str, Any]:
        return {
            "viral_potential": 6,
            "should_engage": True,
            "engagement_style": "helpful",
            "response_type": "reply"
        }
    
    async def generate_reply(self, original_tweet: str, context: Dict[str, Any]) -> str:
        return "Great point! At SME Analytica, we've seen AI-driven analytics help small businesses increase efficiency by focusing on data that actually drives decisions. 📊✨"
