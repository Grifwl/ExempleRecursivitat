"""Output port defining the visualiser contract."""

__all__ = ["TowerVisualiser"]

from abc import ABC, abstractmethod


class TowerVisualiser(ABC):
    """Output port for tower visualisation.

    Defines the contract that any visualiser adapter must fulfil.
    The domain only depends on this interface, never on concrete adapters.
    """

    @abstractmethod
    def on_start(self, n: int, towers: list[list[int]]) -> None:
        """Called once before the first move, with the initial board state.

        Args:
            n: Total number of discs in the game.
            towers: Initial state of all three towers as lists of disc sizes.
        """

    @abstractmethod
    def on_move(
        self,
        step: int,
        disc: int,
        origin: int,
        destination: int,
        towers: list[list[int]],
    ) -> None:
        """Called after each move with the updated board state.

        Args:
            step: Current move number, starting at 1.
            disc: Size of the disc that was moved.
            origin: Index of the tower the disc was moved from.
            destination: Index of the tower the disc was moved to.
            towers: Updated state of all three towers as lists of disc sizes.
        """

    @abstractmethod
    def on_finish(self, total_steps: int, towers: list[list[int]]) -> None:
        """Called once after the last move, when the puzzle is solved.

        Args:
            total_steps: Total number of moves performed.
            towers: Final state of all three towers as lists of disc sizes.
        """
