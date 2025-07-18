#!/usr/bin/env python3
"""
SME Analytica Engagement Automation System
Handles intelligent social media engagement including likes, retweets, comments, and responses
"""

import asyncio
import logging
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass

from ..social.twitter_manager import TwitterManager
from ..social.linkedin_manager import LinkedInManager
from ..content.content_generator import ContentGenerator
from ..notion.notion_manager import NotionManager
from .grok_engagement import GrokEngagementFarmer
from ..ai_providers import AIProviderManager, ContentRequest, ContentType
from config.settings import sme_context


@dataclass
class EngagementOpportunity:
    """Represents a social media engagement opportunity"""
    platform: str  # 'twitter' or 'linkedin'
    post_id: str
    author: str
    content: str
    engagement_score: float
    opportunity_type: str  # 'like', 'retweet', 'comment', 'reply'
    keywords_matched: List[str]
    created_at: datetime
    metrics: Dict[str, int]  # likes, retweets, comments, etc.


@dataclass
class EngagementAction:
    """Represents an engagement action taken"""
    platform: str
    action_type: str  # 'like', 'retweet', 'comment', 'reply'
    target_post_id: str
    our_response_id: Optional[str]
    content: Optional[str]  # For comments/replies
    timestamp: datetime
    success: bool
    error_message: Optional[str] = None


