from types import ModuleType
import importlib
import pytest
import logging


@pytest.fixture
def log() -> ModuleType:
    return importlib.import_module("kernel_builder.utils.log")


def test_log_info(caplog: pytest.LogCaptureFixture, log):
    with caplog.at_level(logging.INFO):
        log.log("hello world")
    assert "hello world" in caplog.text
