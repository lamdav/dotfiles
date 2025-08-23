#!/usr/bin/env python3
"""
Smart pane splitting for kitty - like iTerm2's intelligent splitting
Automatically chooses horizontal vs vertical split based on window dimensions
"""

import subprocess
import json
from typing import Tuple, Optional

class KittySmartSplitter:
    def __init__(self):
        self.min_width = 80   # Minimum characters width for vertical split
        self.min_height = 24  # Minimum lines height for horizontal split
        self.aspect_ratio_threshold = 1.8  # Width/height ratio threshold
    
    def get_current_window_info(self) -> Optional[dict]:
        """Get current window dimensions and info"""
        try:
            result = subprocess.run(
                ["kitty", "@", "ls"], 
                capture_output=True, 
                text=True, 
                check=True
            )
            
            data = json.loads(result.stdout)
            
            # Find the active window and tab
            for window in data:
                for tab in window.get("tabs", []):
                    if tab.get("is_active", False):
                        for pane in tab.get("windows", []):
                            if pane.get("is_active", False):
                                return {
                                    "columns": pane.get("columns", 80),
                                    "lines": pane.get("lines", 24),
                                    "cwd": pane.get("cwd", "")
                                }
            
            return None
            
        except Exception as e:
            print(f"❌ Error getting window info: {e}")
            return None
    
    def should_split_vertically(self, columns: int, lines: int) -> bool:
        """Determine if we should split vertically based on dimensions"""
        aspect_ratio = columns / lines if lines > 0 else 1.0
        
        # Split vertically if:
        # 1. Window is wide enough (more than 2x min width)
        # 2. Aspect ratio is high (wide window)
        # 3. After split, both panes would still be usable
        
        wide_enough = columns > (self.min_width * 2)
        good_aspect_ratio = aspect_ratio > self.aspect_ratio_threshold
        usable_after_split = (columns // 2) >= self.min_width
        
        return wide_enough and good_aspect_ratio and usable_after_split
    
    def should_split_horizontally(self, columns: int, lines: int) -> bool:
        """Determine if we should split horizontally based on dimensions"""
        # Split horizontally if:
        # 1. Window is tall enough (more than 2x min height)
        # 2. After split, both panes would still be usable
        
        tall_enough = lines > (self.min_height * 2)
        usable_after_split = (lines // 2) >= self.min_height
        
        return tall_enough and usable_after_split
    
    def smart_split(self) -> bool:
        """Perform intelligent split based on current window dimensions"""
        window_info = self.get_current_window_info()
        
        if not window_info:
            print("❌ Could not get window information")
            return False
        
        columns = window_info["columns"]
        lines = window_info["lines"]
        cwd = window_info["cwd"]
        
        print(f"📐 Current window: {columns}x{lines} (aspect ratio: {columns/lines:.2f})")
        
        try:
            if self.should_split_vertically(columns, lines):
                # Vertical split (side by side)
                subprocess.run([
                    "kitty", "@", "launch", 
                    "--location=vsplit",
                    "--cwd", cwd
                ], check=True)
                print("↔️  Split vertically (side by side)")
                return True
                
            elif self.should_split_horizontally(columns, lines):
                # Horizontal split (top and bottom)
                subprocess.run([
                    "kitty", "@", "launch", 
                    "--location=hsplit",
                    "--cwd", cwd
                ], check=True)
                print("↕️  Split horizontally (top and bottom)")
                return True
                
            else:
                # Window too small, create new tab instead
                subprocess.run([
                    "kitty", "@", "new-tab",
                    "--cwd", cwd
                ], check=True)
                print("🆕 Window too small for split, created new tab")
                return True
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Error performing split: {e}")
            return False
    
    def force_split(self, direction: str) -> bool:
        """Force split in specified direction"""
        window_info = self.get_current_window_info()
        
        if not window_info:
            print("❌ Could not get window information")
            return False
        
        cwd = window_info["cwd"]
        
        try:
            if direction.lower() in ["v", "vertical", "vsplit"]:
                subprocess.run([
                    "kitty", "@", "launch", 
                    "--location=vsplit",
                    "--cwd", cwd
                ], check=True)
                print("↔️  Forced vertical split")
                
            elif direction.lower() in ["h", "horizontal", "hsplit"]:
                subprocess.run([
                    "kitty", "@", "launch", 
                    "--location=hsplit",
                    "--cwd", cwd
                ], check=True)
                print("↕️  Forced horizontal split")
                
            else:
                print("❌ Invalid direction. Use 'v' or 'h'")
                return False
                
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error performing split: {e}")
            return False

def main():
    import sys
    
    splitter = KittySmartSplitter()
    
    if len(sys.argv) < 2:
        # Default: smart split
        splitter.smart_split()
        return
    
    command = sys.argv[1]
    
    if command == "smart":
        splitter.smart_split()
    
    elif command in ["v", "vertical", "h", "horizontal"]:
        splitter.force_split(command)
    
    elif command == "info":
        window_info = splitter.get_current_window_info()
        if window_info:
            print(f"📐 Window: {window_info['columns']}x{window_info['lines']}")
            print(f"📁 CWD: {window_info['cwd']}")
    
    else:
        print("Usage: smart-split [smart|v|h|info]")
        print("  smart - intelligent split based on window size")
        print("  v     - force vertical split")  
        print("  h     - force horizontal split")
        print("  info  - show current window info")

if __name__ == "__main__":
    main()