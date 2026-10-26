import logging

import colorlog


def setup_logging(level: int = logging.INFO) -> None:
    """Send all log records to the terminal, colored by level. Call once at startup."""
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s [%(levelname)s]%(reset)s %(blue)s%(name)s%(reset)s: %(message)s",
        datefmt="%H:%M:%S",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    ))
    logging.basicConfig(level=level, handlers=[handler])
    # Our own package logs in detail (e.g. every agent step); libraries stay at `level`.
    logging.getLogger("discord_agent").setLevel(logging.DEBUG)
