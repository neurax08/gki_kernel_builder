import os
from typing import Any

import requests
from requests.models import Response


class GithubAPI:
    def _fetch_raw(self, api: str) -> dict[Any, Any]:
        resp: Response = requests.get(
            api, headers={"Authorization": f"token {os.getenv('GH_TOKEN')}"}, timeout=10
        )
        resp.raise_for_status()
        return resp.json()

    def fetch_latest_download_url(self, repo_api: str, extension: str) -> str:
        data: dict[Any, Any] = self._fetch_raw(repo_api)
        url: str | None = next(
            (
                asset["browser_download_url"]
                for asset in data.get("assets", [])
                if asset.get("browser_download_url", "").endswith(extension)
            ),
            None,
        )
        if url is None:
            raise ValueError(f"No asset ending with {extension} found in {repo_api}")
        return url

    def fetch_latest_tag(self, repo_api: str) -> str:
        data: dict[Any, Any] = self._fetch_raw(repo_api)
        try:
            return data["tag_name"]
        except KeyError:
            raise ValueError(f"'tag_name' not found in response from {repo_api}")
