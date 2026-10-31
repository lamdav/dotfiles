#!/usr/bin/env python3

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

from rich.console import Console
from rich.prompt import Confirm

from installer.interfaces import SymlinkManager

console = Console()


@dataclass(frozen=True)
class SymlinkSpec:
    """A single declared symlink: dotfiles-relative source -> home-relative target.

    `platform` is None for all platforms, or "macos"/"linux" to restrict it —
    this is the single source of truth `status()` reads from, so a spec added
    here is automatically picked up by the status table without having to
    remember to add a second, separate row by hand.
    """

    source: str
    target: str
    description: str
    platform: Optional[str] = None


# Simple one-to-one symlinks. Setup functions below build their source/target
# paths from these constants so there is exactly one place to add a new
# mapping; `status()` reads the same list.
ZSHRC = SymlinkSpec("zsh/.zshrc", ".zshrc", "Zsh configuration")
ZSH_PLUGINS = SymlinkSpec("zsh/.zsh_plugins", ".zsh_plugins", "Zsh plugins")
P10K_THEME = SymlinkSpec("zsh/.p10k.zsh", ".p10k.zsh", "Powerlevel10k theme")
ZLOGIN = SymlinkSpec("zsh/.zlogin", ".zlogin", "Zsh login script")

GITCONFIG = SymlinkSpec("git/.gitconfig", ".config/git/.gitconfig", "Git configuration")
GITIGNORE_GLOBAL = SymlinkSpec(
    "git/.gitignore_global", ".gitignore_global", "Global gitignore"
)
GITCONFIG_PERSONAL = SymlinkSpec(
    "git/.gitconfig-personal", ".config/git/.gitconfig-personal", "Git config: personal"
)
GITCONFIG_WORK = SymlinkSpec(
    "git/.gitconfig-work", ".config/git/.gitconfig-work", "Git config: work"
)

VIM_CONFIG = SymlinkSpec("vim/.vimrc", ".vimrc", "Vim configuration")
NVIM_CONFIG = SymlinkSpec("nvim", ".config/nvim", "Neovim configuration")
MISE_CONFIG = SymlinkSpec("mise/config.toml", ".config/mise/config.toml", "mise config")
DIRENV_CONFIG = SymlinkSpec(
    "direnv/direnvrc", ".config/direnv/direnvrc", "direnv config"
)

GLOW_CONFIG_MACOS = SymlinkSpec(
    "glow/glow.yml", "Library/Preferences/glow/glow.yml", "glow config", "macos"
)
GLOW_CONFIG_LINUX = SymlinkSpec(
    "glow/glow.yml", ".config/glow/glow.yml", "glow config", "linux"
)

ATUIN_CONFIG = SymlinkSpec("atuin/config.toml", ".atuin/config.toml", "atuin config")
ATUIN_THEMES = SymlinkSpec("atuin/themes", ".atuin/themes", "atuin themes")

CLAUDE_CONFIG = SymlinkSpec(
    "claude/settings.json", ".claude/settings.json", "Claude Code settings"
)

BORDERS_CONFIG = SymlinkSpec(
    "borders/bordersrc", ".config/borders/bordersrc", "borders config", "macos"
)

KITTY_CONF = SymlinkSpec(
    "kitty/kitty.conf", ".config/kitty/kitty.conf", "Kitty configuration", "macos"
)
KITTY_CUSTOMIZATIONS = SymlinkSpec(
    "kitty/kitty-customizations",
    ".config/kitty/kitty-customizations",
    "Kitty customizations",
    "macos",
)

