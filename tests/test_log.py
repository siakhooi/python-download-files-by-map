import logging
import sys
import io
from download_files_by_map.log import setup_logging


def test_setup_logging_info_level(monkeypatch):
    stream = io.StringIO()
    monkeypatch.setattr(sys, "stderr", stream)
    # Remove all handlers to allow reconfiguration
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    setup_logging(log_level="INFO", debug=False)
    logging.info("info message")
    logging.debug("debug message")
    output = stream.getvalue()
    assert "info message" in output
    assert "debug message" not in output


def test_setup_logging_debug_level(monkeypatch):
    stream = io.StringIO()
    monkeypatch.setattr(sys, "stderr", stream)
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    setup_logging(log_level="WARNING", debug=True)
    logging.debug("debug message")
    logging.warning("warn message")
    output = stream.getvalue()
    assert "debug message" in output
    assert "warn message" in output


def test_setup_logging_log_level(monkeypatch):
    stream = io.StringIO()
    monkeypatch.setattr(sys, "stderr", stream)
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    setup_logging(log_level="ERROR", debug=False)
    logging.error("error message")
    logging.warning("warn message")
    output = stream.getvalue()
    assert "error message" in output
    assert "warn message" not in output
