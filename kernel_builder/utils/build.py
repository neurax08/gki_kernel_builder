import os
import re
import sys
from os import cpu_count
from pathlib import Path

from sh import make

from kernel_builder.config.config import BUILD_HOST, BUILD_USER, DEFCONFIG, IMAGE_COMP
from kernel_builder.constants import (
    CLANG_TRIPLE,
    CROSS_COMPILE,
    LLVM,
    LLVM_IAS,
    TOOLCHAIN,
    WORKSPACE,
)
from kernel_builder.pre_build.configurator import configurator
from kernel_builder.utils.fs import FileSystem
from kernel_builder.utils.log import log


class Builder:
    def __init__(self) -> None:
        self.fs: FileSystem = FileSystem()
        self.clang_bin: Path = TOOLCHAIN / "clang" / "bin"
        self.workspace: Path = WORKSPACE
        self.defconfig: str = DEFCONFIG
        self.image_comp: str = IMAGE_COMP
        self.jobs: int = cpu_count() or 4

        BUILD_ENV_OVERRIDES = {
            # Arch
            "ARCH": "arm64",
            "SUBARCH": "arm64",
            # Kbuild
            "KBUILD_BUILD_USER": BUILD_USER,
            "KBUILD_BUILD_HOST": BUILD_HOST,
            # Clang
            "PATH": f"{self.clang_bin}{os.pathsep}{os.getenv('PATH', '')}",
            "CC": "ccache clang",
            "CXX": "ccache clang++",
            # Cross compile
            "CLANG_TRIPLE": CLANG_TRIPLE,
            "CROSS_COMPILE": CROSS_COMPILE,
            # LLVM
            "LLVM": LLVM,
            "LLVM_IAS": LLVM_IAS,
            "LD": str(self.clang_bin / "ld.lld"),
        }
        self.make_env: dict[str, str] = {**os.environ, **BUILD_ENV_OVERRIDES}

    def _make(self, args: list[str] | None = None, *, jobs: int) -> None:
        make(
            f"-j{jobs}",
            *(args or []),
            "O=out",
            _cwd=Path.cwd(),
            _env={**self.make_env},
            _out=sys.stdout,
            _err=sys.stderr,
        )

    def build(self, jobs: int | None = None) -> None:
        target: str = (
            "Image" if self.image_comp == "raw" else f"Image.{self.image_comp}"
        )
        jobs = jobs or self.jobs
        log(f"Start build: {self.defconfig=}, {jobs or self.jobs=}, {self.image_comp=}")
        self._make([self.defconfig], jobs=jobs)

        configurator()

        log("Making olddefconfig")
        self._make(["olddefconfig"], jobs=jobs)

        log("Starting full build.")
        self._make([target, "modules"], jobs=jobs)
        log("Build completed successfully.")

    def get_kernel_version(self) -> str:
        log("Fetching kernel version...")
        makefile: str = (self.workspace / "Makefile").read_text()
        version: dict[str, str] = dict(
            re.findall(r"^(VERSION|PATCHLEVEL|SUBLEVEL)\s*=\s*(\d+)$", makefile, re.M)
        )
        required = {"VERSION", "PATCHLEVEL", "SUBLEVEL"}
        if not required.issubset(version):
            raise RuntimeError("Unable to determine kernel version")
        return f"{version['VERSION']}.{version['PATCHLEVEL']}.{version['SUBLEVEL']}"


if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
