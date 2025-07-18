#!/usr/bin/env python3
"""
Quick AI response to Grok's Italy expansion suggestion
"""

import asyncio
import os
from src.ai_providers import AIProviderManager

async def generate_response():
    """Generate response to Grok's Italy expansion suggestion"""
    
    print("🤖 Generating AI response to Grok...")
    
    # Initialize AI providers
    ai_config = {
        "google_gemini_api_key": os.getenv("GOOGLE_GEMINI_API_KEY"),
        "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
        "openai_api_key": os.getenv("OPENAI_API_KEY")
    }
    
    ai_provider = AIProviderManager(ai_config)
    
    # Response prompt
    prompt = """Generate a professional, engaging Twitter reply to Grok's Italy expansion suggestion for SME Analytica.

Context: 
- Grok suggested expanding MenuFlow (restaurant analytics) to Italy
- Mentioned top Italian restaurants: OsteriaFrancescana, PiazzaDuomoAlba, UliassiRistorante, RealeNikoRomito, EnotecaPinchiorri
- Grok is excited about analyzing DiverXO results from Spain
- This is a high-value business partnership opportunity

Grok's message: "Absolutely, smeanalytica! Let's expand to Italy next—top prospects: OsteriaFrancescana, PiazzaDuomoAlba, UliassiRistorante, RealeNikoRomito, EnotecaPinchiorri. Focus on regional seasonality for MenuFlow tweaks. Excited to analyze those first DiverXO results! 🇮🇹🚀"

Generate a response that:
- Shows excitement about Italy expansion
- Acknowledges the excellent restaurant choices
- Mentions MenuFlow's benefits for Italian cuisine
- References regional seasonality insight
- Maintains professional yet enthusiastic tone
- Uses relevant emojis
- Stays under 280 characters

Response:"""

    try:
        # Try Anthropic first
        response = await ai_provider._anthropic_generate(prompt)
        response_text = response.strip()
        
        print("\n🎯 AI-GENERATED RESPONSE:")
        print("=" * 60)
        print(response_text)
        print("=" * 60)
        print(f"📏 Length: {len(response_text)} characters")
        
        if len(response_text) <= 280:
            print("✅ Perfect length for Twitter!")
        else:
            print("⚠️ Too long - needs trimming")
            
        return response_text
        
    except Exception as e:
        print(f"❌ Error generating response: {e}")
        
        # Fallback manual response
        fallback = "🇮🇹 Brilliant choices, @grok! Those Italian legends are perfect for MenuFlow's regional seasonality features. OsteriaFrancescana + our AI = culinary magic! Can't wait to see DiverXO's data insights fuel our Italy expansion. Let's revolutionize Italian dining! 🚀✨"
        
        print("\n🔄 FALLBACK RESPONSE:")
        print("=" * 60)
        print(fallback)
        print("=" * 60)
        print(f"📏 Length: {len(fallback)} characters")
        
        return fallback

if __name__ == "__main__":
    response = asyncio.run(generate_response())
    print("\n✅ READY TO POST!")
    print("💡 Copy this response and reply to Grok's tweet:")
    print(f"\n📝 {response}")
