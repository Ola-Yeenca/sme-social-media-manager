#!/usr/bin/env python3
"""
🤖 SME Analytica Autonomous Agent CLI
Comprehensive command-line interface for autonomous social media operations

Usage:
    python agent_cli.py start                    # Start autonomous agent
    python agent_cli.py stop                     # Stop autonomous agent
    python agent_cli.py status                   # Show real-time status
    python agent_cli.py dashboard                # Real-time dashboard
    python agent_cli.py trigger content          # Manual content creation
    python agent_cli.py trigger mentions         # Manual mention response
    python agent_cli.py trigger engagement       # Manual engagement
    python agent_cli.py config show              # Show configuration
    python agent_cli.py config edit              # Edit configuration
    python agent_cli.py health                   # Health check
    python agent_cli.py logs [tail]              # View logs
    python agent_cli.py analytics [period]       # Show analytics
"""

import asyncio
import argparse
import json
import os
import sys
import time
import signal
import subprocess
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import logging
import psutil
import threading
from pathlib import Path

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.ai_agent.intelligent_engagement_agent import create_intelligent_agent
from src.social_media_manager import SocialMediaManager
from src.content.collaborative_content_generator import CollaborativeContentGenerator, ContentCategory
from src.ai_providers import AIProviderManager
from src.notion.notion_manager import NotionManager
from config.settings import sme_context

