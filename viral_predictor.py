#!/usr/bin/env python3
"""
Viral Tweet Prediction System for SME Social Media Manager
Predicts viral potential of tweets and suggests optimizations
"""

import re
import json
import datetime
import hashlib
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
import random

@dataclass
class ViralScore:
    """Represents the viral potential score of a tweet"""
    total_score: float
    content_score: float
    timing_score: float
    hashtag_score: float
    engagement_score: float
    trend_score: float
    recommendations: List[str]
    predicted_engagement: Dict[str, int]
    confidence: float

class ViralTweetPredictor:
    """Predicts viral potential of tweets and suggests improvements"""
    
    def __init__(self):
        # Viral tweet characteristics based on research
        self.viral_patterns = {
            'emotional_triggers': [
                'amazing', 'incredible', 'shocking', 'unbelievable', 'breaking',
                'exclusive', 'urgent', 'wow', 'mind-blowing', 'game-changer',
                'revolutionary', 'transform', 'secret', 'revealed', 'discover'
            ],
            'power_words': [
                'you', 'your', 'free', 'new', 'now', 'today', 'instantly',
                'proven', 'guaranteed', 'easy', 'simple', 'quick', 'best',
                'ultimate', 'essential', 'must-have', 'expert', 'professional'
            ],
            'call_to_actions': [
                'retweet', 'share', 'follow', 'click', 'learn', 'discover',
                'join', 'get', 'try', 'check out', 'don\'t miss', 'save',
                'bookmark', 'tag', 'comment', 'thoughts?', 'agree?'
            ],
            'trending_topics': [
                'AI', 'ChatGPT', 'automation', 'productivity', 'growth',
                'success', 'entrepreneur', 'startup', 'business', 'marketing',
                'sales', 'revenue', 'ROI', 'data', 'analytics', 'insights'
            ]
        }
        
        # Optimal posting times (UTC) based on engagement data
        self.optimal_times = {
            'weekday': [8, 12, 17, 20],  # 8am, 12pm, 5pm, 8pm
            'weekend': [10, 14, 19]       # 10am, 2pm, 7pm
        }
        
        # Hashtag effectiveness scores
        self.hashtag_tiers = {
            'tier1': ['business', 'entrepreneur', 'startup', 'AI', 'tech'],
            'tier2': ['growth', 'marketing', 'sales', 'productivity', 'success'],
            'tier3': ['SME', 'smallbusiness', 'innovation', 'digital', 'data']
        }
    
    def predict_viral_potential(self, tweet: str, 
                               posting_time: Optional[datetime.datetime] = None,
                               historical_data: Optional[Dict] = None) -> ViralScore:
        """
        Predict the viral potential of a tweet
        
        Args:
            tweet: The tweet content
            posting_time: When the tweet will be posted
            historical_data: Past performance data
            
        Returns:
            ViralScore with predictions and recommendations
        """
        if not posting_time:
            posting_time = datetime.datetime.now(datetime.timezone.utc)
        
        # Calculate individual scores
        content_score = self._analyze_content(tweet)
        timing_score = self._analyze_timing(posting_time)
        hashtag_score = self._analyze_hashtags(tweet)
        engagement_score = self._predict_engagement_potential(tweet)
        trend_score = self._analyze_trend_alignment(tweet)
        
        # Calculate weighted total score
        total_score = (
            content_score * 0.3 +
            timing_score * 0.15 +
            hashtag_score * 0.15 +
            engagement_score * 0.25 +
            trend_score * 0.15
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            tweet, content_score, hashtag_score, timing_score
        )
        
        # Predict engagement metrics
        predicted_engagement = self._predict_engagement_metrics(total_score)
        
        # Calculate confidence level
        confidence = self._calculate_confidence(tweet, historical_data)
        
        return ViralScore(
            total_score=round(total_score, 2),
            content_score=round(content_score, 2),
            timing_score=round(timing_score, 2),
            hashtag_score=round(hashtag_score, 2),
            engagement_score=round(engagement_score, 2),
            trend_score=round(trend_score, 2),
            recommendations=recommendations,
            predicted_engagement=predicted_engagement,
            confidence=round(confidence, 2)
        )
    
    def _analyze_content(self, tweet: str) -> float:
        """Analyze tweet content for viral characteristics"""
        score = 50.0  # Base score
        tweet_lower = tweet.lower()
        
        # Check for emotional triggers (+15 points max)
        emotional_count = sum(1 for word in self.viral_patterns['emotional_triggers'] 
                            if word in tweet_lower)
        score += min(emotional_count * 5, 15)
        
        # Check for power words (+15 points max)
        power_count = sum(1 for word in self.viral_patterns['power_words'] 
                        if word in tweet_lower)
        score += min(power_count * 3, 15)
        
        # Check for call to action (+10 points)
        has_cta = any(cta in tweet_lower for cta in self.viral_patterns['call_to_actions'])
        if has_cta:
            score += 10
        
        # Length optimization (140-200 chars is optimal)
        length = len(tweet)
        if 140 <= length <= 200:
            score += 10
        elif 100 <= length < 140 or 200 < length <= 240:
            score += 5
        
        # Question marks increase engagement (+5 points)
        if '?' in tweet:
            score += 5
        
        # Numbers/statistics increase credibility (+5 points)
        if any(char.isdigit() for char in tweet):
            score += 5
        
        # Emojis increase engagement (+5 points, max 3)
        emoji_count = len(re.findall(r'[😀-🙏🌀-🗿🚀-🛿☀-⛿✀-➿]', tweet))
        if 1 <= emoji_count <= 3:
            score += 5
        
        return min(score, 100)
    
    def _analyze_timing(self, posting_time: datetime.datetime) -> float:
        """Analyze posting time for optimal engagement"""
        score = 40.0  # Base score
        
        hour = posting_time.hour
        weekday = posting_time.weekday()
        
        # Check if weekend or weekday
        if weekday < 5:  # Weekday
            optimal_hours = self.optimal_times['weekday']
        else:  # Weekend
            optimal_hours = self.optimal_times['weekend']
        
        # Calculate proximity to optimal times
        min_distance = min(abs(hour - oh) for oh in optimal_hours)
        
        if min_distance == 0:
            score += 60  # Perfect timing
        elif min_distance == 1:
            score += 40  # Close to optimal
        elif min_distance == 2:
            score += 20  # Acceptable
        else:
            score += 0   # Suboptimal
        
        # Weekday bonus (Tuesday-Thursday are best)
        if 1 <= weekday <= 3:
            score += 10
        
        return min(score, 100)
    
    def _analyze_hashtags(self, tweet: str) -> float:
        """Analyze hashtag effectiveness"""
        score = 30.0  # Base score
        
        hashtags = re.findall(r'#\w+', tweet.lower())
        hashtag_count = len(hashtags)
        
        # Optimal hashtag count is 2-4
        if 2 <= hashtag_count <= 4:
            score += 20
        elif hashtag_count == 1 or hashtag_count == 5:
            score += 10
        elif hashtag_count > 5:
            score -= 10  # Too many hashtags
        
        # Check hashtag quality
        for hashtag in hashtags:
            tag = hashtag[1:]  # Remove #
            if any(t in tag for t in self.hashtag_tiers['tier1']):
                score += 15
            elif any(t in tag for t in self.hashtag_tiers['tier2']):
                score += 10
            elif any(t in tag for t in self.hashtag_tiers['tier3']):
                score += 5
        
        # Trending hashtag bonus
        if any('#trending' in h.lower() or '#viral' in h.lower() for h in hashtags):
            score += 10
        
        return min(score, 100)
    
    def _predict_engagement_potential(self, tweet: str) -> float:
        """Predict engagement potential based on content type"""
        score = 50.0  # Base score
        tweet_lower = tweet.lower()
        
        # Questions drive engagement
        if '?' in tweet:
            score += 15
        
        # Lists and tips perform well
        if any(marker in tweet for marker in ['1.', '•', '→', '✓']):
            score += 10
        
        # Quotes and insights
        if '"' in tweet or '"' in tweet:
            score += 10
        
        # Personal stories
        if any(word in tweet_lower for word in ['i ', 'my ', 'me ', "i've", "i'm"]):
            score += 5
        
        # Controversial or debate-worthy
        if any(word in tweet_lower for word in ['unpopular opinion', 'hot take', 'debate', 'controversial']):
            score += 15
        
        # Educational content
        if any(word in tweet_lower for word in ['how to', 'guide', 'tips', 'learn', 'tutorial']):
            score += 10
        
        return min(score, 100)
    
    def _analyze_trend_alignment(self, tweet: str) -> float:
        """Check alignment with current trends"""
        score = 40.0  # Base score
        tweet_lower = tweet.lower()
        
        # Check for trending topics
        trend_matches = sum(1 for topic in self.viral_patterns['trending_topics']
                          if topic.lower() in tweet_lower)
        score += min(trend_matches * 15, 60)
        
        return min(score, 100)
    
    def _generate_recommendations(self, tweet: str, content_score: float,
                                 hashtag_score: float, timing_score: float) -> List[str]:
        """Generate specific recommendations to improve viral potential"""
        recommendations = []
        
        # Content recommendations
        if content_score < 70:
            if not any(word in tweet.lower() for word in self.viral_patterns['emotional_triggers']):
                recommendations.append("Add emotional triggers (e.g., 'amazing', 'incredible')")
            if not any(cta in tweet.lower() for cta in self.viral_patterns['call_to_actions']):
                recommendations.append("Include a call-to-action (e.g., 'What do you think?')")
            if len(tweet) > 240:
                recommendations.append("Shorten tweet to 140-200 characters for optimal engagement")
        
        # Hashtag recommendations
        if hashtag_score < 70:
            hashtag_count = len(re.findall(r'#\w+', tweet))
            if hashtag_count < 2:
                recommendations.append("Add 2-4 relevant hashtags")
            elif hashtag_count > 4:
                recommendations.append("Reduce to 2-4 hashtags for better reach")
        
        # Timing recommendations
        if timing_score < 70:
            recommendations.append("Post during peak hours: 8am, 12pm, 5pm, or 8pm")
        
        # Engagement recommendations
        if '?' not in tweet:
            recommendations.append("Add a question to encourage responses")
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def _predict_engagement_metrics(self, total_score: float) -> Dict[str, int]:
        """Predict specific engagement metrics based on score"""
        base_metrics = {
            'likes': 5,
            'retweets': 2,
            'replies': 1,
            'impressions': 100
        }
        
        # Apply multiplier based on score
        multiplier = (total_score / 50) ** 1.5  # Exponential growth for viral content
        
        return {
            'likes': int(base_metrics['likes'] * multiplier * random.uniform(0.8, 1.2)),
            'retweets': int(base_metrics['retweets'] * multiplier * random.uniform(0.7, 1.3)),
            'replies': int(base_metrics['replies'] * multiplier * random.uniform(0.6, 1.4)),
            'impressions': int(base_metrics['impressions'] * multiplier * random.uniform(0.9, 1.1))
        }
    
    def _calculate_confidence(self, tweet: str, historical_data: Optional[Dict]) -> float:
        """Calculate confidence level in prediction"""
        confidence = 70.0  # Base confidence
        
        # More data points increase confidence
        if historical_data and 'tweet_count' in historical_data:
            if historical_data['tweet_count'] > 100:
                confidence += 15
            elif historical_data['tweet_count'] > 50:
                confidence += 10
        
        # Well-structured tweets increase confidence
        if len(tweet) > 50 and any(char in tweet for char in ['.', '!', '?']):
            confidence += 10
        
        # Hashtags present
        if '#' in tweet:
            confidence += 5
        
        return min(confidence, 95)
    
    def optimize_tweet(self, original_tweet: str) -> Tuple[str, ViralScore]:
        """
        Automatically optimize a tweet for viral potential
        
        Args:
            original_tweet: The original tweet content
            
        Returns:
            Tuple of optimized tweet and its viral score
        """
        optimized = original_tweet
        
        # Add trending hashtags if missing
        hashtags = re.findall(r'#\w+', optimized)
        if len(hashtags) < 2:
            trending_tags = random.sample(self.hashtag_tiers['tier1'], 2 - len(hashtags))
            optimized += ' ' + ' '.join(f'#{tag}' for tag in trending_tags)
        
        # Add call-to-action if missing
        if not any(cta in optimized.lower() for cta in self.viral_patterns['call_to_actions']):
            if '?' not in optimized:
                optimized += '\n\nWhat are your thoughts?'
        
        # Add emoji if missing (but not too many)
        emoji_count = len(re.findall(r'[😀-🙏🌀-🗿🚀-🛿☀-⛿✀-➿]', optimized))
        if emoji_count == 0:
            optimized = '🚀 ' + optimized
        
        # Ensure within character limit
        if len(optimized) > 280:
            optimized = optimized[:277] + '...'
        
        # Get score for optimized version
        score = self.predict_viral_potential(optimized)
        
        return optimized, score
    
    def generate_viral_variations(self, base_content: str, count: int = 3) -> List[Tuple[str, ViralScore]]:
        """
        Generate multiple viral variations of content
        
        Args:
            base_content: The base content idea
            count: Number of variations to generate
            
        Returns:
            List of tweet variations with their scores
        """
        variations = []
        
        # Templates for viral tweets
        templates = [
            "🚀 {content}\n\nAgree? Let me know below! 👇",
            "Unpopular opinion: {content}\n\nWhat's your take?",
            "💡 Quick tip: {content}\n\nSave this for later!",
            "Breaking: {content}\n\nRT to spread awareness!",
            "{content}\n\nThread below 🧵",
            "The truth about {content} that nobody talks about:",
            "Stop scrolling! {content}\n\nThis changes everything.",
            "I tested {content} for 30 days. Results? Mind-blowing.",
            "{content}\n\n❤️ if you agree\n🔄 to share with others"
        ]
        
        # Generate variations
        used_templates = random.sample(templates, min(count, len(templates)))
        
        for template in used_templates:
            # Create variation
            if '{content}' in template:
                tweet = template.format(content=base_content)
            else:
                tweet = f"{template} {base_content}"
            
            # Add trending hashtags
            trending_tags = random.sample(
                self.hashtag_tiers['tier1'] + self.hashtag_tiers['tier2'], 
                random.randint(2, 3)
            )
            tweet += ' ' + ' '.join(f'#{tag}' for tag in trending_tags)
            
            # Ensure within limit
            if len(tweet) > 280:
                tweet = tweet[:277] + '...'
            
            # Calculate score
            score = self.predict_viral_potential(tweet)
            variations.append((tweet, score))
        
        # Sort by score
        variations.sort(key=lambda x: x[1].total_score, reverse=True)
        
        return variations

