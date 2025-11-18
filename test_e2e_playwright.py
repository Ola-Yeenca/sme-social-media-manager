#!/usr/bin/env python3
"""
End-to-end tests for SME Social Media Bot using Playwright
Tests complete workflows and GitHub Actions integration
"""

import unittest
import subprocess
import json
import os
import sys
from pathlib import Path
from unittest.mock import patch, Mock, MagicMock

# Mock external libraries
sys.modules['tweepy'] = MagicMock()
sys.modules['openai'] = MagicMock()
sys.modules['groq'] = MagicMock()
sys.modules['anthropic'] = MagicMock()


class TestCompleteWorkflow(unittest.TestCase):
    """Test complete bot workflow end-to-end"""

    def setUp(self):
        """Set up test environment"""
        self.project_root = Path(__file__).parent

    def test_bot_import_successful(self):
        """Test that bot can be imported without errors"""
        try:
            from bot import SMESocialBot
            self.assertTrue(True, "Bot imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import bot: {e}")

    def test_config_import_successful(self):
        """Test that config can be imported"""
        try:
            from config import Config
            self.assertTrue(True, "Config imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import config: {e}")

    def test_viral_predictor_import_successful(self):
        """Test that viral predictor can be imported"""
        try:
            from viral_predictor import ViralTweetPredictor
            self.assertTrue(True, "Viral predictor imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import viral predictor: {e}")

    @patch.dict(os.environ, {
        'TWITTER_API_KEY': 'test-key',
        'TWITTER_API_SECRET': 'test-secret',
        'TWITTER_ACCESS_TOKEN': 'test-token',
        'TWITTER_ACCESS_TOKEN_SECRET': 'test-token-secret',
        'TWITTER_BEARER_TOKEN': 'test-bearer',
        'OPENAI_API_KEY': 'test-openai-key'
    })
    def test_bot_initialization_workflow(self):
        """Test complete bot initialization workflow"""
        from bot import SMESocialBot

        bot = SMESocialBot(test_mode=True)

        # Verify all components initialized
        self.assertIsNotNone(bot.config)
        self.assertIsNotNone(bot.viral_predictor)
        self.assertIsNotNone(bot.session_stats)
        self.assertEqual(bot.session_stats['posts_created'], 0)

    @patch.dict(os.environ, {
        'TWITTER_API_KEY': 'test-key',
        'TWITTER_API_SECRET': 'test-secret',
        'TWITTER_ACCESS_TOKEN': 'test-token',
        'TWITTER_ACCESS_TOKEN_SECRET': 'test-token-secret',
        'TWITTER_BEARER_TOKEN': 'test-bearer',
        'OPENAI_API_KEY': 'test-openai-key'
    })
    def test_content_generation_to_posting_workflow(self):
        """Test complete workflow from content generation to posting"""
        from bot import SMESocialBot

        bot = SMESocialBot(test_mode=True)
        bot.rate_limited = True  # Use simulation mode

        # Generate content
        with patch('bot.openai.chat.completions.create') as mock_openai:
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "AI analytics boost restaurant revenue by 47%! #AI #Business"
            mock_openai.return_value = mock_response

            content = bot.generate_content()
            self.assertIsInstance(content, str)

            # Post content
            result = bot.post_content(content)
            self.assertTrue(result)
            self.assertEqual(bot.session_stats['posts_created'], 1)
            self.assertEqual(bot.session_stats['viral_predictions'], 1)

    @patch.dict(os.environ, {
        'TWITTER_API_KEY': 'test-key',
        'TWITTER_API_SECRET': 'test-secret',
        'TWITTER_ACCESS_TOKEN': 'test-token',
        'TWITTER_ACCESS_TOKEN_SECRET': 'test-token-secret',
        'TWITTER_BEARER_TOKEN': 'test-bearer',
        'OPENAI_API_KEY': 'test-openai-key'
    })
    def test_engagement_workflow(self):
        """Test complete engagement workflow (mentions -> engage)"""
        from bot import SMESocialBot

        bot = SMESocialBot(test_mode=True)
        bot.rate_limited = True

        # Check mentions
        mentions = bot.check_mentions(days_back=1)
        self.assertIsInstance(mentions, list)
        self.assertGreater(len(mentions), 0)

        # Engage with mentions
        engagements = bot.engage_with_mentions(mentions)
        self.assertGreater(engagements, 0)
        self.assertGreater(bot.session_stats['engagements_made'], 0)

    @patch.dict(os.environ, {
        'TWITTER_API_KEY': 'test-key',
        'TWITTER_API_SECRET': 'test-secret',
        'TWITTER_ACCESS_TOKEN': 'test-token',
        'TWITTER_ACCESS_TOKEN_SECRET': 'test-token-secret',
        'TWITTER_BEARER_TOKEN': 'test-bearer',
        'OPENAI_API_KEY': 'test-openai-key',
        'LINKEDIN_ACCESS_TOKEN': 'test-linkedin-token'
    })
    def test_multi_platform_workflow(self):
        """Test complete multi-platform posting workflow"""
        from bot import SMESocialBot

        with patch('bot.LinkedInManager'):
            bot = SMESocialBot(test_mode=False, multi_platform=True)
            bot.rate_limited = True

            # Generate and post to multiple platforms
            with patch('bot.openai.chat.completions.create') as mock_openai:
                mock_response = Mock()
                mock_response.choices = [Mock()]
                mock_response.choices[0].message.content = "Test multi-platform content"
                mock_openai.return_value = mock_response

                content = bot.generate_content()

                # Mock LinkedIn posting
                if bot.linkedin:
                    bot.linkedin.post_to_linkedin = Mock(return_value=(True, {'id': 'test-123'}))

                result = bot.post_multi_platform(content)
                self.assertTrue(result)


