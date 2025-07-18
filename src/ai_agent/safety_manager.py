#!/usr/bin/env python3
"""
Safety Manager for SME Analytica AI Agent
Comprehensive safety measures, rate limiting, and spam prevention for authentic engagement
"""

import logging
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import json
import re

class SafetyLevel(str, Enum):
    SAFE = "safe"
    CAUTION = "caution"
    UNSAFE = "unsafe"
    BLOCKED = "blocked"

class RateLimitType(str, Enum):
    HOURLY_RESPONSES = "hourly_responses"
    DAILY_RESPONSES = "daily_responses"
    WEEKLY_RESPONSES = "weekly_responses"
    MENTIONS_PER_HOUR = "mentions_per_hour"
    HASHTAG_ENGAGEMENTS = "hashtag_engagements"
    SAME_AUTHOR_LIMIT = "same_author_limit"

@dataclass
class SafetyCheck:
    """Safety check result"""
    is_safe: bool
    safety_level: SafetyLevel
    confidence_score: float
    risk_factors: List[str]
    recommendations: List[str]
    reasoning: str

@dataclass
class RateLimitStatus:
    """Rate limit status"""
    limit_type: RateLimitType
    current_count: int
    limit_threshold: int
    time_window: str
    is_exceeded: bool
    reset_time: datetime

