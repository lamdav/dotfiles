# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Repository Overview

Comprehensive dotfiles for macOS (primary) and Ubuntu. Covers modular zsh, Kitty terminal, AeroSpace window management, Neovim, status bar (simple-bar/Übersicht), and automated package management.

**Supported Platforms:** macOS (full), Ubuntu/Debian (core tools + shell)

---

## Directory Structure & Symlinks

```
dotfiles/
├── .github/
│   └── workflows/ci.yml  CI: pre-commit + pytest on push/PR (lint/test only)
├── aerospace/          → ~/.aerospace.toml
├── atuin/
│   ├── config.toml     → ~/.atuin/config.toml
│   └── themes/         → ~/.atuin/themes/ (symlink to whole dir; dracula.toml inside)
├── borders/
│   └── bordersrc       → ~/.config/borders/bordersrc
├── brew/               Modular Brewfiles (devtools, k8s, gui, apps, media, optional)
├── claude/
│   ├── settings.json           → ~/.claude/settings.json
│   └── conductor-workspace/    Agent-Deck conductor role config (not symlinked)
├── colors/
│   └── firewatch.conf  Kitty color scheme source
├── direnv/
│   └── direnvrc        → ~/.config/direnv/direnvrc
├── docs/               Runbooks (new-machine.md, maintenance.md, tools.md)
├── git/
│   ├── .gitconfig         → ~/.config/git/.gitconfig  (included by ~/.gitconfig)
│   ├── .gitconfig-personal → ~/.config/git/.gitconfig-personal
│   └── .gitconfig-work    → ~/.config/git/.gitconfig-work
├── glow/
│   └── glow.yml        → ~/Library/Preferences/glow/glow.yml (macOS) or ~/.config/glow/glow.yml (Linux)
├── installer/          Python installer (main.py, symlink_manager.py, …)
├── iterm/              → ~/Library/Application Support/iTerm2/DynamicProfiles/
├── kitty/
│   ├── kitty.conf                → ~/.config/kitty/kitty.conf
│   └── kitty-customizations/     → ~/.config/kitty/kitty-customizations/
├── mise/
│   └── config.toml     → ~/.config/mise/config.toml
├── nvim/
│   └── init.lua        → ~/.config/nvim/  (symlink to whole dir)
├── scripts/
│   └── setup-simple-bar.sh
├── tests/              pytest suite for installer/ (mocked subprocess, tmp_path)
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
| `du` | dust | dust |
| `http`/`https` | xh | xh |
| `jq` | jaq | jaq |
| `top` | btop | btop |
| `vim` / `vi` | nvim | neovim |
| `glow` | glow --tui | glow |

Use `cdi` for interactive directory picker (fzf-powered zoxide).

### Key Shell Functions
- `updateplugins` — regenerate antidote cache
- `benchmarkzsh` — 10-run startup benchmark
- `y` — launch yazi file manager; `cd`s the shell to wherever you exited it
- `mkcd <dir>` — mkdir + cd
- `extract <file>` — universal archive extractor
- `envrc-init` — scaffold `.envrc` in the current directory from a numbered menu over the direnv layout helpers below (multi-select, e.g. `1 5` for `uv` + `mise`); run it yourself after `git init` or in any new project dir. No-ops if `.envrc` already exists.
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

"pypi:pre-commit" = "latest"
"pypi:poetry"     = "latest"
"pypi:commitizen" = "latest"
```

Standalone Python CLI tools (pre-commit, poetry, commitizen) are installed via mise's `pypi:` backend, not pipx/brew — a pipx venv hard-links to a specific brew Python formula, so a `brew autoremove` that drops that formula silently breaks the venv. mise pins its own Python runtime instead, so `mise upgrade` is the only thing that moves it.

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

**Work profile:** repos under `~/work/` auto-load `~/.config/git/.gitconfig-work` the same way. `git/.gitconfig-work` ships with placeholder `[user]` values (`REPLACE_ME`) — fill in the real work name/email before relying on it; it's intentionally not pre-filled since this file is checked into the repo.

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

**Quick-setup:** `envrc-init` (in `zsh/10_aliases.zsh`) offers a numbered menu over the layouts above and writes `.envrc` for you — run it manually in a project dir (e.g. right after `git init`). git has no hook that fires on `git init` itself (`githooks(5)` has no `post-init`), so this is a standalone command rather than something wired into git.

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

**Key tools in devtools:** git, git-delta, gh, mise, neovim, fzf, fd, ripgrep, bat, eza, zoxide, direnv, btop, jaq, xh, tmux

