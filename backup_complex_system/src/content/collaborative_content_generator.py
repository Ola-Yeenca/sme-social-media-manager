#!/usr/bin/env python3
"""
Collaborative Content Generator for SME Analytica
AI Council-powered content creation where GPT, Claude, and Gemini work together
to create, validate, and optimize social media content for maximum impact
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

from ..ai_council import AICouncilManager, VoteType
from ..ai_providers import AIProviderManager, ContentRequest, ContentType
from ..notion.notion_manager import NotionManager

class ContentCategory(str, Enum):
    THOUGHT_LEADERSHIP = "thought_leadership"
    DATA_INSIGHTS = "data_insights"
    INDUSTRY_TRENDS = "industry_trends"
    SUCCESS_STORIES = "success_stories"
    EDUCATIONAL = "educational"
    VIRAL_HOOKS = "viral_hooks"
    COMMUNITY_ENGAGEMENT = "community_engagement"
    PRODUCT_SHOWCASE = "product_showcase"

@dataclass
class CollaborativeContent:
    """Content created through AI collaboration"""
    content: str
    category: ContentCategory
    council_decision: Any  # CouncilDecision
    collaboration_process: Dict[str, Any]
    final_score: float
    posting_priority: int
    optimal_timing: str
    target_audience: List[str]
    expected_engagement: Dict[str, float]
    hashtags: List[str]
    created_at: datetime

class CollaborativeContentGenerator:
    """AI Council-powered collaborative content generation system"""
    
    def __init__(self, ai_provider_manager: AIProviderManager, notion_manager: NotionManager = None):
        self.ai_provider = ai_provider_manager
        self.ai_council = AICouncilManager(ai_provider_manager)
        self.notion_manager = notion_manager
        self.logger = logging.getLogger(__name__)
        
        # Content strategy configuration
        self.content_strategy = self._initialize_content_strategy()
        self.collaboration_history = []
        
        # Performance tracking
        self.generation_stats = {
            "content_created": 0,
            "council_approvals": 0,
            "collaborative_successes": 0,
            "unanimous_decisions": 0,
            "start_time": datetime.now()
        }

    def _initialize_content_strategy(self) -> Dict[str, Any]:
        """Initialize content strategy for different categories"""
        return {
            ContentCategory.THOUGHT_LEADERSHIP: {
                "themes": [
                    "future_of_restaurant_analytics", "ai_transformation_hospitality",
                    "data_driven_restaurant_success", "sme_digital_revolution"
                ],
                "tone": "authoritative_visionary",
                "target_engagement": 0.08,
                "posting_frequency": "daily",
                "optimal_times": ["9:00 AM", "2:00 PM", "6:00 PM"]
            },
            ContentCategory.DATA_INSIGHTS: {
                "themes": [
                    "restaurant_performance_metrics", "pricing_optimization_data",
                    "customer_behavior_analytics", "operational_efficiency_stats"
                ],
                "tone": "analytical_revealing",
                "target_engagement": 0.12,
                "posting_frequency": "3x_weekly",
                "optimal_times": ["10:00 AM", "3:00 PM"]
            },
            ContentCategory.SUCCESS_STORIES: {
                "themes": [
                    "client_transformation_stories", "roi_case_studies",
                    "before_after_analytics", "restaurant_growth_journeys"
                ],
                "tone": "inspiring_results_focused",
                "target_engagement": 0.15,
                "posting_frequency": "2x_weekly",
                "optimal_times": ["11:00 AM", "4:00 PM"]
            },
            ContentCategory.VIRAL_HOOKS: {
                "themes": [
                    "shocking_restaurant_statistics", "industry_myths_busted",
                    "hidden_profit_opportunities", "restaurant_owner_secrets"
                ],
                "tone": "attention_grabbing_provocative",
                "target_engagement": 0.25,
                "posting_frequency": "weekly",
                "optimal_times": ["8:00 PM", "9:00 PM"]
            },
            ContentCategory.EDUCATIONAL: {
                "themes": [
                    "restaurant_analytics_tutorials", "pricing_strategy_guides",
                    "pos_integration_tips", "data_interpretation_help"
                ],
                "tone": "helpful_educational",
                "target_engagement": 0.14,
                "posting_frequency": "2x_weekly",
                "optimal_times": ["12:00 PM", "5:00 PM"]
            }
        }

    async def generate_collaborative_content(self, category: ContentCategory, 
                                           custom_theme: str = None) -> CollaborativeContent:
        """Generate content through AI Council collaboration"""
        
        try:
            # Get strategy for this category
            strategy = self.content_strategy.get(category, {})
            
            # Select theme
            if custom_theme:
                theme = custom_theme
            else:
                themes = strategy.get("themes", ["general_content"])
                theme = themes[len(self.collaboration_history) % len(themes)]
            
            self.logger.info(f"🤝 Starting AI Council collaboration for {category.value} content on theme: {theme}")
            
            # Phase 1: Collaborative content creation
            collaboration_result = await self.ai_council.collaborative_content_creation(
                theme=theme,
                context={
                    "category": category.value,
                    "strategy": strategy,
                    "sme_context": {
                        "company": "SME Analytica",
                        "product": "MenuFlow dynamic pricing",
                        "achievements": "500+ restaurants, 10% margin improvement",
                        "expertise": "restaurant analytics, AI optimization"
                    }
                }
            )
            
            if not collaboration_result["collaboration_success"]:
                raise Exception("AI Council collaboration failed to produce approved content")
            
            selected_content = collaboration_result["selected_content"]["content"]
            council_decision = collaboration_result["council_decision"]
            
            # Phase 2: Content optimization based on council feedback
            if council_decision.final_decision == VoteType.MODIFY:
                self.logger.info(f"🔄 Optimizing content based on council suggestions: {council_decision.modifications_required[:2]}")
                optimized_content = await self._optimize_content_with_suggestions(
                    selected_content, council_decision.modifications_required, category, theme
                )
                
                # Re-validate optimized content
                final_decision = await self.ai_council.evaluate_content_for_posting(
                    optimized_content,
                    {"category": category.value, "theme": theme, "optimization_round": 2}
                )
                
                if final_decision.final_decision == VoteType.APPROVE:
                    selected_content = optimized_content
                    council_decision = final_decision
            
            # Phase 3: Generate metadata and optimization details
            content_metadata = await self._generate_content_metadata(
                selected_content, category, theme, council_decision
            )
            
            # Create collaborative content object
            collaborative_content = CollaborativeContent(
                content=selected_content,
                category=category,
                council_decision=council_decision,
                collaboration_process=collaboration_result,
                final_score=council_decision.consensus_score,
                posting_priority=council_decision.execution_priority,
                optimal_timing=content_metadata["optimal_timing"],
                target_audience=content_metadata["target_audience"],
                expected_engagement=content_metadata["expected_engagement"],
                hashtags=content_metadata["hashtags"],
                created_at=datetime.now()
            )
            
            # Store collaboration history
            self.collaboration_history.append(collaborative_content)
            self._update_generation_stats(collaborative_content)
            
            # Save to Notion if available
            if self.notion_manager:
                await self._save_to_notion(collaborative_content)
            
            self.logger.info(
                f"✅ Collaborative content created: {category.value} "
                f"(Score: {council_decision.consensus_score:.1f}/10, "
                f"Priority: {council_decision.execution_priority})"
            )
            
            return collaborative_content
            
        except Exception as e:
            self.logger.error(f"❌ Collaborative content generation failed: {e}")
            raise

    async def _optimize_content_with_suggestions(self, content: str, suggestions: List[str],
                                               category: ContentCategory, theme: str) -> str:
        """Optimize content based on AI Council suggestions"""
        
        optimization_prompt = f"""
        Optimize this SME Analytica social media content based on AI Council feedback:
        
        Original Content: "{content}"
        Category: {category.value}
        Theme: {theme}
        
        Council Suggestions:
        {chr(10).join(f"• {suggestion}" for suggestion in suggestions[:5])}
        
        Create an improved version that:
        - Addresses all council suggestions
        - Maintains SME Analytica's professional brand voice
        - Stays under 280 characters for Twitter
        - Maximizes engagement potential
        - Includes specific data or insights when possible
        
        Return only the optimized content, no explanation.
        """
        
        try:
            content_request = ContentRequest(
                content_type=ContentType.SOCIAL_MEDIA_POST,
                platform="twitter",
                context={"prompt": optimization_prompt},
                max_length=280,
                tone="professional_engaging"
            )
            
            # Use the best available AI provider for optimization
            response = await self.ai_provider.generate_content(content_request, provider="gemini")
            optimized = response.text if hasattr(response, 'text') else str(response)
            
            return optimized.strip()
            
        except Exception as e:
            self.logger.error(f"Content optimization failed: {e}")
            return content  # Return original if optimization fails

    async def _generate_content_metadata(self, content: str, category: ContentCategory,
                                       theme: str, council_decision: Any) -> Dict[str, Any]:
        """Generate metadata for the collaborative content"""
        
        strategy = self.content_strategy.get(category, {})
        
        # Determine optimal timing
        optimal_times = strategy.get("optimal_times", ["12:00 PM"])
        optimal_timing = optimal_times[0]  # Use first optimal time
        
        # Identify target audience
        target_audience = self._identify_target_audience(category, content)
        
        # Calculate expected engagement
        base_engagement = strategy.get("target_engagement", 0.1)
        council_multiplier = council_decision.consensus_score / 10.0
        expected_engagement = {
            "likes": base_engagement * council_multiplier * 100,
            "retweets": base_engagement * council_multiplier * 30,
            "replies": base_engagement * council_multiplier * 20,
            "impressions": base_engagement * council_multiplier * 1000
        }
        
        # Generate hashtags
        hashtags = self._generate_strategic_hashtags(category, content, theme)
        
        return {
            "optimal_timing": optimal_timing,
            "target_audience": target_audience,
            "expected_engagement": expected_engagement,
            "hashtags": hashtags
        }

    def _identify_target_audience(self, category: ContentCategory, content: str) -> List[str]:
        """Identify target audience for content"""
        
        audience_map = {
            ContentCategory.THOUGHT_LEADERSHIP: ["industry_leaders", "restaurant_owners", "tech_professionals"],
            ContentCategory.DATA_INSIGHTS: ["restaurant_managers", "data_enthusiasts", "business_analysts"],
            ContentCategory.SUCCESS_STORIES: ["potential_clients", "restaurant_owners", "small_business_owners"],
            ContentCategory.VIRAL_HOOKS: ["broad_audience", "restaurant_community", "social_media_users"],
            ContentCategory.EDUCATIONAL: ["restaurant_owners", "managers", "entrepreneurs"],
            ContentCategory.INDUSTRY_TRENDS: ["industry_professionals", "investors", "thought_leaders"],
            ContentCategory.COMMUNITY_ENGAGEMENT: ["restaurant_community", "followers", "industry_peers"],
            ContentCategory.PRODUCT_SHOWCASE: ["prospects", "restaurant_owners", "decision_makers"]
        }
        
        return audience_map.get(category, ["restaurant_owners", "business_professionals"])

    def _generate_strategic_hashtags(self, category: ContentCategory, content: str, theme: str) -> List[str]:
        """Generate strategic hashtags for maximum reach"""
        
        # Base SME Analytica hashtags
        base_hashtags = ["#SMEAnalytica", "#RestaurantAnalytics", "#MenuFlow"]
        
        # Category-specific hashtags
        category_hashtags = {
            ContentCategory.THOUGHT_LEADERSHIP: ["#ThoughtLeadership", "#RestaurantTech", "#BusinessIntelligence"],
            ContentCategory.DATA_INSIGHTS: ["#DataDriven", "#Analytics", "#RestaurantData"],
            ContentCategory.SUCCESS_STORIES: ["#SuccessStory", "#RestaurantGrowth", "#ROI"],
            ContentCategory.VIRAL_HOOKS: ["#RestaurantSecrets", "#BusinessTips", "#DataRevealed"],
            ContentCategory.EDUCATIONAL: ["#RestaurantTips", "#BusinessEducation", "#Analytics101"],
            ContentCategory.INDUSTRY_TRENDS: ["#RestaurantTrends", "#FoodTech", "#HospitalityAI"],
            ContentCategory.COMMUNITY_ENGAGEMENT: ["#RestaurantCommunity", "#SmallBusiness", "#Hospitality"],
            ContentCategory.PRODUCT_SHOWCASE: ["#DynamicPricing", "#ProfitOptimization", "#RestaurantSoftware"]
        }
        
        # Combine hashtags
        hashtags = base_hashtags + category_hashtags.get(category, [])
        
        # Add trending hashtags if relevant
        trending_keywords = ["ai", "data", "optimization", "growth", "profit"]
        content_lower = content.lower()
        
        if any(keyword in content_lower for keyword in trending_keywords):
            hashtags.extend(["#AIForBusiness", "#DataDriven", "#BusinessGrowth"])
        
        return hashtags[:8]  # Limit to 8 hashtags for optimal performance

    async def generate_content_campaign(self, campaign_theme: str, 
                                      num_posts: int = 5) -> List[CollaborativeContent]:
        """Generate a coordinated content campaign through AI collaboration"""
        
        self.logger.info(f"🚀 Starting collaborative content campaign: {campaign_theme} ({num_posts} posts)")
        
        campaign_content = []
        
        # Define campaign structure
        campaign_categories = [
            ContentCategory.VIRAL_HOOKS,      # Hook to grab attention
            ContentCategory.DATA_INSIGHTS,    # Provide valuable data
            ContentCategory.THOUGHT_LEADERSHIP, # Establish authority
            ContentCategory.SUCCESS_STORIES,  # Show results
            ContentCategory.EDUCATIONAL       # Provide value
        ]
        
        for i in range(num_posts):
            category = campaign_categories[i % len(campaign_categories)]
            
            try:
                content = await self.generate_collaborative_content(
                    category=category,
                    custom_theme=f"{campaign_theme}_{category.value}"
                )
                campaign_content.append(content)
                
                # Brief pause between generations
                await asyncio.sleep(2)
                
            except Exception as e:
                self.logger.error(f"Failed to generate campaign content {i+1}: {e}")
        
        self.logger.info(f"✅ Campaign completed: {len(campaign_content)}/{num_posts} posts generated")
        
        return campaign_content

    def _update_generation_stats(self, content: CollaborativeContent) -> None:
        """Update generation statistics"""
        
        self.generation_stats["content_created"] += 1
        
        if content.council_decision.final_decision == VoteType.APPROVE:
            self.generation_stats["council_approvals"] += 1
        
        if content.collaboration_process["collaboration_success"]:
            self.generation_stats["collaborative_successes"] += 1
        
        # Check for unanimous decisions
        votes = content.council_decision.votes
        if len(set(vote.vote for vote in votes)) == 1:
            self.generation_stats["unanimous_decisions"] += 1

    async def _save_to_notion(self, content: CollaborativeContent) -> None:
        """Save collaborative content to Notion database"""
        
        try:
            content_data = {
                "content": content.content,
                "category": content.category.value,
                "final_score": content.final_score,
                "posting_priority": content.posting_priority,
                "optimal_timing": content.optimal_timing,
                "target_audience": ", ".join(content.target_audience),
                "hashtags": ", ".join(content.hashtags),
                "council_decision": content.council_decision.final_decision.value,
                "consensus_score": content.council_decision.consensus_score,
                "created_at": content.created_at.isoformat(),
                "ai_collaboration": True
            }
            
            # Save to Notion (implement based on your schema)
            # self.notion_manager.save_collaborative_content(content_data)
            
        except Exception as e:
            self.logger.error(f"Error saving to Notion: {e}")

    def get_collaboration_stats(self) -> Dict[str, Any]:
        """Get collaboration performance statistics"""
        
        total_content = self.generation_stats["content_created"]
        
        return {
            "total_content_created": total_content,
            "council_approval_rate": (self.generation_stats["council_approvals"] / max(total_content, 1)) * 100,
            "collaboration_success_rate": (self.generation_stats["collaborative_successes"] / max(total_content, 1)) * 100,
            "unanimous_decision_rate": (self.generation_stats["unanimous_decisions"] / max(total_content, 1)) * 100,
            "average_content_score": sum(c.final_score for c in self.collaboration_history) / max(len(self.collaboration_history), 1),
            "content_by_category": {
                category.value: len([c for c in self.collaboration_history if c.category == category])
                for category in ContentCategory
            },
            "recent_content": [
                {
                    "content": c.content[:50] + "...",
                    "category": c.category.value,
                    "score": c.final_score,
                    "decision": c.council_decision.final_decision.value
                }
                for c in self.collaboration_history[-5:]  # Last 5 pieces of content
            ]
        }

    async def get_ready_to_post_content(self, min_score: float = 7.0) -> List[CollaborativeContent]:
        """Get content that's ready to post based on AI Council approval"""
        
        ready_content = [
            content for content in self.collaboration_history
            if content.council_decision.final_decision == VoteType.APPROVE
            and content.final_score >= min_score
        ]
        
        # Sort by posting priority and score
        ready_content.sort(key=lambda x: (x.posting_priority, x.final_score), reverse=True)
        
        return ready_content
