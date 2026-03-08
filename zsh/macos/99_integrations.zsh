# macOS-specific Integrations

# =============================================================================
# FZF — fd backend (fd binary is available on macOS via Homebrew)
# =============================================================================

if command -v fd >/dev/null 2>&1; then
  export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'
  export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
  export FZF_ALT_C_COMMAND='fd --type d --hidden --follow --exclude .git'
fi

# =============================================================================
# KITTY TERMINAL INTEGRATION
# =============================================================================

if [[ "$TERM" == "xterm-kitty" ]]; then
  kitty-help() {
    echo "Kitty Terminal Shortcuts (from ~/.config/kitty/kitty.conf)"
    echo "================================================================"
    if [[ -f "${HOME}/.config/kitty/kitty.conf" ]]; then
      grep "^map " "${HOME}/.config/kitty/kitty.conf" | sed "s/^map /  /" | sort
    else
      echo "kitty.conf not found at ~/.config/kitty/kitty.conf"
    fi
    echo ""
    echo "For full documentation: https://sw.kovidgoyal.net/kitty/overview/"
  }

  if [[ -d "${HOME}/.config/kitty/kitty-customizations" ]]; then
    ksave()   { "${HOME}/.config/kitty/kitty-customizations/session_manager.py" save "$1"; }
    kload()   { "${HOME}/.config/kitty/kitty-customizations/session_manager.py" load "$1"; }
    ksplit()  { "${HOME}/.config/kitty/kitty-customizations/smart_split.py"; }
    knotify() { "${HOME}/.config/kitty/kitty-customizations/notify.py" "$@"; }
    ktheme()  { "${HOME}/.config/kitty/kitty-customizations/theme_switcher.py"; }
  fi
fi
