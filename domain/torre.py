"""Tower entity for the Towers of Hanoi domain."""

__all__ = ["Tower"]

from domain.disc import Disc


class Tower:
    """Represents one of the three towers in the Towers of Hanoi game.

    A tower acts as a stack of discs, enforcing push and pop semantics.
    The internal list is never exposed directly to prevent external mutation.
    """

    __discs: list[Disc]

    def __init__(self, discs: list[Disc] | None = None) -> None:
        """Initialises the tower with an optional list of discs.

        Args:
            discs: Initial discs from bottom to top, largest first.
                   Defaults to an empty tower if not provided.
        """
        self.__discs = list(discs or [])

    def push(self, disc: Disc) -> None:
        """Places a disc on top of the tower.

        Args:
            disc: The disc to place on top.
        """
        self.__discs.append(disc)

    def pop(self) -> Disc:
        """Removes and returns the disc on top of the tower.

        Returns:
            The disc that was on top.

        Raises:
            IndexError: If the tower is empty.
        """
        if not self.__discs:
            raise IndexError("Cannot pop from an empty tower")
        return self.__discs.pop()

    @property
    def top(self) -> Disc | None:
        """The disc currently on top of the tower, or None if empty."""
        return self.__discs[-1] if self.__discs else None

    @property
    def discs(self) -> list[Disc]:
        """A copy of all discs in the tower, from bottom to top."""
        return list(self.__discs)

    def __len__(self) -> int:
        """Returns the number of discs currently on the tower."""
        return len(self.__discs)

    def __repr__(self) -> str:
        """Returns an unambiguous string representation.

        Returns:
            A string listing all discs from bottom to top.
        """
        return f"Tower({self.__discs})"
