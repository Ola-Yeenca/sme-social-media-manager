#!/usr/bin/env python3
"""
Setup script to create a new Notion database for SME Social Media Manager
"""

import os
import sys
import json
from datetime import datetime
from notion_client import Client

def create_social_media_database():
    """Create a new Social Media Posts database in Notion"""
    
    # Get Notion API key from environment
    notion_token = os.getenv('NOTION_API_KEY')
    if not notion_token:
        print("❌ NOTION_API_KEY environment variable not set")
        return None
    
    try:
        client = Client(auth=notion_token)
        
        # Database properties schema
        properties = {
            "Title": {
                "title": {}
            },
            "Content": {
                "rich_text": {}
            },
            "Status": {
                "select": {
                    "options": [
                        {"name": "Draft", "color": "gray"},
                        {"name": "Scheduled", "color": "yellow"},
                        {"name": "Published", "color": "green"},
                        {"name": "Failed", "color": "red"}
                    ]
                }
            },
            "Platform": {
                "select": {
                    "options": [
                        {"name": "Twitter", "color": "blue"},
                        {"name": "LinkedIn", "color": "blue"},
                        {"name": "Instagram", "color": "pink"},
                        {"name": "Facebook", "color": "blue"}
                    ]
                }
            },
            "Theme": {
                "select": {
                    "options": [
                        {"name": "Data Monday", "color": "blue"},
                        {"name": "Talk Tuesday", "color": "green"},
                        {"name": "Case Wednesday", "color": "orange"},
                        {"name": "Tech Thursday", "color": "purple"},
                        {"name": "Fact Friday", "color": "yellow"},
                        {"name": "Weekend Insights", "color": "gray"}
                    ]
                }
            },
            "Language": {
                "select": {
                    "options": [
                        {"name": "English", "color": "blue"},
                        {"name": "Spanish", "color": "red"},
                        {"name": "French", "color": "green"}
                    ]
                }
            },
            "Scheduled Time": {
                "date": {}
            },
            "Posted Time": {
                "date": {}
            },
            "Hashtags": {
                "multi_select": {
                    "options": [
                        {"name": "#SMEAnalytica", "color": "blue"},
                        {"name": "#AIforSMEs", "color": "green"},
                        {"name": "#DataInsights", "color": "orange"},
                        {"name": "#SmallBusiness", "color": "purple"},
                        {"name": "#RestaurantTech", "color": "red"},
                        {"name": "#MenuFlow", "color": "yellow"}
                    ]
                }
            },
            "Engagement Score": {
                "number": {
                    "format": "number"
                }
            },
            "Viral Score": {
                "number": {
                    "format": "number"
                }
            },
            "Tweet ID": {
                "rich_text": {}
            },
            "Created": {
                "created_time": {}
            },
            "Last Edited": {
                "last_edited_time": {}
            }
        }
        
        # Create the database
        new_database = client.databases.create(
            parent={
                "type": "page_id",
                "page_id": "20f7ad8571fa80218720c787d7c4b388"  # Your workspace page
            },
            title=[
                {
                    "type": "text",
                    "text": {
                        "content": "SME Social Media Posts - New"
                    }
                }
            ],
            properties=properties
        )
        
        database_id = new_database['id']
        print(f"✅ Created new Notion database!")
        print(f"📋 Database ID: {database_id}")
        print(f"🔗 Database URL: https://notion.so/{database_id.replace('-', '')}")
        
        # Create a sample post to test the database
        sample_post = client.pages.create(
            parent={"database_id": database_id},
            properties={
                "Title": {
                    "title": [
                        {
                            "text": {
                                "content": "Welcome to SME Analytica Social Media Automation!"
                            }
                        }
                    ]
                },
                "Content": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "🚀 SME Analytica's AI-driven analytics help restaurants boost margins by 10% with dynamic pricing. Ready to transform your business? #SMEAnalytica #AIforSMEs #RestaurantTech"
                            }
                        }
                    ]
                },
                "Status": {
                    "select": {
                        "name": "Draft"
                    }
                },
                "Platform": {
                    "select": {
                        "name": "Twitter"
                    }
                },
                "Theme": {
                    "select": {
                        "name": "Data Monday"
                    }
                },
                "Language": {
                    "select": {
                        "name": "English"
                    }
                },
                "Hashtags": {
                    "multi_select": [
                        {"name": "#SMEAnalytica"},
                        {"name": "#AIforSMEs"},
                        {"name": "#RestaurantTech"}
                    ]
                },
                "Viral Score": {
                    "number": 8.5
                }
            }
        )
        
        print(f"✅ Created sample post: {sample_post['id']}")
        
        return database_id
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return None

def main():
    """Main function"""
    print("🔧 Setting up new Notion database for SME Social Media Manager...")
    
    database_id = create_social_media_database()
    
    if database_id:
        print("\n🎉 Setup complete!")
        print(f"📝 Add this to your GitHub Secrets:")
        print(f"   SOCIAL_MEDIA_DB_ID = {database_id}")
        print(f"\n🔗 Database URL: https://notion.so/{database_id.replace('-', '')}")
        
        # Save to a config file for reference
        config = {
            "database_id": database_id,
            "created_at": datetime.now().isoformat(),
            "database_url": f"https://notion.so/{database_id.replace('-', '')}"
        }
        
        with open('notion_database_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"💾 Configuration saved to: notion_database_config.json")
    else:
        print("❌ Failed to create database")
        sys.exit(1)

if __name__ == "__main__":
    main()
