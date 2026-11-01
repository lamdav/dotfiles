"""Tests for installer/dotfiles_installer.py: install() orchestration and
status() reporting/--fix behavior.

install() tests swap in fake SymlinkManager/MacOSManager/PackageManager
objects instead of calling the real ones, so nothing here runs brew, apt,
curl, or any other real system-mutating command. status() tests run against
a tmp_path "home" and a small, test-local SymlinkSpec list monkeypatched in
place of the real SYMLINK_TARGETS, so nothing here touches a real home
directory either.
"""

from pathlib import Path

import pytest

from installer import dotfiles_installer as di_module
from installer.dotfiles_installer import DotfilesInstaller
from installer.enums import OSType
from installer.symlink_manager import SymlinkSpec


@pytest.fixture
def installer(tmp_path, monkeypatch):
    dotfiles_dir = (tmp_path / "dotfiles").resolve()
    dotfiles_dir.mkdir()
    home_dir = (tmp_path / "home").resolve()
    home_dir.mkdir()
    monkeypatch.setattr(Path, "home", lambda: home_dir)

    inst = DotfilesInstaller(dotfiles_dir)
    inst.system_manager.get_os_type = lambda: OSType.MACOS
    return inst


def with_specs(monkeypatch, specs, macos_specs=None):
    monkeypatch.setattr(di_module, "SYMLINK_TARGETS", specs)
    monkeypatch.setattr(di_module, "MACOS_SYMLINK_TARGETS", macos_specs or [])


# --- status() -----------------------------------------------------------


def test_status_reports_linked_symlink(installer, monkeypatch, capsys):
    source = installer.dotfiles_dir / "foo.conf"
    source.write_text("x")
    target = Path.home() / "foo.conf"
    target.symlink_to(source)
    with_specs(monkeypatch, [SymlinkSpec("foo.conf", "foo.conf", "Foo config")])

    installer.status()

    out = capsys.readouterr().out
    assert "Foo config" in out
    assert "Linked" in out


def test_status_reports_not_configured(installer, monkeypatch, capsys):
    source = installer.dotfiles_dir / "foo.conf"
    source.write_text("x")
    with_specs(monkeypatch, [SymlinkSpec("foo.conf", "foo.conf", "Foo config")])

    installer.status()

    out = capsys.readouterr().out
    assert "Not configured" in out


def test_status_fix_creates_missing_symlink(installer, monkeypatch, capsys):
    source = installer.dotfiles_dir / "foo.conf"
    source.write_text("x")
    with_specs(monkeypatch, [SymlinkSpec("foo.conf", "foo.conf", "Foo config")])

    installer.status(fix=True)

    target = Path.home() / "foo.conf"
    assert target.is_symlink()
    assert target.resolve() == source.resolve()
    assert "Fixed 1 symlink" in capsys.readouterr().out


def test_status_fix_leaves_correct_symlinks_untouched(installer, monkeypatch, capsys):
    source = installer.dotfiles_dir / "foo.conf"
    source.write_text("x")
    target = Path.home() / "foo.conf"
    target.symlink_to(source)
    with_specs(monkeypatch, [SymlinkSpec("foo.conf", "foo.conf", "Foo config")])

    installer.status(fix=True)

    assert "Nothing to fix" in capsys.readouterr().out


def test_status_filters_specs_by_platform(installer, monkeypatch, capsys):
    source = installer.dotfiles_dir / "linuxonly.conf"
    source.write_text("x")
    with_specs(
        monkeypatch,
        [SymlinkSpec("linuxonly.conf", "linuxonly.conf", "Linux-only config", "linux")],
    )
    # the `installer` fixture forces OSType.MACOS

    installer.status()

    assert "Linux-only config" not in capsys.readouterr().out


# --- install() ------------------------------------------------------------


