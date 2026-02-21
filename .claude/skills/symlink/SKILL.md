---
name: symlink
description: Audit and repair dotfiles symlinks. Use when the user asks to check, fix, verify, or re-link their dotfiles configuration.
argument-hint: "[status|repair|<specific-config>]"
allowed-tools: Bash, Read
---

Audit and optionally repair dotfiles symlinks. Reference `docs/maintenance.md` for context.

The user may pass an optional argument via $ARGUMENTS:
- `status` or no argument — show status of all symlinks
- `repair` — re-run the installer in symlinks-only mode to fix any broken links
- A specific config name (e.g. `nvim`, `git`, `zsh`, `mise`) — check just that one

## Steps by scope

### status (default)
```bash
cd ~/personal/dotfiles && python3 installer/main.py status
```

### repair
```bash
cd ~/personal/dotfiles && python3 installer/main.py install --skip-packages --skip-system
```

### specific config — manual checks
```bash
# nvim
ls -la ~/.config/nvim

# git
ls -la ~/.gitconfig
ls -la ~/.gitconfig-work

# zsh
ls -la ~/.zshrc
ls -la ~/.zsh_plugins
ls -la ~/.p10k.zsh
ls -la ~/.config/zsh/

# mise
ls -la ~/.config/mise/config.toml

# direnv
ls -la ~/.config/direnv/direnvrc

# kitty
ls -la ~/.config/kitty/kitty.conf
```

## Instructions

1. Run the appropriate check for the requested scope.
2. For each symlink, confirm it points to the correct file inside `~/configs/dotfiles/`.
3. Flag any symlink that is broken, missing, or pointing to the wrong target.
4. If `repair` was requested, run the installer and report what was fixed.
5. Summarize the results in a clear table.
