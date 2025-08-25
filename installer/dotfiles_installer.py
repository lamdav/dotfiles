#!/usr/bin/env python3

from pathlib import Path
from typing import List, Tuple

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table

from installer.enums import OSType
from installer.interfaces import Installer
from installer.macos_manager import ConcreteMacOSManager
from installer.package_managers import create_package_manager
from installer.symlink_manager import ConcreteSymlinkManager
from installer.system_manager import ConcreteSystemManager

console = Console()


class DotfilesInstaller(Installer):
    """Main installer implementation for dotfiles configuration."""

    def __init__(self, dotfiles_dir: Path):
        self.dotfiles_dir = dotfiles_dir
        self.system_manager = ConcreteSystemManager()
        self.symlink_manager = ConcreteSymlinkManager()
        self.macos_manager = (
            ConcreteMacOSManager()
            if self.system_manager.get_os_type() == OSType.MACOS
            else None
        )

        # Check if OS is supported
        if not self.system_manager.is_supported():
            console.print("[red]Unsupported operating system. Exiting.[/red]")
            raise SystemExit(1)

    def install(
        self,
        skip_packages: bool = False,
        skip_shell: bool = False,
        skip_system: bool = False,
        interactive: bool = True,
    ) -> None:
        """Run the installation process."""

        os_type = self.system_manager.get_os_type()
        console.print(f"[cyan]Detected OS: {os_type}[/cyan]")

        console.print(
            Panel.fit(
                "[bold blue]Dotfiles Configuration Installer[/bold blue]\n"
                f"Installing from: {self.dotfiles_dir}\n"
                f"Target OS: {os_type}",
                border_style="blue",
            )
        )

        # Show installation plan
        self._show_installation_plan(os_type, skip_packages, skip_shell, skip_system)

        if interactive and not Confirm.ask(
            "\n[bold]Proceed with installation?[/bold]", default=True
        ):
            console.print("[yellow]Installation cancelled.[/yellow]")
            return

        success_count = 0
        total_steps = 0

        # Package installation
        if not skip_packages:
            total_steps += 1
            package_manager = create_package_manager(os_type, self.dotfiles_dir)
            if package_manager.install_packages(self.system_manager):
                success_count += 1

        # Shell configuration
        if not skip_shell:
            shell_success, shell_steps = self.symlink_manager.setup_shell_config(
                self.dotfiles_dir
            )
            success_count += shell_success
            total_steps += shell_steps

        # Git configuration
        if self.symlink_manager.setup_git_config(self.dotfiles_dir):
            success_count += 1
        total_steps += 1

        # Vim configuration
        if self.symlink_manager.setup_vim_config(self.dotfiles_dir):
            success_count += 1
        total_steps += 1

        # macOS-specific configurations
        if os_type == OSType.MACOS and self.macos_manager:
            # AeroSpace configuration
            if self.macos_manager.setup_aerospace_config(self.dotfiles_dir):
                success_count += 1
            total_steps += 1

            # iTerm2 configuration
            if self.macos_manager.setup_iterm_config(self.dotfiles_dir):
                success_count += 1
            total_steps += 1

            # Übersicht setup
            ubersicht_success, ubersicht_steps = self.macos_manager.setup_ubersicht(
                self.dotfiles_dir, self.system_manager, interactive
            )
            success_count += ubersicht_success
            total_steps += ubersicht_steps

            # System preferences
            if not skip_system:
                if self.macos_manager.configure_system_preferences(
                    self.system_manager, interactive
                ):
                    success_count += 1
                total_steps += 1

        # Kitty configuration (cross-platform)
        kitty_success, kitty_steps = self.symlink_manager.setup_kitty_config(
            self.dotfiles_dir
        )
        success_count += kitty_success
        total_steps += kitty_steps

        # Installation summary
        self._show_installation_summary(success_count, total_steps, os_type)

    def status(self) -> None:
        """Show the current status of dotfiles configuration."""
        console.print(
            Panel.fit(
                "[bold blue]Dotfiles Status Check[/bold blue]", border_style="blue"
            )
        )

        table = Table(title="Configuration Status")
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="bold")
        table.add_column("Path")

        configs = [
            ("zsh/.zshrc", ".zshrc", "Zsh configuration"),
            ("git/.gitconfig", ".gitconfig", "Git configuration"),
            ("vim/.vimrc", ".vimrc", "Vim configuration"),
            ("kitty/kitty.conf", ".config/kitty/kitty.conf", "Kitty configuration"),
        ]

        # Add macOS-specific configs
        if self.system_manager.get_os_type() == OSType.MACOS:
            configs.extend(
                [
                    (
                        "aerospace/.aerospace.toml",
                        ".aerospace.toml",
                        "AeroSpace configuration",
                    ),
                    (
                        "iterm/iterm-profiles.json",
                        "Library/Application Support/iTerm2/DynamicProfiles/iterm-profiles.json",
                        "iTerm2 profiles",
                    ),
                ]
            )

        for source_path, target_path, description in configs:
            target = Path.home() / target_path
            source = self.dotfiles_dir / source_path

            if target.is_symlink() and target.resolve() == source:
                status = "[green]✓ Linked[/green]"
            elif target.exists():
                status = "[yellow]⚠ File exists (not linked)[/yellow]"
            else:
                status = "[red]✗ Not configured[/red]"

            table.add_row(description, status, str(target))

        console.print(table)

        # Check tools
        console.print("\n[bold cyan]Installed Tools:[/bold cyan]")
        tools = (
            ["brew", "git", "zsh", "vim"]
            if self.system_manager.get_os_type() == OSType.MACOS
            else ["git", "zsh", "vim", "apt"]
        )
        for tool in tools:
            status = (
                "[green]✓[/green]"
                if self.system_manager.check_command_exists(tool)
                else "[red]✗[/red]"
            )
            console.print(f"{status} {tool}")

    def _show_installation_plan(
        self, os_type: OSType, skip_packages: bool, skip_shell: bool, skip_system: bool
    ) -> None:
        """Show the installation plan based on OS and options."""
        table = Table(title="Installation Plan")
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Description")

        package_manager = (
            "Homebrew" if os_type == OSType.MACOS else "APT (Ubuntu/Debian)"
        )
        table.add_row(
            "Packages",
            "Skip" if skip_packages else "Install",
            f"{package_manager} and development tools",
        )
        table.add_row(
            "Shell Config",
            "Skip" if skip_shell else "Install",
            "Zsh, Oh My Zsh, plugins",
        )
        table.add_row("Git Config", "Install", "Git configuration and aliases")
        table.add_row("Vim Config", "Install", "Vim editor configuration")

        if os_type == OSType.MACOS:
            table.add_row("AeroSpace", "Install", "Window management (macOS only)")
            table.add_row("iTerm2", "Install", "Terminal profiles (macOS only)")
            table.add_row("Übersicht", "Install", "Status bar and widgets (macOS only)")
            table.add_row(
                "System Prefs",
                "Skip" if skip_system else "Install",
                "macOS system preferences",
            )

        table.add_row("Kitty", "Install", "Kitty terminal configuration")

        console.print(table)

    def _show_installation_summary(
        self, success_count: int, total_steps: int, os_type: OSType
    ) -> None:
        """Show the installation summary and next steps."""
        console.print(f"\n[bold green]🎉 Installation Complete![/bold green]")
        console.print(f"Successfully completed {success_count}/{total_steps} steps")

        if success_count < total_steps:
            console.print(
                f"[yellow]⚠️  {total_steps - success_count} steps had issues[/yellow]"
            )

        # Next steps
        next_steps = [
            "• Run 'exec zsh' to reload your shell",
            "• Run 'updateplugins' to refresh Zsh plugins",
        ]

        if os_type == OSType.MACOS:
            next_steps.extend(
                [
                    "• Restart iTerm2 to see the new profile",
                    "• Some macOS changes may require a system restart",
                    "• For Kitty hotkey window (ctrl+`), set up a macOS shortcut in System Preferences",
                ]
            )

        if Path.home().joinpath(".config/kitty/kitty.conf").exists():
            next_steps.append("• Launch Kitty to use the new terminal configuration")

        console.print(
            Panel.fit(
                f"[bold]Next Steps:[/bold]\n" + "\n".join(next_steps),
                title="What's Next?",
                border_style="green",
            )
        )
