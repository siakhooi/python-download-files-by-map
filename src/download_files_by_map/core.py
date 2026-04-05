import sys
import json
import signal
import requests
import urllib3
import os
from download_files_by_map.util import get_filename_from_arguments
from download_files_by_map.util import mkdir_parent_directories

urllib3.disable_warnings()

CHUNK_SIZE = 8192


def _download(file_list, shutdown_requested, verify_ssl):
    for file in file_list:
        if shutdown_requested():
            print("Shutdown requested, skipping remaining downloads.")
            break
        path = file["path"]
        url = file["url"]
        print(f"{path}")
        mkdir_parent_directories(path)

        with (
            open(path, "+bw") as f,
            requests.get(url, stream=True, verify=verify_ssl) as response,
        ):
            response.raise_for_status()
            for c in response.iter_content(chunk_size=CHUNK_SIZE):
                f.write(c)


def _collect_files(data, parent_directory, file_list):
    path = os.path.join(parent_directory, data["local_filename"])
    if data["type"] == "folder":
        for child in data["children"]:
            _collect_files(child, path, file_list)
    else:
        file_list.append({"path": path, "url": data["remote_url"]})


def download_files_by_map(verify_ssl=False):
    _shutdown_requested = False

    def handle_shutdown_signal(signum, frame):
        nonlocal _shutdown_requested
        signal_name = signal.Signals(signum).name
        print(f"\n{signal_name} received, finishing current download...")
        _shutdown_requested = True

    signal.signal(signal.SIGINT, handle_shutdown_signal)
    signal.signal(signal.SIGTERM, handle_shutdown_signal)

    filename = get_filename_from_arguments()

    if filename:
        if not os.path.exists(filename):
            print(f"{filename} does not exist.", file=sys.stderr)
            sys.exit(2)
        with open(filename, "r") as file:
            data = json.load(file)
    else:
        data = json.load(sys.stdin)

    file_list = []
    if isinstance(data, list):
        for item in data:
            _collect_files(item, "", file_list)
    elif isinstance(data, dict):
        _collect_files(data, "", file_list)

    _download(
        file_list,
        lambda: _shutdown_requested,
        verify_ssl,
    )
