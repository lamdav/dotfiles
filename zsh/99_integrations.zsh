# External Tool Integrations — cross-platform
# These tools are installed on every supported platform by the installer.

# =============================================================================
# MISE (version manager for node, python, java, etc.)
# =============================================================================

command -v mise >/dev/null 2>&1 && eval "$(mise activate zsh)"

# =============================================================================
# FZF (fuzzy finder)
# =============================================================================

command -v fzf >/dev/null 2>&1 && eval "$(fzf --zsh)"
export FZF_DEFAULT_OPTS='--height 40% --layout=reverse --border --bind ctrl-/:toggle-preview'

# =============================================================================
# ZOXIDE (smart cd)
# =============================================================================

command -v zoxide >/dev/null 2>&1 && eval "$(zoxide init zsh --cmd cd)"

# =============================================================================
# DIRENV (per-directory environment)
# =============================================================================

command -v direnv >/dev/null 2>&1 && eval "$(direnv hook zsh)"

# =============================================================================
# POWERLEVEL10K CONFIGURATION
# =============================================================================

if [[ -f "${HOME}/.p10k.zsh" ]]; then
  source "${HOME}/.p10k.zsh"
else
  echo "Run 'p10k configure' to set up your prompt"
fi

# =============================================================================
# DIRENV COMPLETION HOOK
# Picks up DIRENV_COMPLETION_DIR set by layout_uv in direnvrc.
# Adds the dir to fpath and runs compdef on enter; cleans up on exit.
# =============================================================================

_direnv_completion_hook() {
  local active="${DIRENV_COMPLETION_DIR:-}"

  if [[ -n "$active" && -d "$active" ]]; then
    # Source each completion file once per directory.
    # Each file defines its function and calls compdef itself.
    if [[ "$active" != "${_DIRENV_COMPLETION_DIR_LOADED:-}" ]]; then
      for f in "$active"/_*(N); do
        source "$f"
      done
      _DIRENV_COMPLETION_DIR_LOADED="$active"
    fi
  elif [[ -n "${_DIRENV_COMPLETION_DIR_LOADED:-}" ]]; then
    # Left the project — strip .direnv completion dirs from fpath
    fpath=("${(@)fpath:#*/.direnv/completions}")
    unset _DIRENV_COMPLETION_DIR_LOADED
  fi
}
add-zsh-hook precmd _direnv_completion_hook

# =============================================================================
# CUSTOM CONFIGURATION
# =============================================================================

[[ ! -f "${HOME}/.zshrc_custom" ]] || source "${HOME}/.zshrc_custom"
