"""Game state for the Towers of Hanoi domain."""

__all__ = ["GameState"]

from domain.disc import Disc
from domain.torre import Tower


class GameState:
    """Holds and mutates the state of the three towers.

    This class is the single source of truth for the board.
    All mutations go through move(), which keeps the state consistent.
    """

    __n: int
    __towers: list[Tower]

    def __init__(self, n: int) -> None:
        """Initialises the game with n discs stacked on the first tower.

        Args:
            n: Number of discs. Must be a positive integer.

        Raises:
            ValueError: If n is not a positive integer.
        """
        if not isinstance(n, int) or n < 1:
            raise ValueError(f"Number of discs must be a positive integer, got {n!r}")
        self.__n = n
        self.__towers = [
            Tower([Disc(size) for size in range(n, 0, -1)]),
            Tower(),
            Tower(),
        ]

    @property
    def n(self) -> int:
        """The number of discs in the game. Read-only."""
        return self.__n

    def move(self, origin: int, destination: int) -> Disc:
        """Moves the top disc from origin to destination.

        Args:
            origin: Index of the source tower (0, 1, or 2).
            destination: Index of the destination tower (0, 1, or 2).

        Returns:
            The disc that was moved.

        Raises:
            IndexError: If either tower index is out of range.
            IndexError: If the origin tower is empty.
        """
        disc = self.__towers[origin].pop()
        self.__towers[destination].push(disc)
        return disc

    def all_towers(self) -> list[list[int]]:
        """Returns a snapshot of the current board as plain integers.

        Converts Tower and Disc objects to nested lists of integers so that
        adapters remain decoupled from the domain model.

        Returns:
            A list of three lists, each containing disc sizes from bottom to top.
        """
        return [
            [d.size for d in tower.discs]
            for tower in self.__towers
        ]