**Third-party taps (`Brewfile.k8s`, `Brewfile.gui`):** Homebrew 6.x requires `brew trust --tap <name>` before `brew bundle` will install formulae/casks from a non-official tap — otherwise they're silently skipped with no error. `installer/main.py install` trusts a Brewfile's taps automatically before bundling; the manual `brew bundle` runbook in `docs/new-machine.md` trusts them explicitly first. Check with `brew tap-info --json <tap>` → `"trusted"` if a bundled tool (e.g. `k9s`, `aerospace`, `borders`) seems missing after install.

**No `Brewfile.databases`:** redis/mongo for local dev are run via docker (per-project, not a persistent host service), not installed natively — there's deliberately no Brewfile for them.

---

## FZF Integration

Keybindings (active in shell):
- `Ctrl+T` — fuzzy file picker (uses fd, respects .gitignore)
- `Alt+C` — fuzzy cd (uses fd, dirs only)

Default options: `--height 40% --layout=reverse --border`

Uses `fd` as backend on macOS, `fdfind` on Ubuntu — both configured in the platform `99_integrations` layer. Hidden files included, `.git` excluded.

**Note:** `Ctrl+R` is bound to atuin, not fzf — atuin's `99_integrations.zsh` block loads after fzf's and overrides the history widget. See Atuin below.

## Atuin (Shell History)

Context-aware history search (`Ctrl+R`) — filters by directory, exit code, and duration, not just substring match on the command text. Shared `99_integrations.zsh` module; init must stay ordered after fzf's.

**Config:** `atuin/config.toml` → `~/.atuin/config.toml` (not XDG-based — atuin always uses `~/.atuin/` on both macOS and Linux). Daemon mode is enabled (`[daemon] enabled/autostart = true`) and kept running via `brew services start atuin` (launchd-managed), since `autostart` alone only spins the daemon up on demand and won't start it from a cold shell.

**Theme:** `atuin/themes/dracula.toml` (whole `themes/` dir symlinked to `~/.atuin/themes/`) — a custom theme since atuin ships no Dracula option itself, mapping its `Base`/`Annotation`/`Guidance`/`Important`/`AlertInfo`/`AlertWarn`/`AlertError` meanings to the same Dracula hex palette already used by `bat --theme=Dracula` and the `#6272a4` zsh-autosuggestions color. Active via `[theme] name = "dracula"` in `config.toml`.

```bash
atuin search <query>   # search from the CLI
atuin stats             # usage stats
atuin daemon status    # confirm the daemon is running and healthy
```

Sync across machines is opt-in (`atuin register`/`atuin login`), not configured by default. Threads capture (resuming Claude Code/Codex/etc. sessions via `atuin threads resume`) is also off by default — `atuin config enable threads` turns it on.

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

Tab bar uses kitty's native `tab_bar_style fade` (`kitty.conf`) — an earlier custom `tab_bar.py` script was tried and abandoned; there is no custom tab bar script in this setup anymore.

**SSH from Kitty:** `alias ssh='kitten ssh'` is active in `zsh/macos/10_aliases.zsh` when `$TERM == xterm-kitty`. This auto-pushes kitty terminfo to the remote before the session. The Ubuntu installer also installs terminfo server-side as a fallback.

---

## Installer (installer/)

```bash
dot install           # full install
dot install --skip-packages  # skip brew bundle
dot install --skip-shell     # skip zsh/oh-my-zsh setup
dot install --skip-system    # skip macOS system preferences
dot status            # check symlink status
dot status --fix      # create/repair any symlink reported as broken or missing
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
changelog body, and creates an annotated tag. It refuses up front (clear error,
no commit made) if the target tag name already exists — e.g. a stale tag left
pointing at a commit orphaned by a rebase.

`git-cliff`'s bump flag is `--bump <major|minor|patch>` (one flag, optional
value) — there is no `--bump-major`/`--bump-minor`/`--bump-patch`.

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
| Symlink broken | `dot status --fix` (re-creates broken/missing symlinks only; prompts before replacing a non-symlink file) |
| AeroSpace hotkeys don't work (mouse doesn't move) | Key is intercepted before AeroSpace. Check: `pgrep skhd` (yabai leftover — `brew services stop skhd`); `defaults read com.googlecode.iterm2 GlobalKeyMap` (remove conflicting iTerm2 global bindings) |
| AeroSpace hotkeys work via CLI but not keyboard | Same as above — another process has a CGEventTap for that key combination |
| simple-bar mode indicator always shows "main" | `aerospace-mode.jsx` has wrong home path. Re-run installer or: `sed "s|__HOME__|$HOME|g" ~/configs/dotfiles/ubersicht/aerospace-mode.jsx > ~/Library/Application\ Support/Übersicht/widgets/aerospace-mode.jsx` |
| Ubuntu: `fd` not found | `fd` is `fdfind` on Debian/Ubuntu — `linux/10_aliases.zsh` aliases it automatically |
| Ubuntu: `bat` not found | `bat` is `batcat` on Debian/Ubuntu — `linux/10_aliases.zsh` aliases it automatically |
| `dot next` exits 1 immediately | No unreleased conventional commits since last tag |
| `dot release` errors "tag already exists" | A tag with that name is already present — often a stale one left pointing at a commit orphaned by a rebase. Fix or delete it (`git tag -d vX.Y.Z`) before releasing again |
| detect-secrets flags a real false positive | Add an inline `# pragma: allowlist secret` comment on that line, or regenerate `.secrets.baseline` (`detect-secrets scan >\| .secrets.baseline`) |
| glow TUI exits instead of scrolling left on wide code blocks | Upstream behavior, not configurable: glow's pager has no horizontal scroll; `h`/`left`/`delete` are hard-bound to "unload document" (`ui/ui.go`), which exits when there's no file list to fall back to (as with the `glow --tui <file>` alias). Use `batmd <file>` instead — it pipes through `bat`/`less`, which supports real left/right arrow panning |

