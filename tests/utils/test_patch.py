from sh import RunningCommand
from pathlib import Path
import subprocess
from types import SimpleNamespace
import pytest
from pytest_mock import MockerFixture
from kernel_builder.utils.command import apply_patch


@pytest.fixture
def dummy_patch(tmp_path: Path) -> Path:
    p: Path = tmp_path / "fix.patch"
    p.write_text("--- a/README.md\n+++ b/README.md\n@@\n-old line\n+new line\n")
    return p


def test_patch_success(mocker: MockerFixture, dummy_patch: Path):
    fake_proc: SimpleNamespace = SimpleNamespace(returncode=0, stdout=b"", stderr=b"")
    spy_run = mocker.patch(
        "kernel_builder.utils.command.patch",
        return_value=fake_proc,
    )
    result: RunningCommand = apply_patch(dummy_patch)
    spy_run.assert_called_once_with(
        _in=dummy_patch.read_bytes(),
        _cwd=str(Path.cwd()),
        _ok_code=[0],
    )
    assert result is fake_proc


def test_patch_failure(mocker: MockerFixture, dummy_patch: Path):
    err = subprocess.CalledProcessError(1, ["patch"])
    mocker.patch(
        "kernel_builder.utils.command.patch",
        side_effect=err,
    )

    with pytest.raises(subprocess.CalledProcessError) as exc:
        apply_patch(dummy_patch)

    assert exc.value is err
