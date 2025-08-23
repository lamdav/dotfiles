#!/usr/bin/env zsh
# ~/.zshrc - Modular Zsh Configuration
# Performance-optimized setup with best practices

# =============================================================================
# PERFORMANCE PROFILING (uncomment to debug startup time)
# =============================================================================
# zmodload zsh/zprof

# =============================================================================
# POWERLEVEL10K INSTANT PROMPT (must be at the top)
# =============================================================================
# Enable Powerlevel10k instant prompt. Should stay close to the top of ~/.zshrc.
# Initialization code that may require console input (password prompts, [y/n]
# confirmations, etc.) must go above this block; everything else may go below.
if [[ -r "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh" ]]; then
  source "${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh"
fi

# =============================================================================
# MODULAR CONFIGURATION LOADING
# =============================================================================

# Define the configuration directory - prefer ~/.config/zsh if it exists
if [[ -d "${HOME}/.config/zsh" ]]; then
  ZSH_CONFIG_DIR="${HOME}/.config/zsh"
else
  # Fallback to dotfiles directory relative to this file
  ZSH_CONFIG_DIR="$(dirname "${(%):-%x}")/zsh"
fi

# Load configuration modules in order
zsh_modules=(
  "options"      # ZSH options and behavior
  "completion"   # Completion system setup
  "keybindings"  # Key bindings configuration  
  "environment"  # Environment variables and PATH
  "lazy-loading" # Lazy loading functions
  "aliases"      # Aliases and utility functions
  "integrations" # External tool integrations
)

# Source each module with error handling
for module in "${zsh_modules[@]}"; do
  module_file="${ZSH_CONFIG_DIR}/${module}.zsh"
  if [[ -r "$module_file" ]]; then
    source "$module_file"
  else
    echo "Warning: Could not load zsh module: $module_file"
    echo "  ZSH_CONFIG_DIR: $ZSH_CONFIG_DIR"
    echo "  File exists: $(test -f "$module_file" && echo "yes" || echo "no")"
    echo "  File readable: $(test -r "$module_file" && echo "yes" || echo "no")"
  fi
done

# =============================================================================
# CLEANUP
# =============================================================================

# Remove duplicate entries from arrays
typeset -U path fpath

# Clean up variables
unset ZSH_CONFIG_DIR zsh_modules module module_file

# =============================================================================
# DEBUG PROFILING (uncomment first line of file to enable)
# =============================================================================
# zprof