"""
SME Analytica Analytics Dashboard
Comprehensive analytics system for tracking growth metrics, ROI, and providing actionable insights.
"""

import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
from collections import defaultdict
import statistics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class GrowthMetrics:
    """Data class for growth metrics"""
    timestamp: datetime
    followers_count: int
    following_count: int
    tweet_count: int
    listed_count: int
    account_age_days: int
    growth_rate_followers: float
    growth_rate_tweets: float
    engagement_rate: float = 0.0
    reach: int = 0
    impressions: int = 0

@dataclass
class ContentPerformance:
    """Data class for content performance metrics"""
    content_id: str
    theme: str
    content_type: str
    posted_time: datetime
    likes: int = 0
    retweets: int = 0
    replies: int = 0
    quotes: int = 0
    impressions: int = 0
    engagement_rate: float = 0.0
    viral_score: float = 0.0
    conversion_actions: int = 0
    hashtags: List[str] = None

@dataclass
class ROIMetrics:
    """Data class for ROI tracking"""
    timestamp: datetime
    social_impressions: int
    website_visits: int
    demo_requests: int
    business_inquiries: int
    customers_acquired: int
    revenue_generated: float
    cost_per_acquisition: float
    conversion_rate: float
    roi_percentage: float

@dataclass
class WeeklyReport:
    """Data class for weekly analytics report"""
    week_start: datetime
    week_end: datetime
    follower_growth: int
    engagement_total: int
    top_performing_content: List[ContentPerformance]
    conversion_metrics: ROIMetrics
    recommendations: List[str]
    growth_forecast: Dict[str, Any]
    competitive_analysis: Dict[str, Any]

