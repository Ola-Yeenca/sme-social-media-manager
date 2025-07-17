# SME Analytica Engagement Automation System

## Overview

The engagement automation system performs **real social media engagement** including likes, retweets, comments, and responses to grow SME Analytica's social media presence organically.

## What It Actually Does

### 🎯 Real Engagement Actions

1. **Likes** - Automatically likes relevant tweets about restaurant analytics, small business data, and hospitality tech
2. **Retweets with Comments** - Retweets high-value content with thoughtful AI-generated comments
3. **Replies** - Responds to questions and discussions with expert insights
4. **Mention Responses** - Automatically responds to mentions of SME Analytica
5. **🤖 Grok Engagement Farming** - Asks strategic questions to @grok to generate valuable conversations

### 🔍 Smart Opportunity Discovery

The system finds engagement opportunities by searching for:
- `#RestaurantTech`, `#HospitalityTech`, `#SmallBusiness`
- "restaurant analytics", "small business data", "menu optimization"
- "ai for restaurants", "business intelligence", "data driven decisions"
- Posts from restaurant owners, cafe owners, and SME decision makers

### 🤖 AI-Powered Responses

All comments and replies are generated using AI to:
- Maintain SME Analytica's expert voice
- Provide genuine value and insights
- Reference restaurant analytics expertise
- Stay professional but engaging
- Include relevant emojis and data points

### 📊 Analytics & Limits

**Daily Engagement Limits** (to avoid spam):
- Twitter Likes: 50/day
- Twitter Retweets: 20/day  
- Twitter Comments: 15/day
- Twitter Replies: 10/day
- LinkedIn Likes: 30/day
- LinkedIn Comments: 10/day

**Analytics Tracking**:
- All engagement actions saved to Notion database
- Daily/weekly engagement reports
- Opportunity discovery metrics
- Success/failure tracking

## How to Use

### 1. Manual Engagement Run
```bash
python main.py --mode=engagement
```

### 2. Scheduled Engagement (GitHub Actions)
The workflow runs engagement automation at 6:00 PM UTC (evening engagement time):
```bash
# Manually trigger engagement
gh workflow run social_automation.yml -f action=engagement
```

### 3. Test the System
```bash
python test_engagement.py
python test_grok_farming.py  # Test Grok farming specifically
```

## Workflow Integration

### Updated Workflow Behavior

**Before**: The "engagement" option just ran basic content generation (no actual engagement)

**Now**: The "engagement" option runs real engagement automation:

1. **Finds Opportunities** - Searches for relevant tweets and posts
2. **Analyzes Content** - Determines best engagement action (like, retweet, comment)
3. **Takes Action** - Performs actual social media engagement
4. **Responds to Mentions** - Handles @SMEAnalytica mentions
5. **Saves Analytics** - Tracks all actions in Notion database

### Engagement Schedule

- **8:00 AM UTC** - Content generation
- **1:00 PM UTC** - Post scheduled content  
- **6:00 PM UTC** - **ENGAGEMENT AUTOMATION** (new!)

## Safety Features

### Rate Limiting
- Respects Twitter API rate limits
- Built-in delays between actions (2-8 seconds)
- Daily engagement limits prevent spam

### Content Filtering
- Only engages with relevant industry content
- Minimum engagement score thresholds
- Avoids controversial or inappropriate content

### Quality Control
- AI-generated responses reviewed for quality
- Fallback to template responses if AI fails
- Professional tone maintained across all interactions

## 🤖 Grok Engagement Farming

### What It Does
The system strategically asks @grok (Twitter's AI bot) questions about business insights to:
- **Generate conversations** around SME Analytica's expertise areas
- **Attract relevant audience** interested in business analytics
- **Position as thought leaders** in restaurant/SME analytics
- **Create engagement opportunities** when Grok responds

### Strategic Questions
Pre-crafted questions in categories:
- **Restaurant Analytics**: Menu pricing, customer flow, profit optimization
- **SME Insights**: Business intelligence, growth strategies, data analytics
- **Hospitality Tech**: Guest experience, revenue management, booking patterns
- **Data Trends**: AI in business, predictive analytics, automation

### Example Grok Questions
- "What's the biggest mistake restaurants make when analyzing their menu profitability?"
- "How can small businesses compete with enterprise-level analytics without the budget?"
- "What's the most underutilized data source that small businesses have access to?"

### Timing Strategy
- **Morning (8-12)**: Business strategy questions
- **Afternoon (12-17)**: Industry-specific questions
- **Evening (17-22)**: Broader analytics questions

### Safety Limits
- **Maximum 3 questions per day** to avoid spam
- **1-hour minimum** between questions
- **Professional questions only** that add value

## Expected Results

### Engagement Growth
- **50-100 daily engagements** across platforms
- **3-5 strategic Grok conversations** per week
- **Increased visibility** in restaurant/SME communities
- **Organic follower growth** through valuable interactions
- **Brand positioning** as restaurant analytics experts

### Community Building
- **Thought leadership** through expert responses
- **Network expansion** with industry professionals
- **Lead generation** through helpful interactions
- **Brand awareness** in target markets

## Monitoring & Analytics

### Notion Database Tracking
All engagement actions are saved to your Notion database with:
- Action type (like, retweet, comment, reply)
- Target post details
- Our response content
- Success/failure status
- Timestamp and metrics

### Daily Reports
View engagement statistics:
```bash
python main.py --mode=analytics
```

### GitHub Actions Logs
Monitor engagement automation in GitHub Actions:
- Go to Actions tab in your repository
- View "SME Analytica Social Media Automation" runs
- Check logs for engagement details

## Troubleshooting

### No Engagements Happening
1. Check Twitter API credentials in GitHub Secrets
2. Verify daily limits haven't been reached
3. Check logs for API errors
4. Ensure target keywords are finding relevant content

### Too Many/Few Engagements
Adjust limits in `src/engagement/engagement_automation.py`:
```python
self.daily_engagement_limits = {
    'twitter_likes': 50,  # Adjust these numbers
    'twitter_retweets': 20,
    # ...
}
```

### Response Quality Issues
The AI generates contextual responses, but you can customize templates in:
```python
self.response_templates = {
    'supportive_comment': [...],
    'helpful_addition': [...],
    # ...
}
```

## Next Steps

1. **Run a test**: `python test_engagement.py`
2. **Manual engagement**: `python main.py --mode=engagement`
3. **Monitor results** in Notion database
4. **Adjust settings** based on performance
5. **Scale up** engagement limits as audience grows

The engagement automation will now perform **real social media engagement** to grow SME Analytica's presence organically! 🚀
