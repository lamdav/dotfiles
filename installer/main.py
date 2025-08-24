#!/usr/bin/env python3

import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm, Prompt
from rich.table import Table

app = typer.Typer(help="Interactive dotfiles configuration installer", rich_markup_mode=None)
console = Console()

DOTFILES_DIR = Path(__file__).parent.parent.resolve()


def run_command(command: str, description: str = "") -> bool:
    """Run a shell command with progress indicator."""
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task(description or command, total=None)
            result = subprocess.run(
                command, shell=True, capture_output=True, text=True, cwd=DOTFILES_DIR
            )
            progress.remove_task(task)
            
        if result.returncode != 0:
            console.print(f"[red]Error running: {command}[/red]")
            console.print(f"[red]{result.stderr}[/red]")
            return False
        return True
    except Exception as e:
        console.print(f"[red]Exception running {command}: {e}[/red]")
        return False


def check_command_exists(command: str) -> bool:
    """Check if a command exists in the system."""
    return subprocess.run(
        f"command -v {command}", shell=True, capture_output=True
    ).returncode == 0


def create_symlink(source: Path, target: Path, description: str = "") -> bool:
    """Create a symbolic link with user confirmation if target exists."""
    if target.exists() or target.is_symlink():
        if not Confirm.ask(
            f"[yellow]{target} already exists. Replace it?[/yellow]", default=True
        ):
            console.print(f"[yellow]Skipping {description}[/yellow]")
            return False
        
        if target.is_symlink():
            target.unlink()
        elif target.is_file():
            target.unlink()
        elif target.is_dir():
            import shutil
            shutil.rmtree(target)
    
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.symlink_to(source)
        console.print(f"[green]✓ Created symlink: {description}[/green]")
        return True
    except Exception as e:
        console.print(f"[red]✗ Failed to create symlink for {description}: {e}[/red]")
        return False