class GrowthTracker:
    """Real-time follower growth tracking and projections"""
    
    def __init__(self, db_path: str = "data/social_manager.db"):
        self.db_path = db_path
        self.analytics_db_path = "data/analytics.db"
        self._init_analytics_db()
    
    def _init_analytics_db(self):
        """Initialize analytics database"""
        with sqlite3.connect(self.analytics_db_path) as conn:
            cursor = conn.cursor()
            
            # Growth metrics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS growth_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    followers_count INTEGER NOT NULL,
                    following_count INTEGER NOT NULL,
                    tweet_count INTEGER NOT NULL,
                    listed_count INTEGER DEFAULT 0,
                    account_age_days INTEGER NOT NULL,
                    growth_rate_followers REAL DEFAULT 0.0,
                    growth_rate_tweets REAL DEFAULT 0.0,
                    engagement_rate REAL DEFAULT 0.0,
                    reach INTEGER DEFAULT 0,
                    impressions INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Growth targets table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS growth_targets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    week_number INTEGER NOT NULL,
                    target_followers INTEGER NOT NULL,
                    target_engagements INTEGER NOT NULL,
                    target_demo_requests INTEGER NOT NULL,
                    target_business_inquiries INTEGER NOT NULL,
                    focus_area TEXT NOT NULL,
                    actual_followers INTEGER DEFAULT 0,
                    actual_engagements INTEGER DEFAULT 0,
                    actual_demo_requests INTEGER DEFAULT 0,
                    actual_business_inquiries INTEGER DEFAULT 0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def record_growth_metrics(self, metrics: GrowthMetrics) -> bool:
        """Record current growth metrics"""
        try:
            with sqlite3.connect(self.analytics_db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO growth_metrics 
                    (timestamp, followers_count, following_count, tweet_count, 
                     listed_count, account_age_days, growth_rate_followers, 
                     growth_rate_tweets, engagement_rate, reach, impressions)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    metrics.timestamp.isoformat(),
                    metrics.followers_count,
                    metrics.following_count,
                    metrics.tweet_count,
                    metrics.listed_count,
                    metrics.account_age_days,
                    metrics.growth_rate_followers,
                    metrics.growth_rate_tweets,
                    metrics.engagement_rate,
                    metrics.reach,
                    metrics.impressions
                ))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error recording growth metrics: {e}")
            return False
    
    def get_growth_trajectory(self, days: int = 30) -> List[GrowthMetrics]:
        """Get growth trajectory for specified days"""
        try:
            with sqlite3.connect(self.analytics_db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM growth_metrics 
                    WHERE timestamp >= datetime('now', '-{} days')
                    ORDER BY timestamp DESC
                '''.format(days))
                
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                
                metrics = []
                for row in rows:
                    data = dict(zip(columns, row))
                    metrics.append(GrowthMetrics(
                        timestamp=datetime.fromisoformat(data['timestamp']),
                        followers_count=data['followers_count'],
                        following_count=data['following_count'],
                        tweet_count=data['tweet_count'],
                        listed_count=data['listed_count'],
                        account_age_days=data['account_age_days'],
                        growth_rate_followers=data['growth_rate_followers'],
                        growth_rate_tweets=data['growth_rate_tweets'],
                        engagement_rate=data['engagement_rate'],
                        reach=data['reach'],
                        impressions=data['impressions']
                    ))
                
                return metrics
        except Exception as e:
            logger.error(f"Error getting growth trajectory: {e}")
            return []
    
    def calculate_growth_forecast(self, target_days: int = 28) -> Dict[str, Any]:
        """Calculate growth forecast using various models"""
        metrics = self.get_growth_trajectory(days=30)
        if len(metrics) < 7:
            return {"error": "Insufficient data for forecasting"}
        
        # Prepare data for forecasting
        followers_data = [(m.timestamp, m.followers_count) for m in metrics]
        followers_data.sort(key=lambda x: x[0])
        
        if len(followers_data) < 2:
            return {"error": "Insufficient follower data"}
        
        # Linear regression forecast
        days_since_start = [(d[0] - followers_data[0][0]).days for d in followers_data]
        follower_counts = [d[1] for d in followers_data]
        
        if len(days_since_start) > 1:
            # Simple linear regression
            n = len(days_since_start)
            sum_x = sum(days_since_start)
            sum_y = sum(follower_counts)
            sum_xy = sum(x * y for x, y in zip(days_since_start, follower_counts))
            sum_x2 = sum(x * x for x in days_since_start)
            
            # Calculate slope and intercept
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x) if n * sum_x2 - sum_x * sum_x != 0 else 0
            intercept = (sum_y - slope * sum_x) / n
            
            # Forecast
            current_day = max(days_since_start)
            forecast_day = current_day + target_days
            forecasted_followers = int(slope * forecast_day + intercept)
            
            # Growth rate calculation
            current_followers = follower_counts[-1]
            growth_needed = forecasted_followers - current_followers
            daily_growth_rate = growth_needed / target_days if target_days > 0 else 0
            
            # Calculate confidence score based on R²
            y_mean = statistics.mean(follower_counts)
            ss_tot = sum((y - y_mean) ** 2 for y in follower_counts)
            ss_res = sum((y - (slope * x + intercept)) ** 2 for x, y in zip(days_since_start, follower_counts))
            r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
            confidence = max(0, min(100, r_squared * 100))
            
            return {
                "current_followers": current_followers,
                "forecasted_followers": forecasted_followers,
                "growth_needed": growth_needed,
                "daily_growth_rate": daily_growth_rate,
                "weekly_growth_rate": daily_growth_rate * 7,
                "confidence_score": confidence,
                "model": "linear_regression",
                "data_points": len(followers_data),
                "forecast_horizon_days": target_days
            }
        
        return {"error": "Unable to calculate forecast"}
    
    def get_progress_toward_targets(self) -> Dict[str, Any]:
        """Get progress toward weekly targets"""
        # Default SME Analytica growth targets
        targets = {
            "week_1": {"followers": 50, "engagements": 350, "demo_requests": 5, "business_inquiries": 3, "focus": "Foundation building and initial community engagement"},
            "week_2": {"followers": 150, "engagements": 490, "demo_requests": 10, "business_inquiries": 7, "focus": "Influencer outreach and relationship building"},
            "week_3": {"followers": 300, "engagements": 630, "demo_requests": 20, "business_inquiries": 15, "focus": "Viral amplification and thought leadership"},
            "week_4": {"followers": 500, "engagements": 700, "demo_requests": 30, "business_inquiries": 25, "focus": "Conversion optimization and customer acquisition"}
        }
        
        current_metrics = self.get_growth_trajectory(days=1)
        
        if not current_metrics:
            return {"error": "No current metrics available"}
        
        current = current_metrics[0]
        current_week = min(4, max(1, (current.account_age_days // 7) + 1))
        
        week_key = f"week_{current_week}"
        if week_key in targets:
            target = targets[week_key]
            
            return {
                "current_week": current_week,
                "target_followers": target["followers"],
                "actual_followers": current.followers_count,
                "follower_progress": (current.followers_count / target["followers"]) * 100,
                "target_engagements": target["engagements"],
                "target_demo_requests": target["demo_requests"],
                "target_business_inquiries": target["business_inquiries"],
                "focus_area": target["focus"],
                "days_remaining_in_week": 7 - (current.account_age_days % 7),
                "on_track": current.followers_count >= (target["followers"] * 0.8)
            }
        
        return {"error": "No targets found for current week"}

class PerformanceAnalytics:
    """Content performance analytics and optimization"""
    
    def __init__(self, db_path: str = "data/social_manager.db"):
        self.db_path = db_path
        self.hashtag_db_path = "data/hashtag_analytics.db"
        self.analytics_db_path = "data/analytics.db"
        self._init_performance_db()
    
    def _init_performance_db(self):
        """Initialize performance analytics database"""
        with sqlite3.connect(self.analytics_db_path) as conn:
            cursor = conn.cursor()
            
            # Content performance table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS content_performance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    content_id TEXT UNIQUE NOT NULL,
                    theme TEXT NOT NULL,
                    content_type TEXT NOT NULL,
                    posted_time TEXT NOT NULL,
                    likes INTEGER DEFAULT 0,
                    retweets INTEGER DEFAULT 0,
                    replies INTEGER DEFAULT 0,
                    quotes INTEGER DEFAULT 0,
                    impressions INTEGER DEFAULT 0,
                    engagement_rate REAL DEFAULT 0.0,
                    viral_score REAL DEFAULT 0.0,
                    conversion_actions INTEGER DEFAULT 0,
                    hashtags TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def record_content_performance(self, performance: ContentPerformance) -> bool:
        """Record content performance metrics"""
        try:
            with sqlite3.connect(self.analytics_db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO content_performance 
                    (content_id, theme, content_type, posted_time, likes, retweets, 
                     replies, quotes, impressions, engagement_rate, viral_score, 
                     conversion_actions, hashtags)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    performance.content_id,
                    performance.theme,
                    performance.content_type,
                    performance.posted_time.isoformat(),
                    performance.likes,
                    performance.retweets,
                    performance.replies,
                    performance.quotes,
                    performance.impressions,
                    performance.engagement_rate,
                    performance.viral_score,
                    performance.conversion_actions,
                    json.dumps(performance.hashtags) if performance.hashtags else None
                ))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error recording content performance: {e}")
            return False
    
    def get_top_performing_content(self, days: int = 30, limit: int = 10) -> List[ContentPerformance]:
        """Get top performing content by engagement rate"""
        try:
            with sqlite3.connect(self.analytics_db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM content_performance 
                    WHERE posted_time >= datetime('now', '-{} days')
                    ORDER BY viral_score DESC, engagement_rate DESC
                    LIMIT ?
                '''.format(days), (limit,))
                
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                
                performances = []
                for row in rows:
                    data = dict(zip(columns, row))
                    hashtags = json.loads(data['hashtags']) if data['hashtags'] else []
                    
                    performances.append(ContentPerformance(
                        content_id=data['content_id'],
                        theme=data['theme'],
                        content_type=data['content_type'],
                        posted_time=datetime.fromisoformat(data['posted_time']),
                        likes=data['likes'],
                        retweets=data['retweets'],
                        replies=data['replies'],
                        quotes=data['quotes'],
                        impressions=data['impressions'],
                        engagement_rate=data['engagement_rate'],
                        viral_score=data['viral_score'],
                        conversion_actions=data['conversion_actions'],
                        hashtags=hashtags
                    ))
                
                return performances
        except Exception as e:
            logger.error(f"Error getting top performing content: {e}")
            return []
    
    def analyze_content_patterns(self) -> Dict[str, Any]:
        """Analyze content performance patterns"""
        try:
            with sqlite3.connect(self.analytics_db_path) as conn:
                cursor = conn.cursor()
                
                # Theme performance analysis
                cursor.execute('''
                    SELECT theme, 
                           AVG(engagement_rate) as avg_engagement,
                           AVG(viral_score) as avg_viral_score,
                           COUNT(*) as content_count,
                           SUM(conversion_actions) as total_conversions
                    FROM content_performance 
                    GROUP BY theme
                    ORDER BY avg_engagement DESC
                ''')
                
                theme_performance = []
                for row in cursor.fetchall():
                    theme_performance.append({
                        "theme": row[0],
                        "avg_engagement": row[1],
                        "avg_viral_score": row[2],
                        "content_count": row[3],
                        "total_conversions": row[4]
                    })
                
                # Time-based analysis
                cursor.execute('''
                    SELECT strftime('%H', posted_time) as hour,
                           AVG(engagement_rate) as avg_engagement,
                           COUNT(*) as post_count
                    FROM content_performance 
                    GROUP BY hour
                    ORDER BY avg_engagement DESC
                    LIMIT 5
                ''')
                
                optimal_posting_times = []
                for row in cursor.fetchall():
                    optimal_posting_times.append({
                        "hour": int(row[0]),
                        "avg_engagement": row[1],
                        "post_count": row[2]
                    })
                
                return {
                    "theme_performance": theme_performance,
                    "optimal_posting_times": optimal_posting_times,
                    "analysis_timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error analyzing content patterns: {e}")
            return {}
    
    def calculate_viral_score(self, likes: int, retweets: int, replies: int, 
                            impressions: int, followers: int) -> float:
        """Calculate viral score for content"""
        if impressions == 0 or followers == 0:
            return 0.0
        
        # Engagement rate
        total_engagements = likes + retweets + replies
        engagement_rate = total_engagements / impressions if impressions > 0 else 0
        
        # Reach amplification (retweets extend reach)
        amplification_factor = 1 + (retweets / followers) if followers > 0 else 1
        
        # Viral score = engagement rate * amplification * 100
        viral_score = engagement_rate * amplification_factor * 100
        
        return min(viral_score, 100.0)  # Cap at 100
    
    def get_content_optimization_recommendations(self) -> List[str]:
        """Generate content optimization recommendations"""
        recommendations = []
        
        # Analyze patterns
        patterns = self.analyze_content_patterns()
        
        if patterns and "theme_performance" in patterns:
            theme_perf = patterns["theme_performance"]
            
            if theme_perf:
                best_theme = theme_perf[0]
                recommendations.append(
                    f"Focus more on '{best_theme['theme']}' content - "
                    f"it has {best_theme['avg_engagement']:.2f}% average engagement rate"
                )
                
                if len(theme_perf) > 1:
                    worst_theme = theme_perf[-1]
                    if worst_theme['avg_engagement'] < best_theme['avg_engagement'] * 0.5:
                        recommendations.append(
                            f"Optimize or reduce '{worst_theme['theme']}' content - "
                            f"it's underperforming with {worst_theme['avg_engagement']:.2f}% engagement"
                        )
        
        if patterns and "optimal_posting_times" in patterns:
            optimal_times = patterns["optimal_posting_times"]
            if optimal_times:
                best_time = optimal_times[0]
                recommendations.append(
                    f"Post more content at {best_time['hour']}:00 for optimal engagement "
                    f"({best_time['avg_engagement']:.2f}% avg engagement)"
                )
        
        # Hashtag recommendations
        try:
            with sqlite3.connect(self.hashtag_db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT hashtag, viral_score, engagement_rate 
                    FROM hashtag_performance 
                    ORDER BY viral_score DESC 
                    LIMIT 3
                ''')
                
                top_hashtags = cursor.fetchall()
                if top_hashtags:
                    hashtag_list = [row[0] for row in top_hashtags]
                    recommendations.append(
                        f"Use high-performing hashtags: {', '.join(hashtag_list)}"
                    )
        except Exception as e:
            logger.error(f"Error getting hashtag recommendations: {e}")
        
        return recommendations

class ROIMeasurement:
    """ROI measurement and conversion tracking"""
    
    def __init__(self, db_path: str = "data/social_manager.db"):
        self.db_path = db_path
        self.analytics_db_path = "data/analytics.db"
        self._init_roi_db()
    
    def _init_roi_db(self):
        """Initialize ROI tracking database"""
        with sqlite3.connect(self.analytics_db_path) as conn:
            cursor = conn.cursor()
            
            # ROI metrics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS roi_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    social_impressions INTEGER DEFAULT 0,
                    website_visits INTEGER DEFAULT 0,
                    demo_requests INTEGER DEFAULT 0,
                    business_inquiries INTEGER DEFAULT 0,
                    customers_acquired INTEGER DEFAULT 0,
                    revenue_generated REAL DEFAULT 0.0,
                    cost_per_acquisition REAL DEFAULT 0.0,
                    conversion_rate REAL DEFAULT 0.0,
                    roi_percentage REAL DEFAULT 0.0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Conversion funnel table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversion_funnel (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT,
                    stage TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    source_content_id TEXT,
                    conversion_value REAL DEFAULT 0.0,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def record_roi_metrics(self, metrics: ROIMetrics) -> bool:
        """Record ROI metrics"""
        try:
            with sqlite3.connect(self.analytics_db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO roi_metrics 
                    (timestamp, social_impressions, website_visits, demo_requests,
                     business_inquiries, customers_acquired, revenue_generated,
                     cost_per_acquisition, conversion_rate, roi_percentage)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    metrics.timestamp.isoformat(),
                    metrics.social_impressions,
                    metrics.website_visits,
                    metrics.demo_requests,
                    metrics.business_inquiries,
                    metrics.customers_acquired,
                    metrics.revenue_generated,
                    metrics.cost_per_acquisition,
                    metrics.conversion_rate,
                    metrics.roi_percentage
                ))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error recording ROI metrics: {e}")
            return False
    
    def track_conversion(self, user_id: str, stage: str, source_content_id: str = None, 
                        conversion_value: float = 0.0) -> bool:
        """Track conversion funnel events"""
        try:
            with sqlite3.connect(self.analytics_db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO conversion_funnel 
                    (user_id, stage, timestamp, source_content_id, conversion_value)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    user_id,
                    stage,
                    datetime.now().isoformat(),
                    source_content_id,
                    conversion_value
                ))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error tracking conversion: {e}")
            return False
    
    def calculate_current_roi(self) -> Dict[str, Any]:
        """Calculate current ROI metrics"""
        try:
            with sqlite3.connect(self.analytics_db_path) as conn:
                cursor = conn.cursor()
                
                # Get latest ROI metrics
                cursor.execute('''
                    SELECT * FROM roi_metrics 
                    ORDER BY timestamp DESC 
                    LIMIT 1
                ''')
                
                latest_row = cursor.fetchone()
                if not latest_row:
                    return {"error": "No ROI data available"}
                
                columns = [desc[0] for desc in cursor.description]
                latest_data = dict(zip(columns, latest_row))
                
                # Calculate conversion funnel
                cursor.execute('''
                    SELECT stage, COUNT(*) as count
                    FROM conversion_funnel 
                    WHERE timestamp >= datetime('now', '-30 days')
                    GROUP BY stage
                ''')
                
                funnel_data = {row[0]: row[1] for row in cursor.fetchall()}
                
                # Calculate conversion rates
                total_impressions = latest_data.get('social_impressions', 0)
                website_visits = latest_data.get('website_visits', 0)
                demo_requests = latest_data.get('demo_requests', 0)
                customers = latest_data.get('customers_acquired', 0)
                
                conversion_rates = {}
                if total_impressions > 0:
                    conversion_rates['impression_to_visit'] = (website_visits / total_impressions) * 100
                if website_visits > 0:
                    conversion_rates['visit_to_demo'] = (demo_requests / website_visits) * 100
                if demo_requests > 0:
                    conversion_rates['demo_to_customer'] = (customers / demo_requests) * 100
                if total_impressions > 0:
                    conversion_rates['impression_to_customer'] = (customers / total_impressions) * 100
                
                return {
                    "current_metrics": latest_data,
                    "conversion_funnel": funnel_data,
                    "conversion_rates": conversion_rates,
                    "roi_summary": {
                        "total_revenue": latest_data.get('revenue_generated', 0),
                        "total_customers": customers,
                        "cost_per_customer": latest_data.get('cost_per_acquisition', 0),
                        "roi_percentage": latest_data.get('roi_percentage', 0)
                    }
                }
                
        except Exception as e:
            logger.error(f"Error calculating ROI: {e}")
            return {"error": str(e)}
    
    def get_attribution_analysis(self) -> Dict[str, Any]:
        """Analyze which content drives conversions"""
        try:
            with sqlite3.connect(self.analytics_db_path) as conn:
                cursor = conn.cursor()
                
                # Content attribution analysis
                cursor.execute('''
                    SELECT cf.source_content_id, cp.theme, cp.content_type,
                           COUNT(*) as conversion_count,
                           SUM(cf.conversion_value) as total_value
                    FROM conversion_funnel cf
                    LEFT JOIN content_performance cp ON cf.source_content_id = cp.content_id
                    WHERE cf.source_content_id IS NOT NULL
                    GROUP BY cf.source_content_id
                    ORDER BY conversion_count DESC
                    LIMIT 10
                ''')
                
                content_attribution = []
                for row in cursor.fetchall():
                    content_attribution.append({
                        "content_id": row[0],
                        "theme": row[1],
                        "content_type": row[2],
                        "conversion_count": row[3],
                        "total_value": row[4]
                    })
                
                return {
                    "content_attribution": content_attribution,
                    "analysis_timestamp": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Error analyzing attribution: {e}")
            return {}

class AnalyticsDashboard:
    """Main analytics dashboard coordinating all analytics components"""
    
    def __init__(self, db_path: str = "data/social_manager.db"):
        self.db_path = db_path
        self.growth_tracker = GrowthTracker(db_path)
        self.performance_analytics = PerformanceAnalytics(db_path)
        self.roi_measurement = ROIMeasurement(db_path)
    
    def generate_comprehensive_report(self, weeks: int = 4) -> Dict[str, Any]:
        """Generate comprehensive analytics report"""
        report = {
            "report_generated": datetime.now().isoformat(),
            "report_period_weeks": weeks,
            "sme_analytica_context": "AI analytics platform for restaurants/hotels/retail"
        }
        
        # Growth analysis
        growth_forecast = self.growth_tracker.calculate_growth_forecast(target_days=weeks*7)
        progress_targets = self.growth_tracker.get_progress_toward_targets()
        
        report["growth_analysis"] = {
            "forecast": growth_forecast,
            "target_progress": progress_targets,
            "trajectory": [asdict(m) for m in self.growth_tracker.get_growth_trajectory(days=weeks*7)]
        }
        
        # Performance analysis
        top_content = self.performance_analytics.get_top_performing_content(days=weeks*7)
        content_patterns = self.performance_analytics.analyze_content_patterns()
        optimization_recommendations = self.performance_analytics.get_content_optimization_recommendations()
        
        report["performance_analysis"] = {
            "top_performing_content": [asdict(c) for c in top_content],
            "content_patterns": content_patterns,
            "optimization_recommendations": optimization_recommendations
        }
        
        # ROI analysis
        roi_metrics = self.roi_measurement.calculate_current_roi()
        attribution_analysis = self.roi_measurement.get_attribution_analysis()
        
        report["roi_analysis"] = {
            "current_roi": roi_metrics,
            "attribution": attribution_analysis
        }
        
        # Strategic recommendations
        report["strategic_recommendations"] = self._generate_strategic_recommendations(report)
        
        return report
    
    def _generate_strategic_recommendations(self, report_data: Dict[str, Any]) -> List[str]:
        """Generate strategic recommendations based on analytics"""
        recommendations = []
        
        # Growth recommendations
        if "growth_analysis" in report_data:
            growth_data = report_data["growth_analysis"]
            
            if "forecast" in growth_data and "confidence_score" in growth_data["forecast"]:
                confidence = growth_data["forecast"]["confidence_score"]
                if confidence < 70:
                    recommendations.append(
                        "Growth trajectory has low confidence - implement more consistent engagement strategies"
                    )
                
                if "daily_growth_rate" in growth_data["forecast"]:
                    daily_rate = growth_data["forecast"]["daily_growth_rate"]
                    if daily_rate < 5:
                        recommendations.append(
                            f"Current growth rate ({daily_rate:.1f} followers/day) is below target - "
                            "increase content frequency and community engagement"
                        )
            
            if "target_progress" in growth_data and "follower_progress" in growth_data["target_progress"]:
                progress = growth_data["target_progress"]["follower_progress"]
                if progress < 80:
                    recommendations.append(
                        f"Behind target ({progress:.1f}% of weekly goal) - "
                        "activate viral content strategies and influencer outreach"
                    )
        
        # Performance recommendations
        if "performance_analysis" in report_data:
            perf_data = report_data["performance_analysis"]
            recommendations.extend(perf_data.get("optimization_recommendations", []))
        
        # ROI recommendations
        if "roi_analysis" in report_data:
            roi_data = report_data["roi_analysis"]
            
            if "current_roi" in roi_data and "conversion_rates" in roi_data["current_roi"]:
                conversion_rates = roi_data["current_roi"]["conversion_rates"]
                
                if "impression_to_visit" in conversion_rates:
                    visit_rate = conversion_rates["impression_to_visit"]
                    if visit_rate < 2.0:
                        recommendations.append(
                            f"Low impression-to-visit rate ({visit_rate:.2f}%) - "
                            "improve call-to-action messaging and link placement"
                        )
                
                if "demo_to_customer" in conversion_rates:
                    demo_rate = conversion_rates["demo_to_customer"]
                    if demo_rate < 20.0:
                        recommendations.append(
                            f"Low demo-to-customer rate ({demo_rate:.2f}%) - "
                            "enhance demo experience and follow-up process"
                        )
        
        # SME Analytica specific recommendations
        recommendations.extend([
            "Highlight MenuFlow's 10% margin improvement in restaurant-focused content",
            "Share case studies showing real-time analytics impact on SME operations",
            "Create bilingual content (70% English, 30% Spanish) for broader reach",
            "Focus on Data Monday and Tech Thursday themes for higher engagement",
            "Demonstrate integration capabilities with existing POS systems",
            "Showcase AI-powered dynamic pricing benefits for small businesses",
            "Create content around vertical specialization for restaurants/hotels/retail",
            "Highlight user-friendly interface designed for non-technical business owners"
        ])
        
        return recommendations[:10]  # Limit to top 10 recommendations
    
    def generate_weekly_report(self, week_number: int = None) -> WeeklyReport:
        """Generate weekly analytics report"""
        if week_number is None:
            # Calculate current week based on account age
            growth_data = self.growth_tracker.get_growth_trajectory(days=1)
            if growth_data:
                week_number = min(4, max(1, (growth_data[0].account_age_days // 7) + 1))
            else:
                week_number = 1
        
        # Calculate week dates
        week_start = datetime.now() - timedelta(days=7)
        week_end = datetime.now()
        
        # Get metrics for the week
        weekly_growth = self.growth_tracker.get_growth_trajectory(days=7)
        follower_growth = weekly_growth[0].followers_count - weekly_growth[-1].followers_count if len(weekly_growth) > 1 else 0
        
        top_content = self.performance_analytics.get_top_performing_content(days=7, limit=5)
        roi_metrics = self.roi_measurement.calculate_current_roi()
        
        # Generate comprehensive report
        full_report = self.generate_comprehensive_report(weeks=1)
        
        return WeeklyReport(
            week_start=week_start,
            week_end=week_end,
            follower_growth=follower_growth,
            engagement_total=sum(c.likes + c.retweets + c.replies for c in top_content),
            top_performing_content=top_content,
            conversion_metrics=ROIMetrics(
                timestamp=datetime.now(),
                social_impressions=roi_metrics.get("current_metrics", {}).get("social_impressions", 0),
                website_visits=roi_metrics.get("current_metrics", {}).get("website_visits", 0),
                demo_requests=roi_metrics.get("current_metrics", {}).get("demo_requests", 0),
                business_inquiries=roi_metrics.get("current_metrics", {}).get("business_inquiries", 0),
                customers_acquired=roi_metrics.get("current_metrics", {}).get("customers_acquired", 0),
                revenue_generated=roi_metrics.get("current_metrics", {}).get("revenue_generated", 0.0),
                cost_per_acquisition=roi_metrics.get("current_metrics", {}).get("cost_per_acquisition", 0.0),
                conversion_rate=roi_metrics.get("current_metrics", {}).get("conversion_rate", 0.0),
                roi_percentage=roi_metrics.get("current_metrics", {}).get("roi_percentage", 0.0)
            ),
            recommendations=full_report.get("strategic_recommendations", []),
            growth_forecast=full_report.get("growth_analysis", {}).get("forecast", {}),
            competitive_analysis={"status": "Coming soon - competitor benchmarking system"}
        )
    
    def get_real_time_dashboard(self) -> Dict[str, Any]:
        """Get real-time dashboard data"""
        dashboard = {
            "timestamp": datetime.now().isoformat(),
            "status": "active"
        }
        
        # Current metrics
        current_growth = self.growth_tracker.get_growth_trajectory(days=1)
        if current_growth:
            dashboard["current_metrics"] = asdict(current_growth[0])
        
        # Progress indicators
        progress = self.growth_tracker.get_progress_toward_targets()
        dashboard["target_progress"] = progress
        
        # Recent top content
        recent_content = self.performance_analytics.get_top_performing_content(days=7, limit=3)
        dashboard["recent_top_content"] = [asdict(c) for c in recent_content]
        
        # Quick ROI summary
        roi_data = self.roi_measurement.calculate_current_roi()
        dashboard["roi_summary"] = roi_data.get("roi_summary", {})
        
        # Immediate recommendations
        recommendations = self.performance_analytics.get_content_optimization_recommendations()
        dashboard["immediate_actions"] = recommendations[:3]
        
        return dashboard
    
    def export_analytics_data(self, format: str = "json") -> str:
        """Export analytics data for external analysis"""
        comprehensive_report = self.generate_comprehensive_report()
        
        if format.lower() == "json":
            return json.dumps(comprehensive_report, indent=2, default=str)
        else:
            return str(comprehensive_report)

# Demo and testing functions
def demo_analytics_dashboard():
    """Demonstrate the analytics dashboard functionality"""
    print("SME Analytica Analytics Dashboard Demo")
    print("=" * 50)
    
    # Initialize dashboard
    dashboard = AnalyticsDashboard()
    
    # Create sample data
    sample_growth = GrowthMetrics(
        timestamp=datetime.now(),
        followers_count=8,
        following_count=16,
        tweet_count=25,
        listed_count=0,
        account_age_days=75,
        growth_rate_followers=0.0,
        growth_rate_tweets=0.0,
        engagement_rate=2.5,
        reach=150,
        impressions=300
    )
    
    # Record sample data
    dashboard.growth_tracker.record_growth_metrics(sample_growth)
    
    # Generate reports
    print("\n1. Real-time Dashboard:")
    real_time = dashboard.get_real_time_dashboard()
    print(json.dumps(real_time, indent=2, default=str))
    
    print("\n2. Growth Forecast:")
    forecast = dashboard.growth_tracker.calculate_growth_forecast()
    print(json.dumps(forecast, indent=2))
    
    print("\n3. Strategic Recommendations:")
    report = dashboard.generate_comprehensive_report(weeks=1)
    for i, rec in enumerate(report.get("strategic_recommendations", [])[:5], 1):
        print(f"{i}. {rec}")
    
    print("\nAnalytics Dashboard Demo Complete!")

if __name__ == "__main__":
    demo_analytics_dashboard()