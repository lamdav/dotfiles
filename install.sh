#!/usr/bin/env bash
set -euo pipefail

export dir="$(pwd)"

# Check if Homebrew is installed, install if not
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Update and install packages
echo "Updating Homebrew and installing packages..."
brew update && brew bundle --no-lock

# Install RVM if not present
if ! command -v rvm &> /dev/null; then
    echo "Installing RVM..."
    curl -sSL https://get.rvm.io | bash -s stable
fi

# Install Oh My Zsh if not present
if [ ! -d "$HOME/.oh-my-zsh" ]; then
    echo "Installing Oh My Zsh..."
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
fi
# Create symbolic links for shell configuration
echo "Setting up shell configuration..."
ln -sf "$dir/.zshrc" ~/.zshrc
ln -sf "$dir/.zsh_plugins" ~/.zsh_plugins
[ -f "$dir/.zlogin" ] && ln -sf "$dir/.zlogin" ~/.zlogin
mkdir -p ~/.oh-my-zsh/custom/themes
ln -sf "$dir/steeef-lambda.zsh-theme" ~/.oh-my-zsh/custom/themes/steeef-lambda.zsh-theme
[ -f "$dir/.p10k.zsh" ] && ln -sf "$dir/.p10k.zsh" ~/.p10k.zsh

# Setup vim configuration
if [ -f "$dir/.vimrc" ]; then
    echo "Setting up vim configuration..."
    ln -sf "$dir/.vimrc" ~/.vimrc
fi

# Setup Aerospace configuration
if [ -f "$dir/.aerospace.toml" ]; then
    ln -sf "$dir/.aerospace.toml" ~/.aerospace.toml
fi

# Setup git configuration
echo "Setting up git configuration..."
ln -sf "$dir/.gitconfig" ~/.gitconfig

# Setup iTerm2 profile
if [ -f "$dir/iterm-profiles.json" ]; then
    echo "Setting up iTerm2 profile..."
    mkdir -p ~/Library/Application\ Support/iTerm2/DynamicProfiles
    ln -sf "$dir/iterm-profiles.json" ~/Library/Application\ Support/iTerm2/DynamicProfiles/iterm-profiles.json
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
# Show battery percentage in menu bar
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
# Safari: Enable develop menu and web inspector
defaults write com.apple.Safari IncludeDevelopMenu -bool true
defaults write com.apple.Safari WebKitDeveloperExtrasEnabledPreferenceKey -bool true

# Restart affected applications to apply changes
echo "Restarting applications to apply changes..."
killall Dock 2>/dev/null || true
killall Finder 2>/dev/null || true
killall SystemUIServer 2>/dev/null || true

echo "\nDotfiles installation complete!"
echo "System preferences have been configured for optimal development workflow."
echo "Run 'exec zsh' to reload your shell."
echo "You may need to restart iTerm2 to see the new profile."
echo "Some changes may require a system restart to take full effect."
