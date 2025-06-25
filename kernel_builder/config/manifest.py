from typing import Final, TypeAlias

from kernel_builder.constants import TOOLCHAIN, WORKSPACE

from .config import ANYKERNEL_BRANCH, ANYKERNEL_REPO, KERNEL_BRANCH, KERNEL_REPO

# Simplified Git link format
#
# 1. Format
#    {host}:{user}/{repo}
#    Example: github.com:bachnxuan/gki_kernel_builder
#
# 2. Rules
#    - Do not include the ".git" suffix
#    - Do not use git ssh links (only https/http)

Source: TypeAlias = Final[dict[str, str]]

KERNEL: Source = {
    "url": KERNEL_REPO,
    "branch": KERNEL_BRANCH,
    "to": str(WORKSPACE),
}

ANYKERNEL: Source = {
    "url": ANYKERNEL_REPO,
    "branch": ANYKERNEL_BRANCH,
    "to": str(WORKSPACE / "AnyKernel3"),
}

BUILD_TOOL: Source = {
    "url": "android.googlesource.com:kernel/prebuilts/build-tools",
    "branch": "main-kernel-build-2024",
    "to": str(TOOLCHAIN / "build-tools"),
}

MKBOOTIMG: Source = {
    "url": "android.googlesource.com:platform/system/tools/mkbootimg",
    "branch": "main-kernel-build-2024",
    "to": str(TOOLCHAIN / "mkbootimg"),
}

SUSFS: Source = {
    "url": "gitlab.com:simonpunk/susfs4ksu",
    "branch": "gki-android12-5.10",
    "to": str(WORKSPACE / "susfs4ksu"),
}

SOURCES: Final[list[Source]] = [
    KERNEL,
    ANYKERNEL,
    BUILD_TOOL,
    MKBOOTIMG,
    SUSFS,
]

if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
