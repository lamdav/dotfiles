# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a comprehensive dotfiles configuration for macOS and Ubuntu development environments. The setup includes modular shell configuration (zsh/), terminal customization (iTerm2/Kitty), window management (AeroSpace), editor setup (vim), status bar (simple-bar), and automated package management via Homebrew (macOS) or APT (Ubuntu).

**Supported Platforms:**
- macOS (full feature set including AeroSpace, Übersicht, iTerm2, system preferences)
- Ubuntu/Debian (core development tools, shell configuration, terminal setup)

## Core Architecture

### Shell Environment (zsh/)
- **Framework**: Oh My Zsh with antidote plugin manager
- **Configuration**: Modular zsh setup with `.zshrc`, `.zsh_plugins`, `.zlogin`, and `.p10k.zsh` in `zsh/` directory
- **Modules**: Split into numbered modules with explicit load order:
  - `01_options.zsh` - Basic zsh options and behavior (no dependencies)
  - `02_environment.zsh` - PATH, FPATH, exports (must set FPATH before compinit)
  - `03_completion.zsh` - Completion system setup (requires FPATH)
  - `04_keybindings.zsh` - Key bindings (requires completion system)
  - `05_lazy-loading.zsh` - Lazy load functions (requires environment)
  - `10_aliases.zsh` - Aliases and functions (requires all tools available)
  - `99_integrations.zsh` - External tools (requires everything else)
- **Theme**: Powerlevel10k with custom configuration (zsh/.p10k.zsh)
- **Performance**: Implements lazy loading for NVM, PyEnv, and Java (JABBA) to maintain fast startup times
- **Plugins**: Managed via zsh/.zsh_plugins file with automatic caching
- **Completions**: Homebrew completions automatically available for all CLI tools

### Package Management (Brewfile)
Manages 25+ CLI tools and development environments including:
- Development tools: git, ripgrep, jq, helm, kubectl
- Language runtimes: go, python, node (via nvm)
- Productivity tools: bat, eza, tldr, tmux
- GUI applications: aerospace, font-fira-code-nerd-font

### Window Management (aerospace/)
AeroSpace configuration with i3-inspired keybindings:
- Workspaces 1-9 plus dedicated workspaces (S=Spotify, F=Finder, M=Mail)
- Custom resize modes and movement commands
- Auto-assignment rules for applications to workspaces
- Integration with simple-bar for real-time workspace updates

### Terminal Configuration (kitty/ & iterm/)
- **Kitty**: Primary terminal with comprehensive configuration in `kitty/kitty.conf`
  - Custom tab bar with process icons
  - Split pane management and session handling
  - Performance optimized with GPU acceleration
- **iTerm2**: Legacy support with profiles in `iterm/iterm-profiles.json`
- **Color scheme**: Firewatch theme applied consistently across terminals
- **Font**: FiraCode Nerd Font with full ligature support

### Status Bar (ubersicht/simple-bar/)
- **simple-bar**: Custom Übersicht widget with Firewatch theme integration
- **Features**: AeroSpace workspace indicators, system metrics, battery, time
- **Styling**: Pill-shaped widgets with consistent color scheme
- **Auto-refresh**: Syncs with AeroSpace workspace changes

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

## Installation Architecture

The installer supports both shell script and Python implementations with a modular, class-based architecture.

### Python Installer (Recommended)
Located in `installer/`, the Python installer provides a clean, modular architecture:

**Core Components:**
- `interfaces.py` - Abstract base classes defining contracts
- `system_manager.py` - OS detection and command execution
- `package_managers.py` - Platform-specific package installation (Homebrew/APT)
- `symlink_manager.py` - Configuration file linking and management
- `macos_manager.py` - macOS-specific operations (AeroSpace, Übersicht, system preferences)
- `dotfiles_installer.py` - Main orchestrator implementing the installation flow
- `main.py` - CLI interface using Typer

**Key Features:**
- **Cross-platform support** - Detects macOS vs Ubuntu and adapts accordingly
- **Interactive command handling** - Properly manages password prompts for brew/sudo commands
- **Modular design** - Each class has a single responsibility
- **Rich output** - Progress indicators, status tables, and colored output
- **Übersicht widget management** - Automatic restart to recognize new widgets

