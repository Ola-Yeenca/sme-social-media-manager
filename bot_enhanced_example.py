#!/usr/bin/env python3
"""
Enhanced SME Social Media Bot - Example Integration
Demonstrates usage of new logging, AI provider, config, and analytics infrastructure
"""

from logger import get_logger
from ai_provider import AIProviderChain
from config_loader import ConfigLoader
from analytics_dashboard import BotAnalytics
from config import Config

# Setup logging
logger = get_logger(__name__, level="INFO")


def main():
    """
    Example of enhanced bot usage with all new features
    """
    logger.info("="*60)
    logger.info("Enhanced SME Social Media Bot - Starting...")
    logger.info("="*60)

    try:
        # 1. Load configuration
        logger.info("📋 Loading configuration...")
        runtime_config = ConfigLoader.load()
        env_config = Config()  # Environment variables

        logger.info(f"✅ Configuration loaded")
        logger.info(f"   Min viral score: {ConfigLoader.get_min_viral_score()}")
        logger.info(f"   Posting hours: {ConfigLoader.get_posting_hours()}")
        logger.info(f"   Auto-optimize: {ConfigLoader.get('viral_prediction.auto_optimize')}")

        # 2. Initialize AI Provider Chain
        logger.info("\n🤖 Initializing AI provider chain...")
        ai_chain = AIProviderChain(env_config)

        stats = ai_chain.get_provider_stats()
        logger.info(f"✅ AI chain initialized with {stats['total_providers']} providers")
        logger.info(f"   Current provider: {stats['current_provider']}")

        # 3. Initialize Analytics
        logger.info("\n📊 Initializing analytics dashboard...")
        analytics = BotAnalytics()
        logger.info(f"✅ Analytics initialized with {len(analytics.posts)} historical posts")

        # 4. Generate content with AI provider chain
        logger.info("\n📝 Generating content...")

        prompt = "Write a concise tweet about restaurant analytics (under 200 characters)"
        system_context = "You are the social media manager for SME Analytica, a restaurant analytics company"

        response = ai_chain.generate(
            prompt=prompt,
            system_context=system_context,
            max_tokens=100,
            temperature=0.7
        )

        logger.info(f"✅ Content generated using {response.provider.value}")
        logger.info(f"   Length: {len(response.content)} characters")
        logger.info(f"   Tokens used: {response.tokens_used}")
        logger.info(f"   Content: {response.content}")

        # 5. Predict viral score (using existing viral_predictor)
        from viral_predictor import ViralTweetPredictor

        logger.info("\n🎯 Predicting viral potential...")
        predictor = ViralTweetPredictor()
        viral_score = predictor.predict_viral_potential(response.content)

        logger.info(f"✅ Viral prediction complete")
        logger.info(f"   Total score: {viral_score.total_score}/100")
        logger.info(f"   Content: {viral_score.content_score}/100")
        logger.info(f"   Engagement: {viral_score.engagement_score}/100")
        logger.info(f"   Predicted likes: {viral_score.predicted_engagement['likes']}")
        logger.info(f"   Predicted retweets: {viral_score.predicted_engagement['retweets']}")

        # 6. Log to analytics
        logger.info("\n📈 Logging to analytics...")
        analytics.log_post(
            content=response.content,
            viral_score=viral_score.total_score,
            predicted_engagement=viral_score.predicted_engagement,
            platform="twitter",
            optimized=False
        )
        logger.info("✅ Post logged to analytics")

        # 7. Generate analytics report
        logger.info("\n📊 Generating analytics report...")
        report = analytics.generate_report(days=30)
        print(report)

        # 8. Summary
        logger.info("\n" + "="*60)
        logger.info("✅ Enhanced bot demo completed successfully!")
        logger.info("="*60)
        logger.info("\n📁 Check the following directories:")
        logger.info("   logs/           - Bot execution logs")
        logger.info("   analytics_data/ - Performance metrics")

        return True

    except Exception as e:
        logger.error(f"❌ Bot execution failed: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    import sys

    success = main()
    sys.exit(0 if success else 1)
