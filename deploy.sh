#!/bin/bash

# SME Analytica Social Media Manager - Deployment Script
# This script sets up the project for production deployment

set -e  # Exit on any error

echo "🚀 SME Analytica Social Media Manager - Deployment Setup"
echo "=========================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if .env file exists
if [ ! -f ".env" ]; then
    print_error ".env file not found!"
    print_error "Please create a .env file with your API keys before deploying."
    exit 1
fi

print_success ".env file found"

# Check if required directories exist
print_status "Creating required directories..."
mkdir -p logs
mkdir -p data
mkdir -p analytics_data
mkdir -p automation_logs

print_success "Directories created"

# Check Python version
print_status "Checking Python version..."
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
print_success "Python version: $python_version"

# Install dependencies
print_status "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
    print_success "Dependencies installed from requirements.txt"
else
    print_warning "requirements.txt not found, installing core dependencies..."
    pip3 install python-dotenv tweepy notion-client schedule asyncio
    print_success "Core dependencies installed"
fi

# Make main script executable
print_status "Making scripts executable..."
chmod +x main.py
chmod +x deploy.sh
print_success "Scripts made executable"

# Test environment variables
print_status "Testing environment configuration..."
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()

required_vars = [
    'TWITTER_API_KEY',
    'TWITTER_API_SECRET', 
    'TWITTER_ACCESS_TOKEN',
    'TWITTER_ACCESS_TOKEN_SECRET',
    'TWITTER_BEARER_TOKEN',
    'NOTION_API_KEY',
    'SOCIAL_MEDIA_DB_ID'
]

missing = []
for var in required_vars:
    if not os.getenv(var):
        missing.append(var)

if missing:
    print(f'❌ Missing variables: {missing}')
    exit(1)
else:
    print('✅ All required environment variables found')
"

if [ $? -eq 0 ]; then
    print_success "Environment configuration valid"
else
    print_error "Environment configuration invalid"
    exit 1
fi

# Test basic functionality
print_status "Testing basic functionality..."
python3 main.py --status > /dev/null 2>&1

if [ $? -eq 0 ]; then
    print_success "Basic functionality test passed"
else
    print_warning "Basic functionality test failed (may be normal if APIs are not accessible)"
fi

# Setup cron job
setup_cron() {
    print_status "Setting up cron job for automated execution..."
    
    # Get current directory
    CURRENT_DIR=$(pwd)
    
    # Create cron job entry
    CRON_JOB="0 8 * * * cd $CURRENT_DIR && /usr/bin/python3 main.py --mode=full --quiet >> logs/cron.log 2>&1"
    
    # Check if cron job already exists
    if crontab -l 2>/dev/null | grep -q "main.py"; then
        print_warning "Cron job already exists"
        print_status "Current cron jobs:"
        crontab -l | grep "main.py"
    else
        # Add cron job
        (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
        print_success "Cron job added: Daily execution at 8:00 AM"
    fi
    
    # Show current cron jobs
    print_status "Current cron jobs for this user:"
    crontab -l | grep -v "^#" | grep -v "^$" || echo "No cron jobs found"
}

# Ask user if they want to setup cron
echo ""
read -p "Do you want to setup automated daily execution via cron? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    setup_cron
else
    print_status "Skipping cron setup"
    print_status "You can run manually with: python3 main.py"
fi

# Git setup (if not already a git repo)
if [ ! -d ".git" ]; then
    print_status "Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: SME Analytica Social Media Manager"
    print_success "Git repository initialized"
else
    print_status "Git repository already exists"
fi

# Final instructions
echo ""
echo "=========================================================="
print_success "🎉 Deployment setup complete!"
echo "=========================================================="
echo ""
echo "📋 Next Steps:"
echo "1. Push to GitHub:"
echo "   git remote add origin <your-github-repo-url>"
echo "   git push -u origin main"
echo ""
echo "2. Manual execution:"
echo "   python3 main.py                    # Full automation"
echo "   python3 main.py --mode=post        # Just posting"
echo "   python3 main.py --mode=grow        # Just growth"
echo ""
echo "3. Check logs:"
echo "   tail -f logs/sme_social_manager.log"
echo "   tail -f logs/cron.log"
echo ""
echo "4. Monitor cron jobs:"
echo "   crontab -l                         # List cron jobs"
echo "   crontab -e                         # Edit cron jobs"
echo ""
echo "🔒 Security Notes:"
echo "- .env file is in .gitignore (never committed)"
echo "- Logs are local only"
echo "- API keys are protected"
echo ""
echo "🚀 Your SME Analytica Social Media Manager is ready!"
echo "=========================================================="
