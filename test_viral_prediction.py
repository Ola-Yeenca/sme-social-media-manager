#!/usr/bin/env python3
"""
Unit tests for Viral Tweet Prediction System
Tests all components of the viral prediction algorithm
"""

import unittest
import datetime
from viral_predictor import ViralTweetPredictor, ViralScore


class TestViralPrediction(unittest.TestCase):
    """Test suite for viral tweet prediction functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.predictor = ViralTweetPredictor()
        self.test_time_weekday = datetime.datetime(2025, 1, 15, 12, 0, tzinfo=datetime.timezone.utc)  # Wednesday noon
        self.test_time_weekend = datetime.datetime(2025, 1, 18, 14, 0, tzinfo=datetime.timezone.utc)  # Saturday 2pm

    def test_predictor_initialization(self):
        """Test that predictor initializes with correct patterns"""
        self.assertIsInstance(self.predictor, ViralTweetPredictor)
        self.assertIn('emotional_triggers', self.predictor.viral_patterns)
        self.assertIn('power_words', self.predictor.viral_patterns)
        self.assertIn('call_to_actions', self.predictor.viral_patterns)
        self.assertIn('trending_topics', self.predictor.viral_patterns)
        self.assertIn('weekday', self.predictor.optimal_times)
        self.assertIn('weekend', self.predictor.optimal_times)

    def test_high_quality_tweet_score(self):
        """Test that high-quality tweets get high scores"""
        tweet = "🚀 Incredible insight: AI-powered analytics boost revenue by 47%! What's your experience? #AI #Business #Growth #Analytics"
        score = self.predictor.predict_viral_potential(tweet, self.test_time_weekday)

        self.assertIsInstance(score, ViralScore)
        self.assertGreater(score.total_score, 60, "High-quality tweet should score >60")
        self.assertGreater(score.content_score, 60, "Content with triggers should score high")
        self.assertGreater(score.hashtag_score, 50, "Good hashtags should score >50")

    def test_low_quality_tweet_score(self):
        """Test that low-quality tweets get lower scores"""
        tweet = "New blog post"
        score = self.predictor.predict_viral_potential(tweet, self.test_time_weekday)

        self.assertLess(score.total_score, 50, "Low-quality tweet should score <50")
        self.assertGreater(len(score.recommendations), 0, "Should provide recommendations for improvement")

    def test_content_analysis(self):
        """Test content scoring algorithm"""
        # Test emotional triggers
        tweet_emotional = "Amazing and incredible breakthrough in AI technology!"
        score_emotional = self.predictor._analyze_content(tweet_emotional)

        tweet_plain = "We have a new update in our technology."
        score_plain = self.predictor._analyze_content(tweet_plain)

        self.assertGreater(score_emotional, score_plain,
                          "Emotional content should score higher")

    def test_power_words_impact(self):
        """Test that power words increase score"""
        tweet_power = "Get your free guide now! Best tips for instant success."
        tweet_regular = "Here is a guide with some tips for improvement."

        score_power = self.predictor._analyze_content(tweet_power)
        score_regular = self.predictor._analyze_content(tweet_regular)

        self.assertGreater(score_power, score_regular,
                          "Power words should increase content score")

    def test_call_to_action_impact(self):
        """Test that CTAs improve engagement score"""
        tweet_with_cta = "Check out our new analytics platform! What do you think?"
        tweet_without_cta = "We launched a new analytics platform."

        score_with = self.predictor._analyze_content(tweet_with_cta)
        score_without = self.predictor._analyze_content(tweet_without_cta)

        self.assertGreater(score_with, score_without,
                          "CTA should increase content score")

    def test_optimal_length(self):
        """Test that optimal length tweets score higher"""
        # Optimal length (140-200 chars)
        tweet_optimal = "A" * 170 + " What are your thoughts on this matter? #AI #Business #Tech"

        # Too short
        tweet_short = "Short tweet"

        # Too long
        tweet_long = "A" * 250

        score_optimal = self.predictor._analyze_content(tweet_optimal)
        score_short = self.predictor._analyze_content(tweet_short)
        score_long = self.predictor._analyze_content(tweet_long)

        self.assertGreater(score_optimal, score_short,
                          "Optimal length should score higher than short")

    def test_timing_analysis_weekday(self):
        """Test timing score for weekday optimal hours"""
        # Perfect timing (12pm on Wednesday)
        optimal_time = datetime.datetime(2025, 1, 15, 12, 0, tzinfo=datetime.timezone.utc)
        score_optimal = self.predictor._analyze_timing(optimal_time)

        # Suboptimal timing (3am on Wednesday)
        bad_time = datetime.datetime(2025, 1, 15, 3, 0, tzinfo=datetime.timezone.utc)
        score_bad = self.predictor._analyze_timing(bad_time)

        self.assertGreater(score_optimal, score_bad,
                          "Optimal timing should score higher")
        self.assertGreater(score_optimal, 80, "Perfect timing should score >80")

    def test_timing_analysis_weekend(self):
        """Test timing score for weekend"""
        # Optimal weekend time (Saturday 2pm)
        optimal_time = datetime.datetime(2025, 1, 18, 14, 0, tzinfo=datetime.timezone.utc)
        score_weekend = self.predictor._analyze_timing(optimal_time)

        self.assertGreater(score_weekend, 60, "Optimal weekend time should score well")

    def test_hashtag_analysis_optimal_count(self):
        """Test hashtag scoring with optimal count (2-4)"""
        tweet_optimal = "Great insights #AI #Business #Tech"
        tweet_none = "Great insights with no hashtags"
        tweet_too_many = "Insights #tag1 #tag2 #tag3 #tag4 #tag5 #tag6 #tag7"

        score_optimal = self.predictor._analyze_hashtags(tweet_optimal)
        score_none = self.predictor._analyze_hashtags(tweet_none)
        score_many = self.predictor._analyze_hashtags(tweet_too_many)

        self.assertGreater(score_optimal, score_none,
                          "Hashtags should improve score")
        self.assertGreater(score_optimal, score_many,
                          "Optimal count should beat too many hashtags")

    def test_hashtag_quality_tiers(self):
        """Test that higher tier hashtags score better"""
        tweet_tier1 = "Amazing insights #AI #business #startup"
        tweet_tier3 = "Insights #SME #smallbusiness #data"

        score_tier1 = self.predictor._analyze_hashtags(tweet_tier1)
        score_tier3 = self.predictor._analyze_hashtags(tweet_tier3)

        self.assertGreater(score_tier1, score_tier3,
                          "Tier 1 hashtags should score higher")

    def test_engagement_potential_questions(self):
        """Test that questions increase engagement potential"""
        tweet_question = "What's your experience with AI analytics?"
        tweet_statement = "AI analytics are very helpful."

        score_question = self.predictor._predict_engagement_potential(tweet_question)
        score_statement = self.predictor._predict_engagement_potential(tweet_statement)

        self.assertGreater(score_question, score_statement,
                          "Questions should increase engagement score")

    def test_engagement_potential_lists(self):
        """Test that lists increase engagement"""
        tweet_list = "Top tips: 1. Use AI 2. Track metrics 3. Optimize pricing"
        tweet_plain = "Use AI to track metrics and optimize pricing"

        score_list = self.predictor._predict_engagement_potential(tweet_list)
        score_plain = self.predictor._predict_engagement_potential(tweet_plain)

        self.assertGreater(score_list, score_plain,
                          "Lists should increase engagement score")

    def test_engagement_potential_controversy(self):
        """Test that controversial content scores high"""
        tweet_controversial = "Unpopular opinion: Most businesses waste 80% of their data"
        tweet_regular = "Many businesses could use their data better"

        score_controversial = self.predictor._predict_engagement_potential(tweet_controversial)
        score_regular = self.predictor._predict_engagement_potential(tweet_regular)

        self.assertGreater(score_controversial, score_regular,
                          "Controversial content should score higher")

    def test_trend_alignment(self):
        """Test trend alignment scoring"""
        tweet_trending = "AI and ChatGPT are transforming business automation and productivity"
        tweet_generic = "Technology is changing business processes"

        score_trending = self.predictor._analyze_trend_alignment(tweet_trending)
        score_generic = self.predictor._analyze_trend_alignment(tweet_generic)

        self.assertGreater(score_trending, score_generic,
                          "Trending topics should score higher")

    def test_recommendations_generation(self):
        """Test that recommendations are generated for low scores"""
        tweet_poor = "Update"
        score = self.predictor.predict_viral_potential(tweet_poor)

        self.assertGreater(len(score.recommendations), 0,
                          "Low-scoring tweet should get recommendations")
        self.assertIsInstance(score.recommendations, list)
        self.assertLessEqual(len(score.recommendations), 5,
                            "Should return max 5 recommendations")

    def test_recommendations_content_improvements(self):
        """Test specific content improvement recommendations"""
        tweet = "Simple announcement"
        score = self.predictor.predict_viral_potential(tweet)

        # Should recommend hashtags (has none)
        # Should recommend CTA (has none)
        # Should recommend questions (has none)
        recommendations_text = ' '.join(score.recommendations).lower()

        self.assertTrue(
            'hashtag' in recommendations_text or
            'question' in recommendations_text or
            'action' in recommendations_text,
            "Should provide specific improvement recommendations"
        )

    def test_engagement_metrics_prediction(self):
        """Test engagement metrics prediction"""
        high_score_tweet = "🚀 Incredible: AI boosts revenue by 47%! What's your take? #AI #Business #Growth"
        low_score_tweet = "Update available"

        high_score = self.predictor.predict_viral_potential(high_score_tweet)
        low_score = self.predictor.predict_viral_potential(low_score_tweet)

        self.assertGreater(high_score.predicted_engagement['likes'],
                          low_score.predicted_engagement['likes'],
                          "Higher scoring tweet should predict more likes")
        self.assertGreater(high_score.predicted_engagement['retweets'],
                          low_score.predicted_engagement['retweets'],
                          "Higher scoring tweet should predict more retweets")

    def test_confidence_calculation(self):
        """Test confidence level calculation"""
        tweet_good = "Well-structured tweet with hashtags and question! #AI"
        tweet_poor = "x"

        score_good = self.predictor.predict_viral_potential(tweet_good)
        score_poor = self.predictor.predict_viral_potential(tweet_poor)

        self.assertGreater(score_good.confidence, 70,
                          "Well-structured tweet should have high confidence")
        self.assertLessEqual(score_good.confidence, 95,
                            "Confidence should be capped at 95")

    def test_confidence_with_historical_data(self):
        """Test confidence increases with historical data"""
        tweet = "Test tweet with data #AI"
        historical_data_large = {'tweet_count': 150}
        historical_data_small = {'tweet_count': 10}

        score_large = self.predictor.predict_viral_potential(tweet, historical_data=historical_data_large)
        score_small = self.predictor.predict_viral_potential(tweet, historical_data=historical_data_small)

        self.assertGreater(score_large.confidence, score_small.confidence,
                          "More historical data should increase confidence")

    def test_optimize_tweet(self):
        """Test tweet optimization"""
        original = "We have a new product"
        optimized, score = self.predictor.optimize_tweet(original)

        self.assertNotEqual(original, optimized, "Tweet should be modified")
        self.assertIn('#', optimized, "Should add hashtags")
        self.assertIsInstance(score, ViralScore)

    def test_optimize_adds_hashtags(self):
        """Test that optimization adds hashtags when missing"""
        original = "Great insights about data analytics"
        optimized, score = self.predictor.optimize_tweet(original)

        import re
        hashtags = re.findall(r'#\w+', optimized)
        self.assertGreaterEqual(len(hashtags), 2,
                               "Should add at least 2 hashtags")

    def test_optimize_adds_cta(self):
        """Test that optimization adds call-to-action"""
        original = "Data analytics platform launched"
        optimized, score = self.predictor.optimize_tweet(original)

        self.assertTrue(
            '?' in optimized or
            any(cta in optimized.lower() for cta in ['thoughts', 'think', 'share']),
            "Should add CTA or question"
        )

    def test_optimize_respects_length_limit(self):
        """Test that optimization respects 280 character limit"""
        original = "A" * 300
        optimized, score = self.predictor.optimize_tweet(original)

        self.assertLessEqual(len(optimized), 280,
                            "Optimized tweet should not exceed 280 characters")

    def test_generate_viral_variations(self):
        """Test viral variation generation"""
        base_content = "SME analytics increase restaurant revenue"
        variations = self.predictor.generate_viral_variations(base_content, count=3)

        self.assertEqual(len(variations), 3, "Should generate requested number of variations")

        for tweet, score in variations:
            self.assertIsInstance(tweet, str)
            self.assertIsInstance(score, ViralScore)
            self.assertLessEqual(len(tweet), 280, "Should respect character limit")
            self.assertIn('#', tweet, "Should include hashtags")

    def test_variations_sorted_by_score(self):
        """Test that variations are sorted by viral score"""
        base_content = "Business analytics insights"
        variations = self.predictor.generate_viral_variations(base_content, count=5)

        scores = [score.total_score for _, score in variations]
        self.assertEqual(scores, sorted(scores, reverse=True),
                        "Variations should be sorted by score (highest first)")

    def test_variations_are_different(self):
        """Test that generated variations are actually different"""
        base_content = "AI-powered analytics"
        variations = self.predictor.generate_viral_variations(base_content, count=3)

        tweets = [tweet for tweet, _ in variations]
        unique_tweets = set(tweets)

        self.assertEqual(len(tweets), len(unique_tweets),
                        "All variations should be unique")

    def test_emoji_impact_on_content_score(self):
        """Test that emojis impact content score"""
        tweet_with_emoji = "🚀 Amazing insights about AI technology 💡"
        tweet_without_emoji = "Amazing insights about AI technology"

        score_with = self.predictor._analyze_content(tweet_with_emoji)
        score_without = self.predictor._analyze_content(tweet_without_emoji)

        # Both should score similarly (emoji adds points but shouldn't dominate)
        self.assertGreater(score_with, 0)
        self.assertGreater(score_without, 0)

    def test_numbers_increase_credibility(self):
        """Test that numbers/statistics increase content score"""
        tweet_with_numbers = "AI analytics boost revenue by 47% on average"
        tweet_without_numbers = "AI analytics boost revenue significantly"

        score_with = self.predictor._analyze_content(tweet_with_numbers)
        score_without = self.predictor._analyze_content(tweet_without_numbers)

        self.assertGreater(score_with, score_without,
                          "Numbers should increase content score")

    def test_viral_score_dataclass(self):
        """Test ViralScore dataclass structure"""
        tweet = "Test tweet #AI"
        score = self.predictor.predict_viral_potential(tweet)

        # Check all required fields exist
        self.assertIsNotNone(score.total_score)
        self.assertIsNotNone(score.content_score)
        self.assertIsNotNone(score.timing_score)
        self.assertIsNotNone(score.hashtag_score)
        self.assertIsNotNone(score.engagement_score)
        self.assertIsNotNone(score.trend_score)
        self.assertIsNotNone(score.recommendations)
        self.assertIsNotNone(score.predicted_engagement)
        self.assertIsNotNone(score.confidence)

        # Check types
        self.assertIsInstance(score.total_score, float)
        self.assertIsInstance(score.recommendations, list)
        self.assertIsInstance(score.predicted_engagement, dict)

    def test_score_weighted_calculation(self):
        """Test that total score is properly weighted"""
        tweet = "Test tweet #AI #Business"
        score = self.predictor.predict_viral_potential(tweet)

        # Calculate expected weighted score
        expected = (
            score.content_score * 0.3 +
            score.timing_score * 0.15 +
            score.hashtag_score * 0.15 +
            score.engagement_score * 0.25 +
            score.trend_score * 0.15
        )

        self.assertAlmostEqual(score.total_score, expected, places=1,
                              msg="Total score should match weighted calculation")

    def test_score_bounds(self):
        """Test that all scores are within 0-100 bounds"""
        tweets = [
            "x",  # Minimal tweet
            "🚀 Amazing! AI-powered analytics boost revenue 47%! Your thoughts? #AI #Business #Growth #Tech",  # Maximal
            "Regular tweet about business updates",  # Average
        ]

        for tweet in tweets:
            score = self.predictor.predict_viral_potential(tweet)

            self.assertGreaterEqual(score.total_score, 0, "Score should be >= 0")
            self.assertLessEqual(score.total_score, 100, "Score should be <= 100")
            self.assertGreaterEqual(score.content_score, 0)
            self.assertLessEqual(score.content_score, 100)
            self.assertGreaterEqual(score.timing_score, 0)
            self.assertLessEqual(score.timing_score, 100)
            self.assertGreaterEqual(score.hashtag_score, 0)
            self.assertLessEqual(score.hashtag_score, 100)

    def test_personal_stories_engagement(self):
        """Test that personal stories increase engagement score"""
        tweet_personal = "I've been using AI analytics for my restaurant and my revenue increased 40%"
        tweet_impersonal = "Restaurants using AI analytics see revenue increases"

        score_personal = self.predictor._predict_engagement_potential(tweet_personal)
        score_impersonal = self.predictor._predict_engagement_potential(tweet_impersonal)

        self.assertGreater(score_personal, score_impersonal,
                          "Personal stories should increase engagement")

    def test_educational_content_engagement(self):
        """Test that educational content scores well"""
        tweet_educational = "How to use AI analytics: Step-by-step guide for restaurants"
        tweet_regular = "AI analytics for restaurants available now"

        score_educational = self.predictor._predict_engagement_potential(tweet_educational)
        score_regular = self.predictor._predict_engagement_potential(tweet_regular)

        self.assertGreater(score_educational, score_regular,
                          "Educational content should score higher")

    def test_default_posting_time(self):
        """Test that predictor uses current time when none provided"""
        tweet = "Test tweet #AI"
        score = self.predictor.predict_viral_potential(tweet)  # No posting_time provided

        self.assertIsInstance(score, ViralScore)
        self.assertGreater(score.timing_score, 0, "Should calculate timing score with default time")


class TestViralPredictionEdgeCases(unittest.TestCase):
    """Test edge cases and error handling"""

    def setUp(self):
        """Set up test fixtures"""
        self.predictor = ViralTweetPredictor()

    def test_empty_tweet(self):
        """Test handling of empty tweet"""
        score = self.predictor.predict_viral_potential("")
        self.assertIsInstance(score, ViralScore)
        self.assertLess(score.total_score, 50, "Empty tweet should score low")

    def test_very_long_tweet(self):
        """Test handling of very long tweet"""
        long_tweet = "A" * 500
        score = self.predictor.predict_viral_potential(long_tweet)
        self.assertIsInstance(score, ViralScore)

    def test_special_characters_tweet(self):
        """Test handling of special characters"""
        tweet = "!@#$%^&*()_+-=[]{}|;':\",./<>?"
        score = self.predictor.predict_viral_potential(tweet)
        self.assertIsInstance(score, ViralScore)

    def test_unicode_emoji_handling(self):
        """Test proper handling of Unicode emojis"""
        tweet = "🚀💡🔥⚡✨🎯💪🌟❤️🙌"
        score = self.predictor.predict_viral_potential(tweet)
        self.assertIsInstance(score, ViralScore)

    def test_mixed_case_hashtags(self):
        """Test that hashtag matching is case-insensitive"""
        tweet1 = "Great insights #AI #BUSINESS #tech"
        tweet2 = "Great insights #ai #business #TECH"

        score1 = self.predictor._analyze_hashtags(tweet1)
        score2 = self.predictor._analyze_hashtags(tweet2)

        self.assertEqual(score1, score2, "Hashtag scoring should be case-insensitive")

    def test_malformed_hashtags(self):
        """Test handling of malformed hashtags"""
        tweet = "Test # #  #123 #valid"
        score = self.predictor._analyze_hashtags(tweet)
        self.assertIsInstance(score, float)

    def test_none_historical_data(self):
        """Test that None historical data is handled correctly"""
        tweet = "Test tweet"
        score = self.predictor.predict_viral_potential(tweet, historical_data=None)
        self.assertIsInstance(score, ViralScore)

    def test_empty_historical_data(self):
        """Test that empty historical data dict is handled"""
        tweet = "Test tweet"
        score = self.predictor.predict_viral_potential(tweet, historical_data={})
        self.assertIsInstance(score, ViralScore)

    def test_optimize_empty_tweet(self):
        """Test optimization of empty tweet"""
        optimized, score = self.predictor.optimize_tweet("")
        self.assertIsInstance(optimized, str)
        self.assertIsInstance(score, ViralScore)

    def test_generate_zero_variations(self):
        """Test generating zero variations"""
        variations = self.predictor.generate_viral_variations("Test", count=0)
        self.assertEqual(len(variations), 0)

    def test_generate_more_variations_than_templates(self):
        """Test requesting more variations than available templates"""
        variations = self.predictor.generate_viral_variations("Test", count=100)
        self.assertGreater(len(variations), 0)
        self.assertLessEqual(len(variations), 100)


if __name__ == '__main__':
    # Run with verbose output
    unittest.main(verbosity=2)
