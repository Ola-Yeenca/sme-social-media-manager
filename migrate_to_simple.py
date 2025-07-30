#!/usr/bin/env python3
"""
Migration Script: Complex to Simple System
Safely migrates from complex 50+ file system to simple 8-file system
"""

import os
import shutil
import datetime

def main():
    print("🔄 SME Social Media Manager - Migration to Simple System")
    print("=" * 60)
    
    # 1. Verify backup exists
    if not os.path.exists('backup_complex_system'):
        print("❌ Backup not found! Run backup first.")
        return False
    
    print("✅ Complex system backup verified")
    
    # 2. Test new system
    print("\n🧪 Testing new simplified system...")
    
    try:
        # Test system status
        import subprocess
        result = subprocess.run(['python', 'main_simple.py', '--status'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ New system status check passed")
        else:
            print(f"❌ New system status check failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ New system test failed: {e}")
        return False
    
    # 3. Migration steps
    print("\n🚀 Performing migration...")
    
    try:
        # Replace main.py with simplified version
        if os.path.exists('main.py'):
            shutil.move('main.py', 'backup_complex_system/main_original.py')
        shutil.copy('main_simple.py', 'main.py')
        print("✅ Replaced main.py with simplified version")
        
        # Replace requirements.txt
        if os.path.exists('requirements.txt'):
            shutil.move('requirements.txt', 'backup_complex_system/requirements_original.txt')
        shutil.copy('requirements_simple.txt', 'requirements.txt')
        print("✅ Replaced requirements.txt with minimal dependencies")
        
        # Disable old workflows (rename them)
        workflow_dir = '.github/workflows'
        if os.path.exists(workflow_dir):
            old_workflows = [
                'social-media-automation.yml',
                'ai-council-automation.yml', 
                'ai-agent-continuous.yml'
            ]
            
            for workflow in old_workflows:
                workflow_path = os.path.join(workflow_dir, workflow)
                if os.path.exists(workflow_path):
                    backup_path = os.path.join(workflow_dir, f"{workflow}.disabled")
                    shutil.move(workflow_path, backup_path)
                    print(f"✅ Disabled old workflow: {workflow}")
        
        print("✅ Migration completed successfully!")
        
        # 4. Next steps
        print("\n📋 Next Steps:")
        print("1. Test the new system: python main.py --status")
        print("2. Run a test automation: python main.py --mode=content")
        print("3. Update GitHub secrets to remove unused ones")
        print("4. Monitor the daily-automation.yml workflow")
        print("5. Clean up old files if everything works well")
        
        print(f"\n💾 Backup location: backup_complex_system/")
        print("   ↳ Full complex system backed up for rollback if needed")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        print("🔄 Rolling back changes...")
        rollback()
        return False

def rollback():
    """Rollback to original complex system"""
    print("\n🔄 Rolling back to complex system...")
    
    try:
        # Restore original files
        if os.path.exists('backup_complex_system/main_original.py'):
            shutil.copy('backup_complex_system/main_original.py', 'main.py')
            
        if os.path.exists('backup_complex_system/requirements_original.txt'):
            shutil.copy('backup_complex_system/requirements_original.txt', 'requirements.txt')
        
        # Restore workflows
        workflow_dir = '.github/workflows'
        for file in os.listdir(workflow_dir):
            if file.endswith('.disabled'):
                original_name = file.replace('.disabled', '')
                shutil.move(os.path.join(workflow_dir, file), 
                           os.path.join(workflow_dir, original_name))
        
        print("✅ Rollback completed - complex system restored")
        
    except Exception as e:
        print(f"❌ Rollback failed: {e}")

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)