class TestViralPredictionWorkflow(unittest.TestCase):
    """Test viral prediction integrated workflow"""

    @patch.dict(os.environ, {
        'TWITTER_API_KEY': 'test-key',
        'TWITTER_API_SECRET': 'test-secret',
        'TWITTER_ACCESS_TOKEN': 'test-token',
        'TWITTER_ACCESS_TOKEN_SECRET': 'test-token-secret',
        'TWITTER_BEARER_TOKEN': 'test-bearer',
        'OPENAI_API_KEY': 'test-openai-key'
    })
    def test_viral_prediction_during_posting(self):
        """Test that viral prediction is integrated into posting"""
        from bot import SMESocialBot

        bot = SMESocialBot(test_mode=True)
        bot.rate_limited = True

        content = "Simple test tweet"
        initial_predictions = bot.session_stats['viral_predictions']

        bot.post_content(content)

        # Should have made a viral prediction
        self.assertEqual(bot.session_stats['viral_predictions'], initial_predictions + 1)

    @patch.dict(os.environ, {
        'TWITTER_API_KEY': 'test-key',
        'TWITTER_API_SECRET': 'test-secret',
        'TWITTER_ACCESS_TOKEN': 'test-token',
        'TWITTER_ACCESS_TOKEN_SECRET': 'test-token-secret',
        'TWITTER_BEARER_TOKEN': 'test-bearer',
        'OPENAI_API_KEY': 'test-openai-key'
    })
    def test_viral_optimization_workflow(self):
        """Test that low-scoring content gets optimized"""
        from bot import SMESocialBot
        from viral_predictor import ViralTweetPredictor

        predictor = ViralTweetPredictor()

        # Low-quality tweet
        low_quality = "update"
        score_before = predictor.predict_viral_potential(low_quality)

        # Optimize it
        optimized, score_after = predictor.optimize_tweet(low_quality)

        # Should be improved
        self.assertNotEqual(low_quality, optimized)
        self.assertIn('#', optimized)  # Should add hashtags

    @patch.dict(os.environ, {
        'TWITTER_API_KEY': 'test-key',
        'TWITTER_API_SECRET': 'test-secret',
        'TWITTER_ACCESS_TOKEN': 'test-token',
        'TWITTER_ACCESS_TOKEN_SECRET': 'test-token-secret',
        'TWITTER_BEARER_TOKEN': 'test-bearer',
        'OPENAI_API_KEY': 'test-openai-key'
    })
    def test_viral_variations_generation_workflow(self):
        """Test complete viral variations workflow"""
        from bot import SMESocialBot

        bot = SMESocialBot(test_mode=True)

        base_idea = "Restaurant analytics increase revenue"
        variations = bot.generate_viral_content(base_idea)

        # Should generate 3 variations
        self.assertEqual(len(variations), 3)

        # All should have decent scores
        for tweet, score in variations:
            self.assertIsInstance(tweet, str)
            self.assertLessEqual(len(tweet), 280)
            self.assertGreater(score.total_score, 0)

        # Should be sorted by score
        scores = [score.total_score for _, score in variations]
        self.assertEqual(scores, sorted(scores, reverse=True))


