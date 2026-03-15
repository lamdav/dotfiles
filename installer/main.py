#!/usr/bin/env python3

import subprocess
from pathlib import Path

import typer
from rich.console import Console

from installer.dotfiles_installer import DotfilesInstaller

app = typer.Typer(
    name="dot",
    help="Dotfiles management CLI",
    rich_markup_mode="rich",
    no_args_is_help=True,
)
console = Console()

DOTFILES_DIR = Path(__file__).parent.parent.resolve()


@app.command(rich_help_panel="Setup")
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


@app.command(rich_help_panel="Setup")
def status() -> None:
    """Show the current status of dotfiles configuration."""
    installer = DotfilesInstaller(DOTFILES_DIR)
    installer.status()


@app.command(rich_help_panel="Release")
def release(
    patch: bool = typer.Option(False, "--patch", help="Force patch version bump"),
    minor: bool = typer.Option(False, "--minor", help="Force minor version bump"),
    major: bool = typer.Option(False, "--major", help="Force major version bump"),
) -> None:
    """Cut a release: bump version, update CHANGELOG.md, commit, and tag."""
    if sum([patch, minor, major]) > 1:
        console.print(
            "[red]Error: only one of --patch, --minor, --major may be specified[/red]"
        )
        raise typer.Exit(1)

    if patch:
        bump_flag = "--bump-patch"
    elif minor:
        bump_flag = "--bump-minor"
    elif major:
        bump_flag = "--bump-major"
    else:
        bump_flag = "--bump"

    has_tags = bool(
        subprocess.run(
            ["git", "tag", "--list"], capture_output=True, text=True, cwd=DOTFILES_DIR
        ).stdout.strip()
    )

    if has_tags:
        result = subprocess.run(
            ["git", "cliff", bump_flag, "--bumped-version"],
            capture_output=True,
            text=True,
            cwd=DOTFILES_DIR,
        )
        if "There is nothing to bump" in result.stderr:
            console.print(
                "[yellow]Nothing to release — no unreleased commits since last tag.[/yellow]"
            )
            raise typer.Exit(1)
        new_version = result.stdout.strip()
    else:
        new_version = "v1.0.0"

    console.print(f"Releasing [bold]{new_version}[/bold]...")

    subprocess.run(
        ["git", "cliff", bump_flag, "--tag", new_version, "-o", "CHANGELOG.md"],
        check=True,
        cwd=DOTFILES_DIR,
    )

    release_body = subprocess.run(
        ["git", "cliff", "--latest", "--strip", "all"],
        capture_output=True,
        text=True,
        check=True,
        cwd=DOTFILES_DIR,
    ).stdout.strip()

    subprocess.run(["git", "add", "CHANGELOG.md"], check=True, cwd=DOTFILES_DIR)
    subprocess.run(
        ["git", "commit", "-m", f"chore: release {new_version}\n\n{release_body}"],
        check=True,
        cwd=DOTFILES_DIR,
    )
    subprocess.run(
        ["git", "tag", "-a", new_version, "-m", release_body],
        check=True,
        cwd=DOTFILES_DIR,
    )

    console.print(f"[green]✓ Released {new_version}[/green]")


@app.command(name="next", rich_help_panel="Release")
def next_version() -> None:
    """Preview the next version based on unreleased commits. Exits 1 if nothing to release."""
    result = subprocess.run(
        ["git", "cliff", "--bumped-version"],
        capture_output=True,
        text=True,
        cwd=DOTFILES_DIR,
    )
    if "There is nothing to bump" in result.stderr:
        current = subprocess.run(
            ["git", "describe", "--tags", "--abbrev=0"],
            capture_output=True,
            text=True,
            cwd=DOTFILES_DIR,
        ).stdout.strip()
        console.print(
            f"[yellow]Nothing to release — no unreleased commits since {current}.[/yellow]"
        )
        raise typer.Exit(1)
    console.print(result.stdout.strip())


if __name__ == "__main__":
    app()
