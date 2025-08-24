# Plugin Manager and Plugin Loading
#
# This module initializes the antidote plugin manager and loads all plugins.
# It runs after environment setup but before completion initialization,
# allowing plugins to add their completion directories to FPATH.

# =============================================================================
# ANTIDOTE PLUGIN MANAGER
# =============================================================================

if [[ -f "/opt/homebrew/opt/antidote/share/antidote/antidote.zsh" ]]; then
  source "/opt/homebrew/opt/antidote/share/antidote/antidote.zsh"
  
  # Lazy-load antidote and generate the static load file only when needed
  zsh_plugins=${ZDOTDIR:-$HOME}/.zsh_plugins
  if [[ ! ${zsh_plugins}.zsh -nt ${zsh_plugins} ]]; then
    antidote bundle <${zsh_plugins} >${zsh_plugins}.zsh
  fi
  source ${zsh_plugins}.zsh
  
  # =============================================================================
  # PLUGIN-SPECIFIC FPATH ADDITIONS
  # =============================================================================
  
  # Add wd (warp directory) completion to fpath if plugin is loaded
  if (( $+functions[wd] )); then
    wd_plugin_dir="${HOME}/Library/Caches/antidote/https-COLON--SLASH--SLASH-github.com-SLASH-mfaerevaag-SLASH-wd"
    if [[ -d "$wd_plugin_dir" ]]; then
      fpath=("$wd_plugin_dir" $fpath)
      
      # Handle wd completion naming issue (_wd.sh -> _wd function)
      if [[ -f "$wd_plugin_dir/_wd.sh" ]]; then
        eval "$(echo '_wd() {'; cat "$wd_plugin_dir/_wd.sh" | tail -n +2; echo '}')"
      fi
    fi
  fi
  
  # Add zsh-users/zsh-completions to fpath if plugin is loaded
  zsh_completions_dir="${HOME}/Library/Caches/antidote/https-COLON--SLASH--SLASH-github.com-SLASH-zsh-users-SLASH-zsh-completions/src"
  if [[ -d "$zsh_completions_dir" ]]; then
    fpath=("$zsh_completions_dir" $fpath)
  fi
  
else
  echo "Warning: Antidote not found. Install with: brew install antidote"
fi