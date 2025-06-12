#!/usr/bin/env python3
"""
SME Analytica Analytics Dashboard Demonstration
Comprehensive demo showing all analytics features and capabilities.
"""

import sys
import os
import json
from datetime import datetime, timedelta
from pathlib import Path

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from analytics.analytics_dashboard import (
    AnalyticsDashboard, GrowthTracker, PerformanceAnalytics, ROIMeasurement,
    GrowthMetrics, ContentPerformance, ROIMetrics
)

def create_sample_data(dashboard: AnalyticsDashboard):
    """Create comprehensive sample data for demonstration"""
    print("Creating sample analytics data...")
    
    # Sample growth metrics over time
    base_date = datetime.now() - timedelta(days=30)
    follower_progression = [8, 12, 18, 25, 35, 45, 60, 75, 95, 120, 150, 180, 220, 250, 290, 330, 380, 430, 480, 520]
    
    for i, followers in enumerate(follower_progression):
        metrics = GrowthMetrics(
            timestamp=base_date + timedelta(days=i*1.5),
            followers_count=followers,
            following_count=16 + i,
            tweet_count=25 + i*2,
            listed_count=i//5,
            account_age_days=75 + i,
            growth_rate_followers=((followers - (follower_progression[i-1] if i > 0 else 8)) / (follower_progression[i-1] if i > 0 else 8)) * 100 if i > 0 else 0,
            growth_rate_tweets=2.0 + (i * 0.1),
            engagement_rate=2.5 + (i * 0.3),
            reach=followers * 15,
            impressions=followers * 25
        )
        dashboard.growth_tracker.record_growth_metrics(metrics)
    
    # Sample content performance data
    themes = ["data_monday", "tech_thursday", "case_wednesday", "talk_tuesday", "fact_friday"]
    content_types = ["educational", "case_study", "industry_insight", "product_feature", "community_engagement"]
    
    for i in range(50):
        performance = ContentPerformance(
            content_id=f"content_{i+1}",
            theme=themes[i % len(themes)],
            content_type=content_types[i % len(content_types)],
            posted_time=base_date + timedelta(days=i*0.6),
            likes=10 + (i * 2) + (5 if themes[i % len(themes)] == "case_wednesday" else 0),
            retweets=2 + i + (3 if themes[i % len(themes)] == "tech_thursday" else 0),
            replies=1 + (i // 2),
            quotes=i // 5,
            impressions=200 + (i * 15),
            engagement_rate=((10 + (i * 2)) / (200 + (i * 15))) * 100,
            conversion_actions=i // 10,
            hashtags=["#SMEAnalytica", "#AIforSMEs", "#DataInsights", "#SmallBusiness"]
        )
        performance.viral_score = dashboard.performance_analytics.calculate_viral_score(
            performance.likes, performance.retweets, performance.replies,
            performance.impressions, follower_progression[min(i//3, len(follower_progression)-1)]
        )
        dashboard.performance_analytics.record_content_performance(performance)
    
    # Sample ROI metrics
    for i in range(10):
        roi_metrics = ROIMetrics(
            timestamp=base_date + timedelta(days=i*3),
            social_impressions=5000 + (i * 1000),
            website_visits=150 + (i * 25),
            demo_requests=5 + i,
            business_inquiries=3 + i,
            customers_acquired=1 + (i // 3),
            revenue_generated=2500.0 * (1 + (i // 3)),
            cost_per_acquisition=150.0 - (i * 5),
            conversion_rate=((5 + i) / (150 + (i * 25))) * 100,
            roi_percentage=((2500.0 * (1 + (i // 3))) / (150.0 * (5 + i))) * 100
        )
        dashboard.roi_measurement.record_roi_metrics(roi_metrics)
    
    # Sample conversion tracking
    for i in range(30):
        dashboard.roi_measurement.track_conversion(
            user_id=f"user_{i+1}",
            stage="awareness" if i < 20 else "interest" if i < 25 else "intent",
            source_content_id=f"content_{(i % 50) + 1}",
            conversion_value=100.0 if i > 25 else 0.0
        )
    
    print("Sample data created successfully!")

def demonstrate_growth_tracking(dashboard: AnalyticsDashboard):
    """Demonstrate growth tracking capabilities"""
    print("\n" + "="*60)
    print("GROWTH TRACKING DEMONSTRATION")
    print("="*60)
    
    # Current growth trajectory
    print("\n1. CURRENT GROWTH TRAJECTORY (Last 30 days):")
    trajectory = dashboard.growth_tracker.get_growth_trajectory(days=30)
    if trajectory:
        print(f"   • Current Followers: {trajectory[0].followers_count}")
        print(f"   • Engagement Rate: {trajectory[0].engagement_rate:.2f}%")
        print(f"   • Growth Rate: {trajectory[0].growth_rate_followers:.2f}%")
        print(f"   • Account Age: {trajectory[0].account_age_days} days")
        print(f"   • Total Impressions: {trajectory[0].impressions:,}")
    
    # Growth forecast
    print("\n2. GROWTH FORECAST (Next 28 days):")
    forecast = dashboard.growth_tracker.calculate_growth_forecast(target_days=28)
    if "error" not in forecast:
        print(f"   • Current Followers: {forecast['current_followers']}")
        print(f"   • Forecasted Followers: {forecast['forecasted_followers']}")
        print(f"   • Growth Needed: {forecast['growth_needed']} followers")
        print(f"   • Daily Growth Rate: {forecast['daily_growth_rate']:.1f} followers/day")
        print(f"   • Weekly Growth Rate: {forecast['weekly_growth_rate']:.1f} followers/week")
        print(f"   • Forecast Confidence: {forecast['confidence_score']:.1f}%")
        print(f"   • Model: {forecast['model']}")
    else:
        print(f"   • Error: {forecast['error']}")
    
    # Progress toward targets
    print("\n3. PROGRESS TOWARD WEEKLY TARGETS:")
    progress = dashboard.growth_tracker.get_progress_toward_targets()
    if "error" not in progress:
        print(f"   • Current Week: {progress['current_week']}")
        print(f"   • Target Followers: {progress['target_followers']}")
        print(f"   • Actual Followers: {progress['actual_followers']}")
        print(f"   • Progress: {progress['follower_progress']:.1f}%")
        print(f"   • On Track: {'✅' if progress['on_track'] else '❌'}")
        print(f"   • Focus Area: {progress['focus_area']}")
        print(f"   • Days Remaining: {progress['days_remaining_in_week']}")
    else:
        print(f"   • Error: {progress['error']}")

def demonstrate_performance_analytics(dashboard: AnalyticsDashboard):
    """Demonstrate performance analytics capabilities"""
    print("\n" + "="*60)
    print("PERFORMANCE ANALYTICS DEMONSTRATION")
    print("="*60)
    
    # Top performing content
    print("\n1. TOP PERFORMING CONTENT (Last 30 days):")
    top_content = dashboard.performance_analytics.get_top_performing_content(days=30, limit=5)
    for i, content in enumerate(top_content, 1):
        print(f"   {i}. Content ID: {content.content_id}")
        print(f"      • Theme: {content.theme}")
        print(f"      • Type: {content.content_type}")
        print(f"      • Engagement Rate: {content.engagement_rate:.2f}%")
        print(f"      • Viral Score: {content.viral_score:.1f}")
        print(f"      • Likes: {content.likes}, Retweets: {content.retweets}, Replies: {content.replies}")
        print(f"      • Impressions: {content.impressions:,}")
        print()
    
    # Content patterns analysis
    print("2. CONTENT PATTERNS ANALYSIS:")
    patterns = dashboard.performance_analytics.analyze_content_patterns()
    if patterns and "theme_performance" in patterns:
        print("   Theme Performance Rankings:")
        for i, theme in enumerate(patterns["theme_performance"], 1):
            print(f"   {i}. {theme['theme']}: {theme['avg_engagement']:.2f}% avg engagement "
                  f"({theme['content_count']} posts, {theme['total_conversions']} conversions)")
    
    if patterns and "optimal_posting_times" in patterns:
        print("\n   Optimal Posting Times:")
        for i, time in enumerate(patterns["optimal_posting_times"], 1):
            print(f"   {i}. {time['hour']}:00 - {time['avg_engagement']:.2f}% avg engagement "
                  f"({time['post_count']} posts)")
    
    # Optimization recommendations
    print("\n3. CONTENT OPTIMIZATION RECOMMENDATIONS:")
    recommendations = dashboard.performance_analytics.get_content_optimization_recommendations()
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")

def demonstrate_roi_measurement(dashboard: AnalyticsDashboard):
    """Demonstrate ROI measurement capabilities"""
    print("\n" + "="*60)
    print("ROI MEASUREMENT DEMONSTRATION")
    print("="*60)
    
    # Current ROI metrics
    print("\n1. CURRENT ROI METRICS:")
    roi_data = dashboard.roi_measurement.calculate_current_roi()
    if "error" not in roi_data:
        roi_summary = roi_data.get("roi_summary", {})
        print(f"   • Total Revenue: ${roi_summary.get('total_revenue', 0):,.2f}")
        print(f"   • Total Customers: {roi_summary.get('total_customers', 0)}")
        print(f"   • Cost per Customer: ${roi_summary.get('cost_per_customer', 0):,.2f}")
        print(f"   • ROI Percentage: {roi_summary.get('roi_percentage', 0):.1f}%")
        
        conversion_rates = roi_data.get("conversion_rates", {})
        print(f"\n   Conversion Funnel:")
        for stage, rate in conversion_rates.items():
            print(f"   • {stage.replace('_', ' ').title()}: {rate:.2f}%")
        
        funnel_data = roi_data.get("conversion_funnel", {})
        if funnel_data:
            print(f"\n   Conversion Funnel Counts (Last 30 days):")
            for stage, count in funnel_data.items():
                print(f"   • {stage.title()}: {count}")
    else:
        print(f"   • Error: {roi_data['error']}")
    
    # Attribution analysis
    print("\n2. CONTENT ATTRIBUTION ANALYSIS:")
    attribution = dashboard.roi_measurement.get_attribution_analysis()
    if attribution and "content_attribution" in attribution:
        print("   Top Converting Content:")
        for i, content in enumerate(attribution["content_attribution"][:5], 1):
            print(f"   {i}. Content ID: {content['content_id']}")
            print(f"      • Theme: {content['theme']}")
            print(f"      • Type: {content['content_type']}")
            print(f"      • Conversions: {content['conversion_count']}")
            print(f"      • Total Value: ${content['total_value']:.2f}")
            print()

def demonstrate_comprehensive_reporting(dashboard: AnalyticsDashboard):
    """Demonstrate comprehensive reporting capabilities"""
    print("\n" + "="*60)
    print("COMPREHENSIVE REPORTING DEMONSTRATION")
    print("="*60)
    
    # Real-time dashboard
    print("\n1. REAL-TIME DASHBOARD:")
    real_time = dashboard.get_real_time_dashboard()
    print(f"   • Status: {real_time.get('status', 'Unknown')}")
    print(f"   • Timestamp: {real_time.get('timestamp', 'N/A')}")
    
    current_metrics = real_time.get("current_metrics", {})
    if current_metrics:
        print(f"   • Current Followers: {current_metrics.get('followers_count', 0)}")
        print(f"   • Engagement Rate: {current_metrics.get('engagement_rate', 0):.2f}%")
        print(f"   • Total Impressions: {current_metrics.get('impressions', 0):,}")
    
    target_progress = real_time.get("target_progress", {})
    if target_progress and "error" not in target_progress:
        print(f"   • Week {target_progress.get('current_week', 0)} Progress: {target_progress.get('follower_progress', 0):.1f}%")
        print(f"   • On Track: {'✅' if target_progress.get('on_track', False) else '❌'}")
    
    immediate_actions = real_time.get("immediate_actions", [])
    if immediate_actions:
        print(f"\n   Immediate Actions Needed:")
        for i, action in enumerate(immediate_actions, 1):
            print(f"   {i}. {action}")
    
    # Weekly report
    print("\n2. WEEKLY REPORT:")
    weekly_report = dashboard.generate_weekly_report()
    print(f"   • Report Period: {weekly_report.week_start.strftime('%Y-%m-%d')} to {weekly_report.week_end.strftime('%Y-%m-%d')}")
    print(f"   • Follower Growth: {weekly_report.follower_growth}")
    print(f"   • Total Engagement: {weekly_report.engagement_total}")
    print(f"   • Demo Requests: {weekly_report.conversion_metrics.demo_requests}")
    print(f"   • Business Inquiries: {weekly_report.conversion_metrics.business_inquiries}")
    print(f"   • Revenue Generated: ${weekly_report.conversion_metrics.revenue_generated:,.2f}")
    
    print(f"\n   Top Performing Content This Week:")
    for i, content in enumerate(weekly_report.top_performing_content[:3], 1):
        print(f"   {i}. {content.theme} ({content.content_type}) - {content.viral_score:.1f} viral score")
    
    print(f"\n   Weekly Strategic Recommendations:")
    for i, rec in enumerate(weekly_report.recommendations[:5], 1):
        print(f"   {i}. {rec}")
    
    # Comprehensive report
    print("\n3. COMPREHENSIVE ANALYTICS REPORT:")
    comprehensive = dashboard.generate_comprehensive_report(weeks=4)
    
    print(f"   • Report Generated: {comprehensive.get('report_generated', 'N/A')}")
    print(f"   • Report Period: {comprehensive.get('report_period_weeks', 0)} weeks")
    print(f"   • Context: {comprehensive.get('sme_analytica_context', 'N/A')}")
    
    growth_analysis = comprehensive.get("growth_analysis", {})
    if growth_analysis:
        forecast = growth_analysis.get("forecast", {})
        if forecast and "error" not in forecast:
            print(f"   • Forecasted Growth: {forecast.get('growth_needed', 0)} followers needed")
            print(f"   • Daily Growth Target: {forecast.get('daily_growth_rate', 0):.1f} followers/day")
            print(f"   • Forecast Confidence: {forecast.get('confidence_score', 0):.1f}%")
    
    strategic_recs = comprehensive.get("strategic_recommendations", [])
    print(f"\n   Strategic Recommendations ({len(strategic_recs)} total):")
    for i, rec in enumerate(strategic_recs[:8], 1):
        print(f"   {i}. {rec}")

def demonstrate_sme_analytica_specific_features(dashboard: AnalyticsDashboard):
    """Demonstrate SME Analytica specific analytics features"""
    print("\n" + "="*60)
    print("SME ANALYTICA SPECIFIC FEATURES")
    print("="*60)
    
    print("\n1. BUSINESS CONTEXT INTEGRATION:")
    print("   • Company: SME Analytica - AI analytics platform")
    print("   • Target: Restaurants, Hotels, Retail SMEs")
    print("   • Current State: 8 followers → 500+ followers in 4 weeks")
    print("   • Focus: Generate demo requests and customers from social media")
    
    print("\n2. CONTENT THEME PERFORMANCE:")
    from config.settings import sme_context
    themes = sme_context.CONTENT_THEMES
    for theme, description in themes.items():
        print(f"   • {theme}: {description}")
    
    print("\n3. GROWTH TARGETS BY WEEK:")
    targets = sme_context.GROWTH_TARGETS
    for week, target in targets.items():
        print(f"   • {week.replace('_', ' ').title()}:")
        print(f"     - Followers: {target['followers']}")
        print(f"     - Engagements: {target['engagements']}")
        print(f"     - Demo Requests: {target['demo_requests']}")
        print(f"     - Business Inquiries: {target['business_inquiries']}")
        print(f"     - Focus: {target['focus']}")
    
    print("\n4. CONVERSION FUNNEL TRACKING:")
    funnel = sme_context.CONVERSION_FUNNEL
    for stage, description in funnel.items():
        print(f"   • {stage.title()}: {description}")
    
    print("\n5. KEY DIFFERENTIATORS TO HIGHLIGHT:")
    for differentiator in sme_context.DIFFERENTIATORS[:3]:
        print(f"   • {differentiator}")

def main():
    """Main demonstration function"""
    print("SME ANALYTICA ANALYTICS DASHBOARD")
    print("=" * 80)
    print("Comprehensive Analytics System for Social Media Growth Tracking")
    print("Building analytics for: 8 → 500+ followers in 4 weeks")
    print("=" * 80)
    
    try:
        # Initialize dashboard
        dashboard = AnalyticsDashboard()
        
        # Create sample data
        create_sample_data(dashboard)
        
        # Run demonstrations
        demonstrate_growth_tracking(dashboard)
        demonstrate_performance_analytics(dashboard)
        demonstrate_roi_measurement(dashboard)
        demonstrate_comprehensive_reporting(dashboard)
        demonstrate_sme_analytica_specific_features(dashboard)
        
        print("\n" + "="*80)
        print("ANALYTICS DASHBOARD DEMONSTRATION COMPLETE")
        print("="*80)
        print("\nKey Capabilities Demonstrated:")
        print("✅ Real-time follower growth tracking and projections")
        print("✅ Content performance analytics with viral scores")
        print("✅ ROI measurement from social media to business outcomes")
        print("✅ Growth trajectory modeling and forecasting")
        print("✅ Content optimization recommendations")
        print("✅ Weekly/monthly automated reporting")
        print("✅ SME Analytica specific metrics and targets")
        print("✅ Business conversion tracking and attribution")
        
        print(f"\nAnalytics Data Export Available:")
        print(f"📊 JSON format: dashboard.export_analytics_data('json')")
        print(f"📈 Comprehensive reports: dashboard.generate_comprehensive_report()")
        print(f"⏱️  Real-time dashboard: dashboard.get_real_time_dashboard()")
        
        # Save sample report
        print(f"\n💾 Saving sample comprehensive report...")
        report = dashboard.generate_comprehensive_report(weeks=4)
        report_path = "analytics_data/comprehensive_report.json"
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        print(f"   Report saved to: {os.path.abspath(report_path)}")
        
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()