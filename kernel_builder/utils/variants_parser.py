import json
import os
from pathlib import Path
from typing import Any


class VariantsParser:
    def __init__(self, variant_json: Path) -> None:
        self.variants: list[dict[str, Any]] = json.loads(variant_json.read_text())

    def _check_env(self, key: str, val: bool) -> bool:
        return os.getenv(key, "").lower() == str(val).lower()

    def _detect_variant(self) -> dict[str, bool] | None:
        for entry in self.variants:
            env_map = entry.get("env", {})
            if all(self._check_env(key, val) for key, val in env_map.items()):
                return entry
        return None

    def name(self) -> str:
        v: dict[str, Any] | None = self._detect_variant()
        if not v:
            raise RuntimeError("No matching variant for current environment")
        return v["variant"]

    def config(self) -> dict[str, bool]:
        v: dict[str, Any] | None = self._detect_variant()
        if not v:
            raise RuntimeError("No matching variant for current environment")
        return v.get("config", {})
