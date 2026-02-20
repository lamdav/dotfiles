---
name: maintain
description: Run dotfiles maintenance tasks. Use when the user asks to update, upgrade, or maintain their dotfiles, tools, plugins, or shell config.
argument-hint: "[daily|weekly|monthly|all]"
allowed-tools: Bash, Read, Edit
---

Run dotfiles maintenance for this machine. Reference `docs/maintenance.md` for the full runbook.

The user may pass an optional scope via $ARGUMENTS:
- `daily` — reload shell, direnv, plugins if needed
- `weekly` — brew upgrade, mise upgrade, nvim plugins, gh extensions
- `monthly` — omz update, mise bump, brew cleanup, audit symlinks
- `all` or no argument — run everything interactively, asking before destructive steps

## Steps by scope

### Daily (always safe)
```bash
exec zsh
updateplugins
```

### Weekly
```bash
brew update && brew upgrade
brew upgrade --cask
mise upgrade
nvim --headless "+Lazy sync" +qa
gh extension upgrade --all
```

### Monthly
```bash
omz update
mise self-update && mise upgrade --bump
brew cleanup
brew bundle cleanup --file brew/Brewfile.devtools --dry-run
python installer/main.py status
```

## Instructions

1. Read `docs/maintenance.md` first for full context.
2. Run the appropriate commands for the requested scope using the Bash tool.
3. Report what was updated and flag anything that needs attention (failed updates, outdated symlinks, etc.).
4. For destructive steps (brew cleanup, removing packages), show the user what would be removed and confirm before proceeding.
5. After running, summarize what changed.
