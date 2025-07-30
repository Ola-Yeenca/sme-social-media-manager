#!/usr/bin/env python3
"""
AI Response Generator for SME Analytica
Advanced response generation using Anthropic/Claude with brand voice consistency
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import json
import re

from ..ai_providers import AIProviderManager, ContentRequest, ContentType

class ResponseType(str, Enum):
    HELPFUL_EXPERT = "helpful_expert"
    THOUGHT_LEADERSHIP = "thought_leadership"
    COMMUNITY_SUPPORT = "community_support"
    PROSPECT_ENGAGEMENT = "prospect_engagement"
    TREND_COMMENTARY = "trend_commentary"
    COMPETITIVE_RESPONSE = "competitive_response"

@dataclass
class ResponseContext:
    """Context for AI response generation"""
    content: str
    author: str
    author_profile: Dict[str, Any]
    conversation_thread: List[Dict[str, Any]]
    opportunity_type: str
    industry_relevance: float
    conversion_potential: float
    brand_alignment: float
    urgency: int
    competitive_context: Optional[str] = None
    trending_context: Optional[str] = None

@dataclass
class GeneratedResponse:
    """AI-generated response with metadata"""
    content: str
    response_type: ResponseType
    confidence_score: float
    brand_voice_score: float
    safety_score: float
    reasoning: str
    alternative_responses: List[str]
    engagement_strategy: str

class IntelligentResponseGenerator:
    """Advanced AI response generator with brand voice consistency"""
    
    def __init__(self, ai_provider: AIProviderManager):
        self.ai_provider = ai_provider
        self.logger = logging.getLogger(__name__)
        
        # Brand voice configuration
        self.brand_voice = self._initialize_brand_voice()
        self.response_templates = self._initialize_response_templates()
        self.safety_guidelines = self._initialize_safety_guidelines()
        
        # Performance tracking
        self.generation_stats = {
            "responses_generated": 0,
            "high_confidence_responses": 0,
            "safety_blocks": 0,
            "brand_voice_scores": []
        }

    def _initialize_brand_voice(self) -> Dict[str, Any]:
        """Initialize SME Analytica brand voice guidelines"""
        return {
            "personality": {
                "core_traits": [
                    "Data-driven expert", "Helpful mentor", "Industry thought leader",
                    "Approachable professional", "Innovation advocate"
                ],
                "tone": "Professional yet approachable, confident but not arrogant",
                "voice": "Authoritative on analytics, supportive of restaurant owners"
            },
            "messaging_pillars": {
                "expertise": "Deep knowledge of restaurant analytics and optimization",
                "helpfulness": "Genuinely wants to help restaurant owners succeed",
                "innovation": "Passionate about AI and data-driven solutions",
                "community": "Values the restaurant and hospitality community",
                "results": "Focuses on measurable business outcomes"
            },
            "language_style": {
                "preferred_words": [
                    "analytics", "insights", "optimization", "data-driven", "efficiency",
                    "growth", "margins", "revenue", "performance", "intelligence"
                ],
                "avoid_words": [
                    "cheap", "basic", "simple", "easy money", "guaranteed",
                    "revolutionary", "game-changer", "disruption"
                ],
                "emoji_usage": "Strategic and professional (📊📈🚀💡🎯🤝💪🔥)",
                "hashtag_strategy": "Relevant industry tags, avoid hashtag spam"
            },
            "content_guidelines": {
                "always_include": [
                    "Specific data or statistics when relevant",
                    "Helpful insights or actionable advice",
                    "Reference to SME Analytica's experience with 500+ restaurants"
                ],
                "never_include": [
                    "Overly promotional language",
                    "Pushy sales tactics",
                    "Unsubstantiated claims",
                    "Generic responses"
                ]
            }
        }

    def _initialize_response_templates(self) -> Dict[ResponseType, Dict[str, Any]]:
        """Initialize response templates for different scenarios"""
        return {
            ResponseType.HELPFUL_EXPERT: {
                "intro_phrases": [
                    "Great question! In our experience with 500+ restaurants,",
                    "This resonates with many restaurant owners we work with.",
                    "Excellent point! We've seen similar challenges across the hospitality industry."
                ],
                "data_integration": [
                    "Our analytics show that {statistic}",
                    "We've documented {percentage}% improvement in {metric}",
                    "The data tells us that {insight}"
                ],
                "closing_phrases": [
                    "Happy to share more insights if helpful! 📊",
                    "Feel free to reach out if you'd like to discuss further! 🤝",
                    "Would love to share what we've learned! 💡"
                ]
            },
            ResponseType.THOUGHT_LEADERSHIP: {
                "intro_phrases": [
                    "This trend is exactly what we're seeing in restaurant analytics!",
                    "💯 This! Our research with SME restaurants shows",
                    "Spot on analysis! At SME Analytica, we've documented similar patterns."
                ],
                "authority_builders": [
                    "Our data from 500+ restaurants confirms",
                    "We've been tracking this trend for months",
                    "The analytics community has been discussing this"
                ],
                "future_focus": [
                    "The future is definitely data-driven! 🔥",
                    "This is just the beginning of the AI revolution in hospitality! 🚀",
                    "The opportunity for optimization is massive! 📈"
                ]
            },
            ResponseType.COMMUNITY_SUPPORT: {
                "community_praise": [
                    "The restaurant community is incredible!",
                    "Love seeing restaurant owners support each other!",
                    "This is why the hospitality community is so strong!"
                ],
                "support_offers": [
                    "We're always happy to share insights from our analytics work.",
                    "If analytics insights would be helpful for your situation, we're here to help.",
                    "Data can definitely help with challenges like this."
                ],
                "encouragement": [
                    "Keep pushing forward! 💪",
                    "Growth through collaboration! 🤝",
                    "The community has your back! 🚀"
                ]
            },
            ResponseType.PROSPECT_ENGAGEMENT: {
                "problem_acknowledgment": [
                    "This sounds like exactly the type of challenge MenuFlow helps solve!",
                    "We help restaurants tackle this exact issue!",
                    "Perfect timing! This is precisely what SME Analytica specializes in."
                ],
                "value_propositions": [
                    "Our analytics platform has helped similar establishments {result}",
                    "MenuFlow's dynamic pricing shows how AI can immediately boost profitability",
                    "We've documented {percentage}% improvement in similar situations"
                ],
                "soft_ctas": [
                    "Would be happy to show you how it works. DM us! 📩",
                    "Free consultation available if you'd like to explore solutions! 💡",
                    "Interested in learning more? 🎯"
                ]
            }
        }

    def _initialize_safety_guidelines(self) -> Dict[str, List[str]]:
        """Initialize safety guidelines for response generation"""
        return {
            "prohibited_content": [
                "Personal attacks or harassment",
                "Discriminatory language",
                "False or misleading claims",
                "Spam or overly promotional content",
                "Political or controversial topics"
            ],
            "required_checks": [
                "Factual accuracy of any statistics mentioned",
                "Appropriate tone for the context",
                "Compliance with brand voice guidelines",
                "No overpromising or guarantees"
            ],
            "escalation_triggers": [
                "Negative sentiment about SME Analytica",
                "Competitor mentions requiring careful response",
                "Complex technical questions requiring expert input",
                "Potential legal or compliance issues"
            ]
        }

    async def generate_response(self, context: ResponseContext) -> Optional[GeneratedResponse]:
        """Generate AI-powered response with brand voice consistency"""
        try:
            # Determine response type
            response_type = self._determine_response_type(context)
            
            # Build comprehensive prompt
            prompt = self._build_response_prompt(context, response_type)
            
            # Generate response using AI (Gemini preferred for intelligent responses)
            response_content = await self._generate_with_ai(prompt, "gemini")
            
            if not response_content:
                return None
            
            # Analyze response quality
            confidence_score = self._analyze_confidence(response_content, context)
            brand_voice_score = self._analyze_brand_voice(response_content)
            safety_score = self._analyze_safety(response_content)
            
            # Generate alternatives if needed
            alternatives = []
            if confidence_score < 8.0:
                alternatives = await self._generate_alternatives(context, response_type)
            
            # Determine engagement strategy
            engagement_strategy = self._determine_engagement_strategy(context, response_type)
            
            # Create response object
            generated_response = GeneratedResponse(
                content=response_content,
                response_type=response_type,
                confidence_score=confidence_score,
                brand_voice_score=brand_voice_score,
                safety_score=safety_score,
                reasoning=f"Generated {response_type.value} response for {context.opportunity_type}",
                alternative_responses=alternatives,
                engagement_strategy=engagement_strategy
            )
            
            # Update statistics
            self._update_generation_stats(generated_response)
            
            return generated_response
            
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return None

    def _determine_response_type(self, context: ResponseContext) -> ResponseType:
        """Determine the best response type for the context"""
        
        # High conversion potential -> prospect engagement
        if context.conversion_potential > 7.0:
            return ResponseType.PROSPECT_ENGAGEMENT
        
        # Industry thought leadership opportunities
        if context.industry_relevance > 8.0 and "?" not in context.content:
            return ResponseType.THOUGHT_LEADERSHIP
        
        # Community support for questions and help requests
        if "?" in context.content or any(word in context.content.lower() 
                                       for word in ['help', 'advice', 'struggling']):
            return ResponseType.COMMUNITY_SUPPORT
        
        # Trending topics
        if context.trending_context:
            return ResponseType.TREND_COMMENTARY
        
        # Competitive context
        if context.competitive_context:
            return ResponseType.COMPETITIVE_RESPONSE
        
        # Default to helpful expert
        return ResponseType.HELPFUL_EXPERT

    def _build_response_prompt(self, context: ResponseContext, response_type: ResponseType) -> str:
        """Build comprehensive prompt for AI response generation"""
        
        # Get response template
        template = self.response_templates.get(response_type, {})
        
        prompt = f"""
