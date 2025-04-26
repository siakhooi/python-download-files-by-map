from download_files_by_map.cli import run
import pytest


def test_cli_file_not_found(monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv",
        ["download_files_by_map.py", "i-am-blahblah.json"],
    )
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2
    expected_output = "i-am-blahblah.json is not exist.\n"
    captured = capsys.readouterr()
    assert captured.err == expected_output


def test_cli_file_wrong_arguments(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["download_files_by_map.py", "a", "b"])
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    expected_output = "Usage: download_files_by_maps [map_json_file]\n"
    captured = capsys.readouterr()
    assert captured.err == expected_output
