from pathlib import Path

from sh import Command

from kernel_builder.config.config import LTO
from kernel_builder.constants import VARIANT_JSON, WORKSPACE
from kernel_builder.utils.fs import FileSystem
from kernel_builder.utils.log import log
from kernel_builder.utils.variants_parser import VariantsParser


def _config(
    conf: str, mode: bool, target: Path = WORKSPACE / "out" / ".config"
) -> None:
    config: Command = Command(str(WORKSPACE / "scripts" / "config"))
    config("--file", str(target), "--enable" if mode else "--disable", conf)
    simplified_target: Path = FileSystem.relative_to(WORKSPACE, target)
    log(
        f"{'Enabling' if mode else 'Disabling'} config: {conf} (file={simplified_target})"
    )

def _lto() -> None:
    _config("CONFIG_LTO_CLANG", True) # Enable LTO

    if LTO == "thin":
        _config("CONFIG_LTO_CLANG_THIN", True)
        _config("CONFIG_LTO_CLANG_FULL", False)
    else:
        _config("CONFIG_LTO_CLANG_THIN", False)
        _config("CONFIG_LTO_CLANG_FULL", True)

def configurator() -> None:
    parser: VariantsParser = VariantsParser(VARIANT_JSON)

    for k, v in parser.config().items():
        _config(k, v)

    # Clang LTO setup
    _lto()
