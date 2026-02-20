# Maintenance

Day-to-day and periodic maintenance commands.

---

## Daily / As Needed

```bash
# Reload shell after config changes
exec zsh

# Reload shell plugins after editing .zsh_plugins
updateplugins && exec zsh

# Allow a new .envrc after creating/editing it
direnv allow
```

---

## Weekly

```bash
# Update Homebrew packages
brew update && brew upgrade

# Update casks (GUI apps)
brew upgrade --cask

# Update mise runtimes
mise upgrade

# Update neovim plugins
nvim --headless "+Lazy sync" +qa

# Update gh extensions
gh extension upgrade --all
```

---

## Monthly

```bash
# Update Oh My Zsh
omz update

# Full mise self-update + runtime upgrade
mise self-update
mise upgrade --bump   # updates to newer minor/major versions

# Clean up old brew versions
brew cleanup

# Check for unused brew packages
brew bundle cleanup --file brew/Brewfile.devtools --dry-run
```

---

## Adding a New Tool

### Brew package
```bash
# 1. Install it
brew install <tool>

# 2. Add to the appropriate Brewfile
echo 'brew "<tool>"' >> brew/Brewfile.devtools

# 3. If it has a shell integration, add to 99_integrations.zsh
```

### Neovim plugin
Add a spec to the `require("lazy").setup({ ... })` table in `nvim/init.lua`:
```lua
{
  "author/plugin-name",
  event = "VeryLazy",   -- lazy load trigger
  opts = {},            -- passed to setup()
},
```
Then run `:Lazy sync` inside nvim.

### mise runtime
```bash
# Add to global config
mise use --global <tool>@<version>
# This updates mise/config.toml automatically
```

### New zsh alias
Add to `zsh/10_aliases.zsh`. Wrap in `command -v <tool>` guard:
```zsh
if command -v <tool> >/dev/null 2>&1; then
  alias <cmd>='<tool> [flags]'
fi
```

### New shell integration
Add to `zsh/99_integrations.zsh` at the appropriate position (mise first, p10k last).

---

## Symlink Audit

```bash
# Check all symlink statuses
python installer/main.py status

# Manually verify a specific symlink
ls -la ~/.config/nvim    # should point to ~/configs/dotfiles/nvim
ls -la ~/.gitconfig      # should point to ~/configs/dotfiles/git/.gitconfig
ls -la ~/.config/mise/config.toml
ls -la ~/.config/direnv/direnvrc
```

---

## Rebuilding from Scratch (symlinks only)

```bash
cd ~/configs/dotfiles
python installer/main.py install --skip-packages --skip-system
exec zsh && updateplugins && exec zsh
```

---

## Troubleshooting Slow Shell Startup

```bash
# Quick benchmark (10 runs)
benchmarkzsh

# Detailed profile — uncomment zprof lines in zsh/.zshrc then:
exec zsh 2>&1 | head -30

# Re-comment zprof lines after done
```

Target: < 200ms cold start.