@app.command()
def install(
    skip_brew: bool = typer.Option(False, "--skip-brew", help="Skip Homebrew installation"),
    skip_shell: bool = typer.Option(False, "--skip-shell", help="Skip shell configuration"),
    skip_system: bool = typer.Option(False, "--skip-system", help="Skip macOS system preferences"),
    interactive: bool = typer.Option(True, "--interactive/--no-interactive", help="Interactive mode"),
) -> None:
    """Install dotfiles configuration with optional components."""
    
    console.print(Panel.fit(
        "[bold blue]Dotfiles Configuration Installer[/bold blue]\n"
        f"Installing from: {DOTFILES_DIR}",
        border_style="blue"
    ))
    
    # Show installation plan
    table = Table(title="Installation Plan")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Description")
    
    table.add_row("Homebrew", "Skip" if skip_brew else "Install", "Package manager and tools")
    table.add_row("Shell Config", "Skip" if skip_shell else "Install", "Zsh, Oh My Zsh, plugins")
    table.add_row("Git Config", "Install", "Git configuration and aliases")
    table.add_row("Vim Config", "Install", "Vim editor configuration")
    table.add_row("AeroSpace", "Install", "Window management")
    table.add_row("iTerm2", "Install", "Terminal profiles")
    table.add_row("Kitty", "Install", "Kitty terminal configuration")
    table.add_row("System Prefs", "Skip" if skip_system else "Install", "macOS system preferences")
    
    console.print(table)
    
    if interactive and not Confirm.ask("\n[bold]Proceed with installation?[/bold]", default=True):
        console.print("[yellow]Installation cancelled.[/yellow]")
        raise typer.Exit(1)
    
    success_count = 0
    total_steps = 0
    
    # Homebrew installation
    if not skip_brew:
        console.print("\n[bold cyan]📦 Setting up Homebrew and packages...[/bold cyan]")
        total_steps += 2
        
        if not check_command_exists("brew"):
            console.print("Installing Homebrew...")
            if run_command(
                '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
                "Installing Homebrew..."
            ):
                success_count += 1
        else:
            console.print("[green]✓ Homebrew already installed[/green]")
            success_count += 1
        
        console.print("Installing/updating packages from Brewfile...")
        if run_command("brew update && brew bundle --no-lock", "Installing packages..."):
            success_count += 1
    
    # Shell configuration
    if not skip_shell:
        console.print("\n[bold cyan]🐚 Setting up shell configuration...[/bold cyan]")
        total_steps += 3
        
        # Install Oh My Zsh if not present
        oh_my_zsh_dir = Path.home() / ".oh-my-zsh"
        if not oh_my_zsh_dir.exists():
            console.print("Installing Oh My Zsh...")
            if run_command(
                'sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended',
                "Installing Oh My Zsh..."
            ):
                success_count += 1
        else:
            console.print("[green]✓ Oh My Zsh already installed[/green]")
            success_count += 1
        
        # Create shell configuration symlinks
        shell_configs = [
            (".zshrc", "Zsh configuration"),
            (".zsh_plugins", "Zsh plugins"),
            (".p10k.zsh", "Powerlevel10k theme"),
        ]
        
        for config_file, description in shell_configs:
            source = DOTFILES_DIR / config_file
            target = Path.home() / config_file
            if source.exists():
                if create_symlink(source, target, description):
                    success_count += 1
            total_steps += 1
        
        # Custom theme
        theme_source = DOTFILES_DIR / "steeef-lambda.zsh-theme"
        theme_target = Path.home() / ".oh-my-zsh" / "custom" / "themes" / "steeef-lambda.zsh-theme"
        if theme_source.exists():
            if create_symlink(theme_source, theme_target, "Custom Zsh theme"):
                success_count += 1
        
        # Modular zsh configuration
        zsh_modules_dir = DOTFILES_DIR / "zsh"
        if zsh_modules_dir.exists():
            console.print("Setting up modular Zsh configuration...")
            zsh_config_dir = Path.home() / ".config" / "zsh"
            zsh_config_dir.mkdir(parents=True, exist_ok=True)
            
            module_count = 0
            for module_file in zsh_modules_dir.glob("*.zsh"):
                target_module = zsh_config_dir / module_file.name
                if create_symlink(module_file, target_module, f"Zsh module: {module_file.name}"):
                    module_count += 1
            
            console.print(f"[green]✓ {module_count} Zsh modules configured[/green]")
    
    # Git configuration
    console.print("\n[bold cyan]🔧 Setting up Git configuration...[/bold cyan]")
    total_steps += 1
    git_source = DOTFILES_DIR / ".gitconfig"
    git_target = Path.home() / ".gitconfig"
    if create_symlink(git_source, git_target, "Git configuration"):
        success_count += 1
    
    # Vim configuration
    console.print("\n[bold cyan]📝 Setting up Vim configuration...[/bold cyan]")
    vim_source = DOTFILES_DIR / ".vimrc"
    if vim_source.exists():
        total_steps += 1
        vim_target = Path.home() / ".vimrc"
        if create_symlink(vim_source, vim_target, "Vim configuration"):
            success_count += 1
    
    # AeroSpace configuration
    console.print("\n[bold cyan]🪟 Setting up AeroSpace window manager...[/bold cyan]")
    aerospace_source = DOTFILES_DIR / ".aerospace.toml"
    if aerospace_source.exists():
        total_steps += 1
        aerospace_target = Path.home() / ".aerospace.toml"
        if create_symlink(aerospace_source, aerospace_target, "AeroSpace configuration"):
            success_count += 1
    
    # iTerm2 profiles
    console.print("\n[bold cyan]💻 Setting up iTerm2 profiles...[/bold cyan]")
    iterm_source = DOTFILES_DIR / "iterm-profiles.json"
    if iterm_source.exists():
        total_steps += 1
        iterm_target = Path.home() / "Library" / "Application Support" / "iTerm2" / "DynamicProfiles" / "iterm-profiles.json"
        if create_symlink(iterm_source, iterm_target, "iTerm2 profiles"):
            success_count += 1
    
    # Kitty configuration
    console.print("\n[bold cyan]🐱 Setting up Kitty terminal...[/bold cyan]")
    kitty_source = DOTFILES_DIR / "kitty.conf"
    if kitty_source.exists():
        total_steps += 1
        kitty_target = Path.home() / ".config" / "kitty" / "kitty.conf"
        if create_symlink(kitty_source, kitty_target, "Kitty configuration"):
            success_count += 1
    
    # Kitty customizations directory
    kitty_custom_source = DOTFILES_DIR / "kitty-customizations"
    if kitty_custom_source.exists():
        total_steps += 1
        kitty_custom_target = Path.home() / ".config" / "kitty" / "kitty-customizations"
        if create_symlink(kitty_custom_source, kitty_custom_target, "Kitty customizations"):
            success_count += 1
    
    # Übersicht and simple-bar setup
    console.print("\n[bold cyan]📊 Setting up Übersicht and simple-bar...[/bold cyan]")
    
    if interactive and Confirm.ask(
        "[yellow]Set up Übersicht with simple-bar and AeroSpace mode indicator?[/yellow]", 
        default=True
    ):
        total_steps += 3
        
        # Check and install Übersicht
        if not (Path("/Applications/Übersicht.app").exists() or 
               Path("/Applications/Uebersicht.app").exists()):
            console.print("Installing Übersicht via Homebrew...")
            if run_command("brew install --cask ubersicht", "Installing Übersicht..."):
                success_count += 1
        else:
            console.print("[green]✓ Übersicht already installed[/green]")
            success_count += 1
        
        # Install simple-bar
        simple_bar_dir = Path.home() / "Library/Application Support/Übersicht/widgets/simple-bar"
        if not simple_bar_dir.exists():
            console.print("Installing simple-bar...")
            simple_bar_parent = simple_bar_dir.parent
            simple_bar_parent.mkdir(parents=True, exist_ok=True)
            if run_command(
                f"git clone https://github.com/Jean-Tinland/simple-bar '{simple_bar_dir}'",
                "Installing simple-bar..."
            ):
                success_count += 1
        else:
            console.print("[green]✓ Simple-bar already installed[/green]")
            success_count += 1
        
        # Setup simple-bar configuration
        simplebarrc_source = DOTFILES_DIR / "ubersicht" / "simple-bar" / "simplebarrc"
        if simplebarrc_source.exists():
            simplebarrc_target = Path.home() / ".simplebarrc"
            create_symlink(simplebarrc_source, simplebarrc_target, "Simple-bar configuration")
        
        # Setup aerospace-mode widget
        widgets_dir = Path.home() / "Library/Application Support/Übersicht/widgets"
        widgets_dir.mkdir(parents=True, exist_ok=True)
        
        # Remove any existing aerospace-mode.jsx file
        existing_widget = widgets_dir / "aerospace-mode.jsx"
        if existing_widget.exists():
            existing_widget.unlink()
        
        # Create symlink to dotfiles version
        aerospace_mode_source = DOTFILES_DIR / "ubersicht" / "aerospace-mode.jsx"
        if aerospace_mode_source.exists():
            if create_symlink(aerospace_mode_source, existing_widget, "AeroSpace mode indicator"):
                success_count += 1
        
        # Refresh Übersicht
        console.print("Refreshing Übersicht...")
        refresh_success = run_command(
            'osascript -e \'tell application id "tracesOf.Uebersicht" to refresh\'',
            "Refreshing Übersicht widgets..."
        )
        if not refresh_success:
            console.print("[yellow]⚠️  Could not refresh Übersicht automatically. Please refresh manually.[/yellow]")
    
    # macOS system preferences
    if not skip_system:
        console.print("\n[bold cyan]⚙️  Configuring macOS system preferences...[/bold cyan]")
        
        if interactive and not Confirm.ask(
            "[yellow]This will modify system preferences. Continue?[/yellow]", 
            default=True
        ):
            console.print("[yellow]Skipping system preferences configuration.[/yellow]")
        else:
            total_steps += 1
            system_commands = [
                # UI/UX Settings
                'defaults write NSGlobalDomain AppleInterfaceStyle -string "Dark"',
                'defaults write com.apple.dock autohide -bool true',
                'defaults write com.apple.dock tilesize -int 48',
                'defaults write com.apple.dock orientation -string "left"',
                'defaults write NSGlobalDomain AppleShowAllExtensions -bool true',
                'defaults write com.apple.finder AppleShowAllFiles -bool true',
                'defaults write com.apple.finder ShowPathbar -bool true',
                'defaults write com.apple.finder ShowStatusBar -bool true',
                
                # Input Device Settings
                'defaults write NSGlobalDomain com.apple.swipescrolldirection -bool false',
                'defaults write com.apple.driver.AppleBluetoothMultitouch.trackpad Clicking -bool true',
                'defaults write NSGlobalDomain KeyRepeat -int 2',
                'defaults write NSGlobalDomain InitialKeyRepeat -int 15',
                'defaults write NSGlobalDomain NSAutomaticCapitalizationEnabled -bool false',
                
                # Developer Settings
                f'defaults write com.apple.screencapture location -string "{Path.home()}/Downloads"',
                'defaults write com.apple.screencapture type -string "png"',
                'defaults write com.apple.screencapture disable-shadow -bool true',
                'defaults write NSGlobalDomain AppleKeyboardUIMode -int 3',
                'defaults write com.apple.menuextra.battery ShowPercent -string "YES"',
                
                # Security Settings
                'defaults write com.apple.screensaver askForPassword -int 1',
                'defaults write com.apple.screensaver askForPasswordDelay -int 0',
                
                # Application Settings
                'defaults write com.apple.TextEdit RichText -int 0',
                'defaults write com.apple.TextEdit PlainTextEncoding -int 4',
                'defaults write com.apple.Safari IncludeDevelopMenu -bool true',
            ]
            
            all_success = True
            for cmd in system_commands:
                if not run_command(cmd):
                    all_success = False
                    
            if all_success:
                success_count += 1
                
                # Restart affected applications
                console.print("Restarting applications to apply changes...")
                restart_commands = [
                    "killall Dock 2>/dev/null || true",
                    "killall Finder 2>/dev/null || true", 
                    "killall SystemUIServer 2>/dev/null || true",
                ]
                for cmd in restart_commands:
                    run_command(cmd)
    
    # Installation summary
    console.print(f"\n[bold green]🎉 Installation Complete![/bold green]")
    console.print(f"Successfully completed {success_count}/{total_steps} steps")
    
    if success_count < total_steps:
        console.print(f"[yellow]⚠️  {total_steps - success_count} steps had issues[/yellow]")
    
    # Next steps
    console.print(Panel.fit(
        "[bold]Next Steps:[/bold]\n"
        "• Run 'exec zsh' to reload your shell\n"
        "• Restart iTerm2 to see the new profile\n"
        "• Launch Kitty to use the new terminal configuration\n"
        "• Some macOS changes may require a system restart\n"
        "• Run 'updateplugins' to refresh Zsh plugins\n"
        "• For Kitty hotkey window (ctrl+`), set up a macOS shortcut in System Preferences",
        title="What's Next?",
        border_style="green"
    ))


@app.command()
def status() -> None:
    """Show the current status of dotfiles configuration."""
    console.print(Panel.fit("[bold blue]Dotfiles Status Check[/bold blue]", border_style="blue"))
    
    table = Table(title="Configuration Status")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Path")
    
    configs = [
        (".zshrc", "Zsh configuration"),
        (".gitconfig", "Git configuration"),
        (".vimrc", "Vim configuration"),
        (".aerospace.toml", "AeroSpace configuration"),
        ("Library/Application Support/iTerm2/DynamicProfiles/iterm-profiles.json", "iTerm2 profiles"),
        (".config/kitty/kitty.conf", "Kitty configuration"),
    ]
    
    for config_file, description in configs:
        target = Path.home() / config_file
        source = DOTFILES_DIR / Path(config_file).name
        
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
    tools = ["brew", "git", "zsh", "vim", "rvm", "nvm"]
    for tool in tools:
        status = "[green]✓[/green]" if check_command_exists(tool) else "[red]✗[/red]"
        console.print(f"{status} {tool}")


if __name__ == "__main__":
    app()