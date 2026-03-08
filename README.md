# lamdav's Dotfiles

Comprehensive dotfiles for macOS (primary) and Ubuntu. Covers modular zsh, Kitty terminal, AeroSpace window management, Neovim, status bar (simple-bar/Übersicht), and automated package management.

**Supported Platforms:** macOS (full), Ubuntu/Debian (core tools + shell)

## Installation

### Python Installer (Recommended)

```bash
# Clone the repo
git clone https://github.com/lamdav/dotfiles.git ~/configs/dotfiles
cd ~/configs/dotfiles

# Install dependencies and run
uv sync
uv run install-dotfiles

# Check symlink status
uv run install-dotfiles status

# Full install, skip macOS system preferences
uv run install-dotfiles install --skip-system
```

**Options:**
- `--skip-packages` — skip Homebrew/APT package installation
- `--skip-shell` — skip zsh/Oh My Zsh setup
- `--skip-system` — skip macOS system preferences

### Ubuntu Server

```bash
python installer/main.py install --skip-system
```

Installs in phases: apt base tools → Neovim (unstable PPA) → eza → gh → git-delta → fzf → antidote → mise → uv → zoxide → kitty terminfo.

## Post-Installation

```bash
exec zsh           # reload shell
updateplugins      # refresh zsh plugins
mise install       # install runtimes from mise/config.toml
nvim               # open nvim, run :Lazy sync on first launch
gh auth login      # authenticate GitHub CLI
```

## Key Tools

| Category | Tool | Notes |
|----------|------|-------|
| Shell | zsh + antidote + p10k | Modular, layered per-OS config |
| Editor | Neovim (lazy.nvim) | LSP via mason, Telescope, Treesitter |
| Version mgmt | mise | Replaces nvm, pyenv, jabba |
| Python env | uv | Replaces poetry, pip for project work |
| Window mgmt | AeroSpace | macOS only, i3-inspired |
| Terminal | Kitty | Firewatch theme, FiraCode Nerd Font |
| Status bar | simple-bar + Übersicht | macOS only |
| Git pager | delta | Side-by-side diffs |

## Development (installer)

```bash
uv sync              # install deps
uv run install-dotfiles install --skip-system
uv run black .       # format
uv run isort .       # sort imports
```

## Requirements

- **Python Installer**: Python 3.10+, uv
- **Supported Systems**:
  - macOS (tested on Apple Silicon) — full feature set
  - Ubuntu/Debian — core tools + shell

## License

Personal dotfiles — fork and adapt freely.
