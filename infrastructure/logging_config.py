"""Centralised logging configuration.

Importing this module is sufficient to configure the entire logging system.
All loggers in the project (and in third-party libraries) propagate their
messages up to the root logger, which is the only one with handlers attached.

Environment variables (loaded from .env if python-dotenv is installed):
    LOG_LEVEL: Minimum level for the console handler. Defaults to INFO.
    LOG_FILE:  Path for the file handler. Defaults to hanoi.log.
               Set to an empty string to disable file logging.
"""

import logging
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def _configure() -> None:
    """Reads environment variables and attaches handlers to the root logger.

    Called automatically when this module is imported. Safe to import
    multiple times: handlers are only added if none exist yet on the root logger.
    """
    root = logging.getLogger()

    if root.handlers:
        return

    root.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)-8s] %(name)s — %(message)s",
        datefmt="%H:%M:%S",
    )

    level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    level     = getattr(logging, level_str, logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)

    log_file = os.getenv("LOG_FILE", "hanoi.log")
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)

    logging.getLogger("urllib3").setLevel(logging.WARNING)


_configure()
