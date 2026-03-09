# Plugin Manager and Plugin Loading
#
# This module initializes the antidote plugin manager and loads all plugins.
# It runs after environment setup but before completion initialization,
# allowing plugins to add their completion directories to FPATH.

# =============================================================================
# ANTIDOTE PLUGIN MANAGER
# =============================================================================

# Locate antidote — Homebrew (macOS) or git clone at ~/.antidote (Linux)
_antidote_zsh=""
if [[ -f "/opt/homebrew/opt/antidote/share/antidote/antidote.zsh" ]]; then
  _antidote_zsh="/opt/homebrew/opt/antidote/share/antidote/antidote.zsh"
elif [[ -f "${HOME}/.antidote/antidote.zsh" ]]; then
  _antidote_zsh="${HOME}/.antidote/antidote.zsh"
fi

if [[ -n "$_antidote_zsh" ]]; then
  source "$_antidote_zsh"

  # Lazy-load: regenerate static plugin file only when .zsh_plugins changes
  zsh_plugins=${ZDOTDIR:-$HOME}/.zsh_plugins
  if [[ ! ${zsh_plugins}.zsh -nt ${zsh_plugins} ]]; then
    antidote bundle <${zsh_plugins} >|${zsh_plugins}.zsh
  fi
  source ${zsh_plugins}.zsh

  # =============================================================================
  # PLUGIN-SPECIFIC FPATH ADDITIONS
  # Uses $ANTIDOTE_HOME set by platform 02_environment (macos/ or linux/)
  # =============================================================================

  _antidote_cache="${ANTIDOTE_HOME:-${HOME}/.cache/antidote}"

  # Add wd (warp directory) completion to fpath if plugin is loaded
  if (( $+functions[wd] )); then
    wd_plugin_dir="${_antidote_cache}/https-COLON--SLASH--SLASH-github.com-SLASH-mfaerevaag-SLASH-wd"
    if [[ -d "$wd_plugin_dir" ]]; then
      fpath=("$wd_plugin_dir" $fpath)
      if [[ -f "$wd_plugin_dir/_wd.sh" ]]; then
        eval "$(echo '_wd() {'; cat "$wd_plugin_dir/_wd.sh" | tail -n +2; echo '}')"
      fi
    fi
  fi

  # Add zsh-users/zsh-completions to fpath if plugin is loaded
  zsh_completions_dir="${_antidote_cache}/https-COLON--SLASH--SLASH-github.com-SLASH-zsh-users-SLASH-zsh-completions/src"
  if [[ -d "$zsh_completions_dir" ]]; then
    fpath=("$zsh_completions_dir" $fpath)
  fi

  unset _antidote_cache
else
  echo "Warning: Antidote not found."
  echo "  macOS:  brew install antidote"
  echo "  Linux:  git clone --depth=1 https://github.com/getantidote/antidote.git ~/.antidote"
fi
unset _antidote_zsh
