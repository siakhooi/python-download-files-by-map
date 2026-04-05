from download_files_by_map.util import parse_arguments

import pytest


def test_parse_arguments_no_value(monkeypatch):
    monkeypatch.setattr("sys.argv", ["download_files_by_map.py"])
    args = parse_arguments()
    assert args.map_file is None
    assert args.ssl_verify is True


def test_parse_arguments(monkeypatch):
    monkeypatch.setattr("sys.argv", ["download_files_by_map.py", "a.json"])
    args = parse_arguments()
    assert args.map_file == "a.json"
    assert args.ssl_verify is True


def test_parse_arguments_many_values(monkeypatch):
    argv = ["download_files_by_map.py", "a.json", "b.json"]
    monkeypatch.setattr("sys.argv", argv)
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        parse_arguments()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2


def test_parse_arguments_no_ssl_verify(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        ["download_files_by_map.py", "--no-ssl-verify", "a.json"],
    )
    args = parse_arguments()
    assert args.map_file == "a.json"
    assert args.ssl_verify is False


def test_parse_arguments_ssl_verify(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        ["download_files_by_map.py", "--ssl-verify", "a.json"],
    )
    args = parse_arguments()
    assert args.map_file == "a.json"
    assert args.ssl_verify is True