class TestGitHubActionsWorkflow(unittest.TestCase):
    """Test GitHub Actions workflow validation"""

    def setUp(self):
        """Set up test environment"""
        self.project_root = Path(__file__).parent
        self.workflow_file = self.project_root / '.github' / 'workflows' / 'sme-social-bot.yml'

    def test_workflow_file_exists(self):
        """Test that the GitHub Actions workflow file exists"""
        self.assertTrue(self.workflow_file.exists(),
                       f"Workflow file should exist at {self.workflow_file}")

    def test_workflow_has_required_jobs(self):
        """Test that workflow has all required jobs"""
        if not self.workflow_file.exists():
            self.skipTest("Workflow file not found")

        with open(self.workflow_file, 'r') as f:
            content = f.read()

        # Check for essential workflow components
        self.assertIn('name:', content)
        self.assertIn('on:', content)
        self.assertIn('schedule:', content)
        self.assertIn('jobs:', content)

    def test_workflow_has_schedules(self):
        """Test that workflow has scheduled runs"""
        if not self.workflow_file.exists():
            self.skipTest("Workflow file not found")

        with open(self.workflow_file, 'r') as f:
            content = f.read()

        # Should have cron schedules
        self.assertIn('cron:', content)

    def test_workflow_has_manual_trigger(self):
        """Test that workflow can be triggered manually"""
        if not self.workflow_file.exists():
            self.skipTest("Workflow file not found")

        with open(self.workflow_file, 'r') as f:
            content = f.read()

        # Should have workflow_dispatch for manual triggers
        self.assertIn('workflow_dispatch:', content)

    def test_required_dependencies_installable(self):
        """Test that required dependencies are specified"""
        requirements_file = self.project_root / 'requirements.txt'

        self.assertTrue(requirements_file.exists(),
                       "requirements.txt should exist")

        with open(requirements_file, 'r') as f:
            requirements = f.read()

        # Check for critical dependencies
        required_packages = ['tweepy', 'openai']
        for package in required_packages:
            self.assertIn(package, requirements.lower(),
                         f"{package} should be in requirements.txt")


class TestBotModeWorkflows(unittest.TestCase):
    """Test different bot operation modes"""

    @patch.dict(os.environ, {
        'TWITTER_API_KEY': 'test-key',
        'TWITTER_API_SECRET': 'test-secret',
        'TWITTER_ACCESS_TOKEN': 'test-token',
        'TWITTER_ACCESS_TOKEN_SECRET': 'test-token-secret',
        'TWITTER_BEARER_TOKEN': 'test-bearer',
        'OPENAI_API_KEY': 'test-openai-key'
    })
    def test_posting_only_mode(self):
        """Test posting-only mode workflow"""
        from bot import SMESocialBot

        bot = SMESocialBot(test_mode=True)
        bot.rate_limited = True

        # In posting-only mode, just post content
        with patch('bot.openai.chat.completions.create') as mock_openai:
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "Test content"
            mock_openai.return_value = mock_response

            content = bot.generate_content()
            result = bot.post_content(content)

            self.assertTrue(result)
            self.assertEqual(bot.session_stats['posts_created'], 1)

    @patch.dict(os.environ, {
        'TWITTER_API_KEY': 'test-key',
        'TWITTER_API_SECRET': 'test-secret',
        'TWITTER_ACCESS_TOKEN': 'test-token',
        'TWITTER_ACCESS_TOKEN_SECRET': 'test-token-secret',
        'TWITTER_BEARER_TOKEN': 'test-bearer',
        'OPENAI_API_KEY': 'test-openai-key'
    })
    def test_full_engagement_mode(self):
        """Test full engagement mode workflow"""
        from bot import SMESocialBot

        bot = SMESocialBot(test_mode=True)
        bot.rate_limited = True

        # Full engagement mode: check mentions and engage
        mentions = bot.check_mentions(days_back=7)  # Weekly
        self.assertGreater(len(mentions), 0)

        engagements = bot.engage_with_mentions(mentions)
        self.assertGreater(engagements, 0)

        # Also post content
        with patch('bot.openai.chat.completions.create') as mock_openai:
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "Engagement mode content"
            mock_openai.return_value = mock_response

            content = bot.generate_content()
            result = bot.post_content(content)

            self.assertTrue(result)