class SafetyManager:
    """Comprehensive safety and rate limiting manager"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Safety configuration
        self.safety_config = self._initialize_safety_config()
        self.rate_limits = self._initialize_rate_limits()
        self.blocked_patterns = self._initialize_blocked_patterns()
        
        # Tracking data
        self.engagement_history = []
        self.author_interactions = {}
        self.daily_stats = {}
        self.safety_violations = []
        
        # Current session tracking
        self.session_start = datetime.now()
        self.session_stats = {
            "total_checks": 0,
            "safe_approvals": 0,
            "safety_blocks": 0,
            "rate_limit_blocks": 0
        }

    def _initialize_safety_config(self) -> Dict[str, Any]:
        """Initialize comprehensive safety configuration"""
        return {
            "content_safety": {
                "prohibited_topics": [
                    "politics", "religion", "personal_attacks", "harassment",
                    "discrimination", "hate_speech", "violence", "illegal_activities",
                    "spam", "scams", "misinformation", "adult_content"
                ],
                "sensitive_topics": [
                    "controversial_opinions", "competitor_criticism", "pricing_complaints",
                    "negative_reviews", "legal_issues", "financial_advice"
                ],
                "brand_risks": [
                    "overly_promotional", "pushy_sales", "false_claims",
                    "unsubstantiated_promises", "competitor_bashing"
                ]
            },
            "author_safety": {
                "minimum_account_age_days": 30,
                "minimum_followers": 10,
                "maximum_followers_following_ratio": 10.0,
                "blocked_account_types": ["spam", "bot", "fake", "suspended"],
                "verified_account_bonus": True
            },
            "content_quality": {
                "minimum_content_length": 10,
                "maximum_content_length": 2000,
                "minimum_engagement_threshold": 1,
                "spam_indicators": [
                    "excessive_caps", "excessive_emojis", "repeated_characters",
                    "suspicious_links", "promotional_language"
                ]
            },
            "response_safety": {
                "avoid_controversial_stances": True,
                "require_value_addition": True,
                "maintain_professional_tone": True,
                "fact_check_claims": True
            }
        }

    def _initialize_rate_limits(self) -> Dict[RateLimitType, Dict[str, Any]]:
        """Initialize rate limiting configuration"""
        return {
            RateLimitType.HOURLY_RESPONSES: {
                "limit": 5,
                "window_hours": 1,
                "description": "Maximum responses per hour"
            },
            RateLimitType.DAILY_RESPONSES: {
                "limit": 25,
                "window_hours": 24,
                "description": "Maximum responses per day"
            },
            RateLimitType.WEEKLY_RESPONSES: {
                "limit": 150,
                "window_hours": 168,
                "description": "Maximum responses per week"
            },
            RateLimitType.MENTIONS_PER_HOUR: {
                "limit": 10,
                "window_hours": 1,
                "description": "Maximum mention responses per hour"
            },
            RateLimitType.HASHTAG_ENGAGEMENTS: {
                "limit": 15,
                "window_hours": 1,
                "description": "Maximum hashtag engagements per hour"
            },
            RateLimitType.SAME_AUTHOR_LIMIT: {
                "limit": 2,
                "window_hours": 24,
                "description": "Maximum responses to same author per day"
            }
        }

    def _initialize_blocked_patterns(self) -> Dict[str, List[str]]:
        """Initialize blocked content patterns"""
        return {
            "spam_patterns": [
                r"buy now", r"limited time", r"act fast", r"exclusive offer",
                r"guaranteed", r"100% free", r"click here", r"urgent"
            ],
            "promotional_patterns": [
                r"special deal", r"discount", r"sale", r"promo code",
                r"limited offer", r"best price", r"cheap", r"free trial"
            ],
            "suspicious_patterns": [
                r"dm me", r"check my bio", r"link in bio", r"follow for follow",
                r"f4f", r"follow back", r"mutual follow"
            ],
            "inappropriate_patterns": [
                r"hate", r"stupid", r"idiot", r"scam", r"fake",
                r"worst", r"terrible", r"awful", r"disgusting"
            ]
        }

    async def check_content_safety(self, content: str, author: str, 
                                 context: Dict[str, Any] = None) -> SafetyCheck:
        """Comprehensive content safety check"""
        
        try:
            self.session_stats["total_checks"] += 1
            
            risk_factors = []
            recommendations = []
            safety_level = SafetyLevel.SAFE
            confidence_score = 0.9
            
            # Content analysis
            content_risks = self._analyze_content_safety(content)
            risk_factors.extend(content_risks)
            
            # Author analysis
            author_risks = await self._analyze_author_safety(author, context or {})
            risk_factors.extend(author_risks)
            
            # Pattern matching
            pattern_risks = self._check_blocked_patterns(content)
            risk_factors.extend(pattern_risks)
            
            # Context analysis
            if context:
                context_risks = self._analyze_context_safety(context)
                risk_factors.extend(context_risks)
            
            # Determine safety level
            if len(risk_factors) == 0:
                safety_level = SafetyLevel.SAFE
                confidence_score = 0.95
            elif len(risk_factors) <= 2:
                safety_level = SafetyLevel.CAUTION
                confidence_score = 0.7
                recommendations.append("Proceed with careful monitoring")
            elif len(risk_factors) <= 4:
                safety_level = SafetyLevel.UNSAFE
                confidence_score = 0.4
                recommendations.append("Consider avoiding engagement")
            else:
                safety_level = SafetyLevel.BLOCKED
                confidence_score = 0.1
                recommendations.append("Block engagement immediately")
            
            # Generate reasoning
            reasoning = self._generate_safety_reasoning(risk_factors, safety_level)
            
            # Update statistics
            is_safe = safety_level in [SafetyLevel.SAFE, SafetyLevel.CAUTION]
            if is_safe:
                self.session_stats["safe_approvals"] += 1
            else:
                self.session_stats["safety_blocks"] += 1
                self.safety_violations.append({
                    "timestamp": datetime.now(),
                    "content": content[:100],
                    "author": author,
                    "risk_factors": risk_factors,
                    "safety_level": safety_level.value
                })
            
            return SafetyCheck(
                is_safe=is_safe,
                safety_level=safety_level,
                confidence_score=confidence_score,
                risk_factors=risk_factors,
                recommendations=recommendations,
                reasoning=reasoning
            )
            
        except Exception as e:
            self.logger.error(f"Error in safety check: {e}")
            return SafetyCheck(
                is_safe=False,
                safety_level=SafetyLevel.BLOCKED,
                confidence_score=0.0,
                risk_factors=["safety_check_error"],
                recommendations=["Block due to safety check failure"],
                reasoning=f"Safety check failed: {e}"
            )

    def _analyze_content_safety(self, content: str) -> List[str]:
        """Analyze content for safety risks"""
        risks = []
        content_lower = content.lower()
        
        # Check prohibited topics
        prohibited = self.safety_config["content_safety"]["prohibited_topics"]
        for topic in prohibited:
            if topic in content_lower:
                risks.append(f"prohibited_topic_{topic}")
        
        # Check sensitive topics
        sensitive = self.safety_config["content_safety"]["sensitive_topics"]
        for topic in sensitive:
            if topic.replace("_", " ") in content_lower:
                risks.append(f"sensitive_topic_{topic}")
        
        # Check content quality
        if len(content) < self.safety_config["content_quality"]["minimum_content_length"]:
            risks.append("content_too_short")
        
        if len(content) > self.safety_config["content_quality"]["maximum_content_length"]:
            risks.append("content_too_long")
        
        # Check for excessive caps
        caps_ratio = sum(1 for c in content if c.isupper()) / max(len(content), 1)
        if caps_ratio > 0.5:
            risks.append("excessive_caps")
        
        # Check for excessive emojis
        emoji_count = len(re.findall(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]', content))
        if emoji_count > 5:
            risks.append("excessive_emojis")
        
        return risks

    async def _analyze_author_safety(self, author: str, context: Dict[str, Any]) -> List[str]:
        """Analyze author for safety risks"""
        risks = []
        
        # Check author profile if available
        author_profile = context.get("author_profile", {})
        
        # Check minimum followers
        followers = author_profile.get("followers", 0)
        if followers < self.safety_config["author_safety"]["minimum_followers"]:
            risks.append("low_follower_count")
        
        # Check followers/following ratio
        following = author_profile.get("following", 1)
        ratio = following / max(followers, 1)
        if ratio > self.safety_config["author_safety"]["maximum_followers_following_ratio"]:
            risks.append("suspicious_follow_ratio")
        
        # Check account age (if available)
        created_at = author_profile.get("created_at")
        if created_at:
            try:
                account_age = (datetime.now() - created_at).days
                if account_age < self.safety_config["author_safety"]["minimum_account_age_days"]:
                    risks.append("new_account")
            except:
                pass
        
        # Check for blocked account types
        account_type = author_profile.get("account_type", "").lower()
        blocked_types = self.safety_config["author_safety"]["blocked_account_types"]
        if account_type in blocked_types:
            risks.append(f"blocked_account_type_{account_type}")
        
        # Check interaction history
        if author in self.author_interactions:
            interactions = self.author_interactions[author]
            recent_interactions = [
                i for i in interactions 
                if i["timestamp"] > datetime.now() - timedelta(hours=24)
            ]
            if len(recent_interactions) >= 3:
                risks.append("excessive_author_interaction")
        
        return risks

    def _check_blocked_patterns(self, content: str) -> List[str]:
        """Check content against blocked patterns"""
        risks = []
        content_lower = content.lower()
        
        for category, patterns in self.blocked_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content_lower):
                    risks.append(f"blocked_pattern_{category}")
                    break  # One match per category is enough
        
        return risks

    def _analyze_context_safety(self, context: Dict[str, Any]) -> List[str]:
        """Analyze context for safety risks"""
        risks = []
        
        # Check for competitive context
        if context.get("competitive_context"):
            risks.append("competitive_context")
        
        # Check for trending context that might be controversial
        trending = context.get("trending_context", "").lower()
        controversial_trends = ["drama", "controversy", "scandal", "fight"]
        if any(word in trending for word in controversial_trends):
            risks.append("controversial_trending_topic")
        
        # Check engagement metrics for potential spam
        existing_engagement = context.get("existing_engagement", 0)
        if existing_engagement > 1000:  # Very high engagement might indicate viral/controversial content
            risks.append("high_engagement_content")
        
        return risks

    def _generate_safety_reasoning(self, risk_factors: List[str], 
                                 safety_level: SafetyLevel) -> str:
        """Generate human-readable safety reasoning"""
        
        if not risk_factors:
            return "Content passed all safety checks. No risk factors identified."
        
        risk_descriptions = {
            "prohibited_topic": "Contains prohibited topic",
            "sensitive_topic": "Contains sensitive topic",
            "content_too_short": "Content is too short",
            "content_too_long": "Content is too long",
            "excessive_caps": "Excessive use of capital letters",
            "excessive_emojis": "Excessive use of emojis",
            "low_follower_count": "Author has very few followers",
            "suspicious_follow_ratio": "Author has suspicious follower/following ratio",
            "new_account": "Author account is very new",
            "blocked_account_type": "Author account type is blocked",
            "excessive_author_interaction": "Too many recent interactions with this author",
            "blocked_pattern": "Contains blocked content patterns",
            "competitive_context": "Content involves competitors",
            "controversial_trending_topic": "Related to controversial trending topic",
            "high_engagement_content": "Content has unusually high engagement"
        }
        
        descriptions = []
        for risk in risk_factors:
            for key, desc in risk_descriptions.items():
                if risk.startswith(key):
                    descriptions.append(desc)
                    break
        
        reasoning = f"Safety level: {safety_level.value}. "
        if descriptions:
            reasoning += f"Risk factors: {', '.join(descriptions[:3])}"
            if len(descriptions) > 3:
                reasoning += f" and {len(descriptions) - 3} more"
        
        return reasoning

    async def check_rate_limits(self, engagement_type: str = "response") -> List[RateLimitStatus]:
        """Check all applicable rate limits"""
        
        statuses = []
        current_time = datetime.now()
        
        for limit_type, config in self.rate_limits.items():
            # Calculate time window
            window_start = current_time - timedelta(hours=config["window_hours"])
            
            # Count recent engagements
            recent_count = self._count_recent_engagements(
                engagement_type, window_start, limit_type
            )
            
            # Check if limit is exceeded
            is_exceeded = recent_count >= config["limit"]
            
            # Calculate reset time
            reset_time = self._calculate_reset_time(limit_type, config)
            
            status = RateLimitStatus(
                limit_type=limit_type,
                current_count=recent_count,
                limit_threshold=config["limit"],
                time_window=f"{config['window_hours']} hours",
                is_exceeded=is_exceeded,
                reset_time=reset_time
            )
            
            statuses.append(status)
            
            if is_exceeded:
                self.session_stats["rate_limit_blocks"] += 1
        
        return statuses

    def _count_recent_engagements(self, engagement_type: str, 
                                window_start: datetime, limit_type: RateLimitType) -> int:
        """Count recent engagements for rate limiting"""
        
        count = 0
        
        for engagement in self.engagement_history:
            if engagement["timestamp"] < window_start:
                continue
            
            # Type-specific counting logic
            if limit_type == RateLimitType.SAME_AUTHOR_LIMIT:
                # Count engagements with the same author
                if engagement.get("author") == engagement_type:  # engagement_type used as author here
                    count += 1
            elif limit_type == RateLimitType.MENTIONS_PER_HOUR:
                if engagement.get("type") == "mention":
                    count += 1
            elif limit_type == RateLimitType.HASHTAG_ENGAGEMENTS:
                if engagement.get("type") == "hashtag":
                    count += 1
            else:
                # General response counting
                count += 1
        
        return count

    def _calculate_reset_time(self, limit_type: RateLimitType, 
                            config: Dict[str, Any]) -> datetime:
        """Calculate when rate limit resets"""
        
        current_time = datetime.now()
        
        if limit_type == RateLimitType.HOURLY_RESPONSES:
            return current_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        elif limit_type == RateLimitType.DAILY_RESPONSES:
            return current_time.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
        elif limit_type == RateLimitType.WEEKLY_RESPONSES:
            days_until_monday = (7 - current_time.weekday()) % 7
            return current_time.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=days_until_monday)
        else:
            return current_time + timedelta(hours=config["window_hours"])

    def record_engagement(self, engagement_type: str, author: str, 
                         content: str, success: bool) -> None:
        """Record engagement for rate limiting and safety tracking"""
        
        engagement_record = {
            "timestamp": datetime.now(),
            "type": engagement_type,
            "author": author,
            "content": content[:100],  # Truncate for storage
            "success": success
        }
        
        self.engagement_history.append(engagement_record)
        
        # Update author interaction history
        if author not in self.author_interactions:
            self.author_interactions[author] = []
        
        self.author_interactions[author].append(engagement_record)
        
        # Clean up old records (keep last 7 days)
        cutoff_time = datetime.now() - timedelta(days=7)
        self.engagement_history = [
            e for e in self.engagement_history 
            if e["timestamp"] > cutoff_time
        ]

    def get_safety_stats(self) -> Dict[str, Any]:
        """Get comprehensive safety statistics"""
        
        total_checks = self.session_stats["total_checks"]
        safe_rate = (self.session_stats["safe_approvals"] / max(total_checks, 1)) * 100
        
        return {
            "session_duration": str(datetime.now() - self.session_start),
            "total_safety_checks": total_checks,
            "safe_approvals": self.session_stats["safe_approvals"],
            "safety_blocks": self.session_stats["safety_blocks"],
            "rate_limit_blocks": self.session_stats["rate_limit_blocks"],
            "safety_approval_rate": round(safe_rate, 2),
            "total_engagements_recorded": len(self.engagement_history),
            "unique_authors_interacted": len(self.author_interactions),
            "recent_violations": len([
                v for v in self.safety_violations 
                if v["timestamp"] > datetime.now() - timedelta(hours=24)
            ])
        }

    async def is_engagement_safe(self, content: str, author: str, 
                               engagement_type: str = "response",
                               context: Dict[str, Any] = None) -> Tuple[bool, str]:
        """Comprehensive safety and rate limit check for engagement"""
        
        # Check content safety
        safety_check = await self.check_content_safety(content, author, context)
        
        if not safety_check.is_safe:
            return False, f"Safety check failed: {safety_check.reasoning}"
        
        # Check rate limits
        rate_limit_statuses = await self.check_rate_limits(engagement_type)
        
        exceeded_limits = [status for status in rate_limit_statuses if status.is_exceeded]
        if exceeded_limits:
            limit_descriptions = [f"{status.limit_type.value}" for status in exceeded_limits]
            return False, f"Rate limits exceeded: {', '.join(limit_descriptions)}"
        
        return True, "Engagement approved - all safety and rate limit checks passed"
