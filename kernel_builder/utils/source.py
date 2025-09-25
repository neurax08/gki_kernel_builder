import re
from dataclasses import dataclass, field
from pathlib import Path
from re import Pattern
from shutil import rmtree
from urllib.parse import ParseResult, urlparse, urlunparse

import requests
from sh import git

from kernel_builder.config.manifest import SOURCES
from kernel_builder.utils.log import log


@dataclass(slots=True)
class SourceManager:
    sources: list[dict[str, str]] = field(default_factory=lambda: SOURCES.copy())

    @staticmethod
    def git_simplifier(url: str) -> str:
        with requests.get(url, allow_redirects=True) as resp:
            parsed: ParseResult = urlparse(resp.url)
            cleaned: str = parsed.path.strip("/").removesuffix(".git")
            return f"{parsed.netloc}:{cleaned}"

    @staticmethod
    def is_simplified(url: str) -> bool:
        valid_char: Pattern[str] = re.compile(r"^[A-Za-z0-9_.-]+$")
        try:
            host, rest = url.split(":", 1)
            owner, repo = rest.split("/", 1)
        except ValueError:
            return False

        for part in (host, owner, repo):
            if not part or not valid_char.fullmatch(part):
                return False

        return True

    @staticmethod
    def restore_simplified(simplified: str) -> str:
        if simplified.startswith(("http://", "https://")):
            url = simplified
        else:
            host, repo = simplified.split(":", 1)
            url = urlunparse(("https", host, "/" + repo, "", "", ""))
        return url

    def _strip_git_dotfiles(self, parent: Path) -> None:
        GIT_DOTFILES = [
            parent / ".git",
            parent / ".github",
        ]

        for path in GIT_DOTFILES:
            if not path.exists():
                continue
            elif path.is_dir():
                rmtree(path)
            else:
                path.unlink(missing_ok=True)

    def clone_repo(
        self, repo: dict[str, str], *, depth: int = 1, args: list[str] | None = None
    ) -> None:
        """
        Clone a git repository.

        :param repo: Dictionary with keys 'url', 'branch', and 'to'.
        :param depth: Depth of the clone, default is 1.
        :param args: Additional arguments to pass to git clone.
        :return: None
        """
        git.clone(
            "--depth",
            str(depth),
            "--single-branch",
            "--no-tags",
            "-b",
            repo["branch"],
            *(args or []),
            self.restore_simplified(repo["url"]),
            repo["to"],
        )
        # Strip git dotfiles
        self._strip_git_dotfiles(Path(repo["to"]))

    def clone_sources(self) -> None:
        """
        Clone all sources in SOURCES.

        :return: None
        """
        for source in self.sources:
            log(
                f"Cloning {source['url']} into {source['to']} on branch {source['branch']}"
            )
            self.clone_repo(source)


if __name__ == "__main__":
    raise SystemExit("This file is meant to be imported, not executed.")
