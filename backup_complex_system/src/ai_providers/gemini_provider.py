"""
Google Gemini provider for advanced AI content generation and social media intelligence
"""

import google.generativeai as genai
import asyncio
import json
from typing import Dict, List, Any, Optional
from .base import BaseAIProvider, ContentRequest, GeneratedContent, APIError, RateLimitError

class GeminiProvider(BaseAIProvider):
    """Google Gemini provider for intelligent social media content and engagement"""
    
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-pro"):
        super().__init__(api_key, model_name)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        
        # Gemini-specific configuration for social media optimization
        self.generation_config = genai.types.GenerationConfig(
            temperature=0.7,
            top_p=0.8,
            top_k=40,
            max_output_tokens=300,
            candidate_count=1
        )
        
        # Safety settings for social media content
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
    
    @property
    def provider_name(self) -> str:
        return "Google Gemini"
    
    @property
    def is_available(self) -> bool:
        return bool(self.api_key and self.model)
    
    async def generate_content(self, request: ContentRequest) -> GeneratedContent:
        """Generate intelligent social media content using Gemini"""
        try:
            prompt = self._build_intelligent_prompt(request)
            
            # Use asyncio to run the synchronous Gemini API call
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            
            if not response.text:
                raise APIError("Gemini returned empty response")
            
            content_text = response.text.strip()
            hashtags = self._extract_hashtags(content_text, request.hashtags or [])
            
            return GeneratedContent(
                text=content_text,
                language=request.language,
                hashtags=hashtags,
                confidence_score=0.92,  # Gemini is excellent for intelligent content
                metadata={
                    "model": self.model_name,
                    "provider": self.provider_name,
                    "usage_metadata": getattr(response, 'usage_metadata', {}),
                    "safety_ratings": getattr(response, 'safety_ratings', [])
                }
            )
            
        except Exception as e:
            if "quota" in str(e).lower() or "rate" in str(e).lower():
                raise RateLimitError(f"Gemini rate limit exceeded: {e}")
            else:
                raise APIError(f"Gemini API error: {e}")
    
    async def analyze_engagement_opportunity(self, tweet_text: str, author: str) -> Dict[str, Any]:
        """Analyze engagement opportunity using Gemini's advanced reasoning"""
        try:
            prompt = f"""
            As an AI social media strategist for SME Analytica (restaurant analytics platform), analyze this engagement opportunity:
            
            Tweet: "{tweet_text}"
            Author: @{author}
            
            SME Analytica Context:
            - AI-driven analytics platform for restaurants, hotels, retail
            - MenuFlow dynamic pricing boosts margins ~10%
            - Real-time analytics, POS integration
            - 500+ restaurants served
            - Target: restaurant owners, small business, hospitality sector
            
            Provide detailed analysis in JSON format:
            {{
                "relevance_score": 0-10,
                "engagement_potential": 0-10,
                "conversion_likelihood": 0-10,
                "brand_alignment": 0-10,
                "urgency_level": 0-10,
                "recommended_action": "reply|like|retweet|quote_tweet|ignore",
                "response_strategy": "thought_leadership|community_support|prospect_conversion|brand_awareness",
                "key_talking_points": ["point1", "point2", "point3"],
                "potential_risks": ["risk1", "risk2"],
                "optimal_timing": "immediate|within_hour|within_day|not_urgent",
                "reasoning": "detailed explanation of analysis"
            }}
            
            Focus on authentic value-add opportunities that position SME Analytica as helpful industry experts.
            """
            
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,  # Lower temperature for analytical tasks
                    max_output_tokens=500
                ),
                safety_settings=self.safety_settings
            )
            
            # Parse JSON response
            try:
                analysis = json.loads(response.text.strip())
                return analysis
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return {
                    "relevance_score": 5,
                    "engagement_potential": 5,
                    "conversion_likelihood": 3,
                    "brand_alignment": 5,
                    "urgency_level": 5,
                    "recommended_action": "ignore",
                    "response_strategy": "brand_awareness",
                    "key_talking_points": ["general industry insight"],
                    "potential_risks": ["unclear context"],
                    "optimal_timing": "not_urgent",
                    "reasoning": "Failed to parse detailed analysis"
                }
            
        except Exception as e:
            raise APIError(f"Gemini engagement analysis error: {e}")
    
    async def generate_reply(self, original_tweet: str, context: Dict[str, Any]) -> str:
        """Generate intelligent, contextual reply using Gemini"""
        try:
            prompt = f"""
            As SME Analytica's AI social media manager, craft an intelligent reply to this tweet:
            
            Original Tweet: "{original_tweet}"
            Context: {json.dumps(context, indent=2)}
            
            SME Analytica Brand Voice:
            - Professional yet approachable
            - Data-driven expert and helpful mentor
            - Industry thought leader in restaurant analytics
            - Authentic, never pushy or overly promotional
            - Focuses on genuine value and insights
            
            Key Messaging:
            - 500+ restaurants trust our analytics platform
            - MenuFlow dynamic pricing boosts margins ~10%
            - Real-time analytics + POS integration
            - Making enterprise-level BI accessible to SMEs
            
            Reply Requirements:
            - Under 280 characters for Twitter
            - Provide genuine value and insights
            - Use specific data/statistics when relevant
            - Professional but conversational tone
            - Include strategic emoji usage (📊📈🚀💡🎯🤝)
            - Reference SME Analytica naturally, not forcefully
            - Be helpful first, promotional second
            
            Generate a reply that positions SME Analytica as a knowledgeable, helpful industry expert.
            """
            
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.6,
                    max_output_tokens=100
                ),
                safety_settings=self.safety_settings
            )
            
            return response.text.strip()
            
        except Exception as e:
            raise APIError(f"Gemini reply generation error: {e}")
    
    async def generate_influencer_content(self, request: ContentRequest) -> GeneratedContent:
        """Generate content specifically optimized for social media influence"""
        try:
            prompt = f"""
            As SME Analytica's AI content strategist, create influential social media content that positions us as thought leaders in restaurant analytics.
            
            Content Requirements:
            - Theme: {request.theme}
            - Language: {request.language}
            - Context: {json.dumps(request.context, indent=2)}
            - Max Length: {request.max_length} characters
            - Tone: {request.tone}
            
            SME Analytica Influence Strategy:
            - Establish authority through data-driven insights
            - Share specific, actionable business intelligence
            - Use compelling statistics and real results
            - Create content that restaurant owners want to share
            - Position as the go-to expert for restaurant optimization
            
            Content Types to Consider:
            - Industry insights with specific data points
            - "Did you know?" facts about restaurant analytics
            - Success stories with measurable results
            - Trend analysis with actionable takeaways
            - Behind-the-scenes analytics revelations
            
            Influence Amplifiers:
            - Start with attention-grabbing statistics
            - Use power words: "revealed", "discovered", "proven"
            - Include specific percentages and metrics
            - End with thought-provoking questions
            - Use strategic hashtags for discoverability
            
            Create content that restaurant owners will want to engage with, share, and remember.
            Make SME Analytica the authoritative voice they turn to for business insights.
            """
            
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.8,  # Higher creativity for influential content
                    max_output_tokens=250
                ),
                safety_settings=self.safety_settings
            )
            
            content_text = response.text.strip()
            hashtags = self._extract_hashtags(content_text, request.hashtags or [])
            
            return GeneratedContent(
                text=content_text,
                language=request.language,
                hashtags=hashtags,
                confidence_score=0.94,  # High confidence for influencer content
                metadata={
                    "model": self.model_name,
                    "provider": self.provider_name,
                    "content_type": "influencer_optimized",
                    "usage_metadata": getattr(response, 'usage_metadata', {})
                }
            )
            
        except Exception as e:
            raise APIError(f"Gemini influencer content generation error: {e}")
    
    def _build_intelligent_prompt(self, request: ContentRequest) -> str:
        """Build intelligent prompt optimized for Gemini's capabilities"""
        
        base_prompt = f"""
        You are SME Analytica's AI social media strategist, creating intelligent content for restaurant industry influence.
        
        SME Analytica Profile:
        - AI-driven analytics platform for restaurants, hotels, retail businesses
        - MenuFlow dynamic pricing technology (proven 10% margin improvement)
        - Real-time analytics with seamless POS integration
        - Making enterprise-level business intelligence accessible to SMEs
        - Trusted by 500+ restaurants for operational optimization
        
        Content Mission:
        - Position SME Analytica as the authoritative voice in restaurant analytics
        - Share data-driven insights that restaurant owners find valuable
        - Create content that drives engagement and establishes thought leadership
        - Build authentic relationships with the hospitality community
        
        Content Parameters:
        - Theme: {request.theme}
        - Language: {request.language}
        - Tone: {request.tone}
        - Max Length: {request.max_length} characters
        - Context: {json.dumps(request.context, indent=2)}
        
        Content Guidelines:
        - Lead with compelling data or insights
        - Use specific statistics and measurable results
        - Include actionable takeaways for restaurant owners
        - Maintain professional yet approachable tone
        - End with engagement-driving elements (questions, calls-to-action)
        - Use strategic hashtags for industry discoverability
        
        Create content that restaurant owners will find genuinely valuable and want to share with their networks.
        """
        
        return base_prompt
    
    def _extract_hashtags(self, content: str, suggested_hashtags: List[str]) -> List[str]:
        """Extract and optimize hashtags from content"""
        import re
        
        # Extract existing hashtags from content
        existing_hashtags = re.findall(r'#\w+', content)
        
        # Combine with suggested hashtags
        all_hashtags = list(set(existing_hashtags + [f"#{tag.lstrip('#')}" for tag in suggested_hashtags]))
        
        # SME Analytica relevant hashtags
        sme_hashtags = [
            "#RestaurantAnalytics", "#SMEAnalytics", "#MenuOptimization", 
            "#RestaurantTech", "#HospitalityAI", "#DataDriven",
            "#RestaurantOwner", "#SmallBusiness", "#BusinessIntelligence"
        ]
        
        # Add relevant SME hashtags if not already present
        for hashtag in sme_hashtags[:3]:  # Limit to top 3 relevant ones
            if hashtag.lower() not in [h.lower() for h in all_hashtags]:
                all_hashtags.append(hashtag)
        
        return all_hashtags[:5]  # Limit to 5 hashtags for optimal engagement