class AgentCLI:
    """Comprehensive CLI interface for autonomous agent operations"""
    
    def __init__(self):
        self.logger = self.setup_logging()
        self.agent_pid_file = Path('logs/agent.pid')
        self.config_file = Path('config/agent_config.json')
        self.default_config = {
            "posting_schedule": {
                "enabled": True,
                "times": ["08:00", "13:00", "18:00", "21:00"],
                "timezone": "Europe/Madrid"
            },
            "engagement_limits": {
                "max_daily_posts": 12,
                "max_mention_responses": 25,
                "max_hourly_engagements": 8
            },
            "monitoring": {
                "mention_check_interval": 120,  # seconds
                "trend_analysis_interval": 900,  # 15 minutes
                "analytics_report_interval": 21600  # 6 hours
            },
            "ai_settings": {
                "viral_threshold": 7.5,
                "collaborative_content": True,
                "council_approval_required": True
            }
        }
        
    def setup_logging(self):
        """Setup logging for CLI"""
        os.makedirs('logs', exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/agent_cli.log'),
                logging.StreamHandler()
            ]
        )
        
        # Reduce noise from external libraries
        logging.getLogger('httpx').setLevel(logging.WARNING)
        logging.getLogger('tweepy').setLevel(logging.WARNING)
        
        return logging.getLogger(__name__)
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            else:
                self.save_config(self.default_config)
                return self.default_config
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return self.default_config
    
    def save_config(self, config: Dict[str, Any]):
        """Save configuration to file"""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            self.logger.info("Configuration saved successfully")
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
    
    def is_agent_running(self) -> bool:
        """Check if agent is currently running"""
        try:
            if not self.agent_pid_file.exists():
                return False
            
            with open(self.agent_pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            # Check if process exists
            return psutil.pid_exists(pid)
        except (ValueError, FileNotFoundError):
            return False
    
    def start_agent(self, background: bool = False):
        """Start the autonomous agent"""
        if self.is_agent_running():
            print("❌ Agent is already running")
            return False
        
        if background:
            # Start in background
            cmd = [sys.executable, "autonomous_agent.py"]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            with open(self.agent_pid_file, 'w') as f:
                f.write(str(process.pid))
            
            print(f"🚀 Agent started in background (PID: {process.pid})")
            return True
        else:
            # Start in foreground
            print("🤖 Starting autonomous agent in foreground...")
            try:
                from autonomous_agent import AutonomousSocialAgent
                agent = AutonomousSocialAgent()
                
                if asyncio.run(agent.initialize()):
                    asyncio.run(agent.start_autonomous_operation())
                else:
                    print("❌ Failed to initialize agent")
                    return False
                    
            except KeyboardInterrupt:
                print("\n🛑 Agent stopped by user")
                return True
            except Exception as e:
                print(f"❌ Error starting agent: {e}")
                return False
    
    def stop_agent(self):
        """Stop the autonomous agent"""
        if not self.is_agent_running():
            print("❌ Agent is not running")
            return False
        
        try:
            with open(self.agent_pid_file, 'r') as f:
                pid = int(f.read().strip())
            
            os.kill(pid, signal.SIGTERM)
            self.agent_pid_file.unlink(missing_ok=True)
            print(f"🛑 Agent stopped (PID: {pid})")
            return True
            
        except ProcessLookupError:
            print("❌ Agent process not found")
            self.agent_pid_file.unlink(missing_ok=True)
            return False
        except Exception as e:
            print(f"❌ Error stopping agent: {e}")
            return False
    
    async def get_agent_status(self) -> Dict[str, Any]:
        """Get comprehensive agent status"""
        status = {
            "is_running": self.is_agent_running(),
            "timestamp": datetime.now().isoformat(),
            "uptime": None,
            "system_health": {},
            "recent_activity": {},
            "configuration": self.load_config()
        }
        
        if status["is_running"]:
            try:
                # Check agent health via log analysis
                log_file = Path('logs/autonomous_agent.log')
                if log_file.exists():
                    with open(log_file, 'r') as f:
                        lines = f.readlines()
                        recent_lines = lines[-50:]  # Last 50 lines
                        
                        # Parse recent activity
                        recent_posts = [l for l in recent_lines if "Posted viral content" in l]
                        recent_mentions = [l for l in recent_lines if "Responded to mention" in l]
                        recent_errors = [l for l in recent_lines if "ERROR" in l]
                        
                        status["recent_activity"] = {
                            "posts_last_hour": len(recent_posts),
                            "mentions_last_hour": len(recent_mentions),
                            "errors_last_hour": len(recent_errors)
                        }
                
                # Check system health
                status["system_health"] = await self._check_system_health()
                
            except Exception as e:
                self.logger.error(f"Error getting status: {e}")
        
        return status
    
    async def _check_system_health(self) -> Dict[str, str]:
        """Check system health components"""
        health = {}
        
        try:
            # Check Twitter API
            from src.social.twitter_manager import TwitterManager
            credentials = {
                "api_key": os.getenv("TWITTER_API_KEY"),
                "api_secret": os.getenv("TWITTER_API_SECRET"),
                "access_token": os.getenv("TWITTER_ACCESS_TOKEN"),
                "access_token_secret": os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
                "bearer_token": os.getenv("TWITTER_BEARER_TOKEN")
            }
            
            if all(credentials.values()):
                twitter = TwitterManager(credentials)
                health["twitter"] = "✅ Connected"
            else:
                health["twitter"] = "❌ Missing credentials"
                
        except Exception as e:
            health["twitter"] = f"❌ Error: {e}"
        
        try:
            # Check Notion API
            from src.notion.notion_manager import NotionManager
            notion = NotionManager()
            health["notion"] = "✅ Connected"
        except Exception as e:
            health["notion"] = f"❌ Error: {e}"
        
        try:
            # Check AI providers
            ai_config = {
                "google_gemini_api_key": os.getenv("GOOGLE_GEMINI_API_KEY"),
                "openai_api_key": os.getenv("OPENAI_API_KEY"),
                "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY")
            }
            
            from src.ai_providers import AIProviderManager
            ai_provider = AIProviderManager(ai_config)
            
            available_providers = []
            for provider, status in ai_provider.providers.items():
                if hasattr(status, 'is_available') and status.is_available:
                    available_providers.append(provider)
            
            health["ai_providers"] = f"✅ {', '.join(available_providers)}" if available_providers else "❌ None available"
            
        except Exception as e:
            health["ai_providers"] = f"❌ Error: {e}"
        
        return health
    
    async def trigger_manual_action(self, action: str) -> Dict[str, Any]:
        """Trigger manual actions"""
        result = {"action": action, "success": False, "details": {}}
        
        try:
            if action == "content":
                # Manual content creation
                from src.content.collaborative_content_generator import CollaborativeContentGenerator
                from src.ai_providers import AIProviderManager
                from src.notion.notion_manager import NotionManager
                
                ai_config = {
                    "google_gemini_api_key": os.getenv("GOOGLE_GEMINI_API_KEY"),
                    "openai_api_key": os.getenv("OPENAI_API_KEY"),
                    "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY")
                }
                
                ai_provider = AIProviderManager(ai_config)
                notion_manager = NotionManager()
                content_gen = CollaborativeContentGenerator(ai_provider, notion_manager)
                
                # Generate viral content
                content = await content_gen.generate_collaborative_content(ContentCategory.VIRAL_HOOKS)
                
                result["details"] = {
                    "content_preview": content.content[:100] + "...",
                    "viral_score": content.final_score,
                    "category": content.category.value
                }
                result["success"] = True
                
            elif action == "mentions":
                # Manual mention response
                from src.ai_agent.intelligent_engagement_agent import create_intelligent_agent
                agent = await create_intelligent_agent()
                
                # Simulate mention response
                status = agent.get_agent_status()
                result["details"] = {"agent_status": status}
                result["success"] = True
                
            elif action == "engagement":
                # Manual engagement
                from src.engagement.engagement_automation import EngagementAutomation
                from src.social.twitter_manager import TwitterManager
                
                credentials = {
                    "api_key": os.getenv("TWITTER_API_KEY"),
                    "api_secret": os.getenv("TWITTER_API_SECRET"),
                    "access_token": os.getenv("TWITTER_ACCESS_TOKEN"),
                    "access_token_secret": os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
                    "bearer_token": os.getenv("TWITTER_BEARER_TOKEN")
                }
                
                if all(credentials.values()):
                    twitter = TwitterManager(credentials)
                    engagement = EngagementAutomation(twitter, None)
                    
                    # Run engagement automation
                    engagement_results = await engagement.run_engagement_automation()
                    result["details"] = engagement_results
                    result["success"] = True
                else:
                    result["error"] = "Missing Twitter credentials"
            
        except Exception as e:
            result["error"] = str(e)
            self.logger.error(f"Manual action error: {e}")
        
        return result
    
    def show_dashboard(self):
        """Show real-time dashboard"""
        try:
            import curses
            
            def dashboard_loop(stdscr):
                curses.curs_set(0)  # Hide cursor
                stdscr.nodelay(1)   # Non-blocking input
                
                while True:
                    stdscr.clear()
                    
                    # Header
                    stdscr.addstr(0, 0, "🤖 SME Analytica Agent Dashboard", curses.A_BOLD)
                    stdscr.addstr(1, 0, "=" * 50)
                    
                    # Status
                    running = self.is_agent_running()
                    status_text = "🟢 RUNNING" if running else "🔴 STOPPED"
                    stdscr.addstr(3, 0, f"Status: {status_text}")
                    
                    # System health
                    stdscr.addstr(5, 0, "System Health:", curses.A_BOLD)
                    
                    # Try to get health status
                    try:
                        import asyncio
                        health = asyncio.run(self._check_system_health())
                        
                        y = 6
                        for system, status in health.items():
                            color = curses.color_pair(1) if "✅" in status else curses.color_pair(2)
                            stdscr.addstr(y, 2, f"{system}: {status}")
                            y += 1
                    except:
                        stdscr.addstr(6, 2, "Health check unavailable")
                    
                    # Recent activity
                    stdscr.addstr(12, 0, "Recent Activity:", curses.A_BOLD)
                    log_file = Path('logs/autonomous_agent.log')
                    if log_file.exists():
                        try:
                            with open(log_file, 'r') as f:
                                lines = f.readlines()
                                recent = lines[-5:] if len(lines) >= 5 else lines
                                
                                y = 13
                                for line in recent[-5:]:
                                    clean_line = line.strip()[:60]
                                    if clean_line:
                                        stdscr.addstr(y, 2, clean_line)
                                        y += 1
                        except:
                            stdscr.addstr(13, 2, "Log read error")
                    
                    # Instructions
                    stdscr.addstr(20, 0, "Press 'q' to quit dashboard")
                    stdscr.addstr(21, 0, "Press 'r' to refresh")
                    
                    stdscr.refresh()
                    
                    # Handle input
                    key = stdscr.getch()
                    if key == ord('q'):
                        break
                    elif key == ord('r'):
                        continue
                    
                    time.sleep(2)  # Update every 2 seconds
            
            # Initialize colors
            curses.start_color()
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
            
            curses.wrapper(dashboard_loop)
            
        except ImportError:
            # Fallback if curses not available
            print("📊 SME Analytica Agent Dashboard")
            print("=" * 40)
            print(f"Status: {'🟢 RUNNING' if self.is_agent_running() else '🔴 STOPPED'}")
            
            # Simple status display
            asyncio.run(self.show_simple_status())
    
    async def show_simple_status(self):
        """Show simple status without curses"""
        status = await self.get_agent_status()
        
        print("\nSystem Health:")
        for system, health in status["system_health"].items():
            print(f"  {system}: {health}")
        
        if status["recent_activity"]:
            print("\nRecent Activity:")
            for activity, count in status["recent_activity"].items():
                print(f"  {activity}: {count}")
    
    def show_logs(self, tail: int = 50):
        """Show agent logs"""
        log_files = [
            'logs/autonomous_agent.log',
            'logs/agent_cli.log',
            'logs/sme_social_manager.log'
        ]
        
        for log_file in log_files:
            if Path(log_file).exists():
                print(f"\n📄 {log_file}:")
                print("-" * 50)
                try:
                    with open(log_file, 'r') as f:
                        lines = f.readlines()
                        for line in lines[-tail:]:
                            print(line.rstrip())
                except Exception as e:
                    print(f"Error reading log: {e}")
    
    def show_analytics(self, period: str = "today"):
        """Show analytics for specified period"""
        analytics_file = Path('logs/analytics.json')
        
        if not analytics_file.exists():
            print("❌ No analytics data found")
            return
        
        try:
            with open(analytics_file, 'r') as f:
                analytics = json.load(f)
            
            print("📊 SME Analytica Analytics")
            print("=" * 40)
            print(f"Period: {period}")
            print(f"Generated: {analytics.get('timestamp', 'Unknown')}")
            
            if 'daily_stats' in analytics:
                stats = analytics['daily_stats']
                print(f"\n📈 Performance:")
                print(f"  Posts Created: {stats.get('posts_created', 0)}")
                print(f"  Posts Published: {stats.get('posts_published', 0)}")
                print(f"  Mentions Responded: {stats.get('mentions_responded', 0)}")
                print(f"  Engagements Made: {stats.get('engagements_made', 0)}")
                print(f"  Grok Interactions: {stats.get('grok_interactions', 0)}")
            
            if 'growth_metrics' in analytics:
                metrics = analytics['growth_metrics']
                print(f"\n🎯 Growth Metrics:")
                print(f"  Estimated Reach: {metrics.get('estimated_reach', 0)}")
                print(f"  Engagement Rate: {metrics.get('engagement_rate', 0):.2f}%")
            
        except Exception as e:
            print(f"❌ Error reading analytics: {e}")
    
    def config_show(self):
        """Display current configuration"""
        config = self.load_config()
        
        print("⚙️  Current Configuration")
        print("=" * 30)
        print(json.dumps(config, indent=2))
    
    def config_edit(self):
        """Interactive configuration editor"""
        import tempfile
        import subprocess
        
        config = self.load_config()
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as tmp:
            json.dump(config, tmp, indent=2)
            tmp_path = tmp.name
        
        try:
            # Open in editor
            editor = os.environ.get('EDITOR', 'nano')
            subprocess.call([editor, tmp_path])
            
            # Read back edited config
            with open(tmp_path, 'r') as f:
                new_config = json.load(f)
            
            self.save_config(new_config)
            print("✅ Configuration updated successfully")
            
        except Exception as e:
            print(f"❌ Error editing config: {e}")
        finally:
            # Clean up temp file
            Path(tmp_path).unlink(missing_ok=True)
    
    def health_check(self) -> Dict[str, Any]:
        """Comprehensive health check"""
        health = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "unknown",
            "checks": {},
            "recommendations": []
        }
        
        try:
            # Check environment variables
            required_vars = [
                'TWITTER_API_KEY', 'TWITTER_API_SECRET',
                'TWITTER_ACCESS_TOKEN', 'TWITTER_ACCESS_TOKEN_SECRET',
                'NOTION_API_KEY', 'SOCIAL_MEDIA_DB_ID'
            ]
            
            missing_vars = [var for var in required_vars if not os.getenv(var)]
            health["checks"]["environment"] = "✅ OK" if not missing_vars else f"❌ Missing: {', '.join(missing_vars)}"
            
            if missing_vars:
                health["recommendations"].append(f"Set missing environment variables: {', '.join(missing_vars)}")
            
            # Check file permissions
            log_dir = Path('logs')
            if log_dir.exists() and os.access(log_dir, os.W_OK):
                health["checks"]["logs_directory"] = "✅ Writable"
            else:
                health["checks"]["logs_directory"] = "❌ Not writable"
                health["recommendations"].append("Ensure logs directory is writable")
            
            # Check Python packages
            required_packages = [
                'tweepy', 'notion_client', 'google-generativeai', 'openai', 'anthropic'
            ]
            
            missing_packages = []
            for package in required_packages:
                try:
                    __import__(package.replace('-', '_'))
                except ImportError:
                    missing_packages.append(package)
            
            health["checks"]["dependencies"] = "✅ All installed" if not missing_packages else f"❌ Missing: {', '.join(missing_packages)}"
            
            # Check database connectivity
            try:
                from src.notion.notion_manager import NotionManager
                notion = NotionManager()
                health["checks"]["notion_db"] = "✅ Connected"
            except Exception as e:
                health["checks"]["notion_db"] = f"❌ Error: {e}"
                health["recommendations"].append("Check Notion API configuration")
            
            # Overall status
            failed_checks = [v for v in health["checks"].values() if v.startswith("❌")]
            health["overall_status"] = "✅ Healthy" if not failed_checks else f"⚠️ Issues ({len(failed_checks)} failed checks)"
            
        except Exception as e:
            health["overall_status"] = f"❌ Critical error: {e}"
            health["recommendations"].append("Check system logs for details")
        
        return health

