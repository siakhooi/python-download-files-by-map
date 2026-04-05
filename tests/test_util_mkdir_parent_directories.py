from download_files_by_map.util import mkdir_parent_directories


def test_creates_parent_directories(tmp_path):
    file_path = tmp_path / "a" / "b" / "c.txt"
    # Should not exist before
    assert not (tmp_path / "a" / "b").exists()
    mkdir_parent_directories(str(file_path))
    assert (tmp_path / "a" / "b").is_dir()


def test_does_nothing_if_parent_exists(tmp_path):
    parent = tmp_path / "foo"
    parent.mkdir()
    file_path = parent / "bar.txt"
    mkdir_parent_directories(str(file_path))
    assert parent.is_dir()


def test_does_nothing_if_no_parent(tmp_path):
    file_path = tmp_path / "file.txt"
    # Parent is tmp_path, which always exists
    mkdir_parent_directories(str(file_path))
    assert tmp_path.is_dir()
