"""Tests for the HanoiEngine solver."""

import pytest

from adapters.altres import SilentVisualiser
from domain.engine import HanoiEngine


def solve(n: int) -> SilentVisualiser:
    """Helper that runs the solver for n discs and returns the visualiser.

    Args:
        n: Number of discs to solve for.

    Returns:
        SilentVisualiser with all recorded moves available for inspection.
    """
    visualiser = SilentVisualiser()
    HanoiEngine(n=n, visualiser=visualiser).solve()
    return visualiser


class TestMoveCount:

    def test_one_disc_requires_one_move(self):
        assert len(solve(1).moves) == 1

    def test_two_discs_require_three_moves(self):
        assert len(solve(2).moves) == 3

    def test_three_discs_require_seven_moves(self):
        assert len(solve(3).moves) == 7

    @pytest.mark.parametrize("n", [1, 2, 3, 4, 5, 6])
    def test_n_discs_require_2_to_the_n_minus_1_moves(self, n: int):
        assert len(solve(n).moves) == 2 ** n - 1


class TestMoveValidity:

    @pytest.mark.parametrize("n", [1, 2, 3, 4, 5])
    def test_no_move_places_larger_disc_on_smaller(self, n: int):
        """Simulates the board and verifies every move is legal."""
        towers = [list(range(n, 0, -1)), [], []]

        for move in solve(n).moves:
            orig = move["origin"]
            dest = move["destination"]

            moving_disc = towers[orig][-1]

            if towers[dest]:
                assert moving_disc < towers[dest][-1], (
                    f"Illegal move: disc {moving_disc} placed on {towers[dest][-1]}"
                )

            towers[dest].append(towers[orig].pop())


class TestFinalState:

    @pytest.mark.parametrize("n", [1, 2, 3, 4, 5])
    def test_all_discs_end_on_tower_c(self, n: int):
        """Reconstructs the final board state and checks tower C."""
        towers = [list(range(n, 0, -1)), [], []]

        for move in solve(n).moves:
            towers[move["destination"]].append(towers[move["origin"]].pop())

        assert towers[0] == []
        assert towers[1] == []
        assert towers[2] == list(range(n, 0, -1))

    @pytest.mark.parametrize("n", [1, 2, 3, 4, 5])
    def test_discs_on_tower_c_are_ordered_largest_first(self, n: int):
        """Verifies discs are stacked correctly: largest at bottom."""
        towers = [list(range(n, 0, -1)), [], []]

        for move in solve(n).moves:
            towers[move["destination"]].append(towers[move["origin"]].pop())

        final = towers[2]
        assert final == sorted(final, reverse=True)


class TestStepNumbering:

    def test_steps_are_sequential_starting_at_one(self):
        moves = solve(3).moves
        for i, move in enumerate(moves):
            assert move["step"] == i + 1
