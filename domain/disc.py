"""Disc value object for the Towers of Hanoi domain."""

__all__ = ["Disc"]

import warnings


class Disc:
    """Represents a single disc in the Towers of Hanoi game.

    A disc is an immutable value object identified solely by its size.
    Larger size values represent physically larger discs.
    """

    __size: int

    def __init__(self, size: int) -> None:
        """Initialises a disc with the given size.

        Args:
            size: Positive integer representing the disc size.
                  Larger values mean larger discs.

        Raises:
            ValueError: If size is not a positive integer.
        """
        if not isinstance(size, int) or size < 1:
            raise ValueError(f"Disc size must be a positive integer, got {size!r}")
        self.__size = size

    @property
    def size(self) -> int:
        """The size of the disc. Read-only."""
        return self.__size

    def __eq__(self, other: object) -> bool:
        """Checks equality by size value, not identity.

        Args:
            other: Object to compare against.

        Returns:
            True if other is a Disc with the same size, False otherwise.
            Returns NotImplemented if other is not a Disc, allowing Python
            to attempt the comparison from the other side.
        """
        if not isinstance(other, Disc):
            warnings.warn(
                f"Comparing Disc with {type(other).__name__}",
                UserWarning,
                stacklevel=2,
            )
            return NotImplemented
        return self.__size == other.__size

    def __repr__(self) -> str:
        """Returns an unambiguous string representation.

        Returns:
            A string of the form Disc(n) where n is the size.
        """
        return f"Disc({self.__size})"
