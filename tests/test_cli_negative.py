from download_files_by_map.cli import run
import pytest


def test_cli_file_not_found(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        ["download_files_by_map.py", "i-am-blahblah.json"],
    )
    error = "[Errno 2] No such file or directory: 'i-am-blahblah.json'"  # noqa: E501
    with pytest.raises(FileNotFoundError) as e:
        run()
    assert str(e.value) == error
