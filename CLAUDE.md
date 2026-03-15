# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Repository Overview

Comprehensive dotfiles for macOS (primary) and Ubuntu. Covers modular zsh, Kitty terminal, AeroSpace window management, Neovim, status bar (simple-bar/Übersicht), and automated package management.

**Supported Platforms:** macOS (full), Ubuntu/Debian (core tools + shell)

---

## Directory Structure & Symlinks

```
dotfiles/
├── aerospace/          → ~/.aerospace.toml
├── borders/
│   └── bordersrc       → ~/.config/borders/bordersrc
├── brew/               Modular Brewfiles (devtools, k8s, gui, apps, media, optional)
├── colors/
│   └── firewatch.conf  Kitty color scheme source
├── direnv/
│   └── direnvrc        → ~/.config/direnv/direnvrc
├── docs/               Runbooks (new-machine.md, maintenance.md, tools.md)
├── git/
│   ├── .gitconfig         → ~/.config/git/.gitconfig  (included by ~/.gitconfig)
│   └── .gitconfig-personal → ~/.config/git/.gitconfig-personal
├── installer/          Python installer (main.py, symlink_manager.py, …)
├── iterm/              → ~/Library/Application Support/iTerm2/DynamicProfiles/
├── kitty/
│   ├── kitty.conf                → ~/.config/kitty/kitty.conf
│   ├── kitty-customizations/     → ~/.config/kitty/kitty-customizations/
│   └── kitty-customizations/tab_bar.py → ~/.config/kitty/tab_bar.py  (also linked at root)
├── mise/
│   └── config.toml     → ~/.config/mise/config.toml
├── nvim/
│   └── init.lua        → ~/.config/nvim/  (symlink to whole dir)
├── scripts/
│   └── setup-simple-bar.sh
├── ubersicht/
│   ├── simple-bar/simplebarrc  → COPIED (not symlinked) to ~/.simplebarrc
│   │                              Modified at runtime by sync-simplebar-displays.sh
│   ├── simple-bar/aerospace-mode-tracker.sh → ~/.config/ubersicht/simple-bar/aerospace-mode-tracker.sh
│   ├── simple-bar/sync-simplebar-displays.sh → ~/.config/ubersicht/simple-bar/sync-simplebar-displays.sh
│   └── aerospace-mode.jsx      → COPIED (not symlinked) to ~/Library/Application Support/Übersicht/widgets/
│                                  Contains __HOME__ placeholder substituted at install time
├── vim/
│   └── .vimrc          → ~/.vimrc
└── zsh/
    ├── .zshrc          → ~/.zshrc
    ├── .zsh_plugins    → ~/.zsh_plugins
    ├── .p10k.zsh       → ~/.p10k.zsh
    ├── .zlogin
    ├── 01-99_*.zsh     → ~/.config/zsh/ (shared modules, all platforms)
    ├── macos/          → ~/.config/zsh/macos/  (macOS-specific overrides)
    ├── linux/          → ~/.config/zsh/linux/  (Linux family base, all distros)
    └── ubuntu/         → ~/.config/zsh/ubuntu/ (Ubuntu-specific overrides — currently empty, placeholder for future)
```

---

## Shell Architecture (zsh/)

**Framework:** Oh My Zsh + antidote plugin manager + Powerlevel10k

### Module Load Order (critical — do not reorder)

| File | Purpose | Key constraint |
|------|---------|---------------|
| `01_options.zsh` | History, globbing, safety (`no_clobber`) | No deps |
| `02_environment.zsh` | PATH, FPATH, exports, tool env vars | Must set FPATH before compinit |
| `03_plugins.zsh` | antidote init + plugin load | Adds to FPATH; use `>|` not `>` for cache writes |
| `04_completion.zsh` | compinit + completion config | Requires complete FPATH |
| `05_keybindings.zsh` | Key bindings | Requires completion system |
| `06_lazy-loading.zsh` | Generic lazy_load/group_lazy_load helpers | Version tools now handled by mise |
| `10_aliases.zsh` | Aliases + shell functions | Requires tools on PATH |
| `99_integrations.zsh` | mise, fzf, zoxide, direnv, p10k | Runs last; kitty in macos/ |

