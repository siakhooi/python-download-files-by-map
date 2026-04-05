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
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging (overrides --log-level)",
    )
    parser.add_argument(
        "--log-level",
        default=None,
        help=(
            "Set log level (DEBUG, INFO, WARNING, ERROR, CRITICAL). "
            "Default: INFO."
        ),
    )
    return parser.parse_args()


def mkdir_parent_directories(path):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