### Shell Installer (Legacy)
The `install.sh` script provides a bash-based installation with similar functionality but less sophisticated error handling.

**System Settings Configuration (macOS Only)**
The installers automatically configure macOS system preferences for optimal development:

- **UI/UX**: Dark mode, auto-hide dock (left side), Finder enhancements (show hidden files, extensions, path bar)
- **Input Devices**: Disable natural scrolling, enable tap-to-click, faster keyboard repeat rates, disable auto-capitalization
- **Developer Tools**: Screenshots to Downloads folder (PNG format, no shadows), battery percentage, font smoothing
- **Security**: Immediate password requirement, firewall enabled, Activity Monitor shows all processes
- **Applications**: TextEdit in plain text mode (Safari preferences skipped due to sandboxing)

### Package Management

**macOS (Homebrew):**
```bash
# Install/update all packages
brew bundle

# Add new package to Brewfile
brew bundle dump --force

# Clean up unused packages
brew bundle cleanup
```

**Ubuntu/Debian (APT):**
```bash
# Update package lists
sudo apt update

# Install development tools
sudo apt install git curl wget python3 nodejs zsh bat ripgrep jq tree tmux

# Upgrade all packages
sudo apt upgrade
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

### Directory Structure and Symlinks
The install.sh script creates symbolic links from organized directories to home:

**Organized Structure:**
```
├── aerospace/          # Window management
│   └── .aerospace.toml
├── git/               # Git configuration  
│   └── .gitconfig
├── iterm/             # iTerm2 profiles and colors
│   ├── iterm-profiles.json
│   └── firewatch.itermcolors
├── kitty/             # Kitty terminal configuration
│   ├── kitty.conf
│   └── kitty-customizations/
├── ubersicht/         # Status bar configuration
│   └── simple-bar/
│       └── simplebarrc
├── vim/               # Vim editor configuration
│   └── .vimrc
└── zsh/               # Modular shell configuration
    ├── .zshrc
    ├── .zsh_plugins
    ├── .zlogin
    ├── .p10k.zsh
    ├── 01_options.zsh
    ├── 02_environment.zsh
    ├── 03_completion.zsh
    ├── 04_keybindings.zsh
    ├── 05_lazy-loading.zsh
    ├── 10_aliases.zsh
    └── 99_integrations.zsh
```

**Symlinks Created:**
- zsh/.zshrc → ~/.zshrc
- git/.gitconfig → ~/.gitconfig  
- zsh/.zsh_plugins → ~/.zsh_plugins
- aerospace/.aerospace.toml → ~/.aerospace.toml
- iterm/iterm-profiles.json → ~/Library/Application Support/iTerm2/DynamicProfiles/
- kitty/kitty.conf → ~/.config/kitty/kitty.conf
- ubersicht/simple-bar/simplebarrc → ~/.simplebarrc
- vim/.vimrc → ~/.vimrc
- zsh/01_*.zsh → ~/.config/zsh/ (all numbered module files)

### Plugin System Flow
1. zsh/.zsh_plugins defines plugin list
2. antidote generates .zsh_plugins.zsh (cached)
3. zsh/.zshrc sources the cached file for performance
4. Plugins are auto-updated when zsh/.zsh_plugins changes

### Modular Zsh Configuration Load Order
1. **Critical Dependencies**: FPATH must be set before compinit, so environment loads before completion
2. **Load Sequence**: 01_options → 02_environment → 03_completion → 04_keybindings → 05_lazy-loading → 10_aliases → 99_integrations
3. **Module Isolation**: Each numbered module is self-contained and focused on specific functionality
4. **Symlink Management**: ~/.config/zsh/ contains symlinks to all numbered zsh modules for easy management
5. **Numbering Convention**: 
   - 01-05: Core system setup (sequential dependencies)
   - 10+: User tools and aliases (flexible spacing for future additions)
   - 99: Final integrations that depend on everything else

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