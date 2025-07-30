#!/usr/bin/env python3
"""
Engagement Strategy Engine for SME Analytica
Intelligent system to identify high-value opportunities and determine optimal engagement strategies
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import json

class EngagementStrategy(str, Enum):
    THOUGHT_LEADERSHIP = "thought_leadership"
    COMMUNITY_BUILDING = "community_building"
    PROSPECT_CONVERSION = "prospect_conversion"
    BRAND_AWARENESS = "brand_awareness"
    COMPETITIVE_RESPONSE = "competitive_response"
    TREND_AMPLIFICATION = "trend_amplification"
    RELATIONSHIP_BUILDING = "relationship_building"

class OpportunityPriority(str, Enum):
    CRITICAL = "critical"      # 9-10 score
    HIGH = "high"             # 7-8 score
    MEDIUM = "medium"         # 5-6 score
    LOW = "low"               # 3-4 score
    IGNORE = "ignore"         # 0-2 score

@dataclass
class EngagementOpportunity:
    """Comprehensive engagement opportunity with strategic analysis"""
    id: str
    content: str
    author: str
    author_profile: Dict[str, Any]
    platform: str
    opportunity_type: str
    
    # Scoring metrics
    relevance_score: float
    conversion_potential: float
    engagement_potential: float
    brand_alignment: float
    urgency_score: float
    competitive_value: float
    
    # Strategic analysis
    recommended_strategy: EngagementStrategy
    priority: OpportunityPriority
    estimated_reach: int
    estimated_engagement: int
    conversion_likelihood: float
    
    # Timing and context
    discovered_at: datetime
    optimal_response_time: datetime
    context_factors: List[str]
    competitive_context: Optional[str] = None
    trending_context: Optional[str] = None

@dataclass
class EngagementPlan:
    """Strategic engagement plan with multiple opportunities"""
    opportunities: List[EngagementOpportunity]
    total_estimated_reach: int
    total_estimated_engagement: int
    strategy_distribution: Dict[EngagementStrategy, int]
    priority_distribution: Dict[OpportunityPriority, int]
    execution_timeline: List[Tuple[datetime, str]]  # (time, opportunity_id)

class EngagementStrategyEngine:
    """Intelligent engagement strategy engine"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Strategy configuration
        self.strategy_config = self._initialize_strategy_config()
        self.scoring_weights = self._initialize_scoring_weights()
        self.competitive_intelligence = self._initialize_competitive_intelligence()
        
        # Performance tracking
        self.strategy_performance = {}
        self.opportunity_history = []
        
        # Analytics
        self.engine_stats = {
            "opportunities_analyzed": 0,
            "high_value_opportunities": 0,
            "strategies_recommended": {},
            "conversion_predictions": [],
            "start_time": datetime.now()
        }

    def _initialize_strategy_config(self) -> Dict[str, Any]:
        """Initialize engagement strategy configuration"""
        return {
            EngagementStrategy.THOUGHT_LEADERSHIP: {
                "triggers": [
                    "industry_discussion", "data_sharing", "trend_analysis",
                    "expert_opinion", "research_findings"
                ],
                "target_audience": ["industry_professionals", "influencers", "media"],
                "optimal_timing": "business_hours",
                "content_style": "authoritative_data_driven",
                "success_metrics": ["reach", "engagement_rate", "shares"],
                "conversion_potential": 0.15
            },
            EngagementStrategy.COMMUNITY_BUILDING: {
                "triggers": [
                    "help_request", "question", "community_discussion",
                    "support_needed", "advice_seeking"
                ],
                "target_audience": ["restaurant_owners", "small_business", "community"],
                "optimal_timing": "any_time",
                "content_style": "helpful_supportive",
                "success_metrics": ["replies", "community_engagement", "sentiment"],
                "conversion_potential": 0.25
            },
            EngagementStrategy.PROSPECT_CONVERSION: {
                "triggers": [
                    "solution_seeking", "vendor_evaluation", "pain_point_expression",
                    "budget_discussion", "implementation_planning"
                ],
                "target_audience": ["qualified_prospects", "decision_makers"],
                "optimal_timing": "business_hours",
                "content_style": "solution_focused",
                "success_metrics": ["dm_requests", "website_visits", "demo_requests"],
                "conversion_potential": 0.45
            },
            EngagementStrategy.BRAND_AWARENESS: {
                "triggers": [
                    "industry_mention", "general_discussion", "brand_opportunity",
                    "visibility_moment", "association_building"
                ],
                "target_audience": ["broad_audience", "potential_customers"],
                "optimal_timing": "peak_hours",
                "content_style": "brand_consistent",
                "success_metrics": ["impressions", "brand_mentions", "followers"],
                "conversion_potential": 0.08
            },
            EngagementStrategy.COMPETITIVE_RESPONSE: {
                "triggers": [
                    "competitor_mention", "comparison_discussion", "alternative_seeking",
                    "competitive_threat", "market_positioning"
                ],
                "target_audience": ["prospects", "industry_watchers"],
                "optimal_timing": "immediate",
                "content_style": "confident_differentiated",
                "success_metrics": ["competitive_wins", "positioning_strength"],
                "conversion_potential": 0.35
            },
            EngagementStrategy.TREND_AMPLIFICATION: {
                "triggers": [
                    "trending_topic", "viral_content", "industry_trend",
                    "news_event", "cultural_moment"
                ],
                "target_audience": ["trend_followers", "broad_audience"],
                "optimal_timing": "trend_peak",
                "content_style": "timely_relevant",
                "success_metrics": ["viral_potential", "trend_association"],
                "conversion_potential": 0.12
            },
            EngagementStrategy.RELATIONSHIP_BUILDING: {
                "triggers": [
                    "influencer_content", "partner_mention", "relationship_opportunity",
                    "networking_moment", "collaboration_signal"
                ],
                "target_audience": ["influencers", "partners", "industry_leaders"],
                "optimal_timing": "relationship_appropriate",
                "content_style": "relationship_focused",
                "success_metrics": ["relationship_strength", "collaboration_opportunities"],
                "conversion_potential": 0.20
            }
        }

    def _initialize_scoring_weights(self) -> Dict[str, float]:
        """Initialize scoring weights for opportunity evaluation"""
        return {
            "relevance_score": 0.25,
            "conversion_potential": 0.25,
            "engagement_potential": 0.20,
            "brand_alignment": 0.15,
            "urgency_score": 0.10,
            "competitive_value": 0.05
        }

    def _initialize_competitive_intelligence(self) -> Dict[str, Any]:
        """Initialize competitive intelligence data"""
        return {
            "competitors": {
                "toast": {
                    "strengths": ["market_share", "pos_integration"],
                    "weaknesses": ["analytics_depth", "sme_focus"],
                    "response_strategy": "differentiate_analytics"
                },
                "square": {
                    "strengths": ["ease_of_use", "brand_recognition"],
                    "weaknesses": ["advanced_analytics", "restaurant_specific"],
                    "response_strategy": "highlight_specialization"
                },
                "opentable": {
                    "strengths": ["reservation_system", "diner_network"],
                    "weaknesses": ["pricing_optimization", "operational_analytics"],
                    "response_strategy": "complement_positioning"
                }
            },
            "differentiation_points": [
                "AI-powered dynamic pricing",
                "Restaurant-specific analytics",
                "SME focus and accessibility",
                "Real-time optimization",
                "10% margin improvement proven results"
            ]
        }

    async def analyze_opportunity(self, content: str, author: str, author_profile: Dict[str, Any],
                                platform: str, opportunity_type: str, 
                                context_data: Dict[str, Any]) -> EngagementOpportunity:
        """Analyze and score an engagement opportunity"""
        
        try:
            # Calculate individual scores
            relevance_score = self._calculate_relevance_score(content, author_profile)
            conversion_potential = self._calculate_conversion_potential(content, author_profile)
            engagement_potential = self._calculate_engagement_potential(content, author_profile, context_data)
            brand_alignment = self._calculate_brand_alignment(content)
            urgency_score = self._calculate_urgency_score(content, context_data)
            competitive_value = self._calculate_competitive_value(content)
            
            # Calculate overall opportunity score
            overall_score = (
                relevance_score * self.scoring_weights["relevance_score"] +
                conversion_potential * self.scoring_weights["conversion_potential"] +
                engagement_potential * self.scoring_weights["engagement_potential"] +
                brand_alignment * self.scoring_weights["brand_alignment"] +
                urgency_score * self.scoring_weights["urgency_score"] +
                competitive_value * self.scoring_weights["competitive_value"]
            )
            
            # Determine strategy and priority
            recommended_strategy = self._determine_optimal_strategy(
                content, author_profile, overall_score, context_data
            )
            priority = self._determine_priority(overall_score, recommended_strategy)
            
            # Calculate estimates
            estimated_reach = self._estimate_reach(author_profile, recommended_strategy)
            estimated_engagement = self._estimate_engagement(content, recommended_strategy)
            conversion_likelihood = self._calculate_conversion_likelihood(
                conversion_potential, recommended_strategy
            )
            
            # Determine optimal timing
            optimal_response_time = self._calculate_optimal_timing(
                urgency_score, recommended_strategy, context_data
            )
            
            # Extract context factors
            context_factors = self._extract_context_factors(content, context_data)
            
            # Create opportunity object
            opportunity = EngagementOpportunity(
                id=f"opp_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{hash(content) % 10000}",
                content=content,
                author=author,
                author_profile=author_profile,
                platform=platform,
                opportunity_type=opportunity_type,
                relevance_score=relevance_score,
                conversion_potential=conversion_potential,
                engagement_potential=engagement_potential,
                brand_alignment=brand_alignment,
                urgency_score=urgency_score,
                competitive_value=competitive_value,
                recommended_strategy=recommended_strategy,
                priority=priority,
                estimated_reach=estimated_reach,
                estimated_engagement=estimated_engagement,
                conversion_likelihood=conversion_likelihood,
                discovered_at=datetime.now(),
                optimal_response_time=optimal_response_time,
                context_factors=context_factors,
                competitive_context=context_data.get("competitive_context"),
                trending_context=context_data.get("trending_context")
            )
            
            # Update analytics
            self._update_analytics(opportunity)
            
            return opportunity
            
        except Exception as e:
            self.logger.error(f"Error analyzing opportunity: {e}")
            raise

    def _calculate_relevance_score(self, content: str, author_profile: Dict[str, Any]) -> float:
        """Calculate relevance score (0-10)"""
        score = 3.0  # Base score
        content_lower = content.lower()
        
        # Industry keywords
        industry_keywords = {
            "restaurant": 2.0, "analytics": 2.0, "data": 1.5, "pricing": 2.0,
            "ai": 1.5, "automation": 1.5, "small business": 1.5, "hospitality": 2.0,
            "pos": 1.5, "integration": 1.0, "revenue": 1.5, "profit": 1.5,
            "optimization": 2.0, "efficiency": 1.0, "growth": 1.0, "menu": 1.5
        }
        
        for keyword, weight in industry_keywords.items():
            if keyword in content_lower:
                score += weight
        
        # Author profile relevance
        bio = author_profile.get('description', '').lower()
        if any(word in bio for word in ['restaurant', 'business', 'owner', 'manager']):
            score += 2.0
        
        # Follower count influence
        followers = author_profile.get('followers', 0)
        if followers > 10000:
            score += 1.0
        elif followers > 1000:
            score += 0.5
        
        return min(score, 10.0)

    def _calculate_conversion_potential(self, content: str, author_profile: Dict[str, Any]) -> float:
        """Calculate conversion potential (0-10)"""
        score = 2.0  # Base score
        content_lower = content.lower()
        
        # High conversion signals
        conversion_signals = {
            "looking for": 3.0, "need help": 2.5, "recommendations": 2.0,
            "advice": 1.5, "struggling with": 3.0, "how to": 2.0,
            "best solution": 2.5, "which platform": 3.0, "budget": 2.0,
            "implementation": 2.5, "vendor": 2.0, "comparison": 1.5
        }
        
        for signal, weight in conversion_signals.items():
            if signal in content_lower:
                score += weight
        
        # Target customer indicators
        target_indicators = {
            "restaurant owner": 3.0, "small business": 2.0, "pos system": 2.5,
            "analytics": 2.0, "hotel manager": 2.5, "retail business": 2.0,
            "menu pricing": 3.0, "revenue optimization": 3.0
        }
        
        for indicator, weight in target_indicators.items():
            if indicator in content_lower:
                score += weight
        
        # Author profile factors
        bio = author_profile.get('description', '').lower()
        if 'owner' in bio or 'ceo' in bio or 'founder' in bio:
            score += 2.0
        elif 'manager' in bio or 'director' in bio:
            score += 1.5
        
        return min(score, 10.0)

    def _calculate_engagement_potential(self, content: str, author_profile: Dict[str, Any],
                                      context_data: Dict[str, Any]) -> float:
        """Calculate engagement potential (0-10)"""
        score = 4.0  # Base score
        
        # Content engagement factors
        if '?' in content:
            score += 2.0  # Questions generate engagement
        
        if len(content) > 100:
            score += 1.0  # Longer content often gets more engagement
        
        # Author influence
        followers = author_profile.get('followers', 0)
        if followers > 50000:
            score += 3.0
        elif followers > 10000:
            score += 2.0
        elif followers > 1000:
            score += 1.0
        
        # Existing engagement
        existing_engagement = context_data.get('existing_engagement', 0)
        if existing_engagement > 50:
            score += 2.0
        elif existing_engagement > 10:
            score += 1.0
        
        # Trending context
        if context_data.get('trending_context'):
            score += 1.5
        
        return min(score, 10.0)

    def _calculate_brand_alignment(self, content: str) -> float:
        """Calculate brand alignment score (0-10)"""
        score = 5.0  # Neutral baseline
        content_lower = content.lower()
        
        # Positive alignment
        positive_keywords = [
            'restaurant', 'analytics', 'data', 'pricing', 'ai', 'automation',
            'small business', 'hospitality', 'pos', 'integration', 'revenue',
            'profit', 'optimization', 'efficiency', 'growth', 'technology'
        ]
        
        for keyword in positive_keywords:
            if keyword in content_lower:
                score += 0.3
        
        # Negative alignment
        negative_keywords = [
            'spam', 'scam', 'fake', 'illegal', 'controversial', 'politics',
            'religion', 'personal attack', 'harassment', 'offensive'
        ]
        
        for keyword in negative_keywords:
            if keyword in content_lower:
                score -= 3.0
        
        return max(min(score, 10.0), 0.0)

    def _calculate_urgency_score(self, content: str, context_data: Dict[str, Any]) -> float:
        """Calculate urgency score (0-10)"""
        score = 5.0  # Base urgency
        content_lower = content.lower()
        
        # Time-sensitive indicators
        urgent_words = ['urgent', 'asap', 'immediately', 'now', 'today', 'breaking']
        for word in urgent_words:
            if word in content_lower:
                score += 2.0
        
        # Question urgency
        if '?' in content:
            score += 1.0
        
        # Trending context urgency
        if context_data.get('trending_context'):
            score += 2.0
        
        # Competitive context urgency
        if context_data.get('competitive_context'):
            score += 1.5
        
        # Time decay (older content is less urgent)
        content_age = context_data.get('content_age_hours', 0)
        if content_age > 24:
            score -= 2.0
        elif content_age > 6:
            score -= 1.0
        
        return max(min(score, 10.0), 0.0)

    def _calculate_competitive_value(self, content: str) -> float:
        """Calculate competitive value (0-10)"""
        score = 2.0  # Base score
        content_lower = content.lower()
        
        # Competitor mentions
        competitors = list(self.competitive_intelligence["competitors"].keys())
        for competitor in competitors:
            if competitor in content_lower:
                score += 3.0
        
        # Competitive keywords
        competitive_keywords = [
            'comparison', 'alternative', 'vs', 'versus', 'better than',
            'switch from', 'replace', 'competitor', 'market leader'
        ]
        
        for keyword in competitive_keywords:
            if keyword in content_lower:
                score += 2.0
        
        return min(score, 10.0)

    def _determine_optimal_strategy(self, content: str, author_profile: Dict[str, Any],
                                  overall_score: float, context_data: Dict[str, Any]) -> EngagementStrategy:
        """Determine optimal engagement strategy"""
        
        content_lower = content.lower()
        
        # High conversion potential -> prospect conversion
        if any(signal in content_lower for signal in ['looking for', 'need help', 'budget', 'vendor']):
            return EngagementStrategy.PROSPECT_CONVERSION
        
        # Competitive context -> competitive response
        if context_data.get('competitive_context'):
            return EngagementStrategy.COMPETITIVE_RESPONSE
        
        # Trending context -> trend amplification
        if context_data.get('trending_context'):
            return EngagementStrategy.TREND_AMPLIFICATION
        
        # Questions and help requests -> community building
        if '?' in content or any(word in content_lower for word in ['help', 'advice', 'how to']):
            return EngagementStrategy.COMMUNITY_BUILDING
        
        # Industry discussions with high relevance -> thought leadership
        if overall_score > 7.0 and any(word in content_lower for word in ['analytics', 'data', 'industry']):
            return EngagementStrategy.THOUGHT_LEADERSHIP
        
        # Influencer content -> relationship building
        if author_profile.get('followers', 0) > 10000:
            return EngagementStrategy.RELATIONSHIP_BUILDING
        
        # Default to brand awareness
        return EngagementStrategy.BRAND_AWARENESS

    def _determine_priority(self, overall_score: float, strategy: EngagementStrategy) -> OpportunityPriority:
        """Determine opportunity priority"""
        
        # Strategy-based priority adjustments
        strategy_multipliers = {
            EngagementStrategy.PROSPECT_CONVERSION: 1.2,
            EngagementStrategy.COMPETITIVE_RESPONSE: 1.1,
            EngagementStrategy.THOUGHT_LEADERSHIP: 1.0,
            EngagementStrategy.COMMUNITY_BUILDING: 0.9,
            EngagementStrategy.RELATIONSHIP_BUILDING: 0.9,
            EngagementStrategy.TREND_AMPLIFICATION: 0.8,
            EngagementStrategy.BRAND_AWARENESS: 0.7
        }
        
        adjusted_score = overall_score * strategy_multipliers.get(strategy, 1.0)
        
        if adjusted_score >= 9.0:
            return OpportunityPriority.CRITICAL
        elif adjusted_score >= 7.0:
            return OpportunityPriority.HIGH
        elif adjusted_score >= 5.0:
            return OpportunityPriority.MEDIUM
        elif adjusted_score >= 3.0:
            return OpportunityPriority.LOW
        else:
            return OpportunityPriority.IGNORE

    def _estimate_reach(self, author_profile: Dict[str, Any], strategy: EngagementStrategy) -> int:
        """Estimate potential reach"""
        base_reach = author_profile.get('followers', 0)
        
        # Strategy multipliers
        strategy_multipliers = {
            EngagementStrategy.TREND_AMPLIFICATION: 3.0,
            EngagementStrategy.THOUGHT_LEADERSHIP: 2.0,
            EngagementStrategy.COMPETITIVE_RESPONSE: 1.5,
            EngagementStrategy.BRAND_AWARENESS: 1.2,
            EngagementStrategy.RELATIONSHIP_BUILDING: 1.0,
            EngagementStrategy.COMMUNITY_BUILDING: 0.8,
            EngagementStrategy.PROSPECT_CONVERSION: 0.5
        }
        
        multiplier = strategy_multipliers.get(strategy, 1.0)
        return int(base_reach * multiplier)

    def _estimate_engagement(self, content: str, strategy: EngagementStrategy) -> int:
        """Estimate potential engagement"""
        base_engagement = 10  # Base engagement estimate
        
        # Content factors
        if '?' in content:
            base_engagement += 15
        if len(content) > 100:
            base_engagement += 5
        
        # Strategy multipliers
        strategy_multipliers = {
            EngagementStrategy.COMMUNITY_BUILDING: 2.5,
            EngagementStrategy.PROSPECT_CONVERSION: 2.0,
            EngagementStrategy.THOUGHT_LEADERSHIP: 1.8,
            EngagementStrategy.COMPETITIVE_RESPONSE: 1.5,
            EngagementStrategy.RELATIONSHIP_BUILDING: 1.3,
            EngagementStrategy.TREND_AMPLIFICATION: 1.2,
            EngagementStrategy.BRAND_AWARENESS: 1.0
        }
        
        multiplier = strategy_multipliers.get(strategy, 1.0)
        return int(base_engagement * multiplier)

    def _calculate_conversion_likelihood(self, conversion_potential: float, 
                                       strategy: EngagementStrategy) -> float:
        """Calculate conversion likelihood (0-1)"""
        base_likelihood = conversion_potential / 10.0
        
        # Strategy conversion rates
        strategy_rates = self.strategy_config[strategy]["conversion_potential"]
        
        return min(base_likelihood * strategy_rates, 1.0)

    def _calculate_optimal_timing(self, urgency_score: float, strategy: EngagementStrategy,
                                context_data: Dict[str, Any]) -> datetime:
        """Calculate optimal response timing"""
        now = datetime.now()
        
        # High urgency -> immediate response
        if urgency_score >= 8.0:
            return now
        
        # Strategy-based timing
        strategy_delays = {
            EngagementStrategy.COMPETITIVE_RESPONSE: 0,      # Immediate
            EngagementStrategy.PROSPECT_CONVERSION: 30,      # 30 minutes
            EngagementStrategy.COMMUNITY_BUILDING: 60,       # 1 hour
            EngagementStrategy.THOUGHT_LEADERSHIP: 120,      # 2 hours
            EngagementStrategy.RELATIONSHIP_BUILDING: 180,   # 3 hours
            EngagementStrategy.TREND_AMPLIFICATION: 60,      # 1 hour
            EngagementStrategy.BRAND_AWARENESS: 240          # 4 hours
        }
        
        delay_minutes = strategy_delays.get(strategy, 120)
        return now + timedelta(minutes=delay_minutes)

    def _extract_context_factors(self, content: str, context_data: Dict[str, Any]) -> List[str]:
        """Extract relevant context factors"""
        factors = []
        content_lower = content.lower()
        
        if '?' in content:
            factors.append("question")
        
        if any(word in content_lower for word in ['urgent', 'asap', 'now']):
            factors.append("time_sensitive")
        
        if context_data.get('trending_context'):
            factors.append("trending")
        
        if context_data.get('competitive_context'):
            factors.append("competitive")
        
        if any(word in content_lower for word in ['help', 'advice', 'struggling']):
            factors.append("help_seeking")
        
        return factors

    def _update_analytics(self, opportunity: EngagementOpportunity) -> None:
        """Update engine analytics"""
        self.engine_stats["opportunities_analyzed"] += 1
        
        if opportunity.priority in [OpportunityPriority.CRITICAL, OpportunityPriority.HIGH]:
            self.engine_stats["high_value_opportunities"] += 1
        
        strategy = opportunity.recommended_strategy.value
        if strategy not in self.engine_stats["strategies_recommended"]:
            self.engine_stats["strategies_recommended"][strategy] = 0
        self.engine_stats["strategies_recommended"][strategy] += 1
        
        self.engine_stats["conversion_predictions"].append(opportunity.conversion_likelihood)

    async def create_engagement_plan(self, opportunities: List[EngagementOpportunity],
                                   max_engagements: int = 10) -> EngagementPlan:
        """Create strategic engagement plan from opportunities"""
        
        # Filter and sort opportunities
        filtered_opportunities = [
            opp for opp in opportunities 
            if opp.priority != OpportunityPriority.IGNORE
        ]
        
        # Sort by priority and conversion potential
        sorted_opportunities = sorted(
            filtered_opportunities,
            key=lambda x: (x.priority.value, x.conversion_likelihood),
            reverse=True
        )[:max_engagements]
        
        # Calculate aggregates
        total_reach = sum(opp.estimated_reach for opp in sorted_opportunities)
        total_engagement = sum(opp.estimated_engagement for opp in sorted_opportunities)
        
        # Strategy distribution
        strategy_dist = {}
        for opp in sorted_opportunities:
            strategy = opp.recommended_strategy
            strategy_dist[strategy] = strategy_dist.get(strategy, 0) + 1
        
        # Priority distribution
        priority_dist = {}
        for opp in sorted_opportunities:
            priority = opp.priority
            priority_dist[priority] = priority_dist.get(priority, 0) + 1
        
        # Execution timeline
        timeline = [(opp.optimal_response_time, opp.id) for opp in sorted_opportunities]
        timeline.sort(key=lambda x: x[0])
        
        return EngagementPlan(
            opportunities=sorted_opportunities,
            total_estimated_reach=total_reach,
            total_estimated_engagement=total_engagement,
            strategy_distribution=strategy_dist,
            priority_distribution=priority_dist,
            execution_timeline=timeline
        )

    def get_engine_stats(self) -> Dict[str, Any]:
        """Get engine performance statistics"""
        avg_conversion = (
            sum(self.engine_stats["conversion_predictions"]) / 
            max(len(self.engine_stats["conversion_predictions"]), 1)
        )
        
        runtime = datetime.now() - self.engine_stats["start_time"]
        
        return {
            "runtime": str(runtime),
            "opportunities_analyzed": self.engine_stats["opportunities_analyzed"],
            "high_value_opportunities": self.engine_stats["high_value_opportunities"],
            "strategies_recommended": self.engine_stats["strategies_recommended"],
            "average_conversion_prediction": round(avg_conversion, 3),
            "high_value_rate": (
                self.engine_stats["high_value_opportunities"] / 
                max(self.engine_stats["opportunities_analyzed"], 1) * 100
            )
        }
