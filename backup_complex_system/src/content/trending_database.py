"""
Trending Topics Database and Tracking System for SME Analytica
Persistent storage and analysis of trending topics and viral opportunities
"""

import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
import logging
from collections import defaultdict
import os

# Import viral optimization types
from src.content.viral_optimization import TrendingTopic, TrendType, ViralPotential

class TrendingTopicsDatabase:
    """Database for tracking trending topics and their performance"""
    
    def __init__(self, db_path: str = "data/trending_topics.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Initialize the trending topics database"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Trending topics table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS trending_topics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        topic TEXT NOT NULL,
                        trend_type TEXT NOT NULL,
                        volume INTEGER DEFAULT 0,
                        growth_rate REAL DEFAULT 0.0,
                        viral_potential TEXT NOT NULL,
                        relevance_score REAL DEFAULT 0.0,
                        industry_connection TEXT,
                        hashtags TEXT,
                        context TEXT,
                        discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        expires_at TIMESTAMP,
                        optimal_timing TIMESTAMP,
                        is_active BOOLEAN DEFAULT 1
                    )
                """)
                
                # Content performance table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS content_performance (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        trend_id INTEGER,
                        content_text TEXT NOT NULL,
                        viral_score REAL DEFAULT 0.0,
                        estimated_reach INTEGER DEFAULT 0,
                        actual_likes INTEGER DEFAULT 0,
                        actual_retweets INTEGER DEFAULT 0,
                        actual_replies INTEGER DEFAULT 0,
                        hashtags TEXT,
                        posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        performance_tracked BOOLEAN DEFAULT 0,
                        FOREIGN KEY (trend_id) REFERENCES trending_topics (id)
                    )
                """)
                
                # Hashtag performance tracking
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS hashtag_performance (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        hashtag TEXT NOT NULL,
                        volume INTEGER DEFAULT 0,
                        avg_engagement REAL DEFAULT 0.0,
                        viral_potential TEXT NOT NULL,
                        last_analyzed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        recommendation TEXT
                    )
                """)
                
                # Viral opportunities log
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS viral_opportunities (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        opportunity_type TEXT NOT NULL,
                        priority REAL DEFAULT 0.0,
                        trend_topic TEXT,
                        content_preview TEXT,
                        optimal_posting_time TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        used BOOLEAN DEFAULT 0,
                        performance_rating INTEGER DEFAULT 0
                    )
                """)
                
                # Analytics summary table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS analytics_summary (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date DATE NOT NULL,
                        trends_monitored INTEGER DEFAULT 0,
                        high_potential_trends INTEGER DEFAULT 0,
                        content_generated INTEGER DEFAULT 0,
                        avg_viral_score REAL DEFAULT 0.0,
                        total_estimated_reach INTEGER DEFAULT 0,
                        UNIQUE(date)
                    )
                """)
                
                # Create indexes for better performance
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_trending_topics_discovered ON trending_topics(discovered_at)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_trending_topics_active ON trending_topics(is_active)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_content_performance_posted ON content_performance(posted_at)")
                cursor.execute("CREATE INDEX IF NOT EXISTS idx_hashtag_performance_hashtag ON hashtag_performance(hashtag)")
                
                conn.commit()
                self.logger.info("Trending topics database initialized successfully")
                
        except Exception as e:
            self.logger.error(f"Error initializing database: {e}")
            raise
    
    def store_trending_topic(self, topic: TrendingTopic) -> int:
        """Store a trending topic in the database"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Convert hashtags list to JSON string
                hashtags_json = json.dumps(topic.hashtags) if topic.hashtags else "[]"
                
                cursor.execute("""
                    INSERT INTO trending_topics (
                        topic, trend_type, volume, growth_rate, viral_potential,
                        relevance_score, industry_connection, hashtags, context,
                        discovered_at, expires_at, optimal_timing
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    topic.topic,
                    topic.trend_type.value,
                    topic.volume,
                    topic.growth_rate,
                    topic.viral_potential.value,
                    topic.relevance_score,
                    topic.industry_connection,
                    hashtags_json,
                    topic.context,
                    topic.discovered_at,
                    topic.expires_at,
                    topic.optimal_timing
                ))
                
                topic_id = cursor.lastrowid
                conn.commit()
                
                self.logger.info(f"Stored trending topic: {topic.topic} with ID {topic_id}")
                return topic_id
                
        except Exception as e:
            self.logger.error(f"Error storing trending topic: {e}")
            return -1
    
    def get_active_trending_topics(self, limit: int = 20) -> List[TrendingTopic]:
        """Get currently active trending topics"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get active topics from last 24 hours
                cutoff_time = datetime.now() - timedelta(hours=24)
                
                cursor.execute("""
                    SELECT * FROM trending_topics 
                    WHERE is_active = 1 AND discovered_at > ?
                    ORDER BY relevance_score * 
                        CASE viral_potential 
                            WHEN 'viral' THEN 4 
                            WHEN 'high' THEN 3 
                            WHEN 'medium' THEN 2 
                            ELSE 1 
                        END DESC
                    LIMIT ?
                """, (cutoff_time, limit))
                
                rows = cursor.fetchall()
                topics = []
                
                for row in rows:
                    # Parse hashtags from JSON
                    hashtags = json.loads(row[8]) if row[8] else []
                    
                    topic = TrendingTopic(
                        topic=row[1],
                        trend_type=TrendType(row[2]),
                        volume=row[3],
                        growth_rate=row[4],
                        viral_potential=ViralPotential(row[5]),
                        relevance_score=row[6],
                        industry_connection=row[7],
                        optimal_timing=datetime.fromisoformat(row[11]) if row[11] else datetime.now(),
                        hashtags=hashtags,
                        context=row[9],
                        discovered_at=datetime.fromisoformat(row[10]),
                        expires_at=datetime.fromisoformat(row[12]) if row[12] else None
                    )
                    topics.append(topic)
                
                return topics
                
        except Exception as e:
            self.logger.error(f"Error getting active trending topics: {e}")
            return []
    
    def store_content_performance(self, content_data: Dict[str, Any], trend_id: Optional[int] = None) -> int:
        """Store content performance data"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                hashtags_json = json.dumps(content_data.get("hashtags", []))
                
                cursor.execute("""
                    INSERT INTO content_performance (
                        trend_id, content_text, viral_score, estimated_reach,
                        hashtags, posted_at
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    trend_id,
                    content_data.get("text", ""),
                    content_data.get("viral_score", 0.0),
                    content_data.get("estimated_reach", 0),
                    hashtags_json,
                    datetime.now()
                ))
                
                performance_id = cursor.lastrowid
                conn.commit()
                
                return performance_id
                
        except Exception as e:
            self.logger.error(f"Error storing content performance: {e}")
            return -1
    
    def update_actual_performance(self, performance_id: int, likes: int, retweets: int, replies: int):
        """Update actual performance metrics for content"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE content_performance 
                    SET actual_likes = ?, actual_retweets = ?, actual_replies = ?,
                        performance_tracked = 1
                    WHERE id = ?
                """, (likes, retweets, replies, performance_id))
                
                conn.commit()
                self.logger.info(f"Updated performance for content ID {performance_id}")
                
        except Exception as e:
            self.logger.error(f"Error updating performance: {e}")
    
    def store_hashtag_analysis(self, hashtag: str, analysis_data: Dict[str, Any]):
        """Store hashtag performance analysis"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if hashtag already exists
                cursor.execute("SELECT id FROM hashtag_performance WHERE hashtag = ?", (hashtag,))
                existing = cursor.fetchone()
                
                if existing:
                    # Update existing record
                    cursor.execute("""
                        UPDATE hashtag_performance 
                        SET volume = ?, avg_engagement = ?, viral_potential = ?,
                            last_analyzed = ?, recommendation = ?
                        WHERE hashtag = ?
                    """, (
                        analysis_data.get("volume", 0),
                        analysis_data.get("avg_engagement", 0.0),
                        analysis_data.get("viral_potential", "low"),
                        datetime.now(),
                        analysis_data.get("recommendation", ""),
                        hashtag
                    ))
                else:
                    # Insert new record
                    cursor.execute("""
                        INSERT INTO hashtag_performance (
                            hashtag, volume, avg_engagement, viral_potential, recommendation
                        ) VALUES (?, ?, ?, ?, ?)
                    """, (
                        hashtag,
                        analysis_data.get("volume", 0),
                        analysis_data.get("avg_engagement", 0.0),
                        analysis_data.get("viral_potential", "low"),
                        analysis_data.get("recommendation", "")
                    ))
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Error storing hashtag analysis: {e}")
    
    def store_viral_opportunity(self, opportunity_data: Dict[str, Any]) -> int:
        """Store a viral opportunity"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO viral_opportunities (
                        opportunity_type, priority, trend_topic, content_preview,
                        optimal_posting_time
                    ) VALUES (?, ?, ?, ?, ?)
                """, (
                    opportunity_data.get("type", "general"),
                    opportunity_data.get("priority", 5.0),
                    opportunity_data.get("trend_topic"),
                    opportunity_data.get("content_preview", "")[:200],  # Limit preview length
                    opportunity_data.get("optimal_posting_time", datetime.now())
                ))
                
                opp_id = cursor.lastrowid
                conn.commit()
                
                return opp_id
                
        except Exception as e:
            self.logger.error(f"Error storing viral opportunity: {e}")
            return -1
    
    def get_viral_opportunities(self, limit: int = 10, unused_only: bool = True) -> List[Dict[str, Any]]:
        """Get viral opportunities"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT * FROM viral_opportunities 
                    WHERE optimal_posting_time > ?
                """
                params = [datetime.now()]
                
                if unused_only:
                    query += " AND used = 0"
                
                query += " ORDER BY priority DESC LIMIT ?"
                params.append(limit)
                
                cursor.execute(query, params)
                rows = cursor.fetchall()
                
                opportunities = []
                for row in rows:
                    opp = {
                        "id": row[0],
                        "type": row[1],
                        "priority": row[2],
                        "trend_topic": row[3],
                        "content_preview": row[4],
                        "optimal_posting_time": datetime.fromisoformat(row[5]) if row[5] else None,
                        "created_at": datetime.fromisoformat(row[6]) if row[6] else None,
                        "used": bool(row[7]),
                        "performance_rating": row[8]
                    }
                    opportunities.append(opp)
                
                return opportunities
                
        except Exception as e:
            self.logger.error(f"Error getting viral opportunities: {e}")
            return []
    
    def mark_opportunity_used(self, opportunity_id: int, performance_rating: int = 0):
        """Mark a viral opportunity as used"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE viral_opportunities 
                    SET used = 1, performance_rating = ?
                    WHERE id = ?
                """, (performance_rating, opportunity_id))
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Error marking opportunity as used: {e}")
    
    def update_daily_analytics(self, date: datetime, analytics_data: Dict[str, Any]):
        """Update daily analytics summary"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                date_str = date.strftime("%Y-%m-%d")
                
                cursor.execute("""
                    INSERT OR REPLACE INTO analytics_summary (
                        date, trends_monitored, high_potential_trends,
                        content_generated, avg_viral_score, total_estimated_reach
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    date_str,
                    analytics_data.get("trends_monitored", 0),
                    analytics_data.get("high_potential_trends", 0),
                    analytics_data.get("content_generated", 0),
                    analytics_data.get("avg_viral_score", 0.0),
                    analytics_data.get("total_estimated_reach", 0)
                ))
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Error updating daily analytics: {e}")
    
    def get_analytics_summary(self, days: int = 7) -> Dict[str, Any]:
        """Get analytics summary for the specified number of days"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get data for last N days
                start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
                
                # Daily analytics
                cursor.execute("""
                    SELECT * FROM analytics_summary 
                    WHERE date >= ?
                    ORDER BY date DESC
                """, (start_date,))
                
                daily_data = cursor.fetchall()
                
                # Overall metrics
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_trends,
                        AVG(relevance_score) as avg_relevance,
                        COUNT(CASE WHEN viral_potential IN ('high', 'viral') THEN 1 END) as high_potential_count
                    FROM trending_topics 
                    WHERE discovered_at >= ?
                """, (start_date,))
                
                trend_metrics = cursor.fetchone()
                
                # Content performance
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_content,
                        AVG(viral_score) as avg_viral_score,
                        SUM(estimated_reach) as total_estimated_reach,
                        AVG(actual_likes) as avg_likes,
                        AVG(actual_retweets) as avg_retweets
                    FROM content_performance 
                    WHERE posted_at >= ?
                """, (start_date,))
                
                content_metrics = cursor.fetchone()
                
                # Top performing hashtags
                cursor.execute("""
                    SELECT hashtag, avg_engagement, viral_potential
                    FROM hashtag_performance 
                    WHERE last_analyzed >= ?
                    ORDER BY avg_engagement DESC
                    LIMIT 10
                """, (start_date,))
                
                top_hashtags = cursor.fetchall()
                
                return {
                    "period_days": days,
                    "daily_analytics": [
                        {
                            "date": row[1],
                            "trends_monitored": row[2],
                            "high_potential_trends": row[3],
                            "content_generated": row[4],
                            "avg_viral_score": row[5],
                            "total_estimated_reach": row[6]
                        } for row in daily_data
                    ],
                    "trend_metrics": {
                        "total_trends_monitored": trend_metrics[0] if trend_metrics else 0,
                        "avg_relevance_score": round(trend_metrics[1], 2) if trend_metrics[1] else 0,
                        "high_potential_trends": trend_metrics[2] if trend_metrics else 0
                    },
                    "content_metrics": {
                        "total_content_generated": content_metrics[0] if content_metrics else 0,
                        "avg_viral_score": round(content_metrics[1], 2) if content_metrics[1] else 0,
                        "total_estimated_reach": content_metrics[2] if content_metrics else 0,
                        "avg_actual_likes": round(content_metrics[3], 1) if content_metrics[3] else 0,
                        "avg_actual_retweets": round(content_metrics[4], 1) if content_metrics[4] else 0
                    },
                    "top_hashtags": [
                        {
                            "hashtag": row[0],
                            "avg_engagement": row[1],
                            "viral_potential": row[2]
                        } for row in top_hashtags
                    ]
                }
                
        except Exception as e:
            self.logger.error(f"Error getting analytics summary: {e}")
            return {}
    
    def cleanup_old_data(self, days_to_keep: int = 30):
        """Clean up old trending topics and performance data"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cutoff_date = datetime.now() - timedelta(days=days_to_keep)
                
                # Deactivate old trending topics
                cursor.execute("""
                    UPDATE trending_topics 
                    SET is_active = 0 
                    WHERE discovered_at < ?
                """, (cutoff_date,))
                
                # Delete very old performance data
                very_old_cutoff = datetime.now() - timedelta(days=days_to_keep * 2)
                cursor.execute("""
                    DELETE FROM content_performance 
                    WHERE posted_at < ?
                """, (very_old_cutoff,))
                
                # Clean up old viral opportunities
                cursor.execute("""
                    DELETE FROM viral_opportunities 
                    WHERE created_at < ? AND used = 1
                """, (very_old_cutoff,))
                
                conn.commit()
                self.logger.info(f"Cleaned up data older than {days_to_keep} days")
                
        except Exception as e:
            self.logger.error(f"Error cleaning up old data: {e}")
    
    def get_trending_history(self, topic: str) -> List[Dict[str, Any]]:
        """Get historical data for a specific topic"""
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT discovered_at, viral_potential, relevance_score, volume, growth_rate
                    FROM trending_topics 
                    WHERE topic LIKE ?
                    ORDER BY discovered_at DESC
                    LIMIT 50
                """, (f"%{topic}%",))
                
                rows = cursor.fetchall()
                
                history = []
                for row in rows:
                    history.append({
                        "discovered_at": row[0],
                        "viral_potential": row[1],
                        "relevance_score": row[2],
                        "volume": row[3],
                        "growth_rate": row[4]
                    })
                
                return history
                
        except Exception as e:
            self.logger.error(f"Error getting trending history: {e}")
            return []