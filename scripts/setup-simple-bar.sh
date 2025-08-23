#!/usr/bin/env bash
# Simple-bar Setup Script for Firewatch Theme Integration

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

DOTFILES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SIMPLE_BAR_DIR="$HOME/Library/Application Support/Übersicht/widgets/simple-bar"
SIMPLE_BAR_CONFIG="$HOME/.simplebarrc"

echo -e "${BLUE}🎨 Setting up Simple-bar with Firewatch theme...${NC}"

# Check if Übersicht is installed, install if needed
if ! ls /Applications/ | grep -i "übersicht\|uebersicht" > /dev/null; then
    echo -e "${YELLOW}📥 Übersicht not found. Installing via Homebrew...${NC}"
    
    if command -v brew &> /dev/null; then
        brew install --cask ubersicht
        echo -e "${GREEN}✅ Übersicht installed successfully${NC}"
    else
        echo -e "${RED}❌ Homebrew not found. Please install Homebrew first or download Übersicht manually${NC}"
        echo "   Manual download: https://tracesof.net/uebersicht/"
        exit 1
    fi
fi

# Check if simple-bar is installed
if [ ! -d "$SIMPLE_BAR_DIR" ]; then
    echo -e "${YELLOW}📥 Simple-bar not found. Installing...${NC}"
    
    # Create widgets directory if it doesn't exist
    mkdir -p "$(dirname "$SIMPLE_BAR_DIR")"
    
    # Clone simple-bar
    if command -v git &> /dev/null; then
        git clone https://github.com/Jean-Tinland/simple-bar "$SIMPLE_BAR_DIR"
        echo -e "${GREEN}✅ Simple-bar installed successfully${NC}"
    else
        echo -e "${RED}❌ Git not found. Please install git or download simple-bar manually${NC}"
        exit 1
    fi
fi

# Backup existing config if it exists
if [ -f "$SIMPLE_BAR_CONFIG" ]; then
    echo -e "${BLUE}💾 Backing up existing simple-bar config...${NC}"
    cp "$SIMPLE_BAR_CONFIG" "${SIMPLE_BAR_CONFIG}.backup.$(date +%Y%m%d_%H%M%S)"
fi

# Install our Firewatch theme configuration via symlink
echo -e "${BLUE}🎨 Installing Firewatch theme configuration...${NC}"
ln -sf "$DOTFILES_DIR/ubersicht/simple-bar/simplebarrc" "$SIMPLE_BAR_CONFIG"

# Set up AeroSpace integration (already configured in .aerospace.toml)
echo -e "${BLUE}🚀 AeroSpace integration already configured in .aerospace.toml${NC}"

# Refresh Übersicht
echo -e "${BLUE}🔄 Refreshing Übersicht...${NC}"
osascript -e 'tell application id "tracesOf.Uebersicht" to refresh' 2>/dev/null || {
    echo -e "${YELLOW}⚠️  Could not refresh Übersicht automatically. Please:${NC}"
    echo "   1. Open Übersicht"
    echo "   2. Click the menu bar icon"  
    echo "   3. Click 'Refresh all Widgets'"
}

# Setup completion
echo -e "${GREEN}✅ Simple-bar setup complete!${NC}"
echo ""
echo -e "${BLUE}📋 Configuration Summary:${NC}"
echo "   • Theme: Firewatch Custom (matches your terminal)"
echo "   • Colors: Dark theme with cyan accents (#44a8b6)"
echo "   • Font: FiraCode Nerd Font (matches your terminal)"
echo "   • Widgets: Spaces, App, Clock, Battery, System Info"
echo "   • AeroSpace: Auto-refresh on workspace changes"
echo ""
echo -e "${BLUE}🎛️  Customization:${NC}"
echo "   • Config file: $SIMPLE_BAR_CONFIG"
echo "   • Edit and run: osascript -e 'tell application id \"tracesOf.Uebersicht\" to refresh'"
echo "   • Or use AeroSpace shortcuts to see changes instantly"
echo ""
echo -e "${BLUE}🔧 Troubleshooting:${NC}"
echo "   • If widgets don't appear: Check Übersicht permissions in System Preferences"
echo "   • For styling issues: Edit the customStyles section in the config"
echo "   • Color problems: Verify your terminal theme matches the config"