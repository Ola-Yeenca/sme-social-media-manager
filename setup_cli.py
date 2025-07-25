#!/usr/bin/env python3
"""
Setup script for SME Analytica CLI
Makes the CLI executable and sets up environment
"""

import os
import sys
import stat
import subprocess

def setup_cli():
    """Setup the CLI tool"""
    
    # Make agent_cli.py executable
    agent_cli_path = "agent_cli.py"
    if os.path.exists(agent_cli_path):
        st = os.stat(agent_cli_path)
        os.chmod(agent_cli_path, st.st_mode | stat.S_IEXEC)
        
        print("✅ Made agent_cli.py executable")
    
    # Install additional dependencies
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements_cli.txt"], 
                      check=True)
        print("✅ Installed CLI dependencies")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Failed to install dependencies: {e}")
        print("You can install manually with: pip install -r requirements_cli.txt")
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    print("✅ Created logs directory")
    
    # Create config directory
    os.makedirs("config", exist_ok=True)
    print("✅ Created config directory")
    
    print("\n🎉 CLI Setup Complete!")
    print("\nUsage:")
    print("  python agent_cli.py --help")
    print("  python agent_cli.py status")
    print("  python agent_cli.py start")
    print("  python agent_cli.py dashboard")

if __name__ == "__main__":
    setup_cli()