#!/usr/bin/env python3
"""
Directory-based theme switching for kitty
Changes theme based on current working directory (like iTerm2 automatic profile switching)
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Dict, Optional


class KittyThemeSwitcher:
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "kitty"
        self.themes_config = self.config_dir / "theme_rules.json"

        # Default theme rules - customize these!
        self.default_rules = {
            "/Users/lamdav/work": {
                "theme": "work",
                "colors": {
                    "background": "#1a1a1a",
                    "foreground": "#f0f0f0",
                    "cursor": "#00ff00",
                },
            },
            "/Users/lamdav/personal": {
                "theme": "personal",
                "colors": {
                    "background": "#2d1b69",
                    "foreground": "#f8f8f2",
                    "cursor": "#f92672",
                },
            },
            "/Users/lamdav/configs": {
                "theme": "config",
                "colors": {
                    "background": "#1e2027",  # Current firewatch theme
                    "foreground": "#9ba2b2",
                    "cursor": "#f6f7ed",
                },
            },
        }

        self.load_theme_rules()

    def load_theme_rules(self):
        """Load theme rules from config file"""
        if self.themes_config.exists():
            try:
                with open(self.themes_config, "r") as f:
                    self.rules = json.load(f)
            except Exception as e:
                print(f"Error loading theme config: {e}")
                self.rules = self.default_rules
        else:
            self.rules = self.default_rules
            self.save_theme_rules()

    def save_theme_rules(self):
        """Save current theme rules to config file"""
        try:
            with open(self.themes_config, "w") as f:
                json.dump(self.rules, f, indent=2)
        except Exception as e:
            print(f"Error saving theme config: {e}")

    def get_theme_for_directory(self, directory: str) -> Optional[Dict]:
        """Get theme configuration for a directory"""
        directory = os.path.abspath(directory)

        # Find the longest matching path
        best_match = None
        best_match_length = 0

        for rule_path, theme_config in self.rules.items():
            rule_path = os.path.abspath(rule_path)
            if directory.startswith(rule_path):
                if len(rule_path) > best_match_length:
                    best_match = theme_config
                    best_match_length = len(rule_path)

        return best_match

    def apply_theme(self, theme_config: Dict):
        """Apply theme to current kitty instance"""
        try:
            colors = theme_config.get("colors", {})

            for color_name, color_value in colors.items():
                subprocess.run(
                    ["kitty", "@", "set-colors", f"{color_name}={color_value}"],
                    check=True,
                )

            theme_name = theme_config.get("theme", "custom")
            print(f"🎨 Applied theme: {theme_name}")

        except subprocess.CalledProcessError as e:
            print(f"❌ Error applying theme: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

    def switch_theme_for_current_dir(self):
        """Switch theme based on current working directory"""
        current_dir = os.getcwd()
        theme_config = self.get_theme_for_directory(current_dir)

        if theme_config:
            self.apply_theme(theme_config)
        else:
            print(f"📁 No theme rule for directory: {current_dir}")

    def add_rule(self, directory: str, theme_name: str, colors: Dict[str, str]):
        """Add a new theme rule for a directory"""
        self.rules[directory] = {"theme": theme_name, "colors": colors}
        self.save_theme_rules()
        print(f"✅ Added theme rule for {directory}")

    def list_rules(self):
        """List all theme rules"""
        print("🎨 Theme rules:")
        for directory, config in self.rules.items():
            theme_name = config.get("theme", "unnamed")
            print(f"  📁 {directory} → {theme_name}")


def main():
    import sys

    switcher = KittyThemeSwitcher()

    if len(sys.argv) < 2:
        # Default: switch theme for current directory
        switcher.switch_theme_for_current_dir()
        return

    command = sys.argv[1]

    if command == "switch":
        switcher.switch_theme_for_current_dir()

    elif command == "list":
        switcher.list_rules()

    elif command == "add":
        if len(sys.argv) < 5:
            print(
                "Usage: theme-switcher add <directory> <theme_name> <background_color>"
            )
            sys.exit(1)

        directory = sys.argv[2]
        theme_name = sys.argv[3]
        bg_color = sys.argv[4]

        colors = {"background": bg_color}
        switcher.add_rule(directory, theme_name, colors)

    else:
        print("Usage: theme-switcher [switch|list|add]")


if __name__ == "__main__":
    main()
