---
name: maintain
description: Run dotfiles maintenance tasks. Use when the user asks to update, upgrade, or maintain their dotfiles, tools, plugins, or shell config.
argument-hint: "[daily|weekly|monthly|sync|all]"
allowed-tools: Bash, Read, Edit
---

Run dotfiles maintenance for this machine. Reference `docs/maintenance.md` for the full runbook.

The user may pass an optional scope via $ARGUMENTS:
- `daily` — reload shell, direnv, plugins if needed
- `weekly` — brew upgrade, mise upgrade, nvim plugins, gh extensions
- `monthly` — omz update, mise bump, brew cleanup, audit symlinks
- `sync` — interactive health check: audit symlinks, config consistency, and prompt to repair anything out of date
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

### Sync (interactive install health check)

Run from `~/personal/dotfiles/`:

```bash
# Step 1: Check symlink status
python installer/main.py status

# Step 2: Verify key symlinks individually (catch anything installer misses)
ls -la ~/.zshrc ~/.zsh_plugins ~/.p10k.zsh ~/.zlogin
ls -la ~/.config/zsh/
ls -la ~/.config/nvim
ls -la ~/.config/kitty/kitty.conf
ls -la ~/.config/mise/config.toml
ls -la ~/.config/direnv/direnvrc
ls -la ~/.gitconfig
ls -la ~/.vimrc
ls -la ~/.aerospace.toml

# Step 3: Check that symlinks point INTO the dotfiles repo (not stale old paths)
# Expected dotfiles root: ~/personal/dotfiles
# Flag any symlink pointing elsewhere (e.g. ~/configs/dotfiles, /Users/lamdav/...)

# Step 4: Verify template-copied files (not symlinked)
ls -la ~/Library/Application\ Support/Übersicht/widgets/aerospace-mode.jsx 2>/dev/null
grep "__HOME__" ~/Library/Application\ Support/Übersicht/widgets/aerospace-mode.jsx 2>/dev/null \
  && echo "WARN: __HOME__ placeholder not substituted" || echo "OK: placeholder substituted"

# Step 5: Repair if user approves
python installer/main.py install --skip-packages --skip-system
```

## Instructions

1. Read `docs/maintenance.md` first for full context.
2. For `sync`:
   a. Run `python installer/main.py status` and display the output.
   b. Check each key symlink listed above manually — confirm it exists AND points to `~/personal/dotfiles/` (not a stale path like `~/configs/dotfiles` or a hardcoded username).
   c. Check the aerospace-mode.jsx template substitution.
   d. Summarize all findings in a clear table with columns: **File**, **Status** (OK / broken / missing / wrong target), **Expected target**.
   e. For each issue found, ask the user whether to fix it before taking any action.
   f. If approved, run the installer in symlinks-only mode and report what changed.
   g. Re-run status after repair to confirm everything is green.
3. For all other scopes, run the appropriate commands using the Bash tool.
4. Report what was updated and flag anything that needs attention (failed updates, outdated symlinks, etc.).
5. For destructive steps (brew cleanup, removing packages), show the user what would be removed and confirm before proceeding.
6. After running, summarize what changed.