**Important:** `no_clobber` is set in `01_options.zsh`. Any redirect that writes to an existing file must use `>|` instead of `>`. This applies in `03_plugins.zsh` and the `updateplugins` function.

### Platform Layer Loading

Each module loads in three layers (interleaved):
1. **Shared** (`~/.config/zsh/{module}.zsh`) — universal, `command -v` guards only
2. **OS family** (`~/.config/zsh/linux/{module}.zsh`) — all Linux distros; skipped on macOS
3. **Distro** (`~/.config/zsh/macos/{module}.zsh` or `ubuntu/`) — distro-specific overrides

**Platform files by module:**

| Module | macos/ | linux/ |
|--------|--------|--------|
| `02_environment` | Homebrew PATH, `BROWSER=open`, gcloud | `~/.local/bin` priority, XDG dirs |
| `04_completion` | GCloud SDK completion, Homebrew tool completions | — |
| `10_aliases` | `refreshbar`, `ssh='kitten ssh'` | `fd`→`fdfind`, `find`→`fdfind`, `bat`→`batcat` shims |
| `99_integrations` | fd FZF backend, kitty functions | fdfind FZF backend |

Adding a new distro (e.g. Arch): create `zsh/arch/` — shared and `linux/` modules need no changes.

### Active Plugins (zsh/.zsh_plugins)
- `mfaerevaag/wd` — warp directory bookmarks
- `ael-code/zsh-colored-man-pages`
- `zsh-users/zsh-completions`
- `zsh-users/zsh-autosuggestions` — highlight: `#6272a4` (Dracula comment), strategy: history→completion
- `desyncr/auto-ls`
- `hlissner/zsh-autopair`
- `romkatv/powerlevel10k` — LAST group
- `zdharma-continuum/fast-syntax-highlighting` — LAST group

To update: `updateplugins && exec zsh`

### Modern Command Aliases

| Typed | Runs | Tool |
|-------|------|------|
| `cd` | zoxide smart cd (falls back for `cd -`, `cd ~`) | zoxide `--cmd cd` |
| `ls` / `ll` | eza with git status | eza |
| `tree` | eza --tree | eza |
| `cat` | bat --style=plain | bat |
| `find` | fd | fd |
| `grep` | rg | ripgrep |
| `top` | btop | btop |
| `vim` / `vi` | nvim | neovim |

Use `cdi` for interactive directory picker (fzf-powered zoxide).

### Key Shell Functions
- `updateplugins` — regenerate antidote cache
- `benchmarkzsh` — 10-run startup benchmark
- `mkcd <dir>` — mkdir + cd
- `extract <file>` — universal archive extractor
- `kitty-help` — print all kitty keybindings *(macOS only — defined in `macos/99_integrations.zsh`)*
- `ksave/kload/ksplit/knotify/ktheme` — kitty session helpers *(macOS only)*

---

## Version Management (mise)

mise replaces nvm, pyenv, and jabba entirely.

**Global config:** `mise/config.toml` → `~/.config/mise/config.toml`

```toml
[tools]
node   = "lts"
python = "latest"
go     = "latest"
java   = "temurin-21"
```

**Common commands:**
```bash
mise install                  # install all tools from config
mise use node@20              # switch version in current project
mise use --global python@3.12 # switch global version
mise ls                       # list installed versions
mise exec -- node script.js   # run with mise-managed runtime
```

**Per-project:** add `.mise.toml` to project root. direnv's `use mise` activates it automatically.

---

## Neovim (nvim/)

Config: `nvim/init.lua` → `~/.config/nvim/` (whole directory symlinked)

**Plugin manager:** lazy.nvim (auto-bootstraps on first launch)

