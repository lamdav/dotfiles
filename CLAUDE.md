# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a comprehensive dotfiles configuration for a macOS development environment. The setup includes shell configuration (zsh), terminal customization (iTerm2), window management (AeroSpace), editor setup (vim), and automated package management via Homebrew.

## Core Architecture

### Shell Environment (.zshrc)
- **Framework**: Oh My Zsh with antidote plugin manager
- **Theme**: Powerlevel10k with custom configuration (.p10k.zsh)
- **Performance**: Implements lazy loading for NVM and PyEnv to maintain fast startup times
- **Plugins**: Managed via .zsh_plugins file with automatic caching in .zsh_plugins.zsh

### Package Management (Brewfile)
Manages 25+ CLI tools and development environments including:
- Development tools: git, ripgrep, jq, helm, kubectl
- Language runtimes: go, python, node (via nvm)
- Productivity tools: bat, eza, tldr, tmux
- GUI applications: aerospace, font-fira-code-nerd-font

### Window Management (.aerospace.toml)
AeroSpace configuration with i3-inspired keybindings:
- Workspaces 1-6 with focused applications
- Custom resize modes and movement commands
- Integration with iTerm2 and browser workflows

### Terminal Configuration
- **iTerm2**: Dynamic profiles via iterm-profiles.json (legacy support)
- **Kitty**: Primary terminal with comprehensive configuration (kitty.conf)
- **Color scheme**: Firewatch theme applied to both iTerm2 and Kitty
- **Font**: FiraCode Nerd Font with ligatures enabled

## Key Commands

### Installation and Setup
```bash
# Initial setup (run from repository root)
./install.sh

# Update shell plugins
updateplugins

# Reload shell configuration
exec zsh

# Benchmark shell startup time
benchmarkzsh
```

**System Settings Configuration**
The install.sh script automatically configures macOS system preferences for optimal development:

- **UI/UX**: Dark mode, auto-hide dock (left side), Finder enhancements (show hidden files, extensions, path bar)
- **Input Devices**: Disable natural scrolling, enable tap-to-click, faster keyboard repeat rates, disable auto-capitalization
- **Developer Tools**: Screenshots to Downloads folder (PNG format, no shadows), battery percentage, font smoothing
- **Security**: Immediate password requirement, firewall enabled, Activity Monitor shows all processes
- **Applications**: TextEdit in plain text mode, Chrome/Safari developer settings enabled

### Package Management
```bash
# Install/update all packages
brew bundle

# Add new package to Brewfile
brew bundle dump --force

# Clean up unused packages
brew bundle cleanup
```

### Git Workflow (Custom Aliases)
```bash
# Quick status and operations
git s          # status
git co <branch> # checkout
git ci         # commit
git l          # log --oneline
git b          # branch

# Advanced logging
git graph      # graphical log with colors
git logp       # compact log with author info

# File tracking (useful for sensitive files)
git track <file>   # resume tracking
git untrack <file> # stop tracking changes
```

### Development Environment Management
```bash
# Lazy-loaded tools (automatically initialize on first use)
nvm use <version>    # Node.js version management
pyenv global <version> # Python version management

# Load tools manually if needed
load_nvm
load_pyenv
loadjabba  # Java version management
```

### Terminal Usage (Kitty)
```bash
# View current terminal shortcuts
kitty-help          # Shows all keybindings from kitty.conf

# Key shortcuts (configured in kitty.conf)
cmd+1-9             # Jump to tab 1-9
cmd+0               # Jump to last tab
cmd+t               # New tab (inherits current directory)
cmd+w               # Close current pane (closes tab when last pane)
cmd+d               # Split pane horizontally
cmd+shift+d         # Split pane vertically
cmd+k               # Clear screen and scrollback

# Font control
cmd+plus/minus      # Increase/decrease font size
cmd+ctrl+0          # Reset font size to default

# Pane management
cmd+shift+w         # Close current pane
cmd+shift+z         # Toggle pane zoom (fullscreen)
```

