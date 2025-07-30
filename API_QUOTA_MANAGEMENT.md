# Twitter API Quota Management

## 🚨 CURRENT SITUATION (July 30, 2025)

**Twitter API Free Tier Limits:**
- ✅ **POSTING:** 500/month (bot uses ~100/month for 3-4 daily posts)
- ❌ **RETRIEVING:** 100/month (EXCEEDED - currently 103/100)

**Reset Date:** August 11, 2025

## 🔧 TEMPORARY SOLUTION: POSTING-ONLY MODE

The bot now automatically runs in posting-only mode until August 11th:

```bash
# Current behavior (auto-detects before Aug 11)
python bot.py  # → Runs in posting-only mode

# Manual override
python bot.py --posting-only  # → Force posting-only mode
```

**What works now:**
- ✅ Posts 3-4 times daily (uses POSTING quota - plenty available)
- ✅ AI content generation with fallbacks
- ✅ GitHub Actions automation

**What's temporarily disabled:**
- ❌ Mention checking (`get_users_mentions`) 
- ❌ Relevant post searching (`search_recent_tweets`)
- ❌ User info retrieval (`get_me`)

## 📊 POST-RESET OPTIMIZATION (After August 11th)

### API Call Budget (100 retrievals/month)

**Current bot functions that use retrieval quota:**

1. **Mention Checking** - `check_mentions()`
   - Calls: `get_me()` + `get_users_mentions()`
   - Cost: **2 retrievals per run**
   - Frequency: 4x daily = **240 retrievals/month** ❌

2. **Post Searching** - `find_relevant_posts()`  
   - Calls: `search_recent_tweets()`
   - Cost: **1 retrieval per run**
   - Frequency: 4x daily = **120 retrievals/month** ❌

3. **User Info** - Bot initialization
   - Calls: `get_me()` (if enabled)
   - Cost: **1 retrieval per run**
   - Frequency: 4x daily = **120 retrievals/month** ❌

**TOTAL CURRENT USAGE: 480 retrievals/month (4.8x over limit!)**

### 🎯 OPTIMIZATION STRATEGY

To stay within 100 retrievals/month, implement these changes:

#### Option A: Reduced Frequency
```bash
# Run full bot only once daily (30 retrievals/month)
# Run posting-only mode other 3 times daily
```

#### Option B: Weekly Engagement
```bash
# Check mentions + search posts only on Sundays (12 retrievals/month)  
# Post-only mode rest of week
```

#### Option C: Alternating Days
```bash
# Odd days: Full functionality (45 retrievals/month)
# Even days: Posting only
```

### 🔧 IMPLEMENTATION NEEDED (After August 11th)

1. **Modify GitHub Workflow:**
   ```yaml
   # Add environment variable to control retrieval functions
   env:
     ENABLE_RETRIEVALS: ${{ github.event.schedule == '0 8 * * 0' }} # Sundays only
   ```

2. **Update bot.py:**
   ```python
   # Check environment variable
   enable_retrievals = os.getenv('ENABLE_RETRIEVALS', 'false').lower() == 'true'
   bot.run_daily_automation(posting_only=not enable_retrievals)
   ```

3. **Alternative: Smart Scheduling**
   ```python
   # Only run retrievals on certain days
   current_day = datetime.now().weekday()
   posting_only = current_day not in [0, 3, 6]  # Mon, Thu, Sun only
   ```

## 📈 RECOMMENDED POST-RESET APPROACH

**Week 1-2 (Test Period):**
- Run full functionality once weekly (Sunday)
- Monitor actual usage in Twitter Developer Portal
- Adjust frequency based on real usage

**Long-term:**
- **Sunday:** Full bot (mentions + search + posting)
- **Mon-Sat:** Posting-only mode
- **Monthly Review:** Check usage and adjust

This gives you:
- 4 full functionality runs = ~12 retrievals/month
- 26 posting-only runs = 0 retrievals
- **Buffer:** 88 retrievals remaining for unexpected usage

## ⚠️ CRITICAL REMINDERS

1. **August 11th Action Required:**
   - Bot will automatically resume full functionality
   - Monitor usage closely first few days
   - Implement optimization if usage spikes again

2. **Developer Portal Monitoring:**
   - Check monthly: https://developer.twitter.com/en/portal/dashboard
   - Set calendar reminder for quota reset dates
   - Watch for 80% usage warnings

3. **Upgrade Path:**
   - Basic Plan ($100/month) = 10,000 retrievals
   - Only needed if optimization doesn't work
   - Consider business ROI vs. cost

## 🚀 CURRENT STATUS

✅ **Bot is production-ready with posting-only mode**  
✅ **Will post 3-4 times daily starting now**  
📅 **Full functionality returns August 11th automatically**  
📋 **Optimization strategy documented for implementation**