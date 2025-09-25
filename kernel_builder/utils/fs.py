import shutil
from os import chdir
from pathlib import Path

from kernel_builder.utils.log import log


class FileSystem:
    @staticmethod
    def cd(path: Path) -> None:
        """
        A wrapper for os.chdir()

        :param path: Path to change to.
        :return: None
        """
        log(f"Changing directory to {path}")
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
                shutil.rmtree(path)
            else:
                path.unlink()
        path.mkdir(parents=True)


if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
