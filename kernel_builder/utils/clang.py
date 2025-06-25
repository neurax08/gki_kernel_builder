from functools import partial
from typing import Final

from sh import grep, sed, sort, tail

from kernel_builder.utils.command import curl
from kernel_builder.utils.github import GithubAPI

# Toolchain Repo
SLIM_CLANG: Final[str] = "https://www.kernel.org/pub/tools/llvm/files/"
AOSP_CLANG: Final[str] = (
    "https://api.github.com/repos/bachnxuan/aosp_clang_mirror/releases/latest"
)
RV_CLANG: Final[str] = "https://api.github.com/repos/Rv-Project/RvClang/releases/latest"
YUKI_CLANG: Final[str] = (
    "https://api.github.com/repos/Klozz/Yuki_clang_releases/releases/latest"
)
LILIUM_CLANG: Final[str] = (
    "https://api.github.com/repos/liliumproject/clang/releases/latest"
)
TNF_CLANG: Final[str] = (
    "https://api.github.com/repos/topnotchfreaks/clang/releases/latest"
)
NEUTRON_CLANG: Final[str] = (
    "https://api.github.com/repos/Neutron-Toolchains/clang-build-catalogue/releases/latest"
)

fetch_clang: partial[str] = partial(
    GithubAPI().fetch_latest_download_url, extension=".tar.gz"
)


def fetch_clang_url(variants: str) -> str:
    match variants.upper():
        case "SLIM":
            return str(
                sed(
                    f"s|^|{SLIM_CLANG}|",
                    _in=tail(
                        "-n1",
                        _in=sort(
                            "-V",
                            _in=grep(
                                "-oP",
                                r"llvm-[\d.]+-x86_64\.tar\.xz",
                                _in=curl(SLIM_CLANG),
                            ),
                        ),
                    ),
                )
            ).strip()
        case "AOSP":
            return fetch_clang(AOSP_CLANG)
        case "RV":
            return fetch_clang(RV_CLANG)
        case "YUKI":
            return fetch_clang(YUKI_CLANG)
        case "LILIUM":
            return fetch_clang(LILIUM_CLANG)
        case "TNF":
            return fetch_clang(TNF_CLANG)
        case "NEUTRON":
            return GithubAPI().fetch_latest_download_url(NEUTRON_CLANG, "tar.zst")
        case _:
            raise Exception("Unknown clang variant")
