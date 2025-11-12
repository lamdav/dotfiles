#!/usr/bin/env python3

from pathlib import Path
from typing import Tuple

from rich.console import Console
from rich.prompt import Confirm

from installer.interfaces import MacOSManager, SystemManager
from installer.symlink_manager import ConcreteSymlinkManager

console = Console()


class ConcreteMacOSManager(MacOSManager):
    """Concrete implementation of MacOSManager for macOS-specific operations."""

    def __init__(self):
        self.symlink_manager = ConcreteSymlinkManager()

    def setup_aerospace_config(self, dotfiles_dir: Path) -> bool:
        """Set up AeroSpace configuration symlink."""
        console.print(
            "\n[bold cyan]🪟 Setting up AeroSpace window manager...[/bold cyan]"
        )
        aerospace_source = dotfiles_dir / "aerospace" / ".aerospace.toml"
        if aerospace_source.exists():
            aerospace_target = Path.home() / ".aerospace.toml"
            return self.symlink_manager.create_symlink(
                aerospace_source, aerospace_target, "AeroSpace configuration"
            )
        return True  # Not an error if config doesn't exist

    def setup_iterm_config(self, dotfiles_dir: Path) -> bool:
        """Set up iTerm2 configuration symlink."""
        console.print("\n[bold cyan]💻 Setting up iTerm2 profiles...[/bold cyan]")
        iterm_source = dotfiles_dir / "iterm" / "iterm-profiles.json"
        if iterm_source.exists():
            iterm_target = (
                Path.home()
                / "Library"
                / "Application Support"
                / "iTerm2"
                / "DynamicProfiles"
                / "iterm-profiles.json"
            )
            return self.symlink_manager.create_symlink(
                iterm_source, iterm_target, "iTerm2 profiles"
            )
        return True  # Not an error if config doesn't exist

    def setup_kitty_quick_access(self, system_manager: SystemManager) -> bool:
        """Register Kitty quick-access-terminal (hotkey window) with macOS."""
        console.print("\n[bold cyan]⚡ Setting up Kitty quick-access-terminal...[/bold cyan]")

        if not system_manager.check_command_exists("kitten"):
            console.print("[yellow]Kitty not installed, skipping quick-access-terminal setup[/yellow]")
            return True

        # Run kitten quick-access-terminal once to register with macOS
        console.print("Registering quick-access-terminal service...")
        import subprocess
        import time

        try:
            # Start the quick-access-terminal in the background
            proc = subprocess.Popen(
                ["kitten", "quick-access-terminal"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            time.sleep(2)  # Give it time to register

            # Kill the process
            proc.terminate()
            try:
                proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                proc.kill()

            # Also kill any remaining quick-access-terminal processes
            subprocess.run(
                ["pkill", "-f", "quick-access-terminal"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            console.print("[green]✓ Kitty quick-access-terminal registered[/green]")
            console.print("\n[yellow]To complete setup:[/yellow]")
            console.print("  1. Open System Settings → Keyboard → Keyboard Shortcuts → Services")
            console.print("  2. Scroll to 'General' section and find 'Quick access to kitty'")
            console.print("  3. Check the box to enable it")
            console.print("  4. Click 'Add Shortcut' and press: [bold]Ctrl + `[/bold] (Control + backtick)")
            return True
        except Exception as e:
            console.print(f"[red]✗ Failed to register quick-access-terminal: {e}[/red]")
            return False

    def setup_ubersicht(
        self,
        dotfiles_dir: Path,
        system_manager: SystemManager,
        interactive: bool = True,
    ) -> Tuple[int, int]:
        """Set up Übersicht and simple-bar. Returns (success_count, total_steps)."""
        console.print(
            "\n[bold cyan]📊 Setting up Übersicht and simple-bar...[/bold cyan]"
        )

        success_count = 0
        total_steps = 0

        if not interactive or Confirm.ask(
            "[yellow]Set up Übersicht with simple-bar and AeroSpace mode indicator?[/yellow]",
            default=True,
        ):
            total_steps += 3

            # Check and install Übersicht
            if not (
                Path("/Applications/Übersicht.app").exists()
                or Path("/Applications/Uebersicht.app").exists()
            ):
                console.print("Installing Übersicht via Homebrew...")
                if system_manager.run_interactive_command(
                    "brew install --cask ubersicht",
                    "Installing Übersicht (may require password)...",
                ):
                    success_count += 1
            else:
                console.print("[green]✓ Übersicht already installed[/green]")
                success_count += 1

            # Install simple-bar
            simple_bar_dir = (
                Path.home() / "Library/Application Support/Übersicht/widgets/simple-bar"
            )
            if not simple_bar_dir.exists():
                console.print("Installing simple-bar...")
                simple_bar_parent = simple_bar_dir.parent
                simple_bar_parent.mkdir(parents=True, exist_ok=True)

                # Check if git is available before attempting clone
                if not system_manager.check_command_exists("git"):
                    console.print(
                        "[red]✗ Git is required to install simple-bar but is not available[/red]"
                    )
                    console.print(
                        "[yellow]Please install git first or run with --skip-packages=false[/yellow]"
                    )
                else:
                    if system_manager.run_command(
                        f"git clone https://github.com/Jean-Tinland/simple-bar '{simple_bar_dir}'",
                        "Installing simple-bar...",
                    ):
                        success_count += 1
            else:
                console.print("[green]✓ Simple-bar already installed[/green]")
                success_count += 1

            # Setup simple-bar configuration
            simplebarrc_source = (
                dotfiles_dir / "ubersicht" / "simple-bar" / "simplebarrc"
            )
            if simplebarrc_source.exists():
                simplebarrc_target = Path.home() / ".simplebarrc"
                self.symlink_manager.create_symlink(
                    simplebarrc_source, simplebarrc_target, "Simple-bar configuration"
                )

            # Setup aerospace-mode widget
            widgets_dir = Path.home() / "Library/Application Support/Übersicht/widgets"
            widgets_dir.mkdir(parents=True, exist_ok=True)

            # Remove any existing aerospace-mode.jsx file
            existing_widget = widgets_dir / "aerospace-mode.jsx"
            if existing_widget.exists():
                existing_widget.unlink()

            # Create symlink to dotfiles version
            aerospace_mode_source = dotfiles_dir / "ubersicht" / "aerospace-mode.jsx"
            if aerospace_mode_source.exists():
                if self.symlink_manager.create_symlink(
                    aerospace_mode_source, existing_widget, "AeroSpace mode indicator"
                ):
                    success_count += 1

            # Restart Übersicht to recognize new widgets
            console.print("Restarting Übersicht to recognize new widgets...")
            system_manager.run_command("pkill -f Übersicht", "Stopping Übersicht...")
            system_manager.run_command("open -a Übersicht", "Starting Übersicht...")
            console.print(
                "[green]✓ Übersicht restarted. New widgets should now be visible.[/green]"
            )

        return success_count, total_steps

    def configure_system_preferences(
        self, system_manager: SystemManager, interactive: bool = True
    ) -> bool:
        """Configure macOS system preferences."""
        console.print(
            "\n[bold cyan]⚙️  Configuring macOS system preferences...[/bold cyan]"
        )

        if interactive and not Confirm.ask(
            "[yellow]This will modify system preferences. Continue?[/yellow]",
            default=True,
        ):
            console.print("[yellow]Skipping system preferences configuration.[/yellow]")
            return True

        system_commands = [
            # UI/UX Settings
            'defaults write NSGlobalDomain AppleInterfaceStyle -string "Dark"',
            "defaults write com.apple.dock autohide -bool true",
            "defaults write com.apple.dock tilesize -int 48",
            'defaults write com.apple.dock orientation -string "left"',
            "defaults write NSGlobalDomain AppleShowAllExtensions -bool true",
            "defaults write com.apple.finder AppleShowAllFiles -bool true",
            "defaults write com.apple.finder ShowPathbar -bool true",
            "defaults write com.apple.finder ShowStatusBar -bool true",
            # Input Device Settings
            "defaults write NSGlobalDomain com.apple.swipescrolldirection -bool false",
            "defaults write com.apple.driver.AppleBluetoothMultitouch.trackpad Clicking -bool true",
            "defaults write NSGlobalDomain KeyRepeat -int 2",
            "defaults write NSGlobalDomain InitialKeyRepeat -int 15",
            "defaults write NSGlobalDomain NSAutomaticCapitalizationEnabled -bool false",
            # Developer Settings
            f'defaults write com.apple.screencapture location -string "{Path.home()}/Downloads"',
            'defaults write com.apple.screencapture type -string "png"',
            "defaults write com.apple.screencapture disable-shadow -bool true",
            "defaults write NSGlobalDomain AppleKeyboardUIMode -int 3",
            'defaults write com.apple.menuextra.battery ShowPercent -string "YES"',
            # Security Settings
            "defaults write com.apple.screensaver askForPassword -int 1",
            "defaults write com.apple.screensaver askForPasswordDelay -int 0",
            # Application Settings
            "defaults write com.apple.TextEdit RichText -int 0",
            "defaults write com.apple.TextEdit PlainTextEncoding -int 4",
            # Note: Safari preferences are skipped due to sandboxing restrictions
        ]

        all_success = True
        for cmd in system_commands:
            if not system_manager.run_command(cmd):
                all_success = False

        if all_success:
            # Restart affected applications
            console.print("Restarting applications to apply changes...")
            restart_commands = [
                "killall Dock 2>/dev/null || true",
                "killall Finder 2>/dev/null || true",
                "killall SystemUIServer 2>/dev/null || true",
            ]
            for cmd in restart_commands:
                system_manager.run_command(cmd)

        return all_success
