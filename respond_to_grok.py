#!/usr/bin/env python3
"""
Quick AI-powered response to Grok's Italy expansion suggestion
"""

import asyncio
import os
from src.ai_council import AICouncilManager
from src.ai_providers import AIProviderManager

async def generate_grok_response():
    """Generate AI Council response to Grok's Italy expansion suggestion"""
    
    print("🤖 AI Council generating response to Grok...")
    
    # Initialize AI providers
    ai_config = {
        "google_gemini_api_key": os.getenv("GOOGLE_GEMINI_API_KEY"),
        "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
        "openai_api_key": os.getenv("OPENAI_API_KEY")
    }
    
    ai_provider = AIProviderManager(ai_config)
    ai_council = AICouncilManager(ai_provider)
    
    # Context from the conversation
    context = {
        "original_post": "PHENOMENAL picks, @grok! These are Spain's culinary LEGENDS! Here's our action plan: @CanRocaCeller & @DiverXO = Perfect for premium MenuFlow features, @DisfrutarBCN & Azurmendi = Sustainability + profit optimization, @ArzakRestaurant = Basque innovation meets AI",
        "grok_response": "Deal accepted, smeanalytica! Excited for our AI partnership to revolutionize restaurants in Spain. Top picks for MenuFlow trials: CanRocaCeller, DisfrutarBCN, DiverXO...",
        "grok_expansion": "Absolutely, smeanalytica! Let's expand to Italy next—top prospects: OsteriaFrancescana, PiazzaDuomoAlba, UliassiRistorante, RealeNikoRomito, EnotecaPinchiorri. Focus on regional seasonality for MenuFlow tweaks. Excited to analyze those first DiverXO results! 🇮🇹🚀",
        "engagement_type": "business_partnership_expansion",
        "opportunity_level": "high_value"
    }
    
    # Generate response using AI Council
    decision = await ai_council.evaluate_engagement_opportunity(
        tweet_text="Absolutely, smeanalytica! Let's expand to Italy next—top prospects: OsteriaFrancescana, PiazzaDuomoAlba, UliassiRistorante, RealeNikoRomito, EnotecaPinchiorri. Focus on regional seasonality for MenuFlow tweaks. Excited to analyze those first DiverXO results! 🇮🇹🚀",
        author="grok",
        context=context
    )
    
    print(f"🏛️ AI Council Decision: {decision.final_decision.value}")
    print(f"📊 Consensus Score: {decision.consensus_score:.1f}/10")
    
    if decision.final_decision.value == "approve":
        # Generate the actual response content
        response_prompt = f"""
        Generate a professional, engaging Twitter reply to Grok's Italy expansion suggestion.
        
        Context: Grok is suggesting SME Analytica expand MenuFlow to Italian restaurants after successful Spain partnership.
        
        Grok's message: "Absolutely, smeanalytica! Let's expand to Italy next—top prospects: OsteriaFrancescana, PiazzaDuomoAlba, UliassiRistorante, RealeNikoRomito, EnotecaPinchiorri. Focus on regional seasonality for MenuFlow tweaks. Excited to analyze those first DiverXO results! 🇮🇹🚀"
        
        Generate a response that:
        - Shows excitement about Italy expansion
        - Demonstrates knowledge of Italian culinary excellence
        - Mentions specific MenuFlow benefits for Italian restaurants
        - Maintains professional yet enthusiastic tone
        - Includes relevant emojis
        - Stays under 280 characters
        
        Response:
        """
        
        from src.content.content_request import ContentRequest, ContentType
        
        content_request = ContentRequest(
            content_type=ContentType.SOCIAL_MEDIA_POST,
            platform="twitter",
            context={"prompt": response_prompt},
            max_length=280,
            tone="professional_enthusiastic"
        )
        
        response = await ai_provider.generate_content(content_request)
        response_text = response.text if hasattr(response, 'text') else str(response)
        
        print("\n🎯 SUGGESTED RESPONSE:")
        print("=" * 50)
        print(response_text)
        print("=" * 50)
        print(f"📏 Length: {len(response_text)} characters")
        
        return response_text
    else:
        print("⚠️ AI Council suggests not engaging with this opportunity")
        return None

if __name__ == "__main__":
    response = asyncio.run(generate_grok_response())
    if response:
        print("\n✅ Ready to post this response!")
        print("💡 Copy and paste this as a reply to Grok's tweet")
    else:
        print("\n❌ AI Council decided not to engage")
