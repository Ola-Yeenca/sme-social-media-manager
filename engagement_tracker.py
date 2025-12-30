#!/usr/bin/env python3
"""
Engagement Tracker for SME Social Media Bot
Tracks post performance and learns from engagement data
"""

import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class PostRecord:
    """Record of a posted content with engagement metrics"""
    post_id: str
    platform: str  # 'twitter' or 'linkedin'
    industry: str
    content: str
    viral_score: float
    posted_at: str
    hashtags: List[str]

    # Engagement metrics (updated after posting)
    likes: int = 0
    retweets: int = 0
    replies: int = 0
    impressions: int = 0
    engagement_rate: float = 0.0

    # LinkedIn-specific
    reactions: int = 0
    comments: int = 0
    shares: int = 0
    views: int = 0

    # Analysis
    last_updated: str = ""
    performance_tier: str = ""  # 'viral', 'high', 'medium', 'low'

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict) -> 'PostRecord':
        return cls(**data)


class EngagementTracker:
    """Tracks and analyzes post engagement performance"""

    def __init__(self, storage_path: str = "post_history.json", industry: str = "general"):
        """
        Initialize engagement tracker

        Args:
            storage_path: Path to JSON file for persistence
            industry: Current industry for filtering analytics
        """
        self.storage_path = Path(storage_path)
        self.industry = industry
        self.posts: List[PostRecord] = []

        # Performance thresholds (engagement rate %)
        self.performance_tiers = {
            'viral': 5.0,    # 5%+ engagement rate
            'high': 2.0,     # 2-5%
            'medium': 0.5,   # 0.5-2%
            'low': 0.0       # <0.5%
        }

        # Load existing history
        self._load_history()

    def _load_history(self):
        """Load post history from storage"""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    self.posts = [PostRecord.from_dict(p) for p in data.get('posts', [])]
                    print(f"📊 Loaded {len(self.posts)} historical posts")
            except Exception as e:
                print(f"⚠️ Error loading post history: {e}")
                self.posts = []
        else:
            print("📊 Starting fresh post history")
            self.posts = []

    def _save_history(self):
        """Save post history to storage"""
        try:
            data = {
                'last_updated': datetime.utcnow().isoformat(),
                'total_posts': len(self.posts),
                'posts': [p.to_dict() for p in self.posts]
            }
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Error saving post history: {e}")

    def record_post(self, post_id: str, platform: str, content: str,
                    viral_score: float, hashtags: List[str] = None) -> PostRecord:
        """
        Record a new post

        Args:
            post_id: Platform-specific post ID
            platform: 'twitter' or 'linkedin'
            content: Posted content
            viral_score: Predicted viral score at time of posting
            hashtags: List of hashtags used

        Returns:
            PostRecord object
        """
        record = PostRecord(
            post_id=post_id,
            platform=platform,
            industry=self.industry,
            content=content,
            viral_score=viral_score,
            posted_at=datetime.utcnow().isoformat(),
            hashtags=hashtags or [],
            last_updated=datetime.utcnow().isoformat()
        )

        self.posts.append(record)
        self._save_history()

        print(f"📝 Recorded {platform} post: {post_id[:20]}...")
        return record

    def update_engagement(self, post_id: str, platform: str,
                          engagement_data: Dict) -> Optional[PostRecord]:
        """
        Update engagement metrics for a post

        Args:
            post_id: Platform-specific post ID
            platform: 'twitter' or 'linkedin'
            engagement_data: Dict with engagement metrics

        Returns:
            Updated PostRecord or None if not found
        """
        for post in self.posts:
            if post.post_id == post_id and post.platform == platform:
                # Update Twitter metrics
                if platform == 'twitter':
                    post.likes = engagement_data.get('likes', 0)
                    post.retweets = engagement_data.get('retweets', 0)
                    post.replies = engagement_data.get('replies', 0)
                    post.impressions = engagement_data.get('impressions', 1)

                    # Calculate engagement rate
                    total_engagement = post.likes + post.retweets + post.replies
                    post.engagement_rate = (total_engagement / max(post.impressions, 1)) * 100

                # Update LinkedIn metrics
                elif platform == 'linkedin':
                    post.reactions = engagement_data.get('reactions', 0)
                    post.comments = engagement_data.get('comments', 0)
                    post.shares = engagement_data.get('shares', 0)
                    post.views = engagement_data.get('views', 1)

                    # Calculate engagement rate
                    total_engagement = post.reactions + post.comments + post.shares
                    post.engagement_rate = (total_engagement / max(post.views, 1)) * 100

                # Determine performance tier
                post.performance_tier = self._get_performance_tier(post.engagement_rate)
                post.last_updated = datetime.utcnow().isoformat()

                self._save_history()
                print(f"📊 Updated {platform} post engagement: {post.engagement_rate:.2f}% ({post.performance_tier})")
                return post

        return None

    def _get_performance_tier(self, engagement_rate: float) -> str:
        """Determine performance tier based on engagement rate"""
        if engagement_rate >= self.performance_tiers['viral']:
            return 'viral'
        elif engagement_rate >= self.performance_tiers['high']:
            return 'high'
        elif engagement_rate >= self.performance_tiers['medium']:
            return 'medium'
        else:
            return 'low'

    def get_top_performers(self, limit: int = 10,
                           industry: str = None,
                           platform: str = None,
                           days: int = 30) -> List[PostRecord]:
        """
        Get top performing posts

        Args:
            limit: Maximum number of posts to return
            industry: Filter by industry (None = all)
            platform: Filter by platform (None = all)
            days: Only include posts from last N days

        Returns:
            List of top performing PostRecords
        """
        cutoff = datetime.utcnow() - timedelta(days=days)

        filtered = [
            p for p in self.posts
            if datetime.fromisoformat(p.posted_at) > cutoff
            and (industry is None or p.industry == industry)
            and (platform is None or p.platform == platform)
        ]

        # Sort by engagement rate
        filtered.sort(key=lambda x: x.engagement_rate, reverse=True)

        return filtered[:limit]

    def get_performance_insights(self, industry: str = None) -> Dict:
        """
        Get performance insights and recommendations

        Args:
            industry: Filter by industry (None = use self.industry)

        Returns:
            Dict with insights and recommendations
        """
        target_industry = industry or self.industry

        # Filter relevant posts
        industry_posts = [p for p in self.posts if p.industry == target_industry]

        if not industry_posts:
            return {
                'industry': target_industry,
                'total_posts': 0,
                'message': 'No posts recorded yet for this industry'
            }

        # Calculate metrics
        total_posts = len(industry_posts)
        avg_viral_score = sum(p.viral_score for p in industry_posts) / total_posts
        avg_engagement = sum(p.engagement_rate for p in industry_posts) / total_posts

        # Tier distribution
        tier_counts = {'viral': 0, 'high': 0, 'medium': 0, 'low': 0}
        for p in industry_posts:
            if p.performance_tier:
                tier_counts[p.performance_tier] = tier_counts.get(p.performance_tier, 0) + 1

        # Best performing hashtags
        hashtag_performance: Dict[str, List[float]] = {}
        for p in industry_posts:
            for tag in p.hashtags:
                if tag not in hashtag_performance:
                    hashtag_performance[tag] = []
                hashtag_performance[tag].append(p.engagement_rate)

        best_hashtags = sorted(
            [(tag, sum(rates)/len(rates)) for tag, rates in hashtag_performance.items() if len(rates) >= 2],
            key=lambda x: x[1],
            reverse=True
        )[:5]

        # Viral score correlation
        high_performers = [p for p in industry_posts if p.engagement_rate >= 2.0]
        low_performers = [p for p in industry_posts if p.engagement_rate < 0.5]

        viral_accuracy = 0.0
        if high_performers and low_performers:
            avg_hp_viral = sum(p.viral_score for p in high_performers) / len(high_performers)
            avg_lp_viral = sum(p.viral_score for p in low_performers) / len(low_performers)
            viral_accuracy = (avg_hp_viral - avg_lp_viral) / 100 * 100  # Percentage difference

        # Content patterns
        top_posts = sorted(industry_posts, key=lambda x: x.engagement_rate, reverse=True)[:5]
        content_patterns = self._analyze_content_patterns(top_posts)

        # Best posting times
        best_times = self._analyze_posting_times(industry_posts)

        return {
            'industry': target_industry,
            'total_posts': total_posts,
            'avg_viral_score': round(avg_viral_score, 1),
            'avg_engagement_rate': round(avg_engagement, 2),
            'tier_distribution': tier_counts,
            'best_hashtags': best_hashtags,
            'viral_prediction_accuracy': round(viral_accuracy, 1),
            'content_patterns': content_patterns,
            'best_posting_times': best_times,
            'recommendations': self._generate_recommendations(
                avg_engagement, tier_counts, best_hashtags, content_patterns
            )
        }

    def _analyze_content_patterns(self, top_posts: List[PostRecord]) -> Dict:
        """Analyze patterns in top performing content"""
        if not top_posts:
            return {}

        patterns = {
            'avg_length': 0,
            'has_question': 0,
            'has_emoji': 0,
            'has_numbers': 0,
            'has_cta': 0
        }

        for p in top_posts:
            patterns['avg_length'] += len(p.content)
            if '?' in p.content:
                patterns['has_question'] += 1
            if any(ord(c) > 127 for c in p.content):  # Simple emoji detection
                patterns['has_emoji'] += 1
            if any(c.isdigit() for c in p.content):
                patterns['has_numbers'] += 1
            if any(cta in p.content.lower() for cta in ['learn', 'discover', 'try', 'get', 'start']):
                patterns['has_cta'] += 1

        count = len(top_posts)
        return {
            'avg_length': patterns['avg_length'] // count,
            'question_rate': f"{patterns['has_question'] / count * 100:.0f}%",
            'emoji_rate': f"{patterns['has_emoji'] / count * 100:.0f}%",
            'number_rate': f"{patterns['has_numbers'] / count * 100:.0f}%",
            'cta_rate': f"{patterns['has_cta'] / count * 100:.0f}%"
        }

    def _analyze_posting_times(self, posts: List[PostRecord]) -> List[str]:
        """Analyze best posting times based on engagement"""
        if not posts:
            return []

        hour_performance: Dict[int, List[float]] = {}

        for p in posts:
            try:
                posted = datetime.fromisoformat(p.posted_at)
                hour = posted.hour
                if hour not in hour_performance:
                    hour_performance[hour] = []
                hour_performance[hour].append(p.engagement_rate)
            except:
                continue

        # Calculate average engagement per hour
        hour_avg = [
            (hour, sum(rates)/len(rates))
            for hour, rates in hour_performance.items()
            if len(rates) >= 2
        ]

        # Sort by engagement
        hour_avg.sort(key=lambda x: x[1], reverse=True)

        # Return top 3 hours in readable format
        return [f"{hour:02d}:00 UTC" for hour, _ in hour_avg[:3]]

    def _generate_recommendations(self, avg_engagement: float,
                                   tier_counts: Dict,
                                   best_hashtags: List,
                                   content_patterns: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        # Engagement-based recommendations
        if avg_engagement < 0.5:
            recommendations.append("⚠️ Low engagement - try more questions and CTAs")
        elif avg_engagement < 2.0:
            recommendations.append("📈 Moderate engagement - focus on trending topics")
        else:
            recommendations.append("🔥 Strong engagement - keep current strategy")

        # Tier-based recommendations
        viral_rate = tier_counts.get('viral', 0) / max(sum(tier_counts.values()), 1)
        if viral_rate < 0.05:
            recommendations.append("💡 Try more controversial/surprising angles for viral potential")

        # Hashtag recommendations
        if best_hashtags:
            top_tags = [tag for tag, _ in best_hashtags[:3]]
            recommendations.append(f"#️⃣ Top hashtags: {', '.join(top_tags)}")

        # Content pattern recommendations
        if content_patterns.get('question_rate', '0%') == '0%':
            recommendations.append("❓ Add more questions to boost engagement")

        return recommendations

    def get_learning_context(self, limit: int = 5) -> str:
        """
        Get context from top performers for AI content generation

        Returns:
            String context with examples of high-performing content
        """
        top_posts = self.get_top_performers(limit=limit, industry=self.industry)

        if not top_posts:
            return ""

        context_lines = ["Here are examples of high-performing posts in this industry:"]

        for i, post in enumerate(top_posts, 1):
            context_lines.append(
                f"{i}. (Engagement: {post.engagement_rate:.1f}%) {post.content[:150]}..."
            )

        context_lines.append("\nTry to incorporate similar patterns and topics.")

        return "\n".join(context_lines)

    def get_posts_needing_update(self, min_age_hours: int = 4,
                                  max_age_days: int = 7) -> List[PostRecord]:
        """
        Get posts that need engagement metrics updated

        Args:
            min_age_hours: Minimum hours since posting
            max_age_days: Maximum days since posting

        Returns:
            List of posts needing engagement update
        """
        now = datetime.utcnow()
        min_age = now - timedelta(hours=min_age_hours)
        max_age = now - timedelta(days=max_age_days)

        needs_update = []
        for p in self.posts:
            posted = datetime.fromisoformat(p.posted_at)

            # Check if in valid age range
            if max_age < posted < min_age:
                # Check if never updated or stale
                if not p.last_updated or p.last_updated == p.posted_at:
                    needs_update.append(p)
                else:
                    last_update = datetime.fromisoformat(p.last_updated)
                    if (now - last_update) > timedelta(hours=6):
                        needs_update.append(p)

        return needs_update

    def print_summary(self):
        """Print a summary of engagement performance"""
        insights = self.get_performance_insights()

        print("\n" + "="*50)
        print("📊 ENGAGEMENT PERFORMANCE SUMMARY")
        print("="*50)

        if insights.get('total_posts', 0) == 0:
            print("No posts recorded yet.")
            return

        print(f"\n📈 Industry: {insights['industry']}")
        print(f"   Total Posts: {insights['total_posts']}")
        print(f"   Avg Viral Score: {insights['avg_viral_score']}/100")
        print(f"   Avg Engagement Rate: {insights['avg_engagement_rate']}%")

        print(f"\n🏆 Performance Tiers:")
        for tier, count in insights['tier_distribution'].items():
            emoji = {'viral': '🔥', 'high': '⭐', 'medium': '📊', 'low': '📉'}
            print(f"   {emoji.get(tier, '')} {tier.capitalize()}: {count}")

        if insights.get('best_hashtags'):
            print(f"\n#️⃣ Best Hashtags:")
            for tag, avg_eng in insights['best_hashtags']:
                print(f"   {tag}: {avg_eng:.2f}% avg engagement")

        if insights.get('best_posting_times'):
            print(f"\n⏰ Best Posting Times: {', '.join(insights['best_posting_times'])}")

        if insights.get('content_patterns'):
            print(f"\n📝 Top Content Patterns:")
            patterns = insights['content_patterns']
            print(f"   Avg Length: {patterns.get('avg_length', 'N/A')} chars")
            print(f"   Questions: {patterns.get('question_rate', 'N/A')}")
            print(f"   Has Numbers: {patterns.get('number_rate', 'N/A')}")

        print(f"\n💡 Recommendations:")
        for rec in insights.get('recommendations', []):
            print(f"   {rec}")

        print("\n" + "="*50)


def main():
    """Demo engagement tracker"""
    print("📊 Engagement Tracker Demo\n")

    # Create tracker
    tracker = EngagementTracker(storage_path="demo_history.json", industry="real_estate")

    # Record some demo posts
    demo_posts = [
        ("tweet_001", "twitter", "🏠 AI is revolutionizing real estate valuations! #PropTech #AI", 75.0, ["#PropTech", "#AI"]),
        ("tweet_002", "twitter", "Did you know: 73% of homebuyers start online? #RealEstate", 68.0, ["#RealEstate"]),
        ("tweet_003", "twitter", "Smart pricing = faster sales. Here's why data matters 📊", 82.0, ["#DataDriven"]),
    ]

    for post_id, platform, content, viral_score, hashtags in demo_posts:
        tracker.record_post(post_id, platform, content, viral_score, hashtags)

    # Simulate engagement updates
    engagement_data = [
        ("tweet_001", "twitter", {"likes": 45, "retweets": 12, "replies": 8, "impressions": 2500}),
        ("tweet_002", "twitter", {"likes": 23, "retweets": 5, "replies": 3, "impressions": 1800}),
        ("tweet_003", "twitter", {"likes": 89, "retweets": 34, "replies": 15, "impressions": 5000}),
    ]

    print("\n📥 Updating engagement metrics...")
    for post_id, platform, data in engagement_data:
        tracker.update_engagement(post_id, platform, data)

    # Print summary
    tracker.print_summary()

    # Get learning context
    print("\n📚 Learning Context for AI:")
    print(tracker.get_learning_context())

    # Cleanup demo file
    import os
    if os.path.exists("demo_history.json"):
        os.remove("demo_history.json")

    print("\n✅ Engagement Tracker demo complete!")


if __name__ == "__main__":
    main()
