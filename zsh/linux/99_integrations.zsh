# Linux-specific Integrations

# =============================================================================
# FZF — fdfind backend (fd is installed as fdfind on Debian/Ubuntu)
# fzf subprocesses run in sh, not zsh, so aliases don't apply — use the binary.
# =============================================================================

if command -v fdfind >/dev/null 2>&1; then
  export FZF_DEFAULT_COMMAND='fdfind --type f --hidden --follow --exclude .git'
  export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
  export FZF_ALT_C_COMMAND='fdfind --type d --hidden --follow --exclude .git'
fi