**Key plugins:**
- `Mofiqul/dracula.nvim` — colorscheme (matches `BAT_THEME=Dracula`)
- `nvim-telescope/telescope.nvim` + `telescope-fzf-native` — fuzzy finding
- `nvim-treesitter` — syntax, indent
- `neovim/nvim-lspconfig` + `mason` + `mason-lspconfig` — LSP servers
- `nvim-cmp` + `luasnip` — completion
- `lewis6991/gitsigns.nvim` — git hunk indicators
- `nvim-neo-tree/neo-tree.nvim` — file explorer
- `nvim-lualine/lualine.nvim` — statusline
- `folke/which-key.nvim` — keymap hints

**LSP servers (auto-installed by mason):** `gopls`, `pyright`, `ts_ls`, `yamlls`, `lua_ls`, `dockerls`

**LSP setup uses Neovim 0.11 API:** `vim.lsp.config()` + `vim.lsp.enable()` — NOT `require('lspconfig').server.setup()`

**Leader key:** `<Space>`

Key mappings:
```
<leader>ff  Telescope find files
<leader>fg  Telescope live grep
<leader>fb  Telescope buffers
<leader>fr  Recent files
<leader>e   Neo-tree toggle
gd / gr / K  LSP: definition / references / hover
<leader>rn  LSP rename
<leader>ca  LSP code action
<leader>cf  Format file
]h / [h     Next/prev git hunk
<leader>hs  Stage hunk
```

**First launch:** open `nvim`, run `:Lazy sync` to install plugins, then `:MasonToolsInstall` if LSP servers didn't auto-install.

---

## Git Configuration (git/)

**Aliases:**
```bash
git s           # status
git co          # checkout
git ci          # commit
git amend       # commit --amend --no-edit
git unstage     # reset HEAD --
git undo        # reset --soft HEAD~1
git cleanup     # delete merged branches
git graph       # visual log
git logp        # compact log
git l           # log --oneline
git f/p/pl      # fetch/push/pull
git track/untrack  # manage assume-unchanged
```

**Settings:** `pull.rebase=true`, `push.autoSetupRemote=true`, `fetch.prune=true`, `rebase.autostash=true`, `rerere.enabled=true`

**Personal profile:** repos under `~/personal/` auto-load `~/.config/git/.gitconfig-personal` via `[includeIf]`. Edit `git/.gitconfig-personal` for personal identity/settings.

**Git config layering:** `~/.gitconfig` (user-managed) → includes `~/.config/git/.gitconfig` (symlink to dotfiles) → includes `~/.config/git/.gitconfig-local` (machine-local overrides, not in repo).

**Pager:** delta with side-by-side, line numbers, navigate mode

---

## direnv (direnv/)

Config: `direnv/direnvrc` → `~/.config/direnv/direnvrc`

Provides layout helpers usable in `.envrc` files:
```bash
layout uv              # creates/activates .venv via uv; auto-syncs pyproject.toml/requirements.txt
layout uv my-cmd       # same + generates zsh completion for my-cmd (sourced via precmd hook on enter, cleaned up on exit)
layout python   # creates/activates .venv via python3 -m venv
layout node     # adds node_modules/.bin to PATH
layout go       # sets project-local GOPATH
use mise        # activates .mise.toml (built-in direnv 2.32+)
```

After editing `.envrc`: `direnv allow`

---

## Package Management (brew/)

Modular Brewfiles — run each explicitly:
```bash
brew bundle --file brew/Brewfile.devtools   # core tools (fzf, fd, gh, mise, nvim, direnv...)
brew bundle --file brew/Brewfile.k8s        # helm, kubectx, k9s
brew bundle --file brew/Brewfile.gui        # aerospace, ubersicht, fonts
brew bundle --file brew/Brewfile.apps       # raycast, 1password, vscode, chrome...
brew bundle --file brew/Brewfile.media      # media tools
brew bundle --file brew/Brewfile.optional   # slack, discord
```

**Key tools in devtools:** git, git-delta, gh, mise, neovim, fzf, fd, ripgrep, bat, eza, zoxide, direnv, btop, jq, httpie, tmux

---

## FZF Integration

Keybindings (active in shell):
- `Ctrl+R` — fuzzy history search
- `Ctrl+T` — fuzzy file picker (uses fd, respects .gitignore)
- `Alt+C` — fuzzy cd (uses fd, dirs only)