class TestErrorRecoveryWorkflows(unittest.TestCase):
    """Test error handling and recovery workflows"""

    @patch.dict(os.environ, {
        'TWITTER_API_KEY': 'test-key',
        'TWITTER_API_SECRET': 'test-secret',
        'TWITTER_ACCESS_TOKEN': 'test-token',
        'TWITTER_ACCESS_TOKEN_SECRET': 'test-token-secret',
        'TWITTER_BEARER_TOKEN': 'test-bearer',
        'OPENAI_API_KEY': 'test-openai-key'
    })
    def test_rate_limit_recovery_workflow(self):
        """Test that bot recovers from rate limits"""
        from bot import SMESocialBot

        with patch('bot.tweepy.Client'):
            bot = SMESocialBot(test_mode=False, multi_platform=False)

            # Simulate rate limit error
            mock_twitter = Mock()
            mock_twitter.create_tweet.side_effect = Exception("Rate limit exceeded")
            bot.twitter = mock_twitter

            # Should switch to simulation mode
            result = bot.post_content("Test content")

            self.assertTrue(bot.rate_limited)
            # Second attempt should succeed in simulation
            self.assertTrue(result)

    @patch.dict(os.environ, {
        'TWITTER_API_KEY': 'test-key',
        'TWITTER_API_SECRET': 'test-secret',
        'TWITTER_ACCESS_TOKEN': 'test-token',
        'TWITTER_ACCESS_TOKEN_SECRET': 'test-token-secret',
        'TWITTER_BEARER_TOKEN': 'test-bearer',
        'OPENAI_API_KEY': 'test-openai-key',
        'ANTHROPIC_API_KEY': 'test-anthropic-key'
    })
    def test_ai_provider_fallback_workflow(self):
        """Test AI provider fallback chain"""
        from bot import SMESocialBot

        bot = SMESocialBot(test_mode=True)
        bot.ai_provider = 'openai'

        # OpenAI fails, should fallback
        with patch('bot.openai.chat.completions.create') as mock_openai:
            mock_openai.side_effect = Exception("OpenAI error")

            with patch('bot.anthropic.Anthropic') as mock_anthropic_class:
                mock_anthropic = Mock()
                mock_response = Mock()
                mock_response.content = [Mock()]
                mock_response.content[0].text = "Fallback content from Anthropic"
                mock_anthropic.messages.create.return_value = mock_response
                mock_anthropic_class.return_value = mock_anthropic

                content = bot.generate_content()

                # Should get content (from Anthropic or fallback)
                self.assertIsInstance(content, str)
                self.assertGreater(len(content), 0)


