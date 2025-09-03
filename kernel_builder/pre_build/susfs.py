import os
import shutil
from pathlib import Path

from kernel_builder.constants import WORKSPACE
from kernel_builder.utils.command import apply_patch
from kernel_builder.utils.log import log


class SUSFSPatcher:
    def __init__(self, ksu: str, susfs: bool) -> None:
        self.ksu_variant: str = ksu
        self.susfs: bool = susfs

    def copy(self, src: Path, dest: Path):
        log(f"Copying content from folder {src} to {dest}")
        for entry in os.scandir(src):
            src_path: str = entry.path
            dst_path: str = os.path.join(dest, entry.name)
            if entry.is_dir():
                shutil.copytree(src_path, dst_path)
            else:
                shutil.copy2(src_path, dst_path)

    def _apply_patch_folder(self, path: Path, target: Path) -> None:
        for patch_file in path.iterdir():
            if patch_file.suffix != ".patch":
                continue
            apply_patch(patch_file, check=False, cwd=target)

    def apply(self) -> None:
        if self.ksu_variant == "NONE" or not self.susfs:
            return

        os.chdir(WORKSPACE)

        SUSFS: Path = WORKSPACE / "susfs4ksu" / "kernel_patches"
        GKI_SUSFS: Path = SUSFS / "50_add_susfs_in_gki-android12-5.10.patch"

        log("Applying kernel-side SUSFS patches")
        self.copy(SUSFS / "fs", WORKSPACE / "fs")
        self.copy(SUSFS / "include" / "linux", WORKSPACE / "include" / "linux")

        apply_patch(GKI_SUSFS)


if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
