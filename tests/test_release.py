"""Tests for `dot release` / `dot next` (installer/main.py).

These mock every `subprocess.run` call, so no real git commands run and
nothing ever touches an actual repository or home directory.
"""

from dataclasses import dataclass, field

import pytest
from typer.testing import CliRunner

from installer import main as main_module

runner = CliRunner()


@dataclass
class FakeResult:
    returncode: int = 0
    stdout: str = ""
    stderr: str = ""


@dataclass
class FakeRun:
    """Routes subprocess.run calls to canned responses by predicate, in order."""

    routes: list = field(default_factory=list)
    calls: list = field(default_factory=list)

    def add(self, predicate, result: FakeResult | None = None):
        self.routes.append((predicate, result or FakeResult()))
        return self

    def __call__(self, cmd, *args, check=False, **kwargs):
        self.calls.append(cmd)
        for predicate, result in self.routes:
            if predicate(cmd):
                if check and result.returncode != 0:
                    raise main_module.subprocess.CalledProcessError(
                        result.returncode, cmd
                    )
                return result
        raise AssertionError(f"Unexpected subprocess call: {cmd}")


def is_git(cmd, *parts):
    return cmd[0] == "git" and all(p in cmd for p in parts)


def test_release_rejects_multiple_bump_flags():
    result = runner.invoke(main_module.app, ["release", "--patch", "--minor"])
    assert result.exit_code == 1


@pytest.mark.parametrize(
    "flag,expected_bump_args",
    [
        (None, ["--bump"]),
        ("--patch", ["--bump", "patch"]),
        ("--minor", ["--bump", "minor"]),
        ("--major", ["--bump", "major"]),
    ],
)
def test_release_builds_correct_bump_args(monkeypatch, flag, expected_bump_args):
    """Regression test: --bump-patch/-minor/-major don't exist in git-cliff —
    the real flag is `--bump <major|minor|patch>`."""
    fake = FakeRun()
    fake.add(lambda c: is_git(c, "tag", "--list"), FakeResult(stdout="v1.0.0"))
    fake.add(
        lambda c: is_git(c, "cliff", "--bumped-version"),
        FakeResult(stdout="v1.1.0"),
    )
    fake.add(lambda c: is_git(c, "rev-parse", "--verify"), FakeResult(returncode=1))
    fake.add(
        lambda c: is_git(c, "cliff", "--unreleased"), FakeResult(stdout="- a feat")
    )
    fake.add(lambda c: is_git(c, "cliff", "--tag"))
    fake.add(lambda c: is_git(c, "add", "CHANGELOG.md"))
    fake.add(lambda c: is_git(c, "commit"))
    fake.add(lambda c: is_git(c, "tag", "-a"))
    monkeypatch.setattr(main_module.subprocess, "run", fake)

    args = ["release"] + ([flag] if flag else [])
    result = runner.invoke(main_module.app, args)

    assert result.exit_code == 0, result.output
    bumped_version_call = next(
        c for c in fake.calls if is_git(c, "cliff", "--bumped-version")
    )
    assert bumped_version_call[2:-1] == expected_bump_args


def test_release_exits_cleanly_when_nothing_to_bump(monkeypatch):
    fake = FakeRun()
    fake.add(lambda c: is_git(c, "tag", "--list"), FakeResult(stdout="v1.0.0"))
    fake.add(
        lambda c: is_git(c, "cliff", "--bumped-version"),
        FakeResult(stderr="There is nothing to bump"),
    )
    monkeypatch.setattr(main_module.subprocess, "run", fake)

    result = runner.invoke(main_module.app, ["release"])

    assert result.exit_code == 1


def test_release_refuses_to_overwrite_existing_tag(monkeypatch):
    """Regression test: a stale/colliding tag used to blow up with a raw
    CalledProcessError traceback deep inside `git tag -a`, after the release
    commit had already been made. It should be caught up front instead."""
    fake = FakeRun()
    fake.add(lambda c: is_git(c, "tag", "--list"), FakeResult(stdout="v1.3.0"))
    fake.add(
        lambda c: is_git(c, "cliff", "--bumped-version"),
        FakeResult(stdout="v1.3.0"),
    )
    fake.add(lambda c: is_git(c, "rev-parse", "--verify"), FakeResult(returncode=0))
    monkeypatch.setattr(main_module.subprocess, "run", fake)

    result = runner.invoke(main_module.app, ["release"])

    assert result.exit_code == 1
    assert "already exists" in result.output
    assert not any(is_git(c, "commit") for c in fake.calls)
    assert not any(is_git(c, "tag", "-a") for c in fake.calls)


def test_release_strips_unreleased_banner_from_body(monkeypatch):
    """Regression test: the commit/tag body used to come from `--latest`,
    which resolves to the *previous* release since the new tag doesn't exist
    yet. It now comes from `--unreleased`, with the banner line dropped."""
    fake = FakeRun()
    fake.add(lambda c: is_git(c, "tag", "--list"), FakeResult(stdout="v1.0.0"))
    fake.add(
        lambda c: is_git(c, "cliff", "--bumped-version"),
        FakeResult(stdout="v1.1.0"),
    )
    fake.add(lambda c: is_git(c, "rev-parse", "--verify"), FakeResult(returncode=1))
    fake.add(
        lambda c: is_git(c, "cliff", "--unreleased"),
        FakeResult(stdout="## [unreleased]\n\n- a feat\n- a fix"),
    )
    fake.add(lambda c: is_git(c, "cliff", "--tag"))
    fake.add(lambda c: is_git(c, "add", "CHANGELOG.md"))
    fake.add(lambda c: is_git(c, "commit"))
    fake.add(lambda c: is_git(c, "tag", "-a"))
    monkeypatch.setattr(main_module.subprocess, "run", fake)

    result = runner.invoke(main_module.app, ["release"])
    assert result.exit_code == 0, result.output

    commit_call = next(c for c in fake.calls if is_git(c, "commit"))
    commit_message = commit_call[3]
    assert "## [unreleased]" not in commit_message
    assert "- a feat" in commit_message

    tag_call = next(c for c in fake.calls if is_git(c, "tag", "-a"))
    tag_message = tag_call[5]
    assert "## [unreleased]" not in tag_message


def test_next_version_reports_nothing_to_release(monkeypatch):
    fake = FakeRun()
    fake.add(
        lambda c: is_git(c, "cliff", "--bumped-version"),
        FakeResult(stderr="There is nothing to bump"),
    )
    fake.add(lambda c: is_git(c, "describe", "--tags"), FakeResult(stdout="v1.4.0"))
    monkeypatch.setattr(main_module.subprocess, "run", fake)

    result = runner.invoke(main_module.app, ["next"])

    assert result.exit_code == 1
