#!/usr/bin/env python3
"""
AI Council Manager for SME Analytica
Collaborative AI decision-making system where GPT, Claude, and Gemini work together
to validate ideas, content, and engagement decisions for optimal social media growth
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json

from ..ai_providers import AIProviderManager, ContentRequest, ContentType

class DecisionType(str, Enum):
    CONTENT_APPROVAL = "content_approval"
    ENGAGEMENT_DECISION = "engagement_decision"
    STRATEGY_VALIDATION = "strategy_validation"
    RESPONSE_APPROVAL = "response_approval"
    CAMPAIGN_PLANNING = "campaign_planning"

class VoteType(str, Enum):
    APPROVE = "approve"
    REJECT = "reject"
    MODIFY = "modify"
    ABSTAIN = "abstain"

@dataclass
class AIVote:
    """Individual AI provider vote"""
    provider: str
    vote: VoteType
    confidence: float
    reasoning: str
    suggestions: List[str]
    score: float  # 0-10 rating

@dataclass
class CouncilDecision:
    """Final council decision"""
    decision_id: str
    decision_type: DecisionType
    content_or_action: str
    votes: List[AIVote]
    final_decision: VoteType
    consensus_score: float
    execution_priority: int
    modifications_required: List[str]
    reasoning: str
    timestamp: datetime

class AICouncilManager:
    """Manages collaborative AI decision-making for social media growth"""
    
    def __init__(self, ai_provider_manager: AIProviderManager):
        self.ai_provider = ai_provider_manager
        self.logger = logging.getLogger(__name__)
        
        # Council configuration
        self.council_config = self._initialize_council_config()
        self.decision_history = []
        
        # Performance tracking
        self.council_stats = {
            "decisions_made": 0,
            "unanimous_decisions": 0,
            "split_decisions": 0,
            "successful_outcomes": 0,
            "start_time": datetime.now()
        }

    def _initialize_council_config(self) -> Dict[str, Any]:
        """Initialize AI council configuration"""
        return {
            "council_members": {
                "gemini": {
                    "role": "Strategic Analyst",
                    "expertise": ["strategic_thinking", "market_analysis", "trend_prediction"],
                    "weight": 1.2,  # Slightly higher weight for strategic decisions
                    "personality": "analytical, forward-thinking, data-driven"
                },
                "anthropic": {
                    "role": "Brand Guardian", 
                    "expertise": ["brand_consistency", "safety_analysis", "professional_tone"],
                    "weight": 1.1,
                    "personality": "careful, professional, brand-focused"
                },
                "openai": {
                    "role": "Creative Director",
                    "expertise": ["creative_content", "engagement_optimization", "viral_potential"],
                    "weight": 1.0,
                    "personality": "creative, engaging, audience-focused"
                },
                "perplexity": {
                    "role": "Industry Expert",
                    "expertise": ["industry_insights", "factual_accuracy", "market_intelligence"],
                    "weight": 0.9,
                    "personality": "knowledgeable, accurate, industry-focused"
                }
            },
            "decision_thresholds": {
                "unanimous_required": ["brand_safety", "major_strategy"],
                "majority_sufficient": ["content_approval", "engagement_decision"],
                "minimum_consensus": 0.6,  # 60% agreement required
                "high_confidence_threshold": 8.0,
                "modification_threshold": 6.0
            },
            "voting_weights": {
                "content_quality": {"openai": 1.2, "anthropic": 1.1, "gemini": 1.0},
                "brand_safety": {"anthropic": 1.3, "gemini": 1.1, "openai": 0.9},
                "strategic_value": {"gemini": 1.3, "perplexity": 1.1, "anthropic": 1.0},
                "viral_potential": {"openai": 1.2, "gemini": 1.1, "anthropic": 0.9}
            }
        }

    async def evaluate_content_for_posting(self, content: str, context: Dict[str, Any] = None) -> CouncilDecision:
        """Have the AI council evaluate content before posting"""
        
        decision_id = f"content_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Get votes from each AI provider
        votes = []
        
        for provider_name, config in self.council_config["council_members"].items():
            if provider_name in self.ai_provider.providers and self.ai_provider.providers[provider_name].is_available:
                try:
                    vote = await self._get_content_vote(provider_name, config, content, context or {})
                    votes.append(vote)
                except Exception as e:
                    self.logger.error(f"Error getting vote from {provider_name}: {e}")
        
        # Make final decision based on votes
        decision = self._make_final_decision(
            decision_id, DecisionType.CONTENT_APPROVAL, content, votes
        )
        
        # Record decision
        self.decision_history.append(decision)
        self._update_stats(decision)
        
        return decision

    async def _get_content_vote(self, provider_name: str, config: Dict[str, Any], 
                              content: str, context: Dict[str, Any]) -> AIVote:
        """Get vote from individual AI provider"""
        
        prompt = f"""You are the {config['role']} in SME Analytica's AI Council evaluating social media content.

