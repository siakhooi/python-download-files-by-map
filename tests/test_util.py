from download_files_by_map.util import get_filename_from_arguments

import pytest


def test_get_filename_from_arguments_no_value(monkeypatch):
    monkeypatch.setattr("sys.argv", ["download_files_by_map.py"])
    assert get_filename_from_arguments() is None


def test_get_filename_from_arguments(monkeypatch):
    monkeypatch.setattr("sys.argv", ["download_files_by_map.py", "a.json"])
    assert get_filename_from_arguments() == "a.json"


def test_get_filename_from_arguments_many_values(monkeypatch):
    argv = ["download_files_by_map.py", "a.json", "b.json"]
    monkeypatch.setattr("sys.argv", argv)
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        get_filename_from_arguments()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
