from pathlib import Path
from kernel_builder.utils.fs import FileSystem
import pytest
import os


@pytest.fixture(autouse=True)
def restore_cwd():
    original = Path.cwd()
    yield
    os.chdir(original)

def test_reset_path(tmp_path: Path) -> None:
    p: Path = tmp_path / "out"
    p.mkdir()
    (p / "text").write_text("x")
    FileSystem.reset_path(p)
    assert p.exists() and not any(p.iterdir())


class TestChangeDir:
    def test_cd(self, tmp_path: Path) -> None:
        target: Path = tmp_path / "target_folder"
        target.mkdir(parents=True)
        FileSystem.cd(target)
        assert Path.cwd() == target

    def test_path_nonexistence(self) -> None:
        target: Path = Path("foo/bar")
        with pytest.raises(FileNotFoundError):
            FileSystem.cd(target)

    def test_path_is_a_file(self, tmp_path: Path) -> None:
        target: Path = tmp_path / "dummy_text_file"
        target.write_text("hello world")
        with pytest.raises(NotADirectoryError):
            FileSystem.cd(target)