def main():
    """Main CLI entry point"""
    cli = AgentCLI()
    
    parser = argparse.ArgumentParser(
        description='SME Analytica Autonomous Agent CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python agent_cli.py start                    # Start agent in foreground
  python agent_cli.py start --background       # Start agent in background
  python agent_cli.py status                   # Check agent status
  python agent_cli.py dashboard                # Show real-time dashboard
  python agent_cli.py trigger content          # Create content manually
  python agent_cli.py trigger mentions         # Process mentions manually
  python agent_cli.py config show              # Show configuration
  python agent_cli.py logs --tail 100          # Show last 100 log lines
  python agent_cli.py analytics today          # Show today's analytics
  python agent_cli.py health                   # Run health check
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Start command
    start_parser = subparsers.add_parser('start', help='Start autonomous agent')
    start_parser.add_argument('--background', action='store_true', help='Run in background')
    
    # Stop command
    subparsers.add_parser('stop', help='Stop autonomous agent')
    
    # Status command
    subparsers.add_parser('status', help='Show agent status')
    
    # Dashboard command
    subparsers.add_parser('dashboard', help='Show real-time dashboard')
    
    # Trigger command
    trigger_parser = subparsers.add_parser('trigger', help='Trigger manual actions')
    trigger_parser.add_argument('action', choices=['content', 'mentions', 'engagement'], help='Action to trigger')
    
    # Config commands
    config_parser = subparsers.add_parser('config', help='Configuration management')
    config_subparsers = config_parser.add_subparsers(dest='config_action')
    config_subparsers.add_parser('show', help='Show current configuration')
    config_subparsers.add_parser('edit', help='Edit configuration interactively')
    
    # Logs command
    logs_parser = subparsers.add_parser('logs', help='View logs')
    logs_parser.add_argument('--tail', type=int, default=50, help='Number of lines to show')
    
    # Analytics command
    analytics_parser = subparsers.add_parser('analytics', help='Show analytics')
    analytics_parser.add_argument('period', nargs='?', default='today', help='Time period')
    
    # Health command
    subparsers.add_parser('health', help='Run health check')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'start':
            cli.start_agent(background=args.background)
            
        elif args.command == 'stop':
            cli.stop_agent()
            
        elif args.command == 'status':
            status = asyncio.run(cli.get_agent_status())
            
            print("🤖 SME Analytica Agent Status")
            print("=" * 40)
            print(f"Status: {'🟢 Running' if status['is_running'] else '🔴 Stopped'}")
            print(f"Timestamp: {status['timestamp']}")
            
            if status['system_health']:
                print("\nSystem Health:")
                for system, health in status['system_health'].items():
                    print(f"  {system}: {health}")
            
            if status['recent_activity']:
                print("\nRecent Activity:")
                for activity, count in status['recent_activity'].items():
                    print(f"  {activity}: {count}")
        
        elif args.command == 'dashboard':
            cli.show_dashboard()
            
        elif args.command == 'trigger':
            result = asyncio.run(cli.trigger_manual_action(args.action))
            
            print(f"🎯 Manual {args.action} triggered")
            print("=" * 30)
            print(f"Success: {result['success']}")
            
            if 'details' in result and result['details']:
                print("Details:")
                for key, value in result['details'].items():
                    print(f"  {key}: {value}")
            
            if 'error' in result:
                print(f"Error: {result['error']}")
        
        elif args.command == 'config':
            if args.config_action == 'show':
                cli.config_show()
            elif args.config_action == 'edit':
                cli.config_edit()
        
        elif args.command == 'logs':
            cli.show_logs(tail=args.tail)
            
        elif args.command == 'analytics':
            cli.show_analytics(period=args.period)
            
        elif args.command == 'health':
            health = cli.health_check()
            
            print("🏥 SME Analytica Health Check")
            print("=" * 35)
            print(f"Overall: {health['overall_status']}")
            print(f"Timestamp: {health['timestamp']}")
            
            if health['checks']:
                print("\nChecks:")
                for check, status in health['checks'].items():
                    print(f"  {check}: {status}")
            
            if health['recommendations']:
                print("\nRecommendations:")
                for rec in health['recommendations']:
                    print(f"  • {rec}")
    
    except KeyboardInterrupt:
        print("\n⏹️ Operation cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        cli.logger.error(f"CLI error: {e}")

if __name__ == "__main__":
    main()