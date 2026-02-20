# External Tool Integrations

# =============================================================================
# MISE (version manager for node, python, java, etc.)
# =============================================================================

if command -v mise >/dev/null 2>&1; then
  eval "$(mise activate zsh)"
fi

# =============================================================================
# FZF (fuzzy finder)
# =============================================================================

if [[ -f "/opt/homebrew/opt/fzf/shell/key-bindings.zsh" ]]; then
  source "/opt/homebrew/opt/fzf/shell/key-bindings.zsh"
fi
if [[ -f "/opt/homebrew/opt/fzf/shell/completion.zsh" ]]; then
  source "/opt/homebrew/opt/fzf/shell/completion.zsh"
fi

if command -v fd >/dev/null 2>&1; then
  export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'
  export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
  export FZF_ALT_C_COMMAND='fd --type d --hidden --follow --exclude .git'
fi
export FZF_DEFAULT_OPTS='--height 40% --layout=reverse --border --bind ctrl-/:toggle-preview'

# =============================================================================
# ZOXIDE (smart cd)
# =============================================================================

if command -v zoxide >/dev/null 2>&1; then
  eval "$(zoxide init zsh --cmd cd)"
fi

# =============================================================================
# DIRENV (per-directory environment)
# =============================================================================

if command -v direnv >/dev/null 2>&1; then
  eval "$(direnv hook zsh)"
fi

# =============================================================================
# KITTY TERMINAL INTEGRATION
# =============================================================================

if [[ "$TERM" == "xterm-kitty" ]] && [[ -f "${HOME}/.config/kitty/kitty.conf" ]]; then
  # Dynamic kitty shortcuts help
  kitty-help() {
    echo "Kitty Terminal Shortcuts (from ~/.config/kitty/kitty.conf)"
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
  echo "Run 'p10k configure' to set up your prompt"
fi

# =============================================================================
# GOOGLE CLOUD SDK
# =============================================================================

if [[ -f "/opt/homebrew/share/google-cloud-sdk/completion.zsh.inc" ]]; then
  source "/opt/homebrew/share/google-cloud-sdk/completion.zsh.inc"
fi

# =============================================================================
# CUSTOM CONFIGURATION
# =============================================================================

# Source custom configuration if it exists
[[ ! -f ~/.zshrc_custom ]] || source ~/.zshrc_custom