class FakeSymlinkManager:
    def __init__(self):
        self.calls = []

    def create_symlink(self, source, target, description=""):
        return True

    def setup_shell_config(self, dotfiles_dir):
        self.calls.append("shell")
        return (2, 2)

    def setup_git_config(self, dotfiles_dir):
        self.calls.append("git")
        return True

    def setup_vim_config(self, dotfiles_dir):
        self.calls.append("vim")
        return True

    def setup_mise_config(self, dotfiles_dir):
        self.calls.append("mise")
        return True

    def setup_direnv_config(self, dotfiles_dir):
        self.calls.append("direnv")
        return True

    def setup_nvim_config(self, dotfiles_dir):
        self.calls.append("nvim")
        return True

    def setup_borders_config(self, dotfiles_dir):
        self.calls.append("borders")
        return True

    def setup_claude_config(self, dotfiles_dir):
        self.calls.append("claude")
        return True

    def setup_glow_config(self, dotfiles_dir):
        self.calls.append("glow")
        return True

    def setup_atuin_config(self, dotfiles_dir):
        self.calls.append("atuin")
        return True

    def setup_kitty_config(self, dotfiles_dir):
        self.calls.append("kitty")
        return (1, 1)


class FakeMacOSManager:
    def __init__(self):
        self.calls = []

    def setup_aerospace_config(self, dotfiles_dir):
        self.calls.append("aerospace")
        return True

    def setup_iterm_config(self, dotfiles_dir):
        self.calls.append("iterm")
        return True

    def setup_kitty_quick_access(self, system_manager):
        self.calls.append("kitty_quick_access")
        return True

    def setup_ubersicht(self, dotfiles_dir, system_manager, interactive=True):
        self.calls.append("ubersicht")
        return (1, 1)

    def configure_system_preferences(self, system_manager, interactive=True):
        self.calls.append("system_preferences")
        return True


class FakePackageManager:
    def __init__(self):
        self.called = False

    def install_packages(self, system_manager):
        self.called = True
        return True

    def get_package_manager_name(self):
        return "fake"


@pytest.fixture
def install_fakes(installer, monkeypatch):
    symlink_fake = FakeSymlinkManager()
    macos_fake = FakeMacOSManager()
    package_fake = FakePackageManager()

    installer.symlink_manager = symlink_fake
    installer.macos_manager = macos_fake
    monkeypatch.setattr(
        di_module, "create_package_manager", lambda os_type, dotfiles_dir: package_fake
    )
    monkeypatch.setattr(di_module.Confirm, "ask", lambda *a, **k: True)

    return installer, symlink_fake, macos_fake, package_fake


def test_install_skips_packages_and_shell_when_flagged(install_fakes):
    installer, symlink_fake, _macos_fake, package_fake = install_fakes

    installer.install(skip_packages=True, skip_shell=True, interactive=False)

    assert package_fake.called is False
    assert "shell" not in symlink_fake.calls
    assert "git" in symlink_fake.calls  # unskippable steps still ran


def test_install_runs_packages_and_shell_by_default(install_fakes):
    installer, symlink_fake, _macos_fake, package_fake = install_fakes

    installer.install(interactive=False)

    assert package_fake.called is True
    assert "shell" in symlink_fake.calls


def test_install_runs_macos_steps_only_on_macos(install_fakes):
    installer, _symlink_fake, macos_fake, _package_fake = install_fakes
    installer.system_manager.get_os_type = lambda: OSType.UBUNTU

    installer.install(interactive=False)

    assert macos_fake.calls == []


def test_install_skip_system_does_not_configure_system_preferences(install_fakes):
    installer, _symlink_fake, macos_fake, _package_fake = install_fakes

    installer.install(skip_system=True, interactive=False)

    assert "system_preferences" not in macos_fake.calls
    assert "aerospace" in macos_fake.calls  # other macOS steps still ran


def test_install_cancelled_when_user_declines(install_fakes, monkeypatch, capsys):
    installer, symlink_fake, macos_fake, package_fake = install_fakes
    monkeypatch.setattr(di_module.Confirm, "ask", lambda *a, **k: False)

    installer.install(interactive=True)

    assert symlink_fake.calls == []
    assert macos_fake.calls == []
    assert package_fake.called is False
    assert "cancelled" in capsys.readouterr().out.lower()


def test_install_reports_success_and_total_steps(install_fakes, capsys):
    installer, _symlink_fake, _macos_fake, _package_fake = install_fakes

    installer.install(interactive=False)

    out = capsys.readouterr().out
    assert "Successfully completed" in out
    assert "issues" not in out  # every fake returns success
