# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**SME Social Media Manager** - Content manager and social media automation for the SME Analytica product family:

| Product | Domain | SME_INDUSTRY value |
|---------|--------|-------------------|
| MenuFlow | restaurants.smeanalytica.dev | `restaurant` |
| RealEstate | smeanalytica.dev/products/realestate | `real_estate` |
| Regula AI | regula-ai.com | `compliance` |
| Conversa | conversa.smeanalytica.dev | `conversa` |
| SME Analytica | smeanalytica.dev | `general` |

Automates Twitter and LinkedIn posting with AI-powered viral prediction scoring. Posts 1 unique piece of content per run (3x daily) to maintain natural posting frequency.

## Commands

```bash
# Install
pip install -r requirements.txt

# Bot modes
python bot.py                      # Auto mode
python bot.py --posting-only       # Post only (no API retrievals)
python bot.py --weekly-engagement  # Full engagement + 7-day mentions
python bot.py --multi-platform     # Twitter + LinkedIn
python bot.py --test               # Dry run
python bot.py --viral-test         # Test viral scoring
python bot.py --viral-analyze "text"  # Analyze specific content
python bot.py --analytics          # Show performance insights
python bot.py --update-engagement  # Update engagement metrics for past posts

# Test modules directly
python viral_predictor.py          # Demo viral prediction
python linkedin_manager.py         # Test LinkedIn connection
python engagement_tracker.py       # Demo engagement tracking
python config.py                   # Validate environment

# Run tests
pip install -r requirements_test.txt && playwright install chromium
python run_all_tests.py            # Full suite -> ./test-results/

# Single test file
PYTHONPATH=. python tests/test_viral_prediction.py
PYTHONPATH=. python tests/test_bot_integration.py
```

## Architecture

```
bot.py (SMESocialBot)
    |
    +-- generate_content()
    |       +-- dynamic_content.py (DynamicContentEngine)
    |       |       Pulls from HackerNews, Reddit, industry stats
    |       +-- content_generator.py (ContentGenerator)
    |               Template-based generation with variable substitution
    |
    +-- post_content() / post_multi_platform()
    |       +-- viral_predictor.py (ViralTweetPredictor)
    |       |       Scores 0-100, auto-optimizes if <70
    |       +-- linkedin_manager.py (LinkedInManager)
    |       |       Adapts content for professional context
    |       +-- engagement_tracker.py (EngagementTracker)
    |               Records posts, tracks performance, provides learning insights
    |
    +-- config.py (Config)
            Environment validation, AI fallback chain
```

### Strategy Pattern

Both content systems use abstract base classes for multi-product support:

**content_generator.py** - `IndustryStrategy` (template-based):
- `RestaurantStrategy` - Restaurant/hospitality templates with POS, food cost, menu metrics
- `RealEstateStrategy` - Property market templates with DOM, pricing, lead conversion metrics
- `ComplianceStrategy` - Compliance/GRC templates with audit, risk, regulatory metrics
- `ConversaStrategy` - Customer experience templates with response time, satisfaction, chatbot metrics
- `GeneralSMEStrategy` - General SME/tech focus with productivity, automation, AI metrics

**dynamic_content.py** - `IndustryDynamicStrategy` (real-time data):
- `RestaurantDynamicStrategy` - Subreddits: r/restaurateur, r/KitchenConfidential; Keywords: food, hospitality
- `RealEstateDynamicStrategy` - Subreddits: r/realestate, r/RealEstateInvesting; Keywords: proptech, valuation
- `ComplianceDynamicStrategy` - Subreddits: r/compliance, r/cybersecurity; Keywords: GRC, audit, regtech
- `ConversaDynamicStrategy` - Subreddits: r/customerservice, r/chatbots; Keywords: CX, support, NLP
- `GeneralSMEDynamicStrategy` - Subreddits: r/startups, r/Entrepreneur; Keywords: automation, productivity

Each strategy defines: `get_subreddits()`, `get_keywords()`, `get_base_stats()`, `get_competitors()`, `get_time_insights()`, `get_scenarios()`, `get_hashtag_pools()`

### AI Provider Fallback Chain

1. **OpenAI GPT-3.5** (primary) - `OPENAI_API_KEY`
2. **Anthropic Claude Haiku** (fallback) - `ANTHROPIC_API_KEY`
3. **Groq Llama3** (final fallback) - `GROK_API_KEY` (note: env var is `GROK_API_KEY`, package is `groq`)

