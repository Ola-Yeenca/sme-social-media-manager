"""
AI Agent module for SME Analytica
Intelligent engagement automation with continuous monitoring and AI-powered responses
"""

from .intelligent_engagement_agent import (
    IntelligentEngagementAgent,
    EngagementContext,
    AIResponse,
    OpportunityType,
    AgentMode,
    create_intelligent_agent
)

__all__ = [
    'IntelligentEngagementAgent',
    'EngagementContext', 
    'AIResponse',
    'OpportunityType',
    'AgentMode',
    'create_intelligent_agent'
]
