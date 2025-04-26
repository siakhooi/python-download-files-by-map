from download_files_by_map.cli import run
import os
import io


def setup_responses(responses):
    url = "http://download-server-123/file1.txt"
    responses.add(responses.GET, url, body="file1")
    url = "http://download-server-123/file2.txt"
    responses.add(responses.GET, url, body="file2")
    url = "http://download-server-123/file3.txt"
    responses.add(responses.GET, url, body="file3")


def test_cli_map_objects(monkeypatch, responses, tmp_path):
    original_cwd = os.getcwd()

    monkeypatch.setattr(
        "sys.argv",
        [
            "download_files_by_map.py",
            os.path.join(original_cwd, "tests/test-data/map1.json"),
        ],
    )

    os.chdir(tmp_path)

    setup_responses(responses)

    run()

    file = open("sample/zip_files/file1.txt")
    assert file.read() == "file1"
    file = open("sample/zip_files/file2.txt")
    assert file.read() == "file2"
    file = open("sample/file3.txt")
    assert file.read() == "file3"

    os.chdir(original_cwd)


def test_cli_map_array(monkeypatch, responses, tmp_path):
    original_cwd = os.getcwd()
    monkeypatch.setattr(
        "sys.argv",
        [
            "download_files_by_map.py",
            os.path.join(original_cwd, "tests/test-data/map2.json"),
        ],
    )
    os.chdir(tmp_path)

    setup_responses(responses)

    run()

    file = open("sample/zip_files/file1.txt")
    assert file.read() == "file1"
    file = open("sample/file3.txt")
    assert file.read() == "file3"
    file = open("file2.txt")
    assert file.read() == "file2"

    os.chdir(original_cwd)


def test_cli_map_stdin(monkeypatch, responses, tmp_path):
    original_cwd = os.getcwd()
    map_file = os.path.join(original_cwd, "tests/test-data/map1.json")
    with open(map_file, "r") as file:
        file_content = file.read()
    data = io.StringIO(file_content)
    monkeypatch.setattr("sys.stdin", data)

    monkeypatch.setattr(
        "sys.argv",
        ["download_files_by_map.py"],
    )

    os.chdir(tmp_path)

    setup_responses(responses)

    run()

    file = open("sample/zip_files/file1.txt")
    assert file.read() == "file1"
    file = open("sample/zip_files/file2.txt")
    assert file.read() == "file2"
    file = open("sample/file3.txt")
    assert file.read() == "file3"

    os.chdir(original_cwd)
