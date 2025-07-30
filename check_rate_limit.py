#!/usr/bin/env python3
"""
Check Twitter API rate limit status
"""

import tweepy
import os
import time
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

print('🕐 TWITTER RATE LIMIT INVESTIGATION')
print('=' * 50)

try:
    client = tweepy.Client(
        bearer_token=os.getenv('TWITTER_BEARER_TOKEN'),
        consumer_key=os.getenv('TWITTER_API_KEY'),
        consumer_secret=os.getenv('TWITTER_API_SECRET'),
        access_token=os.getenv('TWITTER_ACCESS_TOKEN'),
        access_token_secret=os.getenv('TWITTER_ACCESS_TOKEN_SECRET'),
        wait_on_rate_limit=False
    )
    
    try:
        me = client.get_me()
        print('✅ NO RATE LIMIT - API is working!')
        print(f'   Connected as: @{me.data.username}')
        print('   Your bot is ready to run!')
    except tweepy.TooManyRequests as e:
        print('🚨 CONFIRMED: Currently rate limited')
        
        if hasattr(e, 'response') and e.response and e.response.headers:
            headers = e.response.headers
            
            limit_remaining = headers.get('x-rate-limit-remaining', 'unknown')
            limit_reset = headers.get('x-rate-limit-reset', 'unknown') 
            limit_limit = headers.get('x-rate-limit-limit', 'unknown')
            
            print(f'📊 Rate Limit Details:')
            print(f'   Limit: {limit_limit} requests per window')
            print(f'   Remaining: {limit_remaining}')
            print(f'   Reset timestamp: {limit_reset}')
            
            if limit_reset != 'unknown':
                try:
                    reset_timestamp = int(limit_reset)
                    reset_time = datetime.fromtimestamp(reset_timestamp)
                    current_time = datetime.now()
                    
                    print(f'   Reset time: {reset_time}')
                    print(f'   Current time: {current_time}')
                    
                    if reset_time > current_time:
                        time_diff = reset_time - current_time
                        minutes_left = int(time_diff.total_seconds() / 60)
                        seconds_left = int(time_diff.total_seconds() % 60)
                        print(f'   ⏰ Time until reset: {minutes_left}m {seconds_left}s')
                        
                        if minutes_left > 30:
                            print('   🚨 WARNING: This is unusually long!')
                            print('   🔍 Possible causes:')
                            print('     - Multiple apps using same API keys')
                            print('     - Background processes making requests')
                            print('     - API keys compromised/shared')
                            print('     - Twitter API issue')
                        elif minutes_left > 15:
                            print('   ⚠️  Longer than normal 15-minute window')
                        else:
                            print('   ✅ Normal rate limit duration')
                    else:
                        print('   ❌ Rate limit should have reset already!')
                        print('   🔍 This suggests an API issue or stuck state')
                        
                except ValueError as ve:
                    print(f'   ❌ Could not parse reset time: {ve}')
            else:
                print('   ❌ No reset time available in headers')
        else:
            print('   ❌ No rate limit headers available')
            
        print('\n💡 WHAT TO DO:')
        print('1. Wait for the rate limit to reset naturally')
        print('2. Check if you have other Twitter bots/scripts running')
        print('3. Look for background processes using these API keys')
        print('4. If this persists, regenerate your API keys')
        print('5. Check Twitter Developer Portal for any account issues')

except Exception as e:
    print(f'❌ Investigation failed: {e}')
    print('Check your API keys in .env file')