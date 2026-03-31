"""ASCII terminal adapter for tower visualisation."""

__all__ = ["ASCIIVisualiser"]

import builtins
import logging
import os
import time

from ports.visualitzador import TowerVisualiser

log = logging.getLogger(__name__)


def _t(text: str) -> str:
    """Looks up the current translation function at call time, not import time.

    This avoids capturing _ at module import, which would happen before
    infrastructure/i18n.py has had a chance to install the real translator
    as a built-in.

    Args:
        text: The string to translate.

    Returns:
        Translated string, or the original if no translator is installed.
    """
    return builtins.__dict__.get("_", lambda x: x)(text)

_TOWER_NAMES = ["A", "B", "C"]


class ASCIIVisualiser(TowerVisualiser):
    """Renders the towers as ASCII art in the terminal with ANSI colours.

    Clears the screen before each frame and pauses between moves
    to create a simple animation effect.
    """

    _DISC_COLOURS = [
        "\033[95m", "\033[94m", "\033[96m", "\033[92m",
        "\033[93m", "\033[91m", "\033[35m", "\033[33m", "\033[36m",
    ]
    _RESET  = "\033[0m"
    _BOLD   = "\033[1m"
    _DIM    = "\033[2m"
    _CYAN   = "\033[96m"
    _YELLOW = "\033[93m"
    _GREEN  = "\033[92m"

    _MAX_DISC_WIDTH: int = 17
    _MIN_DISC_WIDTH: int = 3
    _COL_WIDTH: int      = 25
    _COL_SEP: str        = "   "

    __pause: float
    __colours: bool
    __n: int

    def __init__(self, pause: float = 0.8, colours: bool = True) -> None:
        """Initialises the ASCII visualiser.

        Args:
            pause: Seconds to wait between moves.
            colours: Whether to use ANSI colour codes. Set to False if the
                     terminal does not support them.
        """
        self.__pause   = pause
        self.__colours = colours
        self.__n       = 0

    def on_start(self, n: int, towers: list[list[int]]) -> None:
        """Renders the initial board before any move is made.

        Args:
            n: Total number of discs.
            towers: Initial board state.
        """
        self.__n = n
        self.__render(towers, step=0, total=2 ** n - 1)
        time.sleep(self.__pause)

    def on_move(self, step: int, disc: int, origin: int, destination: int, towers: list[list[int]]) -> None:
        """Renders the board after a move.

        Args:
            step: Current move number.
            disc: Size of the disc that was moved.
            origin: Source tower index.
            destination: Destination tower index.
            towers: Updated board state.
        """
        self.__render(
            towers,
            step=step,
            total=2 ** self.__n - 1,
            last_move=(disc, _TOWER_NAMES[origin], _TOWER_NAMES[destination]),
        )
        time.sleep(self.__pause)

    def on_finish(self, total_steps: int, towers: list[list[int]]) -> None:
        """Prints the completion message.

        Args:
            total_steps: Total number of moves performed.
            towers: Final board state (unused in this adapter).
        """
        print(self.__c(
            _t("  Solved in {n} moves!\n").format(n=total_steps),
            self._BOLD + self._GREEN,
        ))

    # ── Private helpers ───────────────────────────────────────────────────────

    def __c(self, text: str, code: str) -> str:
        """Wraps text in an ANSI colour code if colours are enabled.

        Args:
            text: The text to colour.
            code: ANSI escape code to apply.

        Returns:
            Coloured string if colours are enabled, plain string otherwise.
        """
        return f"{code}{text}{self._RESET}" if self.__colours else text

    def __disc_width(self, disc: int) -> int:
        """Computes the display width for a disc, always odd.

        Args:
            disc: Disc size value.

        Returns:
            Odd integer width proportional to the disc size.
        """
        span = self._MAX_DISC_WIDTH - self._MIN_DISC_WIDTH
        w = self._MIN_DISC_WIDTH + round(span * (disc - 1) / max(self.__n - 1, 1))
        return w if w % 2 == 1 else w + 1

    def __disc_row(self, disc: int) -> str:
        """Builds the ASCII string for a single disc row.

        Args:
            disc: Disc size value.

        Returns:
            Centred, coloured disc string padded to column width.
        """
        w   = self.__disc_width(disc)
        txt = f"({'=' * (w - 2)})"
        pad = (self._COL_WIDTH - w) // 2
        return " " * pad + self.__c(txt, self._DISC_COLOURS[(disc - 1) % len(self._DISC_COLOURS)]) + " " * pad

    def __empty_row(self) -> str:
        """Builds the ASCII string for an empty tower slot (pole only).

        Returns:
            String with a vertical bar centred in the column width.
        """
        mid = self._COL_WIDTH // 2
        return " " * mid + self.__c("|", self._DIM) + " " * (self._COL_WIDTH - mid - 1)

    def __render(
        self,
        towers: list[list[int]],
        step: int,
        total: int,
        last_move: tuple[int, str, str] | None = None,
    ) -> None:
        """Clears the screen and renders the full board.

        Args:
            towers: Current board state.
            step: Current step number to display in the header.
            total: Total number of moves for the header.
            last_move: Tuple of (disc, origin_name, destination_name) for the
                       last move annotation, or None for the initial render.
        """
        os.system("cls" if os.name == "nt" else "clear")
        print(self.__c(_t("  Towers of Hanoi — {n} discs").format(n=self.__n), self._BOLD + self._CYAN))
        print(self.__c(_t("  Step {step}/{total}").format(step=step, total=total), self._DIM))
        if last_move:
            disc, orig, dest = last_move
            print(self.__c(_t("  >  Disc {d}: {o} -> {t}").format(d=disc, o=orig, t=dest), self._YELLOW))
        else:
            print()
        print()

        for row in range(self.__n - 1, -1, -1):
            parts = []
            for t in range(3):
                if row < len(towers[t]):
                    parts.append(self.__disc_row(towers[t][row]))
                else:
                    parts.append(self.__empty_row())
            print("  " + self._COL_SEP.join(parts))

        ground = self.__c("-" * self._COL_WIDTH, self._DIM)
        print("  " + self._COL_SEP.join([ground, ground, ground]))

        for line in [["/ --- \\", "/ --- \\", "/ --- \\"],
                     ["[  A  ]", "[  B  ]", "[  C  ]"],
                     ["\\ --- /", "\\ --- /", "\\ --- /"]]:
            row_parts = []
            for label in line:
                pad = (self._COL_WIDTH - len(label)) // 2
                row_parts.append(" " * pad + label + " " * (self._COL_WIDTH - pad - len(label)))
            print("  " + self._COL_SEP.join(row_parts))
        print()
