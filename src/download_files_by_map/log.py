import logging
import sys


def setup_logging(log_level: str = "INFO", debug: bool = False):
    level = log_level.upper()
    if debug:
        level = "DEBUG"
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(message)s",
        stream=sys.stderr,
    )
    logging.debug(f"Logging initialized at level: {level}")
