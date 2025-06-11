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
        Max length: {request.max_length} characters
        Tone: {request.tone}
        
        Context:
        {context_str}
        
        Requirements:
        - Focus on SME business analytics and AI insights
        - Include relevant hashtags naturally
        - Be educational and engaging
        - Highlight practical business value
        """
    
    def _get_system_prompt(self, request: ContentRequest) -> str:
        """Get system prompt for consistent brand voice"""
        return """
        You are the social media voice for SME Analytica, an AI-driven analytics platform for small and medium enterprises.
        
        Brand voice:
        - Conversational yet expert
        - Educational and helpful
        - Focus on practical business value
        - Friendly data consultant tone
        - Avoid heavy jargon, explain concepts simply
        
        Key messaging:
        - AI-powered dynamic pricing boosts margins ~10%
        - Real-time analytics without complex setup
        - Vertical-specific solutions (MenuFlow for restaurants)
        - Built for non-technical business owners
        
        Always provide actionable insights and position SME Analytica as the friendly AI analyst for small businesses.
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