## File Relationships and Dependencies

### Symlink Architecture
The install.sh script creates symbolic links from this repository to home directory:
- .zshrc → ~/.zshrc
- .gitconfig → ~/.gitconfig
- .zsh_plugins → ~/.zsh_plugins
- .aerospace.toml → ~/.aerospace.toml
- iterm-profiles.json → ~/Library/Application Support/iTerm2/DynamicProfiles/
- kitty.conf → ~/.config/kitty/kitty.conf

### Plugin System Flow
1. .zsh_plugins defines plugin list
2. antidote generates .zsh_plugins.zsh (cached)
3. .zshrc sources the cached file for performance
4. Plugins are auto-updated when .zsh_plugins changes

### Performance Optimizations
- **Conditional loading**: Tools only load when first accessed
- **Plugin caching**: antidote generates static load files
- **PATH consolidation**: Single export instead of multiple appends
- **Completion caching**: zcompdump regenerated daily

## Troubleshooting

### Shell Performance Issues
- Run `benchmarkzsh` to measure startup time
- Uncomment zprof lines in .zshrc for detailed profiling
- Check plugin load times in .zsh_plugins.zsh

### Missing Tools
- Verify Brewfile installations: `brew bundle check`
- Reinstall Oh My Zsh if missing: `rm -rf ~/.oh-my-zsh && ./install.sh`
- Regenerate plugin cache: `updateplugins`

### Kitty Terminal Issues
- Check config syntax: `kitty -c ~/.config/kitty/kitty.conf --version`
- Verify symlink: `ls -la ~/.config/kitty/kitty.conf` should point to dotfiles/kitty.conf
- Reload configuration: `cmd+shift+r` in Kitty or restart Kitty
- Font issues: Ensure FiraCode Nerd Font is installed via Homebrew

### System Settings Not Applied
- Some macOS preferences require restart to take effect
- Applications are automatically restarted during install (Dock, Finder, SystemUIServer)
- For trackpad settings, log out and back in or restart the system
- Check System Preferences to verify settings were applied correctly

### Git Configuration Issues
- Test delta integration: `git show` should display enhanced diffs
- Verify aliases: `git ls-alias` lists all custom commands

## Maintenance

### Regular Updates
```bash
# Update Homebrew packages
brew update && brew upgrade

# Update shell plugins
updateplugins && exec zsh

# Update Oh My Zsh framework
omz update
```

### Adding New Configurations
1. Add files to repository root
2. Update install.sh with appropriate symlinks
3. Test installation on clean environment
4. Update this documentation if needed

## Development Workflow Integration

This configuration optimizes for:
- **Multi-language development**: Supports Node.js, Python, Go, Java
- **Container workflows**: Includes kubectl, helm, k9s
- **Git-heavy workflows**: Enhanced diff viewing and comprehensive aliases
- **Terminal-centric development**: Kitty terminal, vim, tmux, and efficient CLI tools
- **Window management**: AeroSpace for organized workspace layouts
- **Modern terminal features**: Kitty provides GPU acceleration, ligatures, and advanced pane management

## Kitty Terminal Features

### Configuration Highlights
- **Firewatch color scheme** with carefully converted RGB values from iTerm2
- **FiraCode Nerd Font** with full ligature support
- **Dynamic shortcuts help**: `kitty-help` command reads current keybindings
- **Pane management**: Split horizontally (`cmd+d`), vertically (`cmd+shift+d`), close with `cmd+w`
- **Smart tab management**: New tabs inherit current working directory
- **Performance optimized**: GPU acceleration and efficient rendering

### Hotkey Window Setup
For global hotkey access (ctrl+`), create a macOS keyboard shortcut:
1. System Preferences → Keyboard → Shortcuts
2. Add new shortcut with command: `/Applications/kitty.app/Contents/MacOS/kitty --single-instance --instance-group=hotkey`
3. Assign ctrl+` as the keyboard shortcut

The lazy loading system ensures fast shell startup while maintaining access to full development toolchain when needed.