CONTENT TO EVALUATE: "{content}"

As the {config['role']}, provide your evaluation in this EXACT JSON format:

{{
    "vote": "approve",
    "confidence": 8.5,
    "score": 8.5,
    "reasoning": "Your detailed reasoning here",
    "suggestions": ["suggestion 1", "suggestion 2"],
    "concerns": ["concern 1"],
    "strengths": ["strength 1", "strength 2"]
}}

Vote options: approve, reject, modify
Scores: 0-10 (decimals allowed)

Evaluate based on:
- Brand alignment with SME Analytica (restaurant analytics platform)
- Professional tone and authenticity
- Engagement potential
- Business value

RESPOND ONLY WITH THE JSON - NO OTHER TEXT."""
        
        try:
            # Generate vote using the specific provider
            provider = self.ai_provider.providers[provider_name]
            
            if hasattr(provider, 'generate_content'):
                content_request = ContentRequest(
                    content_type=ContentType.ANALYSIS,
                    platform="internal",
                    context={"prompt": prompt},
                    max_length=500,
                    tone="analytical"
                )
                response = await provider.generate_content(content_request)
                response_text = response.text if hasattr(response, 'text') else str(response)
            else:
                # Fallback method
                response_text = await self._fallback_vote_generation(prompt)
            
            # Parse JSON response with better error handling
            try:
                # Clean the response text
                cleaned_response = response_text.strip()

                # Try direct JSON parsing first
                vote_data = json.loads(cleaned_response)
            except json.JSONDecodeError:
                try:
                    # Extract JSON from response if it's embedded in text
                    import re
                    json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', cleaned_response, re.DOTALL)
                    if json_match:
                        vote_data = json.loads(json_match.group())
                    else:
                        # Create a fallback vote based on response content
                        vote_data = self._create_fallback_vote(provider_name, cleaned_response, "content_evaluation")
                except:
                    # Final fallback
                    vote_data = self._create_fallback_vote(provider_name, cleaned_response, "content_evaluation")
            
            return AIVote(
                provider=provider_name,
                vote=VoteType(vote_data.get("vote", "abstain")),
                confidence=float(vote_data.get("confidence", 5.0)),
                reasoning=vote_data.get("reasoning", "No reasoning provided"),
                suggestions=vote_data.get("suggestions", []),
                score=float(vote_data.get("score", 5.0))
            )
            
        except Exception as e:
            self.logger.error(f"Error getting vote from {provider_name}: {e}")
            return AIVote(
                provider=provider_name,
                vote=VoteType.ABSTAIN,
                confidence=0.0,
                reasoning=f"Error in vote generation: {e}",
                suggestions=[],
                score=0.0
            )

    def _create_fallback_vote(self, provider_name: str, response_text: str, vote_type: str) -> Dict[str, Any]:
        """Create a fallback vote when JSON parsing fails"""

        # Analyze response text for sentiment
        response_lower = response_text.lower()

        if any(word in response_lower for word in ["approve", "good", "excellent", "great", "yes"]):
            vote = "approve"
            score = 7.0
        elif any(word in response_lower for word in ["reject", "bad", "poor", "no", "inappropriate"]):
            vote = "reject"
            score = 3.0
        else:
            vote = "modify"
            score = 5.0

        return {
            "vote": vote,
            "confidence": 6.0,
            "score": score,
            "reasoning": f"Fallback analysis from {provider_name}: {response_text[:100]}...",
            "suggestions": ["Review and improve based on AI feedback"],
            "concerns": ["JSON parsing failed"],
            "strengths": ["AI provided feedback"]
        }

    async def _fallback_vote_generation(self, prompt: str) -> str:
        """Fallback vote generation if provider-specific method fails"""
        try:
            content_request = ContentRequest(
                content_type=ContentType.ANALYSIS,
                platform="internal",
                context={"prompt": prompt},
                max_length=500,
                tone="analytical"
            )
            response = await self.ai_provider.generate_content(content_request)
            return response.text if hasattr(response, 'text') else str(response)
        except:
            return '{"vote": "abstain", "confidence": 0, "score": 0, "reasoning": "Fallback vote due to error", "suggestions": []}'

    def _make_final_decision(self, decision_id: str, decision_type: DecisionType, 
                           content: str, votes: List[AIVote]) -> CouncilDecision:
        """Make final decision based on AI council votes"""
        
        if not votes:
            return CouncilDecision(
                decision_id=decision_id,
                decision_type=decision_type,
                content_or_action=content,
                votes=[],
                final_decision=VoteType.REJECT,
                consensus_score=0.0,
                execution_priority=0,
                modifications_required=["No AI providers available for voting"],
                reasoning="No votes received from AI council",
                timestamp=datetime.now()
            )
        
        # Calculate weighted scores
        total_weight = 0
        weighted_score = 0
        approve_votes = 0
        reject_votes = 0
        modify_votes = 0
        
        all_suggestions = []
        all_reasoning = []
        
        for vote in votes:
            provider_config = self.council_config["council_members"].get(vote.provider, {})
            weight = provider_config.get("weight", 1.0)
            
            total_weight += weight
            weighted_score += vote.score * weight
            
            if vote.vote == VoteType.APPROVE:
                approve_votes += weight
            elif vote.vote == VoteType.REJECT:
                reject_votes += weight
            elif vote.vote == VoteType.MODIFY:
                modify_votes += weight
            
            all_suggestions.extend(vote.suggestions)
            all_reasoning.append(f"{vote.provider}: {vote.reasoning}")
        
        # Calculate consensus score
        consensus_score = weighted_score / total_weight if total_weight > 0 else 0
        
        # Determine final decision
        total_votes = approve_votes + reject_votes + modify_votes
        
        if approve_votes / total_votes >= 0.6 and consensus_score >= 7.0:
            final_decision = VoteType.APPROVE
            execution_priority = int(consensus_score)
        elif modify_votes / total_votes >= 0.4 or (approve_votes > reject_votes and consensus_score >= 6.0):
            final_decision = VoteType.MODIFY
            execution_priority = max(int(consensus_score - 2), 1)
        else:
            final_decision = VoteType.REJECT
            execution_priority = 0
        
        # Generate reasoning
        reasoning = self._generate_decision_reasoning(votes, final_decision, consensus_score)
        
        return CouncilDecision(
            decision_id=decision_id,
            decision_type=decision_type,
            content_or_action=content,
            votes=votes,
            final_decision=final_decision,
            consensus_score=consensus_score,
            execution_priority=execution_priority,
            modifications_required=list(set(all_suggestions)),
            reasoning=reasoning,
            timestamp=datetime.now()
        )

    def _generate_decision_reasoning(self, votes: List[AIVote], final_decision: VoteType, 
                                   consensus_score: float) -> str:
        """Generate human-readable reasoning for the decision"""
        
        vote_summary = {}
        for vote in votes:
            vote_summary[vote.provider] = vote.vote.value
        
        reasoning = f"AI Council Decision (Consensus: {consensus_score:.1f}/10)\n"
        reasoning += f"Votes: {vote_summary}\n"
        reasoning += f"Final Decision: {final_decision.value.upper()}\n\n"
        
        if final_decision == VoteType.APPROVE:
            reasoning += "✅ APPROVED: The council agrees this content aligns with SME Analytica's brand and will drive positive engagement."
        elif final_decision == VoteType.MODIFY:
            reasoning += "🔄 MODIFY: The council sees potential but recommends improvements before posting."
        else:
            reasoning += "❌ REJECTED: The council determined this content doesn't meet our standards or could harm the brand."
        
        # Add key insights from each AI
        reasoning += "\n\nCouncil Insights:\n"
        for vote in votes:
            if vote.reasoning:
                reasoning += f"• {vote.provider.title()}: {vote.reasoning[:100]}...\n"
        
        return reasoning

    async def evaluate_engagement_opportunity(self, tweet_text: str, author: str, 
                                            context: Dict[str, Any] = None) -> CouncilDecision:
        """Have the AI council evaluate whether to engage with an opportunity"""
        
        decision_id = f"engage_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Get votes from each AI provider
        votes = []
        
        for provider_name, config in self.council_config["council_members"].items():
            if provider_name in self.ai_provider.providers and self.ai_provider.providers[provider_name].is_available:
                try:
                    vote = await self._get_engagement_vote(provider_name, config, tweet_text, author, context or {})
                    votes.append(vote)
                except Exception as e:
                    self.logger.error(f"Error getting engagement vote from {provider_name}: {e}")
        
        # Make final decision
        decision = self._make_final_decision(
            decision_id, DecisionType.ENGAGEMENT_DECISION, f"Engage with @{author}: {tweet_text}", votes
        )
        
        # Record decision
        self.decision_history.append(decision)
        self._update_stats(decision)
        
        return decision

    async def _get_engagement_vote(self, provider_name: str, config: Dict[str, Any],
                                 tweet_text: str, author: str, context: Dict[str, Any]) -> AIVote:
        """Get engagement vote from individual AI provider"""
        
        prompt = f"""You are the {config['role']} evaluating an engagement opportunity for SME Analytica.

