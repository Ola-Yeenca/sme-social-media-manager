#!/usr/bin/env python3
"""
LinkedIn Manager for SME Social Media Bot
Handles LinkedIn posting with viral prediction integration
"""

import os
import json
import time
import requests
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from viral_predictor import ViralTweetPredictor, ViralScore

class LinkedInManager:
    """Manages LinkedIn posting with viral prediction"""
    
    def __init__(self, access_token: str, organization_id: Optional[str] = None):
        """
        Initialize LinkedIn manager
        
        Args:
            access_token: LinkedIn API access token
            organization_id: Optional organization ID for company page posting
        """
        self.access_token = access_token
        self.organization_id = organization_id
        self.viral_predictor = ViralTweetPredictor()
        
        # LinkedIn API endpoints
        self.base_url = "https://api.linkedin.com/v2"
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }
        
        # Get user info
        self.user_info = self._get_user_info()
        
    def _get_user_info(self) -> Dict:
        """Get current user information"""
        try:
            response = requests.get(
                f"{self.base_url}/me",
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"⚠️ LinkedIn user info failed: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"⚠️ LinkedIn user info error: {e}")
            return {}
    
    def adapt_content_for_linkedin(self, twitter_content: str) -> str:
        """
        Adapt Twitter content for LinkedIn
        - Expand hashtags to full words where appropriate
        - Adjust tone to be more professional
        - Optimize length (LinkedIn allows longer posts)
        """
        linkedin_content = twitter_content
        
        # Expand common hashtags for LinkedIn
        hashtag_expansions = {
            '#AI': '#ArtificialIntelligence #AI',
            '#SME': '#SmallMediumEnterprise #SME #SmallBusiness',
            '#RestaurantTech': '#RestaurantTechnology #HospitalityTech',
            '#BusinessTips': '#BusinessStrategy #EntrepreneurTips',
            '#DataAnalytics': '#DataAnalytics #BusinessIntelligence',
            '#Growth': '#BusinessGrowth #ScaleUp',
            '#Productivity': '#BusinessProductivity #Efficiency'
        }
        
        for short, expanded in hashtag_expansions.items():
            linkedin_content = linkedin_content.replace(short, expanded)
        
        # Add professional context if too short
        if len(linkedin_content) < 100:
            linkedin_content += "\n\nHow are you leveraging data in your business? Share your experiences in the comments below."
        
        # Add call to action for LinkedIn engagement
        if not any(phrase in linkedin_content.lower() for phrase in ['comment', 'share', 'thoughts', 'experience']):
            linkedin_content += "\n\n💭 What are your thoughts on this? Let's discuss in the comments."
        
        return linkedin_content
    
    def predict_linkedin_performance(self, content: str) -> ViralScore:
        """
        Predict LinkedIn post performance
        LinkedIn has different engagement patterns than Twitter
        """
        # Get base prediction
        score = self.viral_predictor.predict_viral_potential(content)
        
        # Adjust for LinkedIn characteristics
        linkedin_content = content.lower()
        
        # LinkedIn-specific boosts
        if 'business' in linkedin_content or 'professional' in linkedin_content:
            score.content_score = min(score.content_score + 5, 100)
        
        if 'experience' in linkedin_content or 'insight' in linkedin_content:
            score.engagement_score = min(score.engagement_score + 10, 100)
        
        if len(content) > 200:  # LinkedIn appreciates longer, thoughtful content
            score.content_score = min(score.content_score + 5, 100)
        
        # LinkedIn has different optimal posting times (business hours)
        current_hour = datetime.now().hour
        if 8 <= current_hour <= 17:  # Business hours
            score.timing_score = min(score.timing_score + 15, 100)
        
        # Recalculate total score
        score.total_score = (
            score.content_score * 0.3 +
            score.timing_score * 0.15 +
            score.hashtag_score * 0.15 +
            score.engagement_score * 0.25 +
            score.trend_score * 0.15
        )
        
        # Adjust engagement predictions for LinkedIn
        linkedin_multiplier = 0.7  # LinkedIn typically has lower engagement numbers
        score.predicted_engagement = {
            'reactions': int(score.predicted_engagement['likes'] * linkedin_multiplier),
            'comments': int(score.predicted_engagement['replies'] * 1.2),  # More comments on LinkedIn
            'shares': int(score.predicted_engagement['retweets'] * 0.5),
            'views': int(score.predicted_engagement['impressions'] * 2.0)  # Higher reach on LinkedIn
        }
        
        return score
    
    def post_to_linkedin(self, content: str, optimize_viral: bool = True) -> Tuple[bool, Dict]:
        """
        Post content to LinkedIn with optional viral optimization
        
        Args:
            content: Content to post
            optimize_viral: Whether to optimize for viral potential
            
        Returns:
            Tuple of (success, response_data)
        """
        try:
            # Adapt content for LinkedIn
            linkedin_content = self.adapt_content_for_linkedin(content)
            
            # Predict and optimize if requested
            if optimize_viral:
                print("\n📊 LinkedIn Viral Prediction:")
                viral_score = self.predict_linkedin_performance(linkedin_content)
                print(f"   Score: {viral_score.total_score}/100")
                print(f"   Predicted: {viral_score.predicted_engagement['reactions']} reactions, {viral_score.predicted_engagement['comments']} comments")
                
                # Optimize if score is below threshold
                if viral_score.total_score < 70:
                    print("🔧 Optimizing content for LinkedIn...")
                    # Add professional call-to-action
                    if '?' not in linkedin_content:
                        linkedin_content += "\n\nWhat's your experience with this? I'd love to hear your thoughts."
                    
                    # Ensure professional hashtags
                    if '#Business' not in linkedin_content:
                        linkedin_content += " #Business #Leadership"
                    
                    # Re-predict
                    viral_score = self.predict_linkedin_performance(linkedin_content)
                    print(f"   Improved Score: {viral_score.total_score}/100")
            
            # Prepare post data
            if self.organization_id:
                # Post as organization
                author = f"urn:li:organization:{self.organization_id}"
            else:
                # Post as individual
                person_id = self.user_info.get('id', 'unknown')
                author = f"urn:li:person:{person_id}"
            
            post_data = {
                "author": author,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": linkedin_content
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            # Make the post
            response = requests.post(
                f"{self.base_url}/ugcPosts",
                headers=self.headers,
                json=post_data,
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                response_data = response.json()
                post_id = response_data.get('id', 'unknown')
                
                print(f"✅ LinkedIn post successful!")
                print(f"   Content: {linkedin_content[:100]}...")
                print(f"   Post ID: {post_id}")
                
                if optimize_viral:
                    print(f"   Viral Score: {viral_score.total_score}/100")
                
                return True, response_data
            else:
                print(f"❌ LinkedIn post failed: {response.status_code}")
                print(f"   Response: {response.text}")
                return False, {'error': response.text}
                
        except Exception as e:
            print(f"❌ LinkedIn posting error: {e}")
            return False, {'error': str(e)}
    
    def generate_linkedin_content_variations(self, base_content: str) -> List[Tuple[str, ViralScore]]:
        """Generate LinkedIn-optimized viral variations"""
        
        # LinkedIn-specific templates
        linkedin_templates = [
            "💼 Professional insight: {content}\n\nWhat strategies have worked for you?",
            "🎯 Business tip: {content}\n\nShare your experiences below!",
            "📈 Data-driven approach: {content}\n\nHow do you measure success in this area?",
            "🚀 Growth strategy: {content}\n\nWhat's your take on this approach?",
            "💡 From the field: {content}\n\nI'd love to hear your perspective.",
            "🔍 Industry insight: {content}\n\nWhat trends are you seeing?",
            "📊 Performance metric: {content}\n\nHow do you track similar metrics?",
            "⚡ Game changer: {content}\n\nWhat innovations are driving your business?"
        ]
        
        variations = []
        
        for template in linkedin_templates[:3]:  # Generate 3 variations
            # Create LinkedIn variation
            linkedin_content = template.format(content=base_content)
            
            # Add professional hashtags
            professional_tags = ['#Business', '#Leadership', '#Strategy', '#Growth', '#Innovation']
            linkedin_content += ' ' + ' '.join(professional_tags[:2])
            
            # Predict performance
            score = self.predict_linkedin_performance(linkedin_content)
            variations.append((linkedin_content, score))
        
        # Sort by score
        variations.sort(key=lambda x: x[1].total_score, reverse=True)
        
        return variations
    
    def test_connection(self) -> bool:
        """Test LinkedIn API connection"""
        try:
            response = requests.get(
                f"{self.base_url}/me",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                user_data = response.json()
                name = f"{user_data.get('firstName', {}).get('localized', {}).get('en_US', 'Unknown')} {user_data.get('lastName', {}).get('localized', {}).get('en_US', '')}"
                print(f"✅ LinkedIn connection successful!")
                print(f"   Connected as: {name}")
                return True
            else:
                print(f"❌ LinkedIn connection failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ LinkedIn connection error: {e}")
            return False

def main():
    """Test LinkedIn integration"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    linkedin_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
    linkedin_org_id = os.getenv('LINKEDIN_ORGANIZATION_ID')
    
    if not linkedin_token:
        print("❌ LINKEDIN_ACCESS_TOKEN not found in environment")
        return
    
    print("🔗 Testing LinkedIn Integration...")
    linkedin = LinkedInManager(linkedin_token, linkedin_org_id)
    
    # Test connection
    if not linkedin.test_connection():
        return
    
    # Test content generation
    test_content = "SME Analytica helps restaurants increase revenue by 47% through data-driven pricing optimization."
    
    print(f"\n📝 Testing content: {test_content}")
    
    # Test viral prediction
    score = linkedin.predict_linkedin_performance(test_content)
    print(f"📊 LinkedIn Viral Score: {score.total_score}/100")
    
    # Test content adaptation
    adapted = linkedin.adapt_content_for_linkedin(test_content)
    print(f"🔧 Adapted content: {adapted[:100]}...")
    
    # Test variations
    print(f"\n🚀 Generating LinkedIn variations...")
    variations = linkedin.generate_linkedin_content_variations(test_content)
    
    for i, (content, score) in enumerate(variations, 1):
        print(f"\nVariation {i} (Score: {score.total_score}/100):")
        print(f"  {content[:120]}...")
    
    print(f"\n✅ LinkedIn integration test complete!")

if __name__ == "__main__":
    main()