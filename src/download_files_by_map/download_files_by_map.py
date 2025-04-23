import sys
import json
import requests
import urllib3
import os

urllib3.disable_warnings()

file_list = []


def mkdir_p(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def download():
    for file in file_list:
        path = file["path"]
        url = file["url"]
        print(f"{path}")
        mkdir_p(path)

        with (
            open(path, "+bw") as f,
            requests.get(url, stream=True, verify=False) as response,
        ):
            for c in response.iter_content():
                f.write(c)


def process_file(data, parent_directory):
    local_filename = data["local_filename"]
    remote_url = data["remote_url"]
    filepath = os.path.join(parent_directory, local_filename)
    file_list.append({"path": filepath, "url": remote_url})


def process_folder(data, parent_directory):
    local_filename = data["local_filename"]
    new_parent = os.path.join(parent_directory, local_filename)
    for child in data["children"]:
        process(child, new_parent)


def process(data, parent_directory):
    if data["type"] == "folder":
        process_folder(data, parent_directory)
    else:
        process_file(data, parent_directory)


def download_files_by_map():
    if len(sys.argv) == 2:
        file = open(sys.argv[1], "r")
    else:
        file = sys.stdin

    data = json.load(file)
    if isinstance(data, list):
        for item in data:
            process(item, "")
    elif isinstance(data, dict):
        process(data, "")

    download()
    file.close()
