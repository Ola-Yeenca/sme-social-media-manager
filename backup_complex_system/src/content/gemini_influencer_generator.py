#!/usr/bin/env python3
"""
Gemini-Powered Influencer Content Generator for SME Analytica
Creates intelligent, viral-optimized content that positions SME Analytica as a thought leader
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

from ..ai_providers import AIProviderManager, ContentRequest, ContentType
from config.settings import sme_context

class InfluencerContentType(str, Enum):
    THOUGHT_LEADERSHIP = "thought_leadership"
    DATA_INSIGHTS = "data_insights"
    INDUSTRY_TRENDS = "industry_trends"
    SUCCESS_STORIES = "success_stories"
    BEHIND_SCENES = "behind_scenes"
    VIRAL_HOOKS = "viral_hooks"
    EDUCATIONAL = "educational"
    CONTROVERSIAL_TAKES = "controversial_takes"

class ViralityFactor(str, Enum):
    SHOCKING_STATISTICS = "shocking_statistics"
    CONTRARIAN_VIEWS = "contrarian_views"
    INSIDER_SECRETS = "insider_secrets"
    FUTURE_PREDICTIONS = "future_predictions"
    MYTH_BUSTING = "myth_busting"
    PERSONAL_STORIES = "personal_stories"
    INDUSTRY_DRAMA = "industry_drama"
    ACTIONABLE_TIPS = "actionable_tips"

@dataclass
class InfluencerContent:
    """Influencer-optimized content with viral potential"""
    content: str
    content_type: InfluencerContentType
    virality_factors: List[ViralityFactor]
    engagement_hooks: List[str]
    hashtags: List[str]
    optimal_posting_time: str
    target_audience: List[str]
    expected_engagement_rate: float
    viral_potential_score: float
    brand_authority_score: float

class GeminiInfluencerGenerator:
    """Gemini-powered content generator for social media influence"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize AI provider with Gemini focus
        import os
        ai_config = {
            "google_gemini_api_key": os.getenv("GOOGLE_GEMINI_API_KEY"),
            "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
            "openai_api_key": os.getenv("OPENAI_API_KEY")
        }
        self.ai_provider = AIProviderManager(ai_config)
        
        # Influencer content strategies
        self.content_strategies = self._initialize_content_strategies()
        self.viral_templates = self._initialize_viral_templates()
        self.engagement_hooks = self._initialize_engagement_hooks()

    def _initialize_content_strategies(self) -> Dict[InfluencerContentType, Dict[str, Any]]:
        """Initialize content strategies for different influencer content types"""
        return {
            InfluencerContentType.THOUGHT_LEADERSHIP: {
                "approach": "Establish authority through data-driven insights",
                "tone": "Confident, analytical, forward-thinking",
                "structure": "Bold statement → Supporting data → Industry implication → Call to action",
                "viral_factors": [ViralityFactor.SHOCKING_STATISTICS, ViralityFactor.FUTURE_PREDICTIONS],
                "engagement_rate": 0.08
            },
            InfluencerContentType.DATA_INSIGHTS: {
                "approach": "Share exclusive analytics and hidden patterns",
                "tone": "Authoritative, revealing, data-focused",
                "structure": "Surprising finding → Data visualization → Business impact → Actionable insight",
                "viral_factors": [ViralityFactor.INSIDER_SECRETS, ViralityFactor.SHOCKING_STATISTICS],
                "engagement_rate": 0.12
            },
            InfluencerContentType.INDUSTRY_TRENDS: {
                "approach": "Predict and analyze emerging restaurant tech trends",
                "tone": "Visionary, analytical, trend-setting",
                "structure": "Trend observation → Market analysis → SME impact → Future prediction",
                "viral_factors": [ViralityFactor.FUTURE_PREDICTIONS, ViralityFactor.CONTRARIAN_VIEWS],
                "engagement_rate": 0.10
            },
            InfluencerContentType.SUCCESS_STORIES: {
                "approach": "Share specific client wins with measurable results",
                "tone": "Celebratory, results-focused, inspiring",
                "structure": "Client challenge → SME solution → Measurable results → Broader lesson",
                "viral_factors": [ViralityFactor.PERSONAL_STORIES, ViralityFactor.ACTIONABLE_TIPS],
                "engagement_rate": 0.15
            },
            InfluencerContentType.BEHIND_SCENES: {
                "approach": "Show the human side of AI and analytics",
                "tone": "Authentic, relatable, educational",
                "structure": "Behind-scenes moment → Technical insight → Human element → Community connection",
                "viral_factors": [ViralityFactor.INSIDER_SECRETS, ViralityFactor.PERSONAL_STORIES],
                "engagement_rate": 0.18
            },
            InfluencerContentType.VIRAL_HOOKS: {
                "approach": "Create shareable content with strong hooks",
                "tone": "Attention-grabbing, provocative, memorable",
                "structure": "Hook → Surprise element → Value delivery → Share trigger",
                "viral_factors": [ViralityFactor.SHOCKING_STATISTICS, ViralityFactor.MYTH_BUSTING],
                "engagement_rate": 0.25
            },
            InfluencerContentType.EDUCATIONAL: {
                "approach": "Teach restaurant owners valuable business concepts",
                "tone": "Educational, helpful, expert",
                "structure": "Problem identification → Solution explanation → Step-by-step guide → Results",
                "viral_factors": [ViralityFactor.ACTIONABLE_TIPS, ViralityFactor.MYTH_BUSTING],
                "engagement_rate": 0.14
            },
            InfluencerContentType.CONTROVERSIAL_TAKES: {
                "approach": "Challenge industry assumptions with data",
                "tone": "Bold, contrarian, evidence-based",
                "structure": "Controversial statement → Supporting evidence → Industry challenge → New perspective",
                "viral_factors": [ViralityFactor.CONTRARIAN_VIEWS, ViralityFactor.INDUSTRY_DRAMA],
                "engagement_rate": 0.20
            }
        }

    def _initialize_viral_templates(self) -> Dict[ViralityFactor, List[str]]:
        """Initialize viral content templates"""
        return {
            ViralityFactor.SHOCKING_STATISTICS: [
                "🚨 SHOCKING: {statistic} of restaurants are losing ${amount} monthly because they don't track {metric}",
                "📊 Data that will blow your mind: {finding} (and why it matters for your restaurant)",
                "💰 The ${amount} mistake 90% of restaurant owners make (backed by data from 500+ establishments)"
            ],
            ViralityFactor.CONTRARIAN_VIEWS: [
                "🔥 Unpopular opinion: {controversial_statement} (here's why the data proves me right)",
                "❌ Everyone says {common_belief}. Our analytics show the opposite is true.",
                "🎯 Hot take: {industry_assumption} is killing restaurant profits. Here's what actually works:"
            ],
            ViralityFactor.INSIDER_SECRETS: [
                "🤫 Restaurant industry secret: {secret_insight} (most owners don't know this)",
                "💡 What we learned analyzing 500+ restaurants: {insider_finding}",
                "🔍 Behind the scenes: How top-performing restaurants really {action}"
            ],
            ViralityFactor.FUTURE_PREDICTIONS: [
                "🔮 Prediction: By 2025, restaurants that don't {action} will lose {percentage}% of their market share",
                "📈 The future of restaurants: {trend_prediction} (and how to prepare now)",
                "⚡ Coming soon to restaurants: {technology_prediction} will change everything"
            ],
            ViralityFactor.MYTH_BUSTING: [
                "❌ MYTH: {common_myth} ✅ REALITY: {actual_truth} (data from 500+ restaurants)",
                "🚫 Stop believing this restaurant myth: {myth}. Here's what actually drives {outcome}:",
                "💥 Busted: {industry_myth}. Our analytics reveal the truth:"
            ]
        }

    def _initialize_engagement_hooks(self) -> List[str]:
        """Initialize engagement hooks for viral content"""
        return [
            "What's your experience with this?",
            "Agree or disagree? Let me know below 👇",
            "Which restaurant owner needs to see this?",
            "Tag a restaurant owner who should know this",
            "What would you add to this list?",
            "Share if this helped you!",
            "Thoughts? Drop them below 💭",
            "Who else is seeing this trend?",
            "What's your biggest challenge with this?",
            "Save this for later and share with your team!"
        ]

    async def generate_influencer_content(self, content_type: InfluencerContentType, 
                                        context: Dict[str, Any] = None) -> InfluencerContent:
        """Generate influencer-optimized content using Gemini"""
        
        try:
            strategy = self.content_strategies[content_type]
            
            # Build Gemini prompt for influencer content
            prompt = self._build_influencer_prompt(content_type, strategy, context or {})
            
            # Generate content using Gemini
            if "gemini" in self.ai_provider.providers:
                gemini_provider = self.ai_provider.providers["gemini"]
                if hasattr(gemini_provider, 'generate_influencer_content'):
                    content_request = ContentRequest(
                        content_type=ContentType.SOCIAL_MEDIA_POST,
                        platform="twitter",
                        theme=content_type.value,
                        context=context or {},
                        max_length=280,
                        tone=strategy["tone"]
                    )
                    generated = await gemini_provider.generate_influencer_content(content_request)
                    content_text = generated.text
                else:
                    # Fallback to regular generation
                    content_text = await self._generate_with_fallback(prompt)
            else:
                content_text = await self._generate_with_fallback(prompt)
            
            # Analyze viral potential
            viral_potential = self._calculate_viral_potential(content_text, strategy)
            brand_authority = self._calculate_brand_authority(content_text)
            
            # Extract engagement hooks
            hooks = self._extract_engagement_hooks(content_text)
            
            # Generate optimal hashtags
            hashtags = self._generate_optimal_hashtags(content_type, content_text)
            
            return InfluencerContent(
                content=content_text,
                content_type=content_type,
                virality_factors=strategy["viral_factors"],
                engagement_hooks=hooks,
                hashtags=hashtags,
                optimal_posting_time=self._determine_optimal_timing(content_type),
                target_audience=self._identify_target_audience(content_type),
                expected_engagement_rate=strategy["engagement_rate"],
                viral_potential_score=viral_potential,
                brand_authority_score=brand_authority
            )
            
        except Exception as e:
            self.logger.error(f"Error generating influencer content: {e}")
            raise

    def _build_influencer_prompt(self, content_type: InfluencerContentType, 
                               strategy: Dict[str, Any], context: Dict[str, Any]) -> str:
        """Build specialized prompt for influencer content generation"""
        
        viral_templates = [template for factor in strategy["viral_factors"] 
                          for template in self.viral_templates.get(factor, [])]
        
        prompt = f"""
        You are SME Analytica's AI social media strategist, creating viral influencer content that positions us as the #1 thought leader in restaurant analytics.
        
        MISSION: Create content that restaurant owners can't ignore, want to share, and positions SME Analytica as the authoritative voice they trust.
        
        Content Type: {content_type.value}
        Strategy: {strategy["approach"]}
        Tone: {strategy["tone"]}
        Structure: {strategy["structure"]}
        
        SME Analytica Authority Builders:
        - 500+ restaurants trust our analytics platform
        - MenuFlow dynamic pricing: Proven 10% margin improvement
        - Real-time analytics + seamless POS integration
        - Making enterprise-level BI accessible to SMEs
        - Industry-leading AI-powered optimization
        
        Viral Content Requirements:
        - Start with an attention-grabbing hook
        - Include specific, shocking statistics
        - Share insider insights only we would know
        - End with engagement-driving questions
        - Use power words: "revealed", "discovered", "proven", "secret"
        - Include measurable results and percentages
        - Create FOMO (fear of missing out)
        - Make it shareable and quotable
        
        Viral Templates to Consider:
        {chr(10).join(viral_templates[:3])}
        
        Context: {context}
        
        Create content that will:
        1. Stop restaurant owners mid-scroll
        2. Make them think "I need to know more"
        3. Position SME Analytica as the expert they trust
        4. Drive massive engagement and shares
        5. Generate leads and demo requests
        
        Maximum 280 characters. Make every word count for maximum viral impact.
        """
        
        return prompt.strip()

    async def _generate_with_fallback(self, prompt: str) -> str:
        """Generate content with fallback providers"""
        try:
            content_request = ContentRequest(
                content_type=ContentType.SOCIAL_MEDIA_POST,
                platform="twitter",
                context={"prompt": prompt},
                max_length=280,
                tone="influential"
            )
            
            generated = await self.ai_provider.generate_content(content_request)
            return generated.text if hasattr(generated, 'text') else str(generated)
            
        except Exception as e:
            self.logger.error(f"Content generation failed: {e}")
            return "🚀 SME Analytica: Transforming restaurants with AI-powered analytics. 500+ establishments trust our data-driven insights for 10% margin improvements. #RestaurantTech #DataDriven"

    def _calculate_viral_potential(self, content: str, strategy: Dict[str, Any]) -> float:
        """Calculate viral potential score (0-10)"""
        score = 5.0  # Base score
        
        # Check for viral elements
        viral_indicators = [
            "🚨", "💰", "📊", "🔥", "❌", "✅", "🤫", "💡", "🔮", "📈", "⚡", "💥"
        ]
        for indicator in viral_indicators:
            if indicator in content:
                score += 0.5
        
        # Check for numbers and statistics
        import re
        if re.search(r'\d+%', content):
            score += 1.0
        if re.search(r'\$\d+', content):
            score += 1.0
        
        # Check for engagement triggers
        engagement_words = ["shocking", "secret", "revealed", "proven", "discovered"]
        for word in engagement_words:
            if word.lower() in content.lower():
                score += 0.5
        
        # Strategy-based multiplier
        base_engagement = strategy.get("engagement_rate", 0.1)
        score *= (1 + base_engagement)
        
        return min(score, 10.0)

    def _calculate_brand_authority(self, content: str) -> float:
        """Calculate brand authority score (0-10)"""
        score = 6.0  # Good baseline
        
        # Authority indicators
        authority_words = ["analytics", "data", "proven", "500+", "restaurants", "insights"]
        for word in authority_words:
            if word.lower() in content.lower():
                score += 0.3
        
        # SME Analytica mentions
        if "sme analytica" in content.lower() or "menuflow" in content.lower():
            score += 1.0
        
        # Specific results
        if "10%" in content or "margin" in content.lower():
            score += 0.5
        
        return min(score, 10.0)

    def _extract_engagement_hooks(self, content: str) -> List[str]:
        """Extract engagement hooks from content"""
        hooks = []
        
        if "?" in content:
            hooks.append("question_based")
        
        if any(word in content.lower() for word in ["agree", "disagree", "thoughts"]):
            hooks.append("opinion_seeking")
        
        if any(word in content.lower() for word in ["share", "tag", "save"]):
            hooks.append("action_trigger")
        
        return hooks

    def _generate_optimal_hashtags(self, content_type: InfluencerContentType, content: str) -> List[str]:
        """Generate optimal hashtags for viral reach"""
        
        base_hashtags = ["#RestaurantAnalytics", "#SMEAnalytics", "#RestaurantTech"]
        
        type_specific = {
            InfluencerContentType.THOUGHT_LEADERSHIP: ["#ThoughtLeadership", "#BusinessIntelligence"],
            InfluencerContentType.DATA_INSIGHTS: ["#DataDriven", "#Analytics"],
            InfluencerContentType.INDUSTRY_TRENDS: ["#RestaurantTrends", "#FoodTech"],
            InfluencerContentType.SUCCESS_STORIES: ["#SuccessStory", "#RestaurantGrowth"],
            InfluencerContentType.BEHIND_SCENES: ["#BehindTheScenes", "#TechLife"],
            InfluencerContentType.VIRAL_HOOKS: ["#RestaurantOwner", "#SmallBusiness"],
            InfluencerContentType.EDUCATIONAL: ["#RestaurantTips", "#BusinessGrowth"],
            InfluencerContentType.CONTROVERSIAL_TAKES: ["#HotTake", "#RestaurantReality"]
        }
        
        hashtags = base_hashtags + type_specific.get(content_type, [])
        return hashtags[:5]  # Limit to 5 for optimal engagement

    def _determine_optimal_timing(self, content_type: InfluencerContentType) -> str:
        """Determine optimal posting time for content type"""
        
        timing_map = {
            InfluencerContentType.THOUGHT_LEADERSHIP: "9:00 AM EST (business hours)",
            InfluencerContentType.DATA_INSIGHTS: "10:00 AM EST (peak business engagement)",
            InfluencerContentType.INDUSTRY_TRENDS: "2:00 PM EST (afternoon engagement)",
            InfluencerContentType.SUCCESS_STORIES: "11:00 AM EST (mid-morning inspiration)",
            InfluencerContentType.BEHIND_SCENES: "7:00 PM EST (evening casual browsing)",
            InfluencerContentType.VIRAL_HOOKS: "8:00 PM EST (peak viral hours)",
            InfluencerContentType.EDUCATIONAL: "12:00 PM EST (lunch break learning)",
            InfluencerContentType.CONTROVERSIAL_TAKES: "6:00 PM EST (evening debate time)"
        }
        
        return timing_map.get(content_type, "12:00 PM EST")

    def _identify_target_audience(self, content_type: InfluencerContentType) -> List[str]:
        """Identify target audience for content type"""
        
        audience_map = {
            InfluencerContentType.THOUGHT_LEADERSHIP: ["industry_leaders", "restaurant_owners", "business_professionals"],
            InfluencerContentType.DATA_INSIGHTS: ["data_enthusiasts", "restaurant_managers", "tech_professionals"],
            InfluencerContentType.INDUSTRY_TRENDS: ["restaurant_owners", "investors", "industry_analysts"],
            InfluencerContentType.SUCCESS_STORIES: ["potential_clients", "restaurant_owners", "small_business_owners"],
            InfluencerContentType.BEHIND_SCENES: ["tech_community", "followers", "potential_employees"],
            InfluencerContentType.VIRAL_HOOKS: ["broad_audience", "restaurant_community", "business_owners"],
            InfluencerContentType.EDUCATIONAL: ["restaurant_owners", "managers", "entrepreneurs"],
            InfluencerContentType.CONTROVERSIAL_TAKES: ["industry_professionals", "thought_leaders", "debate_enthusiasts"]
        }
        
        return audience_map.get(content_type, ["restaurant_owners", "business_professionals"])

    async def generate_viral_campaign(self, theme: str, num_posts: int = 5) -> List[InfluencerContent]:
        """Generate a viral campaign with multiple coordinated posts"""
        
        campaign_posts = []
        content_types = [
            InfluencerContentType.VIRAL_HOOKS,
            InfluencerContentType.DATA_INSIGHTS,
            InfluencerContentType.SUCCESS_STORIES,
            InfluencerContentType.THOUGHT_LEADERSHIP,
            InfluencerContentType.EDUCATIONAL
        ]
        
        for i in range(num_posts):
            content_type = content_types[i % len(content_types)]
            context = {"theme": theme, "campaign_position": i + 1, "total_posts": num_posts}
            
            post = await self.generate_influencer_content(content_type, context)
            campaign_posts.append(post)
        
        return campaign_posts

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics for influencer content"""
        return {
            "content_types_available": len(self.content_strategies),
            "viral_factors_tracked": len(self.viral_templates),
            "engagement_hooks_available": len(self.engagement_hooks),
            "ai_provider_status": "Gemini-powered" if "gemini" in self.ai_provider.providers else "Fallback mode"
        }
