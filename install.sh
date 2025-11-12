#!/usr/bin/env bash
set -euo pipefail

export dir="$(pwd)"

# Detect operating system (macOS or Ubuntu)
detect_os() {
    case "$(uname -s)" in
        Darwin*)
            echo "macos"
            ;;
        Linux*)
            # Assume Ubuntu/Debian for Linux systems
            echo "ubuntu"
            ;;
        *)
            echo "unsupported"
            ;;
    esac
}

OS=$(detect_os)
echo "Detected OS: $OS"

# Package management based on OS
install_packages() {
    case "$OS" in
        macos)
            # Check if Homebrew is installed, install if not
            if ! command -v brew &> /dev/null; then
                echo "Installing Homebrew..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi

            # Update and install packages
            echo "Updating Homebrew and installing packages..."
            brew update

            # Install packages from modular Brewfiles
            echo "Installing development tools..."
            [ -f brew/Brewfile.devtools ] && brew bundle --file=brew/Brewfile.devtools

            echo "Installing Kubernetes tools..."
            [ -f brew/Brewfile.k8s ] && brew bundle --file=brew/Brewfile.k8s

            echo "Installing media tools..."
            [ -f brew/Brewfile.media ] && brew bundle --file=brew/Brewfile.media

            echo "Installing GUI applications..."
            [ -f brew/Brewfile.gui ] && brew bundle --file=brew/Brewfile.gui

            echo "Installing applications..."
            [ -f brew/Brewfile.apps ] && brew bundle --file=brew/Brewfile.apps

            echo "Optional packages available in brew/Brewfile.optional (run manually if desired)"
            ;;
        ubuntu)
            echo "Installing packages for Ubuntu/Debian..."
            sudo apt update
            
            # Core development tools
            sudo apt install -y git git-lfs curl wget python3 python3-pip nodejs npm zsh
            sudo apt install -y bat ripgrep jq tree tmux rsync coreutils
            
            # Install exa (eza alternative for older Ubuntu versions)
            if ! command -v eza &> /dev/null; then
                sudo apt install -y exa || echo "exa not available, skipping"
            fi
            
            echo "Note: Some macOS-specific apps (Aerospace, Kitty GUI apps) are not available on Linux"
            ;;
        unsupported)
            echo "Error: Unsupported OS detected."
            echo "This installer only supports macOS and Ubuntu/Debian systems."
            exit 1
            ;;
    esac
}

# Install packages based on detected OS
install_packages


# Install Oh My Zsh if not present
if [ ! -d "$HOME/.oh-my-zsh" ]; then
    echo "Installing Oh My Zsh..."
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
fi
# Create symbolic links for shell configuration
echo "Setting up shell configuration..."
ln -sf "$dir/zsh/.zshrc" ~/.zshrc
ln -sf "$dir/zsh/.zsh_plugins" ~/.zsh_plugins
[ -f "$dir/zsh/.zlogin" ] && ln -sf "$dir/zsh/.zlogin" ~/.zlogin
mkdir -p ~/.oh-my-zsh/custom/themes
ln -sf "$dir/steeef-lambda.zsh-theme" ~/.oh-my-zsh/custom/themes/steeef-lambda.zsh-theme
[ -f "$dir/zsh/.p10k.zsh" ] && ln -sf "$dir/zsh/.p10k.zsh" ~/.p10k.zsh

