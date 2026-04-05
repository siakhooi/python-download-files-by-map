import sys
import json
import signal
import requests
import urllib3
import os
import logging
from download_files_by_map.util import (
    parse_arguments,
    mkdir_parent_directories,
)
from download_files_by_map.log import setup_logging

CHUNK_SIZE = 8192


def _download(file_list, shutdown_requested, verify_ssl):
    for file in file_list:
        if shutdown_requested():
            logging.warning(
                "Shutdown requested, skipping remaining downloads."
            )
            break
        path = file["path"]
        url = file["url"]
        logging.info(f"Downloading {url} to {path}")
        mkdir_parent_directories(path)

        try:
            with (
                open(path, "+bw") as f,
                requests.get(url, stream=True, verify=verify_ssl) as response,
            ):
                response.raise_for_status()
                for c in response.iter_content(chunk_size=CHUNK_SIZE):
                    f.write(c)
            logging.info(f"Downloaded {url} to {path}")
        except Exception as e:
            logging.error(f"Failed to download {url} to {path}: {e}")


def _collect_files(data, parent_directory, file_list):
    path = os.path.join(parent_directory, data["local_filename"])
    if data["type"] == "folder":
        logging.debug(f"Entering folder: {path}")
        for child in data["children"]:
            _collect_files(child, path, file_list)
    else:
        logging.debug(f"Queueing file: {path} from {data['remote_url']}")
        file_list.append({"path": path, "url": data["remote_url"]})


def download_files_by_map():
    _shutdown_requested = False

    args = parse_arguments()
    setup_logging(
        log_level=args.log_level or "INFO",
        debug=args.debug,
    )
    logging.debug(f"Parsed arguments: {args}")
    verify_ssl = args.ssl_verify

    if not verify_ssl:
        urllib3.disable_warnings()
        logging.warning("SSL verification is disabled!")

    def handle_shutdown_signal(signum, frame):
        nonlocal _shutdown_requested
        signal_name = signal.Signals(signum).name
        logging.warning(
            f"{signal_name} received, finishing current download..."
        )
        _shutdown_requested = True

    signal.signal(signal.SIGINT, handle_shutdown_signal)
    signal.signal(signal.SIGTERM, handle_shutdown_signal)

    filename = args.map_file

    if filename:
        if not os.path.exists(filename):
            logging.error(f"{filename} does not exist.")
            print(f"{filename} does not exist.", file=sys.stderr)
            sys.exit(2)
        with open(filename, "r") as file:
            data = json.load(file)
        logging.info(f"Loaded map from {filename}")
    else:
        data = json.load(sys.stdin)
        logging.info("Loaded map from stdin")

    file_list = []
    if isinstance(data, list):
        for item in data:
            _collect_files(item, "", file_list)
    elif isinstance(data, dict):
        _collect_files(data, "", file_list)

    logging.info(f"Total files to download: {len(file_list)}")
    _download(
        file_list,
        lambda: _shutdown_requested,
        verify_ssl,
    )
