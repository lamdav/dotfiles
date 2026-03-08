# Linux-generic Aliases
# Applies to ALL Linux distros. Loaded after shared 10_aliases.zsh.

# =============================================================================
# DEBIAN/UBUNTU BINARY NAME SHIMS
# fd-find and batcat are renamed on Debian-family distros
# =============================================================================

# fd: installed as fdfind on Debian/Ubuntu
if command -v fdfind >/dev/null 2>&1 && ! command -v fd >/dev/null 2>&1; then
  alias fd='fdfind'
  # Also update FZF commands that use fd
  export FZF_DEFAULT_COMMAND='fdfind --type f --hidden --follow --exclude .git'
  export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
  export FZF_ALT_C_COMMAND='fdfind --type d --hidden --follow --exclude .git'
fi

# bat: installed as batcat on Debian/Ubuntu
if command -v batcat >/dev/null 2>&1 && ! command -v bat >/dev/null 2>&1; then
  alias bat='batcat'
  alias cat='batcat --style=plain'
fi
