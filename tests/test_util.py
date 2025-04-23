from download_files_by_map.util import get_arguments


def test_get_arguments():
    assert get_arguments(['hello.py', 'arg1', 'arg2']) == ['arg1', 'arg2']
