#!/usr/bin/env python3

import shutil
from pathlib import Path
from typing import Tuple

from rich.console import Console
from rich.prompt import Confirm

from installer.interfaces import SymlinkManager

console = Console()


class ConcreteSymlinkManager(SymlinkManager):
    """Concrete implementation of SymlinkManager for creating and managing symbolic links."""

    def create_symlink(self, source: Path, target: Path, description: str = "") -> bool:
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
                shutil.rmtree(target)

        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to(source)
            console.print(f"[green]✓ Created symlink: {description}[/green]")
            return True
        except Exception as e:
            console.print(
                f"[red]✗ Failed to create symlink for {description}: {e}[/red]"
            )
            return False

    def setup_shell_config(self, dotfiles_dir: Path) -> Tuple[int, int]:
        """Set up shell configuration symlinks. Returns (success_count, total_steps)."""
        console.print("\n[bold cyan]🐚 Setting up shell configuration...[/bold cyan]")

        success_count = 0
        total_steps = 0

        # Install Oh My Zsh if not present
        oh_my_zsh_dir = Path.home() / ".oh-my-zsh"
        if not oh_my_zsh_dir.exists():
            console.print("Installing Oh My Zsh...")
            # Note: This would need system_manager, but keeping it simple for now
            import subprocess

            result = subprocess.run(
                'sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended',
                shell=True,
            )
            if result.returncode == 0:
                success_count += 1
        else:
            console.print("[green]✓ Oh My Zsh already installed[/green]")
            success_count += 1
        total_steps += 1

        # Create shell configuration symlinks
        shell_configs = [
            ("zsh/.zshrc", ".zshrc", "Zsh configuration"),
            ("zsh/.zsh_plugins", ".zsh_plugins", "Zsh plugins"),
            ("zsh/.p10k.zsh", ".p10k.zsh", "Powerlevel10k theme"),
            ("zsh/.zlogin", ".zlogin", "Zsh login script"),
        ]

        for source_path, target_file, description in shell_configs:
            source = dotfiles_dir / source_path
            target = Path.home() / target_file
            if source.exists():
                if self.create_symlink(source, target, description):
                    success_count += 1
            total_steps += 1

        # Custom theme
        theme_source = dotfiles_dir / "iterm" / "steeef-lambda.zsh-theme"
        theme_target = (
            Path.home() / ".oh-my-zsh" / "custom" / "themes" / "steeef-lambda.zsh-theme"
        )
        if theme_source.exists():
            if self.create_symlink(theme_source, theme_target, "Custom Zsh theme"):
                success_count += 1
        total_steps += 1

        # Modular zsh configuration
        zsh_modules_dir = dotfiles_dir / "zsh"
        if zsh_modules_dir.exists():
            console.print("Setting up modular Zsh configuration...")
            zsh_config_dir = Path.home() / ".config" / "zsh"
            zsh_config_dir.mkdir(parents=True, exist_ok=True)

            module_count = 0
            for module_file in zsh_modules_dir.glob("*.zsh"):
                target_module = zsh_config_dir / module_file.name
                if self.create_symlink(
                    module_file, target_module, f"Zsh module: {module_file.name}"
                ):
                    module_count += 1

            console.print(f"[green]✓ {module_count} Zsh modules configured[/green]")

        return success_count, total_steps

    def setup_git_config(self, dotfiles_dir: Path) -> bool:
        """Set up git configuration symlinks."""
        console.print("\n[bold cyan]🔧 Setting up Git configuration...[/bold cyan]")

        # ~/.gitconfig is machine-managed (work/local config) and is never overwritten.
        # We symlink our personal dotfiles config to ~/.config/git/.gitconfig-local
        # and ensure ~/.gitconfig includes it.
        git_config_dir = Path.home() / ".config" / "git"
        git_config_dir.mkdir(parents=True, exist_ok=True)
        git_source = dotfiles_dir / "git" / ".gitconfig"
        git_target = git_config_dir / ".gitconfig-local"
        ok = self.create_symlink(git_source, git_target, "Git personal config (via include)")

        # Append [include] to ~/.gitconfig if not already present
        global_gitconfig = Path.home() / ".gitconfig"
        include_block = '[include]\n\tpath = ~/.config/git/.gitconfig-local\n'
        if global_gitconfig.exists():
            contents = global_gitconfig.read_text()
            if "~/.config/git/.gitconfig-local" not in contents:
                global_gitconfig.write_text(contents.rstrip() + "\n\n" + include_block)
                console.print("[green]✓ Appended [include] to ~/.gitconfig[/green]")
            else:
                console.print("[green]✓ ~/.gitconfig already includes personal config[/green]")
        else:
            global_gitconfig.write_text(include_block)
            console.print("[yellow]⚠ ~/.gitconfig not found — created with [include] only[/yellow]")

        ignore_source = dotfiles_dir / "git" / ".gitignore_global"
        if ignore_source.exists():
            ignore_target = Path.home() / ".gitignore_global"
            self.create_symlink(ignore_source, ignore_target, "Global gitignore")

        # Symlink context-specific git configs into ~/.config/git/
        for name in (".gitconfig-personal",):
            src = dotfiles_dir / "git" / name
            if src.exists():
                self.create_symlink(src, git_config_dir / name, f"Git config: {name}")

        return ok

    def setup_vim_config(self, dotfiles_dir: Path) -> bool:
        """Set up vim configuration symlink."""
        console.print("\n[bold cyan]📝 Setting up Vim configuration...[/bold cyan]")
        vim_source = dotfiles_dir / "vim" / ".vimrc"
        if vim_source.exists():
            vim_target = Path.home() / ".vimrc"
            return self.create_symlink(vim_source, vim_target, "Vim configuration")
        return True  # Not an error if vim config doesn't exist

    def setup_mise_config(self, dotfiles_dir: Path) -> bool:
        """Set up mise global configuration symlink."""
        console.print("\n[bold cyan]🔧 Setting up mise configuration...[/bold cyan]")
        mise_source = dotfiles_dir / "mise" / "config.toml"
        if mise_source.exists():
            mise_target = Path.home() / ".config" / "mise" / "config.toml"
            return self.create_symlink(mise_source, mise_target, "mise global config")
        return True

    def setup_direnv_config(self, dotfiles_dir: Path) -> bool:
        """Set up direnv global configuration symlink."""
        console.print("\n[bold cyan]🔧 Setting up direnv configuration...[/bold cyan]")
        direnv_source = dotfiles_dir / "direnv" / "direnvrc"
        if direnv_source.exists():
            direnv_target = Path.home() / ".config" / "direnv" / "direnvrc"
            return self.create_symlink(direnv_source, direnv_target, "direnv global config")
        return True

    def setup_nvim_config(self, dotfiles_dir: Path) -> bool:
        """Set up Neovim configuration symlink."""
        console.print("\n[bold cyan]📝 Setting up Neovim configuration...[/bold cyan]")
        nvim_source = dotfiles_dir / "nvim"
        if nvim_source.exists():
            nvim_target = Path.home() / ".config" / "nvim"
            return self.create_symlink(nvim_source, nvim_target, "Neovim configuration")
        return True  # Not an error if nvim config doesn't exist

    def setup_borders_config(self, dotfiles_dir: Path) -> bool:
        """Set up borders window border configuration symlink."""
        console.print("\n[bold cyan]🔲 Setting up borders configuration...[/bold cyan]")
        borders_source = dotfiles_dir / "borders" / "bordersrc"
        if borders_source.exists():
            borders_target = Path.home() / ".config" / "borders" / "bordersrc"
            return self.create_symlink(borders_source, borders_target, "borders config")
        return True

    def setup_kitty_config(self, dotfiles_dir: Path) -> Tuple[int, int]:
        """Set up kitty configuration symlinks. Returns (success_count, total_steps)."""
        console.print("\n[bold cyan]🐱 Setting up Kitty terminal...[/bold cyan]")

        success_count = 0
        total_steps = 0

        # Kitty configuration
        kitty_source = dotfiles_dir / "kitty" / "kitty.conf"
        if kitty_source.exists():
            kitty_target = Path.home() / ".config" / "kitty" / "kitty.conf"
            if self.create_symlink(kitty_source, kitty_target, "Kitty configuration"):
                success_count += 1
            total_steps += 1

        # Kitty customizations directory
        kitty_custom_source = dotfiles_dir / "kitty" / "kitty-customizations"
        if kitty_custom_source.exists():
            kitty_custom_target = (
                Path.home() / ".config" / "kitty" / "kitty-customizations"
            )
            if self.create_symlink(
                kitty_custom_source, kitty_custom_target, "Kitty customizations"
            ):
                success_count += 1
            total_steps += 1

        # tab_bar.py must be at the kitty config root (not in a subdirectory)
        tab_bar_source = dotfiles_dir / "kitty" / "kitty-customizations" / "tab_bar.py"
        if tab_bar_source.exists():
            tab_bar_target = Path.home() / ".config" / "kitty" / "tab_bar.py"
            if self.create_symlink(tab_bar_source, tab_bar_target, "Kitty tab bar"):
                success_count += 1
            total_steps += 1

        return success_count, total_steps
