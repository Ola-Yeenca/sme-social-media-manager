# Notion Integration for SME Social Media Manager

This document explains how to use your **Social Media Posts** Notion database as the primary database for the SME Social Media Manager.

## 🎯 Overview

The SME Social Media Manager now integrates directly with your Notion database (`20f7ad8571fa80ea9fe3fa6ba3f484c7`) to:

- **Store all social media posts** in Notion instead of SQLite
- **Track post status** (Draft, Scheduled, Published, Archived)
- **Manage scheduling** with precise timing
- **Monitor engagement** and analytics
- **Link to businesses** from your Local Businesses database

## 🗄️ Database Structure

Your **Social Media Posts** database includes these properties:

| Property | Type | Description |
|----------|------|-------------|
| **Name** | Title | Post title/identifier |
| **Content** | Rich Text | The actual post content |
| **Status** | Select | Draft, Scheduled, Published, Archived |
| **Platform** | Select | Twitter, LinkedIn, Facebook, Instagram |
| **Scheduled Time** | Date | When to publish the post |
| **Published Time** | Date | When it was actually published |
| **Post Type** | Select | Promotional, Informational, Engagement, Announcement |
| **Business** | Relation | Link to Local Businesses database |
| **Engagement Status** | Rich Text | Engagement tracking info |
| **Tags** | Multi-select | Hashtags and categorization |

## 🚀 Quick Start

### 1. Test the Integration

```bash
# Test Notion connection and functionality
python test_notion_integration.py
```

This will:
- ✅ Test Notion API connection
- ✅ Create a sample post
- ✅ Test retrieval and updates
- ✅ Verify all database operations

### 2. Test the Full System

```bash
# Test all components including Notion
python run_with_notion.py test
```

### 3. Generate Sample Content

```bash
# Generate daily content and save to Notion
python run_with_notion.py content
```

### 4. Run Daily Automation

```bash
# Run the complete automation workflow
python run_with_notion.py daily
```

## 📋 Available Commands

| Command | Description |
|---------|-------------|
| `python run_with_notion.py test` | Test all system components |
| `python run_with_notion.py daily` | Run daily automation workflow |
| `python run_with_notion.py content` | Generate sample content |
| `python run_with_notion.py post` | Post scheduled content |

## 🔧 Configuration

### Environment Variables

Make sure your `.env` file contains:

```env
# Notion Configuration
NOTION_API_KEY=your_notion_api_key
SOCIAL_MEDIA_DB_ID=20f7ad8571fa80ea9fe3fa6ba3f484c7
LOCAL_BUSINESSES_DB_ID=1cd7ad8571fa8040ba03e63fcd20872a

# Other required variables...
TWITTER_API_KEY=your_twitter_key
OPENAI_API_KEY=your_openai_key
# etc...
```

### Database Access

Ensure your Notion integration has access to:
1. **Social Media Posts** database (`20f7ad8571fa80ea9fe3fa6ba3f484c7`)
2. **Local Businesses** database (`1cd7ad8571fa8040ba03e63fcd20872a`) - optional

## 🔄 Workflow

### Daily Automation Process

1. **Content Generation**
   - Creates themed content based on day of week
   - Generates posts in multiple languages (English/Spanish)
   - Saves as "Scheduled" status in Notion

2. **Content Publishing**
   - Checks for posts with "Scheduled" status
   - Posts to Twitter when scheduled time arrives
   - Updates status to "Published" with tweet ID

3. **Analytics Tracking**
   - Monitors engagement metrics
   - Updates engagement data in Notion
   - Tracks performance over time

### Content Themes by Day

- **Monday**: Data Monday - Analytics insights
- **Tuesday**: Talk Tuesday - Community engagement
- **Wednesday**: Case Wednesday - Success stories
- **Thursday**: Tech Thursday - Technology features
- **Friday**: Fact Friday - Industry facts
- **Weekend**: General insights

## 📊 Monitoring and Analytics

### View Your Posts

Visit your Notion database to see all posts:
🔗 [Social Media Posts Database](https://www.notion.so/20f7ad8571fa80ea9fe3fa6ba3f484c7)

### Post Status Tracking

- **Draft**: Content created but not scheduled
- **Scheduled**: Ready to post at specified time
- **Published**: Successfully posted to social media
- **Archived**: Older posts for reference

### Engagement Tracking

The system tracks:
- Tweet IDs for published posts
- Engagement metrics (likes, retweets, replies)
- Publishing timestamps
- Performance analytics

## 🛠️ Advanced Usage

### Manual Post Creation

You can manually create posts in Notion:

1. Go to your Social Media Posts database
2. Click "New" to create a post
3. Fill in the required fields:
   - **Name**: Descriptive title
   - **Content**: Your post text
   - **Status**: Set to "Scheduled"
   - **Platform**: Choose "Twitter"
   - **Scheduled Time**: When to post
   - **Post Type**: Select appropriate type

### Business-Specific Content

Link posts to specific businesses from your Local Businesses database:

1. Use the **Business** relation field
2. Select a business from your database
3. The system can generate targeted content for that business

### Custom Scheduling

Set precise posting times:
- Use the **Scheduled Time** field
- The system checks every few minutes for ready posts
- Posts are automatically published when the time arrives

## 🔍 Troubleshooting

### Common Issues

**"Notion API error"**
- Check your `NOTION_API_KEY` in `.env`
- Verify the integration has database access

**"Database not found"**
- Confirm `SOCIAL_MEDIA_DB_ID` is correct
- Ensure database is shared with integration

**"Posts not publishing"**
- Check Twitter API credentials
- Verify post status is "Scheduled"
- Confirm scheduled time has passed

### Debug Mode

Enable detailed logging:

```env
LOG_LEVEL=DEBUG
```

### Test Individual Components

```bash
# Test just Notion integration
python test_notion_integration.py

# Test full system
python run_with_notion.py test
```

## 🔐 Security

- **API Keys**: Store securely in `.env` file
- **Database Access**: Limit integration permissions
- **Content Review**: Monitor generated content
- **Rate Limits**: System respects API limits

## 📈 Benefits of Notion Integration

1. **Visual Management**: See all posts in Notion's interface
2. **Collaboration**: Team members can review/edit posts
3. **Rich Formatting**: Better content organization
4. **Backup**: All data stored in Notion
5. **Flexibility**: Easy to modify post properties
6. **Integration**: Links with your existing business data

## 🎉 Next Steps

1. **Run the test**: `python test_notion_integration.py`
2. **Generate content**: `python run_with_notion.py content`
3. **Check Notion**: View your posts in the database
4. **Schedule automation**: Set up daily runs
5. **Monitor performance**: Track engagement in Notion

Your SME Social Media Manager is now fully integrated with Notion! 🚀
