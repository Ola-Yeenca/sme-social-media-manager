# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🎯 Project Overview

**SME Social Media Manager** - AI-powered multi-platform social media automation system with viral prediction capabilities. Automates Twitter and LinkedIn posting, engagement, and content optimization for SME Analytica, designed to grow followers through data-driven viral content strategies.

## 🚀 Core Development Commands

### Bot Operations
```bash
# Install dependencies
pip install -r requirements.txt

# Run bot in different modes
python bot.py                           # Auto mode (smart scheduling)
python bot.py --posting-only             # Content-only (saves API quota)
python bot.py --weekly-engagement        # Full engagement mode (mentions + posting)
python bot.py --multi-platform           # Post to both Twitter + LinkedIn
python bot.py --test                     # Test mode (no API calls)

# Viral prediction system
python bot.py --viral-test               # Test viral prediction algorithms
python bot.py --viral-analyze "tweet"    # Analyze specific tweet potential
python viral_predictor.py               # Run viral prediction demo

# LinkedIn integration
python linkedin_manager.py              # Test LinkedIn connection and posting

# Configuration testing
python config.py                        # Validate environment variables
python -c "from config import Config; print(Config().get_status())"
```

### Testing Suite
```bash
# Install test dependencies
pip install -r requirements_test.txt
playwright install chromium

# Run all tests
python run_all_tests.py                 # Complete test suite with reports

# Run specific test categories
python test_viral_prediction.py         # Unit tests for viral algorithms
python test_bot_integration.py          # Integration tests (mocked APIs)
python test_e2e_playwright.py           # End-to-end browser automation
python demo_tests.py                    # Interactive demo system
```

### GitHub Actions
- **Workflow**: `.github/workflows/sme-social-bot.yml` (single consolidated workflow)
- **Daily runs**: 6 AM, 12 PM, 6 PM, 12 AM UTC (posting-only mode)
- **Weekly runs**: Sunday 8 AM UTC (full engagement mode)
- **Manual trigger**: GitHub Actions interface with mode selection

## 🏗️ Architecture Overview

### Core System Design
The bot uses a modular architecture centered around three main components:

**SMESocialBot** (`bot.py`) - Main orchestration class that:
- Manages multi-platform posting (Twitter + LinkedIn)
- Coordinates AI content generation with viral optimization
- Handles rate limiting and API quota management
- Implements intelligent scheduling (daily posts vs weekly engagement)

**ViralTweetPredictor** (`viral_predictor.py`) - Predictive content optimization:
- Scores content 0-100 based on viral characteristics
- Analyzes: content quality, timing, hashtags, engagement potential, trends
- Generates optimized variations and recommendations
- Platform-specific optimization (Twitter vs LinkedIn)

**LinkedInManager** (`linkedin_manager.py`) - Professional platform integration:
- Adapts Twitter content for LinkedIn's professional context
- Applies LinkedIn-specific viral prediction adjustments
- Handles LinkedIn API authentication and posting

### AI Integration Chain
The system uses a cascading AI fallback strategy:
1. **OpenAI GPT** (primary) - for content generation
2. **Anthropic Claude** (fallback 1) - if OpenAI fails  
3. **Groq** (fallback 2) - if both fail

Content generation prompts are business-focused for restaurant/SME audience with Spanish/English bilingual support.

### Rate Limiting Strategy
**Current Implementation (until Aug 11, 2025):**
- **Daily mode**: Posting-only (0 API retrievals, 3-4 posts)
- **Sunday mode**: Full engagement (mentions + search + posting, ~12 retrievals)
- **Monthly quota**: 12/100 retrievals used, 100/500 posts used

This strategy prevents API quota exhaustion while maintaining consistent posting.

## 🔧 Environment Configuration

### Required API Keys
```bash
# Twitter API (Required)
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=
TWITTER_BEARER_TOKEN=

# AI Providers (At least one required)
OPENAI_API_KEY=              # Primary AI provider
ANTHROPIC_API_KEY=           # Fallback AI provider
GROQ_API_KEY=                # Fallback AI provider

# LinkedIn Integration (Optional)
LINKEDIN_ACCESS_TOKEN=       # For LinkedIn posting
LINKEDIN_ORGANIZATION_ID=    # For company page posting

# Optional Services
NOTION_API_KEY=             # Analytics storage
SOCIAL_MEDIA_DB_ID=         # Notion database ID
```

### Configuration Validation
The `Config` class (`config.py`) validates all environment variables on startup and provides fallback chains for AI providers. Use `python config.py` to test configuration.

## 🧪 Testing Architecture

### Test Categories
**Unit Tests** (`test_viral_prediction.py`):
- Viral score calculation algorithms
- Content optimization functions
- Hashtag and timing analysis
- Engagement prediction models

**Integration Tests** (`test_bot_integration.py`):
- Bot initialization with mocked APIs
- Multi-platform posting workflows  
- AI provider fallback chains
- Rate limiting behavior

