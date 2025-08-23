# Aliases and Functions

# =============================================================================
# SYSTEM ALIASES
# =============================================================================

# Enhanced ls with eza (if available)
if command -v eza >/dev/null 2>&1; then
  # Clear any existing ls alias first
  unalias ls 2>/dev/null || true
  
  # Use functions instead of aliases to avoid completion conflicts
  ls() { eza --color=always --long --git --no-filesize --no-time --no-permissions --no-user "$@"; }
  ll() { eza --color=always --long --git "$@"; }
  tree() { eza --tree "$@"; }
  
  # Disable completion for ls function completely to avoid _eza errors
  compdef -d ls
else
  # Fallback to regular ls with colors
  alias ls="ls -la --color=auto"
  alias ll="ls -la --color=auto"
fi

# Modern CLI tool replacements
if command -v bat >/dev/null 2>&1; then
  alias cat='bat --style=plain'
fi

if command -v fd >/dev/null 2>&1; then
  alias find='fd'
fi

if command -v rg >/dev/null 2>&1; then
  alias grep='rg'
fi

# =============================================================================
# GIT ALIASES
# =============================================================================

if command -v git >/dev/null 2>&1; then
  alias g='git'
  alias gs='git status'
  alias ga='git add'
  alias gc='git commit'
  alias gp='git push'
  alias gl='git pull'
  alias gd='git diff'
  alias gco='git checkout'
  alias gb='git branch'
  
  # Advanced git operations
  alias git-clean='git -c gc.reflogExpire=0 -c gc.reflogExpireUnreachable=0 -c gc.rerereresolved=0 -c gc.rerereunresolved=0 -c gc.pruneExpire=now gc "$@"'
fi

# =============================================================================
# DIRECTORY NAVIGATION
# =============================================================================

alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'

# =============================================================================
# SAFETY ALIASES
# =============================================================================

alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'

# =============================================================================
# ZSH MANAGEMENT
# =============================================================================

alias editzsh="$EDITOR ~/.zshrc"
alias refreshzsh="exec zsh"
alias reloadzsh="source ~/.zshrc"

# List all aliases with descriptions
aliases() {
  echo "📋 Current Aliases:"
  echo "=================="
  alias | sort | while read line; do
    # Extract alias name and command
    alias_name=$(echo "$line" | cut -d'=' -f1)
    alias_cmd=$(echo "$line" | cut -d'=' -f2- | sed "s/^'//" | sed "s/'$//")
    printf "  %-15s → %s\n" "$alias_name" "$alias_cmd"
  done
}

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

# Benchmark shell startup time
benchmarkzsh() {
  for i in $(seq 1 10); do /usr/bin/time zsh -i -c exit; done
}

# Update shell plugins
updateplugins() {
  if command -v antidote >/dev/null 2>&1; then
    antidote bundle < ~/.zsh_plugins > ~/.zsh_plugins.zsh
    echo "✅ Plugins updated. Run 'refreshzsh' to reload."
  else
    echo "❌ Antidote not found"
  fi
}

# Create directory and change into it
mkcd() {
  [[ $# -eq 1 ]] || { echo "Usage: mkcd <directory>"; return 1 }
  mkdir -p "$1" && cd "$1"
}

# Refresh Übersicht widgets
alias refreshbar='osascript -e '\''tell application id "tracesOf.Uebersicht" to refresh'\'''

# Extract various archive formats
extract() {
  if [[ -f "$1" ]]; then
    case "$1" in
      *.tar.bz2)   tar xjf "$1"   ;;
      *.tar.gz)    tar xzf "$1"   ;;
      *.bz2)       bunzip2 "$1"   ;;
      *.rar)       unrar x "$1"   ;;
      *.gz)        gunzip "$1"    ;;
      *.tar)       tar xf "$1"    ;;
      *.tbz2)      tar xjf "$1"   ;;
      *.tgz)       tar xzf "$1"   ;;
      *.zip)       unzip "$1"     ;;
      *.Z)         uncompress "$1";;
      *.7z)        7z x "$1"      ;;
      *)           echo "'$1' cannot be extracted via extract()" ;;
    esac
  else
    echo "'$1' is not a valid file"
  fi
}