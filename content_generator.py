"""
SME Social Media Manager - Simple Content Generator
AI-powered content creation using single provider (OpenAI or Anthropic)
"""

import openai
import anthropic
from typing import Dict, List, Optional
from config import Config

class ContentGenerator:
    """Simple content generator using single AI provider"""
    
    def __init__(self, config: Config):
        self.config = config
        self.ai_provider = config.get_ai_provider()
        
        # Initialize AI client
        if self.ai_provider == "openai":
            openai.api_key = config.openai_api_key
            self.client = openai.OpenAI(api_key=config.openai_api_key)
        elif self.ai_provider == "anthropic":
            self.client = anthropic.Anthropic(api_key=config.anthropic_api_key)
        else:
            raise ValueError("No valid AI provider configured")
    
    def generate_daily_posts(self, num_posts: int = 3) -> List[Dict]:
        """Generate daily social media posts"""
        posts = []
        
        content_types = [
            "educational_tip",
            "industry_insight", 
            "community_question"
        ]
        
        for i in range(num_posts):
            content_type = content_types[i % len(content_types)]
            post = self._generate_single_post(content_type)
            if post:
                posts.append(post)
                
        return posts
    
    def _generate_single_post(self, content_type: str) -> Optional[Dict]:
        """Generate a single post based on content type"""
        
        prompts = {
            "educational_tip": f"""Create a helpful business tip for {self.config.target_audience}. 
                Focus on practical advice for restaurant/hospitality operations. 
                Keep it under 250 characters for Twitter. Include 2-3 relevant hashtags.""",
                
            "industry_insight": f"""Share an industry trend or insight relevant to {self.config.target_audience}.
                Focus on restaurant/hospitality industry developments.
                Keep it under 250 characters for Twitter. Include 2-3 relevant hashtags.""",
                
            "community_question": f"""Create an engaging question to spark discussion among {self.config.target_audience}.
                Focus on challenges in restaurant/hospitality business.
                Keep it under 250 characters for Twitter. Include 2-3 relevant hashtags."""
        }
        
        prompt = prompts.get(content_type, prompts["educational_tip"])
        
        try:
            if self.ai_provider == "openai":
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"You are a social media expert for {self.config.company_name}, helping restaurant and small business owners grow."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=150,
                    temperature=0.7
                )
                content = response.choices[0].message.content.strip()
                
            elif self.ai_provider == "anthropic":
                response = self.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=150,
                    messages=[
                        {"role": "user", "content": f"As a social media expert for {self.config.company_name}: {prompt}"}
                    ]
                )
                content = response.content[0].text.strip()
            
            return {
                "content": content,
                "type": content_type,
                "platforms": ["twitter", "linkedin"],
                "hashtags": self._extract_hashtags(content)
            }
            
        except Exception as e:
            print(f"Error generating content: {e}")
            return None
    
    def _extract_hashtags(self, content: str) -> List[str]:
        """Extract hashtags from content"""
        import re
        hashtags = re.findall(r'#\w+', content)
        return hashtags
    
    def generate_response_to_mention(self, mention_text: str, author: str) -> Optional[str]:
        """Generate a response to a mention"""
        prompt = f"""Someone mentioned us on social media: "{mention_text}" by @{author}
        
        Generate a helpful, professional response that:
        1. Thanks them for the mention
        2. Offers value related to restaurant/hospitality business
        3. Stays under 240 characters
        4. Uses a friendly, expert tone"""
        
        try:
            if self.ai_provider == "openai":
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"You are the social media voice of {self.config.company_name}, a helpful expert in restaurant analytics."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=100,
                    temperature=0.7
                )
                return response.choices[0].message.content.strip()
                
            elif self.ai_provider == "anthropic":
                response = self.client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=100,
                    messages=[
                        {"role": "user", "content": f"As {self.config.company_name}'s social media expert: {prompt}"}
                    ]
                )
                return response.content[0].text.strip()
                
        except Exception as e:
            print(f"Error generating response: {e}")
            return None