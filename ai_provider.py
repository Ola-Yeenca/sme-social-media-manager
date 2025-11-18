#!/usr/bin/env python3
"""
AI Provider Abstraction Layer for SME Social Media Manager
Manages multiple AI providers with automatic fallback chain
"""

from typing import Optional, List, Dict
from dataclasses import dataclass
from enum import Enum
import openai
import groq
from logger import get_logger

logger = get_logger(__name__)


class AIProviderType(Enum):
    """Supported AI provider types"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GROQ = "groq"


@dataclass
class AIResponse:
    """Response from AI provider"""
    content: str
    provider: AIProviderType
    tokens_used: int = 0
    model: str = ""


class AIProvider:
    """Base class for AI providers"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.provider_type = None

    def generate(self, prompt: str, system_context: str = "",
                 max_tokens: int = 100, temperature: float = 0.7) -> AIResponse:
        """Generate content using this AI provider"""
        raise NotImplementedError("Subclasses must implement generate()")


class OpenAIProvider(AIProvider):
    """OpenAI GPT provider"""

    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.provider_type = AIProviderType.OPENAI
        openai.api_key = api_key
        logger.info("OpenAI provider initialized")

    def generate(self, prompt: str, system_context: str = "",
                 max_tokens: int = 100, temperature: float = 0.7) -> AIResponse:
        """Generate content using OpenAI GPT"""
        try:
            logger.debug(f"Calling OpenAI with prompt: {prompt[:50]}...")

            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_context},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )

            content = response.choices[0].message.content.strip()
            tokens = response.usage.total_tokens if hasattr(response, 'usage') else 0

            logger.info(f"OpenAI generated {len(content)} chars, {tokens} tokens")

            return AIResponse(
                content=content,
                provider=AIProviderType.OPENAI,
                tokens_used=tokens,
                model="gpt-3.5-turbo"
            )

        except Exception as e:
            logger.error(f"OpenAI generation failed: {e}")
            raise


class AnthropicProvider(AIProvider):
    """Anthropic Claude provider"""

    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.provider_type = AIProviderType.ANTHROPIC

        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=api_key)
            logger.info("Anthropic provider initialized")
        except ImportError:
            logger.error("Anthropic library not installed")
            raise

    def generate(self, prompt: str, system_context: str = "",
                 max_tokens: int = 100, temperature: float = 0.7) -> AIResponse:
        """Generate content using Anthropic Claude"""
        try:
            logger.debug(f"Calling Anthropic with prompt: {prompt[:50]}...")

            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_context,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text.strip()
            tokens = response.usage.input_tokens + response.usage.output_tokens if hasattr(response, 'usage') else 0

            logger.info(f"Anthropic generated {len(content)} chars, {tokens} tokens")

            return AIResponse(
                content=content,
                provider=AIProviderType.ANTHROPIC,
                tokens_used=tokens,
                model="claude-3-haiku-20240307"
            )

        except Exception as e:
            logger.error(f"Anthropic generation failed: {e}")
            raise


class GroqProvider(AIProvider):
    """Groq LLM provider"""

    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.provider_type = AIProviderType.GROQ
        self.client = groq.Groq(api_key=api_key)
        logger.info("Groq provider initialized")

    def generate(self, prompt: str, system_context: str = "",
                 max_tokens: int = 100, temperature: float = 0.7) -> AIResponse:
        """Generate content using Groq"""
        try:
            logger.debug(f"Calling Groq with prompt: {prompt[:50]}...")

            response = self.client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": system_context},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )

            content = response.choices[0].message.content.strip()
            tokens = response.usage.total_tokens if hasattr(response, 'usage') else 0

            logger.info(f"Groq generated {len(content)} chars, {tokens} tokens")

            return AIResponse(
                content=content,
                provider=AIProviderType.GROQ,
                tokens_used=tokens,
                model="llama3-8b-8192"
            )

        except Exception as e:
            logger.error(f"Groq generation failed: {e}")
            raise


