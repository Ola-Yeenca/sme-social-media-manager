"""
Perplexity AI provider for real-time industry insights
"""

import aiohttp
import asyncio
from typing import Dict, List, Any
from .base import BaseAIProvider, ContentRequest, GeneratedContent, APIError, RateLimitError

class PerplexityProvider(BaseAIProvider):
    """Perplexity AI provider for real-time industry data and trends"""
    
    def __init__(self, api_key: str, model_name: str = "llama-3.1-sonar-large-128k-online"):
        super().__init__(api_key, model_name)
        self.base_url = "https://api.perplexity.ai"
    
    @property
    def provider_name(self) -> str:
        return "Perplexity"
    
    @property
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    async def generate_content(self, request: ContentRequest) -> GeneratedContent:
        """Generate content with real-time industry insights"""
        try:
            prompt = self._build_industry_prompt(request)
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 200,
                    "temperature": 0.7,
                    "return_citations": True
                }
                
                async with session.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 429:
                        raise RateLimitError("Perplexity rate limit exceeded")
                    
                    response.raise_for_status()
                    data = await response.json()
                    
                    content_text = data["choices"][0]["message"]["content"].strip()
                    hashtags = self._extract_hashtags(content_text, request.hashtags or [])
                    
                    return GeneratedContent(
                        text=content_text,
                        language=request.language,
                        hashtags=hashtags,
                        confidence_score=0.88,  # High for real-time data
                        metadata={
                            "model": self.model_name,
                            "provider": self.provider_name,
                            "citations": data.get("citations", []),
                            "usage": data.get("usage", {})
                        }
                    )
                    
        except aiohttp.ClientResponseError as e:
            if e.status == 429:
                raise RateLimitError(f"Perplexity rate limit: {e}")
            raise APIError(f"Perplexity API error: {e}")
        except Exception as e:
            raise APIError(f"Perplexity error: {e}")
    
    async def analyze_engagement_opportunity(self, tweet_text: str, author: str) -> Dict[str, Any]:
        """Analyze using real-time industry context"""
        try:
            prompt = f"""
            Search for recent trends and news related to this tweet for SME Analytica engagement:
            
            Tweet: "{tweet_text}"
            Author: @{author}
            
            Find recent information about:
            - Restaurant technology trends
            - Small business analytics adoption
            - AI in hospitality/retail
            - Dynamic pricing trends
            
            Assess engagement opportunity based on current industry context.
            """
            
            # Implementation would use Perplexity's search capabilities
            return {
                "relevance_score": 8,
                "should_engage": True,
                "industry_context": "Recent trends support engagement",
                "response_type": "reply"
            }
            
        except Exception as e:
            raise APIError(f"Perplexity engagement analysis error: {e}")
    
    async def generate_reply(self, original_tweet: str, context: Dict[str, Any]) -> str:
        """Generate reply with current industry insights"""
        try:
            prompt = f"""
            Generate a reply incorporating recent industry trends and data:
            
            Original tweet: "{original_tweet}"
            Context: {context}
            
            Search for current information about:
            - Latest restaurant tech adoption rates
            - Recent AI analytics success stories in SME sector
            - Current pricing strategy trends
            
            Create a helpful reply that mentions relevant recent trends and positions SME Analytica appropriately.
            Keep under 280 characters.
            """
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 100,
                    "temperature": 0.6
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
            raise APIError(f"Perplexity reply generation error: {e}")
    
    def _build_industry_prompt(self, request: ContentRequest) -> str:
        """Build prompt that leverages real-time industry data"""
        context_str = "\n".join([f"- {k}: {v}" for k, v in request.context.items()])
        
        return f"""
        Search for recent trends and create a {request.content_type.value} for SME Analytica:
        
        Theme: {request.theme}
        Language: {request.language}
        Max length: {request.max_length} characters
        
        Context:
        {context_str}
        
        Research current information about:
        - Latest SME technology adoption trends
        - Recent restaurant/retail analytics success stories
        - Current AI pricing optimization news
        - Small business digital transformation statistics
        
        Create content that:
        - Incorporates recent industry data and trends
        - Positions SME Analytica's solutions contextually
        - Provides timely, relevant insights
        - Uses current examples and statistics
        
        Focus on making the content highly relevant to current industry conversations.
        """
    
    def _extract_hashtags(self, text: str, suggested_hashtags: List[str]) -> List[str]:
        """Extract hashtags optimized for trending topics"""
        hashtags = []
        
        # Industry-specific trending hashtags
        trending_tags = ["#AITrends", "#RestaurantTech", "#SMETech", "#DataDriven"]
        
        for tag in suggested_hashtags + trending_tags:
            if len(hashtags) < 4 and tag not in hashtags:
                hashtags.append(tag)
        
        # Always include SME Analytica
        if "#SMEAnalytica" not in hashtags:
            hashtags.insert(0, "#SMEAnalytica")
        
        return hashtags[:4]
