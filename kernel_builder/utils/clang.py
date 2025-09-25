from functools import partial
from typing import Final

from kernel_builder.utils.github import GithubAPI

# Toolchain Repo
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

# Partials
fetch_clang_tgz: partial[str] = partial(
    GithubAPI().fetch_latest_download_url, extension=".tar.gz"
)
fetch_clang_tzst: partial[str] = partial(
    GithubAPI().fetch_latest_download_url, extension=".tar.zst"
)


def fetch_clang_url(variants: str) -> str:
    match variants.upper():
        case "AOSP":
            return fetch_clang_tgz(AOSP_CLANG)
        case "RV":
            return fetch_clang_tgz(RV_CLANG)
        case "YUKI":
            return fetch_clang_tgz(YUKI_CLANG)
        case "LILIUM":
            return fetch_clang_tgz(LILIUM_CLANG)
        case "TNF":
            return fetch_clang_tgz(TNF_CLANG)
        case "NEUTRON":
            return fetch_clang_tzst(NEUTRON_CLANG)
        case _:
            raise Exception("Unknown clang variant")