class AIProviderChain:
    """
    Manages AI provider fallback chain with automatic failover

    Example:
        >>> chain = AIProviderChain(config)
        >>> response = chain.generate("Write a tweet about AI")
        >>> print(response.content)
        "AI is transforming business analytics..."
    """

    def __init__(self, config):
        """
        Initialize AI provider chain from config

        Args:
            config: Config object with API keys
        """
        self.config = config
        self.providers: List[AIProvider] = []
        self.current_provider_index = 0
        self._initialize_providers()

    def _initialize_providers(self):
        """Initialize all available AI providers in fallback order"""
        logger.info("Initializing AI provider chain...")

        # Try OpenAI first (primary)
        if self.config.openai_api_key:
            try:
                provider = OpenAIProvider(self.config.openai_api_key)
                self.providers.append(provider)
                logger.info("✅ OpenAI added to provider chain (primary)")
            except Exception as e:
                logger.warning(f"⚠️ OpenAI initialization failed: {e}")

        # Try Anthropic as fallback 1
        if self.config.anthropic_api_key:
            try:
                provider = AnthropicProvider(self.config.anthropic_api_key)
                self.providers.append(provider)
                logger.info("✅ Anthropic added to provider chain (fallback 1)")
            except Exception as e:
                logger.warning(f"⚠️ Anthropic initialization failed: {e}")

        # Try Groq as fallback 2
        if self.config.grok_api_key:
            try:
                provider = GroqProvider(self.config.grok_api_key)
                self.providers.append(provider)
                logger.info("✅ Groq added to provider chain (fallback 2)")
            except Exception as e:
                logger.warning(f"⚠️ Groq initialization failed: {e}")

        if not self.providers:
            logger.critical("❌ No AI providers available - cannot generate content")
            raise Exception("No AI providers configured")

        logger.info(f"✅ AI provider chain initialized with {len(self.providers)} providers")

    def generate(self, prompt: str, system_context: str = "",
                 max_tokens: int = 100, temperature: float = 0.7) -> AIResponse:
        """
        Generate content with automatic provider fallback

        Args:
            prompt: The user prompt
            system_context: System context/instructions
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0-1.0)

        Returns:
            AIResponse with generated content

        Raises:
            Exception: If all providers fail
        """
        last_error = None

        for i, provider in enumerate(self.providers):
            try:
                logger.info(f"Attempting generation with {provider.provider_type.value}...")
                response = provider.generate(prompt, system_context, max_tokens, temperature)

                # Ensure content is under 280 characters for tweets
                if len(response.content) > 280:
                    logger.warning(f"Content too long ({len(response.content)} chars), truncating...")
                    response.content = response.content[:277] + "..."

                logger.info(f"✅ Successfully generated content with {provider.provider_type.value}")
                self.current_provider_index = i  # Remember successful provider
                return response

            except Exception as e:
                last_error = e
                logger.warning(
                    f"⚠️ {provider.provider_type.value} failed: {str(e)[:100]}"
                )

                # Try next provider
                if i < len(self.providers) - 1:
                    next_provider = self.providers[i + 1]
                    logger.info(f"→ Falling back to {next_provider.provider_type.value}...")
                continue

        # All providers failed
        logger.error(f"❌ All {len(self.providers)} AI providers failed")
        raise Exception(f"All AI providers failed. Last error: {last_error}")

    def get_current_provider(self) -> Optional[AIProviderType]:
        """Get currently active provider type"""
        if self.providers and self.current_provider_index < len(self.providers):
            return self.providers[self.current_provider_index].provider_type
        return None

    def get_provider_stats(self) -> Dict[str, int]:
        """Get statistics about provider usage"""
        return {
            "total_providers": len(self.providers),
            "current_provider_index": self.current_provider_index,
            "current_provider": self.get_current_provider().value if self.get_current_provider() else None
        }


# Example usage and testing
if __name__ == "__main__":
    from config import Config

    # Test with config
    config = Config()
    chain = AIProviderChain(config)

    print("\n" + "=" * 60)
    print("AI PROVIDER CHAIN TEST")
    print("=" * 60)

    # Test generation
    try:
        response = chain.generate(
            prompt="Write a short tweet about restaurant analytics in under 200 characters",
            system_context="You are a social media manager for a restaurant analytics company"
        )

        print(f"\n✅ Generated content:")
        print(f"   Provider: {response.provider.value}")
        print(f"   Model: {response.model}")
        print(f"   Tokens: {response.tokens_used}")
        print(f"   Content: {response.content}")

    except Exception as e:
        print(f"\n❌ Generation failed: {e}")

    # Print stats
    stats = chain.get_provider_stats()
    print(f"\n📊 Provider Stats:")
    for key, value in stats.items():
        print(f"   {key}: {value}")
