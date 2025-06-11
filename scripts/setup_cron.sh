#!/bin/bash
"""
Cron job setup script for SME Analytica Social Media Manager
"""

# Daily automation - Run 3 times per day
# 8:00 AM - Generate and schedule content for the day
0 8 * * * cd /path/to/sme_social_manager && python scripts/run_social_manager.py daily >> logs/cron.log 2>&1

# 12:00 PM - Check for engagement opportunities and respond to mentions  
0 12 * * * cd /path/to/sme_social_manager && python scripts/run_social_manager.py engagement >> logs/cron.log 2>&1

# 6:00 PM - Final engagement check and post any remaining scheduled content
0 18 * * * cd /path/to/sme_social_manager && python scripts/run_social_manager.py engagement >> logs/cron.log 2>&1

# Hourly engagement checks during business hours (9 AM - 6 PM)
0 9-18 * * * cd /path/to/sme_social_manager && python scripts/run_social_manager.py engagement >> logs/cron.log 2>&1

# Weekly performance report (Sundays at 10 PM)
0 22 * * 0 cd /path/to/sme_social_manager && python scripts/run_social_manager.py report --days 7 >> logs/reports.log 2>&1

# Monthly comprehensive report (1st of month at 11 PM)
0 23 1 * * cd /path/to/sme_social_manager && python scripts/run_social_manager.py report --days 30 >> logs/reports.log 2>&1

# System health check (every 4 hours)
0 */4 * * * cd /path/to/sme_social_manager && python scripts/run_social_manager.py test >> logs/health.log 2>&1
