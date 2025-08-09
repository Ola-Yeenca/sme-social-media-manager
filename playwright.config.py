#!/usr/bin/env python3
"""
Playwright Configuration for SME Social Media Bot E2E Testing
Configures browser settings, timeouts, and test environment
"""

from playwright.sync_api import Playwright
import os


class PlaywrightConfig:
    """Configuration settings for Playwright tests"""
    
    # Browser settings
    BROWSER_TYPE = 'chromium'  # chromium, firefox, or webkit
    HEADLESS = True           # Set to False for debugging
    SLOW_MO = 0               # Slow down operations by N milliseconds (for debugging)
    
    # Viewport settings  
    VIEWPORT_WIDTH = 1280
    VIEWPORT_HEIGHT = 720
    
    # Timeout settings (in milliseconds)
    DEFAULT_TIMEOUT = 30000      # 30 seconds
    NAVIGATION_TIMEOUT = 60000   # 60 seconds for navigation
    TEST_TIMEOUT = 120000        # 2 minutes per test
    
    # Screenshot settings
    SCREENSHOT_MODE = 'only-on-failure'  # 'off', 'on', 'only-on-failure'
    SCREENSHOT_PATH = './test-results/screenshots'
    
    # Video recording
    VIDEO_MODE = 'retain-on-failure'  # 'off', 'on', 'retain-on-failure'
    VIDEO_PATH = './test-results/videos'
    
    # Trace settings (for debugging)
    TRACE_MODE = 'retain-on-failure'  # 'off', 'on', 'retain-on-failure'
    TRACE_PATH = './test-results/traces'
    
    # Base URLs for testing
    BASE_URLS = {
        'github': 'https://github.com',
        'twitter': 'https://twitter.com',
        'localhost': 'http://localhost:3000'
    }
    
    # Test data
    TEST_DATA = {
        'github_repo': 'sme_social_manager',
        'github_user': 'test_user',
        'test_tweet_content': 'Test tweet from SME Social Media Bot automation 🤖 #Testing #AI #Business',
        'expected_hashtags': ['#Testing', '#AI', '#Business']
    }
    
    @classmethod
    def get_browser_options(cls):
        """Get browser launch options"""
        return {
            'headless': cls.HEADLESS,
            'slow_mo': cls.SLOW_MO,
            'args': [
                '--disable-dev-shm-usage',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding'
            ] if os.getenv('CI') else []
        }
    
    @classmethod 
    def get_context_options(cls):
        """Get browser context options"""
        return {
            'viewport': {
                'width': cls.VIEWPORT_WIDTH,
                'height': cls.VIEWPORT_HEIGHT
            },
            'record_video_dir': cls.VIDEO_PATH if cls.VIDEO_MODE != 'off' else None,
            'record_video_size': {'width': 1280, 'height': 720}
        }
    
    @classmethod
    def get_page_options(cls):
        """Get page options"""
        return {
            'default_timeout': cls.DEFAULT_TIMEOUT,
            'navigation_timeout': cls.NAVIGATION_TIMEOUT
        }
    
    @classmethod
    def setup_directories(cls):
        """Create necessary directories for test artifacts"""
        directories = [
            cls.SCREENSHOT_PATH,
            cls.VIDEO_PATH, 
            cls.TRACE_PATH,
            './test-results/reports'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    @classmethod
    def get_github_token(cls):
        """Get GitHub token for API testing"""
        return os.getenv('GITHUB_TOKEN', 'ghp_test_token_for_testing')
    
    @classmethod
    def should_run_live_tests(cls):
        """Check if live API tests should run"""
        # Only run live tests if explicitly enabled
        return os.getenv('RUN_LIVE_TESTS', 'false').lower() == 'true'
    
    @classmethod
    def get_mock_api_responses(cls):
        """Get mock API responses for testing"""
        return {
            'twitter_post_success': {
                'data': {
                    'id': '1234567890',
                    'text': cls.TEST_DATA['test_tweet_content'],
                    'created_at': '2024-01-15T12:00:00.000Z',
                    'public_metrics': {
                        'like_count': 0,
                        'retweet_count': 0,
                        'reply_count': 0,
                        'impression_count': 100
                    }
                }
            },
            'github_workflow_success': {
                'id': 123456,
                'status': 'completed',
                'conclusion': 'success',
                'created_at': '2024-01-15T12:00:00Z',
                'updated_at': '2024-01-15T12:05:00Z'
            },
            'viral_prediction': {
                'total_score': 85.5,
                'content_score': 80.0,
                'timing_score': 90.0,
                'hashtag_score': 85.0,
                'engagement_score': 88.0,
                'trend_score': 75.0,
                'predicted_engagement': {
                    'likes': 25,
                    'retweets': 8,
                    'replies': 3,
                    'impressions': 500
                },
                'confidence': 87.5,
                'recommendations': [
                    'Add more emotional triggers',
                    'Include a call-to-action',
                    'Post during peak hours'
                ]
            }
        }


# Test environment setup
def setup_test_environment():
    """Setup test environment and dependencies"""
    PlaywrightConfig.setup_directories()
    
    # Set environment variables for testing
    test_env = {
        'NODE_ENV': 'test',
        'TWITTER_API_KEY': 'test_twitter_key',
        'TWITTER_API_SECRET': 'test_twitter_secret',
        'TWITTER_ACCESS_TOKEN': 'test_access_token',
        'TWITTER_ACCESS_TOKEN_SECRET': 'test_access_secret',
        'TWITTER_BEARER_TOKEN': 'test_bearer_token',
        'OPENAI_API_KEY': 'test_openai_key',
        'GITHUB_TOKEN': PlaywrightConfig.get_github_token()
    }
    
    for key, value in test_env.items():
        if key not in os.environ:
            os.environ[key] = value
    
    print("✅ Test environment configured")


def cleanup_test_environment():
    """Clean up test environment"""
    # Clean up test artifacts older than 7 days
    import shutil
    import time
    from pathlib import Path
    
    cutoff_time = time.time() - (7 * 24 * 60 * 60)  # 7 days ago
    
    for directory in ['./test-results/screenshots', './test-results/videos', './test-results/traces']:
        if os.path.exists(directory):
            for file_path in Path(directory).rglob('*'):
                if file_path.is_file() and file_path.stat().st_mtime < cutoff_time:
                    try:
                        file_path.unlink()
                    except OSError:
                        pass  # Ignore errors when cleaning up
    
    print("✅ Test environment cleaned up")


# Pytest configuration (if using pytest-playwright)
def pytest_configure():
    """Configure pytest for Playwright tests"""
    setup_test_environment()


def pytest_unconfigure():
    """Cleanup after pytest run"""
    cleanup_test_environment()


if __name__ == '__main__':
    print("🔧 Playwright Configuration for SME Social Media Bot")
    print(f"Browser: {PlaywrightConfig.BROWSER_TYPE}")
    print(f"Headless: {PlaywrightConfig.HEADLESS}")
    print(f"Default timeout: {PlaywrightConfig.DEFAULT_TIMEOUT}ms")
    print(f"Viewport: {PlaywrightConfig.VIEWPORT_WIDTH}x{PlaywrightConfig.VIEWPORT_HEIGHT}")
    
    setup_test_environment()
    print("\n✅ Configuration complete!")