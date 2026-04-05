import argparse
import os


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Download files using a JSON tree map."
    )
    parser.add_argument(
        "map_file",
        nargs="?",
        default=None,
        help="Path to the JSON map file. Reads from stdin if omitted.",
    )
    parser.add_argument(
        "--ssl-verify",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Enable or disable SSL certificate verification"
        " (default: enabled).",
    )
    return parser.parse_args()


def mkdir_parent_directories(path):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
