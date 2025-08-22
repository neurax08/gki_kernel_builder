from pathlib import Path

import sh
from sh import Command

from kernel_builder.constants import ROOT
from kernel_builder.utils.fs import FileSystem
from kernel_builder.utils.log import log

curl: Command = sh.Command("curl").bake(
    "-fsSL", "--retry", "5", "--retry-all-errors", "--retry-delay", "2"
)
patch: Command = sh.Command("patch").bake("-p1", "--forward", "--fuzz=3")
aria2c: Command = sh.Command("aria2c").bake(
    "-x16", "-s32", "-k8M", "--file-allocation=falloc", "--timeout=60", "--retry-wait=5"
)


def apply_patch(
    patch_file: Path, *, check: bool = True, cwd: Path | None = None
) -> sh.RunningCommand:
    if not patch_file.exists():
        log(f"Patch not found at {patch_file}", "error")
        raise FileNotFoundError()
    log(f"Patching file: {FileSystem.relative_to(ROOT, patch_file)}")
    cwd = cwd or Path.cwd()
    data: bytes = patch_file.read_bytes()
    return patch(
        _in=data,
        _cwd=str(cwd),
        _ok_code=[0, 1] if not check else [0],
    )