**End-to-End Tests** (`test_e2e_playwright.py`):
- Complete workflow simulation with browser automation
- GitHub Actions workflow validation
- API mocking with request interception
- Cross-platform content adaptation

### Test Runner
`run_all_tests.py` orchestrates all test suites and generates JSON reports in `./test-results/`. It provides comprehensive coverage analysis and performance benchmarks.

## 📊 Viral Prediction System

### Scoring Algorithm
The viral predictor uses weighted scoring across 5 dimensions:
- **Content (30%)**: Emotional triggers, power words, call-to-actions, length optimization
- **Engagement (25%)**: Questions, personal stories, controversial topics, lists
- **Timing (15%)**: Optimal posting hours (8am, 12pm, 5pm, 8pm UTC)
- **Hashtags (15%)**: Quality and quantity (2-4 optimal), trending topic alignment  
- **Trends (15%)**: Alignment with current business/AI/productivity topics

### Content Optimization
When viral scores are below 70/100, the system automatically:
1. Adds trending hashtags from tiered quality lists
2. Includes engagement-driving questions
3. Optimizes length for platform (140-200 chars Twitter, 300+ LinkedIn)
4. Adds emotional triggers and power words

### Platform Adaptation
LinkedIn content receives professional context adjustments:
- Hashtag expansion (#AI → #ArtificialIntelligence #AI)
- Professional call-to-actions
- Business hours timing optimization  
- Extended content length support

## 🚨 Critical API Quota Management

### Current Status (Fixed August 9, 2025)
- **GitHub Workflow**: ✅ Fixed sync issue with consolidated `sme-social-bot.yml`
- **Dependency Issue**: ✅ Resolved `grok` → `groq` package correction
- **LinkedIn Integration**: ✅ Active and posting-ready
- **Viral Prediction**: ✅ Integrated with both Twitter and LinkedIn

### Production Behavior
The bot automatically switches modes based on date/time:
- **Until Aug 11**: Posting-only mode (4 posts/day, 0 retrievals)  
- **Sundays**: Full engagement (mentions + posting, ~12 retrievals)
- **After Aug 11**: Weekly engagement strategy (Sunday full mode only)

### Monitoring Commands
```bash
# Check bot status
python bot.py --test                    # Validate without API calls

# Monitor API usage
python check_rate_limit.py             # Check current rate limits

# Test platform connections
python linkedin_manager.py             # Verify LinkedIn integration
python -c "import tweepy; print('Twitter lib OK')"
```

## 🎯 Content Strategy

### Audience Targeting
- **Primary**: Restaurant owners, hospitality managers
- **Secondary**: Small business owners, retail managers  
- **Geographic**: Europe (Madrid timezone), Spanish/English bilingual
- **Content Focus**: Data-driven business insights, pricing optimization, profit margins

### Viral Content Patterns
The system is trained on these high-engagement patterns:
- **Questions**: Drive comments and engagement
- **Data/Statistics**: "47% revenue increase", "Most restaurants waste 80% of data"
- **Professional insights**: Business tips, industry trends, growth strategies
- **Controversial opinions**: "Unpopular opinion: Most businesses...", "Hot take: Dynamic pricing..."

### Multi-Platform Strategy  
- **Twitter**: Concise insights with trending hashtags, real-time engagement
- **LinkedIn**: Professional context, expanded explanations, business networking focus
- **Cross-posting**: Automatic adaptation with platform-specific optimization

## 📁 Key File Structure

```
sme_social_manager/
├── bot.py                     # Main bot orchestration 
├── viral_predictor.py         # Viral content prediction system
├── linkedin_manager.py        # LinkedIn platform integration
├── config.py                  # Environment configuration management
├── requirements.txt           # Core dependencies (Twitter, LinkedIn, AI)
├── requirements_test.txt      # Testing dependencies (Playwright, etc.)
├── .github/workflows/
│   └── sme-social-bot.yml     # Single consolidated workflow
├── test_*.py                  # Test suite files
├── run_all_tests.py           # Master test runner
└── demo_tests.py              # Interactive demo system
```

## 🔄 Development Workflow

### Local Testing
1. `cp .env.example .env` and configure API keys
2. `python bot.py --test` to validate setup
3. `python bot.py --viral-test` to test prediction system
4. `python bot.py --posting-only --multi-platform` for full simulation

### Production Deployment
1. Configure GitHub Secrets with all required API keys
2. Push to main branch triggers workflow validation
3. Monitor GitHub Actions for successful runs
4. Check artifacts for execution logs and viral scores

### Content Quality Assurance
- **Voice**: Conversational expert, data-driven consultant  
- **Languages**: 70% English, 30% Spanish
- **Hashtags**: 2-4 relevant business/tech hashtags per post
- **Value Focus**: Practical insights for restaurant/SME profit optimization

The bot maintains a consistent brand voice while adapting content tone and complexity for each platform's professional context.