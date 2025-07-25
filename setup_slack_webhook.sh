#!/bin/bash

# SME Analytica Slack Webhook Setup Script
# This script helps you set up Slack notifications for the GitHub Actions

set -e

echo "🔧 SME Analytica Slack Webhook Setup"
echo "===================================="

# Check if webhook URL is already configured
check_existing() {
    if [ -n "${SLACK_WEBHOOK_URL:-}" ]; then
        echo "✅ Slack webhook already configured: ${SLACK_WEBHOOK_URL:0:50}..."
        return 0
    fi
    return 1
}

# Test the webhook URL
test_webhook() {
    local webhook_url="$1"
    echo "🧪 Testing Slack webhook..."
    
    response=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$webhook_url" \
        -H "Content-Type: application/json" \
        -d '{"text":"🧪 Testing SME Analytica webhook configuration"}')
    
    if [ "$response" = "200" ]; then
        echo "✅ Slack webhook test successful!"
        return 0
    else
        echo "❌ Slack webhook test failed (HTTP $response)"
        return 1
    fi
}

# Main setup function
setup_webhook() {
    if check_existing; then
        if test_webhook "$SLACK_WEBHOOK_URL"; then
            echo "🎯 Webhook already configured and working!"
            return 0
        fi
    fi
    
    echo ""
    echo "📋 To set up Slack notifications:"
    echo "1. Go to your GitHub repository: https://github.com/your-org/sme_social_manager"
    echo "2. Navigate to Settings → Secrets and variables → Actions"
    echo "3. Click 'New repository secret'"
    echo "4. Set the following:"
    echo "   Name: SLACK_WEBHOOK_URL"
    echo "   Value: https://hooks.slack.com/services/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"
    echo ""
    echo "📝 Optional webhook formats:"
    echo "   - WEBHOOK_URL: Generic webhook URL"
    echo "   - SLACK_WEBHOOK_URL: Slack-specific webhook"
    echo ""
    
    read -p "Enter your Slack webhook URL (or press Enter to use the provided one): " webhook_url
    webhook_url=${webhook_url:-"https://hooks.slack.com/services/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"}
    
    if test_webhook "$webhook_url"; then
        echo ""
        echo "✅ Webhook is working! Add this to your GitHub Secrets:"
        echo "Name: SLACK_WEBHOOK_URL"
        echo "Value: $webhook_url"
        echo ""
        echo "🎯 Done! Your GitHub Actions will now notify Slack when automation fails."
    else
        echo "❌ Please check your webhook URL and try again."
    fi
}

# Run the setup
setup_webhook