You are the AI social media agent for SME Analytica, an AI-driven analytics platform for restaurants, hotels, and retail businesses.

BRAND IDENTITY:
{json.dumps(self.brand_voice, indent=2)}

RESPONSE TYPE: {response_type.value}

CONTEXT:
- Original Content: "{context.content}"
- Author: {context.author}
- Author Profile: {json.dumps(context.author_profile, indent=2)}
- Opportunity Type: {context.opportunity_type}
- Industry Relevance: {context.industry_relevance}/10
- Conversion Potential: {context.conversion_potential}/10
- Urgency: {context.urgency}/10

CONVERSATION THREAD:
{self._format_conversation_thread(context.conversation_thread)}

RESPONSE GUIDELINES FOR {response_type.value.upper()}:
{json.dumps(template, indent=2)}

REQUIREMENTS:
1. Stay true to SME Analytica's brand voice and personality
2. Provide genuine value and insights
3. Use specific data/statistics when relevant (e.g., "10% margin improvement")
4. Keep under 280 characters for Twitter
5. Include strategic emoji usage (📊📈🚀💡🎯🤝💪🔥)
6. Be helpful first, promotional second
7. Reference our experience with 500+ restaurants when appropriate

SAFETY CHECKS:
- No overly promotional language
- No unsubstantiated claims
- No pushy sales tactics
- Maintain professional tone

