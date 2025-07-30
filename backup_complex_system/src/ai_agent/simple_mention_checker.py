#!/usr/bin/env python3
"""
Simple AI Mention Checker for SME Analytica
Single responsibility: Check Twitter mentions once per hour without complex rate limiting
"""

import logging
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

from ..social.twitter_manager import TwitterManager
from ..notion.notion_manager import NotionManager


class SimpleMentionChecker:
    """Simple AI agent that checks Twitter mentions once per run"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize Twitter manager with credentials
        twitter_credentials = {
            "api_key": os.getenv("TWITTER_API_KEY"),
            "api_secret": os.getenv("TWITTER_API_SECRET"),
            "access_token": os.getenv("TWITTER_ACCESS_TOKEN"),
            "access_token_secret": os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
            "bearer_token": os.getenv("TWITTER_BEARER_TOKEN")
        }
        
        # Validate Twitter credentials
        if not all(twitter_credentials.values()):
            raise ValueError("Missing Twitter API credentials")
            
        self.twitter_manager = TwitterManager(twitter_credentials)
        
        # Optional Notion integration
        try:
            self.notion_manager = NotionManager()
        except Exception as e:
            self.logger.warning(f"Notion integration not available: {e}")
            self.notion_manager = None
    
    async def check_mentions(self) -> Dict[str, Any]:
        """
        Check Twitter mentions and process up to 5 sequentially
        Returns simple success/failure status
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "mentions_found": 0,
            "mentions_processed": 0,
            "success": False,
            "errors": []
        }
        
        try:
            self.logger.info("🔍 Checking Twitter mentions for @smeanalytica...")
            
            # Make ONE API call to get mentions - tweepy handles rate limiting
            mentions = await self.twitter_manager.get_mentions()
            
            if not mentions:
                self.logger.info("📭 No new mentions found")
                results["success"] = True
                return results
            
            results["mentions_found"] = len(mentions)
            self.logger.info(f"📨 Found {len(mentions)} mentions")
            
            # Process up to 5 mentions sequentially (no concurrency)
            for mention in mentions[:5]:
                try:
                    processed = await self._process_single_mention(mention)
                    if processed:
                        results["mentions_processed"] += 1
                        
                except Exception as e:
                    self.logger.error(f"Error processing mention: {e}")
                    results["errors"].append(str(e))
            
            results["success"] = True
            self.logger.info(f"✅ Processed {results['mentions_processed']} mentions successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to check mentions: {e}")
            results["errors"].append(str(e))
            results["success"] = False
        
        # Log results to Notion if available
        if self.notion_manager:
            try:
                await self._log_to_notion(results)
            except Exception as e:
                self.logger.warning(f"Failed to log to Notion: {e}")
        
        return results
    
    async def _process_single_mention(self, mention: Dict[str, Any]) -> bool:
        """
        Process a single mention - simple acknowledgment reply
        Returns True if processed successfully
        """
        try:
            author = mention.get('author', {}).get('username', 'unknown')
            content = mention.get('text', '')
            tweet_id = mention.get('id')
            
            self.logger.info(f"📝 Processing mention from @{author}: {content[:50]}...")
            
            # Simple response - just acknowledge the mention
            response = self._generate_simple_response(author, content)
            
            if response and tweet_id:
                # Post reply using Twitter manager
                reply_id = await self.twitter_manager.reply_to_tweet(tweet_id, response)
                
                if reply_id:
                    self.logger.info(f"✅ Replied to @{author}: {response}")
                    return True
                else:
                    self.logger.warning(f"⚠️ Failed to post reply to @{author}")
                    return False
            
        except Exception as e:
            self.logger.error(f"Error processing mention: {e}")
            return False
        
        return False
    
    def _generate_simple_response(self, author: str, content: str) -> Optional[str]:
        """
        Generate a simple acknowledgment response
        No complex AI - just friendly acknowledgment
        """
        content_lower = content.lower()
        
        # Simple response templates based on content
        if any(word in content_lower for word in ['help', 'question', 'how']):
            return f"Hi @{author}! Thanks for reaching out. We'd be happy to help with your restaurant analytics needs. Feel free to DM us for more details! 📊"
        
        elif any(word in content_lower for word in ['thanks', 'thank you', 'great']):
            return f"Thank you @{author}! We're glad you find our restaurant analytics helpful. Always here if you need insights! 🙏"
        
        elif any(word in content_lower for word in ['restaurant', 'menu', 'pricing']):
            return f"Hi @{author}! Restaurant optimization is exactly what we do best. Our analytics help boost margins ~10%. Happy to share more insights! 📈"
        
        else:
            # Generic friendly response
            return f"Hi @{author}! Thanks for the mention. We're here to help restaurants optimize with data-driven insights. DM us anytime! 💡"
    
    async def _log_to_notion(self, results: Dict[str, Any]) -> None:
        """Log results to Notion (optional)"""
        if not self.notion_manager:
            return
            
        try:
            log_data = {
                "timestamp": results["timestamp"],
                "system": "simple_mention_checker",
                "mentions_found": results["mentions_found"],
                "mentions_processed": results["mentions_processed"],
                "success": results["success"],
                "errors": results["errors"]
            }
            
            # Use existing Notion integration
            await self.notion_manager.save_engagement_analytics(log_data)
            
        except Exception as e:
            self.logger.warning(f"Failed to log to Notion: {e}")


# Factory function for easy usage
async def create_simple_mention_checker() -> SimpleMentionChecker:
    """Create and return a simple mention checker"""
    return SimpleMentionChecker()


# CLI interface for testing
if __name__ == "__main__":
    import asyncio
    
    async def main():
        checker = await create_simple_mention_checker()
        results = await checker.check_mentions()
        print(f"Results: {results}")
    
    asyncio.run(main())