### Viral Scoring (viral_predictor.py)

`ViralScore` dataclass with weighted components:
- **Content (30%)** - emotional triggers, power words, CTAs, length (140-200 optimal)
- **Engagement (25%)** - questions, lists, controversy, personal stories
- **Timing (15%)** - peak hours: 8am, 12pm, 5pm, 8pm UTC
- **Hashtags (15%)** - 2-4 optimal, tiered quality scoring
- **Trends (15%)** - alignment with AI/business topics

Auto-optimization triggers below 70/100.

### Engagement Tracking (engagement_tracker.py)

`EngagementTracker` class that persists post history to `post_history.json`:

**Features:**
- Records all posts with metadata (platform, industry, viral score, hashtags)
- Fetches engagement metrics from Twitter API (likes, retweets, replies, impressions)
- Calculates engagement rate and performance tier (viral/high/medium/low)
- Provides analytics insights: best hashtags, posting times, content patterns
- Generates learning context from top performers for AI content generation

**Performance Tiers:**
- `viral`: 5%+ engagement rate
- `high`: 2-5% engagement rate
- `medium`: 0.5-2% engagement rate
- `low`: <0.5% engagement rate

**Analytics Available:**
- Average viral score vs actual engagement correlation
- Best performing hashtags by engagement rate
- Optimal posting times based on historical data
- Content pattern analysis (questions, emojis, numbers, CTAs)
- Recommendations for improvement

## Environment Variables

```bash
# Twitter API (Required)
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=
TWITTER_BEARER_TOKEN=

# AI Providers (at least one required)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GROK_API_KEY=          # Note: uses groq package

# LinkedIn (Optional)
LINKEDIN_ACCESS_TOKEN=
LINKEDIN_ORGANIZATION_ID=

# Product targeting
SME_INDUSTRY=restaurant  # restaurant|compliance|conversa|real_estate|general
```

## GitHub Actions

Workflow: `.github/workflows/sme-social-bot.yml`

**Schedule:**
- 8 AM, 1 PM, 6 PM UTC daily (posting-only, 1 post per run)
- Sunday 8 AM UTC (weekly full engagement)

**Manual dispatch options:**
- Mode: `posting-only`, `full`, `weekly`, `analytics`, `update-engagement`, `viral-test`, `test`
- Industry: `restaurant`, `compliance`, `conversa`, `real_estate`, `general`

**Required secrets:** All Twitter keys, at least one AI provider key.

## Test Structure

Tests in `tests/` directory:
- `test_viral_prediction.py` - Scoring algorithm unit tests
- `test_bot_integration.py` - Mocked API integration tests
- `test_e2e_playwright.py` - Browser automation tests

Output: `./test-results/*.json`

## Key Implementation Notes

1. **One post per run** - Bot generates and posts a single unique tweet per execution to maintain natural posting frequency (changed from batch posting)

2. **Dynamic content priority** - `generate_content()` tries `DynamicContentEngine` first (real sources), falls back to AI generation with `ContentGenerator` prompts

3. **Rate limit handling** - Bot switches to simulation mode when hitting Twitter rate limits, continues tracking stats

4. **LinkedIn adaptation** - Expands hashtags, adds professional context, longer format support

5. **Industry-aware content** - All components (bot, content generators, viral predictor) use `SME_INDUSTRY` to:
   - Generate industry-specific content and prompts
   - Use targeted subreddits for trending topics (r/realestate, r/restaurateur, etc.)
   - Apply industry-specific hashtag tiers for viral optimization
   - Search for relevant posts using industry keywords
   - Generate contextual replies to mentions

6. **Viral optimization per industry** - `ViralTweetPredictor` uses industry-specific:
   - Trending topics (proptech, housing, menu, POS, etc.)
   - Hashtag tiers (#RealEstate, #PropTech, #RestaurantTech, #FoodTech)
   - Content scoring aligned with industry audience

7. **Engagement tracking** - All posts are recorded to `post_history.json` with:
   - Platform, content, viral score, hashtags at time of posting
   - Engagement metrics updated from Twitter API (4h+ after posting)
   - Performance tier classification (viral/high/medium/low)
   - Analytics available via `--analytics` flag or workflow dispatch

8. **Learning from performance** - `EngagementTracker.get_learning_context()` provides:
   - Top performing posts as examples for AI content generation
   - Best hashtags, posting times, and content patterns
   - Recommendations based on historical performance
