#!/usr/bin/env python3
"""
Demo script to showcase the SME Social Media Bot testing capabilities
Runs a subset of tests to demonstrate functionality
"""

import os
import sys
import time
from datetime import datetime

# Ensure we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_viral_prediction_tests():
    """Demonstrate viral prediction testing"""
    print("🎯 Viral Prediction System Demo")
    print("-" * 40)
    
    from viral_predictor import ViralTweetPredictor
    
    predictor = ViralTweetPredictor()
    
    # Test different types of content
    test_cases = [
        ("High viral potential", "🚀 BREAKING: AI revolutionizes small business analytics! 10x revenue growth proven. What's your take? #AI #Business #StartupSuccess"),
        ("Medium viral potential", "Small business tip: Track your profit margins daily. Data shows 15% improvement! #SmallBusiness #Analytics"),
        ("Low viral potential", "We updated our website today."),
        ("Question-based", "What's the biggest challenge you face as a restaurant owner? Let's discuss solutions! #RestaurantOwners")
    ]
    
    for name, tweet in test_cases:
        print(f"\n📝 {name}:")
        print(f"   Content: {tweet[:60]}...")
        
        score = predictor.predict_viral_potential(tweet)
        print(f"   Viral Score: {score.total_score}/100")
        print(f"   Predicted Likes: {score.predicted_engagement['likes']}")
        print(f"   Predicted Retweets: {score.predicted_engagement['retweets']}")
        print(f"   Confidence: {score.confidence}%")
        
        if score.recommendations:
            print(f"   Top Recommendation: {score.recommendations[0]}")
    
    print("\n✅ Viral prediction demo completed!")

def demo_tweet_optimization():
    """Demonstrate tweet optimization"""
    print("\n🔧 Tweet Optimization Demo")
    print("-" * 40)
    
    from viral_predictor import ViralTweetPredictor
    
    predictor = ViralTweetPredictor()
    
    # Test optimization
    original_tweet = "We help restaurants with data analytics"
    print(f"📝 Original: {original_tweet}")
    
    original_score = predictor.predict_viral_potential(original_tweet)
    print(f"   Score: {original_score.total_score}/100")
    
    optimized_tweet, optimized_score = predictor.optimize_tweet(original_tweet)
    print(f"\n✨ Optimized: {optimized_tweet}")
    print(f"   Score: {optimized_score.total_score}/100")
    print(f"   Improvement: +{optimized_score.total_score - original_score.total_score:.1f} points")
    
    print("\n✅ Tweet optimization demo completed!")

def demo_viral_variations():
    """Demonstrate viral variations generation"""
    print("\n🚀 Viral Variations Demo")  
    print("-" * 40)
    
    from viral_predictor import ViralTweetPredictor
    
    predictor = ViralTweetPredictor()
    
    base_content = "SME Analytica helps restaurants increase revenue with analytics"
    print(f"📝 Base content: {base_content}")
    
    variations = predictor.generate_viral_variations(base_content, count=3)
    
    print(f"\n🎯 Generated {len(variations)} viral variations:")
    for i, (tweet, score) in enumerate(variations, 1):
        print(f"\nVariation {i} (Score: {score.total_score}/100):")
        print(f"   {tweet[:80]}..." if len(tweet) > 80 else f"   {tweet}")
        print(f"   Predicted: {score.predicted_engagement['likes']} likes, {score.predicted_engagement['retweets']} RTs")
    
    print("\n✅ Viral variations demo completed!")

