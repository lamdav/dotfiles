# macOS-specific Environment Configuration
# Loaded after shared 02_environment.zsh by the platform-aware .zshrc loader

# =============================================================================
# MACOS-SPECIFIC EXPORTS
# =============================================================================

export BROWSER="${BROWSER:-open}"
export HOMEBREW_NO_ANALYTICS=1
export ANTIDOTE_HOME="${HOME}/Library/Caches/antidote"

# =============================================================================
# HOMEBREW PATH
# =============================================================================

# Add Homebrew to PATH (Apple Silicon path; Intel uses /usr/local)
typeset -U path=(
  /opt/homebrew/bin
  /opt/homebrew/sbin
  $path
)

# Add Homebrew completions to fpath (must be before compinit in 04_completion.zsh)
if [[ -d "/opt/homebrew/share/zsh/site-functions" ]]; then
  fpath=("/opt/homebrew/share/zsh/site-functions" $fpath)
fi

# =============================================================================
# GOOGLE CLOUD SDK
# =============================================================================

if [[ -f "/opt/homebrew/share/google-cloud-sdk/path.zsh.inc" ]]; then
  source "/opt/homebrew/share/google-cloud-sdk/path.zsh.inc"
fi
