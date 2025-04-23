import sys


def get_filename_from_arguments():
    if len(sys.argv) == 2:
        return sys.argv[1]
    elif len(sys.argv) == 1:
        return None
    else:
        print("Usage: download_files_by_maps [map_json_file]")
        sys.exit(1)
