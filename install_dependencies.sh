#!/bin/bash

# SME Analytica Social Media Manager - Dependency Installation Script
# Installs all required dependencies for the AI Council system

echo "🚀 Installing SME Analytica AI Council Dependencies"
echo "=================================================="

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install Python and pip first."
    exit 1
fi

# Upgrade pip
echo "📦 Upgrading pip..."
python -m pip install --upgrade pip

# Install core dependencies
echo "🤖 Installing AI provider dependencies..."
pip install google-generativeai>=0.3.0
pip install anthropic>=0.15.0
pip install openai>=1.12.0

# Install social media APIs
echo "📱 Installing social media APIs..."
pip install tweepy>=4.14.0

# Install database and storage
echo "💾 Installing database dependencies..."
pip install notion-client>=2.2.0

# Install all other requirements
echo "📋 Installing remaining dependencies..."
pip install -r requirements.txt

# Verify installations
echo ""
echo "✅ Verifying installations..."

# Check Google Generative AI
python -c "import google.generativeai; print('✅ Google Generative AI installed')" 2>/dev/null || echo "❌ Google Generative AI failed"

# Check Anthropic
python -c "import anthropic; print('✅ Anthropic installed')" 2>/dev/null || echo "❌ Anthropic failed"

# Check OpenAI
python -c "import openai; print('✅ OpenAI installed')" 2>/dev/null || echo "❌ OpenAI failed"

# Check Tweepy
python -c "import tweepy; print('✅ Tweepy installed')" 2>/dev/null || echo "❌ Tweepy failed"

# Check Notion
python -c "import notion_client; print('✅ Notion client installed')" 2>/dev/null || echo "❌ Notion client failed"

echo ""
echo "🎉 Installation complete!"
echo ""
echo "🚀 Next steps:"
echo "1. Set up your environment variables in .env file"
echo "2. Run: python demo_ai_council_collaboration.py"
echo "3. Or run: python main.py --mode=ai_council"
echo ""
echo "🤝 Your AI Council (GPT + Claude + Gemini) is ready!"