TWEET: "{tweet_text}"
AUTHOR: @{author}

Should SME Analytica engage? Respond in this EXACT JSON format:

{{
    "vote": "approve",
    "confidence": 8.0,
    "score": 8.0,
    "reasoning": "Your reasoning here",
    "suggestions": ["suggestion 1"],
    "engagement_type": "reply",
    "priority": "high"
}}

Vote: approve/reject/modify
Engagement types: reply/like/retweet/quote_tweet/ignore
Priority: high/medium/low

RESPOND ONLY WITH JSON - NO OTHER TEXT."""
        
        try:
            provider = self.ai_provider.providers[provider_name]
            
            if hasattr(provider, 'generate_content'):
                content_request = ContentRequest(
                    content_type=ContentType.ANALYSIS,
                    platform="internal",
                    context={"prompt": prompt},
                    max_length=400,
                    tone="analytical"
                )
                response = await provider.generate_content(content_request)
                response_text = response.text if hasattr(response, 'text') else str(response)
            else:
                response_text = await self._fallback_vote_generation(prompt)
            
            # Parse JSON response with better error handling
            try:
                cleaned_response = response_text.strip()
                vote_data = json.loads(cleaned_response)
            except json.JSONDecodeError:
                try:
                    import re
                    json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', cleaned_response, re.DOTALL)
                    if json_match:
                        vote_data = json.loads(json_match.group())
                    else:
                        vote_data = self._create_fallback_vote(provider_name, cleaned_response, "engagement_evaluation")
                except:
                    vote_data = self._create_fallback_vote(provider_name, cleaned_response, "engagement_evaluation")
            
            return AIVote(
                provider=provider_name,
                vote=VoteType(vote_data.get("vote", "abstain")),
                confidence=float(vote_data.get("confidence", 5.0)),
                reasoning=vote_data.get("reasoning", "No reasoning provided"),
                suggestions=vote_data.get("suggestions", []),
                score=float(vote_data.get("score", 5.0))
            )
            
        except Exception as e:
            self.logger.error(f"Error getting engagement vote from {provider_name}: {e}")
            return AIVote(
                provider=provider_name,
                vote=VoteType.ABSTAIN,
                confidence=0.0,
                reasoning=f"Error in engagement vote: {e}",
                suggestions=[],
                score=0.0
            )

    async def collaborative_content_creation(self, theme: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Have the AI council collaborate to create content"""
        
        # Phase 1: Each AI generates initial ideas
        ideas = {}
        for provider_name, config in self.council_config["council_members"].items():
            if provider_name in self.ai_provider.providers and self.ai_provider.providers[provider_name].is_available:
                try:
                    idea = await self._get_content_idea(provider_name, config, theme, context or {})
                    ideas[provider_name] = idea
                except Exception as e:
                    self.logger.error(f"Error getting idea from {provider_name}: {e}")
        
        # Phase 2: Each AI reviews and improves the ideas
        refined_ideas = {}
        for provider_name in ideas.keys():
            try:
                refined = await self._refine_ideas(provider_name, ideas, theme)
                refined_ideas[provider_name] = refined
            except Exception as e:
                self.logger.error(f"Error refining ideas with {provider_name}: {e}")
        
        # Phase 3: Council votes on the best approach
        best_content = await self._select_best_content(refined_ideas, theme)
        
        # Phase 4: Final validation by the council
        final_decision = await self.evaluate_content_for_posting(best_content["content"], context)
        
        return {
            "initial_ideas": ideas,
            "refined_ideas": refined_ideas,
            "selected_content": best_content,
            "council_decision": final_decision,
            "collaboration_success": final_decision.final_decision in [VoteType.APPROVE, VoteType.MODIFY]
        }

    async def _get_content_idea(self, provider_name: str, config: Dict[str, Any], 
                              theme: str, context: Dict[str, Any]) -> str:
        """Get content idea from individual AI provider"""
        
        prompt = f"""
        As SME Analytica's {config['role']}, generate a social media content idea for:
        Theme: {theme}
        Context: {json.dumps(context, indent=2)}
        
        Your expertise: {', '.join(config['expertise'])}
        Your approach: {config['personality']}
        
        Create content that:
        - Showcases SME Analytica's expertise in restaurant analytics
        - Provides genuine value to restaurant owners
        - Maintains professional yet engaging tone
        - Has potential for viral reach
        - Includes specific data or insights when possible
        
        Generate a tweet (under 280 characters) that exemplifies your role's perspective.
        """
        
        try:
            provider = self.ai_provider.providers[provider_name]
            content_request = ContentRequest(
                content_type=ContentType.SOCIAL_MEDIA_POST,
                platform="twitter",
                theme=theme,
                context=context,
                max_length=280,
                tone=config["personality"]
            )
            
            if hasattr(provider, 'generate_content'):
                response = await provider.generate_content(content_request)
                return response.text if hasattr(response, 'text') else str(response)
            else:
                response = await self.ai_provider.generate_content(content_request)
                return response.text if hasattr(response, 'text') else str(response)
                
        except Exception as e:
            return f"Error generating idea from {provider_name}: {e}"

    async def _refine_ideas(self, provider_name: str, all_ideas: Dict[str, str], theme: str) -> str:
        """Have AI provider refine and improve the collective ideas"""
        
        ideas_text = "\n".join([f"{name}: {idea}" for name, idea in all_ideas.items()])
        
        prompt = f"""
        Review these content ideas from the AI council for theme "{theme}":
        
        {ideas_text}
        
        As the {self.council_config['council_members'][provider_name]['role']}, 
        create an improved version that combines the best elements while maintaining your expertise focus.
        
        Make it:
        - More engaging and shareable
        - Specific to SME Analytica's value proposition
        - Professional yet approachable
        - Under 280 characters
        
        Return only the improved content, no explanation.
        """
        
        try:
            provider = self.ai_provider.providers[provider_name]
            content_request = ContentRequest(
                content_type=ContentType.SOCIAL_MEDIA_POST,
                platform="twitter",
                context={"prompt": prompt},
                max_length=280,
                tone="professional_engaging"
            )
            
            if hasattr(provider, 'generate_content'):
                response = await provider.generate_content(content_request)
                return response.text if hasattr(response, 'text') else str(response)
            else:
                response = await self.ai_provider.generate_content(content_request)
                return response.text if hasattr(response, 'text') else str(response)
                
        except Exception as e:
            return all_ideas.get(provider_name, f"Error refining from {provider_name}")

    async def _select_best_content(self, refined_ideas: Dict[str, str], theme: str) -> Dict[str, Any]:
        """Select the best content from refined ideas"""
        
        best_score = 0
        best_content = ""
        best_provider = ""
        
        # Have each AI rate all the refined ideas
        for content_provider, content in refined_ideas.items():
            total_score = 0
            vote_count = 0
            
            for voter_name in self.council_config["council_members"].keys():
                if voter_name in self.ai_provider.providers and self.ai_provider.providers[voter_name].is_available:
                    try:
                        score = await self._rate_content(voter_name, content, theme)
                        total_score += score
                        vote_count += 1
                    except Exception as e:
                        self.logger.error(f"Error getting rating from {voter_name}: {e}")
            
            avg_score = total_score / vote_count if vote_count > 0 else 0
            
            if avg_score > best_score:
                best_score = avg_score
                best_content = content
                best_provider = content_provider
        
        return {
            "content": best_content,
            "provider": best_provider,
            "score": best_score,
            "all_options": refined_ideas
        }

    async def _rate_content(self, voter_name: str, content: str, theme: str) -> float:
        """Have AI provider rate content on a scale of 0-10"""
        
        prompt = f"""
        Rate this social media content for SME Analytica on a scale of 0-10:
        
        Content: "{content}"
        Theme: {theme}
        
        Consider:
        - Brand alignment (professional, data-driven, helpful)
        - Engagement potential
        - Value to restaurant owners
        - Viral potential
        - Professional standards
        
        Return only a number between 0-10, no explanation.
        """
        
        try:
            provider = self.ai_provider.providers[voter_name]
            content_request = ContentRequest(
                content_type=ContentType.ANALYSIS,
                platform="internal",
                context={"prompt": prompt},
                max_length=10,
                tone="analytical"
            )
            
            if hasattr(provider, 'generate_content'):
                response = await provider.generate_content(content_request)
                response_text = response.text if hasattr(response, 'text') else str(response)
            else:
                response_text = await self._fallback_vote_generation(prompt)
            
            # Extract number from response
            import re
            numbers = re.findall(r'\d+\.?\d*', response_text)
            if numbers:
                return min(float(numbers[0]), 10.0)
            else:
                return 5.0
                
        except Exception as e:
            self.logger.error(f"Error rating content with {voter_name}: {e}")
            return 5.0

    def _update_stats(self, decision: CouncilDecision) -> None:
        """Update council performance statistics"""
        
        self.council_stats["decisions_made"] += 1
        
        # Check for unanimous decisions
        if len(set(vote.vote for vote in decision.votes)) == 1:
            self.council_stats["unanimous_decisions"] += 1
        else:
            self.council_stats["split_decisions"] += 1
        
        # Track successful outcomes (approved or high-scoring modifications)
        if decision.final_decision == VoteType.APPROVE or (
            decision.final_decision == VoteType.MODIFY and decision.consensus_score >= 7.0
        ):
            self.council_stats["successful_outcomes"] += 1

    def get_council_performance(self) -> Dict[str, Any]:
        """Get AI council performance metrics"""
        
        total_decisions = self.council_stats["decisions_made"]
        
        return {
            "total_decisions": total_decisions,
            "unanimous_rate": (self.council_stats["unanimous_decisions"] / max(total_decisions, 1)) * 100,
            "success_rate": (self.council_stats["successful_outcomes"] / max(total_decisions, 1)) * 100,
            "average_consensus": sum(d.consensus_score for d in self.decision_history) / max(len(self.decision_history), 1),
            "council_members_active": len([
                name for name in self.council_config["council_members"].keys()
                if name in self.ai_provider.providers and self.ai_provider.providers[name].is_available
            ]),
            "recent_decisions": [
                {
                    "id": d.decision_id,
                    "type": d.decision_type.value,
                    "decision": d.final_decision.value,
                    "consensus": d.consensus_score,
                    "timestamp": d.timestamp.isoformat()
                }
                for d in self.decision_history[-5:]  # Last 5 decisions
            ]
        }
