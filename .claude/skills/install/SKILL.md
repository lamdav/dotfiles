---
name: install
description: Run dotfiles installation or re-installation tasks. Use when the user asks to install, set up, re-link, or bootstrap their dotfiles on a machine.
argument-hint: "[all|packages|symlinks|nvim|mise|shell]"
allowed-tools: Bash, Read, Edit
---

Run dotfiles installation for this machine. Reference `docs/new-machine.md` for the full new-machine runbook.

The user may pass an optional scope via $ARGUMENTS:
- `all` or no argument — full install (packages + symlinks + post-install)
- `packages` — brew bundle only
- `symlinks` — re-run installer symlinks only (no packages, no system prefs)
- `shell` — regenerate plugin cache and reload
- `nvim` — install/sync neovim plugins
- `mise` — install all mise runtimes
- `gh` — authenticate GitHub CLI

## Steps by scope

### all
```bash
# Packages
brew bundle --file brew/Brewfile.devtools
brew bundle --file brew/Brewfile.k8s
brew bundle --file brew/Brewfile.gui
brew bundle --file brew/Brewfile.apps

# Symlinks
python installer/main.py install --skip-system

# Post-install
exec zsh && updateplugins && exec zsh
mise install
nvim --headless "+Lazy sync" +qa
gh auth login
```

### packages
```bash
brew bundle --file brew/Brewfile.devtools
brew bundle --file brew/Brewfile.k8s
brew bundle --file brew/Brewfile.gui
brew bundle --file brew/Brewfile.apps
```

### symlinks
```bash
python installer/main.py install --skip-packages --skip-system
```

### shell
```bash
updateplugins && exec zsh
```

### nvim
```bash
nvim --headless "+Lazy sync" +qa
```

### mise
```bash
mise install
```

### gh
```bash
gh auth login
```

## Instructions

1. Read `docs/new-machine.md` first for full context and prerequisites.
2. Determine the scope from $ARGUMENTS (default: `all`).
3. Check prerequisites before running (e.g. brew installed, repo cloned, python available).
4. Run the appropriate commands using the Bash tool.
5. After each major step, verify it succeeded before continuing.
6. Run `python installer/main.py status` at the end to confirm symlinks are correct.
7. Report what was installed and flag anything that needs manual action (e.g. `gh auth login` requires browser, Kitty hotkey window requires System Settings).
