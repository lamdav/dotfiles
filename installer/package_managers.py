#!/usr/bin/env python3

from pathlib import Path

from rich.console import Console

from installer.enums import OSType
from installer.interfaces import PackageManager, SystemManager

console = Console()


class MacOSPackageManager(PackageManager):
    """Package manager for macOS using Homebrew."""

    def __init__(self, dotfiles_dir: Path):
        self.dotfiles_dir = dotfiles_dir

    def get_package_manager_name(self) -> str:
        """Get the name of the package manager."""
        return "Homebrew"

    def install_packages(self, system_manager: SystemManager) -> bool:
        """Install packages for macOS using Homebrew."""
        console.print("\n[bold cyan]📦 Setting up Homebrew and packages...[/bold cyan]")

        success = True

        # Install Homebrew if needed
        if not system_manager.check_command_exists("brew"):
            console.print("Installing Homebrew...")
            success &= system_manager.run_interactive_command(
                '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
                "Installing Homebrew (may require password)...",
            )
        else:
            console.print("[green]✓ Homebrew already installed[/green]")

        # Update and install from Brewfiles
        success &= system_manager.run_command("brew update", "Updating Homebrew...")

        brewfiles = [
            ("brew/Brewfile.devtools", "development tools"),
            ("brew/Brewfile.k8s", "Kubernetes tools"),
            ("brew/Brewfile.media", "media tools"),
            ("brew/Brewfile.gui", "GUI applications"),
            ("brew/Brewfile.apps", "applications"),
        ]

        for brewfile, description in brewfiles:
            brewfile_path = self.dotfiles_dir / brewfile
            if brewfile_path.exists():
                console.print(f"Installing {description}...")
                # brew bundle may require password for cask installations
                success &= system_manager.run_interactive_command(
                    f"brew bundle --file={brewfile}",
                    f"Installing {description} (may require password)...",
                )
            else:
                console.print(
                    f"[yellow]⚠️  {brewfile} not found, skipping {description}[/yellow]"
                )

        # Show optional packages
        optional_brewfile = self.dotfiles_dir / "brew" / "Brewfile.optional"
        if optional_brewfile.exists():
            console.print(
                f"[cyan]📦 Optional packages available in brew/Brewfile.optional[/cyan]"
            )
            console.print(
                f"[cyan]Run: brew bundle --file=brew/Brewfile.optional[/cyan]"
            )

        return success


