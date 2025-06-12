#!/usr/bin/env python3
"""
Script to create a new SME Social Media Posts database in Notion
with the exact structure needed for the automation system
"""

import os
import sys
from dotenv import load_dotenv
from notion_client import Client

# Load environment variables
load_dotenv()

def create_sme_social_media_database():
    """Create a new SME Social Media Posts database with proper structure"""
    
    print("🚀 Creating SME Social Media Posts Database")
    print("=" * 50)
    
    # Initialize Notion client
    api_key = os.getenv('NOTION_API_KEY')
    if not api_key:
        print("❌ NOTION_API_KEY not found in .env file")
        return None
    
    client = Client(auth=api_key)
    print("✅ Notion client initialized")
    
    # Database properties structure
    database_properties = {
        "Name": {
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
                    {"name": "Archived", "color": "red"}
                ]
            }
        },
        "Platform": {
            "select": {
                "options": [
                    {"name": "Twitter", "color": "blue"},
                    {"name": "LinkedIn", "color": "blue"},
                    {"name": "Facebook", "color": "blue"},
                    {"name": "Instagram", "color": "pink"}
                ]
            }
        },
        "Post Type": {
            "select": {
                "options": [
                    {"name": "Promotional", "color": "purple"},
                    {"name": "Informational", "color": "blue"},
                    {"name": "Engagement", "color": "green"},
                    {"name": "Announcement", "color": "orange"}
                ]
            }
        },
        "Scheduled Time": {
            "date": {}
        },
        "Published Time": {
            "date": {}
        },
        "Tags": {
            "multi_select": {
                "options": [
                    {"name": "#SMEAnalytica", "color": "blue"},
                    {"name": "#MenuFlow", "color": "green"},
                    {"name": "#RestaurantTech", "color": "orange"},
                    {"name": "#DataInsights", "color": "purple"},
                    {"name": "#AIforSMEs", "color": "red"},
                    {"name": "#BusinessAnalytics", "color": "yellow"},
                    {"name": "#HospitalityAI", "color": "pink"},
                    {"name": "#DynamicPricing", "color": "brown"}
                ]
            }
        },
        "Tweet ID": {
            "rich_text": {}
        },
        "Engagement Metrics": {
            "rich_text": {}
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
        "Content Theme": {
            "select": {
                "options": [
                    {"name": "data_monday", "color": "blue"},
                    {"name": "talk_tuesday", "color": "green"},
                    {"name": "case_wednesday", "color": "orange"},
                    {"name": "tech_thursday", "color": "purple"},
                    {"name": "fact_friday", "color": "yellow"},
                    {"name": "weekend_insights", "color": "pink"}
                ]
            }
        },
        "AI Provider Used": {
            "rich_text": {}
        }
    }
    
    try:
        # Create the database in the same parent as Local Businesses
        response = client.databases.create(
            parent={
                "type": "page_id",
                "page_id": "20f7ad85-71fa-8021-8720-c787d7c4b388"  # Your SME Social Manager workspace
            },
            title=[
                {
                    "type": "text",
                    "text": {
                        "content": "SME Social Media Posts - Automated"
                    }
                }
            ],
            properties=database_properties
        )
        
        database_id = response["id"]
        database_url = response["url"]
        
        print("✅ Database created successfully!")
        print(f"📊 Database ID: {database_id}")
        print(f"🔗 Database URL: {database_url}")
        
        # Update the .env file with the new database ID
        update_env_file(database_id)
        
        # Create a sample post to test the structure
        create_sample_post(client, database_id)
        
        return database_id
        
    except Exception as e:
        print(f"❌ Failed to create database: {e}")
        return None

def update_env_file(database_id):
    """Update the .env file with the new database ID"""
    print("\n🔧 Updating .env file...")
    
    try:
        # Read current .env file
        with open('.env', 'r') as f:
            lines = f.readlines()
        
        # Update the SOCIAL_MEDIA_DB_ID line
        updated_lines = []
        for line in lines:
            if line.startswith('SOCIAL_MEDIA_DB_ID='):
                updated_lines.append(f'SOCIAL_MEDIA_DB_ID={database_id}\n')
                print(f"✅ Updated SOCIAL_MEDIA_DB_ID to: {database_id}")
            else:
                updated_lines.append(line)
        
        # Write back to .env file
        with open('.env', 'w') as f:
            f.writelines(updated_lines)
        
        print("✅ .env file updated successfully")
        
    except Exception as e:
        print(f"❌ Failed to update .env file: {e}")
        print(f"Please manually update SOCIAL_MEDIA_DB_ID={database_id} in your .env file")

def create_sample_post(client, database_id):
    """Create a sample post to test the database structure"""
    print("\n📝 Creating sample post...")
    
    try:
        response = client.pages.create(
            parent={"database_id": database_id},
            properties={
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": "SME Analytica - Database Test Post"
                            }
                        }
                    ]
                },
                "Content": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "🎉 Welcome to your new SME Social Media Posts database! This automated system will generate high-quality content for SME Analytica with proper branding and proven results. #SMEAnalytica #MenuFlow #AIforSMEs"
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
                "Post Type": {
                    "select": {
                        "name": "Informational"
                    }
                },
                "Language": {
                    "select": {
                        "name": "English"
                    }
                },
                "Content Theme": {
                    "select": {
                        "name": "tech_thursday"
                    }
                },
                "Tags": {
                    "multi_select": [
                        {"name": "#SMEAnalytica"},
                        {"name": "#MenuFlow"},
                        {"name": "#AIforSMEs"}
                    ]
                },
                "AI Provider Used": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Database Creation Script"
                            }
                        }
                    ]
                },
                "Engagement Metrics": {
                    "rich_text": [
                        {
                            "text": {
                                "content": "Test post - Database structure verified"
                            }
                        }
                    ]
                }
            }
        )
        
        print("✅ Sample post created successfully!")
        print(f"📄 Post ID: {response['id']}")
        
    except Exception as e:
        print(f"❌ Failed to create sample post: {e}")

def main():
    """Main function"""
    database_id = create_sme_social_media_database()
    
    if database_id:
        print("\n🎉 SUCCESS! Your new SME Social Media Posts database is ready!")
        print("\nNext steps:")
        print("1. ✅ Database created with proper structure")
        print("2. ✅ .env file updated with new database ID")
        print("3. ✅ Sample post created to verify structure")
        print("4. 🚀 Run: python3 run_automation.py generate")
        print("\nYour SME Analytica social media automation system is now ready to go!")
    else:
        print("\n❌ Failed to create database. Please check the error messages above.")

if __name__ == "__main__":
    main()
