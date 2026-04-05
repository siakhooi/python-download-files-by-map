from __future__ import annotations

import sys
import json
import signal
import requests
import urllib3
import os
import logging
from typing import Any, Callable, Literal, TypedDict, Union, cast

from download_files_by_map.util import (
    parse_arguments,
    mkdir_parent_directories,
)
from download_files_by_map.log import setup_logging

CHUNK_SIZE = 8192


class DownloadItem(TypedDict):
    path: str
    url: str


class MapFileNode(TypedDict):
    type: Literal["file"]
    local_filename: str
    remote_url: str


class MapFolderNode(TypedDict):
    type: Literal["folder"]
    local_filename: str
    children: list[Union[MapFileNode, MapFolderNode]]


MapNode = Union[MapFileNode, MapFolderNode]


def _download(
    file_list: list[DownloadItem],
    shutdown_requested: Callable[[], bool],
    verify_ssl: bool,
) -> None:
    for item in file_list:
        if shutdown_requested():
            logging.warning(
                "Shutdown requested, skipping remaining downloads."
            )
            break
        path = item["path"]
        url = item["url"]
        logging.info(f"Downloading {url} to {path}")
        mkdir_parent_directories(path)

        try:
            with (
                open(path, "wb") as f,
                requests.get(url, stream=True, verify=verify_ssl) as response,
            ):
                response.raise_for_status()
                for c in response.iter_content(chunk_size=CHUNK_SIZE):
                    f.write(c)
            logging.info(f"Downloaded {url} to {path}")
        # Skip this URL and continue; do not abort the whole batch.
        except (OSError, requests.RequestException) as e:
            logging.error(f"Failed to download {url} to {path}: {e}")


def _collect_files(
    data: MapNode,
    parent_directory: str,
    file_list: list[DownloadItem],
) -> None:
    path = os.path.join(parent_directory, data["local_filename"])
    if data["type"] == "folder":
        logging.debug(f"Entering folder: {path}")
        for child in data["children"]:
            _collect_files(child, path, file_list)
    else:
        logging.debug(f"Queueing file: {path} from {data['remote_url']}")
        file_list.append({"path": path, "url": data["remote_url"]})


def _load_map_data(filename: str | None) -> Any:
    """Load JSON map from a file path or stdin.
    Exits with code 2 if the file is missing.
    """
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
    return data


def _map_to_file_list(data: object) -> list[DownloadItem]:
    if isinstance(data, list):
        roots = cast(list[MapNode], data)
    elif isinstance(data, dict):
        roots = [cast(MapNode, data)]
    else:
        roots = []

    file_list: list[DownloadItem] = []
    for item in roots:
        _collect_files(item, "", file_list)
    return file_list


def download_files_by_map() -> None:
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

    def handle_shutdown_signal(signum, _frame):
        nonlocal _shutdown_requested
        signal_name = signal.Signals(signum).name
        logging.warning(
            f"{signal_name} received, finishing current download..."
        )
        _shutdown_requested = True

    signal.signal(signal.SIGINT, handle_shutdown_signal)
    signal.signal(signal.SIGTERM, handle_shutdown_signal)

    data = _load_map_data(args.map_file)
    file_list = _map_to_file_list(data)

    logging.info(f"Total files to download: {len(file_list)}")
    _download(
        file_list,
        lambda: _shutdown_requested,
        verify_ssl,
    )