class UbuntuPackageManager(PackageManager):
    """Package manager for Ubuntu using apt and direct installs."""

    def __init__(self):
        self._phase = 0

    def _phase_header(self, name: str) -> None:
        self._phase += 1
        console.print(f"\n[bold cyan]📦 Phase {self._phase} — {name}...[/bold cyan]")

    def get_package_manager_name(self) -> str:
        return "APT (Ubuntu/Debian)"

    def install_packages(self, system_manager: SystemManager) -> bool:
        self._phase = 0
        success = True
        success &= self._install_apt_packages(system_manager)
        success &= self._install_neovim(system_manager)
        success &= self._install_eza(system_manager)
        success &= self._install_gh(system_manager)
        success &= self._install_fzf(system_manager)
        success &= self._install_delta(system_manager)
        success &= self._install_antidote(system_manager)
        success &= self._install_mise(system_manager)
        success &= self._install_uv(system_manager)
        success &= self._install_zoxide(system_manager)
        success &= self._install_git_cliff(system_manager)
        self._install_kitty_terminfo(system_manager)  # non-critical
        return success

    def _install_apt_packages(self, system_manager: SystemManager) -> bool:
        self._phase_header("apt base packages")
        packages = [
            "zsh",
            "git",
            "git-lfs",
            "curl",
            "wget",
            "jq",
            "ripgrep",
            "fd-find",
            "bat",
            "tmux",
            "direnv",
            "btop",
            "httpie",
            "ncdu",
            "unzip",
            "build-essential",
            "software-properties-common",
        ]
        ok = system_manager.run_interactive_command(
            "sudo apt-get update -qq", "Updating apt..."
        )
        ok &= system_manager.run_interactive_command(
            f"sudo apt-get install -y {' '.join(packages)}",
            "Installing apt packages...",
        )
        return ok

    def _install_neovim(self, system_manager: SystemManager) -> bool:
        self._phase_header("Neovim (unstable PPA)")
        if system_manager.check_command_exists("nvim"):
            console.print("[green]✓ Neovim already installed[/green]")
            return True
        ok = system_manager.run_interactive_command(
            "sudo add-apt-repository -y ppa:neovim-ppa/unstable",
            "Adding neovim PPA...",
        )
        ok &= system_manager.run_interactive_command(
            "sudo apt-get update -qq && sudo apt-get install -y neovim",
            "Installing Neovim...",
        )
        return ok

    def _install_eza(self, system_manager: SystemManager) -> bool:
        self._phase_header("eza")
        if system_manager.check_command_exists("eza"):
            console.print("[green]✓ eza already installed[/green]")
            return True
        script = (
            "sudo mkdir -p /etc/apt/keyrings && "
            "wget -qO- https://raw.githubusercontent.com/eza-community/eza/main/deb.asc "
            "| sudo gpg --dearmor -o /etc/apt/keyrings/gierens.gpg && "
            'echo "deb [signed-by=/etc/apt/keyrings/gierens.gpg] http://deb.gierens.de stable main" '
            "| sudo tee /etc/apt/sources.list.d/gierens.list && "
            "sudo chmod 644 /etc/apt/keyrings/gierens.gpg /etc/apt/sources.list.d/gierens.list && "
            "sudo apt-get update -qq && sudo apt-get install -y eza"
        )
        ok = system_manager.run_interactive_command(script, "Installing eza...")
        if not ok:
            console.print("[yellow]⚠ eza install failed — skipping[/yellow]")
        return True  # non-fatal

    def _install_gh(self, system_manager: SystemManager) -> bool:
        self._phase_header("GitHub CLI (gh)")
        if system_manager.check_command_exists("gh"):
            console.print("[green]✓ gh already installed[/green]")
            return True
        script = (
            "curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg"
            " | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && "
            "sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg && "
            'echo "deb [arch=$(dpkg --print-architecture)'
            " signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg]"
            ' https://cli.github.com/packages stable main"'
            " | sudo tee /etc/apt/sources.list.d/github-cli.list && "
            "sudo apt-get update -qq && sudo apt-get install -y gh"
        )
        ok = system_manager.run_interactive_command(script, "Installing gh...")
        if not ok:
            console.print("[yellow]⚠ gh install failed — skipping[/yellow]")
        return True  # non-fatal

    def _install_delta(self, system_manager: SystemManager) -> bool:
        self._phase_header("git-delta (git pager)")
        if system_manager.check_command_exists("delta"):
            console.print("[green]✓ delta already installed[/green]")
            return True
        script = (
            "set -e && "
            "DELTA_VERSION=$(curl -fsSL https://api.github.com/repos/dandavison/delta/releases/latest"
            " | jq -r '.tag_name') && "
            'curl -fsSL "https://github.com/dandavison/delta/releases/download/${DELTA_VERSION}/'
            'git-delta_${DELTA_VERSION}_amd64.deb" -o /tmp/delta.deb && '
            "sudo dpkg -i /tmp/delta.deb && rm /tmp/delta.deb"
        )
        ok = system_manager.run_interactive_command(script, "Installing delta...")
        if not ok:
            console.print("[yellow]⚠ delta install failed — skipping[/yellow]")
        return True  # non-fatal

    def _install_fzf(self, system_manager: SystemManager) -> bool:
        self._phase_header("fzf (GitHub release)")
        if system_manager.check_command_exists("fzf"):
            console.print("[green]✓ fzf already installed[/green]")
            return True
        script = (
            "set -e && "
            "FZF_VERSION=$(curl -fsSL https://api.github.com/repos/junegunn/fzf/releases/latest"
            " | jq -r '.tag_name | ltrimstr(\"v\")') && "
            "mkdir -p ~/.local/bin && "
            'curl -fsSL "https://github.com/junegunn/fzf/releases/download/v${FZF_VERSION}/fzf-${FZF_VERSION}-linux_amd64.tar.gz" '
            "| tar -xz -C ~/.local/bin fzf && "
            "chmod +x ~/.local/bin/fzf"
        )
        ok = system_manager.run_interactive_command(script, "Installing fzf...")
        if not ok:
            console.print("[yellow]⚠ fzf install failed — skipping[/yellow]")
        return True  # non-fatal

    def _install_antidote(self, system_manager: SystemManager) -> bool:
        self._phase_header("antidote (zsh plugin manager)")
        antidote_dir = Path.home() / ".antidote"
        if antidote_dir.exists():
            console.print("[green]✓ antidote already installed[/green]")
            return True
        ok = system_manager.run_interactive_command(
            "git clone --depth=1 https://github.com/getantidote/antidote.git ~/.antidote",
            "Installing antidote...",
        )
        if not ok:
            console.print(
                "[yellow]⚠ antidote install failed — zsh plugins won't load[/yellow]"
            )
        return ok  # fatal: plugins won't work without it

    def _install_mise(self, system_manager: SystemManager) -> bool:
        self._phase_header("mise (version manager)")
        if system_manager.check_command_exists("mise"):
            console.print("[green]✓ mise already installed[/green]")
            return True
        ok = system_manager.run_interactive_command(
            "curl https://mise.run | sh", "Installing mise..."
        )
        if not ok:
            console.print("[yellow]⚠ mise install failed — skipping[/yellow]")
        return True  # non-fatal

    def _install_uv(self, system_manager: SystemManager) -> bool:
        self._phase_header("uv (Python package manager)")
        if system_manager.check_command_exists("uv"):
            console.print("[green]✓ uv already installed[/green]")
            return True
        # Prefer apt (available on Ubuntu 24.10+); fall back to official installer.
        script = (
            "if apt-cache show uv >/dev/null 2>&1; then "
            "sudo apt-get install -y uv; "
            "else "
            "curl -LsSf https://astral.sh/uv/install.sh | sh; "
            "fi"
        )
        ok = system_manager.run_interactive_command(script, "Installing uv...")
        if not ok:
            console.print("[yellow]⚠ uv install failed — skipping[/yellow]")
        return True  # non-fatal

    def _install_zoxide(self, system_manager: SystemManager) -> bool:
        self._phase_header("zoxide")
        if system_manager.check_command_exists("zoxide"):
            console.print("[green]✓ zoxide already installed[/green]")
            return True
        ok = system_manager.run_interactive_command(
            "curl -sSfL https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh | sh",
            "Installing zoxide...",
        )
        if not ok:
            console.print("[yellow]⚠ zoxide install failed — skipping[/yellow]")
        return True  # non-fatal

    def _install_git_cliff(self, system_manager: SystemManager) -> bool:
        self._phase_header("git-cliff (changelog generator)")
        if system_manager.check_command_exists("git-cliff"):
            console.print("[green]✓ git-cliff already installed[/green]")
            return True
        script = (
            "GIT_CLIFF_VERSION=$(curl -fsSL https://api.github.com/repos/orhun/git-cliff/releases/latest"
            " | jq -r '.tag_name' | sed 's/v//') && "
            'curl -fsSL "https://github.com/orhun/git-cliff/releases/download/v${GIT_CLIFF_VERSION}/'
            'git-cliff_${GIT_CLIFF_VERSION}_amd64.deb" -o /tmp/git-cliff.deb && '
            "sudo dpkg -i /tmp/git-cliff.deb && rm /tmp/git-cliff.deb"
        )
        ok = system_manager.run_interactive_command(script, "Installing git-cliff...")
        if not ok:
            console.print("[yellow]⚠ git-cliff install failed — skipping[/yellow]")
        return True  # non-fatal

    def _install_kitty_terminfo(self, system_manager: SystemManager) -> bool:
        self._phase_header("kitty terminfo (SSH from Kitty)")
        check = system_manager.run_command(
            "infocmp xterm-kitty >/dev/null 2>&1", "Checking kitty terminfo..."
        )
        if check:
            console.print("[green]✓ kitty terminfo already installed[/green]")
            return True
        ok = system_manager.run_interactive_command(
            "curl -fsSL https://raw.githubusercontent.com/kovidgoyal/kitty/master/terminfo/x/xterm-kitty"
            " | tic -x -",
            "Installing kitty terminfo...",
        )
        if not ok:
            console.print(
                "[yellow]⚠ kitty terminfo install failed — "
                "use 'kitten ssh' from your Kitty client as fallback[/yellow]"
            )
        return True  # non-fatal


def create_package_manager(os_type: OSType, dotfiles_dir: Path) -> PackageManager:
    """Factory function to create the appropriate package manager."""
    if os_type == OSType.MACOS:
        return MacOSPackageManager(dotfiles_dir)
    elif os_type == OSType.UBUNTU:
        return UbuntuPackageManager()
    else:
        raise ValueError(f"Unsupported OS type: {os_type}")