# Example usage and testing
if __name__ == "__main__":
    predictor = ViralTweetPredictor()
    
    # Test tweets
    test_tweets = [
        "Just launched our new analytics dashboard for SMEs!",
        "🚀 Game-changer: AI-powered analytics that boost revenue by 47% on average. Who's ready to transform their business? #AI #Business #Growth",
        "New blog post about data analytics",
        "Unpopular opinion: Most businesses waste 80% of their data. Here's how to fix it: 🧵"
    ]
    
    print("=" * 60)
    print("VIRAL TWEET PREDICTION SYSTEM - TEST RESULTS")
    print("=" * 60)
    
    for tweet in test_tweets:
        print(f"\nTweet: {tweet[:50]}...")
        score = predictor.predict_viral_potential(tweet)
        print(f"Viral Score: {score.total_score}/100")
        print(f"Predicted Likes: {score.predicted_engagement['likes']}")
        print(f"Predicted Retweets: {score.predicted_engagement['retweets']}")
        print(f"Confidence: {score.confidence}%")
        
        if score.recommendations:
            print("Recommendations:")
            for rec in score.recommendations:
                print(f"  - {rec}")
    
    print("\n" + "=" * 60)
    print("GENERATING VIRAL VARIATIONS")
    print("=" * 60)
    
    base_content = "SME Analytica helps restaurants increase revenue with data insights"
    variations = predictor.generate_viral_variations(base_content, count=3)
    
    for i, (tweet, score) in enumerate(variations, 1):
        print(f"\nVariation {i} (Score: {score.total_score}/100):")
        print(tweet)
        print(f"Predicted engagement: {score.predicted_engagement['likes']} likes, "
              f"{score.predicted_engagement['retweets']} RTs")