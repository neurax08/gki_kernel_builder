from pathlib import Path

from kernel_builder.constants import PATCHES
from kernel_builder.utils.command import apply_patch
from kernel_builder.utils.log import log


class LXCPatcher:
    def __init__(self, lxc: bool) -> None:
        self.lxc: bool = lxc

    def apply(self) -> None:
        LXC: Path = PATCHES / "lxc_support.patch"
        if self.lxc:
            log("Applying LXC Patches")
            apply_patch(LXC)
        else:
            return


if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
