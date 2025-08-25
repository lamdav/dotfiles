# lamdav's Dotfiles

A comprehensive dotfiles configuration for macOS and Ubuntu development environments with both interactive Python and traditional bash installers.

## Features

### Core Components
- **Shell Environment**: Modular Zsh configuration with Oh My Zsh framework and Powerlevel10k theme
- **Package Management**: Homebrew (macOS) or APT (Ubuntu) with 25+ development tools and CLI utilities
- **Window Management**: AeroSpace with dedicated workspaces and i3-inspired keybindings (macOS only)
- **Terminal**: Kitty (primary) and iTerm2 (macOS) with Firewatch theme and FiraCode Nerd Font
- **Status Bar**: simple-bar with Übersicht integration and AeroSpace workspace indicators (macOS only)
- **Editor**: Vim configuration optimized for development
- **Git**: Enhanced configuration with custom aliases and delta integration
- **System Preferences**: Automated settings for developer workflow (platform-specific)

### Development Tools Included
- **Language Runtimes**: Node.js (nvm), Python (pyenv), Ruby (rvm), Go, Java (jabba)
- **CLI Tools**: ripgrep, bat, eza, jq, helm, kubectl, k9s, tmux, tldr
- **Git Enhancements**: delta, custom aliases for efficient workflow
- **Performance**: Lazy loading for runtime managers to maintain fast shell startup

## Installation

### Interactive Python Installer (Recommended)

The modern installer provides rich UI, progress indicators, and component selection:

```bash
# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install and run the interactive installer
poetry install
poetry run install-dotfiles

# Check configuration status
poetry run install-dotfiles status

# Non-interactive with options
poetry run install-dotfiles install --skip-system --no-interactive
```

**Available Options:**
- `--skip-packages` - Skip package installation (Homebrew/APT)
- `--skip-shell` - Skip shell configuration (zsh, Oh My Zsh, plugins)
- `--skip-system` - Skip system preferences configuration (macOS only)
- `--no-interactive` - Run without prompts (useful for automation)

### Traditional Bash Installer

For environments without Python/Poetry or automated setups:

```bash
./install.sh
```

The bash installer will automatically suggest the Python installer if Poetry is available.

## Post-Installation

```bash
# Reload shell to apply changes
exec zsh

# Update shell plugins
updateplugins

# Benchmark shell startup time
benchmarkzsh
```

## Configuration Management

### Git Workflow (Custom Aliases)
```bash
git s          # status
git co <branch> # checkout  
git ci         # commit
git l          # log --oneline
git graph      # graphical log with colors
git track <file>   # resume tracking sensitive files
git untrack <file> # stop tracking changes
```

### Development Environment
```bash
# Lazy-loaded tools (auto-initialize on first use)
nvm use <version>    # Node.js management
rvm use <version>    # Ruby management  
pyenv global <version> # Python management
loadjabba           # Java management

# Manual loading if needed
load_nvm
load_pyenv
```

### Package Management

**macOS (Homebrew):**
```bash
# Update all packages
brew bundle

# Add new package to Brewfile
brew bundle dump --force

# Clean unused packages
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

## System Settings Applied

### macOS Configuration
The installer automatically configures macOS for optimal development:

- **UI/UX**: Dark mode, dock auto-hide (left side), Finder enhancements
- **Input**: Disable natural scrolling, faster key repeat, tap-to-click
- **Developer**: Screenshots to Downloads (PNG, no shadows), battery percentage
- **Security**: Immediate password requirement, firewall enabled
- **Applications**: TextEdit plain text mode (Safari preferences skipped due to sandboxing)

### Ubuntu Configuration
On Ubuntu, the installer focuses on development tools and shell configuration:

- **Core Tools**: Git, curl, wget, Python 3, Node.js, build essentials
- **Modern CLI**: bat, ripgrep, jq, tree, tmux for enhanced terminal experience
- **Shell Setup**: Zsh with Oh My Zsh and modular configuration

## Architecture

### Performance Optimizations
- **Lazy Loading**: Runtime managers only load when first accessed
- **Plugin Caching**: Antidote generates static load files for speed
- **Shell Startup**: Optimized to maintain fast startup times (<100ms)

### File Structure
```
.
├── installer/                    # Modular Python CLI installer
│   ├── interfaces.py            # Abstract base classes
│   ├── system_manager.py        # OS detection & command execution
│   ├── package_managers.py      # Homebrew/APT package installation
│   ├── symlink_manager.py       # Configuration file linking
│   ├── macos_manager.py         # macOS-specific operations
│   ├── dotfiles_installer.py    # Main orchestrator
│   └── main.py                  # CLI interface using Typer
├── pyproject.toml               # Poetry configuration  
├── install.sh                   # Bash installer (legacy)
├── brew/                        # Modular package definitions
│   ├── Brewfile.devtools       # Core development tools
│   ├── Brewfile.k8s            # Kubernetes tools
│   ├── Brewfile.media          # Media tools
│   ├── Brewfile.gui            # GUI applications
│   ├── Brewfile.apps           # Applications
│   └── Brewfile.optional       # Optional packages
├── CLAUDE.md                    # AI assistant instructions
│
├── aerospace/                   # Window management (macOS only)
│   └── .aerospace.toml         # AeroSpace configuration
├── git/                         # Git configuration
│   └── .gitconfig              # Git aliases and settings
├── iterm/                       # iTerm2 terminal (macOS only)
│   ├── iterm-profiles.json     # Terminal profiles
│   ├── firewatch.itermcolors   # Color scheme
│   └── steeef-lambda.zsh-theme # Custom zsh theme
├── kitty/                       # Kitty terminal (cross-platform)
│   ├── kitty.conf              # Configuration
│   └── kitty-customizations/   # Extensions and scripts
├── ubersicht/                   # Status bar (macOS only)
│   ├── aerospace-mode.jsx      # AeroSpace mode indicator widget
│   └── simple-bar/
│       ├── simplebarrc         # simple-bar configuration
│       └── aerospace-mode-tracker.sh # Mode tracking script
├── vim/                         # Vim editor
│   └── .vimrc                  # Vim configuration
└── zsh/                         # Modular shell configuration
    ├── .zshrc                  # Main shell config
    ├── .zsh_plugins            # Plugin definitions
    ├── .zlogin                 # Login shell setup
    ├── .p10k.zsh               # Powerlevel10k theme
    ├── 01_options.zsh          # Basic zsh options
    ├── 02_environment.zsh      # Environment variables
    ├── 03_completion.zsh       # Completion system
    ├── 04_keybindings.zsh      # Key bindings
    ├── 05_lazy-loading.zsh     # Performance optimizations
    ├── 10_aliases.zsh          # Command aliases
    └── 99_integrations.zsh     # External integrations
```

## Troubleshooting

### Shell Performance Issues
```bash
benchmarkzsh           # Measure startup time
updateplugins && exec zsh  # Refresh plugins
```

### Missing Tools
```bash
brew bundle check      # Verify installations
poetry run install-dotfiles status  # Check configuration
```

### Git Issues
```bash
git show               # Test delta integration
git ls-alias          # List custom aliases
```

## Requirements

- **Python Installer**: Python 3.10+, Poetry
- **Bash Installer**: macOS/Ubuntu with bash/zsh
- **Supported Systems**: 
  - macOS (tested on latest versions) - Full feature set
  - Ubuntu/Debian (18.04+) - Core development tools and shell configuration

## License

Personal dotfiles configuration - feel free to fork and adapt for your own use.

