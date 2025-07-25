# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🎯 Project Overview

**SME Analytica Social Media Manager** - AI-powered social media automation system designed to grow SME Analytica's Twitter presence from 8 to 1,000+ followers through strategic content creation, engagement automation, and data-driven optimization.

## 🚀 Quick Commands

### Core Development Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Run full automation (production mode)
python main.py

# Run specific modes
python main.py --mode=enhanced    # Full AI-powered automation
python main.py --mode=smart       # Intelligent decision making
python main.py --mode=content     # Generate content only
python main.py --mode=engagement  # Run engagement automation
python main.py --mode=analytics   # Run analytics only
python main.py --mode=ai_council  # AI Council collaborative content
python main.py --mode=ai_agent    # Continuous AI monitoring

# Check system status
python main.py --status

# Test locally with .env file
cp .env.example .env  # Edit with your API keys
python main.py --mode=content
```

### GitHub Actions Automation
- **Automatic runs**: Daily at 8 AM UTC + every 6 hours
- **Manual trigger**: Go to Actions → "SME Analytica Social Media Automation" → Run workflow
- **Workflow file**: `.github/workflows/social-media-automation.yml`

## 🔧 Required Environment Variables

### Core API Keys (Required)
```bash
TWITTER_API_KEY=
TWITTER_API_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=
TWITTER_BEARER_TOKEN=
NOTION_API_KEY=
SOCIAL_MEDIA_DB_ID=
```

### Optional AI Providers
```bash
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_GEMINI_API_KEY=
GROK_API_KEY=
PERPLEXITY_API_KEY=
```

### LinkedIn Integration (Optional)
```bash
LINKEDIN_ACCESS_TOKEN=
LINKEDIN_ORGANIZATION_ID=
```

## 🏗️ Architecture Overview

### Core Components
- **main.py**: Entry point with multiple automation modes
- **src/social_media_manager.py**: Enhanced AI-powered content generation
- **src/content/**: Content generation and optimization systems
- **src/engagement/**: Community engagement and automation
- **src/analytics/**: Performance tracking and reporting
- **src/social/**: Twitter and LinkedIn API integrations
- **src/ai_agent/**: Intelligent AI engagement systems
- **src/ai_council/**: Collaborative AI content creation

### Key Systems
- **TwitterManager**: Handles Twitter API interactions
- **LinkedInManager**: Handles LinkedIn API interactions
- **ContentGenerator**: AI-powered content creation
- **EngagementAutomation**: Automated liking, retweeting, following
- **AnalyticsDashboard**: Performance tracking and insights
- **NotionManager**: Content database and analytics storage

### Data Flow
1. **Content Generation**: AI creates viral content based on business context
2. **Multi-platform Posting**: Posts to Twitter and LinkedIn simultaneously
3. **Community Engagement**: Automated engagement with target accounts
4. **Analytics Tracking**: Performance metrics stored in Notion
5. **AI Council**: Collaborative content review and optimization

## 📊 Content Strategy

### Content Pillars
- **Educational (40%)**: Data insights and business tips
- **Community (25%)**: Industry discussions and engagement
- **Promotional (20%)**: Product features and benefits
- **Industry (15%)**: Market trends and insights

### Posting Schedule
- **6-12 posts/day** across platforms
- **Optimal times**: 8 AM, 12 PM, 5 PM, 8 PM UTC (Madrid timezone)
- **4-week growth strategy**: 8 → 50 → 150 → 300 → 500+ followers

## 🎯 Target Audience

**Primary**: Restaurant owners and hospitality managers
**Secondary**: Small business entrepreneurs, retail owners
**Geographic**: Europe (Madrid timezone focus), Spanish/English bilingual

## 📁 Key Files & Directories

```
src/
├── ai_agent/          # Intelligent AI engagement systems
├── ai_council/        # Collaborative AI content creation
├── ai_providers/      # Multiple AI service integrations
├── analytics/         # Performance tracking
├── community/         # Influencer targeting & engagement
├── content/           # Content generation systems
├── engagement/        # Social media engagement automation
├── notion/            # Notion database integration
├── social/            # Twitter/LinkedIn API wrappers
└── strategy/          # Hashtag intelligence & optimization
```

## 🔄 Development Workflow

### Local Development
1. Clone repository
2. Install dependencies: `pip install -r requirements.txt`
3. Create `.env` file with required API keys
4. Test locally: `python main.py --mode=content`
5. Push to GitHub for cloud automation

### Testing
```bash
# Run comprehensive system test
python comprehensive_system_test.py

# Test individual components
python test_hashtag_system.py
python test_engagement.py
python test_workflow.py
```

### Monitoring
- **GitHub Actions**: Check Actions tab for automation runs
- **Logs**: Download from artifacts after each run
- **Analytics**: Check Notion database for performance metrics
- **Twitter**: Monitor @SMEAnalytica for live posts

## 🚨 Troubleshooting

### Common Issues
1. **Missing API keys**: Check GitHub Secrets setup
2. **Rate limiting**: Monitor Twitter API usage in logs
3. **Environment issues**: Ensure all required directories exist
4. **Content validation**: Check content generation logs

### Debug Commands
```bash
# Check environment validation
python main.py --status

# Run with verbose logging
python main.py --mode=content --quiet=false

# Check specific components
python -c "from src.social.twitter_manager import TwitterManager; print('Twitter OK')"
python -c "from src.notion.notion_manager import NotionManager; print('Notion OK')"
```

## 📝 Content Quality Guidelines

- **Voice**: Conversational expert, helpful consultant tone
- **Length**: Twitter (280 chars), LinkedIn (300-500 chars)
- **Hashtags**: 3-5 relevant hashtags per post
- **Languages**: 70% English, 30% Spanish
- **Focus**: Practical value for restaurant/small business owners