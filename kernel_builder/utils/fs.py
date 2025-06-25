import shutil
from os import chdir
from pathlib import Path

from kernel_builder.constants import ROOT
from kernel_builder.utils.log import log


class FileSystem:
    @staticmethod
    def is_subpath(parent: Path, child: Path) -> bool:
        try:
            child = child.resolve()
            parent = parent.resolve()
            return parent in child.parents or child == parent
        except FileNotFoundError:
            return False

    @staticmethod
    def relative_to(base: Path, path: Path) -> Path:
        try:
            return path.relative_to(base)
        except ValueError:
            return path

    @staticmethod
    def mkdir(path: Path) -> None:
        """
        Create path and parents if missing (same as mkdir -p).

        :param path: Path to create.
        :return: None
        """
        log(f"Creating directory: {FileSystem.relative_to(ROOT, path)}")
        path.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def cd(path: Path) -> None:
        """
        A more verbose wrapper for os.chdir()

        :param path: Path to change to.
        :return: None
        """
        log(f"Changing directory to {FileSystem.relative_to(ROOT, path)}")
        if path.exists():
            if path.is_dir():
                chdir(path)
            else:
                raise NotADirectoryError(f"Path is not a directory: {path}")
        else:
            raise FileNotFoundError(f"Path does not exist: {path}")

    @staticmethod
    def reset_path(path: Path) -> None:
        """
        - If path does not exist -> create it.
        - If path is an empty dir or non-empty -> remove & recreate.
        - If path is a file/symlink -> delete it.

        :param path: Path to reset.
        :return: None
        """
        if path.exists():
            if path.is_dir():
                log(f"Removing existing directory: {path}")
                shutil.rmtree(path)
            else:
                log(f"Removing file/symlink: {path}")
                path.unlink()
        log(f"Creating path: {path}")
        FileSystem.mkdir(path)


if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
