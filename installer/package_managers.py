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
    """Package manager for Ubuntu using apt."""

    def get_package_manager_name(self) -> str:
        """Get the name of the package manager."""
        return "APT (Ubuntu/Debian)"

    def install_packages(self, system_manager: SystemManager) -> bool:
        """Install packages for Ubuntu using apt."""
        console.print(
            "\n[bold cyan]📦 Installing packages for Ubuntu/Debian...[/bold cyan]"
        )

        success = system_manager.run_interactive_command(
            "sudo apt update", "Updating package lists (may require password)..."
        )

        # Core development tools
        packages = [
            "git",
            "git-lfs",
            "curl",
            "wget",
            "python3",
            "python3-pip",
            "nodejs",
            "npm",
            "zsh",
            "bat",
            "ripgrep",
            "jq",
            "tree",
            "tmux",
            "rsync",
            "coreutils",
        ]
        success &= system_manager.run_interactive_command(
            f"sudo apt install -y {' '.join(packages)}",
            "Installing core packages (may require password)...",
        )

        # Try to install eza (exa alternative)
        system_manager.run_interactive_command(
            "sudo apt install -y exa || echo 'exa not available'", "Installing exa..."
        )

        console.print(
            "[cyan]Note: Some macOS-specific apps (AeroSpace, Übersicht) are not available on Linux[/cyan]"
        )

        return success


def create_package_manager(os_type: OSType, dotfiles_dir: Path) -> PackageManager:
    """Factory function to create the appropriate package manager."""
    if os_type == OSType.MACOS:
        return MacOSPackageManager(dotfiles_dir)
    elif os_type == OSType.UBUNTU:
        return UbuntuPackageManager()
    else:
        raise ValueError(f"Unsupported OS type: {os_type}")