class EngagementAutomation:
    """Intelligent social media engagement automation for SME Analytica"""
    
    def __init__(self, twitter_manager: TwitterManager, linkedin_manager: Optional[LinkedInManager] = None):
        self.twitter_manager = twitter_manager
        self.linkedin_manager = linkedin_manager
        # Initialize AI manager
        import os
        ai_config = {
            "openai_api_key": os.getenv("OPENAI_API_KEY", ""),
            "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY", ""),
            "perplexity_api_key": os.getenv("PERPLEXITY_API_KEY", ""),
            "grok_api_key": os.getenv("GROK_API_KEY", ""),
            "google_gemini_api_key": os.getenv("GOOGLE_GEMINI_API_KEY", "")
        }
        self.ai_manager = AIProviderManager(ai_config)
        self.content_generator = ContentGenerator()
        self.notion_manager = NotionManager()
        self.grok_farmer = GrokEngagementFarmer(twitter_manager)

        self.logger = logging.getLogger(__name__)
        
        # Engagement configuration
        self.daily_engagement_limits = {
            'twitter_likes': 50,
            'twitter_retweets': 20,
            'twitter_comments': 15,
            'twitter_replies': 10,
            'linkedin_likes': 30,
            'linkedin_comments': 10
        }
        
        # Track daily engagement counts
        self.daily_engagement_counts = {key: 0 for key in self.daily_engagement_limits.keys()}
        self.last_reset_date = datetime.now().date()
        
        # Engagement history
        self.engagement_history: List[EngagementAction] = []
        
        # Target keywords for finding engagement opportunities
        self.target_keywords = [
            # Restaurant & hospitality
            "restaurant analytics", "restaurant data", "restaurant pricing",
            "menu optimization", "food cost", "restaurant margins",
            "hospitality tech", "restaurant software", "pos system",
            
            # Small business
            "small business analytics", "sme data", "business intelligence",
            "small business growth", "restaurant owner", "cafe owner",
            
            # Technology & AI
            "ai for restaurants", "restaurant ai", "predictive analytics",
            "business automation", "data driven decisions",
            
            # Industry hashtags
            "#RestaurantTech", "#HospitalityTech", "#SmallBusiness",
            "#RestaurantAnalytics", "#MenuTech", "#AIforSMEs",
            "#RestaurantData", "#BusinessIntelligence"
        ]
        
        # Response templates for different scenarios
        self.response_templates = {
            'supportive_comment': [
                "Great insights! Data-driven decisions are crucial for restaurant success. 📊",
                "This resonates with what we see in restaurant analytics. Smart approach! 🎯",
                "Absolutely! We've seen similar patterns in our restaurant data analysis. 💡"
            ],
            'helpful_addition': [
                "Adding to this - our analytics show that {insight}. Have you considered {suggestion}?",
                "Great point! In our experience with restaurant data, {insight}. Thoughts?",
                "This aligns with our findings. We've also noticed that {insight}. 📈"
            ],
            'question_response': [
                "Great question! From our restaurant analytics perspective, {answer}. Hope this helps! 🤝",
                "We see this often in our data. {answer}. Would love to hear your experience! 💭",
                "Interesting question! Our analytics suggest {answer}. What's been your approach? 🔍"
            ]
        }

    async def run_engagement_automation(self) -> Dict[str, Any]:
        """Run the complete engagement automation workflow"""
        
        self.logger.info("🤝 Starting SME Analytica Engagement Automation")
        
        # Reset daily counters if needed
        self._reset_daily_counters_if_needed()
        
        results = {
            "engagement_mode": "active",
            "opportunities_found": 0,
            "actions_taken": 0,
            "platforms_engaged": [],
            "engagement_breakdown": {},
            "errors": []
        }
        
        try:
            # Phase 1: Find engagement opportunities
            self.logger.info("🔍 Phase 1: Finding engagement opportunities")
            opportunities = await self._find_engagement_opportunities()
            results["opportunities_found"] = len(opportunities)
            
            if not opportunities:
                self.logger.info("No engagement opportunities found")
                return results
            
            # Phase 2: Process engagement opportunities
            self.logger.info(f"🎯 Phase 2: Processing {len(opportunities)} engagement opportunities")
            engagement_actions = await self._process_engagement_opportunities(opportunities)
            results["actions_taken"] = len([a for a in engagement_actions if a.success])
            
            # Phase 3: Respond to mentions and replies
            self.logger.info("💬 Phase 3: Responding to mentions and replies")
            mention_responses = await self._respond_to_mentions()
            results["actions_taken"] += len([a for a in mention_responses if a.success])
            
            # Phase 4: Engage with industry conversations
            self.logger.info("🗣️ Phase 4: Engaging with industry conversations")
            conversation_engagements = await self._engage_with_conversations()
            results["actions_taken"] += len([a for a in conversation_engagements if a.success])

            # Phase 5: Grok engagement farming
            self.logger.info("🤖 Phase 5: Grok engagement farming")
            grok_results = await self.grok_farmer.run_grok_engagement_farming()
            results["grok_questions_asked"] = grok_results.get("questions_asked", 0)
            results["grok_topics_covered"] = grok_results.get("topics_covered", [])
            
            # Compile results
            all_actions = engagement_actions + mention_responses + conversation_engagements
            results["engagement_breakdown"] = self._compile_engagement_breakdown(all_actions)
            results["platforms_engaged"] = list(set([a.platform for a in all_actions if a.success]))

            # Add Grok farming stats
            grok_stats = self.grok_farmer.get_grok_farming_stats()
            results["grok_farming_stats"] = grok_stats

            # Save engagement analytics to Notion
            try:
                analytics_saved = self.notion_manager.save_engagement_analytics(results)
                if analytics_saved:
                    self.logger.info("📊 Engagement analytics saved to Notion")
                else:
                    self.logger.warning("⚠️ Failed to save engagement analytics to Notion")
            except Exception as e:
                self.logger.error(f"Error saving engagement analytics: {e}")

            self.logger.info(f"✅ Engagement automation completed: {results['actions_taken']} actions taken")
            
        except Exception as e:
            self.logger.error(f"❌ Engagement automation failed: {e}")
            results["errors"].append(f"engagement_automation: {e}")
        
        return results

    async def _find_engagement_opportunities(self) -> List[EngagementOpportunity]:
        """Find relevant engagement opportunities across platforms"""
        
        opportunities = []
        
        # Twitter engagement opportunities
        if self.twitter_manager:
            twitter_opportunities = await self._find_twitter_opportunities()
            opportunities.extend(twitter_opportunities)
        
        # LinkedIn engagement opportunities (limited by API)
        if self.linkedin_manager:
            linkedin_opportunities = await self._find_linkedin_opportunities()
            opportunities.extend(linkedin_opportunities)
        
        # Sort by engagement score
        opportunities.sort(key=lambda x: x.engagement_score, reverse=True)
        
        # Limit to top opportunities to avoid spam
        return opportunities[:20]

    async def _find_twitter_opportunities(self) -> List[EngagementOpportunity]:
        """Find Twitter engagement opportunities"""
        
        opportunities = []
        
        try:
            # Use TwitterManager's existing method
            twitter_opps = await self.twitter_manager.get_engagement_opportunities()
            
            for opp in twitter_opps:
                tweet = opp["tweet"]
                opportunity = EngagementOpportunity(
                    platform="twitter",
                    post_id=tweet.id,
                    author=tweet.author.username if hasattr(tweet, 'author') else "unknown",
                    content=tweet.text,
                    engagement_score=opp["engagement_score"],
                    opportunity_type=opp["opportunity_type"],
                    keywords_matched=[opp["search_term"]],
                    created_at=tweet.created_at if hasattr(tweet, 'created_at') else datetime.now(),
                    metrics=getattr(tweet, 'public_metrics', {})
                )
                opportunities.append(opportunity)
                
        except Exception as e:
            self.logger.error(f"Error finding Twitter opportunities: {e}")
        
        return opportunities

    async def _find_linkedin_opportunities(self) -> List[EngagementOpportunity]:
        """Find LinkedIn engagement opportunities (limited by API restrictions)"""
        
        # LinkedIn's API is very restrictive for content search
        # For now, return empty list but structure is ready for future enhancement
        self.logger.info("LinkedIn engagement opportunities: Limited by API restrictions")
        return []

    def _reset_daily_counters_if_needed(self):
        """Reset daily engagement counters if it's a new day"""
        
        current_date = datetime.now().date()
        if current_date != self.last_reset_date:
            self.daily_engagement_counts = {key: 0 for key in self.daily_engagement_limits.keys()}
            self.last_reset_date = current_date
            self.logger.info("🔄 Daily engagement counters reset")

    def _can_engage(self, platform: str, action_type: str) -> bool:
        """Check if we can perform a specific engagement action"""
        
        key = f"{platform}_{action_type}"
        if key not in self.daily_engagement_limits:
            return False
        
        return self.daily_engagement_counts[key] < self.daily_engagement_limits[key]

    def _increment_engagement_count(self, platform: str, action_type: str):
        """Increment the engagement counter for a specific action"""
        
        key = f"{platform}_{action_type}"
        if key in self.daily_engagement_counts:
            self.daily_engagement_counts[key] += 1

    def _compile_engagement_breakdown(self, actions: List[EngagementAction]) -> Dict[str, int]:
        """Compile engagement breakdown by platform and action type"""

        breakdown = {}
        for action in actions:
            if action.success:
                key = f"{action.platform}_{action.action_type}"
                breakdown[key] = breakdown.get(key, 0) + 1

        return breakdown

    async def _process_engagement_opportunities(self, opportunities: List[EngagementOpportunity]) -> List[EngagementAction]:
        """Process engagement opportunities and take appropriate actions"""

        actions = []

        for opportunity in opportunities:
            try:
                # Determine the best engagement action
                action_type = self._determine_engagement_action(opportunity)

                if not action_type or not self._can_engage(opportunity.platform, action_type):
                    continue

                # Execute the engagement action
                action = await self._execute_engagement_action(opportunity, action_type)
                if action:
                    actions.append(action)
                    self._increment_engagement_count(opportunity.platform, action_type)

                    # Minimal delay for fast execution
                    await asyncio.sleep(0.5)

            except Exception as e:
                self.logger.error(f"Error processing engagement opportunity: {e}")
                actions.append(EngagementAction(
                    platform=opportunity.platform,
                    action_type="error",
                    target_post_id=opportunity.post_id,
                    our_response_id=None,
                    content=None,
                    timestamp=datetime.now(),
                    success=False,
                    error_message=str(e)
                ))

        return actions

    def _determine_engagement_action(self, opportunity: EngagementOpportunity) -> Optional[str]:
        """Determine the best engagement action for an opportunity"""

        # Analyze content to determine appropriate action
        content_lower = opportunity.content.lower()

        # High engagement score posts - like and potentially retweet
        if opportunity.engagement_score > 15:
            if any(keyword in content_lower for keyword in ["restaurant", "analytics", "data", "sme"]):
                return "retweets" if random.random() > 0.7 else "likes"
            else:
                return "likes"

        # Medium engagement posts - like or comment
        elif opportunity.engagement_score > 8:
            if "?" in opportunity.content:  # Questions deserve thoughtful responses
                return "comments"
            else:
                return "likes"

        # Lower engagement posts - just like
        elif opportunity.engagement_score > 5:
            return "likes"

        return None

    async def _execute_engagement_action(self, opportunity: EngagementOpportunity, action_type: str) -> Optional[EngagementAction]:
        """Execute a specific engagement action"""

        if opportunity.platform == "twitter":
            return await self._execute_twitter_action(opportunity, action_type)
        elif opportunity.platform == "linkedin":
            return await self._execute_linkedin_action(opportunity, action_type)

        return None

    async def _execute_twitter_action(self, opportunity: EngagementOpportunity, action_type: str) -> Optional[EngagementAction]:
        """Execute Twitter engagement action"""

        try:
            response_id = None
            content = None
            success = False

            if action_type == "likes":
                success = await self.twitter_manager.like_tweet(opportunity.post_id)

            elif action_type == "retweets":
                # Generate a thoughtful comment for the retweet
                comment = await self._generate_retweet_comment(opportunity)
                if comment:
                    response_id = await self.twitter_manager.retweet_with_comment(opportunity.post_id, comment)
                    content = comment
                    success = response_id is not None

            elif action_type == "comments":
                # Generate a thoughtful reply
                comment = await self._generate_thoughtful_reply(opportunity)
                if comment:
                    response_id = await self.twitter_manager.reply_to_tweet(opportunity.post_id, comment)
                    content = comment
                    success = response_id is not None

            return EngagementAction(
                platform="twitter",
                action_type=action_type,
                target_post_id=opportunity.post_id,
                our_response_id=response_id,
                content=content,
                timestamp=datetime.now(),
                success=success
            )

        except Exception as e:
            self.logger.error(f"Error executing Twitter action {action_type}: {e}")
            return EngagementAction(
                platform="twitter",
                action_type=action_type,
                target_post_id=opportunity.post_id,
                our_response_id=None,
                content=None,
                timestamp=datetime.now(),
                success=False,
                error_message=str(e)
            )

    async def _execute_linkedin_action(self, opportunity: EngagementOpportunity, action_type: str) -> Optional[EngagementAction]:
        """Execute LinkedIn engagement action (limited by API)"""

        # LinkedIn engagement is limited by API restrictions
        # For now, just log the intent
        self.logger.info(f"LinkedIn {action_type} action intended for post {opportunity.post_id}")

        return EngagementAction(
            platform="linkedin",
            action_type=action_type,
            target_post_id=opportunity.post_id,
            our_response_id=None,
            content=None,
            timestamp=datetime.now(),
            success=False,
            error_message="LinkedIn engagement limited by API restrictions"
        )

    async def _respond_to_mentions(self) -> List[EngagementAction]:
        """Respond to mentions and direct replies"""

        actions = []

        if not self.twitter_manager:
            return actions

        try:
            # Get recent mentions
            mentions = await self.twitter_manager.get_mentions(max_results=10)

            for mention in mentions:
                if not self._can_engage("twitter", "replies"):
                    break

                # Generate appropriate response
                response = await self._generate_mention_response(mention)
                if response:
                    reply_id = await self.twitter_manager.reply_to_tweet(mention.id, response)

                    actions.append(EngagementAction(
                        platform="twitter",
                        action_type="replies",
                        target_post_id=mention.id,
                        our_response_id=reply_id,
                        content=response,
                        timestamp=datetime.now(),
                        success=reply_id is not None
                    ))

                    if reply_id:
                        self._increment_engagement_count("twitter", "replies")
                        await asyncio.sleep(0.5)

        except Exception as e:
            self.logger.error(f"Error responding to mentions: {e}")

        return actions

    async def _engage_with_conversations(self) -> List[EngagementAction]:
        """Engage with ongoing industry conversations"""

        actions = []

        # Find conversations around our target keywords
        conversation_keywords = [
            "restaurant analytics", "small business data", "hospitality tech",
            "#RestaurantTech", "#SmallBusiness", "#AIforSMEs"
        ]

        for keyword in conversation_keywords[:3]:  # Limit to avoid rate limits
            try:
                if not self._can_engage("twitter", "likes"):
                    break

                # Search for recent conversations
                tweets = await self.twitter_manager.search_tweets(keyword, max_results=10)

                for tweet in tweets:
                    if not self._can_engage("twitter", "likes"):
                        break

                    # Like relevant tweets
                    success = await self.twitter_manager.like_tweet(tweet.id)

                    actions.append(EngagementAction(
                        platform="twitter",
                        action_type="likes",
                        target_post_id=tweet.id,
                        our_response_id=None,
                        content=None,
                        timestamp=datetime.now(),
                        success=success
                    ))

                    if success:
                        self._increment_engagement_count("twitter", "likes")
                        await asyncio.sleep(0.2)

            except Exception as e:
                self.logger.error(f"Error engaging with conversations for {keyword}: {e}")

        return actions

    async def _generate_retweet_comment(self, opportunity: EngagementOpportunity) -> Optional[str]:
        """Generate a thoughtful comment for retweeting"""

        try:
            # Use AI to generate contextual comment
            prompt = f"""
            Generate a brief, professional comment for retweeting this post about {', '.join(opportunity.keywords_matched)}.

            Original post: "{opportunity.content}"

            Requirements:
            - Maximum 100 characters
            - Professional tone suitable for SME Analytica (restaurant analytics company)
            - Add value or insight
            - Include relevant emoji
            - Don't just repeat the original content

            Examples:
            - "Spot on! Data-driven pricing is game-changing for restaurants 📊"
            - "This aligns with our analytics findings! 🎯"
            - "Great insight for restaurant owners! 💡"
            """

            # Create content request
            content_request = ContentRequest(
                content_type=ContentType.TWEET,
                language='en',
                theme='retweet_comment',
                max_length=100,
                context={'prompt': prompt}
            )

            generated_content = await self.ai_manager.generate_content(content_request)
            response = generated_content.text if generated_content else None

            if response and len(response.strip()) <= 100:
                return response.strip()

        except Exception as e:
            self.logger.error(f"Error generating retweet comment: {e}")

        # Fallback to template
        templates = [
            "Great insights! 📊",
            "This resonates with our data! 🎯",
            "Valuable perspective! 💡",
            "Spot on! 🔥",
            "Data-driven approach! 📈"
        ]
        return random.choice(templates)

    async def _generate_thoughtful_reply(self, opportunity: EngagementOpportunity) -> Optional[str]:
        """Generate a thoughtful reply to a post"""

        try:
            # Analyze if it's a question or statement
            is_question = "?" in opportunity.content

            if is_question:
                prompt = f"""
                Generate a helpful, professional response to this question from a restaurant analytics expert perspective.

                Question: "{opportunity.content}"
                Author: @{opportunity.author}

                Requirements:
                - Maximum 280 characters
                - Provide genuine value/insight
                - Professional but friendly tone
                - Include relevant data point or tip if possible
                - Use SME Analytica's expertise in restaurant analytics
                - Include 1-2 relevant emojis

                Context: SME Analytica provides AI-driven analytics for restaurants, hotels, and retail businesses.
                """
            else:
                prompt = f"""
                Generate a supportive, professional comment that adds value to this post.

                Post: "{opportunity.content}"
                Author: @{opportunity.author}

                Requirements:
                - Maximum 280 characters
                - Add complementary insight or perspective
                - Professional but engaging tone
                - Reference restaurant/business analytics when relevant
                - Include 1-2 relevant emojis
                - Don't just agree - add value
                """

            # Create content request
            content_request = ContentRequest(
                content_type=ContentType.TWEET,
                language='en',
                theme='thoughtful_reply',
                max_length=280,
                context={'prompt': prompt}
            )

            generated_content = await self.ai_manager.generate_content(content_request)
            response = generated_content.text if generated_content else None

            if response and len(response.strip()) <= 280:
                return response.strip()

        except Exception as e:
            self.logger.error(f"Error generating thoughtful reply: {e}")

        # Fallback to contextual templates
        if "?" in opportunity.content:
            templates = self.response_templates['question_response']
            template = random.choice(templates)
            return template.format(
                answer="our analytics suggest focusing on peak hours and customer flow patterns"
            )
        else:
            return random.choice(self.response_templates['supportive_comment'])

    async def _generate_mention_response(self, mention) -> Optional[str]:
        """Generate appropriate response to mentions"""

        try:
            mention_text = mention.text if hasattr(mention, 'text') else str(mention)
            author = mention.author.username if hasattr(mention, 'author') and hasattr(mention.author, 'username') else "user"

            prompt = f"""
            Generate a professional, helpful response to this mention of SME Analytica.

            Mention: "{mention_text}"
            From: @{author}

            Requirements:
            - Maximum 280 characters
            - Professional and friendly tone
            - Thank them if appropriate
            - Offer help or insight if they have a question
            - Represent SME Analytica's expertise in restaurant analytics
            - Include relevant emoji
            - Be genuine and helpful, not salesy

            Context: SME Analytica provides AI-driven analytics for restaurants and SMEs.
            """

            # Create content request
            content_request = ContentRequest(
                content_type=ContentType.TWEET,
                language='en',
                theme='mention_response',
                max_length=280,
                context={'prompt': prompt}
            )

            generated_content = await self.ai_manager.generate_content(content_request)
            response = generated_content.text if generated_content else None

            if response and len(response.strip()) <= 280:
                return response.strip()

        except Exception as e:
            self.logger.error(f"Error generating mention response: {e}")

        # Fallback response
        return f"Thanks for the mention! Happy to help with any restaurant analytics questions. 🤝📊"

    def get_engagement_stats(self) -> Dict[str, Any]:
        """Get current engagement statistics"""

        stats = {
            "daily_limits": self.daily_engagement_limits,
            "daily_counts": self.daily_engagement_counts,
            "remaining_capacity": {
                key: self.daily_engagement_limits[key] - self.daily_engagement_counts[key]
                for key in self.daily_engagement_limits
            },
            "last_reset": self.last_reset_date.isoformat(),
            "total_actions_today": sum(self.daily_engagement_counts.values()),
            "engagement_history_count": len(self.engagement_history)
        }

        # Add historical analytics from Notion
        try:
            historical_analytics = self.notion_manager.get_engagement_analytics(days=7)
            stats["historical_analytics"] = historical_analytics
        except Exception as e:
            self.logger.error(f"Error retrieving historical analytics: {e}")
            stats["historical_analytics"] = {"error": str(e)}

        return stats

    def get_engagement_summary(self) -> str:
        """Get a human-readable engagement summary"""

        stats = self.get_engagement_stats()

        summary = f"""
🤝 SME Analytica Engagement Summary

📊 Today's Activity:
• Total Actions: {stats['total_actions_today']}
• Twitter Likes: {stats['daily_counts'].get('twitter_likes', 0)}/{stats['daily_limits']['twitter_likes']}
• Twitter Retweets: {stats['daily_counts'].get('twitter_retweets', 0)}/{stats['daily_limits']['twitter_retweets']}
• Twitter Comments: {stats['daily_counts'].get('twitter_comments', 0)}/{stats['daily_limits']['twitter_comments']}
• Twitter Replies: {stats['daily_counts'].get('twitter_replies', 0)}/{stats['daily_limits']['twitter_replies']}

📈 Historical Data (Last 7 Days):
• Total Sessions: {stats['historical_analytics'].get('total_engagement_sessions', 'N/A')}
• Date Range: {stats['historical_analytics'].get('date_range', 'N/A')}

🔄 System Status:
• Last Reset: {stats['last_reset']}
• Engagement History: {stats['engagement_history_count']} actions recorded
        """

        return summary.strip()
