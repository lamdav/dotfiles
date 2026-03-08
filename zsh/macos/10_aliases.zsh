# macOS-specific Aliases
# Loaded after shared 10_aliases.zsh by the platform-aware .zshrc loader

# =============================================================================
# MACOS SYSTEM ALIASES
# =============================================================================

# Refresh Übersicht widgets
alias refreshbar='osascript -e '\''tell application id "tracesOf.Uebersicht" to refresh'\'''

# =============================================================================
# KITTY TERMINAL
# =============================================================================

# Use kitten ssh when running inside Kitty — auto-pushes terminfo to server.
# Safe as a drop-in: kitten ssh accepts all standard ssh flags.
[[ "$TERM" == "xterm-kitty" ]] && alias ssh='kitten ssh'
