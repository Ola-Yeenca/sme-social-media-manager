# 🤖 SME Analytica Autonomous Agent CLI

A comprehensive command-line interface for managing and monitoring the SME Analytica autonomous social media agent.

## 🚀 Quick Start

### Setup
```bash
# Make setup script executable and run it
chmod +x setup_cli.py
python setup_cli.py
```

### Basic Usage
```bash
# Check agent status
python agent_cli.py status

# Start the autonomous agent
python agent_cli.py start

# Start in background
python agent_cli.py start --background

# Stop the agent
python agent_cli.py stop

# Real-time dashboard
python agent_cli.py dashboard
```

## 📋 Available Commands

### Core Operations
| Command | Description |
|---------|-------------|
| `start [--background]` | Start autonomous agent (foreground or background) |
| `stop` | Stop running agent gracefully |
| `status` | Show current agent status and health |
| `dashboard` | Real-time monitoring dashboard |

### Manual Triggers
| Command | Description |
|---------|-------------|
| `trigger content` | Manually create viral content |
| `trigger mentions` | Process pending mentions manually |
| `trigger engagement` | Run engagement automation |

### Configuration
| Command | Description |
|---------|-------------|
| `config show` | Display current configuration |
| `config edit` | Edit configuration interactively |

### Monitoring & Analytics
| Command | Description |
|---------|-------------|
| `logs [--tail N]` | View agent logs (default: 50 lines) |
| `analytics [period]` | Show analytics (today, week, month) |
| `health` | Comprehensive system health check |

## 🎯 Detailed Usage Examples

### Starting the Agent
```bash
# Start in foreground (interactive)
python agent_cli.py start

# Start in background as daemon
python agent_cli.py start --background

# Check if running
python agent_cli.py status
```

### Real-time Monitoring
```bash
# Interactive dashboard with live updates
python agent_cli.py dashboard

# Simple status check
python agent_cli.py status

# Health check with recommendations
python agent_cli.py health
```

### Manual Content Creation
```bash
# Create viral content on-demand
python agent_cli.py trigger content

# Process all pending mentions
python agent_cli.py trigger mentions

# Run strategic engagement
python agent_cli.py trigger engagement
```

### Configuration Management
```bash
# View current settings
python agent_cli.py config show

# Edit configuration (opens default editor)
python agent_cli.py config edit
```

### Log Analysis
```bash
# View last 100 log entries
python agent_cli.py logs --tail 100

# View all logs
python agent_cli.py logs

# Monitor logs in real-time
python agent_cli.py logs --tail 0 | tail -f logs/autonomous_agent.log
```

## 📊 Dashboard Features

The real-time dashboard provides:
- **Live Status**: Agent running/stopped state
- **System Health**: API connections and service status
- **Recent Activity**: Last 5 log entries
- **Performance Metrics**: Posts, mentions, engagements
- **Interactive Controls**: Refresh and quit options

## ⚙️ Configuration Options

### Key Settings
```json
{
  "posting_schedule": {
    "enabled": true,
    "times": ["08:00", "13:00", "18:00", "21:00"],
    "timezone": "Europe/Madrid"
  },
  "engagement_limits": {
    "max_daily_posts": 12,
    "max_mention_responses": 25,
    "max_hourly_engagements": 8
  },
  "monitoring": {
    "mention_check_interval": 120,
    "trend_analysis_interval": 900,
    "analytics_report_interval": 21600
  }
}
```

### Environment Variables Required
```bash
# Twitter API
TWITTER_API_KEY=your_key
TWITTER_API_SECRET=your_secret
TWITTER_ACCESS_TOKEN=your_token
TWITTER_ACCESS_TOKEN_SECRET=your_secret
TWITTER_BEARER_TOKEN=your_bearer

# Notion API
NOTION_API_KEY=your_key
SOCIAL_MEDIA_DB_ID=your_db_id

# AI Providers (at least one required)
GOOGLE_GEMINI_API_KEY=your_key
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key
```

## 🔧 Health Check

The health check validates:
- ✅ Environment variables
- ✅ API connectivity (Twitter, Notion)
- ✅ AI provider availability
- ✅ File permissions
- ✅ Dependencies
- ✅ Database connectivity

## 📈 Analytics Reports

Analytics include:
- **Daily Performance**: Posts, mentions, engagements
- **Growth Metrics**: Estimated reach, engagement rate
- **AI Performance**: Viral content scores, response quality
- **System Health**: Error rates, uptime

## 🚨 Troubleshooting

### Common Issues

**Agent won't start:**
```bash
# Check health
python agent_cli.py health

# Verify environment
python agent_cli.py config show

# Check logs
python agent_cli.py logs --tail 100
```

**API connection issues:**
```bash
# Test individual connections
python agent_cli.py health

# Check environment variables
env | grep -E "(TWITTER|NOTION|API)"
```

**Performance issues:**
```bash
# Monitor resource usage
python agent_cli.py dashboard

# Check recent activity
python agent_cli.py logs --tail 50
```

### Log Locations
- `logs/autonomous_agent.log` - Main agent logs
- `logs/agent_cli.log` - CLI operation logs
- `logs/sme_social_manager.log` - System-wide logs
- `logs/analytics.json` - Analytics data
- `logs/final_state.json` - Shutdown state

## 🔄 Integration with Existing System

The CLI integrates seamlessly with:
- **main.py** - Existing automation modes
- **autonomous_agent.py** - 24/7 agent
- **src/** - All existing modules
- **config/** - Shared configuration
- **logs/** - Unified logging

## 📋 Quick Reference Card

```bash
# Daily Operations
python agent_cli.py start --background  # Start daemon
python agent_cli.py status              # Check status
python agent_cli.py dashboard           # Monitor live
python agent_cli.py stop                # Stop gracefully

# Content Management
python agent_cli.py trigger content     # Create content
python agent_cli.py trigger mentions    # Process mentions
python agent_cli.py trigger engagement  # Run engagement

# Monitoring
python agent_cli.py logs --tail 50      # View logs
python agent_cli.py analytics today     # Today's stats
python agent_cli.py health              # System check
```

## 🎨 Advanced Features

### Background Service
```bash
# Create systemd service (Linux)
sudo cp agent.service /etc/systemd/system/
sudo systemctl enable agent
sudo systemctl start agent

# Check service status
sudo systemctl status agent
```

### Cron Integration
```bash
# Add to crontab for scheduled restarts
@reboot /usr/bin/python3 /path/to/agent_cli.py start --background
0 6 * * * /usr/bin/python3 /path/to/agent_cli.py health
```

## 🤝 Support

For issues or questions:
1. Run health check: `python agent_cli.py health`
2. Check logs: `python agent_cli.py logs`
3. Verify configuration: `python agent_cli.py config show`
4. Test manual triggers: `python agent_cli.py trigger content`