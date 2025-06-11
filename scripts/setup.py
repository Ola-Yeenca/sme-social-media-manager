#!/usr/bin/env python3
"""
Setup script for SME Analytica Social Media Manager
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def create_directory_structure():
    """Create necessary directories"""
    directories = [
        "data",
        "logs", 
        "config",
        "src/ai_providers",
        "src/content",
        "src/social",
        "scripts"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def setup_database():
    """Initialize the SQLite database"""
    db_path = "data/social_manager.db"
    
    # Create database and tables
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Posts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id TEXT PRIMARY KEY,
            content TEXT NOT NULL,
            scheduled_time TIMESTAMP NOT NULL,
            posted_time TIMESTAMP,
            language TEXT NOT NULL,
            theme TEXT NOT NULL,
            tweet_id TEXT,
            engagement_metrics TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Engagements table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS engagements (
            id TEXT PRIMARY KEY,
            action_type TEXT NOT NULL,
            target_tweet_id TEXT NOT NULL,
            target_author TEXT NOT NULL,
            content TEXT,
            executed_at TIMESTAMP,
            success BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Analytics table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            posts_created INTEGER DEFAULT 0,
            posts_published INTEGER DEFAULT 0,
            engagements_made INTEGER DEFAULT 0,
            followers_gained INTEGER DEFAULT 0,
            total_reach INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()
    
    print(f"✅ Database initialized: {db_path}")

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    
    return True

def setup_environment_file():
    """Create .env file from template"""
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            import shutil
            shutil.copy(".env.example", ".env")
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env file with your API credentials")
        else:
            print("❌ .env.example not found")
    else:
        print("✅ .env file already exists")

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next Steps:")
    print("1. Edit .env file with your API credentials:")
    print("   - Twitter API credentials")
    print("   - OpenAI API key")
    print("   - Anthropic API key")
    print("   - Perplexity API key (optional)")
    print("   - Grok API key (optional)")
    print("\n2. Test the system:")
    print("   python scripts/run_social_manager.py test")
    print("\n3. Generate sample content:")
    print("   python scripts/run_social_manager.py content")
    print("\n4. Run daily automation:")
    print("   python scripts/run_social_manager.py daily")
    print("\n📚 Documentation: Check the README.md for detailed usage instructions")

def main():
    """Main setup function"""
    print("🚀 Setting up SME Analytica Social Media Manager")
    print("=" * 50)
    
    # Run setup steps
    create_directory_structure()
    setup_database()
    setup_environment_file()
    
    # Install dependencies
    if install_dependencies():
        print("✅ Setup completed successfully")
    
    print_next_steps()

if __name__ == "__main__":
    main()
