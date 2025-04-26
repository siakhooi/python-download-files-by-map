import sys
import os


def get_filename_from_arguments():
    if len(sys.argv) == 2:
        return sys.argv[1]
    elif len(sys.argv) == 1:
        return None
    else:
        print("Usage: download_files_by_maps [map_json_file]", file=sys.stderr)
        sys.exit(1)


def mkdir_parent_directories(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
