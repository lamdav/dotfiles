#!/usr/bin/env python3

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Tuple

from installer.enums import OSType


class SystemManager(ABC):
    """Interface for system detection and command execution."""

    @abstractmethod
    def get_os_type(self) -> OSType:
        """Get the detected OS type."""
        pass

    @abstractmethod
    def is_supported(self) -> bool:
        """Check if the current OS is supported."""
        pass

    @abstractmethod
    def check_command_exists(self, command: str) -> bool:
        """Check if a command exists in the system."""
        pass

    @abstractmethod
    def run_command(
        self,
        command: str,
        description: str = "",
        interactive: bool = False,
        cwd: Optional[Path] = None,
    ) -> bool:
        """Run a shell command with progress indicator."""
        pass

    @abstractmethod
    def run_interactive_command(
        self, command: str, description: str = "", cwd: Optional[Path] = None
    ) -> bool:
        """Run an interactive command that may require user input."""
        pass


class PackageManager(ABC):
    """Interface for package management across different operating systems."""

    @abstractmethod
    def install_packages(self, system_manager: SystemManager) -> bool:
        """Install packages for the specific OS."""
        pass

    @abstractmethod
    def get_package_manager_name(self) -> str:
        """Get the name of the package manager."""
        pass


class SymlinkManager(ABC):
    """Interface for creating and managing symbolic links."""

    @abstractmethod
    def create_symlink(self, source: Path, target: Path, description: str = "") -> bool:
        """Create a symbolic link with user confirmation if target exists."""
        pass

    @abstractmethod
    def setup_shell_config(self, dotfiles_dir: Path) -> Tuple[int, int]:
        """Set up shell configuration symlinks. Returns (success_count, total_steps)."""
        pass

    @abstractmethod
    def setup_git_config(self, dotfiles_dir: Path) -> bool:
        """Set up git configuration symlink."""
        pass

    @abstractmethod
    def setup_vim_config(self, dotfiles_dir: Path) -> bool:
        """Set up vim configuration symlink."""
        pass

    @abstractmethod
    def setup_kitty_config(self, dotfiles_dir: Path) -> Tuple[int, int]:
        """Set up kitty configuration symlinks. Returns (success_count, total_steps)."""
        pass


class MacOSManager(ABC):
    """Interface for macOS-specific operations."""

    @abstractmethod
    def setup_aerospace_config(self, dotfiles_dir: Path) -> bool:
        """Set up AeroSpace configuration symlink."""
        pass

    @abstractmethod
    def setup_iterm_config(self, dotfiles_dir: Path) -> bool:
        """Set up iTerm2 configuration symlink."""
        pass

    @abstractmethod
    def setup_kitty_quick_access(self, system_manager: SystemManager) -> bool:
        """Register Kitty quick-access-terminal (hotkey window) with macOS."""
        pass

    @abstractmethod
    def setup_ubersicht(
        self,
        dotfiles_dir: Path,
        system_manager: SystemManager,
        interactive: bool = True,
    ) -> Tuple[int, int]:
        """Set up Übersicht and simple-bar. Returns (success_count, total_steps)."""
        pass

    @abstractmethod
    def configure_system_preferences(
        self, system_manager: SystemManager, interactive: bool = True
    ) -> bool:
        """Configure macOS system preferences."""
        pass


class Installer(ABC):
    """Interface for the main installer."""

    @abstractmethod
    def install(
        self,
        skip_packages: bool = False,
        skip_shell: bool = False,
        skip_system: bool = False,
        interactive: bool = True,
    ) -> None:
        """Run the installation process."""
        pass

    @abstractmethod
    def status(self) -> None:
        """Show the current status of dotfiles configuration."""
        pass
