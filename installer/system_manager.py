#!/usr/bin/env python3

import platform
import subprocess
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from installer.enums import OSType
from installer.interfaces import SystemManager


class ConcreteSystemManager(SystemManager):
    """Concrete implementation of SystemManager for system detection and command execution."""

    def __init__(self):
        self.console = Console()
        try:
            self._os_type = self._detect_os()
        except ValueError:
            raise SystemExit(1)

    def _detect_os(self) -> OSType:
        """Detect the operating system (macOS or Ubuntu)."""
        system = platform.system()
        if system == "Darwin":
            return OSType.MACOS
        elif system == "Linux":
            # Check for Ubuntu/Debian
            try:
                with open("/etc/os-release") as f:
                    content = f.read().lower()
                    if "ubuntu" in content or "debian" in content:
                        return OSType.UBUNTU
            except FileNotFoundError:
                pass
            self.console.print(f"[red]Unsupported Linux distribution[/red]")
            self.console.print(
                "This installer only supports macOS and Ubuntu/Debian systems."
            )
            raise ValueError(f"Unsupported Linux distribution")
        else:
            self.console.print(f"[red]Unsupported OS: {system}[/red]")
            self.console.print(
                "This installer only supports macOS and Ubuntu/Debian systems."
            )
            raise ValueError(f"Unsupported operating system: {system}")

    def get_os_type(self) -> OSType:
        """Get the detected OS type."""
        return self._os_type

    def is_supported(self) -> bool:
        """Check if the current OS is supported."""
        return self._os_type in [OSType.MACOS, OSType.UBUNTU]

    def check_command_exists(self, command: str) -> bool:
        """Check if a command exists in the system."""
        return (
            subprocess.run(
                f"command -v {command}", shell=True, capture_output=True
            ).returncode
            == 0
        )

    def run_command(
        self,
        command: str,
        description: str = "",
        interactive: bool = False,
        cwd: Optional[Path] = None,
    ) -> bool:
        """Run a shell command with progress indicator."""
        try:
            if interactive:
                # For interactive commands, don't capture output and show description
                self.console.print(f"[cyan]{description or command}[/cyan]")
                result = subprocess.run(command, shell=True, cwd=cwd)
                return result.returncode == 0
            else:
                # For non-interactive commands, use progress indicator
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=self.console,
                ) as progress:
                    task = progress.add_task(description or command, total=None)
                    result = subprocess.run(
                        command, shell=True, capture_output=True, text=True, cwd=cwd
                    )
                    progress.remove_task(task)

                if result.returncode != 0:
                    self.console.print(f"[red]Error running: {command}[/red]")
                    self.console.print(f"[red]{result.stderr}[/red]")
                    return False
                return True
        except Exception as e:
            self.console.print(f"[red]Exception running {command}: {e}[/red]")
            return False

    def run_interactive_command(
        self, command: str, description: str = "", cwd: Optional[Path] = None
    ) -> bool:
        """Run an interactive command that may require user input."""
        return self.run_command(command, description, interactive=True, cwd=cwd)
