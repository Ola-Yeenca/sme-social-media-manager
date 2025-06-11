"""
AI Provider Manager - orchestrates multiple AI providers for optimal content generation
"""

import asyncio
import random
from typing import Dict, List, Optional, Any
from enum import Enum
from .base import BaseAIProvider, ContentRequest, GeneratedContent, AIProviderError
from .openai_provider import OpenAIProvider
from .anthropic_provider import AnthropicProvider
from .perplexity_provider import PerplexityProvider
from .grok_provider import GrokProvider, MockGrokProvider

class ProviderStrategy(str, Enum):
    ROUND_ROBIN = "round_robin"
    BEST_FOR_CONTENT = "best_for_content"
    FALLBACK_CHAIN = "fallback_chain"
    RANDOM = "random"

class AIProviderManager:
    """Manages multiple AI providers with intelligent routing and fallback"""
    
    def __init__(self, config: Dict[str, str]):
        self.providers: Dict[str, BaseAIProvider] = {}
        self.provider_order = []
        self.current_provider_index = 0
        
        # Initialize providers based on available API keys
        self._initialize_providers(config)
        
        # Content type to provider mapping
        self.content_preferences = {
            "analytical": ["anthropic", "openai", "perplexity"],
            "creative": ["openai", "grok", "anthropic"],
            "trending": ["grok", "perplexity", "openai"],
            "industry_insight": ["perplexity", "anthropic", "openai"],
            "engagement": ["grok", "openai", "anthropic"]
        }
    
    def _initialize_providers(self, config: Dict[str, str]):
        """Initialize AI providers based on available configuration"""
        
        # OpenAI (primary for creative content)
        if config.get("openai_api_key"):
            self.providers["openai"] = OpenAIProvider(config["openai_api_key"])
            self.provider_order.append("openai")
        
        # Anthropic (primary for analytical content)
        if config.get("anthropic_api_key"):
            self.providers["anthropic"] = AnthropicProvider(config["anthropic_api_key"])
            self.provider_order.append("anthropic")
        
        # Perplexity (for industry insights)
        if config.get("perplexity_api_key"):
            self.providers["perplexity"] = PerplexityProvider(config["perplexity_api_key"])
            self.provider_order.append("perplexity")
        
        # Grok or Mock Grok
        if config.get("grok_api_key"):
            self.providers["grok"] = GrokProvider(config["grok_api_key"])
            self.provider_order.append("grok")
        else:
            # Use mock provider as fallback
            self.providers["grok"] = MockGrokProvider()
            self.provider_order.append("grok")
    
    async def generate_content(self, request: ContentRequest, strategy: ProviderStrategy = ProviderStrategy.BEST_FOR_CONTENT) -> GeneratedContent:
        """Generate content using specified strategy"""
        
        if strategy == ProviderStrategy.BEST_FOR_CONTENT:
            return await self._generate_with_best_provider(request)
        elif strategy == ProviderStrategy.FALLBACK_CHAIN:
            return await self._generate_with_fallback(request)
        elif strategy == ProviderStrategy.ROUND_ROBIN:
            return await self._generate_round_robin(request)
        elif strategy == ProviderStrategy.RANDOM:
            return await self._generate_random(request)
        else:
            return await self._generate_with_fallback(request)
    
    async def _generate_with_best_provider(self, request: ContentRequest) -> GeneratedContent:
        """Choose the best provider based on content type and theme"""
        
        # Determine content category
        content_category = self._categorize_content(request)
        preferred_providers = self.content_preferences.get(content_category, self.provider_order)
        
        # Try providers in preference order
        for provider_name in preferred_providers:
            if provider_name in self.providers and self.providers[provider_name].is_available:
                try:
                    return await self.providers[provider_name].generate_content(request)
                except AIProviderError as e:
                    print(f"Provider {provider_name} failed: {e}")
                    continue
        
        raise AIProviderError("All preferred providers failed")
    
    async def _generate_with_fallback(self, request: ContentRequest) -> GeneratedContent:
        """Try providers in order until one succeeds"""
        
        for provider_name in self.provider_order:
            provider = self.providers.get(provider_name)
            if provider and provider.is_available:
                try:
                    return await provider.generate_content(request)
                except AIProviderError as e:
                    print(f"Provider {provider_name} failed, trying next: {e}")
                    continue
        
        raise AIProviderError("All providers failed")
    
    async def _generate_round_robin(self, request: ContentRequest) -> GeneratedContent:
        """Use providers in round-robin fashion"""
        
        if not self.provider_order:
            raise AIProviderError("No providers available")
        
        provider_name = self.provider_order[self.current_provider_index]
        self.current_provider_index = (self.current_provider_index + 1) % len(self.provider_order)
        
        provider = self.providers[provider_name]
        if provider.is_available:
            try:
                return await provider.generate_content(request)
            except AIProviderError:
                # Fallback to next available provider
                return await self._generate_with_fallback(request)
        else:
            return await self._generate_with_fallback(request)
    
    async def _generate_random(self, request: ContentRequest) -> GeneratedContent:
        """Choose a random available provider"""
        
        available_providers = [name for name in self.provider_order 
                             if self.providers[name].is_available]
        
        if not available_providers:
            raise AIProviderError("No providers available")
        
        provider_name = random.choice(available_providers)
        return await self.providers[provider_name].generate_content(request)
    
    def _categorize_content(self, request: ContentRequest) -> str:
        """Categorize content to choose the best provider"""
        
        theme_lower = request.theme.lower()
        context_str = str(request.context).lower()
        
        # Analytical content
        if any(word in theme_lower for word in ['data', 'analytics', 'insight', 'metric']):
            return "analytical"
        
        # Trending/viral content
        if any(word in theme_lower for word in ['trending', 'viral', 'engagement', 'fun']):
            return "trending"
        
        # Industry insights
        if any(word in theme_lower for word in ['industry', 'news', 'trend', 'market']):
            return "industry_insight"
        
        # Creative content
        if any(word in theme_lower for word in ['creative', 'story', 'case', 'example']):
            return "creative"
        
        # Default to creative for general content
        return "creative"
    
    async def analyze_engagement_opportunity(self, tweet_text: str, author: str) -> Dict[str, Any]:
        """Analyze engagement opportunity using multiple providers"""
        
        analyses = {}
        
        # Get analysis from available providers
        for provider_name, provider in self.providers.items():
            if provider.is_available:
                try:
                    analysis = await provider.analyze_engagement_opportunity(tweet_text, author)
                    analyses[provider_name] = analysis
                except AIProviderError as e:
                    print(f"Engagement analysis failed for {provider_name}: {e}")
        
        # Aggregate results
        return self._aggregate_engagement_analysis(analyses)
    
    def _aggregate_engagement_analysis(self, analyses: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate engagement analyses from multiple providers"""
        
        if not analyses:
            return {"should_engage": False, "confidence": 0}
        
        # Simple aggregation logic
        total_relevance = sum(analysis.get("relevance_score", 0) for analysis in analyses.values())
        avg_relevance = total_relevance / len(analyses)
        
        engage_votes = sum(1 for analysis in analyses.values() if analysis.get("should_engage", False))
        should_engage = engage_votes > len(analyses) / 2
        
        return {
            "should_engage": should_engage,
            "relevance_score": avg_relevance,
            "confidence": len(analyses) / len(self.providers),
            "provider_analyses": analyses
        }
    
    async def generate_reply(self, original_tweet: str, context: Dict[str, Any], preferred_provider: Optional[str] = None) -> str:
        """Generate reply using specified or best available provider"""
        
        if preferred_provider and preferred_provider in self.providers:
            provider = self.providers[preferred_provider]
            if provider.is_available:
                try:
                    return await provider.generate_reply(original_tweet, context)
                except AIProviderError:
                    pass  # Fall through to default selection
        
        # Use best provider for engagement
        for provider_name in self.content_preferences["engagement"]:
            if provider_name in self.providers and self.providers[provider_name].is_available:
                try:
                    return await self.providers[provider_name].generate_reply(original_tweet, context)
                except AIProviderError as e:
                    print(f"Reply generation failed for {provider_name}: {e}")
                    continue
        
        raise AIProviderError("All providers failed to generate reply")
    
    def get_provider_status(self) -> Dict[str, Dict[str, Any]]:
        """Get status of all providers"""
        
        status = {}
        for name, provider in self.providers.items():
            status[name] = {
                "available": provider.is_available,
                "provider_name": provider.provider_name,
                "model_name": provider.model_name
            }
        
        return status
    
    async def test_providers(self) -> Dict[str, bool]:
        """Test all providers with a simple request"""
        
        test_request = ContentRequest(
            content_type="tweet",
            language="en",
            theme="test",
            context={"test": "provider connectivity"},
            max_length=100
        )
        
        results = {}
        for name, provider in self.providers.items():
            try:
                await provider.generate_content(test_request)
                results[name] = True
            except Exception as e:
                print(f"Provider {name} test failed: {e}")
                results[name] = False
        
        return results
