import json
from collections.abc import Generator
from typing import Any
from kernel_builder.utils.variants_parser import VariantsParser
import pytest
from pathlib import Path

dummy_data = [
    {
        "variant": "DUMMY",
        "env": {"KSU": "DUMMY", "SUSFS": False},
        "config": {"CONFIG_DUMMY": True},
    },
    {
        "variant": "DUMMY-2",
        "env": {"KSU": "DUMMY-2", "SUSFS": True},
        "config": {"CONFIG_DUMMY": False},
    },
]


@pytest.fixture
def variants_file(tmp_path: Path) -> Generator[Path, Any, None]:
    path: Path = tmp_path / "variants.json"
    path.write_text(json.dumps(dummy_data, indent=2))
    yield path
    path.unlink(missing_ok=True)


@pytest.mark.parametrize(
    "env, expected",
    [
        ({"KSU": "DUMMY", "SUSFS": "false"}, dummy_data[0]),
        ({"KSU": "DUMMY-2", "SUSFS": "true"}, dummy_data[1]),
    ],
)
def test_variant_matching(
    env, expected, variants_file, monkeypatch: pytest.MonkeyPatch
) -> None:
    for k, v in env.items():
        monkeypatch.setenv(k, v)
    parser: VariantsParser = VariantsParser(variants_file)
    assert parser.name() == expected["variant"]
    assert parser.config() == expected["config"]


def test_no_matching_variant(variants_file, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("KSU", "UNKNOWN")
    monkeypatch.setenv("SUSFS", "false")
    parser = VariantsParser(variants_file)
    with pytest.raises(RuntimeError):
        parser.name()
    with pytest.raises(RuntimeError):
        parser.config()
