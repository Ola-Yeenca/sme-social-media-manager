# 🚀 GitHub Setup Instructions

## Step 1: Create GitHub Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Fill in the details:
   - **Repository name**: `sme-social-media-manager`
   - **Description**: `🚀 Advanced AI-powered social media automation system for SME Analytica. Grows Twitter presence from 8 to 1,000+ followers through strategic content creation, engagement automation, and data-driven optimization.`
   - **Visibility**: Public (or Private if you prefer)
   - **Initialize**: Leave unchecked (we already have files)
5. Click "Create repository"

## Step 2: Push Your Code

After creating the repository, run these commands in your terminal:

```bash
cd /Users/olayinka/sme_social_manager

# Add the GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/sme-social-media-manager.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Verify Deployment

After pushing, verify everything is working:

```bash
# Check cron job is set up
crontab -l

# Test the system
python3 main.py --status

# Run a quick test
python3 main.py --mode=analytics
```

## Step 4: Monitor the System

### Daily Monitoring
```bash
# Check logs
tail -f logs/sme_social_manager.log
tail -f logs/cron.log

# Check system status
python3 main.py --status
```

### Manual Operations
```bash
# Full automation
python3 main.py

# Specific operations
python3 main.py --mode=post        # Just posting
python3 main.py --mode=grow        # Just growth activities
python3 main.py --mode=content     # Just content generation
python3 main.py --mode=analytics   # Just analytics
```

## Step 5: Cron Job Details

Your system is now set to run automatically every day at 8:00 AM:

```bash
# Current cron job
0 8 * * * cd /Users/olayinka/sme_social_manager && /usr/bin/python3 main.py --mode=full --quiet >> logs/cron.log 2>&1
```

### To modify the schedule:
```bash
# Edit cron jobs
crontab -e

# Examples of different schedules:
# Every 6 hours: 0 */6 * * *
# Twice daily (8am, 8pm): 0 8,20 * * *
# Every weekday at 9am: 0 9 * * 1-5
```

## 🎯 What Happens Next

### Automatic Daily Execution
Every day at 8:00 AM, your system will:
1. **Generate 6-12 new posts** with strategic content
2. **Post scheduled content** to Twitter
3. **Engage with target audience** (likes, follows, responses)
4. **Analyze performance** and optimize
5. **Track growth metrics** and save analytics

### Expected Growth Timeline
- **Week 1-2**: 8 → 50 followers (Foundation)
- **Month 1**: 50 → 200 followers (Momentum)
- **Month 2-3**: 200 → 1,000+ followers (Scale)

### Monitoring Your Progress
- **Daily**: Check `logs/cron.log` for automation status
- **Weekly**: Review analytics in `analytics_data/` folder
- **Monthly**: Analyze growth trends and adjust strategy

## 🔧 Troubleshooting

### If automation stops working:
```bash
# Check cron job status
crontab -l

# Check recent logs
tail -20 logs/sme_social_manager.log

# Test manually
python3 main.py --mode=analytics
```

### If you need to stop automation:
```bash
# Remove cron job
crontab -e
# Delete the line with main.py

# Or disable temporarily
crontab -l | sed 's/^/#/' | crontab -
```

### If you need to restart automation:
```bash
# Re-enable cron job
crontab -l | sed 's/^#//' | crontab -
```

## 🎉 Success!

Your SME Analytica Social Media Growth Manager is now:
✅ **Deployed and ready**
✅ **Automated with cron jobs**
✅ **Secured with .gitignore**
✅ **Backed up on GitHub**
✅ **Running daily growth automation**

**Your Twitter account (@smeanalytica) will now grow automatically from 8 to 1,000+ followers!** 🚀