Default options: `--height 40% --layout=reverse --border`

Uses `fd` as backend on macOS, `fdfind` on Ubuntu — both configured in the platform `99_integrations` layer. Hidden files included, `.git` excluded.

---

## AeroSpace (aerospace/)

i3-inspired tiling WM. Workspaces: 1-9, S (Spotify), F (Finder), M (Mail).

Key bindings (all `alt+`):
- `h/j/k/l` — focus window
- `shift+h/j/k/l` — move window
- `1-9`, `s/f/m` — switch workspace
- `shift+1-9`, `shift+s/f/m` — move window to workspace
- `shift+;` — service mode
- `shift+r` — resize mode
- `shift+'` — media mode (Spotify controls)
- `tab` — back-and-forth workspace

Integrates with simple-bar via `exec-on-workspace-change`.

**Useful CLI commands:**
```bash
aerospace reload-config                    # reload after config changes
aerospace focus left/right/up/down         # focus window programmatically
aerospace list-windows --workspace focused # list windows on current workspace
aerospace list-windows --all               # list all windows across workspaces
aerospace mode main                        # force-reset to main mode
```

### Known Conflicts (check if hotkeys stop working)

**skhd** — If migrating from a yabai setup, skhd may still be running with bindings that intercept `alt+h/j/k/l` before AeroSpace sees them. Diagnose: `pgrep skhd`. Fix: `brew services stop skhd` or `brew uninstall skhd`.

**iTerm2 GlobalKeyMap** — iTerm2 can register global key intercepts even when it is not the focused app. Option+H and Option+L are commonly mapped to Emacs word-navigation escape sequences. Check: `defaults read com.googlecode.iterm2 GlobalKeyMap`. Fix: remove conflicting entries via iTerm2 → Preferences → Keys → Key Bindings.