---

## Code Quality (pre-commit)

pre-commit is configured (`.pre-commit-config.yaml`) and installed in the git hook.

```bash
pre-commit run --all-files   # run all hooks manually
pre-commit autoupdate        # update hook versions — only touches pre-commit-hooks/shellcheck-py
```

**Hooks:** trailing-whitespace, end-of-file-fixer, check-yaml, check-merge-conflict, shellcheck (all `rev:`-pinned, mirror repos) — then black, isort, detect-secrets (`repo: local`, see below).

**Single source of truth for Python tool versions:** black, isort, and detect-secrets are declared as dev dependencies in `pyproject.toml`/`uv.lock` and run as `repo: local` hooks whose `entry` is `uv run <tool>` — there is no separate `rev:` pin for them. This exists because `uv.lock` and a `rev:`-pinned mirror repo previously drifted (black/isort resolved to different versions locally vs. under pre-commit) with no warning. `pre-commit autoupdate` has nothing to bump for these three; update their versions with `uv lock --upgrade-package <name>` (or `uv add --dev <name>` for a new tool) instead. shellcheck and the `pre-commit-hooks` repo have no project-dependency equivalent, so their `rev:` here is still their legitimate version source of truth.

**Gotcha:** shellcheck only runs on `.sh`/`.bash` files — `.zsh` files are excluded because shellcheck doesn't understand zsh-specific syntax (`precmd_functions`, `add-zsh-hook`, `N` glob qualifier, etc.).

**detect-secrets:** baseline at `.secrets.baseline`, generated via `detect-secrets scan >| .secrets.baseline` (use `>|`, not `>` — `no_clobber`). Its own heuristic filters (`is_lock_file`, `is_templated_secret`, `is_indirect_reference`, etc.) clear most false positives automatically at hook time — a fresh `scan` output rarely needs manual `is_secret` editing. If a hook run ever reports something already in the baseline as new, regenerate the baseline fresh rather than hand-editing it; the two code paths (`detect-secrets scan` vs. the `detect-secrets-hook` the local hook invokes) don't always agree on an edited file's exact entry shape.

---

## Testing

```bash
uv run pytest           # run the installer test suite
uv run pytest -v        # verbose
```

Tests live in `tests/`, covering `installer/main.py` (release command logic —
all `subprocess.run` calls mocked, no real git commands run) and
`installer/symlink_manager.py` (`create_symlink` against `tmp_path`, plus a
sanity check that the `SymlinkSpec` tables have no duplicate targets). Nothing
in the suite touches a real home directory or repository.

---

## CI (.github/workflows/ci.yml)

Single job on every push to `master` and every PR: `uv sync --dev`, then
`uv run pre-commit run --all-files`, then `uv run pytest`. It runs through
`uv` (not a bare `actions/setup-python` + `pre-commit/action`) because the
local black/isort/detect-secrets hooks shell out to `uv run <tool>` and need
the project's synced venv on PATH — a plain pre-commit install has no `uv` and
would fail on those three hooks. **CI never runs `dot install` or
`dot release`**, since both mutate a real home directory, brew, or macOS
system preferences and have no safe meaning on a hosted runner. Local
pre-commit + manual testing is still the loop for anything beyond the
installer's Python code.

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
