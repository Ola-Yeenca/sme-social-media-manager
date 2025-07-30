"""
Analytics Visualization Module
Creates charts, graphs, and visual representations of analytics data.
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import statistics

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalyticsVisualizer:
    """Create visual representations of analytics data"""
    
    def __init__(self):
        self.colors = {
            'primary': '#2E86AB',
            'secondary': '#A23B72', 
            'success': '#F18F01',
            'warning': '#C73E1D',
            'info': '#0B4F6C',
            'light': '#F8F9FA',
            'dark': '#212529'
        }
    
    def generate_ascii_chart(self, data: List[Tuple[str, float]], title: str, 
                           max_width: int = 50) -> str:
        """Generate ASCII bar chart"""
        if not data:
            return f"{title}\nNo data available"
        
        max_value = max(value for _, value in data)
        if max_value == 0:
            return f"{title}\nAll values are zero"
        
        chart_lines = [title, "=" * len(title)]
        
        for label, value in data:
            bar_length = int((value / max_value) * max_width)
            bar = "█" * bar_length
            chart_lines.append(f"{label:<15} |{bar:<{max_width}} {value:.1f}")
        
        return "\n".join(chart_lines)
    
    def generate_growth_trend_ascii(self, growth_data: List[Dict], days: int = 30) -> str:
        """Generate ASCII growth trend chart"""
        if not growth_data:
            return "Growth Trend\nNo data available"
        
        # Sort by timestamp
        sorted_data = sorted(growth_data, key=lambda x: x['timestamp'])
        
        # Get follower counts
        followers = [d['followers_count'] for d in sorted_data[-days:]]
        
        if len(followers) < 2:
            return "Growth Trend\nInsufficient data"
        
        # Create ASCII line chart
        min_val = min(followers)
        max_val = max(followers)
        range_val = max_val - min_val if max_val > min_val else 1
        
        chart_height = 10
        chart_width = min(50, len(followers))
        
        # Normalize values to chart height
        normalized = [int((f - min_val) / range_val * (chart_height - 1)) for f in followers[-chart_width:]]
        
        chart_lines = ["Follower Growth Trend", "=" * 21]
        
        # Build chart from top to bottom
        for row in range(chart_height - 1, -1, -1):
            line = ""
            for col, val in enumerate(normalized):
                if val == row:
                    line += "●"
                elif val > row:
                    line += "│"
                else:
                    line += " "
            chart_lines.append(f"{max_val - (row * range_val / (chart_height - 1)):>6.0f} │{line}")
        
        # Add bottom axis
        chart_lines.append(f"{'':>6} └{'─' * chart_width}")
        chart_lines.append(f"{'':>8}{len(followers)} days ago → now")
        
        return "\n".join(chart_lines)
    
    def create_performance_heatmap(self, theme_performance: List[Dict]) -> str:
        """Create ASCII heatmap of theme performance"""
        if not theme_performance:
            return "Theme Performance Heatmap\nNo data available"
        
        chart_lines = ["Content Theme Performance Heatmap", "=" * 33]
        
        max_engagement = max(theme['avg_engagement'] for theme in theme_performance)
        
        for theme in theme_performance:
            engagement = theme['avg_engagement']
            intensity = int((engagement / max_engagement) * 5) if max_engagement > 0 else 0
            
            # Create visual intensity indicator
            heatmap_chars = [' ', '░', '▒', '▓', '█', '██']
            heat_visual = heatmap_chars[min(intensity, len(heatmap_chars) - 1)]
            
            chart_lines.append(
                f"{theme['theme']:<20} {heat_visual:<4} {engagement:>6.2f}% "
                f"({theme['content_count']} posts)"
            )
        
        return "\n".join(chart_lines)
    
    def generate_roi_funnel_visual(self, conversion_data: Dict) -> str:
        """Generate ASCII conversion funnel visualization"""
        if not conversion_data:
            return "Conversion Funnel\nNo data available"
        
        # Define funnel stages in order
        funnel_stages = [
            ('social_impressions', 'Social Impressions'),
            ('website_visits', 'Website Visits'),
            ('demo_requests', 'Demo Requests'),
            ('business_inquiries', 'Business Inquiries'),
            ('customers_acquired', 'Customers')
        ]
        
        chart_lines = ["ROI Conversion Funnel", "=" * 19]
        
        max_width = 40
        max_value = conversion_data.get('social_impressions', 1)
        
        for stage_key, stage_name in funnel_stages:
            value = conversion_data.get(stage_key, 0)
            if max_value > 0:
                width = int((value / max_value) * max_width)
                funnel_bar = "█" * width
                percentage = (value / max_value) * 100 if max_value > 0 else 0
                
                chart_lines.append(
                    f"{stage_name:<20} │{funnel_bar:<{max_width}} {value:>6} ({percentage:>5.1f}%)"
                )
            else:
                chart_lines.append(f"{stage_name:<20} │{'':40} {value:>6}")
        
        return "\n".join(chart_lines)
    
    def create_target_progress_visual(self, progress_data: Dict) -> str:
        """Create visual representation of target progress"""
        if not progress_data or "error" in progress_data:
            return "Target Progress\nNo data available"
        
        chart_lines = [f"Week {progress_data.get('current_week', 0)} Target Progress", "=" * 25]
        
        target = progress_data.get('target_followers', 1)
        actual = progress_data.get('actual_followers', 0)
        progress_pct = (actual / target) * 100 if target > 0 else 0
        
        # Progress bar
        bar_width = 30
        filled_width = int((progress_pct / 100) * bar_width)
        empty_width = bar_width - filled_width
        
        progress_bar = "█" * filled_width + "░" * empty_width
        status_icon = "✅" if progress_pct >= 100 else "🎯" if progress_pct >= 80 else "⚠️"
        
        chart_lines.extend([
            f"Target Followers: {target}",
            f"Actual Followers: {actual}",
            f"Progress: [{progress_bar}] {progress_pct:.1f}% {status_icon}",
            f"",
            f"Focus Area: {progress_data.get('focus_area', 'N/A')}",
            f"Days Remaining: {progress_data.get('days_remaining_in_week', 0)}"
        ])
        
        return "\n".join(chart_lines)
    
    def generate_forecast_visual(self, forecast_data: Dict) -> str:
        """Generate visual representation of growth forecast"""
        if not forecast_data or "error" in forecast_data:
            return "Growth Forecast\nNo data available"
        
        chart_lines = ["Growth Forecast (Next 28 Days)", "=" * 29]
        
        current = forecast_data.get('current_followers', 0)
        forecasted = forecast_data.get('forecasted_followers', 0)
        growth_needed = forecasted - current
        daily_rate = forecast_data.get('daily_growth_rate', 0)
        confidence = forecast_data.get('confidence_score', 0)
        
        # Create visual forecast line
        chart_lines.extend([
            f"Current Followers:    {current:>6}",
            f"Forecasted Followers: {forecasted:>6}",
            f"Growth Needed:        {growth_needed:>6} (+{growth_needed/current*100:.1f}%)" if current > 0 else f"Growth Needed: {growth_needed}",
            "",
            f"Daily Growth Rate:    {daily_rate:>6.1f} followers/day",
            f"Weekly Growth Rate:   {daily_rate*7:>6.1f} followers/week",
            "",
            f"Forecast Confidence:  {confidence:>6.1f}%"
        ])
        
        # Confidence indicator
        conf_bar_width = 20
        conf_filled = int((confidence / 100) * conf_bar_width)
        conf_empty = conf_bar_width - conf_filled
        conf_bar = "█" * conf_filled + "░" * conf_empty
        
        conf_status = "🎯" if confidence >= 80 else "⚠️" if confidence >= 60 else "❌"
        chart_lines.append(f"Confidence Level:     [{conf_bar}] {conf_status}")
        
        return "\n".join(chart_lines)
    
    def create_comprehensive_dashboard(self, dashboard_data: Dict) -> str:
        """Create comprehensive ASCII dashboard"""
        dashboard_lines = [
            "SME ANALYTICA ANALYTICS DASHBOARD",
            "=" * 35,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Status: {dashboard_data.get('status', 'Unknown')}",
            ""
        ]
        
        # Current metrics section
        if "current_metrics" in dashboard_data:
            metrics = dashboard_data["current_metrics"]
            dashboard_lines.extend([
                "📊 CURRENT METRICS",
                "-" * 18,
                f"Followers:      {metrics.get('followers_count', 0):>8}",
                f"Following:      {metrics.get('following_count', 0):>8}",
                f"Tweets:         {metrics.get('tweet_count', 0):>8}",
                f"Engagement:     {metrics.get('engagement_rate', 0):>7.2f}%",
                f"Impressions:    {metrics.get('impressions', 0):>8,}",
                ""
            ])
        
        # Target progress
        if "target_progress" in dashboard_data:
            progress_visual = self.create_target_progress_visual(dashboard_data["target_progress"])
            dashboard_lines.extend([progress_visual, ""])
        
        # ROI summary
        if "roi_summary" in dashboard_data:
            roi = dashboard_data["roi_summary"]
            dashboard_lines.extend([
                "💰 ROI SUMMARY",
                "-" * 13,
                f"Revenue:        ${roi.get('total_revenue', 0):>8,.2f}",
                f"Customers:      {roi.get('total_customers', 0):>8}",
                f"Cost/Customer:  ${roi.get('cost_per_customer', 0):>8,.2f}",
                f"ROI:            {roi.get('roi_percentage', 0):>8.1f}%",
                ""
            ])
        
        # Top content
        if "recent_top_content" in dashboard_data:
            dashboard_lines.extend([
                "🔥 TOP PERFORMING CONTENT",
                "-" * 24
            ])
            
            for i, content in enumerate(dashboard_data["recent_top_content"][:3], 1):
                dashboard_lines.append(
                    f"{i}. {content.get('theme', 'Unknown')} - "
                    f"Viral Score: {content.get('viral_score', 0):.1f}"
                )
            dashboard_lines.append("")
        
        # Immediate actions
        if "immediate_actions" in dashboard_data:
            dashboard_lines.extend([
                "⚡ IMMEDIATE ACTIONS",
                "-" * 18
            ])
            
            for i, action in enumerate(dashboard_data["immediate_actions"], 1):
                dashboard_lines.append(f"{i}. {action}")
            dashboard_lines.append("")
        
        return "\n".join(dashboard_lines)
    
    def export_dashboard_html(self, dashboard_data: Dict, filepath: str = "analytics_dashboard.html") -> bool:
        """Export dashboard as HTML file"""
        try:
            html_content = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>SME Analytica Analytics Dashboard</title>
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
                    .dashboard {{ max-width: 1200px; margin: 0 auto; }}
                    .header {{ background: {self.colors['primary']}; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                    .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 20px; }}
                    .metric-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                    .metric-value {{ font-size: 2em; font-weight: bold; color: {self.colors['primary']}; }}
                    .metric-label {{ color: #666; margin-top: 5px; }}
                    .chart-container {{ background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                    .recommendations {{ background: white; padding: 20px; border-radius: 8px; }}
                    .recommendation {{ padding: 10px; margin: 5px 0; background: #f8f9fa; border-left: 4px solid {self.colors['primary']}; }}
                    pre {{ background: #f8f9fa; padding: 15px; border-radius: 4px; overflow-x: auto; }}
                </style>
            </head>
            <body>
                <div class="dashboard">
                    <div class="header">
                        <h1>SME Analytica Analytics Dashboard</h1>
                        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                        <p>Status: {dashboard_data.get('status', 'Active')}</p>
                    </div>
            """
            
            # Add metrics cards
            if "current_metrics" in dashboard_data:
                metrics = dashboard_data["current_metrics"]
                html_content += """
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <div class="metric-value">{}</div>
                            <div class="metric-label">Followers</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">{:.2f}%</div>
                            <div class="metric-label">Engagement Rate</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">{:,}</div>
                            <div class="metric-label">Impressions</div>
                        </div>
                    </div>
                """.format(
                    metrics.get('followers_count', 0),
                    metrics.get('engagement_rate', 0),
                    metrics.get('impressions', 0)
                )
            
            # Add dashboard visualization
            dashboard_ascii = self.create_comprehensive_dashboard(dashboard_data)
            html_content += f"""
                <div class="chart-container">
                    <h2>Dashboard Overview</h2>
                    <pre>{dashboard_ascii}</pre>
                </div>
            """
            
            # Add recommendations
            if "immediate_actions" in dashboard_data:
                html_content += """
                    <div class="recommendations">
                        <h2>Immediate Actions</h2>
                """
                for action in dashboard_data["immediate_actions"]:
                    html_content += f'<div class="recommendation">{action}</div>'
                html_content += "</div>"
            
            html_content += """
                </div>
                <script>
                    // Auto-refresh every 5 minutes
                    setTimeout(() => location.reload(), 300000);
                </script>
            </body>
            </html>
            """
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            return True
            
        except Exception as e:
            logger.error(f"Error exporting HTML dashboard: {e}")
            return False
    
    def create_weekly_report_visual(self, weekly_report: Dict) -> str:
        """Create visual weekly report"""
        report_lines = [
            "SME ANALYTICA WEEKLY REPORT",
            "=" * 27,
            f"Week: {weekly_report.get('week_start', '')} to {weekly_report.get('week_end', '')}",
            ""
        ]
        
        # Key metrics
        report_lines.extend([
            "📈 WEEKLY PERFORMANCE",
            "-" * 20,
            f"Follower Growth:      {weekly_report.get('follower_growth', 0):>6}",
            f"Total Engagement:     {weekly_report.get('engagement_total', 0):>6}",
            f"Demo Requests:        {weekly_report.get('conversion_metrics', {}).get('demo_requests', 0):>6}",
            f"Business Inquiries:   {weekly_report.get('conversion_metrics', {}).get('business_inquiries', 0):>6}",
            f"Revenue Generated:    ${weekly_report.get('conversion_metrics', {}).get('revenue_generated', 0):>6,.2f}",
            ""
        ])
        
        # Top content
        top_content = weekly_report.get('top_performing_content', [])
        if top_content:
            report_lines.extend([
                "🏆 TOP PERFORMING CONTENT",
                "-" * 24
            ])
            
            for i, content in enumerate(top_content[:5], 1):
                report_lines.append(
                    f"{i}. {content.get('theme', 'Unknown')} - "
                    f"Viral Score: {content.get('viral_score', 0):.1f} - "
                    f"Engagement: {content.get('engagement_rate', 0):.2f}%"
                )
            report_lines.append("")
        
        # Recommendations
        recommendations = weekly_report.get('recommendations', [])
        if recommendations:
            report_lines.extend([
                "💡 STRATEGIC RECOMMENDATIONS",
                "-" * 27
            ])
            
            for i, rec in enumerate(recommendations[:8], 1):
                report_lines.append(f"{i}. {rec}")
            report_lines.append("")
        
        # Growth forecast
        forecast = weekly_report.get('growth_forecast', {})
        if forecast and "error" not in forecast:
            forecast_visual = self.generate_forecast_visual(forecast)
            report_lines.extend([forecast_visual, ""])
        
        return "\n".join(report_lines)

