#!/usr/bin/env python3
"""
Analytics Dashboard for SME Social Media Manager
Tracks performance metrics, viral prediction accuracy, and engagement
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict
from dataclasses import dataclass, asdict
from logger import get_logger

logger = get_logger(__name__)


@dataclass
class PostMetrics:
    """Metrics for a single post"""
    timestamp: str
    platform: str  # 'twitter' or 'linkedin'
    content: str
    content_hash: str  # For deduplication
    predicted_viral_score: float
    predicted_likes: int
    predicted_retweets: int
    actual_likes: int = 0
    actual_retweets: int = 0
    actual_replies: int = 0
    actual_impressions: int = 0
    post_id: Optional[str] = None
    optimized: bool = False


@dataclass
class SessionMetrics:
    """Metrics for a bot session"""
    session_id: str
    start_time: str
    end_time: Optional[str] = None
    posts_created: int = 0
    linkedin_posts: int = 0
    mentions_checked: int = 0
    engagements_made: int = 0
    errors: int = 0
    viral_predictions: int = 0
    ai_provider_used: Optional[str] = None
    rate_limited: bool = False


class BotAnalytics:
    """
    Track and analyze bot performance metrics

    Example:
        >>> analytics = BotAnalytics()
        >>> analytics.log_post(content, viral_score, actual_engagement)
        >>> report = analytics.generate_report(days=7)
        >>> print(report)
    """

    def __init__(self, data_dir: str = "analytics_data"):
        """
        Initialize analytics dashboard

        Args:
            data_dir: Directory to store analytics data
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

        self.posts: List[PostMetrics] = []
        self.sessions: List[SessionMetrics] = []

        # Load existing data
        self._load_data()

        logger.info(f"Analytics dashboard initialized with {len(self.posts)} posts")

    def _load_data(self):
        """Load existing analytics data from disk"""
        posts_file = self.data_dir / 'posts.json'
        sessions_file = self.data_dir / 'sessions.json'

        try:
            if posts_file.exists():
                with open(posts_file, 'r') as f:
                    data = json.load(f)
                    self.posts = [PostMetrics(**post) for post in data]
                logger.info(f"Loaded {len(self.posts)} posts from disk")
        except Exception as e:
            logger.warning(f"Failed to load posts data: {e}")

        try:
            if sessions_file.exists():
                with open(sessions_file, 'r') as f:
                    data = json.load(f)
                    self.sessions = [SessionMetrics(**session) for session in data]
                logger.info(f"Loaded {len(self.sessions)} sessions from disk")
        except Exception as e:
            logger.warning(f"Failed to load sessions data: {e}")

    def _save_data(self):
        """Save analytics data to disk"""
        try:
            # Save posts
            posts_file = self.data_dir / 'posts.json'
            with open(posts_file, 'w') as f:
                json.dump([asdict(post) for post in self.posts], f, indent=2)

            # Save sessions
            sessions_file = self.data_dir / 'sessions.json'
            with open(sessions_file, 'w') as f:
                json.dump([asdict(session) for session in self.sessions], f, indent=2)

            logger.debug(f"Saved analytics data ({len(self.posts)} posts, {len(self.sessions)} sessions)")

        except Exception as e:
            logger.error(f"Failed to save analytics data: {e}")

    def log_post(self, content: str, viral_score: float,
                  predicted_engagement: Dict[str, int],
                  platform: str = "twitter",
                  actual_engagement: Optional[Dict[str, int]] = None,
                  post_id: Optional[str] = None,
                  optimized: bool = False):
        """
        Log a post for analytics tracking

        Args:
            content: Post content
            viral_score: Predicted viral score (0-100)
            predicted_engagement: Dict with predicted likes, retweets, etc.
            platform: 'twitter' or 'linkedin'
            actual_engagement: Optional dict with actual engagement metrics
            post_id: Platform-specific post ID
            optimized: Whether content was optimized
        """
        import hashlib

        # Create content hash for deduplication
        content_hash = hashlib.md5(content.encode()).hexdigest()[:16]

        # Create post metrics
        post = PostMetrics(
            timestamp=datetime.now().isoformat(),
            platform=platform,
            content=content,
            content_hash=content_hash,
            predicted_viral_score=viral_score,
            predicted_likes=predicted_engagement.get('likes', 0),
            predicted_retweets=predicted_engagement.get('retweets', 0),
            post_id=post_id,
            optimized=optimized
        )

        # Add actual engagement if available
        if actual_engagement:
            post.actual_likes = actual_engagement.get('likes', 0)
            post.actual_retweets = actual_engagement.get('retweets', 0)
            post.actual_replies = actual_engagement.get('replies', 0)
            post.actual_impressions = actual_engagement.get('impressions', 0)

        self.posts.append(post)
        self._save_data()

        logger.info(f"Logged post: {content[:50]}... (score: {viral_score:.1f})")

    def update_post_engagement(self, post_id: str, actual_engagement: Dict[str, int]):
        """
        Update actual engagement metrics for a post

        Args:
            post_id: Platform-specific post ID
            actual_engagement: Dict with actual engagement metrics
        """
        for post in self.posts:
            if post.post_id == post_id:
                post.actual_likes = actual_engagement.get('likes', 0)
                post.actual_retweets = actual_engagement.get('retweets', 0)
                post.actual_replies = actual_engagement.get('replies', 0)
                post.actual_impressions = actual_engagement.get('impressions', 0)
                self._save_data()
                logger.info(f"Updated engagement for post {post_id}")
                return

        logger.warning(f"Post {post_id} not found for engagement update")

    def log_session(self, session_stats: Dict[str, int],
                     session_id: Optional[str] = None,
                     ai_provider: Optional[str] = None):
        """
        Log session statistics

        Args:
            session_stats: Dict with session metrics
            session_id: Unique session identifier
            ai_provider: AI provider used in session
        """
        if session_id is None:
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

        session = SessionMetrics(
            session_id=session_id,
            start_time=datetime.now().isoformat(),
            posts_created=session_stats.get('posts_created', 0),
            linkedin_posts=session_stats.get('linkedin_posts', 0),
            mentions_checked=session_stats.get('mentions_checked', 0),
            engagements_made=session_stats.get('engagements_made', 0),
            errors=session_stats.get('errors', 0),
            viral_predictions=session_stats.get('viral_predictions', 0),
            ai_provider_used=ai_provider,
            rate_limited=session_stats.get('rate_limited', False)
        )

        self.sessions.append(session)
        self._save_data()

        logger.info(f"Logged session {session_id}: {session.posts_created} posts, {session.engagements_made} engagements")

    def get_prediction_accuracy(self, days: int = 30) -> float:
        """
        Calculate viral prediction accuracy

        Args:
            days: Number of days to analyze

        Returns:
            Accuracy percentage (0-100)
        """
        cutoff_date = datetime.now() - timedelta(days=days)

        # Filter posts with actual engagement data
        posts_with_actuals = [
            post for post in self.posts
            if datetime.fromisoformat(post.timestamp) > cutoff_date
            and post.actual_likes > 0  # Has real engagement data
        ]

        if not posts_with_actuals:
            logger.warning("No posts with actual engagement data for accuracy calculation")
            return 0.0

        # Calculate prediction errors
        errors = []
        for post in posts_with_actuals:
            # Normalize scores (viral score is 0-100, actuals vary)
            # Use likes as primary metric
            predicted_normalized = post.predicted_likes / 100  # Rough normalization
            actual_normalized = post.actual_likes / 100

            error = abs(predicted_normalized - actual_normalized) / max(actual_normalized, 1)
            errors.append(error)

        # Calculate accuracy (inverse of average error)
        avg_error = sum(errors) / len(errors)
        accuracy = max(0, 100 * (1 - avg_error))

        logger.debug(f"Prediction accuracy over {days} days: {accuracy:.1f}%")
        return accuracy

    def get_average_viral_score(self, days: int = 7) -> float:
        """
        Get average viral score for recent posts

        Args:
            days: Number of days to analyze

        Returns:
            Average viral score
        """
        cutoff_date = datetime.now() - timedelta(days=days)

        recent_posts = [
            post for post in self.posts
            if datetime.fromisoformat(post.timestamp) > cutoff_date
        ]

        if not recent_posts:
            return 0.0

        avg_score = sum(post.predicted_viral_score for post in recent_posts) / len(recent_posts)
        return avg_score

    def get_engagement_stats(self, days: int = 7) -> Dict[str, float]:
        """
        Get engagement statistics

        Args:
            days: Number of days to analyze

        Returns:
            Dict with engagement metrics
        """
        cutoff_date = datetime.now() - timedelta(days=days)

        recent_posts = [
            post for post in self.posts
            if datetime.fromisoformat(post.timestamp) > cutoff_date
        ]

        if not recent_posts:
            return {'total_posts': 0}

        # Calculate averages
        total_posts = len(recent_posts)
        total_likes = sum(post.actual_likes for post in recent_posts)
        total_retweets = sum(post.actual_retweets for post in recent_posts)
        total_replies = sum(post.actual_replies for post in recent_posts)

        return {
            'total_posts': total_posts,
            'avg_likes': total_likes / total_posts if total_posts > 0 else 0,
            'avg_retweets': total_retweets / total_posts if total_posts > 0 else 0,
            'avg_replies': total_replies / total_posts if total_posts > 0 else 0,
            'total_engagement': total_likes + total_retweets + total_replies
        }

    def get_best_performing_posts(self, limit: int = 5, days: int = 30) -> List[PostMetrics]:
        """
        Get best performing posts by actual engagement

        Args:
            limit: Number of posts to return
            days: Number of days to analyze

        Returns:
            List of top performing posts
        """
        cutoff_date = datetime.now() - timedelta(days=days)

        recent_posts = [
            post for post in self.posts
            if datetime.fromisoformat(post.timestamp) > cutoff_date
            and post.actual_likes > 0
        ]

        # Sort by total engagement
        recent_posts.sort(
            key=lambda p: p.actual_likes + p.actual_retweets * 2 + p.actual_replies * 3,
            reverse=True
        )

        return recent_posts[:limit]

    def generate_report(self, days: int = 7) -> str:
        """
        Generate performance report

        Args:
            days: Number of days to analyze

        Returns:
            Formatted report string
        """
        logger.info(f"Generating analytics report for last {days} days")

        cutoff_date = datetime.now() - timedelta(days=days)

        # Filter data
        recent_posts = [
            post for post in self.posts
            if datetime.fromisoformat(post.timestamp) > cutoff_date
        ]

        recent_sessions = [
            session for session in self.sessions
            if datetime.fromisoformat(session.start_time) > cutoff_date
        ]

        # Generate report
        report = f"\n{'='*60}\n"
        report += f"📊 BOT PERFORMANCE REPORT (Last {days} Days)\n"
        report += f"{'='*60}\n\n"

        # Post metrics
        report += f"📝 Content Performance:\n"
        report += f"   Total Posts: {len(recent_posts)}\n"

        if recent_posts:
            avg_score = self.get_average_viral_score(days)
            report += f"   Avg Viral Score: {avg_score:.1f}/100\n"

            # Engagement stats
            engagement = self.get_engagement_stats(days)
            report += f"   Avg Likes: {engagement.get('avg_likes', 0):.1f}\n"
            report += f"   Avg Retweets: {engagement.get('avg_retweets', 0):.1f}\n"
            report += f"   Total Engagement: {engagement.get('total_engagement', 0)}\n"

            # Platform breakdown
            twitter_posts = sum(1 for p in recent_posts if p.platform == 'twitter')
            linkedin_posts = sum(1 for p in recent_posts if p.platform == 'linkedin')
            report += f"\n📱 Platform Distribution:\n"
            report += f"   Twitter: {twitter_posts} posts\n"
            report += f"   LinkedIn: {linkedin_posts} posts\n"

            # Optimization stats
            optimized_posts = sum(1 for p in recent_posts if p.optimized)
            report += f"\n🔧 Optimization:\n"
            report += f"   Auto-optimized Posts: {optimized_posts}/{len(recent_posts)} "
            report += f"({100*optimized_posts/len(recent_posts):.1f}%)\n"

        # Session metrics
        if recent_sessions:
            report += f"\n🤖 Bot Sessions:\n"
            report += f"   Total Sessions: {len(recent_sessions)}\n"

            total_engagements = sum(s.engagements_made for s in recent_sessions)
            total_errors = sum(s.errors for s in recent_sessions)

            report += f"   Total Engagements: {total_engagements}\n"
            report += f"   Total Errors: {total_errors}\n"

            # AI provider stats
            ai_providers = defaultdict(int)
            for session in recent_sessions:
                if session.ai_provider_used:
                    ai_providers[session.ai_provider_used] += 1

            if ai_providers:
                report += f"\n🤖 AI Provider Usage:\n"
                for provider, count in ai_providers.items():
                    report += f"   {provider.title()}: {count} sessions\n"

        # Best posts
        best_posts = self.get_best_performing_posts(limit=3, days=days)
        if best_posts:
            report += f"\n🏆 Top Performing Posts:\n"
            for i, post in enumerate(best_posts, 1):
                engagement = post.actual_likes + post.actual_retweets * 2
                report += f"   {i}. Score: {post.predicted_viral_score:.0f} | "
                report += f"Likes: {post.actual_likes} | RTs: {post.actual_retweets}\n"
                report += f"      {post.content[:60]}...\n"

        report += f"\n{'='*60}\n"

        return report

    def export_data(self, format: str = 'json', filename: Optional[str] = None) -> str:
        """
        Export analytics data

        Args:
            format: Export format ('json' or 'csv')
            filename: Optional filename (auto-generated if not provided)

        Returns:
            Path to exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"analytics_export_{timestamp}.{format}"

        export_path = self.data_dir / filename

        if format == 'json':
            with open(export_path, 'w') as f:
                json.dump({
                    'posts': [asdict(post) for post in self.posts],
                    'sessions': [asdict(session) for session in self.sessions]
                }, f, indent=2)

        elif format == 'csv':
            import csv
            with open(export_path, 'w', newline='') as f:
                if self.posts:
                    writer = csv.DictWriter(f, fieldnames=asdict(self.posts[0]).keys())
                    writer.writeheader()
                    for post in self.posts:
                        writer.writerow(asdict(post))

        logger.info(f"Exported analytics data to {export_path}")
        return str(export_path)


# Example usage and testing
if __name__ == "__main__":
    print("=" * 60)
    print("ANALYTICS DASHBOARD TEST")
    print("=" * 60)

    # Create analytics instance
    analytics = BotAnalytics()

    # Log some test posts
    print("\n📝 Logging test posts...")

    test_posts = [
        ("AI analytics boost restaurant revenue by 47%! #AI #Business", 85),
        ("Quick tip: Track your profit margins daily! #Restaurant #Tips", 72),
        ("New blog post about data analytics", 45)
    ]

    for content, score in test_posts:
        analytics.log_post(
            content=content,
            viral_score=score,
            predicted_engagement={'likes': 10, 'retweets': 3},
            platform='twitter'
        )

    # Generate report
    print("\n" + analytics.generate_report(days=30))

    # Export data
    export_path = analytics.export_data(format='json')
    print(f"\n✅ Data exported to: {export_path}")
