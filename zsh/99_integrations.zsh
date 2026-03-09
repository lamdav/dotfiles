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
  if [[ -n "${DIRENV_COMPLETION_DIR:-}" && -d "$DIRENV_COMPLETION_DIR" ]]; then
    if (( ! $fpath[(Ie)$DIRENV_COMPLETION_DIR] )); then
      fpath=("$DIRENV_COMPLETION_DIR" $fpath)
      for f in "$DIRENV_COMPLETION_DIR"/_*(N); do
        compdef "${f:t}" "${${f:t}#_}"
      done
    fi
  else
    # Remove any stale .direnv completion dirs when leaving a project
    fpath=("${(@)fpath:#*/.direnv/completions}")
  fi
}
add-zsh-hook precmd _direnv_completion_hook

# =============================================================================
# CUSTOM CONFIGURATION
# =============================================================================

[[ ! -f "${HOME}/.zshrc_custom" ]] || source "${HOME}/.zshrc_custom"