# Demo function
def demo_visualization():
    """Demonstrate visualization capabilities"""
    print("SME Analytica Analytics Visualization Demo")
    print("=" * 45)
    
    visualizer = AnalyticsVisualizer()
    
    # Sample data
    theme_data = [
        {"theme": "case_wednesday", "avg_engagement": 8.5, "content_count": 12},
        {"theme": "tech_thursday", "avg_engagement": 7.2, "content_count": 10},
        {"theme": "data_monday", "avg_engagement": 6.8, "content_count": 15},
        {"theme": "fact_friday", "avg_engagement": 5.5, "content_count": 8},
        {"theme": "talk_tuesday", "avg_engagement": 4.2, "content_count": 9}
    ]
    
    progress_data = {
        "current_week": 2,
        "target_followers": 150,
        "actual_followers": 120,
        "follower_progress": 80.0,
        "focus_area": "Influencer outreach and relationship building",
        "days_remaining_in_week": 3,
        "on_track": True
    }
    
    forecast_data = {
        "current_followers": 120,
        "forecasted_followers": 450,
        "growth_needed": 330,
        "daily_growth_rate": 11.8,
        "weekly_growth_rate": 82.6,
        "confidence_score": 85.5
    }
    
    dashboard_data = {
        "status": "active",
        "current_metrics": {
            "followers_count": 120,
            "following_count": 25,
            "tweet_count": 45,
            "engagement_rate": 6.8,
            "impressions": 3500
        },
        "target_progress": progress_data,
        "roi_summary": {
            "total_revenue": 7500.0,
            "total_customers": 3,
            "cost_per_customer": 250.0,
            "roi_percentage": 125.5
        },
        "immediate_actions": [
            "Focus more on 'case_wednesday' content - it has 8.50% average engagement rate",
            "Post more content at 14:00 for optimal engagement (7.25% avg engagement)",
            "Use high-performing hashtags: #SMEAnalytica, #DataInsights, #RestaurantTech"
        ]
    }
    
    # Demonstrate visualizations
    print("\n1. Theme Performance Heatmap:")
    print(visualizer.create_performance_heatmap(theme_data))
    
    print("\n2. Target Progress Visual:")
    print(visualizer.create_target_progress_visual(progress_data))
    
    print("\n3. Growth Forecast:")
    print(visualizer.generate_forecast_visual(forecast_data))
    
    print("\n4. Comprehensive Dashboard:")
    print(visualizer.create_comprehensive_dashboard(dashboard_data))
    
    # Export HTML
    if visualizer.export_dashboard_html(dashboard_data, "demo_dashboard.html"):
        print("\n5. HTML Dashboard exported to: demo_dashboard.html")
    
    print("\nVisualization Demo Complete!")

if __name__ == "__main__":
    demo_visualization()