**Diagnosis approach** when a binding does nothing (mouse doesn't move, no visible effect):
1. `aerospace list-mode` (or check `/tmp/aerospace-current-mode`) — confirm you are in `main` mode
2. `aerospace focus left` from terminal — if CLI works but hotkey doesn't, the key is being intercepted
3. Temporarily rebind the key to `workspace 1` and test — if workspace doesn't switch, key never reaches AeroSpace
4. `pgrep skhd` — check for skhd
5. `defaults read com.googlecode.iterm2 GlobalKeyMap` — check iTerm2 global keys

---

## Kitty Terminal (kitty/)

Color scheme: Firewatch. Font: FiraCode Nerd Font with ligatures.

Key shortcuts: `cmd+t` new tab, `cmd+d` split horizontal, `cmd+shift+d` split vertical, `cmd+w` close pane, `cmd+1-9` jump to tab, `cmd+k` clear+scrollback.

Hotkey window (Quake-style): `ctrl+\`` — registered via `kitten quick-access-terminal`.

**Note:** `tab_bar.py` is symlinked to both `~/.config/kitty/kitty-customizations/tab_bar.py` (via dir symlink) AND directly to `~/.config/kitty/tab_bar.py` — kitty requires it at the config root to load it as a custom tab bar.

**SSH from Kitty:** `alias ssh='kitten ssh'` is active in `zsh/macos/10_aliases.zsh` when `$TERM == xterm-kitty`. This auto-pushes kitty terminfo to the remote before the session. The Ubuntu installer also installs terminfo server-side as a fallback.

---

## Installer (installer/)

```bash
dot install           # full install
dot install --skip-packages  # skip brew bundle
dot install --skip-shell     # skip zsh/oh-my-zsh setup
dot install --skip-system    # skip macOS system preferences
dot status            # check symlink status
```

Components installed:
- Shell config (zsh, oh-my-zsh, plugins, p10k)
- Git + Neovim + Vim configs
- mise + direnv configs
- Kitty config + customizations
- macOS only: AeroSpace, iTerm2, Übersicht, system preferences, Kitty hotkey window

**Ubuntu server install** (run on the remote machine after cloning):
```bash
dot install --skip-system
```
Installs in phases: apt base tools → Neovim (unstable PPA) → eza → gh → git-delta → fzf → antidote → mise → zoxide → kitty terminfo. macOS-only components (AeroSpace, Übersicht, Kitty config, system prefs) are automatically skipped.

**Template files** (copied with substitution, not symlinked):
- `ubersicht/aerospace-mode.jsx` — contains `__HOME__` placeholder replaced with the actual home directory at install time. Do not symlink this file; run the installer to redeploy after edits.
- `ubersicht/simple-bar/simplebarrc` — copied (not symlinked) to `~/.simplebarrc`. The live copy is modified at runtime by `sync-simplebar-displays.sh` to inject machine-specific `customAeroSpaceDisplayIndexes`. The dotfiles version is the stable baseline with `{}`. To persist UI setting changes back to dotfiles, manually diff and copy the relevant fields.

---

## Versioning & Releases

Versioning follows [SemVer](https://semver.org). Changelogs are generated by
[git-cliff](https://git-cliff.org) from conventional commits. Config: `[tool.git-cliff]` in `pyproject.toml`.

```bash
dot release            # auto-bump based on commits (feat→minor, fix→patch, breaking→major)
dot release --patch    # force patch bump
dot release --minor    # force minor bump
dot release --major    # force major bump
dot next               # preview next version; exits 1 if nothing to release
```

`dot release` generates `CHANGELOG.md`, commits as `chore: release vX.Y.Z` with
changelog body, and creates an annotated tag.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Shell startup slow | `benchmarkzsh`, uncomment zprof in `.zshrc` |
| Plugins not loading | `updateplugins && exec zsh` |
| `file exists` error on redirect | Check for `>` vs `>|` — `no_clobber` is set |
| mise tool not found | `mise install`, check `mise ls` |
| direnv not loading | `direnv allow` in project dir |
| Neovim plugins missing | Open nvim, run `:Lazy sync` |
| LSP not working | `:Mason`, install server; check `:LspInfo` |
| Kitty config error | `kitty --config ~/.config/kitty/kitty.conf --version` |
| Git delta not showing | `git show` — verify delta is on PATH |
| Symlink broken | `dot status` |
| AeroSpace hotkeys don't work (mouse doesn't move) | Key is intercepted before AeroSpace. Check: `pgrep skhd` (yabai leftover — `brew services stop skhd`); `defaults read com.googlecode.iterm2 GlobalKeyMap` (remove conflicting iTerm2 global bindings) |
| AeroSpace hotkeys work via CLI but not keyboard | Same as above — another process has a CGEventTap for that key combination |
| simple-bar mode indicator always shows "main" | `aerospace-mode.jsx` has wrong home path. Re-run installer or: `sed "s|__HOME__|$HOME|g" ~/configs/dotfiles/ubersicht/aerospace-mode.jsx > ~/Library/Application\ Support/Übersicht/widgets/aerospace-mode.jsx` |
| Ubuntu: `fd` not found | `fd` is `fdfind` on Debian/Ubuntu — `linux/10_aliases.zsh` aliases it automatically |
| Ubuntu: `bat` not found | `bat` is `batcat` on Debian/Ubuntu — `linux/10_aliases.zsh` aliases it automatically |
| `dot next` exits 1 immediately | No unreleased conventional commits since last tag |

---

## Code Quality (pre-commit)

pre-commit is configured (`.pre-commit-config.yaml`) and installed in the git hook.

```bash
pre-commit run --all-files   # run all hooks manually
pre-commit autoupdate        # update hook versions
```

**Hooks:** trailing-whitespace, end-of-file-fixer, check-yaml, check-merge-conflict, black, isort, shellcheck

**Gotcha:** shellcheck only runs on `.sh`/`.bash` files — `.zsh` files are excluded because shellcheck doesn't understand zsh-specific syntax (`precmd_functions`, `add-zsh-hook`, `N` glob qualifier, etc.).

---

## Maintenance

```bash
# Full update
brew update && brew upgrade
updateplugins && exec zsh

# Update neovim plugins
nvim --headless "+Lazy sync" +qa

# Update mise tools
mise self-update && mise upgrade

# Update gh
gh extension upgrade --all
```
