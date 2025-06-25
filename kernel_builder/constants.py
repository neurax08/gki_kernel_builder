from pathlib import Path
from typing import Final

# Paths
ROOT: Final[Path] = Path(__file__).resolve().parent.parent
SRC: Final[Path] = Path(__file__).resolve().parent

OUTPUT: Final[Path] = ROOT / "dist"
WILD_PATCHES: Path = ROOT / "wild_patches"
WORKSPACE: Final[Path] = ROOT / "kernel"
TOOLCHAIN: Final[Path] = ROOT / "toolchain"
PATCHES: Final[Path] = ROOT / "kernel_patches"
VARIANT_JSON: Final[Path] = SRC / "config" / "variants.json"

# Compiler
LLVM: Final[str] = "1"
LLVM_IAS: Final[str] = "1"
LTO_CLANG_THIN: Final[str] = "y"
LTO_CLANG_FULL: Final[str] = "n"

CLANG_TRIPLE: Final[str] = "aarch64-linux-gnu-"
CROSS_COMPILE: Final[str] = "aarch64-linux-gnu-"
