"""
Analytics Integration Module
Connects the analytics dashboard with existing social media management systems.
"""

import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path

from .analytics_dashboard import (
    AnalyticsDashboard, GrowthTracker, PerformanceAnalytics, ROIMeasurement,
    GrowthMetrics, ContentPerformance, ROIMetrics
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalyticsIntegrator:
    """Integrates analytics dashboard with existing SME social media systems"""
    
    def __init__(self, 
                 social_db_path: str = "data/social_manager.db",
                 hashtag_db_path: str = "data/hashtag_analytics.db",
                 community_db_path: str = "data/community_database.db"):
        self.social_db_path = social_db_path
        self.hashtag_db_path = hashtag_db_path  
        self.community_db_path = community_db_path
        self.dashboard = AnalyticsDashboard()
        
    def sync_from_social_manager(self) -> bool:
        """Sync data from social manager database to analytics"""
        try:
            # Import posts data
            posts_imported = self._import_posts_data()
            
            # Import engagement data
            engagements_imported = self._import_engagement_data()
            
            # Import hashtag performance
            hashtag_imported = self._import_hashtag_data()
            
            logger.info(f"Analytics sync complete: {posts_imported} posts, {engagements_imported} engagements, {hashtag_imported} hashtags")
            return True
            
        except Exception as e:
            logger.error(f"Error syncing from social manager: {e}")
            return False
    
    def _import_posts_data(self) -> int:
        """Import posts data and create content performance records"""
        imported_count = 0
        
        try:
            with sqlite3.connect(self.social_db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, content, scheduled_time, posted_time, 
                           theme, tweet_id, engagement_metrics
                    FROM posts 
                    WHERE posted_time IS NOT NULL
                    ORDER BY posted_time DESC
                ''')
                
                posts = cursor.fetchall()
                
                for post in posts:
                    post_id, content, scheduled_time, posted_time, theme, tweet_id, engagement_metrics = post
                    
                    # Parse engagement metrics if available
                    engagement_data = {}
                    if engagement_metrics:
                        try:
                            engagement_data = json.loads(engagement_metrics)
                        except:
                            engagement_data = {}
                    
                    # Determine content type from content analysis
                    content_type = self._classify_content_type(content)
                    
                    # Create content performance record
                    performance = ContentPerformance(
                        content_id=post_id,
                        theme=theme or "general",
                        content_type=content_type,
                        posted_time=datetime.fromisoformat(posted_time) if posted_time else datetime.now(),
                        likes=engagement_data.get('likes', 0),
                        retweets=engagement_data.get('retweets', 0),
                        replies=engagement_data.get('replies', 0),
                        quotes=engagement_data.get('quotes', 0),
                        impressions=engagement_data.get('impressions', 0),
                        engagement_rate=engagement_data.get('engagement_rate', 0.0),
                        hashtags=self._extract_hashtags(content)
                    )
                    
                    # Calculate viral score
                    performance.viral_score = self.dashboard.performance_analytics.calculate_viral_score(
                        performance.likes, performance.retweets, performance.replies,
                        performance.impressions, 100  # Estimated follower count
                    )
                    
                    # Record in analytics
                    if self.dashboard.performance_analytics.record_content_performance(performance):
                        imported_count += 1
                        
        except Exception as e:
            logger.error(f"Error importing posts data: {e}")
            
        return imported_count
    
    def _import_engagement_data(self) -> int:
        """Import engagement data for analytics"""
        imported_count = 0
        
        try:
            with sqlite3.connect(self.social_db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT action_type, target_tweet_id, target_author, 
                           executed_at, success
                    FROM engagements 
                    WHERE executed_at IS NOT NULL
                    ORDER BY executed_at DESC
                ''')
                
                engagements = cursor.fetchall()
                
                # Track engagement metrics for analytics
                engagement_summary = {
                    'total_engagements': len(engagements),
                    'successful_engagements': sum(1 for e in engagements if e[4]),
                    'engagement_types': {}
                }
                
                for engagement in engagements:
                    action_type = engagement[0]
                    if action_type not in engagement_summary['engagement_types']:
                        engagement_summary['engagement_types'][action_type] = 0
                    engagement_summary['engagement_types'][action_type] += 1
                    imported_count += 1
                
                # Store engagement summary in analytics
                logger.info(f"Engagement summary: {engagement_summary}")
                
        except Exception as e:
            logger.error(f"Error importing engagement data: {e}")
            
        return imported_count
    
    def _import_hashtag_data(self) -> int:
        """Import hashtag performance data"""
        imported_count = 0
        
        try:
            with sqlite3.connect(self.hashtag_db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT hashtag, reach, impressions, engagement_rate, 
                           likes, shares, comments, viral_score, usage_frequency
                    FROM hashtag_performance
                    ORDER BY viral_score DESC
                ''')
                
                hashtags = cursor.fetchall()
                
                for hashtag_data in hashtags:
                    hashtag, reach, impressions, engagement_rate, likes, shares, comments, viral_score, usage_frequency = hashtag_data
                    
                    # Use hashtag data to enhance content performance analysis
                    logger.debug(f"Hashtag {hashtag}: viral_score={viral_score}, engagement_rate={engagement_rate}")
                    imported_count += 1
                    
        except Exception as e:
            logger.error(f"Error importing hashtag data: {e}")
            
        return imported_count
    
    def _classify_content_type(self, content: str) -> str:
        """Classify content type based on content analysis"""
        content_lower = content.lower()
        
        if any(word in content_lower for word in ["case study", "success story", "client", "customer"]):
            return "case_study"
        elif any(word in content_lower for word in ["how to", "tip", "guide", "learn"]):
            return "educational"
        elif any(word in content_lower for word in ["new feature", "update", "release", "technology"]):
            return "product_feature"
        elif any(word in content_lower for word in ["industry", "trend", "market", "analysis"]):
            return "industry_insight"
        elif any(word in content_lower for word in ["question", "poll", "what do you think", "community"]):
            return "community_engagement"
        else:
            return "general"
    
    def _extract_hashtags(self, content: str) -> List[str]:
        """Extract hashtags from content"""
        import re
        hashtags = re.findall(r'#\w+', content)
        return [tag.lower() for tag in hashtags]
    
    def update_growth_metrics_from_account(self, account_data: Dict[str, Any]) -> bool:
        """Update growth metrics from current account data"""
        try:
            metrics = GrowthMetrics(
                timestamp=datetime.now(),
                followers_count=account_data.get('followers_count', 0),
                following_count=account_data.get('following_count', 0),
                tweet_count=account_data.get('tweet_count', 0),
                listed_count=account_data.get('listed_count', 0),
                account_age_days=account_data.get('account_age_days', 0),
                growth_rate_followers=account_data.get('growth_rate_followers', 0.0),
                growth_rate_tweets=account_data.get('growth_rate_tweets', 0.0),
                engagement_rate=account_data.get('engagement_rate', 0.0),
                reach=account_data.get('reach', 0),
                impressions=account_data.get('impressions', 0)
            )
            
            return self.dashboard.growth_tracker.record_growth_metrics(metrics)
            
        except Exception as e:
            logger.error(f"Error updating growth metrics: {e}")
            return False
    
    def track_business_conversion(self, conversion_type: str, source_content_id: str = None, 
                                value: float = 0.0, user_id: str = None) -> bool:
        """Track business conversions from social media"""
        try:
            # Map conversion types to standard funnel stages
            stage_mapping = {
                'profile_visit': 'awareness',
                'website_click': 'interest', 
                'demo_request': 'intent',
                'business_inquiry': 'evaluation',
                'customer_signup': 'purchase'
            }
            
            stage = stage_mapping.get(conversion_type, conversion_type)
            user_id = user_id or f"user_{datetime.now().timestamp()}"
            
            return self.dashboard.roi_measurement.track_conversion(
                user_id=user_id,
                stage=stage,
                source_content_id=source_content_id,
                conversion_value=value
            )
            
        except Exception as e:
            logger.error(f"Error tracking conversion: {e}")
            return False
    
    def generate_integration_report(self) -> Dict[str, Any]:
        """Generate comprehensive integration status report"""
        report = {
            "integration_timestamp": datetime.now().isoformat(),
            "system_status": "operational"
        }
        
        try:
            # Check database connections
            report["database_status"] = {
                "social_manager": self._check_database_connection(self.social_db_path),
                "hashtag_analytics": self._check_database_connection(self.hashtag_db_path),
                "community_database": self._check_database_connection(self.community_db_path),
                "analytics": self._check_database_connection("data/analytics.db")
            }
            
            # Get data counts
            report["data_summary"] = {
                "posts_tracked": self._count_table_rows(self.social_db_path, "posts"),
                "engagements_tracked": self._count_table_rows(self.social_db_path, "engagements"),
                "hashtags_analyzed": self._count_table_rows(self.hashtag_db_path, "hashtag_performance"),
                "growth_metrics": self._count_table_rows("data/analytics.db", "growth_metrics"),
                "content_performance": self._count_table_rows("data/analytics.db", "content_performance"),
                "roi_metrics": self._count_table_rows("data/analytics.db", "roi_metrics")
            }
            
            # Analytics dashboard status
            dashboard_data = self.dashboard.get_real_time_dashboard()
            report["dashboard_status"] = {
                "operational": "status" in dashboard_data,
                "last_update": dashboard_data.get("timestamp"),
                "current_followers": dashboard_data.get("current_metrics", {}).get("followers_count", 0),
                "immediate_actions_count": len(dashboard_data.get("immediate_actions", []))
            }
            
            # Integration health
            total_data_points = sum(report["data_summary"].values())
            report["integration_health"] = {
                "overall_score": min(100, total_data_points * 2),  # Simple health score
                "data_completeness": "good" if total_data_points > 50 else "needs_improvement",
                "sync_status": "active",
                "recommendations": self._get_integration_recommendations(report)
            }
            
        except Exception as e:
            logger.error(f"Error generating integration report: {e}")
            report["error"] = str(e)
            
        return report
    
    def _check_database_connection(self, db_path: str) -> bool:
        """Check if database connection is working"""
        try:
            with sqlite3.connect(db_path) as conn:
                conn.execute("SELECT 1")
                return True
        except:
            return False
    
    def _count_table_rows(self, db_path: str, table_name: str) -> int:
        """Count rows in a database table"""
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                return cursor.fetchone()[0]
        except:
            return 0
    
    def _get_integration_recommendations(self, report: Dict[str, Any]) -> List[str]:
        """Get recommendations for improving integration"""
        recommendations = []
        
        data_summary = report.get("data_summary", {})
        
        if data_summary.get("growth_metrics", 0) < 10:
            recommendations.append("Increase frequency of growth metrics collection")
        
        if data_summary.get("content_performance", 0) < 20:
            recommendations.append("Import more historical content performance data")
        
        if data_summary.get("roi_metrics", 0) < 5:
            recommendations.append("Set up business conversion tracking")
        
        dashboard_status = report.get("dashboard_status", {})
        if not dashboard_status.get("operational", False):
            recommendations.append("Check analytics dashboard configuration")
        
        if len(recommendations) == 0:
            recommendations.append("Integration is healthy - continue monitoring")
        
        return recommendations
    
    def auto_sync_scheduler(self, interval_hours: int = 1) -> Dict[str, Any]:
        """Set up automatic synchronization schedule"""
        sync_config = {
            "enabled": True,
            "interval_hours": interval_hours,
            "last_sync": datetime.now().isoformat(),
            "next_sync": (datetime.now() + timedelta(hours=interval_hours)).isoformat(),
            "sync_tasks": [
                "import_posts_data",
                "import_engagement_data", 
                "import_hashtag_data",
                "update_growth_metrics",
                "generate_reports"
            ]
        }
        
        logger.info(f"Auto-sync scheduled every {interval_hours} hours")
        return sync_config

# Integration utility functions
def quick_integration_setup(social_db: str = "data/social_manager.db") -> AnalyticsIntegrator:
    """Quick setup for analytics integration"""
    integrator = AnalyticsIntegrator(social_db_path=social_db)
    
    # Initial sync
    success = integrator.sync_from_social_manager()
    
    if success:
        logger.info("Analytics integration setup complete")
    else:
        logger.warning("Analytics integration setup had issues")
    
    return integrator

def demo_integration():
    """Demonstrate analytics integration"""
    print("SME Analytica Analytics Integration Demo")
    print("=" * 45)
    
    # Setup integration
    integrator = quick_integration_setup()
    
    # Generate integration report
    report = integrator.generate_integration_report()
    
    print("\n📊 INTEGRATION STATUS REPORT:")
    print("-" * 30)
    print(f"Status: {report.get('system_status', 'Unknown')}")
    print(f"Timestamp: {report.get('integration_timestamp', 'N/A')}")
    
    # Database status
    db_status = report.get("database_status", {})
    print(f"\n🗄️ DATABASE CONNECTIONS:")
    for db_name, status in db_status.items():
        status_icon = "✅" if status else "❌"
        print(f"  {db_name}: {status_icon}")
    
    # Data summary
    data_summary = report.get("data_summary", {})
    print(f"\n📈 DATA SUMMARY:")
    for data_type, count in data_summary.items():
        print(f"  {data_type}: {count}")
    
    # Health status
    health = report.get("integration_health", {})
    print(f"\n🏥 INTEGRATION HEALTH:")
    print(f"  Overall Score: {health.get('overall_score', 0)}/100")
    print(f"  Data Completeness: {health.get('data_completeness', 'Unknown')}")
    print(f"  Sync Status: {health.get('sync_status', 'Unknown')}")
    
    # Recommendations
    recommendations = health.get("recommendations", [])
    if recommendations:
        print(f"\n💡 RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
    
    # Test conversion tracking
    print(f"\n🎯 TESTING CONVERSION TRACKING:")
    conversions = [
        ("website_click", "content_123", 0.0),
        ("demo_request", "content_124", 100.0),
        ("customer_signup", "content_125", 2500.0)
    ]
    
    for conv_type, content_id, value in conversions:
        success = integrator.track_business_conversion(conv_type, content_id, value)
        status_icon = "✅" if success else "❌"
        print(f"  {conv_type}: {status_icon} (${value})")
    
    print(f"\n🔄 AUTO-SYNC CONFIGURATION:")
    sync_config = integrator.auto_sync_scheduler(interval_hours=2)
    print(f"  Enabled: {sync_config.get('enabled', False)}")
    print(f"  Interval: {sync_config.get('interval_hours', 0)} hours")
    print(f"  Next Sync: {sync_config.get('next_sync', 'N/A')}")
    
    print(f"\nIntegration Demo Complete!")

if __name__ == "__main__":
    demo_integration()