"""Application entry point for the Towers of Hanoi solver.

Usage:
    python main.py [discs] [mode]

Arguments:
    discs: Number of discs to solve for (1–9). Defaults to 4.
    mode:  Visualisation mode. One of:
               ascii   — animated ASCII terminal output (default)
               log     — ASCII output + moves saved to a text file
               silent  — no output, useful for benchmarking or tests

Environment variables (see .env.example):
    LOG_LEVEL: Console log level (DEBUG, INFO, WARNING, ERROR). Defaults to INFO.
    LOG_FILE:  Path for the log file. Defaults to hanoi.log.
    LANG:      Language for user-facing output (ca, en). Defaults to en.
"""

import infrastructure.logging_config  # noqa: F401 — configures logging on import
import infrastructure.i18n             # noqa: F401 — installs _() on import

import logging
import sys

from adapters.ascii import ASCIIVisualiser
from adapters.altres import SilentVisualiser, LogFileVisualiser, CompositeVisualiser
from domain.engine import HanoiEngine

log = logging.getLogger(__name__)


def main() -> None:
    """Parses arguments, builds the engine with the chosen adapter, and runs it."""
    n    = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    n    = max(1, min(n, 9))
    mode = sys.argv[2] if len(sys.argv) > 2 else "ascii"

    log.info("Starting application — discs: %d, mode: %s", n, mode)

    if mode == "silent":
        visualiser = SilentVisualiser()
    elif mode == "log":
        visualiser = CompositeVisualiser(
            ASCIIVisualiser(pause=0.6),
            LogFileVisualiser("hanoi_log.txt"),
        )
    else:
        visualiser = ASCIIVisualiser(pause=0.8)

    engine = HanoiEngine(n=n, visualiser=visualiser)
    engine.solve()


if __name__ == "__main__":
    main()
