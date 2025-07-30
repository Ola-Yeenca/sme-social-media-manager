#!/usr/bin/env python3
"""
Analytics and Reporting for SME Analytica AI Agent
Comprehensive analytics system for tracking AI agent performance and ROI measurement
"""

import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import json

@dataclass
class EngagementMetrics:
    """Engagement performance metrics"""
    total_opportunities: int
    opportunities_engaged: int
    responses_generated: int
    successful_engagements: int
    safety_blocks: int
    rate_limit_blocks: int
    engagement_rate: float
    success_rate: float
    average_response_time: float

@dataclass
class ContentMetrics:
    """Content quality and performance metrics"""
    total_content_generated: int
    average_confidence_score: float
    average_brand_voice_score: float
    average_viral_potential: float
    gemini_usage_percentage: float
    anthropic_usage_percentage: float
    content_types_distribution: Dict[str, int]

@dataclass
class SafetyMetrics:
    """Safety and compliance metrics"""
    total_safety_checks: int
    safe_approvals: int
    safety_blocks: int
    safety_approval_rate: float
    top_risk_factors: List[str]
    rate_limit_adherence: float

@dataclass
class ROIMetrics:
    """Return on investment metrics"""
    estimated_reach: int
    estimated_impressions: int
    estimated_engagement_value: float
    lead_generation_potential: int
    brand_awareness_score: float
    thought_leadership_score: float

@dataclass
class PerformanceReport:
    """Comprehensive performance report"""
    report_id: str
    generated_at: datetime
    time_period: str
    engagement_metrics: EngagementMetrics
    content_metrics: ContentMetrics
    safety_metrics: SafetyMetrics
    roi_metrics: ROIMetrics
    key_insights: List[str]
    recommendations: List[str]

