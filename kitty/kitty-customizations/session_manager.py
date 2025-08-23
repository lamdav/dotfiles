#!/usr/bin/env python3
"""
Kitty session management similar to iTerm2 profiles
Allows saving and restoring window/tab layouts
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Dict, List

class KittySessionManager:
    def __init__(self):
        self.sessions_dir = Path.home() / ".config" / "kitty" / "sessions"
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
    
    def save_session(self, name: str):
        """Save current kitty session layout"""
        try:
            # Get current window and tab info
            result = subprocess.run(
                ["kitty", "@", "ls"], 
                capture_output=True, 
                text=True, 
                check=True
            )
            
            session_data = json.loads(result.stdout)
            session_file = self.sessions_dir / f"{name}.json"
            
            with open(session_file, "w") as f:
                json.dump(session_data, f, indent=2)
            
            print(f"📁 Session '{name}' saved to {session_file}")
            
        except subprocess.CalledProcessError:
            print("❌ Error: Could not communicate with kitty. Make sure remote control is enabled.")
        except Exception as e:
            print(f"❌ Error saving session: {e}")
    
    def load_session(self, name: str):
        """Load and restore a saved session"""
        session_file = self.sessions_dir / f"{name}.json"
        
        if not session_file.exists():
            print(f"❌ Session '{name}' not found")
            return
        
        try:
            with open(session_file, "r") as f:
                session_data = json.load(f)
            
            # Create new OS window for the session
            subprocess.run(["kitty", "@", "new-window"], check=True)
            
            # Restore tabs and their working directories
            for window in session_data:
                for tab in window.get("tabs", []):
                    tab_title = tab.get("title", "")
                    cwd = tab.get("windows", [{}])[0].get("cwd", os.getcwd())
                    
                    subprocess.run([
                        "kitty", "@", "new-tab", 
                        "--tab-title", tab_title,
                        "--cwd", cwd
                    ], check=True)
            
            print(f"✅ Session '{name}' restored")
            
        except Exception as e:
            print(f"❌ Error loading session: {e}")
    
    def list_sessions(self):
        """List all saved sessions"""
        sessions = list(self.sessions_dir.glob("*.json"))
        
        if not sessions:
            print("📝 No saved sessions found")
            return
        
        print("💾 Saved sessions:")
        for session in sessions:
            name = session.stem
            size = session.stat().st_size
            modified = session.stat().st_mtime
            print(f"  • {name} ({size} bytes, modified {modified})")

def main():
    import sys
    
    manager = KittySessionManager()
    
    if len(sys.argv) < 2:
        print("Usage: kitty-session <save|load|list> [session_name]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "save":
        if len(sys.argv) < 3:
            print("Usage: kitty-session save <session_name>")
            sys.exit(1)
        manager.save_session(sys.argv[2])
    
    elif command == "load":
        if len(sys.argv) < 3:
            print("Usage: kitty-session load <session_name>")
            sys.exit(1)
        manager.load_session(sys.argv[2])
    
    elif command == "list":
        manager.list_sessions()
    
    else:
        print("Unknown command. Use: save, load, or list")

if __name__ == "__main__":
    main()