class TestDynamicContentWorkflow(unittest.TestCase):
    """Test dynamic content generation workflow"""

    @patch.dict(os.environ, {
        'TWITTER_API_KEY': 'test-key',
        'TWITTER_API_SECRET': 'test-secret',
        'TWITTER_ACCESS_TOKEN': 'test-token',
        'TWITTER_ACCESS_TOKEN_SECRET': 'test-token-secret',
        'TWITTER_BEARER_TOKEN': 'test-bearer',
        'OPENAI_API_KEY': 'test-openai-key'
    })
    def test_dynamic_content_integration(self):
        """Test that dynamic content engine integrates properly"""
        try:
            from dynamic_content import DynamicContentEngine

            engine = DynamicContentEngine()
            content = engine.generate_dynamic_content()

            # Should return content or None
            if content:
                self.assertIsInstance(content, str)
                self.assertLessEqual(len(content), 280)
        except ImportError:
            self.skipTest("Dynamic content engine not available")

    @patch.dict(os.environ, {
        'TWITTER_API_KEY': 'test-key',
        'TWITTER_API_SECRET': 'test-secret',
        'TWITTER_ACCESS_TOKEN': 'test-token',
        'TWITTER_ACCESS_TOKEN_SECRET': 'test-token-secret',
        'TWITTER_BEARER_TOKEN': 'test-bearer',
        'OPENAI_API_KEY': 'test-openai-key'
    })
    def test_content_generator_integration(self):
        """Test that content generator provides prompts"""
        try:
            from content_generator import get_dynamic_content_prompt

            prompt = get_dynamic_content_prompt()

            self.assertIsInstance(prompt, str)
            self.assertGreater(len(prompt), 0)
        except ImportError:
            self.skipTest("Content generator not available")


class TestLinkedInIntegration(unittest.TestCase):
    """Test LinkedIn integration workflow"""

    def test_linkedin_manager_import(self):
        """Test that LinkedIn manager can be imported"""
        try:
            from linkedin_manager import LinkedInManager
            self.assertTrue(True, "LinkedIn manager imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import LinkedIn manager: {e}")

    @patch.dict(os.environ, {
        'LINKEDIN_ACCESS_TOKEN': 'test-token'
    })
    def test_linkedin_manager_initialization(self):
        """Test LinkedIn manager initialization"""
        from linkedin_manager import LinkedInManager

        manager = LinkedInManager(access_token='test-token')
        self.assertIsNotNone(manager)

    @patch.dict(os.environ, {
        'LINKEDIN_ACCESS_TOKEN': 'test-token'
    })
    def test_linkedin_content_adaptation(self):
        """Test that content is adapted for LinkedIn"""
        from linkedin_manager import LinkedInManager

        manager = LinkedInManager(access_token='test-token')
        twitter_content = "Short tweet #AI"

        # LinkedIn adaptation should expand content
        adapted = manager._adapt_for_linkedin(twitter_content)

        self.assertIsInstance(adapted, str)
        self.assertGreaterEqual(len(adapted), len(twitter_content))


class TestSessionStatistics(unittest.TestCase):
    """Test session statistics tracking"""

    @patch.dict(os.environ, {
        'TWITTER_API_KEY': 'test-key',
        'TWITTER_API_SECRET': 'test-secret',
        'TWITTER_ACCESS_TOKEN': 'test-token',
        'TWITTER_ACCESS_TOKEN_SECRET': 'test-token-secret',
        'TWITTER_BEARER_TOKEN': 'test-bearer',
        'OPENAI_API_KEY': 'test-openai-key'
    })
    def test_stats_tracking_during_workflow(self):
        """Test that statistics are properly tracked"""
        from bot import SMESocialBot

        bot = SMESocialBot(test_mode=True)
        bot.rate_limited = True

        # Initial stats
        self.assertEqual(bot.session_stats['posts_created'], 0)
        self.assertEqual(bot.session_stats['viral_predictions'], 0)

        # Post content
        bot.post_content("Test content #AI")

        # Stats should update
        self.assertEqual(bot.session_stats['posts_created'], 1)
        self.assertEqual(bot.session_stats['viral_predictions'], 1)

        # Check mentions
        mentions = bot.check_mentions()
        engagements = bot.engage_with_mentions(mentions)

        # Engagement stats should update
        self.assertGreater(bot.session_stats['engagements_made'], 0)


if __name__ == '__main__':
    # Run with verbose output
    unittest.main(verbosity=2)
