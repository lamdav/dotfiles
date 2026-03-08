# Environment Variables and PATH Configuration

# =============================================================================
# CORE ENVIRONMENT
# =============================================================================

export TERM="${TERM:-xterm-256color}"
export EDITOR="${EDITOR:-nvim}"
export PAGER="${PAGER:-less}"

# SSH configuration
export SSH_KEY_PATH="~/.ssh/id_ed25519"

# GitHub token for MCP and tooling (sourced from gh CLI to avoid storing in plaintext)
if command -v gh >/dev/null 2>&1; then
  export GITHUB_PERSONAL_ACCESS_TOKEN="$(gh auth token 2>/dev/null)"
fi

# Language and locale
export LANG="${LANG:-en_US.UTF-8}"
export LC_ALL="${LC_ALL:-en_US.UTF-8}"

# =============================================================================
# TOOL-SPECIFIC SETTINGS
# =============================================================================

# Bat theme
export BAT_THEME=Dracula

# zsh-autosuggestions
export ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE="fg=#6272a4"  # Dracula comment color — visible but dim
export ZSH_AUTOSUGGEST_STRATEGY=(history completion)  # try history first, then completion
export ZSH_AUTOSUGGEST_BUFFER_MAX_SIZE=20             # don't suggest for very long commands

# Avoid wd named dir exports (fixes prompt issues)
export WD_SKIP_EXPORT=1

# =============================================================================
# PATH CONSTRUCTION
# =============================================================================

# Build PATH efficiently to avoid duplicates
typeset -U path=(
  /usr/local/bin
  /usr/local/sbin
  $path
  "${HOME}/.cargo/bin"
  "${HOME}/go/bin"
  "${HOME}/.local/bin"
)

# =============================================================================
# EXTERNAL INTEGRATIONS
# =============================================================================
