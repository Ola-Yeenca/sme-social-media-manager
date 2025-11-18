# 🚀 SME Social Media Manager

**AI-powered multi-platform social media automation with viral prediction capabilities**

Automate your Twitter and LinkedIn presence with intelligent content generation, viral prediction, and engagement optimization. Built for SME Analytica to grow followers through data-driven viral content strategies.

[![GitHub Actions](https://img.shields.io/badge/CI-GitHub%20Actions-blue)](https://github.com/Ola-Yeenca/sme-social-media-manager/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ✨ Key Features

- **🤖 Multi-AI Provider Support** - Seamless fallback chain: OpenAI → Anthropic → Groq
- **📊 Viral Prediction System** - Scores content 0-100 and auto-optimizes for maximum engagement
- **🔄 Multi-Platform Posting** - Simultaneous Twitter and LinkedIn with platform-specific optimization
- **🎯 Dynamic Content Generation** - Real-time data from HackerNews, Reddit, and industry trends
- **💬 Smart Engagement** - Automated mention monitoring and intelligent reply generation
- **⚡ Rate Limit Management** - Graceful degradation to simulation mode when limits hit
- **📈 Session Analytics** - Track posts, engagements, viral scores, and API usage
- **🔁 GitHub Actions Automation** - 4x daily posts + weekly full engagement

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Twitter Developer Account with API keys
- At least one AI provider API key (OpenAI, Anthropic, or Groq)
- (Optional) LinkedIn access token for multi-platform posting

### Installation

```bash
# Clone the repository
git clone https://github.com/Ola-Yeenca/sme-social-media-manager.git
cd sme-social-media-manager

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env
# Edit .env with your API keys
```

### Configuration

Create a `.env` file with your API credentials:

```bash
# Twitter API (Required)
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_BEARER_TOKEN=your_bearer_token

# AI Providers (At least one required)
OPENAI_API_KEY=your_openai_key        # Primary
ANTHROPIC_API_KEY=your_anthropic_key  # Fallback 1
GROQ_API_KEY=your_groq_key            # Fallback 2

# LinkedIn (Optional for multi-platform)
LINKEDIN_ACCESS_TOKEN=your_linkedin_token
LINKEDIN_ORGANIZATION_ID=your_org_id
```

### Basic Usage

```bash
# Run in auto mode (smart scheduling)
python bot.py

# Content posting only (saves API quota)
python bot.py --posting-only

# Full engagement mode (mentions + posting)
python bot.py --weekly-engagement

# Multi-platform (Twitter + LinkedIn)
python bot.py --multi-platform

# Test mode (no API calls)
python bot.py --test

# Test viral prediction
python bot.py --viral-test
```

---

## 📖 Documentation

- **[CLAUDE.md](CLAUDE.md)** - Comprehensive project guide for AI assistants
- **[TESTING.md](TESTING.md)** - Testing infrastructure and strategy
- **[README_VIRAL_PREDICTION.md](README_VIRAL_PREDICTION.md)** - Viral prediction system deep dive
- **[API_QUOTA_MANAGEMENT.md](API_QUOTA_MANAGEMENT.md)** - Rate limiting and quota strategies
- **[CHANGELOG.md](CHANGELOG.md)** - Project version history

---

## 🏗️ Architecture

### Core Components

#### **SMESocialBot** (`bot.py`)
Main orchestration class handling:
- Multi-platform content posting
- AI provider fallback chain management
- Rate limiting and quota management
- Intelligent scheduling (daily vs weekly modes)

#### **ViralTweetPredictor** (`viral_predictor.py`)
Predictive content optimization engine:
- Viral scoring algorithm (0-100 scale)
- Analyzes: content quality, timing, hashtags, engagement potential, trends
- Auto-optimization for low-scoring content
- Generates multiple viral variations

#### **LinkedInManager** (`linkedin_manager.py`)
Professional platform integration:
- Twitter-to-LinkedIn content adaptation
- Platform-specific viral optimization
- LinkedIn API handling

#### **DynamicContentEngine** (`dynamic_content.py`)
Real-time content generation:
- Fetches trending topics from HackerNews & Reddit
- Industry statistics and insights
- Time-contextual content strategies

### AI Provider Fallback Chain

```
┌─────────────┐     Fails?     ┌──────────────┐     Fails?     ┌─────────────┐     Fails?     ┌──────────────┐
│   OpenAI    │─────────────────▶  Anthropic   │─────────────────▶    Groq     │─────────────────▶   Fallback   │
│  (Primary)  │                 │ (Fallback 1) │                 │ (Fallback 2)│                 │   Content    │
└─────────────┘                 └──────────────┘                 └─────────────┘                 └──────────────┘
```

---

## 🧪 Testing

### Install Test Dependencies

```bash
pip install -r requirements_test.txt
playwright install chromium  # For E2E tests
```

### Run Tests

```bash
# Run all tests
python run_all_tests.py

# Run specific test suites
python test_viral_prediction.py     # Unit tests
python test_bot_integration.py      # Integration tests
python test_e2e_playwright.py       # End-to-end tests

# Interactive demo
python demo_tests.py
```

### Test Coverage

- **Unit Tests** (`test_viral_prediction.py`) - 50+ tests for viral prediction algorithms
- **Integration Tests** (`test_bot_integration.py`) - Bot workflows with mocked APIs
- **E2E Tests** (`test_e2e_playwright.py`) - Complete workflow validation

See **[TESTING.md](TESTING.md)** for comprehensive testing documentation.

---

## 🤖 GitHub Actions Automation

The bot runs automatically via GitHub Actions:

- **4x Daily** (6 AM, 12 PM, 6 PM, 12 AM UTC) - Posting-only mode
- **Weekly** (Sunday 8 AM UTC) - Full engagement mode (mentions + posting)
- **Manual Trigger** - Run anytime via Actions interface

### Workflow Configuration

Located at `.github/workflows/sme-social-bot.yml`

**Required GitHub Secrets:**
- All environment variables from `.env` above
- Add via: Repository Settings → Secrets and variables → Actions

---

## 📊 Viral Prediction System

### Scoring Algorithm

Content is scored 0-100 based on weighted factors:

| Factor | Weight | Components |
|--------|--------|------------|
| **Content Quality** | 30% | Emotional triggers, power words, CTAs, optimal length |
| **Engagement Potential** | 25% | Questions, lists, personal stories, controversy |
| **Timing** | 15% | Optimal hours (8am, 12pm, 5pm, 8pm UTC) |
| **Hashtags** | 15% | Quality, quantity (2-4 optimal), trending alignment |
| **Trend Alignment** | 15% | AI, business, productivity topic matching |

### Auto-Optimization

When viral scores fall below 70/100, the system automatically:
1. ✅ Adds trending hashtags from tiered quality lists
2. ✅ Includes engagement-driving questions
3. ✅ Optimizes length (140-200 chars Twitter, 300+ LinkedIn)
4. ✅ Adds emotional triggers and power words

### Example Output

```
📊 Viral Prediction Score: 78/100
   Predicted Likes: 24
   Predicted Retweets: 8
   Confidence: 85%

💡 Recommendations:
   - Post during peak hours: 8am, 12pm, 5pm, or 8pm
   - Add emotional triggers (e.g., 'amazing', 'incredible')
```

See **[README_VIRAL_PREDICTION.md](README_VIRAL_PREDICTION.md)** for detailed documentation.

---

## 🎯 Content Strategy

### Target Audience

- **Primary:** Restaurant owners, hospitality managers
- **Secondary:** Small business owners, retail managers
- **Geographic:** Europe (Madrid timezone), Spanish/English bilingual

### Content Focus

- Data-driven business insights
- Restaurant pricing optimization
- Profit margin analysis
- AI and analytics for SMEs
- Industry trends and statistics

### Viral Content Patterns

The system is trained on high-engagement patterns:
- **Questions:** Drive comments and engagement
- **Data/Statistics:** "47% revenue increase", "80% of restaurants..."
- **Professional Insights:** Business tips, industry trends, growth strategies
- **Controversial Opinions:** "Unpopular opinion...", "Hot take..."

---

## 📈 API Quota Management

### Current Strategy

**Daily Mode (Posting-only):**
- 0 API retrievals (mentions, search)
- 3-4 posts per day
- Preserves rate limits for weekly engagement

**Weekly Mode (Sunday):**
- ~12 API retrievals (mentions + search)
- 3-4 posts
- Full engagement with followers

**Rate Limit Handling:**
- Automatic detection of rate limit errors
- Graceful degradation to simulation mode
- Logs all simulated actions for verification

See **[API_QUOTA_MANAGEMENT.md](API_QUOTA_MANAGEMENT.md)** for detailed strategy.

---

## 🛠️ Development

### Project Structure

```
sme-social-media-manager/
├── bot.py                      # Main bot orchestration
├── viral_predictor.py          # Viral prediction engine
├── linkedin_manager.py         # LinkedIn integration
├── dynamic_content.py          # Real-time content generation
├── content_generator.py        # Template-based content
├── config.py                   # Configuration management
├── requirements.txt            # Core dependencies
├── requirements_test.txt       # Test dependencies
├── .github/workflows/
│   └── sme-social-bot.yml      # GitHub Actions workflow
├── test_viral_prediction.py    # Unit tests
├── test_bot_integration.py     # Integration tests
├── test_e2e_playwright.py      # E2E tests
├── run_all_tests.py            # Test runner
├── demo_tests.py               # Interactive demos
└── docs/                       # Additional documentation
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`python run_all_tests.py`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

## 🐛 Troubleshooting

### Common Issues

**Problem:** "No working AI provider available"
- **Solution:** Ensure at least one AI API key (OpenAI, Anthropic, or Groq) is set in `.env`

**Problem:** "Twitter authentication failed"
- **Solution:** Verify all Twitter API credentials are correct and your app has read/write permissions

**Problem:** Rate limit errors
- **Solution:** The bot automatically switches to simulation mode. Check API usage at Twitter Developer Portal

**Problem:** LinkedIn posting fails
- **Solution:** Verify `LINKEDIN_ACCESS_TOKEN` is valid. LinkedIn tokens expire after 60 days

**Problem:** Tests failing
- **Solution:** Run `pip install -r requirements_test.txt` and `playwright install chromium`

### Getting Help

- Check the [CLAUDE.md](CLAUDE.md) for detailed project documentation
- Review [TESTING.md](TESTING.md) for test-related issues
- Open an issue on GitHub for bug reports or feature requests

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenAI** - GPT models for content generation
- **Anthropic** - Claude models for fallback AI
- **Groq** - High-speed inference
- **Tweepy** - Twitter API wrapper
- **Playwright** - E2E testing framework

---

## 📞 Contact

**SME Analytica**
- Twitter: [@smeanalytica](https://twitter.com/smeanalytica)
- LinkedIn: [SME Analytica](https://linkedin.com/company/sme-analytica)
- Website: [smeanalytica.com](https://smeanalytica.com)

---

## 🗺️ Roadmap

- [ ] Instagram integration
- [ ] Advanced sentiment analysis
- [ ] A/B testing for content variations
- [ ] Machine learning model for engagement prediction
- [ ] Analytics dashboard
- [ ] Multi-account management
- [ ] Thread generation for Twitter
- [ ] Video content support

---

**Made with ❤️ for restaurant and SME owners worldwide**
