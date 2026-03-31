"""Recursive solver engine for the Towers of Hanoi."""

__all__ = ["HanoiEngine"]

import logging

from domain.estat import GameState
from ports.visualitzador import TowerVisualiser

log = logging.getLogger(__name__)


class HanoiEngine:
    """Recursive solver for the Towers of Hanoi problem.

    Contains the pure domain logic. Unaware of any I/O concerns.
    Communicates outward exclusively through the TowerVisualiser port.
    """

    __state: GameState
    __visualiser: TowerVisualiser
    __n: int
    __step: int

    def __init__(self, n: int, visualiser: TowerVisualiser) -> None:
        """Initialises the engine with a given number of discs and a visualiser.

        Args:
            n: Number of discs to solve for.
            visualiser: Adapter implementing the TowerVisualiser port.
        """
        self.__state = GameState(n)
        self.__visualiser = visualiser
        self.__n = n
        self.__step = 0

    def solve(self) -> None:
        """Starts the recursive resolution from tower A to tower C.

        Notifies the visualiser before the first move and after completion.
        """
        log.info("Starting Hanoi resolution with %d discs", self.__n)
        self.__visualiser.on_start(self.__n, self.__state.all_towers())
        self.__hanoi(self.__n, origin=0, destination=2, auxiliary=1)
        self.__visualiser.on_finish(self.__step, self.__state.all_towers())
        log.info("Resolution completed in %d moves", self.__step)

    def __hanoi(self, n: int, origin: int, destination: int, auxiliary: int) -> None:
        """Recursively solves the problem for n discs.

        Base case:    n == 1  — move directly and notify.
        Recursive case:
            1. Move n-1 discs from origin to auxiliary (using destination as support).
            2. Move disc n from origin to destination.
            3. Move n-1 discs from auxiliary to destination (using origin as support).

        Args:
            n: Number of discs to move in this recursive call.
            origin: Index of the source tower.
            destination: Index of the destination tower.
            auxiliary: Index of the auxiliary tower.
        """
        if n == 1:
            self.__move_and_notify(origin, destination)
            return

        self.__hanoi(n - 1, origin, auxiliary, destination)
        self.__move_and_notify(origin, destination)
        self.__hanoi(n - 1, auxiliary, destination, origin)

    def __move_and_notify(self, origin: int, destination: int) -> None:
        """Performs a single disc move and notifies the visualiser.

        Args:
            origin: Index of the source tower.
            destination: Index of the destination tower.
        """
        disc = self.__state.move(origin, destination)
        self.__step += 1
        log.debug("Step %d: disc %d · tower %d → tower %d", self.__step, disc.size, origin, destination)
        self.__visualiser.on_move(
            step=self.__step,
            disc=disc.size,
            origin=origin,
            destination=destination,
            towers=self.__state.all_towers(),
        )
