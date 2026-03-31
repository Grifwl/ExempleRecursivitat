"""Secondary visualiser adapters: silent, file log, and composite."""

__all__ = ["SilentVisualiser", "LogFileVisualiser", "CompositeVisualiser"]

import logging

from ports.visualitzador import TowerVisualiser

log = logging.getLogger(__name__)


class SilentVisualiser(TowerVisualiser):
    """Adapter that produces no output.

    Records all moves internally so they can be inspected in tests
    or used for benchmarking pure domain performance.
    """

    __moves: list[dict]

    def __init__(self) -> None:
        """Initialises the silent visualiser with an empty move history."""
        self.__moves = []

    @property
    def moves(self) -> list[dict]:
        """All recorded moves as a list of dicts with keys:
        step, disc, origin, destination."""
        return list(self.__moves)

    def on_start(self, n: int, towers: list[list[int]]) -> None:
        """No-op. Required by the TowerVisualiser contract.

        Args:
            n: Total number of discs.
            towers: Initial board state.
        """

    def on_move(self, step: int, disc: int, origin: int, destination: int, towers: list[list[int]]) -> None:
        """Records the move without producing any output.

        Args:
            step: Current move number.
            disc: Size of the disc that was moved.
            origin: Source tower index.
            destination: Destination tower index.
            towers: Updated board state.
        """
        self.__moves.append({
            "step": step,
            "disc": disc,
            "origin": origin,
            "destination": destination,
        })

    def on_finish(self, total_steps: int, towers: list[list[int]]) -> None:
        """No-op. Required by the TowerVisualiser contract.

        Args:
            total_steps: Total number of moves performed.
            towers: Final board state.
        """


class LogFileVisualiser(TowerVisualiser):
    """Adapter that writes each move to a plain text file.

    Can be combined with other adapters using CompositeVisualiser.
    """

    __file_path: str
    __file: object
    __tower_names: list[str]

    def __init__(self, file_path: str = "hanoi_log.txt") -> None:
        """Initialises the log file visualiser.

        Args:
            file_path: Path to the output file. Created or overwritten on start.
        """
        self.__file_path   = file_path
        self.__file        = None
        self.__tower_names = ["A", "B", "C"]

    def on_start(self, n: int, towers: list[list[int]]) -> None:
        """Opens the file and writes the header.

        Args:
            n: Total number of discs.
            towers: Initial board state (unused).
        """
        self.__file = open(self.__file_path, "w", encoding="utf-8")
        self.__file.write(f"Towers of Hanoi — {n} discs\n")
        self.__file.write("=" * 35 + "\n\n")
        log.debug("Log file opened: %s", self.__file_path)

    def on_move(self, step: int, disc: int, origin: int, destination: int, towers: list[list[int]]) -> None:
        """Writes a single move entry to the file.

        Args:
            step: Current move number.
            disc: Size of the disc that was moved.
            origin: Source tower index.
            destination: Destination tower index.
            towers: Updated board state (unused).
        """
        orig = self.__tower_names[origin]
        dest = self.__tower_names[destination]
        self.__file.write(f"Step {step:>4}: disc {disc}  {orig} -> {dest}\n")

    def on_finish(self, total_steps: int, towers: list[list[int]]) -> None:
        """Writes the summary footer and closes the file.

        Args:
            total_steps: Total number of moves performed.
            towers: Final board state (unused).
        """
        self.__file.write(f"\nTotal: {total_steps} moves\n")
        self.__file.close()
        log.info("Move log saved to: %s", self.__file_path)
        print(f"  Log saved to: {self.__file_path}")


class CompositeVisualiser(TowerVisualiser):
    """Adapter that delegates to multiple visualisers simultaneously.

    Allows combining adapters freely, for example rendering to the terminal
    while also writing to a log file.
    """

    __children: tuple[TowerVisualiser, ...]

    def __init__(self, *visualisers: TowerVisualiser) -> None:
        """Initialises the composite with one or more child visualisers.

        Args:
            *visualisers: Any number of TowerVisualiser adapters to delegate to.
        """
        self.__children = visualisers

    def on_start(self, n: int, towers: list[list[int]]) -> None:
        """Delegates on_start to all children.

        Args:
            n: Total number of discs.
            towers: Initial board state.
        """
        for v in self.__children:
            v.on_start(n, towers)

    def on_move(self, step: int, disc: int, origin: int, destination: int, towers: list[list[int]]) -> None:
        """Delegates on_move to all children.

        Args:
            step: Current move number.
            disc: Size of the disc that was moved.
            origin: Source tower index.
            destination: Destination tower index.
            towers: Updated board state.
        """
        for v in self.__children:
            v.on_move(step, disc, origin, destination, towers)

    def on_finish(self, total_steps: int, towers: list[list[int]]) -> None:
        """Delegates on_finish to all children.

        Args:
            total_steps: Total number of moves performed.
            towers: Final board state.
        """
        for v in self.__children:
            v.on_finish(total_steps, towers)
