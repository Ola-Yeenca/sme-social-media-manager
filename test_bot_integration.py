#!/usr/bin/env python3
"""
Integration tests for SME Social Media Bot
Tests bot functionality with mocked APIs
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
from datetime import datetime, timedelta

# Mock the external libraries before importing bot
sys.modules['tweepy'] = MagicMock()
sys.modules['openai'] = MagicMock()
sys.modules['groq'] = MagicMock()
sys.modules['anthropic'] = MagicMock()

from bot import SMESocialBot


class TestBotInitialization(unittest.TestCase):
    """Test bot initialization and setup"""

    @patch('bot.Config')
    def test_bot_initialization_test_mode(self, mock_config):
        """Test bot initializes correctly in test mode"""
        mock_config_instance = Mock()
        mock_config.return_value = mock_config_instance

        bot = SMESocialBot(test_mode=True)

        self.assertTrue(bot.test_mode)
        self.assertIsNotNone(bot.config)
        self.assertIsNotNone(bot.viral_predictor)
        self.assertEqual(bot.session_stats['posts_created'], 0)
        self.assertEqual(bot.session_stats['errors'], 0)

    @patch('bot.ViralTweetPredictor')
    @patch('bot.Config')
    def test_viral_predictor_initialized(self, mock_config, mock_viral):
        """Test that viral predictor is initialized"""
        mock_config_instance = Mock()
        mock_config.return_value = mock_config_instance

        bot = SMESocialBot(test_mode=True)

        self.assertIsNotNone(bot.viral_predictor)
        mock_viral.assert_called_once()

    @patch('bot.Config')
    def test_session_stats_initialized(self, mock_config):
        """Test that session stats are properly initialized"""
        mock_config_instance = Mock()
        mock_config.return_value = mock_config_instance

        bot = SMESocialBot(test_mode=True)

        required_keys = [
            'posts_created', 'linkedin_posts', 'mentions_checked',
            'engagements_made', 'errors', 'viral_predictions'
        ]

        for key in required_keys:
            self.assertIn(key, bot.session_stats)
            self.assertEqual(bot.session_stats[key], 0)


class TestAIProviderSetup(unittest.TestCase):
    """Test AI provider initialization and fallback"""

    @patch('bot.Config')
    def test_openai_as_primary_provider(self, mock_config):
        """Test OpenAI is set as primary provider when available"""
        mock_config_instance = Mock()
        mock_config_instance.openai_api_key = 'test-openai-key'
        mock_config_instance.anthropic_api_key = None
        mock_config_instance.grok_api_key = None
        mock_config.return_value = mock_config_instance

        bot = SMESocialBot(test_mode=True)

        self.assertEqual(bot.ai_provider, 'openai')

    @patch('bot.Config')
    def test_anthropic_as_fallback_provider(self, mock_config):
        """Test Anthropic is used when OpenAI unavailable"""
        mock_config_instance = Mock()
        mock_config_instance.openai_api_key = None
        mock_config_instance.anthropic_api_key = 'test-anthropic-key'
        mock_config_instance.grok_api_key = None
        mock_config.return_value = mock_config_instance

        with patch('bot.anthropic.Anthropic') as mock_anthropic:
            bot = SMESocialBot(test_mode=True)

            self.assertEqual(bot.ai_provider, 'anthropic')
            self.assertIsNotNone(bot.anthropic_client)

    @patch('bot.Config')
    def test_grok_as_second_fallback(self, mock_config):
        """Test Grok is used when both OpenAI and Anthropic unavailable"""
        mock_config_instance = Mock()
        mock_config_instance.openai_api_key = None
        mock_config_instance.anthropic_api_key = None
        mock_config_instance.grok_api_key = 'test-grok-key'
        mock_config.return_value = mock_config_instance

        with patch('bot.groq.Groq') as mock_groq:
            bot = SMESocialBot(test_mode=True)

            self.assertEqual(bot.ai_provider, 'grok')
            self.assertIsNotNone(bot.grok_client)


class TestContentGeneration(unittest.TestCase):
    """Test content generation functionality"""

    @patch('bot.Config')
    def setUp(self, mock_config):
        """Set up test bot"""
        mock_config_instance = Mock()
        mock_config_instance.openai_api_key = 'test-key'
        mock_config_instance.anthropic_api_key = None
        mock_config_instance.grok_api_key = None
        mock_config.return_value = mock_config_instance

        self.bot = SMESocialBot(test_mode=True)

    def test_generate_content_returns_string(self):
        """Test that generate_content returns a string"""
        with patch('bot.openai.chat.completions.create') as mock_openai:
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "Test tweet content"
            mock_openai.return_value = mock_response

            content = self.bot.generate_content()

            self.assertIsInstance(content, str)
            self.assertGreater(len(content), 0)

    def test_generate_content_under_280_chars(self):
        """Test that generated content respects 280 char limit"""
        with patch('bot.openai.chat.completions.create') as mock_openai:
            # Simulate long content
            long_content = "A" * 300
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = long_content
            mock_openai.return_value = mock_response

            content = self.bot.generate_content()

            self.assertLessEqual(len(content), 280)

    def test_content_generation_fallback_to_anthropic(self):
        """Test fallback to Anthropic when OpenAI fails"""
        self.bot.ai_provider = 'openai'
        self.bot.config.anthropic_api_key = 'test-anthropic-key'

        with patch('bot.openai.chat.completions.create') as mock_openai:
            mock_openai.side_effect = Exception("OpenAI API error")

            with patch('bot.anthropic.Anthropic') as mock_anthropic_class:
                mock_anthropic = Mock()
                mock_response = Mock()
                mock_response.content = [Mock()]
                mock_response.content[0].text = "Anthropic generated content"
                mock_anthropic.messages.create.return_value = mock_response
                mock_anthropic_class.return_value = mock_anthropic

                content = self.bot.generate_content()

                # Should fallback to Anthropic or use fallback content
                self.assertIsInstance(content, str)
                self.assertGreater(len(content), 0)

    def test_content_generation_uses_fallback_on_total_failure(self):
        """Test that fallback content is used when all AI providers fail"""
        self.bot.ai_provider = 'openai'

        with patch('bot.openai.chat.completions.create') as mock_openai:
            mock_openai.side_effect = Exception("All providers failed")

            content = self.bot.generate_content()

            # Should use fallback content
            self.assertIsInstance(content, str)
            self.assertGreater(len(content), 0)
            self.assertEqual(self.bot.session_stats['errors'], 1)


class TestPostingFunctionality(unittest.TestCase):
    """Test posting to Twitter"""

    @patch('bot.Config')
    def setUp(self, mock_config):
        """Set up test bot with mocked Twitter"""
        mock_config_instance = Mock()
        mock_config_instance.openai_api_key = 'test-key'
        mock_config_instance.twitter_bearer_token = 'test-bearer'
        mock_config_instance.twitter_api_key = 'test-key'
        mock_config_instance.twitter_api_secret = 'test-secret'
        mock_config_instance.twitter_access_token = 'test-token'
        mock_config_instance.twitter_access_token_secret = 'test-secret'
        mock_config.return_value = mock_config_instance

        with patch('bot.tweepy.Client'):
            self.bot = SMESocialBot(test_mode=False, multi_platform=False)

    def test_post_content_with_viral_prediction(self):
        """Test that posting includes viral prediction"""
        content = "Test tweet content #AI #Business"

        mock_twitter = Mock()
        mock_response = Mock()
        mock_response.data = {'id': '12345'}
        mock_twitter.create_tweet.return_value = mock_response
        self.bot.twitter = mock_twitter

        result = self.bot.post_content(content)

        self.assertTrue(result)
        self.assertEqual(self.bot.session_stats['posts_created'], 1)
        self.assertEqual(self.bot.session_stats['viral_predictions'], 1)
        mock_twitter.create_tweet.assert_called_once()

    def test_post_content_optimization_low_score(self):
        """Test that low-scoring content gets optimized"""
        # Content with low viral score
        content = "Simple update"

        mock_twitter = Mock()
        mock_response = Mock()
        mock_response.data = {'id': '12345'}
        mock_twitter.create_tweet.return_value = mock_response
        self.bot.twitter = mock_twitter

        result = self.bot.post_content(content)

        # Should still post (optimized or original)
        self.assertTrue(result)
        mock_twitter.create_tweet.assert_called_once()

    def test_post_content_handles_rate_limit(self):
        """Test rate limit handling during posting"""
        content = "Test content"

        mock_twitter = Mock()
        mock_twitter.create_tweet.side_effect = Exception("Rate limit exceeded")
        self.bot.twitter = mock_twitter

        result = self.bot.post_content(content)

        # Should switch to simulation mode
        self.assertTrue(hasattr(self.bot, 'rate_limited'))
        self.assertTrue(self.bot.rate_limited)
        # Second attempt should succeed in simulation
        self.assertTrue(result)

    def test_post_content_handles_empty_content(self):
        """Test that empty content is rejected"""
        result = self.bot.post_content("")

        self.assertFalse(result)

    def test_post_content_simulation_mode(self):
        """Test posting in simulation mode (rate limited)"""
        content = "Test content for simulation"
        self.bot.rate_limited = True

        result = self.bot.post_content(content)

        self.assertTrue(result)
        self.assertEqual(self.bot.session_stats['posts_created'], 1)


class TestMultiPlatformPosting(unittest.TestCase):
    """Test multi-platform posting functionality"""

    @patch('bot.Config')
    @patch('bot.LinkedInManager')
    def setUp(self, mock_linkedin, mock_config):
        """Set up test bot with multi-platform support"""
        mock_config_instance = Mock()
        mock_config_instance.openai_api_key = 'test-key'
        mock_config_instance.linkedin_access_token = 'test-linkedin-token'
        mock_config_instance.twitter_bearer_token = 'test-bearer'
        mock_config_instance.twitter_api_key = 'test-key'
        mock_config_instance.twitter_api_secret = 'test-secret'
        mock_config_instance.twitter_access_token = 'test-token'
        mock_config_instance.twitter_access_token_secret = 'test-secret'
        mock_config.return_value = mock_config_instance

        with patch('bot.tweepy.Client'):
            self.bot = SMESocialBot(test_mode=False, multi_platform=True)

    def test_post_multi_platform_twitter_and_linkedin(self):
        """Test posting to both Twitter and LinkedIn"""
        content = "Multi-platform test content #AI"

        # Mock Twitter
        mock_twitter = Mock()
        mock_response = Mock()
        mock_response.data = {'id': '12345'}
        mock_twitter.create_tweet.return_value = mock_response
        self.bot.twitter = mock_twitter

        # Mock LinkedIn
        mock_linkedin = Mock()
        mock_linkedin.post_to_linkedin.return_value = (True, {'id': 'linkedin-123'})
        self.bot.linkedin = mock_linkedin

        result = self.bot.post_multi_platform(content)

        self.assertTrue(result)
        mock_twitter.create_tweet.assert_called_once()
        mock_linkedin.post_to_linkedin.assert_called_once_with(content, optimize_viral=True)
        self.assertEqual(self.bot.session_stats['linkedin_posts'], 1)

    def test_post_multi_platform_linkedin_not_configured(self):
        """Test multi-platform posting when LinkedIn not configured"""
        content = "Test content"
        self.bot.linkedin = None

        mock_twitter = Mock()
        mock_response = Mock()
        mock_response.data = {'id': '12345'}
        mock_twitter.create_tweet.return_value = mock_response
        self.bot.twitter = mock_twitter

        result = self.bot.post_multi_platform(content)

        # Should still succeed with Twitter only
        self.assertTrue(result)
        self.assertEqual(self.bot.session_stats['linkedin_posts'], 0)

    def test_post_multi_platform_linkedin_fails(self):
        """Test handling of LinkedIn posting failure"""
        content = "Test content"

        # Mock Twitter (succeeds)
        mock_twitter = Mock()
        mock_response = Mock()
        mock_response.data = {'id': '12345'}
        mock_twitter.create_tweet.return_value = mock_response
        self.bot.twitter = mock_twitter

        # Mock LinkedIn (fails)
        mock_linkedin = Mock()
        mock_linkedin.post_to_linkedin.return_value = (False, {'error': 'LinkedIn error'})
        self.bot.linkedin = mock_linkedin

        result = self.bot.post_multi_platform(content)

        # Should still return True if Twitter succeeded
        self.assertTrue(result)


class TestMentionHandling(unittest.TestCase):
    """Test mention checking and engagement"""

    @patch('bot.Config')
    def setUp(self, mock_config):
        """Set up test bot"""
        mock_config_instance = Mock()
        mock_config_instance.openai_api_key = 'test-key'
        mock_config_instance.twitter_bearer_token = 'test-bearer'
        mock_config_instance.twitter_api_key = 'test-key'
        mock_config_instance.twitter_api_secret = 'test-secret'
        mock_config_instance.twitter_access_token = 'test-token'
        mock_config_instance.twitter_access_token_secret = 'test-secret'
        mock_config.return_value = mock_config_instance

        with patch('bot.tweepy.Client'):
            self.bot = SMESocialBot(test_mode=False, multi_platform=False)

    def test_check_mentions_simulation_mode(self):
        """Test checking mentions in simulation mode"""
        self.bot.rate_limited = True

        mentions = self.bot.check_mentions(days_back=1)

        self.assertIsInstance(mentions, list)
        self.assertGreater(len(mentions), 0)
        # Should get 3 simulated mentions for 1 day
        self.assertEqual(len(mentions), 3)

    def test_check_mentions_weekly_mode(self):
        """Test checking mentions for weekly engagement (7 days)"""
        self.bot.rate_limited = True

        mentions = self.bot.check_mentions(days_back=7)

        self.assertIsInstance(mentions, list)
        # Should get 5 simulated mentions for weekly
        self.assertEqual(len(mentions), 5)

    def test_check_mentions_live_mode(self):
        """Test checking mentions via live API"""
        mock_twitter = Mock()
        mock_me = Mock()
        mock_me.data.id = 'user123'
        mock_twitter.get_me.return_value = mock_me

        mock_mentions = Mock()
        mock_mention1 = Mock()
        mock_mention1.id = 'mention1'
        mock_mention1.text = 'Test mention'
        mock_mention1.author_id = 'user456'
        mock_mention1.created_at = datetime.now()
        mock_mentions.data = [mock_mention1]
        mock_twitter.get_users_mentions.return_value = mock_mentions

        self.bot.twitter = mock_twitter

        mentions = self.bot.check_mentions(days_back=1)

        self.assertEqual(len(mentions), 1)
        self.assertEqual(mentions[0]['id'], 'mention1')
        mock_twitter.get_users_mentions.assert_called_once()

    def test_check_mentions_handles_rate_limit(self):
        """Test rate limit handling during mention check"""
        mock_twitter = Mock()
        mock_twitter.get_me.side_effect = Exception("Rate limit exceeded")
        self.bot.twitter = mock_twitter

        mentions = self.bot.check_mentions(days_back=1)

        # Should switch to simulation mode
        self.assertTrue(self.bot.rate_limited)
        self.assertGreater(len(mentions), 0)

    def test_engage_with_mentions_simulation(self):
        """Test engagement in simulation mode"""
        self.bot.rate_limited = True
        mentions = [
            {'id': '1', 'text': 'Great content!', 'author_id': 'user1'},
            {'id': '2', 'text': 'Love your insights', 'author_id': 'user2'},
        ]

        engagements = self.bot.engage_with_mentions(mentions)

        self.assertGreater(engagements, 0)
        self.assertEqual(self.bot.session_stats['engagements_made'], engagements)

    def test_engage_with_mentions_live_mode(self):
        """Test engagement via live API"""
        mock_twitter = Mock()
        self.bot.twitter = mock_twitter

        mentions = [
            {'id': '1', 'text': 'Great content!', 'author_id': 'user1'},
        ]

        with patch.object(self.bot, 'generate_reply', return_value=None):
            engagements = self.bot.engage_with_mentions(mentions)

            # Should like at least
            mock_twitter.like.assert_called()
            self.assertGreater(engagements, 0)

    def test_engage_with_mentions_limits_to_three(self):
        """Test that engagement is limited to 3 mentions"""
        self.bot.rate_limited = True
        mentions = [
            {'id': str(i), 'text': f'Mention {i}', 'author_id': f'user{i}'}
            for i in range(10)
        ]

        engagements = self.bot.engage_with_mentions(mentions)

        # Should only engage with first 3
        self.assertLessEqual(engagements, 6)  # Max 2 per mention (like + reply)


class TestViralContentGeneration(unittest.TestCase):
    """Test viral content generation and optimization"""

    @patch('bot.Config')
    def setUp(self, mock_config):
        """Set up test bot"""
        mock_config_instance = Mock()
        mock_config_instance.openai_api_key = 'test-key'
        mock_config.return_value = mock_config_instance

        self.bot = SMESocialBot(test_mode=True)

    def test_generate_viral_content(self):
        """Test viral variation generation"""
        base_idea = "AI analytics for restaurants"

        variations = self.bot.generate_viral_content(base_idea)

        self.assertIsInstance(variations, list)
        self.assertEqual(len(variations), 3)

        for tweet, score in variations:
            self.assertIsInstance(tweet, str)
            self.assertLessEqual(len(tweet), 280)
            self.assertGreater(score.total_score, 0)

    def test_generate_viral_content_default_base(self):
        """Test viral generation with default base idea"""
        variations = self.bot.generate_viral_content()

        self.assertIsInstance(variations, list)
        self.assertGreater(len(variations), 0)

    def test_post_best_viral_content(self):
        """Test posting the best viral variation"""
        self.bot.rate_limited = True

        with patch.object(self.bot, 'generate_content', return_value="Test base content"):
            result = self.bot.post_best_viral_content(multi_platform=False)

            # Should successfully post in simulation
            self.assertTrue(result)
            self.assertGreater(self.bot.session_stats['posts_created'], 0)


class TestReplyGeneration(unittest.TestCase):
    """Test reply generation for mentions"""

    @patch('bot.Config')
    def setUp(self, mock_config):
        """Set up test bot"""
        mock_config_instance = Mock()
        mock_config_instance.openai_api_key = 'test-key'
        mock_config_instance.anthropic_api_key = None
        mock_config_instance.grok_api_key = None
        mock_config.return_value = mock_config_instance

        self.bot = SMESocialBot(test_mode=True)

    def test_generate_reply_returns_string(self):
        """Test that reply generation returns a string"""
        original_text = "Love your restaurant analytics insights!"

        with patch('bot.openai.chat.completions.create') as mock_openai:
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "Thanks for the support!"
            mock_openai.return_value = mock_response

            reply = self.bot.generate_reply(original_text)

            self.assertIsInstance(reply, str)
            self.assertGreater(len(reply), 0)

    def test_generate_reply_under_280_chars(self):
        """Test that replies respect character limit"""
        original_text = "Can you help with pricing?"

        with patch('bot.openai.chat.completions.create') as mock_openai:
            long_reply = "A" * 300
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = long_reply
            mock_openai.return_value = mock_response

            reply = self.bot.generate_reply(original_text)

            self.assertLessEqual(len(reply), 280)

    def test_generate_reply_handles_failure(self):
        """Test reply generation handles AI failures"""
        original_text = "Question about analytics"

        with patch('bot.openai.chat.completions.create') as mock_openai:
            mock_openai.side_effect = Exception("AI error")

            reply = self.bot.generate_reply(original_text)

            # Should return None or fallback
            self.assertIsNone(reply)


class TestErrorHandling(unittest.TestCase):
    """Test error handling and recovery"""

    @patch('bot.Config')
    def setUp(self, mock_config):
        """Set up test bot"""
        mock_config_instance = Mock()
        mock_config_instance.openai_api_key = 'test-key'
        mock_config.return_value = mock_config_instance

        self.bot = SMESocialBot(test_mode=True)

    def test_error_stats_tracking(self):
        """Test that errors are tracked in stats"""
        initial_errors = self.bot.session_stats['errors']

        # Force an error in content generation
        with patch('bot.openai.chat.completions.create') as mock_openai:
            mock_openai.side_effect = Exception("API error")

            content = self.bot.generate_content()

            # Should increment error count
            self.assertEqual(self.bot.session_stats['errors'], initial_errors + 1)
            # Should return fallback content
            self.assertIsInstance(content, str)

    def test_rate_limit_flag_persistence(self):
        """Test that rate limit flag persists across operations"""
        self.bot.rate_limited = True

        # Should stay in simulation mode for all operations
        mentions = self.bot.check_mentions()
        self.assertIsInstance(mentions, list)

        result = self.bot.post_content("Test content")
        self.assertTrue(result)

        # Rate limited flag should persist
        self.assertTrue(self.bot.rate_limited)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""

    @patch('bot.Config')
    def setUp(self, mock_config):
        """Set up test bot"""
        mock_config_instance = Mock()
        mock_config_instance.openai_api_key = 'test-key'
        mock_config.return_value = mock_config_instance

        self.bot = SMESocialBot(test_mode=True)

    def test_empty_mentions_list(self):
        """Test handling of empty mentions list"""
        engagements = self.bot.engage_with_mentions([])

        self.assertEqual(engagements, 0)

    def test_none_content_posting(self):
        """Test posting None content"""
        result = self.bot.post_content(None)

        self.assertFalse(result)

    def test_very_long_content(self):
        """Test handling of extremely long content"""
        long_content = "A" * 1000
        self.bot.rate_limited = True

        result = self.bot.post_content(long_content)

        # Should still attempt to post (truncated by viral predictor)
        self.assertTrue(result)


if __name__ == '__main__':
    # Run with verbose output
    unittest.main(verbosity=2)
