from pathlib import Path
import sh
import pytest
from pytest_mock import MockerFixture
from kernel_builder.utils.source import SourceManager
from pytest_mock.plugin import MockType
import importlib


class FakeResp:
    url = "https://github.com/torvalds/linux"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass


def test_clone_sources_logs_and_calls(mocker: MockerFixture):
    mocker.patch.object(SourceManager, "clone_repo", return_value=None)
    spy_clone = mocker.spy(SourceManager, "clone_repo")
    spy_log: MockType = mocker.spy(
        importlib.import_module("kernel_builder.utils.source"), "log"
    )

    sm: SourceManager = SourceManager(
        sources=[
            {
                "url": "github.com:foo/bar",
                "branch": "main",
                "to": "bar",
            }
        ]
    )
    sm.clone_sources()

    spy_clone.assert_called_once()
    assert (
        "Cloning github.com:foo/bar into bar on branch main" in spy_log.call_args[0][0]
    )


def test_git_simplifier(mocker: MockerFixture):
    mocker.patch("kernel_builder.utils.source.requests.get", return_value=FakeResp())

    sm: SourceManager = SourceManager()
    simplified: str = sm.git_simplifier("https://github.com/torvalds/linux")
    assert simplified == "github.com:torvalds/linux"


def test_restore_simplified():
    original = "github.com:foo/bar"
    full = SourceManager.restore_simplified(original)
    assert full == "https://github.com/foo/bar"

    assert SourceManager.restore_simplified(full) == full
