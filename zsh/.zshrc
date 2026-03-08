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
# PLATFORM DETECTION
# =============================================================================

if [[ "$OSTYPE" == darwin* ]]; then
  ZSH_OS_FAMILY="macos"
  ZSH_DISTRO="macos"
elif [[ "$OSTYPE" == linux* ]]; then
  ZSH_OS_FAMILY="linux"
  ZSH_DISTRO="${${(f)"$(</etc/os-release)"}[(r)ID=*]#ID=}"
  ZSH_DISTRO="${ZSH_DISTRO:-linux}"
fi
export ZSH_OS_FAMILY ZSH_DISTRO

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

# Homebrew completions are set up in environment.zsh module

# =============================================================================
# MODULAR CONFIGURATION LOADING SEQUENCE
# =============================================================================
# 
# Load order is critical - modules have dependencies:
# 1. options:      Basic zsh options and behavior (no dependencies)
# 2. environment:  PATH, FPATH, exports (sets base FPATH)
# 3. plugins:      Initialize plugin manager and load plugins (adds to FPATH)
# 4. completion:   Initialize completion system (requires complete FPATH)
# 5. keybindings:  Key bindings (requires completion system)
# 6. aliases:      Aliases and functions (requires all tools available)
# 7. integrations: External tool integrations (requires everything else)

zsh_modules=(
  "01_options"
  "02_environment"
  "03_plugins"
  "04_completion"
  "05_keybindings"
  "10_aliases"
  "99_integrations"
)

# Source each module with platform layers: shared → family → distro
for module in "${zsh_modules[@]}"; do
  # Shared layer
  module_file="${ZSH_CONFIG_DIR}/${module}.zsh"
  if [[ -r "$module_file" ]]; then
    source "$module_file"
  else
    echo "Warning: Could not load zsh module: $module_file"
  fi

  # OS family layer (e.g. linux/) — skipped when family == distro (macOS)
  if [[ -n "$ZSH_OS_FAMILY" && "$ZSH_OS_FAMILY" != "$ZSH_DISTRO" ]]; then
    family_file="${ZSH_CONFIG_DIR}/${ZSH_OS_FAMILY}/${module}.zsh"
    [[ -r "$family_file" ]] && source "$family_file"
  fi

  # Distro layer (e.g. macos/, ubuntu/)
  if [[ -n "$ZSH_DISTRO" ]]; then
    distro_file="${ZSH_CONFIG_DIR}/${ZSH_DISTRO}/${module}.zsh"
    [[ -r "$distro_file" ]] && source "$distro_file"
  fi
done

# =============================================================================
# CLEANUP
# =============================================================================

# Remove duplicate entries from arrays
typeset -U path fpath

# Clean up variables
unset ZSH_CONFIG_DIR zsh_modules module module_file family_file distro_file

# =============================================================================
# DEBUG PROFILING (uncomment first line of file to enable)
# =============================================================================
# zprof