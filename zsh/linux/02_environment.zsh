# Linux-generic Environment Configuration
# Applies to ALL Linux distros. Loaded after shared 02_environment.zsh.

# =============================================================================
# XDG BASE DIRECTORIES
# =============================================================================

export XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
export XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
export XDG_CACHE_HOME="${XDG_CACHE_HOME:-$HOME/.cache}"

# =============================================================================
# PATH — prioritise ~/.local/bin
# mise, fzf, zoxide, and other tools install here on Linux
# =============================================================================

typeset -U path=(
  "${HOME}/.local/bin"
  $path
)
