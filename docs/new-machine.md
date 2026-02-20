# New Machine Setup

Complete runbook for setting up a fresh macOS machine from scratch.

---

## 1. Prerequisites

```bash
# Install Xcode command line tools (required for git, compilers)
xcode-select --install

# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Add Homebrew to PATH for this session (Apple Silicon)
eval "$(/opt/homebrew/bin/brew shellenv)"
```

---

## 2. Clone Dotfiles

```bash
mkdir -p ~/configs
git clone https://github.com/lamdav/dotfiles.git ~/configs/dotfiles
cd ~/configs/dotfiles
```

---

## 3. Install Packages

```bash
brew bundle --file brew/Brewfile.devtools
brew bundle --file brew/Brewfile.k8s
brew bundle --file brew/Brewfile.gui
brew bundle --file brew/Brewfile.apps
# Optional:
brew bundle --file brew/Brewfile.optional
```

---

## 4. Run Installer

```bash
cd ~/configs/dotfiles
python installer/main.py install
```

This sets up all symlinks for: zsh, git, neovim, vim, kitty, mise, direnv, aerospace, iterm2, übersicht, and macOS system preferences.

---

## 5. Shell Setup

```bash
# Set zsh as default shell (if not already)
chsh -s $(which zsh)

# Reload shell with new config
exec zsh

# Generate plugin cache
updateplugins && exec zsh
```

---

## 6. Tool Runtimes (mise)

```bash
# Install all global runtimes (node lts, python latest, go latest, java temurin-21)
mise install

# Optional: register Java with macOS JVM picker
sudo mkdir /Library/Java/JavaVirtualMachines/temurin-21.0.10+7.0.LTS.jdk
sudo ln -s ~/.local/share/mise/installs/java/temurin-21.0.10+7.0.LTS/Contents \
  /Library/Java/JavaVirtualMachines/temurin-21.0.10+7.0.LTS.jdk/Contents
```

---

## 7. Authenticate Services

```bash
# GitHub CLI
gh auth login

# Tailscale (if installed)
# Open Tailscale.app and sign in via menu bar
```

---

## 8. Neovim Plugins

```bash
# First launch installs lazy.nvim and all plugins automatically
nvim

# Inside nvim, if plugins didn't auto-install:
# :Lazy sync
# :MasonToolsInstall
```

---

## 9. Kitty Hotkey Window

1. Run `kitten quick-access-terminal` once to register the service
2. Open **System Settings → Keyboard → Keyboard Shortcuts → Services → General**
3. Find "Quick access to kitty" → enable it → set shortcut: **Ctrl + `**

---

## 10. AeroSpace

AeroSpace starts at login automatically (`start-at-login = true`).

If not running: open AeroSpace.app from Applications or run `open -a AeroSpace`.

---

## Verification Checklist

```bash
python installer/main.py status   # all symlinks green
mise ls                           # node, python, go, java listed
gh auth status                    # authenticated
nvim --version                    # 0.11+
fzf --version                     # installed
direnv --version                  # installed
```
