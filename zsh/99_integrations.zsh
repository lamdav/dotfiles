# External Tool Integrations

# =============================================================================
# CLAUDE CODE INTEGRATION
# =============================================================================

if [[ -f "${HOME}/.claude/local/claude" ]]; then
  alias claude="${HOME}/.claude/local/claude"
fi

# =============================================================================
# KITTY TERMINAL INTEGRATION
# =============================================================================

if [[ "$TERM" == "xterm-kitty" ]] && [[ -f "${HOME}/.config/kitty/kitty.conf" ]]; then
  # Dynamic kitty shortcuts help
  kitty-help() {
    echo "🐱 Kitty Terminal Shortcuts (from ~/.config/kitty/kitty.conf)"
    echo "================================================================"
    if [[ -f ~/.config/kitty/kitty.conf ]]; then
      grep "^map " ~/.config/kitty/kitty.conf | sed "s/^map /  /" | sort
    else
      echo "kitty.conf not found at ~/.config/kitty/kitty.conf"
    fi
    echo ""
    echo "For full documentation: https://sw.kovidgoyal.net/kitty/overview/"
  }
  
  # Kitty enhancement functions
  if [[ -d "${HOME}/.config/kitty/kitty-customizations" ]]; then
    ksave() { ~/.config/kitty/kitty-customizations/session_manager.py save "$1"; }
    kload() { ~/.config/kitty/kitty-customizations/session_manager.py load "$1"; }
    ksplit() { ~/.config/kitty/kitty-customizations/smart_split.py; }
    knotify() { ~/.config/kitty/kitty-customizations/notify.py "$@"; }
    ktheme() { ~/.config/kitty/kitty-customizations/theme_switcher.py; }
  fi
fi

# =============================================================================
# POWERLEVEL10K CONFIGURATION
# =============================================================================

# Load p10k configuration if it exists
if [[ -f "${HOME}/.p10k.zsh" ]]; then
  source "${HOME}/.p10k.zsh"
else
  echo "💡 Run 'p10k configure' to set up your prompt"
fi

# =============================================================================
# CUSTOM CONFIGURATION
# =============================================================================

# Source custom configuration if it exists
[[ ! -f ~/.zshrc_custom ]] || source ~/.zshrc_custom