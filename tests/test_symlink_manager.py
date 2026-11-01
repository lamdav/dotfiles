"""Tests for installer/symlink_manager.py.

create_symlink takes explicit Path arguments, so these exercise it against
tmp_path fixtures only — nothing here ever touches a real home directory.
"""

from installer.macos_manager import MACOS_SYMLINK_TARGETS
from installer.symlink_manager import SYMLINK_TARGETS, ConcreteSymlinkManager


def test_create_symlink_creates_new_link(tmp_path):
    source = tmp_path / "source.conf"
    source.write_text("content")
    target = tmp_path / "target.conf"

    assert ConcreteSymlinkManager().create_symlink(source, target, "test config")

    assert target.is_symlink()
    assert target.resolve() == source


def test_create_symlink_creates_missing_parent_dirs(tmp_path):
    source = tmp_path / "source.conf"
    source.write_text("content")
    target = tmp_path / "nested" / "dir" / "target.conf"

    assert ConcreteSymlinkManager().create_symlink(source, target, "test config")

    assert target.is_symlink()


def test_create_symlink_replaces_existing_file_when_confirmed(tmp_path, monkeypatch):
    monkeypatch.setattr("installer.symlink_manager.Confirm.ask", lambda *a, **k: True)
    source = tmp_path / "source.conf"
    source.write_text("new content")
    target = tmp_path / "target.conf"
    target.write_text("old content")

    assert ConcreteSymlinkManager().create_symlink(source, target, "test config")

    assert target.is_symlink()
    assert target.resolve() == source


def test_create_symlink_replaces_existing_dir_when_confirmed(tmp_path, monkeypatch):
    monkeypatch.setattr("installer.symlink_manager.Confirm.ask", lambda *a, **k: True)
    source = tmp_path / "source_dir"
    source.mkdir()
    target = tmp_path / "target_dir"
    target.mkdir()
    (target / "stale.txt").write_text("stale")

    assert ConcreteSymlinkManager().create_symlink(source, target, "test config")

    assert target.is_symlink()
    assert target.resolve() == source


def test_create_symlink_skips_when_declined(tmp_path, monkeypatch):
    monkeypatch.setattr("installer.symlink_manager.Confirm.ask", lambda *a, **k: False)
    source = tmp_path / "source.conf"
    source.write_text("new content")
    target = tmp_path / "target.conf"
    target.write_text("old content")

    assert not ConcreteSymlinkManager().create_symlink(source, target, "test config")

    assert not target.is_symlink()
    assert target.read_text() == "old content"


def test_symlink_spec_table_has_no_duplicate_targets_per_platform():
    """Regression guard for the declarative SymlinkSpec table: two entries
    with the same target and overlapping platform scope would silently
    clobber each other at install time."""
    all_specs = list(SYMLINK_TARGETS) + list(MACOS_SYMLINK_TARGETS)
    seen = {}
    for spec in all_specs:
        key = (spec.target, spec.platform)
        assert key not in seen, f"Duplicate target {spec.target!r} ({spec.platform})"
        seen[key] = spec