def demo_bot_integration():
    """Demonstrate bot integration testing"""
    print("\n🤖 Bot Integration Demo")
    print("-" * 40)
    
    # Set up test environment
    test_env = {
        'TWITTER_API_KEY': 'demo_key',
        'TWITTER_API_SECRET': 'demo_secret',
        'TWITTER_ACCESS_TOKEN': 'demo_token',
        'TWITTER_ACCESS_TOKEN_SECRET': 'demo_secret',
        'TWITTER_BEARER_TOKEN': 'demo_bearer',
        'OPENAI_API_KEY': 'demo_openai'
    }
    
    original_env = dict(os.environ)
    os.environ.update(test_env)
    
    try:
        from bot import SMESocialBot
        
        # Initialize bot in test mode
        print("🔧 Initializing bot in test mode...")
        bot = SMESocialBot(test_mode=True)
        
        print("✅ Bot initialized successfully!")
        print(f"   AI Provider: {bot.ai_provider}")
        print(f"   Test Mode: {bot.test_mode}")
        print(f"   Viral Predictor: {'✅' if bot.viral_predictor else '❌'}")
        
        # Test viral prediction integration
        print("\n🎯 Testing viral prediction integration...")
        test_content = "Restaurant owners: Dynamic pricing boosts profits by 15%! #RestaurantTech"
        score = bot.viral_predictor.predict_viral_potential(test_content)
        print(f"   Content: {test_content}")
        print(f"   Viral Score: {score.total_score}/100")
        
        # Test session stats
        print(f"\n📊 Session stats initialized:")
        for key, value in bot.session_stats.items():
            print(f"   {key}: {value}")
        
        print("\n✅ Bot integration demo completed!")
        
    finally:
        # Restore original environment
        os.environ.clear()
        os.environ.update(original_env)

def run_sample_unit_tests():
    """Run a few sample unit tests"""
    print("\n🧪 Sample Unit Tests Demo")
    print("-" * 40)
    
    import unittest
    from test_viral_prediction import TestViralPrediction
    
    # Create a test suite with specific tests
    suite = unittest.TestSuite()
    suite.addTest(TestViralPrediction('test_viral_score_calculation'))
    suite.addTest(TestViralPrediction('test_tweet_optimization'))
    suite.addTest(TestViralPrediction('test_hashtag_analysis'))
    
    # Run the tests
    print("Running sample unit tests...")
    runner = unittest.TextTestRunner(verbosity=1, stream=sys.stdout)
    result = runner.run(suite)
    
    print(f"\n📊 Test Results:")
    print(f"   Tests run: {result.testsRun}")
    print(f"   Failures: {len(result.failures)}")
    print(f"   Errors: {len(result.errors)}")
    print(f"   Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.wasSuccessful():
        print("✅ All sample tests passed!")
    else:
        print("❌ Some tests failed!")
        
    return result.wasSuccessful()

def main():
    """Run the complete demo"""
    print("🎭 SME Social Media Bot - Testing Suite Demo")
    print("=" * 60)
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    start_time = time.time()
    
    try:
        # Run demos
        demo_viral_prediction_tests()
        demo_tweet_optimization()
        demo_viral_variations()
        demo_bot_integration()
        success = run_sample_unit_tests()
        
        duration = time.time() - start_time
        
        print("\n" + "=" * 60)
        print("📊 DEMO SUMMARY")
        print("=" * 60)
        print(f"⏱️  Total Duration: {duration:.2f} seconds")
        print(f"🎯 Components Tested:")
        print("   ✅ Viral Prediction System")
        print("   ✅ Tweet Optimization")
        print("   ✅ Viral Variations Generation")
        print("   ✅ Bot Integration")
        print("   ✅ Sample Unit Tests")
        
        if success:
            print("\n🎉 Demo completed successfully!")
            print("🚀 The SME Social Media Bot testing suite is fully functional!")
        else:
            print("\n⚠️  Demo completed with some test failures.")
            print("🔧 Review the test output above for details.")
            
        print("\n📋 Next Steps:")
        print("   • Run full test suite: python run_all_tests.py")
        print("   • Run specific tests: python test_viral_prediction.py")
        print("   • Run E2E tests: python test_e2e_playwright.py")
        print("   • View documentation: cat TESTING.md")
        
    except Exception as e:
        print(f"\n💥 Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()