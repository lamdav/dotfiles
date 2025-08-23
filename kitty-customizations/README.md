# Kitty Customizations

Enhanced scripts to add iTerm2-like features to kitty terminal.

## Scripts Overview

### 1. 📁 Session Manager (`session_manager.py`)
Save and restore kitty window/tab layouts like iTerm2 profiles.

```bash
python3 session_manager.py save work-setup     # Save current layout
python3 session_manager.py load work-setup     # Restore layout
python3 session_manager.py list                # List saved sessions
```

### 2. 🎨 Theme Switcher (`theme_switcher.py`) 
Automatically switch themes based on current directory.

```bash
python3 theme_switcher.py                      # Switch theme for current dir
python3 theme_switcher.py list                 # Show theme rules
python3 theme_switcher.py add /path theme bg   # Add new rule
```

### 3. ↔️ Smart Split (`smart_split.py`)
Intelligent pane splitting based on window dimensions.

```bash
python3 smart_split.py                         # Auto-choose split direction
python3 smart_split.py v                       # Force vertical split
python3 smart_split.py h                       # Force horizontal split
python3 smart_split.py info                    # Show window dimensions
```

### 4. 🔔 Notifications (`notify.py`)
Monitor commands and send macOS notifications on completion/failure.

```bash
python3 notify.py sleep 5                      # Monitor a command
python3 notify.py --test                       # Test notification
python3 notify.py --jobs                       # Check background jobs
```

### 5. 📊 Status Line (`status_line.py`)
Dynamic window title with git, system load, battery, and time info.

```bash
python3 status_line.py once                    # Update once
python3 status_line.py run                     # Continuous updates
python3 status_line.py config                  # Show configuration
```

### 6. 🎯 Tab Bar (`tab_bar.py`)
Custom tab bar with process-based icons (already configured in kitty.conf).

## Shell Functions

Add these to your `.zshrc` for convenient access:

```bash
# Kitty enhancement functions
ksave() { ~/.config/kitty/kitty-customizations/session_manager.py save "$1"; }
kload() { ~/.config/kitty/kitty-customizations/session_manager.py load "$1"; }
ksplit() { ~/.config/kitty/kitty-customizations/smart_split.py; }
knotify() { ~/.config/kitty/kitty-customizations/notify.py "$@"; }
kstatus() { ~/.config/kitty/kitty-customizations/status_line.py once; }
ktheme() { ~/.config/kitty/kitty-customizations/theme_switcher.py; }
```

## Setup Requirements

1. **Enable kitty remote control** in `kitty.conf`:
   ```
   allow_remote_control yes
   listen_on unix:@mykitty
   ```

2. **For notifications**: macOS with `osascript` (built-in)

3. **For git status**: Git installed and repositories

4. **For battery info**: macOS with `pmset` (built-in)

## Usage Examples

### Workflow Enhancement
```bash
# Save your current development setup
ksave dev-work

# Switch to a different project with auto-theme
cd ~/personal/blog && ktheme

# Smart split for side-by-side editing
ksplit

# Monitor a long-running build
knotify make all

# Restore your work session later
kload dev-work
```

### Automatic Status Updates
```bash
# Add to your shell prompt function or run in background
kstatus run &
```

### Directory-Based Themes
The theme switcher comes with default rules for:
- `/Users/lamdav/work` → Work theme (dark green)
- `/Users/lamdav/personal` → Personal theme (purple) 
- `/Users/lamdav/configs` → Config theme (current Firewatch theme)

Add your own with:
```bash
python3 theme_switcher.py add /path/to/project "project-name" "#1a1a1a"
```

## Integration with kitty.conf

The `tab_bar.py` is already integrated. For other scripts, you can add keybindings:

```
# Smart splitting
map cmd+alt+d launch --type=overlay ~/.config/kitty/kitty-customizations/smart_split.py

# Quick status update  
map cmd+alt+s launch --type=overlay ~/.config/kitty/kitty-customizations/status_line.py once

# Theme switch for current directory
map cmd+alt+t launch --type=overlay ~/.config/kitty/kitty-customizations/theme_switcher.py
```