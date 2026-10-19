# Aliases and Functions

# =============================================================================
# SYSTEM ALIASES
# =============================================================================

# Enhanced ls with eza (if available)
if command -v eza >/dev/null 2>&1; then
  alias ls='eza --color=always --git --no-filesize --no-time --no-permissions --no-user'
  alias ll='eza --color=always --long --git'
  alias tree='eza --tree'
else
  # Fallback to regular ls with colors
  alias ls="ls -la --color=auto"
  alias ll="ls -la --color=auto"
fi

# Modern CLI tool replacements
if command -v bat >/dev/null 2>&1; then
  alias cat='bat --style=plain'
fi

if command -v glow >/dev/null 2>&1 && command -v bat >/dev/null 2>&1; then
  batmd() { PAGER='bat' glow -p "$@"; }
fi

if command -v fd >/dev/null 2>&1; then
  alias find='fd'
fi

if command -v rg >/dev/null 2>&1; then
  alias grep='rg'
fi

if command -v dust >/dev/null 2>&1; then
  alias du='dust'
fi

# xh mirrors httpie's flag syntax, so this is a safe drop-in
if command -v xh >/dev/null 2>&1; then
  alias http='xh'
fi

# jaq covers standard jq syntax; some advanced jq-specific filters differ
if command -v jaq >/dev/null 2>&1; then
  alias jq='jaq'
fi

if command -v btop >/dev/null 2>&1; then
  alias top='btop'
fi

if command -v nvim >/dev/null 2>&1; then
  alias vim='nvim'
  alias vi='nvim'
fi

# glow.yml sets pager/style defaults, but --tui isn't a persistable config
# option (only a CLI flag), so force it here for interactive use
if command -v glow >/dev/null 2>&1; then
  alias glow='glow --tui'
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
# DIRENV QUICK-SETUP
# git has no hook that fires on `git init` (githooks(5) has no post-init —
# init.templateDir only helps `git clone`, via post-checkout), so this is a
# plain standalone command, not an automatic hook on an existing command.
# Run it yourself in any project dir to scaffold .envrc.
# =============================================================================

if command -v direnv >/dev/null 2>&1; then
  envrc-init() {
    if [[ -f .envrc ]]; then
      echo ".envrc already exists in $PWD — not touching it."
      return 1
    fi

    echo "Layouts (space-separated numbers, e.g. '1 5'):"
    echo "  1) uv      Python venv via uv, auto-syncs pyproject.toml/requirements.txt"
    echo "  2) python  Python venv via python3 -m venv"
    echo "  3) node    adds node_modules/.bin to PATH"
    echo "  4) go      project-local GOPATH"
    echo "  5) mise    activates .mise.toml (language/tool versions via mise)"

    local picks
    read -r "picks?Choice: "
    local -a selected=(${(z)picks})

    local -a lines
    local c
    for c in "${selected[@]}"; do
      case "$c" in
        1) lines+=("layout uv") ;;
        2) lines+=("layout python") ;;
        3) lines+=("layout node") ;;
        4) lines+=("layout go") ;;
        5) lines+=("use mise") ;;
      esac
    done

    if (( ${#lines[@]} == 0 )); then
      echo "No layout selected — skipping .envrc creation."
      return 1
    fi

    printf '%s\n' "${lines[@]}" >| .envrc
    direnv allow
    echo "Created .envrc:"
    cat .envrc
  }
fi

# =============================================================================
# DIRECTORY NAVIGATION
# =============================================================================

alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'

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
    antidote bundle < ~/.zsh_plugins >| ~/.zsh_plugins.zsh
    echo "✅ Plugins updated. Run 'refreshzsh' to reload."
  else
    echo "❌ Antidote not found"
  fi
}

# Launch yazi file manager; cd the shell to wherever you exited it
y() {
  if ! command -v yazi >/dev/null 2>&1; then
    echo "yazi not found"
    return 1
  fi
  local tmp cwd
  tmp="$(mktemp -t "yazi-cwd.XXXXXX")"
  yazi "$@" --cwd-file="$tmp"
  if cwd="$(command cat -- "$tmp")" && [[ -n "$cwd" && "$cwd" != "$PWD" ]]; then
    builtin cd -- "$cwd"
  fi
  rm -f -- "$tmp"
}

# Create directory and change into it
mkcd() {
  [[ $# -eq 1 ]] || { echo "Usage: mkcd <directory>"; return 1 }
  mkdir -p "$1" && cd "$1"
}

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
