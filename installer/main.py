#!/usr/bin/env python3

from pathlib import Path

import typer
from rich.console import Console

from installer.dotfiles_installer import DotfilesInstaller

app = typer.Typer(
    help="Interactive dotfiles configuration installer", rich_markup_mode=None
)
console = Console()

DOTFILES_DIR = Path(__file__).parent.parent.resolve()


@app.command()
def install(
    skip_packages: bool = typer.Option(
        False, "--skip-packages", help="Skip package installation"
    ),
    skip_shell: bool = typer.Option(
        False, "--skip-shell", help="Skip shell configuration"
    ),
    skip_system: bool = typer.Option(
        False, "--skip-system", help="Skip macOS system preferences"
    ),
    interactive: bool = typer.Option(
        True, "--interactive/--no-interactive", help="Interactive mode"
    ),
) -> None:
    """Install dotfiles configuration with optional components."""
    installer = DotfilesInstaller(DOTFILES_DIR)
    installer.install(skip_packages, skip_shell, skip_system, interactive)


@app.command()
def status() -> None:
    """Show the current status of dotfiles configuration."""
    installer = DotfilesInstaller(DOTFILES_DIR)
    installer.status()


if __name__ == "__main__":
    app()