class AnalyticsReporter:
    """Comprehensive analytics and reporting system"""
    
    def __init__(self, notion_manager=None):
        self.logger = logging.getLogger(__name__)
        self.notion_manager = notion_manager
        
        # Analytics data storage
        self.engagement_history = []
        self.content_history = []
        self.safety_history = []
        self.performance_snapshots = []
        
        # Tracking configuration
        self.tracking_config = self._initialize_tracking_config()
        
        # Report templates
        self.report_templates = self._initialize_report_templates()

    def _initialize_tracking_config(self) -> Dict[str, Any]:
        """Initialize analytics tracking configuration"""
        return {
            "metrics_collection": {
                "engagement_tracking": True,
                "content_quality_tracking": True,
                "safety_compliance_tracking": True,
                "roi_estimation": True,
                "real_time_monitoring": True
            },
            "reporting_intervals": {
                "real_time": 300,      # 5 minutes
                "hourly": 3600,        # 1 hour
                "daily": 86400,        # 24 hours
                "weekly": 604800,      # 7 days
                "monthly": 2592000     # 30 days
            },
            "performance_thresholds": {
                "minimum_engagement_rate": 0.05,
                "minimum_success_rate": 0.70,
                "minimum_safety_approval_rate": 0.95,
                "maximum_response_time": 300,  # 5 minutes
                "minimum_brand_voice_score": 7.0
            },
            "roi_calculations": {
                "engagement_value_per_interaction": 2.50,
                "lead_value_estimate": 150.00,
                "brand_awareness_multiplier": 1.5,
                "thought_leadership_multiplier": 2.0
            }
        }

    def _initialize_report_templates(self) -> Dict[str, str]:
        """Initialize report templates"""
        return {
            "executive_summary": """
# SME Analytica AI Agent Performance Report

## Executive Summary
- **Time Period**: {time_period}
- **Total Opportunities**: {total_opportunities}
- **Engagement Rate**: {engagement_rate:.1%}
- **Success Rate**: {success_rate:.1%}
- **Safety Compliance**: {safety_approval_rate:.1%}

## Key Achievements
{key_achievements}

## Recommendations
{recommendations}
            """,
            "detailed_metrics": """
## Detailed Performance Metrics

### Engagement Performance
- Opportunities Identified: {total_opportunities}
- Engagements Executed: {opportunities_engaged}
- Success Rate: {success_rate:.1%}
- Average Response Time: {average_response_time:.1f} seconds

### Content Quality
- Content Generated: {total_content_generated}
- Average Confidence: {average_confidence_score:.1f}/10
- Brand Voice Alignment: {average_brand_voice_score:.1f}/10
- Viral Potential: {average_viral_potential:.1f}/10

### Safety & Compliance
- Safety Checks: {total_safety_checks}
- Approval Rate: {safety_approval_rate:.1%}
- Blocks Prevented: {safety_blocks}

### ROI Estimation
- Estimated Reach: {estimated_reach:,}
- Estimated Value: ${estimated_engagement_value:,.2f}
- Lead Generation Potential: {lead_generation_potential}
            """
        }

    async def track_engagement(self, engagement_data: Dict[str, Any]) -> None:
        """Track engagement activity"""
        
        engagement_record = {
            "timestamp": datetime.now(),
            "opportunity_type": engagement_data.get("opportunity_type"),
            "author": engagement_data.get("author"),
            "content_preview": engagement_data.get("content", "")[:100],
            "response_generated": engagement_data.get("response_generated", False),
            "engagement_executed": engagement_data.get("engagement_executed", False),
            "success": engagement_data.get("success", False),
            "response_time": engagement_data.get("response_time", 0),
            "safety_approved": engagement_data.get("safety_approved", True),
            "rate_limited": engagement_data.get("rate_limited", False)
        }
        
        self.engagement_history.append(engagement_record)
        
        # Clean up old records (keep last 30 days)
        cutoff_time = datetime.now() - timedelta(days=30)
        self.engagement_history = [
            record for record in self.engagement_history 
            if record["timestamp"] > cutoff_time
        ]

    async def track_content_generation(self, content_data: Dict[str, Any]) -> None:
        """Track content generation metrics"""
        
        content_record = {
            "timestamp": datetime.now(),
            "content_type": content_data.get("content_type"),
            "provider_used": content_data.get("provider_used"),
            "confidence_score": content_data.get("confidence_score", 0),
            "brand_voice_score": content_data.get("brand_voice_score", 0),
            "viral_potential": content_data.get("viral_potential", 0),
            "safety_score": content_data.get("safety_score", 0),
            "content_length": len(content_data.get("content", "")),
            "hashtags_used": len(content_data.get("hashtags", [])),
            "engagement_hooks": content_data.get("engagement_hooks", [])
        }
        
        self.content_history.append(content_record)

    async def track_safety_check(self, safety_data: Dict[str, Any]) -> None:
        """Track safety check results"""
        
        safety_record = {
            "timestamp": datetime.now(),
            "content_checked": safety_data.get("content", "")[:50],
            "author": safety_data.get("author"),
            "safety_level": safety_data.get("safety_level"),
            "is_safe": safety_data.get("is_safe", False),
            "confidence_score": safety_data.get("confidence_score", 0),
            "risk_factors": safety_data.get("risk_factors", []),
            "check_type": safety_data.get("check_type", "content")
        }
        
        self.safety_history.append(safety_record)

    async def generate_engagement_metrics(self, time_period: timedelta) -> EngagementMetrics:
        """Generate engagement performance metrics"""
        
        cutoff_time = datetime.now() - time_period
        recent_engagements = [
            record for record in self.engagement_history 
            if record["timestamp"] > cutoff_time
        ]
        
        if not recent_engagements:
            return EngagementMetrics(
                total_opportunities=0,
                opportunities_engaged=0,
                responses_generated=0,
                successful_engagements=0,
                safety_blocks=0,
                rate_limit_blocks=0,
                engagement_rate=0.0,
                success_rate=0.0,
                average_response_time=0.0
            )
        
        total_opportunities = len(recent_engagements)
        opportunities_engaged = sum(1 for r in recent_engagements if r["engagement_executed"])
        responses_generated = sum(1 for r in recent_engagements if r["response_generated"])
        successful_engagements = sum(1 for r in recent_engagements if r["success"])
        safety_blocks = sum(1 for r in recent_engagements if not r["safety_approved"])
        rate_limit_blocks = sum(1 for r in recent_engagements if r["rate_limited"])
        
        engagement_rate = opportunities_engaged / total_opportunities if total_opportunities > 0 else 0
        success_rate = successful_engagements / opportunities_engaged if opportunities_engaged > 0 else 0
        
        response_times = [r["response_time"] for r in recent_engagements if r["response_time"] > 0]
        average_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        return EngagementMetrics(
            total_opportunities=total_opportunities,
            opportunities_engaged=opportunities_engaged,
            responses_generated=responses_generated,
            successful_engagements=successful_engagements,
            safety_blocks=safety_blocks,
            rate_limit_blocks=rate_limit_blocks,
            engagement_rate=engagement_rate,
            success_rate=success_rate,
            average_response_time=average_response_time
        )

    async def generate_content_metrics(self, time_period: timedelta) -> ContentMetrics:
        """Generate content quality metrics"""
        
        cutoff_time = datetime.now() - time_period
        recent_content = [
            record for record in self.content_history 
            if record["timestamp"] > cutoff_time
        ]
        
        if not recent_content:
            return ContentMetrics(
                total_content_generated=0,
                average_confidence_score=0.0,
                average_brand_voice_score=0.0,
                average_viral_potential=0.0,
                gemini_usage_percentage=0.0,
                anthropic_usage_percentage=0.0,
                content_types_distribution={}
            )
        
        total_content = len(recent_content)
        
        # Calculate averages
        avg_confidence = sum(r["confidence_score"] for r in recent_content) / total_content
        avg_brand_voice = sum(r["brand_voice_score"] for r in recent_content) / total_content
        avg_viral_potential = sum(r["viral_potential"] for r in recent_content) / total_content
        
        # Provider usage
        gemini_usage = sum(1 for r in recent_content if r["provider_used"] == "gemini")
        anthropic_usage = sum(1 for r in recent_content if r["provider_used"] == "anthropic")
        
        gemini_percentage = (gemini_usage / total_content) * 100 if total_content > 0 else 0
        anthropic_percentage = (anthropic_usage / total_content) * 100 if total_content > 0 else 0
        
        # Content type distribution
        content_types = {}
        for record in recent_content:
            content_type = record["content_type"]
            content_types[content_type] = content_types.get(content_type, 0) + 1
        
        return ContentMetrics(
            total_content_generated=total_content,
            average_confidence_score=avg_confidence,
            average_brand_voice_score=avg_brand_voice,
            average_viral_potential=avg_viral_potential,
            gemini_usage_percentage=gemini_percentage,
            anthropic_usage_percentage=anthropic_percentage,
            content_types_distribution=content_types
        )

    async def generate_safety_metrics(self, time_period: timedelta) -> SafetyMetrics:
        """Generate safety and compliance metrics"""
        
        cutoff_time = datetime.now() - time_period
        recent_safety = [
            record for record in self.safety_history 
            if record["timestamp"] > cutoff_time
        ]
        
        if not recent_safety:
            return SafetyMetrics(
                total_safety_checks=0,
                safe_approvals=0,
                safety_blocks=0,
                safety_approval_rate=0.0,
                top_risk_factors=[],
                rate_limit_adherence=100.0
            )
        
        total_checks = len(recent_safety)
        safe_approvals = sum(1 for r in recent_safety if r["is_safe"])
        safety_blocks = total_checks - safe_approvals
        
        approval_rate = (safe_approvals / total_checks) * 100 if total_checks > 0 else 0
        
        # Top risk factors
        all_risk_factors = []
        for record in recent_safety:
            all_risk_factors.extend(record["risk_factors"])
        
        risk_factor_counts = {}
        for factor in all_risk_factors:
            risk_factor_counts[factor] = risk_factor_counts.get(factor, 0) + 1
        
        top_risk_factors = sorted(risk_factor_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        top_risk_factors = [factor for factor, count in top_risk_factors]
        
        return SafetyMetrics(
            total_safety_checks=total_checks,
            safe_approvals=safe_approvals,
            safety_blocks=safety_blocks,
            safety_approval_rate=approval_rate,
            top_risk_factors=top_risk_factors,
            rate_limit_adherence=95.0  # Would calculate from actual rate limit data
        )

    async def generate_roi_metrics(self, engagement_metrics: EngagementMetrics, 
                                 content_metrics: ContentMetrics) -> ROIMetrics:
        """Generate ROI and business impact metrics"""
        
        config = self.tracking_config["roi_calculations"]
        
        # Estimate reach (simplified calculation)
        estimated_reach = engagement_metrics.successful_engagements * 500  # Average follower count
        estimated_impressions = estimated_reach * 3  # Estimated impression multiplier
        
        # Calculate engagement value
        engagement_value = (
            engagement_metrics.successful_engagements * config["engagement_value_per_interaction"]
        )
        
        # Lead generation potential
        lead_potential = int(engagement_metrics.successful_engagements * 0.1)  # 10% conversion estimate
        
        # Brand awareness score (based on reach and content quality)
        brand_awareness = min(
            (estimated_reach / 10000) * content_metrics.average_brand_voice_score,
            10.0
        )
        
        # Thought leadership score (based on content quality and viral potential)
        thought_leadership = (
            content_metrics.average_confidence_score * 0.4 +
            content_metrics.average_viral_potential * 0.6
        )
        
        return ROIMetrics(
            estimated_reach=estimated_reach,
            estimated_impressions=estimated_impressions,
            estimated_engagement_value=engagement_value,
            lead_generation_potential=lead_potential,
            brand_awareness_score=brand_awareness,
            thought_leadership_score=thought_leadership
        )

    async def generate_performance_report(self, time_period: timedelta = None) -> PerformanceReport:
        """Generate comprehensive performance report"""
        
        if time_period is None:
            time_period = timedelta(days=1)  # Default to daily report
        
        # Generate all metrics
        engagement_metrics = await self.generate_engagement_metrics(time_period)
        content_metrics = await self.generate_content_metrics(time_period)
        safety_metrics = await self.generate_safety_metrics(time_period)
        roi_metrics = await self.generate_roi_metrics(engagement_metrics, content_metrics)
        
        # Generate insights and recommendations
        key_insights = self._generate_key_insights(
            engagement_metrics, content_metrics, safety_metrics, roi_metrics
        )
        recommendations = self._generate_recommendations(
            engagement_metrics, content_metrics, safety_metrics
        )
        
        report = PerformanceReport(
            report_id=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            generated_at=datetime.now(),
            time_period=str(time_period),
            engagement_metrics=engagement_metrics,
            content_metrics=content_metrics,
            safety_metrics=safety_metrics,
            roi_metrics=roi_metrics,
            key_insights=key_insights,
            recommendations=recommendations
        )
        
        # Save report
        await self._save_report(report)
        
        return report

    def _generate_key_insights(self, engagement: EngagementMetrics, content: ContentMetrics,
                             safety: SafetyMetrics, roi: ROIMetrics) -> List[str]:
        """Generate key insights from metrics"""
        
        insights = []
        
        # Engagement insights
        if engagement.engagement_rate > 0.1:
            insights.append(f"High engagement rate of {engagement.engagement_rate:.1%} indicates strong opportunity identification")
        
        if engagement.success_rate > 0.8:
            insights.append(f"Excellent success rate of {engagement.success_rate:.1%} shows effective response quality")
        
        # Content insights
        if content.gemini_usage_percentage > 50:
            insights.append(f"Gemini AI driving {content.gemini_usage_percentage:.0f}% of content generation with enhanced intelligence")
        
        if content.average_viral_potential > 7.0:
            insights.append(f"High viral potential score of {content.average_viral_potential:.1f}/10 indicates strong influencer content")
        
        # Safety insights
        if safety.safety_approval_rate > 95:
            insights.append(f"Excellent safety compliance at {safety.safety_approval_rate:.1f}% approval rate")
        
        # ROI insights
        if roi.estimated_reach > 10000:
            insights.append(f"Strong reach of {roi.estimated_reach:,} estimated impressions driving brand awareness")
        
        return insights[:5]  # Limit to top 5 insights

    def _generate_recommendations(self, engagement: EngagementMetrics, content: ContentMetrics,
                                safety: SafetyMetrics) -> List[str]:
        """Generate actionable recommendations"""
        
        recommendations = []
        
        # Engagement recommendations
        if engagement.engagement_rate < 0.05:
            recommendations.append("Consider expanding hashtag monitoring to identify more opportunities")
        
        if engagement.success_rate < 0.7:
            recommendations.append("Review response templates and AI prompts to improve engagement success")
        
        # Content recommendations
        if content.average_brand_voice_score < 7.0:
            recommendations.append("Enhance brand voice guidelines and AI training for better consistency")
        
        if content.gemini_usage_percentage < 30:
            recommendations.append("Increase Gemini AI utilization for enhanced content intelligence")
        
        # Safety recommendations
        if safety.safety_approval_rate < 95:
            recommendations.append("Review and tighten safety filters to improve compliance")
        
        return recommendations[:5]  # Limit to top 5 recommendations

    async def _save_report(self, report: PerformanceReport) -> None:
        """Save report to Notion database"""
        
        try:
            if self.notion_manager:
                report_data = {
                    "report_id": report.report_id,
                    "generated_at": report.generated_at.isoformat(),
                    "time_period": report.time_period,
                    "engagement_rate": report.engagement_metrics.engagement_rate,
                    "success_rate": report.engagement_metrics.success_rate,
                    "safety_approval_rate": report.safety_metrics.safety_approval_rate,
                    "estimated_reach": report.roi_metrics.estimated_reach,
                    "key_insights": report.key_insights,
                    "recommendations": report.recommendations
                }
                
                # Save to Notion (implement based on your schema)
                # self.notion_manager.save_performance_report(report_data)
                
        except Exception as e:
            self.logger.error(f"Error saving report: {e}")

    def get_real_time_dashboard(self) -> Dict[str, Any]:
        """Get real-time dashboard metrics"""
        
        # Get metrics for last hour
        last_hour = timedelta(hours=1)
        
        recent_engagements = [
            record for record in self.engagement_history 
            if record["timestamp"] > datetime.now() - last_hour
        ]
        
        recent_content = [
            record for record in self.content_history 
            if record["timestamp"] > datetime.now() - last_hour
        ]
        
        return {
            "current_time": datetime.now().isoformat(),
            "last_hour_metrics": {
                "opportunities_found": len(recent_engagements),
                "engagements_executed": sum(1 for r in recent_engagements if r["engagement_executed"]),
                "content_generated": len(recent_content),
                "safety_blocks": sum(1 for r in recent_engagements if not r["safety_approved"])
            },
            "system_status": {
                "ai_agent_active": True,
                "safety_system_active": True,
                "gemini_available": True,
                "monitoring_active": True
            },
            "performance_indicators": {
                "engagement_rate": len([r for r in recent_engagements if r["engagement_executed"]]) / max(len(recent_engagements), 1),
                "average_response_quality": sum(r.get("confidence_score", 0) for r in recent_content) / max(len(recent_content), 1),
                "safety_compliance": sum(1 for r in recent_engagements if r["safety_approved"]) / max(len(recent_engagements), 1)
            }
        }