# Link modular zsh configuration
mkdir -p ~/.config/zsh
if [ -d "$dir/zsh" ]; then
    for config_file in "$dir/zsh"/*.zsh; do
        [ -f "$config_file" ] && ln -sf "$config_file" ~/.config/zsh/
    done
fi

# Setup vim configuration
if [ -f "$dir/vim/.vimrc" ]; then
    echo "Setting up vim configuration..."
    ln -sf "$dir/vim/.vimrc" ~/.vimrc
fi

# Setup Aerospace configuration
if [ -f "$dir/aerospace/.aerospace.toml" ]; then
    echo "Setting up Aerospace configuration..."
    ln -sf "$dir/aerospace/.aerospace.toml" ~/.aerospace.toml
fi

# Setup git configuration
echo "Setting up git configuration..."
ln -sf "$dir/git/.gitconfig" ~/.gitconfig

# Setup terminal configurations
if [ -f "$dir/kitty/kitty.conf" ]; then
    echo "Setting up Kitty configuration..."
    mkdir -p ~/.config/kitty
    ln -sf "$dir/kitty/kitty.conf" ~/.config/kitty/kitty.conf
    
    # Link kitty customizations directory
    if [ -d "$dir/kitty/kitty-customizations" ]; then
        ln -sf "$dir/kitty/kitty-customizations" ~/.config/kitty/kitty-customizations
    fi
fi

# macOS-specific configurations
if [ "$OS" = "macos" ]; then
    # Setup iTerm2 profile and colors (macOS only)
    if [ -f "$dir/iterm/iterm-profiles.json" ]; then
        echo "Setting up iTerm2 profile..."
        mkdir -p ~/Library/Application\ Support/iTerm2/DynamicProfiles
        ln -sf "$dir/iterm/iterm-profiles.json" ~/Library/Application\ Support/iTerm2/DynamicProfiles/iterm-profiles.json
    fi

    # Setup Kitty quick-access-terminal (hotkey window)
    if command -v kitten &> /dev/null; then
        echo "Registering Kitty quick-access-terminal..."
        # Run once to register the service with macOS
        kitten quick-access-terminal &
        sleep 2
        # Kill the window that was just opened
        pkill -f "quick-access-terminal" 2>/dev/null || true

        echo "✅ Kitty quick-access-terminal registered"
        echo "   To complete setup:"
        echo "   1. Open System Settings → Keyboard → Keyboard Shortcuts → Services"
        echo "   2. Scroll to 'General' section and find 'Quick access to kitty'"
        echo "   3. Check the box to enable it"
        echo "   4. Click 'Add Shortcut' and press: Ctrl + \` (Control + backtick)"
    fi

    # Configure macOS system preferences for optimal development environment
    echo "Configuring macOS system preferences..."

# UI/UX Settings - Dark mode, dock behavior, and Finder preferences
echo "Setting up UI/UX preferences..."
# Enable dark mode
defaults write NSGlobalDomain AppleInterfaceStyle -string "Dark"
# Auto-hide dock and reduce dock size
defaults write com.apple.dock autohide -bool true
defaults write com.apple.dock tilesize -int 48
defaults write com.apple.dock magnification -bool false
# Move dock to left side for more vertical screen space
defaults write com.apple.dock orientation -string "left"
# Show all filename extensions in Finder
defaults write NSGlobalDomain AppleShowAllExtensions -bool true
# Show hidden files in Finder
defaults write com.apple.finder AppleShowAllFiles -bool true
# Show path bar in Finder
defaults write com.apple.finder ShowPathbar -bool true
# Show status bar in Finder
defaults write com.apple.finder ShowStatusBar -bool true
# Use list view in all Finder windows by default
defaults write com.apple.finder FXPreferredViewStyle -string "Nlsv"
# Disable the warning when changing a file extension
defaults write com.apple.finder FXEnableExtensionChangeWarning -bool false

# Input Device Settings - Trackpad and keyboard optimizations for productivity
echo "Configuring input device settings..."
# Disable natural scrolling (more familiar for developers coming from other platforms)
defaults write NSGlobalDomain com.apple.swipescrolldirection -bool false
# Enable tap to click on trackpad
defaults write com.apple.driver.AppleBluetoothMultitouch.trackpad Clicking -bool true
defaults write NSGlobalDomain com.apple.mouse.tapBehavior -int 1
# Enable three finger drag
defaults write com.apple.driver.AppleBluetoothMultitouch.trackpad TrackpadThreeFingerDrag -bool true
# Increase keyboard repeat rate for faster coding
defaults write NSGlobalDomain KeyRepeat -int 2
defaults write NSGlobalDomain InitialKeyRepeat -int 15
# Disable automatic capitalization and smart quotes (annoying for code)
defaults write NSGlobalDomain NSAutomaticCapitalizationEnabled -bool false
defaults write NSGlobalDomain NSAutomaticQuoteSubstitutionEnabled -bool false
defaults write NSGlobalDomain NSAutomaticDashSubstitutionEnabled -bool false

# Developer-focused Settings - Screenshots, text editing, and terminal enhancements
echo "Configuring developer-focused settings..."
# Change screenshot location to Downloads folder
defaults write com.apple.screencapture location -string "${HOME}/Downloads"
# Change screenshot format to PNG (better for documentation)
defaults write com.apple.screencapture type -string "png"
# Disable drop shadow in screenshots
defaults write com.apple.screencapture disable-shadow -bool true
# Enable full keyboard access for all controls (important for accessibility and keyboard navigation)
defaults write NSGlobalDomain AppleKeyboardUIMode -int 3
# Hide menu bar (since simple-bar provides all info)
defaults write NSGlobalDomain _HIHideMenuBar -bool true
# Show battery percentage in menu bar (for fallback when simple-bar isn't running)
defaults write com.apple.menuextra.battery ShowPercent -string "YES"
# Enable font smoothing for external monitors
defaults write NSGlobalDomain AppleFontSmoothing -int 2

# Security and Privacy Settings - Enhanced security for development work
echo "Configuring security and privacy settings..."
# Require password immediately after sleep or screen saver begins
defaults write com.apple.screensaver askForPassword -int 1
defaults write com.apple.screensaver askForPasswordDelay -int 0
# Show all processes in Activity Monitor
defaults write com.apple.ActivityMonitor ShowCategory -int 0
# Enable firewall
sudo defaults write /Library/Preferences/com.apple.alf globalstate -int 1

# Application-specific Settings - Configure apps for development workflow
echo "Configuring application-specific settings..."
# TextEdit: Use plain text mode by default
defaults write com.apple.TextEdit RichText -int 0
# TextEdit: Open and save files as UTF-8
defaults write com.apple.TextEdit PlainTextEncoding -int 4
defaults write com.apple.TextEdit PlainTextEncodingForWrite -int 4
# Chrome: Disable the all too sensitive backswipe on trackpads
defaults write com.google.Chrome AppleEnableSwipeNavigateWithScrolls -bool false
# Note: Safari preferences are skipped due to sandboxing restrictions in modern macOS
# To enable Safari developer menu, go to Safari > Preferences > Advanced > Show Develop menu

# Restart affected applications to apply changes
echo "Restarting applications to apply changes..."
killall Dock 2>/dev/null || true
killall Finder 2>/dev/null || true
killall SystemUIServer 2>/dev/null || true

echo "\nDotfiles installation complete!"
echo "System preferences have been configured for optimal development workflow."
echo "Run 'exec zsh' to reload your shell."
echo "You may need to restart iTerm2 to see the new profile."
echo "If using Kitty, your configuration has been linked to ~/.config/kitty/kitty.conf"

    # Setup simple-bar configuration (macOS only)
    if [ -f "$dir/ubersicht/simple-bar/simplebarrc" ]; then
        echo "Setting up simple-bar configuration..."
        ln -sf "$dir/ubersicht/simple-bar/simplebarrc" ~/.simplebarrc
    fi

    # Optional: Set up Übersicht and simple-bar (macOS only)
    echo ""
    read -p "Would you like to set up Übersicht and simple-bar with Firewatch theme? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Check if Übersicht is installed, install if needed
    if ! ls /Applications/ | grep -i "übersicht\\|uebersicht" > /dev/null; then
        echo "📥 Übersicht not found. Installing via Homebrew..."
        
        if command -v brew &> /dev/null; then
            brew install --cask ubersicht
            echo "✅ Übersicht installed successfully"
        else
            echo "❌ Homebrew not found. Please install Homebrew first or download Übersicht manually"
            echo "   Manual download: https://tracesof.net/uebersicht/"
            exit 1
        fi
    fi

    # Check if simple-bar is installed
    SIMPLE_BAR_DIR="$HOME/Library/Application Support/Übersicht/widgets/simple-bar"
    if [ ! -d "$SIMPLE_BAR_DIR" ]; then
        echo "📥 Simple-bar not found. Installing..."
        
        # Create widgets directory if it doesn't exist
        mkdir -p "$(dirname "$SIMPLE_BAR_DIR")"
        
        # Clone simple-bar
        if command -v git &> /dev/null; then
            git clone https://github.com/Jean-Tinland/simple-bar "$SIMPLE_BAR_DIR"
            echo "✅ Simple-bar installed successfully"
        else
            echo "❌ Git not found. Please install git or download simple-bar manually"
            exit 1
        fi
    fi

    # Restart Übersicht to recognize new widgets
    echo "🔄 Restarting Übersicht to recognize new widgets..."
    pkill -f Übersicht 2>/dev/null || true
    sleep 2
    open -a Übersicht 2>/dev/null || {
        echo "⚠️  Could not restart Übersicht automatically. Please:"
        echo "   1. Force-quit Übersicht (if running)"
        echo "   2. Reopen Übersicht"
    }
    echo "✅ Übersicht restarted. New widgets should now be visible."

    # Setup aerospace-mode widget symlink
    echo "Setting up AeroSpace mode indicator widget..."
    WIDGETS_DIR="$HOME/Library/Application Support/Übersicht/widgets"
    mkdir -p "$WIDGETS_DIR"
    
    # Remove any existing aerospace-mode.jsx file
    rm -f "$WIDGETS_DIR/aerospace-mode.jsx"
    
    # Create symlink to dotfiles version
    ln -sf "$dir/ubersicht/aerospace-mode.jsx" "$WIDGETS_DIR/aerospace-mode.jsx"
    echo "✅ AeroSpace mode widget linked successfully"

    # Setup completion
    echo "✅ Simple-bar setup complete!"
    echo ""
    echo "📋 Configuration Summary:"
    echo "   • Theme: Firewatch Custom (matches your terminal)"
    echo "   • Colors: Dark theme with cyan accents (#44a8b6)"
    echo "   • Font: FiraCode Nerd Font (matches your terminal)"
    echo "   • Widgets: Spaces, App, Clock, Battery, System Info"
    echo "   • AeroSpace: Auto-refresh on workspace changes"
    echo "   • AeroSpace Mode Indicator: Shows current mode (main/media/resize/service)"
fi

    echo "Some macOS changes may require a system restart to take full effect."
fi

echo "Dotfiles installation complete!"
if [ "$OS" = "macos" ]; then
    echo "System preferences have been configured for optimal development workflow."
    echo "You may need to restart iTerm2 to see the new profile."
fi
echo "Run 'exec zsh' to reload your shell."
if [ -f ~/.config/kitty/kitty.conf ]; then
    echo "Kitty configuration has been linked to ~/.config/kitty/kitty.conf"
fi
