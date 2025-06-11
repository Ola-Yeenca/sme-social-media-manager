# 🧪 Testing Guide - GitHub Actions & Secrets

## Quick Test Instructions

### 1. **Add GitHub Secrets First**
Go to: https://github.com/Ola-Yeenca/sme-social-media-manager/settings/secrets/actions

Add these secrets:
- `TWITTER_API_KEY`
- `TWITTER_API_SECRET` 
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_TOKEN_SECRET`
- `TWITTER_BEARER_TOKEN`
- `NOTION_API_KEY`
- `SOCIAL_MEDIA_DB_ID`

### 2. **Run Test Workflow**
1. Go to: https://github.com/Ola-Yeenca/sme-social-media-manager/actions
2. Click "Test GitHub Secrets and Environment"
3. Click "Run workflow"
4. Select test mode:
   - `secrets` - Test if all secrets are available
   - `environment` - Test API connections
   - `content` - Test AI content generation
5. Click "Run workflow"

### 3. **What Each Test Does**

#### **Secrets Test:**
- ✅ Verifies all required secrets are available
- ✅ Shows character count (without exposing values)
- ✅ Confirms GitHub Secrets work in cloud

#### **Environment Test:**
- ✅ Tests Twitter API connection
- ✅ Tests Notion API connection  
- ✅ Verifies your @smeanalytica account access
- ✅ Confirms database connectivity

#### **Content Test:**
- ✅ Tests AI content generation
- ✅ Creates real posts in your Notion database
- ✅ Verifies end-to-end functionality

## 🔍 Answers to Your Questions:

### **Q: Will GitHub Actions work without .env file?**
**A: YES!** ✅ 
- GitHub Actions uses **GitHub Secrets**, not your local `.env` file
- Secrets are encrypted and injected as environment variables
- Your `.env` file stays local and protected by `.gitignore`

### **Q: Are we using AI models or hardcoded content?**
**A: AI MODELS!** 🤖
- Fixed the hardcoded content issue
- Now using `ai_content_generator.py` with real AI models
- AI generates content dynamically with SME Analytica context
- Fallback content only for reliability, not primary generation

### **Q: How to test the full workflow?**
**A: Use the test workflow!** 🧪
- Run "Test GitHub Secrets and Environment" workflow
- Test each component individually
- Verify everything works in the cloud

## 🚀 Expected Test Results:

### **✅ Successful Test Output:**
```
🔐 Testing GitHub Secrets...
✅ TWITTER_API_KEY is available (25 chars)
✅ TWITTER_API_SECRET is available (50 chars)
✅ TWITTER_ACCESS_TOKEN is available (50 chars)
✅ TWITTER_ACCESS_TOKEN_SECRET is available (45 chars)
✅ TWITTER_BEARER_TOKEN is available (112 chars)
✅ NOTION_API_KEY is available (50 chars)
✅ SOCIAL_MEDIA_DB_ID is available (36 chars)

🎉 All required secrets are available!

🐦 Testing Twitter API connection...
✅ Twitter API connected successfully
   Account: @smeanalytica
   User ID: 1234567890

📊 Testing Notion API connection...
✅ Notion API connected successfully
   Database: SME Social Media Posts
   Database ID: 20f7ad85-71fa-81f2-a6e6-fa9fda42c74c

🎯 Test Summary:
===============
✅ GitHub Secrets are properly configured
✅ Environment variables are accessible in GitHub Actions
✅ API connections work in cloud environment
✅ Your automation will work 24/7 in the cloud!

🚀 Ready for full automation!
```

### **❌ If Tests Fail:**
- Check that all secrets are added correctly
- Verify secret names match exactly (case-sensitive)
- Ensure API keys are valid and have proper permissions

## 🎯 After Successful Tests:

### **Your automation will:**
1. ✅ **Run daily at 8 AM UTC** - Full automation
2. ✅ **Run every 6 hours** - Posting & engagement  
3. ✅ **Generate AI content** - Dynamic, not hardcoded
4. ✅ **Use SME Analytica context** - Authentic messaging
5. ✅ **Post bilingually** - 70% English, 30% Spanish
6. ✅ **Track everything** - Analytics and performance

### **Monitor Progress:**
- **Actions Tab**: https://github.com/Ola-Yeenca/sme-social-media-manager/actions
- **Twitter**: @smeanalytica for live posts
- **Notion**: Your database for content tracking

## 🔧 Troubleshooting:

### **Common Issues:**
1. **Missing Secrets**: Add all required secrets
2. **Wrong Secret Names**: Must match exactly
3. **Invalid API Keys**: Check permissions and validity
4. **Database Access**: Ensure Notion integration has access

### **How to Debug:**
1. Check workflow logs in Actions tab
2. Look for specific error messages
3. Verify each secret individually
4. Test API connections manually if needed

---

## 🎉 Ready to Test!

**Run the test workflow now to verify everything works!**

1. Add your GitHub Secrets
2. Run "Test GitHub Secrets and Environment" 
3. Watch the magic happen in the cloud! ✨

Your SME Analytica social media will grow automatically with AI-generated, authentic content! 🚀
