# Environment Variables and PATH Configuration

# =============================================================================
# CORE ENVIRONMENT
# =============================================================================

export TERM="${TERM:-xterm-256color}"
export EDITOR="${EDITOR:-vim}"
export PAGER="${PAGER:-less}"
export BROWSER="${BROWSER:-open}"

# SSH configuration
export SSH_KEY_PATH="~/.ssh/id_ed25519"

# Language and locale
export LANG="${LANG:-en_US.UTF-8}"
export LC_ALL="${LC_ALL:-en_US.UTF-8}"

# =============================================================================
# TOOL-SPECIFIC SETTINGS
# =============================================================================

# Bat theme
export BAT_THEME=Dracula

# Homebrew
export HOMEBREW_NO_ANALYTICS=1

# Add Homebrew completions to fpath (must be before compinit)
if [[ -d "/opt/homebrew/share/zsh/site-functions" ]]; then
  fpath=("/opt/homebrew/share/zsh/site-functions" $fpath)
fi

# Avoid wd named dir exports (fixes prompt issues)
export WD_SKIP_EXPORT=1

# =============================================================================
# PATH CONSTRUCTION
# =============================================================================

# Build PATH efficiently to avoid duplicates
typeset -U path=(
  /opt/homebrew/bin
  /opt/homebrew/sbin
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

# Google Cloud SDK (if installed via Homebrew)
if [[ -f "/opt/homebrew/share/google-cloud-sdk/path.zsh.inc" ]]; then
  source "/opt/homebrew/share/google-cloud-sdk/path.zsh.inc"
fi

if [[ -f "/opt/homebrew/share/google-cloud-sdk/completion.zsh.inc" ]]; then
  source "/opt/homebrew/share/google-cloud-sdk/completion.zsh.inc"
fi