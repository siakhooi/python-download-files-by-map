import io
import json
import logging
import os
import sys

import pytest

from download_files_by_map.core import (
    _collect_files,
    _download,
    _load_map_data,
    _map_to_file_list,
)


def _shutdown_after_first_item():
    first = True

    def shutdown():
        nonlocal first
        if first:
            first = False
            return False
        return True

    return shutdown


def test_collect_files_nested_folder():
    data = {
        "type": "folder",
        "local_filename": "sample",
        "children": [
            {
                "type": "folder",
                "local_filename": "zip_files",
                "children": [
                    {
                        "type": "file",
                        "local_filename": "a.txt",
                        "remote_url": "http://example.com/a",
                    },
                ],
            },
            {
                "type": "file",
                "local_filename": "b.txt",
                "remote_url": "http://example.com/b",
            },
        ],
    }
    out = []
    _collect_files(data, "", out)
    paths_urls = {(d["path"], d["url"]) for d in out}
    assert paths_urls == {
        (os.path.join("sample", "zip_files", "a.txt"), "http://example.com/a"),
        (os.path.join("sample", "b.txt"), "http://example.com/b"),
    }


def test_map_to_file_list_dict_root():
    data = {
        "type": "file",
        "local_filename": "x.txt",
        "remote_url": "http://example.com/x",
    }
    out = _map_to_file_list(data)
    assert out == [{"path": "x.txt", "url": "http://example.com/x"}]


def test_map_to_file_list_list_root():
    data = [
        {
            "type": "file",
            "local_filename": "a.txt",
            "remote_url": "http://example.com/a",
        },
        {
            "type": "file",
            "local_filename": "b.txt",
            "remote_url": "http://example.com/b",
        },
    ]
    out = _map_to_file_list(data)
    assert len(out) == 2


def test_map_to_file_list_non_container_returns_empty():
    assert _map_to_file_list(42) == []
    assert _map_to_file_list(None) == []


def test_load_map_data_from_file(tmp_path):
    path = tmp_path / "map.json"
    payload = {
        "type": "file",
        "local_filename": "f.txt",
        "remote_url": "http://x",
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert _load_map_data(str(path)) == payload


def test_load_map_data_from_stdin(monkeypatch):
    monkeypatch.setattr(sys, "stdin", io.StringIO('{"k": "v"}'))
    assert _load_map_data(None) == {"k": "v"}


def test_load_map_data_missing_file_exits(tmp_path):
    missing = str(tmp_path / "nope.json")
    with pytest.raises(SystemExit) as exc:
        _load_map_data(missing)
    assert exc.value.code == 2


def test_download_writes_streamed_body(responses, tmp_path):
    url = "http://example.com/file.txt"
    responses.add(responses.GET, url, body="hello-bytes")
    target = tmp_path / "out.txt"
    _download(
        [{"path": str(target), "url": url}],
        lambda: False,
        True,
    )
    assert target.read_text() == "hello-bytes"


def test_download_shutdown_skips_remaining(responses, tmp_path, caplog):
    caplog.set_level(logging.WARNING)
    url1 = "http://example.com/one.txt"
    url2 = "http://example.com/two.txt"
    responses.add(responses.GET, url1, body="first")
    # Only url1 is fetched; second item is skipped (do not register url2 or
    # responses teardown asserts unused mocks).
    p1 = tmp_path / "one.txt"
    p2 = tmp_path / "two.txt"
    _download(
        [
            {"path": str(p1), "url": url1},
            {"path": str(p2), "url": url2},
        ],
        _shutdown_after_first_item(),
        True,
    )
    assert p1.read_text() == "first"
    assert not p2.exists()
    assert "skipping remaining downloads" in caplog.text.lower()


def test_download_continues_after_http_error(responses, tmp_path, caplog):
    caplog.set_level(logging.ERROR)
    bad = "http://example.com/bad.txt"
    good = "http://example.com/good.txt"
    responses.add(responses.GET, bad, status=404)
    responses.add(responses.GET, good, body="ok")
    pb = tmp_path / "bad.txt"
    pg = tmp_path / "good.txt"
    _download(
        [
            {"path": str(pb), "url": bad},
            {"path": str(pg), "url": good},
        ],
        lambda: False,
        True,
    )
    assert pg.read_text() == "ok"
    assert any("Failed to download" in r.message for r in caplog.records)
