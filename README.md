# lamdav's Dotfiles

A comprehensive dotfiles configuration for macOS development environments with both interactive Python and traditional bash installers.

## Features

### Core Components
- **Shell Environment**: Modular Zsh configuration with Oh My Zsh framework and Powerlevel10k theme
- **Package Management**: Homebrew with 25+ development tools and CLI utilities
- **Window Management**: AeroSpace with dedicated workspaces and i3-inspired keybindings
- **Terminal**: Kitty (primary) and iTerm2 with Firewatch theme and FiraCode Nerd Font
- **Status Bar**: simple-bar with Übersicht integration and AeroSpace workspace indicators
- **Editor**: Vim configuration optimized for development
- **Git**: Enhanced configuration with custom aliases and delta integration
- **System Preferences**: Automated macOS settings for developer workflow

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
- `--skip-brew` - Skip Homebrew and package installation
- `--skip-shell` - Skip shell configuration (zsh, Oh My Zsh, plugins)
- `--skip-system` - Skip macOS system preferences configuration
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
```bash
# Update all packages
brew bundle

# Add new package to Brewfile
brew bundle dump --force

# Clean unused packages
brew bundle cleanup
```

## System Settings Applied

The installer automatically configures macOS for optimal development:

- **UI/UX**: Dark mode, dock auto-hide (left side), Finder enhancements
- **Input**: Disable natural scrolling, faster key repeat, tap-to-click
- **Developer**: Screenshots to Downloads (PNG, no shadows), battery percentage
- **Security**: Immediate password requirement, firewall enabled
- **Applications**: TextEdit plain text mode, Safari/Chrome dev tools enabled

## Architecture

### Performance Optimizations
- **Lazy Loading**: Runtime managers only load when first accessed
- **Plugin Caching**: Antidote generates static load files for speed
- **Shell Startup**: Optimized to maintain fast startup times (<100ms)

### File Structure
```
.
├── installer/              # Python CLI installer
├── pyproject.toml         # Poetry configuration  
├── install.sh             # Bash installer
├── Brewfile               # Package definitions
├── steeef-lambda.zsh-theme # Custom zsh theme
├── CLAUDE.md             # AI assistant instructions
│
├── aerospace/            # Window management
│   └── .aerospace.toml   # AeroSpace configuration
├── git/                  # Git configuration
│   └── .gitconfig       # Git aliases and settings
├── iterm/                # iTerm2 terminal
│   ├── iterm-profiles.json # Terminal profiles
│   └── firewatch.itermcolors # Color scheme
├── kitty/                # Kitty terminal (primary)
│   ├── kitty.conf       # Configuration
│   └── kitty-customizations/ # Extensions
├── ubersicht/            # Status bar
│   └── simple-bar/
│       └── simplebarrc  # simple-bar configuration
├── vim/                  # Vim editor
│   └── .vimrc           # Vim configuration
└── zsh/                  # Modular shell configuration
    ├── .zshrc           # Main shell config
    ├── .zsh_plugins     # Plugin definitions
    ├── .zlogin         # Login shell setup
    ├── .p10k.zsh       # Powerlevel10k theme
    ├── aliases.zsh     # Command aliases
    ├── completion.zsh  # Completion system
    ├── environment.zsh # Environment variables
    ├── integrations.zsh # External integrations
    ├── keybindings.zsh # Key bindings
    ├── lazy-loading.zsh # Performance optimizations
    └── options.zsh     # Zsh options
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
- **Bash Installer**: macOS with bash/zsh
- **System**: macOS (tested on latest versions)

## License

Personal dotfiles configuration - feel free to fork and adapt for your own use.

