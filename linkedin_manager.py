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

    def __init__(self, access_token: str, organization_id: Optional[str] = None, industry: str = 'general'):
        """
        Initialize LinkedIn manager

        Args:
            access_token: LinkedIn API access token
            organization_id: Optional organization ID for company page posting
            industry: Target industry for content adaptation
        """
        self.access_token = access_token
        self.organization_id = organization_id
        self.industry = industry
        self.viral_predictor = ViralTweetPredictor(industry=industry)

        # LinkedIn API endpoints
        self.base_url = "https://api.linkedin.com/v2"
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }

        # Industry-specific hashtag expansions
        self._load_industry_hashtags()

        # Get user info
        self.user_info = self._get_user_info()

    def _load_industry_hashtags(self):
        """Load industry-specific hashtag expansions for LinkedIn"""
        self.industry_hashtag_expansions = {
            'restaurant': {
                '#AI': '#ArtificialIntelligence #AI #FoodTech',
                '#RestaurantTech': '#RestaurantTechnology #HospitalityTech #FoodService',
                '#MenuFlow': '#MenuFlow #RestaurantAnalytics #DynamicPricing',
                '#FoodTech': '#FoodTech #RestaurantInnovation #HospitalityIndustry',
                '#DataDriven': '#DataDriven #RestaurantData #BusinessIntelligence',
            },
            'real_estate': {
                '#AI': '#ArtificialIntelligence #AI #PropTech',
                '#RealEstate': '#RealEstate #PropertyMarket #RealEstateIndustry',
                '#PropTech': '#PropTech #RealEstateTechnology #PropertyTech',
                '#RealEstateAgent': '#RealEstateAgent #Realtor #RealEstateProfessional',
                '#DataDriven': '#DataDriven #RealEstateData #MarketAnalytics',
            },
            'compliance': {
                '#AI': '#ArtificialIntelligence #AI #RegTech',
                '#Compliance': '#Compliance #RegulatoryCompliance #GRC',
                '#RegTech': '#RegTech #RegulatoryTechnology #ComplianceAutomation',
                '#RiskManagement': '#RiskManagement #EnterpriseRisk #GRC',
                '#DataDriven': '#DataDriven #ComplianceData #RiskAnalytics',
            },
            'conversa': {
                '#AI': '#ArtificialIntelligence #AI #ConversationalAI',
                '#Chatbot': '#Chatbot #ConversationalAI #CustomerEngagement',
                '#CX': '#CustomerExperience #CX #CustomerSuccess',
                '#CustomerService': '#CustomerService #CustomerSupport #ServiceExcellence',
                '#DataDriven': '#DataDriven #CustomerData #EngagementAnalytics',
            },
            'general': {
                '#AI': '#ArtificialIntelligence #AI #BusinessTech',
                '#SME': '#SmallMediumEnterprise #SME #SmallBusiness',
                '#BusinessTips': '#BusinessStrategy #EntrepreneurTips #Leadership',
                '#DataAnalytics': '#DataAnalytics #BusinessIntelligence #Analytics',
                '#Growth': '#BusinessGrowth #ScaleUp #StartupGrowth',
                '#Productivity': '#BusinessProductivity #Efficiency #Performance',
            }
        }

        # Industry-specific professional hashtags for LinkedIn
        self.industry_professional_tags = {
            'restaurant': ['#Business', '#Hospitality', '#FoodService', '#RestaurantManagement'],
            'real_estate': ['#Business', '#RealEstateIndustry', '#PropertyInvestment', '#MarketTrends'],
            'compliance': ['#Business', '#Governance', '#RiskManagement', '#RegulatoryAffairs'],
            'conversa': ['#Business', '#CustomerSuccess', '#DigitalTransformation', '#Innovation'],
            'general': ['#Business', '#Leadership', '#Strategy', '#Growth', '#Innovation'],
        }
        
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
        - Expand hashtags using industry-specific expansions
        - Adjust tone to be more professional
        - Optimize length (LinkedIn allows longer posts)
        """
        linkedin_content = twitter_content

        # Get industry-specific hashtag expansions
        hashtag_expansions = self.industry_hashtag_expansions.get(
            self.industry,
            self.industry_hashtag_expansions['general']
        )

        for short, expanded in hashtag_expansions.items():
            linkedin_content = linkedin_content.replace(short, expanded)

        # Industry-specific professional context additions
        context_additions = {
            'restaurant': "\n\nHow are you leveraging data in your restaurant business? Share your experiences below.",
            'real_estate': "\n\nHow are you using data to stay competitive in today's market? I'd love to hear your approach.",
            'compliance': "\n\nHow is your organization handling compliance automation? Share your insights below.",
            'conversa': "\n\nHow are you improving customer conversations? Share your strategies below.",
            'general': "\n\nHow are you leveraging data in your business? Share your experiences in the comments below."
        }

        # Add professional context if too short
        if len(linkedin_content) < 100:
            linkedin_content += context_additions.get(self.industry, context_additions['general'])

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

                    # Ensure industry-specific professional hashtags
                    professional_tags = self.industry_professional_tags.get(
                        self.industry,
                        self.industry_professional_tags['general']
                    )
                    for tag in professional_tags[:2]:
                        if tag not in linkedin_content:
                            linkedin_content += f" {tag}"
                            break

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

        # Industry-specific LinkedIn templates
        industry_templates = {
            'restaurant': [
                "🍽️ Restaurant insight: {content}\n\nWhat's working in your kitchen?",
                "📊 From the data: {content}\n\nHow are you optimizing your operations?",
                "🚀 Hospitality innovation: {content}\n\nShare your success stories!",
            ],
            'real_estate': [
                "🏠 Market insight: {content}\n\nWhat trends are you seeing in your market?",
                "📊 From the data: {content}\n\nHow are you staying ahead of the competition?",
                "🚀 PropTech innovation: {content}\n\nShare your strategies!",
            ],
            'compliance': [
                "⚖️ Compliance insight: {content}\n\nHow is your organization adapting?",
                "📊 Risk perspective: {content}\n\nWhat's your approach to automation?",
                "🔒 Regulatory update: {content}\n\nShare your implementation stories!",
            ],
            'conversa': [
                "💬 CX insight: {content}\n\nHow are you improving conversations?",
                "📊 Engagement data: {content}\n\nWhat's driving your customer success?",
                "🤖 AI innovation: {content}\n\nShare your automation wins!",
            ],
            'general': [
                "💼 Professional insight: {content}\n\nWhat strategies have worked for you?",
                "🎯 Business tip: {content}\n\nShare your experiences below!",
                "📈 Data-driven approach: {content}\n\nHow do you measure success?",
            ]
        }

        templates = industry_templates.get(self.industry, industry_templates['general'])
        professional_tags = self.industry_professional_tags.get(
            self.industry,
            self.industry_professional_tags['general']
        )

        variations = []

        for template in templates:
            # Create LinkedIn variation
            linkedin_content = template.format(content=base_content)

            # Add industry-specific professional hashtags
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