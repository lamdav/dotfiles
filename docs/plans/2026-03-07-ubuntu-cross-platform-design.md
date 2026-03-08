---
# Ubuntu Server Support — Cross-Platform Zsh Design

## Problem

The dotfiles are macOS-centric. Several zsh modules hardcode Homebrew paths, macOS-only commands (`open`, `pbcopy`, `osascript`), and the installer's Ubuntu support is skeletal. This design adds clean Ubuntu server support and makes the zsh configuration properly cross-platform.

## Goals

- Clean Ubuntu server setup via SSH (no GUI apps)
- Cross-platform zsh that works on macOS and any Linux distro without inline OS guards cluttering shared files
- Kitty terminal awareness when SSH-ing from macOS Kitty into Ubuntu
- Extensible to other Linux distros with minimal effort

## Architecture: Layered Zsh Directory Structure

```
zsh/
├── *.zsh           # Universal — any POSIX system, command -v guards only
├── macos/          # macOS-specific (Homebrew, open, pbcopy, kitten)
├── linux/          # Linux family base — ALL Linux distros share this
└── ubuntu/         # Ubuntu-specific thin shim (near-empty for shell config)
```

**Key principle:** `linux/` carries the heavy lifting for all Linux distros. `ubuntu/` is intentionally thin — most "Ubuntu-specific" shell config is actually Linux-generic. Adding Arch/Fedora later only requires a new thin directory; `linux/` and shared modules need zero changes.

## Loader: Interleaved Platform Loading (.zshrc)

Platform is detected once at startup:

```zsh
if [[ "$OSTYPE" == darwin* ]]; then
  ZSH_OS_FAMILY="macos"
  ZSH_DISTRO="macos"
elif [[ "$OSTYPE" == linux* ]]; then
  ZSH_OS_FAMILY="linux"
  ZSH_DISTRO="${$(grep ^ID= /etc/os-release 2>/dev/null)#ID=}"
  ZSH_DISTRO="${ZSH_DISTRO:-linux}"
fi
```

For each shared module, the loader sources three layers in order:
1. `~/.config/zsh/{module}.zsh` — shared base
2. `~/.config/zsh/$ZSH_OS_FAMILY/{module}.zsh` — family layer (skipped when `family == distro`, i.e. macOS)
3. `~/.config/zsh/$ZSH_DISTRO/{module}.zsh` — distro layer

This means macOS PATH extensions load *immediately after* shared PATH setup — module ordering semantics are fully preserved.

## Platform Module Contents

### macos/02_environment.zsh
- `BROWSER=open`
- `HOMEBREW_NO_ANALYTICS=1`
- Homebrew fpath (`/opt/homebrew/share/zsh/site-functions`)
- `/opt/homebrew/bin`, `/opt/homebrew/sbin` PATH entries
- Google Cloud SDK path include

### macos/10_aliases.zsh
- `alias refreshbar='osascript ...'` (Übersicht widget refresh)
- `[[ "$TERM" == "xterm-kitty" ]] && alias ssh='kitten ssh'`

### linux/02_environment.zsh
- `~/.local/bin` at front of PATH (mise, fzf, zoxide install here)
- XDG base dir exports if not already set

### linux/10_aliases.zsh
- `fdfind` → `fd` alias (Debian/Ubuntu rename)
- `batcat` → `bat` alias + fix `cat` alias (Debian/Ubuntu rename)
- Fix FZF commands to use `fdfind` when `fd` not available

### ubuntu/
Intentionally near-empty for shell config. Most Linux-generic things live in `linux/`. Distro-specific overrides (e.g. apt completions) go here.

## Shared Module Changes

### 02_environment.zsh — remove
- `BROWSER=open` — macOS-only `open` command
- `HOMEBREW_NO_ANALYTICS`
- Homebrew fpath block
- `/opt/homebrew/` PATH entries
- Google Cloud SDK source block

### 99_integrations.zsh — modernize fzf
```zsh
# Remove (macOS Homebrew-only):
if [[ -f "/opt/homebrew/opt/fzf/shell/key-bindings.zsh" ]]; then ...

# Replace with (cross-platform, fzf 0.48+):
if command -v fzf >/dev/null 2>&1; then
  eval "$(fzf --zsh)"
fi
```

### 10_aliases.zsh — remove
- `alias refreshbar='osascript...'` → moves to `macos/10_aliases.zsh`

## Ubuntu Installer Phases

| Phase | What |
|-------|------|
| 1 — apt base | `zsh git git-lfs curl wget jq ripgrep fd-find bat tmux direnv build-essential software-properties-common` |
| 2 — neovim | `ppa:neovim-ppa/unstable` → `apt install neovim` |
| 3 — eza | Official eza apt repo → `apt install eza` |
| 4 — fzf | GitHub releases binary → `~/.local/bin/fzf` |
| 5 — mise | `curl https://mise.run \| sh` |
| 6 — zoxide | curl install script → `~/.local/bin` |
| 7 — kitty terminfo | curl xterm-kitty terminfo → `tic -x -` |

Each phase warns and continues on failure — no hard abort.

## Kitty SSH Integration

Belt-and-suspenders approach:
- **Ubuntu server (server-side):** kitty terminfo installed via Phase 7. Any SSH client sending `TERM=xterm-kitty` works correctly — ncurses apps, tmux, bat all render properly.
- **macOS client (client-side):** `alias ssh='kitten ssh'` in `macos/10_aliases.zsh`, guarded by `[[ "$TERM" == "xterm-kitty" ]]`. `kitten ssh` auto-pushes terminfo before the session starts.

## Installer Symlink Changes

`setup_shell_config()` additionally symlinks platform subdirectories:
- macOS: `zsh/macos/` → `~/.config/zsh/macos/`
- Linux: `zsh/linux/` → `~/.config/zsh/linux/`, `zsh/{distro}/` → `~/.config/zsh/{distro}/`

`setup_kitty_config()` skips entirely on Linux (no Kitty on servers).

## Future Extensibility

Adding Arch Linux support:
1. Create `zsh/arch/` with Arch-specific overrides (pacman completions, AUR paths)
2. Add `ArchPackageManager` in `installer/package_managers.py`

The loader, `linux/` family layer, and shared modules require zero changes.