Generate a response that embodies SME Analytica's expertise while providing genuine value to the conversation.
"""
        
        return prompt.strip()

    async def _generate_with_ai(self, prompt: str, preferred_provider: str = "gemini") -> Optional[str]:
        """Generate response using preferred AI provider (Gemini by default)"""
        try:
            content_request = ContentRequest(
                content_type=ContentType.SOCIAL_MEDIA_RESPONSE,
                platform="twitter",
                context=prompt,
                max_length=280,
                tone="professional_helpful"
            )

            # Try preferred provider first (Gemini for intelligent responses)
            if preferred_provider == "gemini" and hasattr(self.ai_provider, 'providers') and "gemini" in self.ai_provider.providers:
                try:
                    gemini_provider = self.ai_provider.providers["gemini"]
                    if gemini_provider.is_available:
                        response = await gemini_provider.generate_reply(prompt, {})
                        return response
                except Exception as e:
                    self.logger.warning(f"Gemini generation failed, falling back: {e}")

            # Fallback to provider manager
            response = await self.ai_provider.generate_content(
                content_request,
                provider=preferred_provider if preferred_provider != "gemini" else "anthropic"
            )

            return response

        except Exception as e:
            self.logger.error(f"Error generating with AI: {e}")
            return None

    def _format_conversation_thread(self, thread: List[Dict[str, Any]]) -> str:
        """Format conversation thread for AI context"""
        if not thread:
            return "No previous conversation context."
        
        formatted = []
        for tweet in thread[-3:]:  # Last 3 tweets for context
            author = tweet.get('author', 'Unknown')
            content = tweet.get('text', '')
            formatted.append(f"@{author}: {content}")
        
        return "\n".join(formatted)

    def _analyze_confidence(self, response: str, context: ResponseContext) -> float:
        """Analyze confidence in response quality"""
        score = 7.0  # Base confidence
        
        # Length check
        if len(response) < 20:
            score -= 2.0
        elif len(response) > 280:
            score -= 1.0
        
        # Brand voice elements
        brand_words = self.brand_voice["language_style"]["preferred_words"]
        if any(word in response.lower() for word in brand_words):
            score += 1.0
        
        # Specific data mentions
        if any(pattern in response for pattern in ['%', 'restaurants', '500+', 'MenuFlow']):
            score += 1.0
        
        # Professional tone indicators
        helpful_phrases = ['happy to', 'feel free', 'would love', 'experience shows']
        if any(phrase in response.lower() for phrase in helpful_phrases):
            score += 0.5
        
        return min(score, 10.0)

    def _analyze_brand_voice(self, response: str) -> float:
        """Analyze brand voice alignment"""
        score = 7.0  # Good baseline
        
        # Check for brand voice elements
        preferred_words = self.brand_voice["language_style"]["preferred_words"]
        for word in preferred_words:
            if word in response.lower():
                score += 0.3
        
        # Check for avoided words
        avoid_words = self.brand_voice["language_style"]["avoid_words"]
        for word in avoid_words:
            if word in response.lower():
                score -= 1.0
        
        # Check for helpful tone
        if any(phrase in response.lower() for phrase in ['help', 'share', 'insights', 'experience']):
            score += 0.5
        
        # Check for data-driven language
        if any(word in response.lower() for word in ['data', 'analytics', 'metrics', 'performance']):
            score += 0.5
        
        return max(min(score, 10.0), 0.0)

    def _analyze_safety(self, response: str) -> float:
        """Analyze safety score of response"""
        score = 9.0  # High safety baseline
        
        # Check for promotional language
        promotional_words = ['buy now', 'limited time', 'act fast', 'exclusive offer', 'guaranteed']
        for word in promotional_words:
            if word in response.lower():
                score -= 2.0
        
        # Check for overpromising
        overpromise_words = ['guaranteed', 'promise', 'definitely will', 'always works']
        for word in overpromise_words:
            if word in response.lower():
                score -= 1.5
        
        return max(score, 0.0)

    async def _generate_alternatives(self, context: ResponseContext, 
                                   response_type: ResponseType) -> List[str]:
        """Generate alternative responses"""
        try:
            # Generate 2 alternative responses with slightly different prompts
            alternatives = []
            
            for i in range(2):
                alt_prompt = self._build_alternative_prompt(context, response_type, i)
                alt_response = await self._generate_with_ai(alt_prompt, "gemini")
                if alt_response:
                    alternatives.append(alt_response)
            
            return alternatives
            
        except Exception as e:
            self.logger.error(f"Error generating alternatives: {e}")
            return []

    def _build_alternative_prompt(self, context: ResponseContext, 
                                response_type: ResponseType, variant: int) -> str:
        """Build alternative prompt with slight variations"""
        base_prompt = self._build_response_prompt(context, response_type)
        
        variations = [
            "\n\nVARIATION: Focus more on community building and support.",
            "\n\nVARIATION: Emphasize data insights and specific statistics.",
            "\n\nVARIATION: Use a more conversational and approachable tone."
        ]
        
        return base_prompt + variations[variant % len(variations)]

    def _determine_engagement_strategy(self, context: ResponseContext, 
                                     response_type: ResponseType) -> str:
        """Determine engagement strategy for the response"""
        
        if context.conversion_potential > 7.0:
            return "conversion_focused"
        elif context.industry_relevance > 8.0:
            return "thought_leadership"
        elif "?" in context.content:
            return "community_support"
        else:
            return "brand_awareness"

    def _update_generation_stats(self, response: GeneratedResponse) -> None:
        """Update generation statistics"""
        self.generation_stats["responses_generated"] += 1
        
        if response.confidence_score >= 8.0:
            self.generation_stats["high_confidence_responses"] += 1
        
        if response.safety_score < 7.0:
            self.generation_stats["safety_blocks"] += 1
        
        self.generation_stats["brand_voice_scores"].append(response.brand_voice_score)

    def get_generation_stats(self) -> Dict[str, Any]:
        """Get response generation statistics"""
        avg_brand_voice = (
            sum(self.generation_stats["brand_voice_scores"]) / 
            max(len(self.generation_stats["brand_voice_scores"]), 1)
        )
        
        return {
            "responses_generated": self.generation_stats["responses_generated"],
            "high_confidence_responses": self.generation_stats["high_confidence_responses"],
            "safety_blocks": self.generation_stats["safety_blocks"],
            "average_brand_voice_score": round(avg_brand_voice, 2),
            "confidence_rate": (
                self.generation_stats["high_confidence_responses"] / 
                max(self.generation_stats["responses_generated"], 1) * 100
            )
        }
