# 🚨 SME Analytica Automation Troubleshooting Guide

## Problem: 13:00 Tweet Not Posted

Your automation was supposed to trigger at 13:00 UTC but didn't post. Here's how to fix it:

## 🔧 Immediate Quick Fixes

### 1. Manual Test (Right Now)
```bash
# Test if everything works manually
cd sme_social_manager
python scripts/post_scheduled_content.py --test

# If test passes, try actual posting
python scripts/post_scheduled_content.py
```

### 2. Run Diagnosis Script
```bash
# Run our comprehensive diagnosis
python scripts/automation_fixer.py
```

### 3. Check GitHub Actions
1. Go to your repository on GitHub
2. Click "Actions" tab
3. Look for "Social Media Automation" workflow
4. Check if it ran at 13:00 UTC today
5. If it failed, click on the failed run to see logs

## 🔍 Common Issues & Solutions

### Issue 1: GitHub Workflow Not Triggering

**Check:**
- Is the workflow file in `.github/workflows/social_automation.yml`?
- Is the cron schedule correct: `'0 13 * * *'`?
- Are GitHub Actions enabled for your repository?

**Fix:**
```bash
# Ensure workflow file exists
ls -la .github/workflows/

# If missing, the file should be created automatically
# Check the cron schedule in the file
grep -n "cron" .github/workflows/social_automation.yml
```

### Issue 2: Missing GitHub Secrets

**Required Secrets in GitHub:**
- `NOTION_TOKEN` 
- `NOTION_DATABASE_ID`
- `TWITTER_API_KEY`
- `TWITTER_API_SECRET` 
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_TOKEN_SECRET`
- `TWITTER_BEARER_TOKEN`
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`

**Fix:**
1. Go to GitHub repo > Settings > Secrets and variables > Actions
2. Add all missing secrets
3. Use the exact values from your `.env` file

### Issue 3: Notion Integration Issues

**Check Notion Setup:**
1. Notion integration token is valid
2. Database ID is correct: `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`
3. Integration has access to the database

**Test Notion Connection:**
```bash
# Test Notion connection
python -c "
import asyncio
import os
from src.notion.notion_manager import SMEAnalyticaNotionManager

async def test():
    manager = SMEAnalyticaNotionManager(
        os.getenv('NOTION_TOKEN'),
        os.getenv('NOTION_DATABASE_ID')
    )
    result = await manager.test_connection()
    print('Notion Connection:', 'SUCCESS' if result else 'FAILED')

asyncio.run(test())
"
```

### Issue 4: Twitter API Issues

**Check Twitter Setup:**
- API keys are valid and active
- App has read/write permissions
- Rate limits not exceeded

**Test Twitter Connection:**
```bash
# Test Twitter connection
python -c "
import asyncio
import os
from src.social.twitter_manager import TwitterManager

async def test():
    manager = TwitterManager({
        'api_key': os.getenv('TWITTER_API_KEY'),
        'api_secret': os.getenv('TWITTER_API_SECRET'),
        'access_token': os.getenv('TWITTER_ACCESS_TOKEN'),
        'access_token_secret': os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
        'bearer_token': os.getenv('TWITTER_BEARER_TOKEN')
    })
    info = await manager.get_account_metrics()
    print('Twitter Connection:', 'SUCCESS' if info else 'FAILED')

asyncio.run(test())
"
```

## ⚡ Emergency Manual Posting

If you need to post content immediately:

```bash
# Generate and post content right now
python scripts/run_social_manager.py daily

# Or just post content without full automation
python scripts/run_social_manager.py content
```

## 🎯 Force 13:00 Posting to Work

### Option 1: Manual GitHub Actions Trigger
1. Go to GitHub repo > Actions tab
2. Click "Social Media Automation" workflow
3. Click "Run workflow" button
4. Select "post_now" from dropdown
5. Click "Run workflow"

### Option 2: Fix and Re-run
```bash
# 1. Run the fixer
python scripts/automation_fixer.py

# 2. Commit any fixes
git add .
git commit -m "Fix 13:00 automation issues"
git push

# 3. Manually trigger workflow
# (Use GitHub UI as described above)
```

### Option 3: Local Cron Setup (Backup)
```bash
# Add to your local crontab as backup
crontab -e

# Add this line (adjust path):
0 13 * * * cd /path/to/sme_social_manager && python scripts/post_scheduled_content.py
```

## 🛠️ Environment Setup Verification

### Check .env File
```bash
# Verify all required variables are set
cat .env | grep -E "(NOTION_TOKEN|TWITTER_API|OPENAI_API|ANTHROPIC_API)"
```

### Check Python Dependencies
```bash
# Reinstall dependencies if needed
pip install -r requirements.txt
```

## 📊 Debugging Steps

### 1. Check Logs
```bash
# Look for error logs
tail -f logs/social_manager.log

# Check automation debug log
cat automation_debug.log
```

### 2. Verify System Components
```bash
# Test all components
python scripts/run_social_manager.py test
```

### 3. Generate Test Content
```bash
# Test content generation only
python scripts/run_social_manager.py content
```

## 🚀 Prevention for Future

### Set Up Monitoring
```bash
# Add this to your crontab for daily health checks
0 8 * * * cd /path/to/sme_social_manager && python scripts/automation_fixer.py >> logs/health_check.log 2>&1
```

### GitHub Actions Notifications
Add this to your workflow for failure notifications:
```yaml
- name: Notify on failure
  if: failure()
  run: |
    echo "Automation failed - check logs"
    # Add webhook to Slack/Discord here
```

## 💡 Most Likely Causes (In Order)

1. **GitHub Secrets Missing** - Check repo settings
2. **Workflow File Issues** - Verify cron syntax
3. **API Rate Limits** - Check Twitter/OpenAI usage
4. **Notion Integration** - Verify token and database access
5. **Environment Variables** - Check .env vs GitHub secrets mismatch

## 🆘 Need Immediate Help?

Run this one-liner to get a quick status:

```bash
python scripts/automation_fixer.py && echo "=== QUICK TEST ===" && python scripts/post_scheduled_content.py --test
```

This will diagnose issues and test posting functionality immediately.

---

**Next Steps:**
1. Run the diagnosis script
2. Fix any identified issues  
3. Test manually
4. Check GitHub Actions
5. Set up monitoring for the future

The 13:00 posting should work after following these steps! 🎯