# Single source of truth for `status()`. Add a new simple mapping above and
# to this list, and it shows up in `dot status` with no further wiring.
SYMLINK_TARGETS: List[SymlinkSpec] = [
    ZSHRC,
    ZSH_PLUGINS,
    P10K_THEME,
    ZLOGIN,
    GITCONFIG,
    GITIGNORE_GLOBAL,
    GITCONFIG_PERSONAL,
    GITCONFIG_WORK,
    VIM_CONFIG,
    NVIM_CONFIG,
    MISE_CONFIG,
    DIRENV_CONFIG,
    GLOW_CONFIG_MACOS,
    GLOW_CONFIG_LINUX,
    ATUIN_CONFIG,
    ATUIN_THEMES,
    CLAUDE_CONFIG,
    BORDERS_CONFIG,
    KITTY_CONF,
    KITTY_CUSTOMIZATIONS,
]


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
        for spec in (ZSHRC, ZSH_PLUGINS, P10K_THEME, ZLOGIN):
            source = dotfiles_dir / spec.source
            target = Path.home() / spec.target
            if source.exists():
                if self.create_symlink(source, target, spec.description):
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

        # Platform-specific zsh directories
        import platform as _platform

        _system = _platform.system()
        if _system == "Darwin":
            platform_dirs = ["macos"]
        elif _system == "Linux":
            platform_dirs = ["linux", "ubuntu"]
        else:
            platform_dirs = []

        for platform_dir in platform_dirs:
            platform_source = dotfiles_dir / "zsh" / platform_dir
            if platform_source.exists():
                platform_target = zsh_config_dir / platform_dir
                self.create_symlink(
                    platform_source,
                    platform_target,
                    f"Zsh platform dir: {platform_dir}",
                )

        return success_count, total_steps

    def setup_git_config(self, dotfiles_dir: Path) -> bool:
        """Set up git configuration symlinks."""
        console.print("\n[bold cyan]🔧 Setting up Git configuration...[/bold cyan]")

        # ~/.config/git/.gitconfig is a symlink to the dotfiles config.
        # ~/.gitconfig is machine-managed — created as a plain file (hard copy) with
        # an [include] pointing to ~/.config/git/.gitconfig. Never symlinked.
        git_config_dir = Path.home() / ".config" / "git"
        git_config_dir.mkdir(parents=True, exist_ok=True)
        git_source = dotfiles_dir / GITCONFIG.source
        git_target = Path.home() / GITCONFIG.target
        ok = self.create_symlink(git_source, git_target, GITCONFIG.description)

        # Bootstrap ~/.gitconfig as a plain file if it doesn't already include our config
        global_gitconfig = Path.home() / ".gitconfig"
        include_line = "path = ~/.config/git/.gitconfig"
        include_block = f"[include]\n\t{include_line}\n"
        if global_gitconfig.exists():
            contents = global_gitconfig.read_text()
            if include_line not in contents:
                global_gitconfig.write_text(contents.rstrip() + "\n\n" + include_block)
                console.print("[green]✓ Appended [include] to ~/.gitconfig[/green]")
            else:
                console.print(
                    "[green]✓ ~/.gitconfig already includes dotfiles config[/green]"
                )
        else:
            global_gitconfig.write_text(include_block)
            console.print("[green]✓ Created ~/.gitconfig with [include][/green]")

        ignore_source = dotfiles_dir / GITIGNORE_GLOBAL.source
        if ignore_source.exists():
            ignore_target = Path.home() / GITIGNORE_GLOBAL.target
            self.create_symlink(
                ignore_source, ignore_target, GITIGNORE_GLOBAL.description
            )

        # Bootstrap ~/.config/git/.gitconfig-local as a plain empty file if absent.
        # This is machine-local (not in the repo). Users configure it themselves.
        gitconfig_local = git_config_dir / ".gitconfig-local"
        if not gitconfig_local.exists() and not gitconfig_local.is_symlink():
            gitconfig_local.touch()
            console.print(
                "[green]✓ Created empty ~/.config/git/.gitconfig-local[/green]"
            )
        else:
            console.print(
                "[green]✓ ~/.config/git/.gitconfig-local already exists[/green]"
            )

        # Symlink context-specific git configs into ~/.config/git/
        for spec in (GITCONFIG_PERSONAL, GITCONFIG_WORK):
            src = dotfiles_dir / spec.source
            if src.exists():
                self.create_symlink(src, Path.home() / spec.target, spec.description)

        return ok

    def setup_vim_config(self, dotfiles_dir: Path) -> bool:
        """Set up vim configuration symlink."""
        console.print("\n[bold cyan]📝 Setting up Vim configuration...[/bold cyan]")
        vim_source = dotfiles_dir / VIM_CONFIG.source
        if vim_source.exists():
            vim_target = Path.home() / VIM_CONFIG.target
            return self.create_symlink(vim_source, vim_target, VIM_CONFIG.description)
        return True  # Not an error if vim config doesn't exist

    def setup_mise_config(self, dotfiles_dir: Path) -> bool:
        """Set up mise global configuration symlink."""
        console.print("\n[bold cyan]🔧 Setting up mise configuration...[/bold cyan]")
        mise_source = dotfiles_dir / MISE_CONFIG.source
        if mise_source.exists():
            mise_target = Path.home() / MISE_CONFIG.target
            return self.create_symlink(
                mise_source, mise_target, MISE_CONFIG.description
            )
        return True

    def setup_direnv_config(self, dotfiles_dir: Path) -> bool:
        """Set up direnv global configuration symlink."""
        console.print("\n[bold cyan]🔧 Setting up direnv configuration...[/bold cyan]")
        direnv_source = dotfiles_dir / DIRENV_CONFIG.source
        if direnv_source.exists():
            direnv_target = Path.home() / DIRENV_CONFIG.target
            return self.create_symlink(
                direnv_source, direnv_target, DIRENV_CONFIG.description
            )
        return True

    def setup_nvim_config(self, dotfiles_dir: Path) -> bool:
        """Set up Neovim configuration symlink."""
        console.print("\n[bold cyan]📝 Setting up Neovim configuration...[/bold cyan]")
        nvim_source = dotfiles_dir / NVIM_CONFIG.source
        if nvim_source.exists():
            nvim_target = Path.home() / NVIM_CONFIG.target
            return self.create_symlink(
                nvim_source, nvim_target, NVIM_CONFIG.description
            )
        return True  # Not an error if nvim config doesn't exist

    def setup_borders_config(self, dotfiles_dir: Path) -> bool:
        """Set up borders window border configuration symlink."""
        console.print("\n[bold cyan]🔲 Setting up borders configuration...[/bold cyan]")
        borders_source = dotfiles_dir / BORDERS_CONFIG.source
        if borders_source.exists():
            borders_target = Path.home() / BORDERS_CONFIG.target
            return self.create_symlink(
                borders_source, borders_target, BORDERS_CONFIG.description
            )
        return True

    def setup_claude_config(self, dotfiles_dir: Path) -> bool:
        """Set up Claude Code settings symlink."""
        console.print(
            "\n[bold cyan]🤖 Setting up Claude Code configuration...[/bold cyan]"
        )
        claude_source = dotfiles_dir / CLAUDE_CONFIG.source
        if not claude_source.exists():
            return True

        claude_target = Path.home() / CLAUDE_CONFIG.target
        return self.create_symlink(
            claude_source, claude_target, CLAUDE_CONFIG.description
        )

    def setup_glow_config(self, dotfiles_dir: Path) -> bool:
        """Set up glow markdown viewer configuration symlink."""
        console.print("\n[bold cyan]📖 Setting up glow configuration...[/bold cyan]")

        import platform as _platform

        # glow follows os.UserConfigDir(), which is ~/Library/Preferences on macOS
        spec = (
            GLOW_CONFIG_MACOS if _platform.system() == "Darwin" else GLOW_CONFIG_LINUX
        )
        glow_source = dotfiles_dir / spec.source
        if not glow_source.exists():
            return True

        glow_target = Path.home() / spec.target
        return self.create_symlink(glow_source, glow_target, spec.description)

    def setup_atuin_config(self, dotfiles_dir: Path) -> bool:
        """Set up atuin shell history configuration and themes symlinks."""
        console.print("\n[bold cyan]🕐 Setting up atuin configuration...[/bold cyan]")
        atuin_source = dotfiles_dir / ATUIN_CONFIG.source
        success = True
        if atuin_source.exists():
            atuin_target = Path.home() / ATUIN_CONFIG.target
            success = self.create_symlink(
                atuin_source, atuin_target, ATUIN_CONFIG.description
            )

        themes_source = dotfiles_dir / ATUIN_THEMES.source
        if themes_source.exists():
            themes_target = Path.home() / ATUIN_THEMES.target
            success = (
                self.create_symlink(
                    themes_source, themes_target, ATUIN_THEMES.description
                )
                and success
            )
        return success

    def setup_kitty_config(self, dotfiles_dir: Path) -> Tuple[int, int]:
        """Set up kitty configuration symlinks. Returns (success_count, total_steps)."""
        import platform as _platform

        if _platform.system() == "Linux":
            console.print(
                "[yellow]⚠ Skipping Kitty config on Linux (server environment)[/yellow]"
            )
            return 0, 0

        console.print("\n[bold cyan]🐱 Setting up Kitty terminal...[/bold cyan]")

        success_count = 0
        total_steps = 0

        # Kitty configuration and customizations directory
        for spec in (KITTY_CONF, KITTY_CUSTOMIZATIONS):
            source = dotfiles_dir / spec.source
            if source.exists():
                target = Path.home() / spec.target
                if self.create_symlink(source, target, spec.description):
                    success_count += 1
                total_steps += 1

        return success_count, total_steps
