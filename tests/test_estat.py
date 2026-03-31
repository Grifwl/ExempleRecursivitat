"""Tests for the GameState domain object."""

import pytest

from domain.estat import GameState


class TestGameStateCreation:

    def test_initialises_with_all_discs_on_first_tower(self):
        state = GameState(3)
        towers = state.all_towers()
        assert towers[0] == [3, 2, 1]
        assert towers[1] == []
        assert towers[2] == []

    def test_n_property_returns_disc_count(self):
        state = GameState(4)
        assert state.n == 4

    def test_n_is_read_only(self):
        state = GameState(3)
        with pytest.raises(AttributeError):
            state.n = 5

    def test_raises_on_zero_discs(self):
        with pytest.raises(ValueError):
            GameState(0)

    def test_raises_on_negative_discs(self):
        with pytest.raises(ValueError):
            GameState(-1)

    def test_raises_on_non_integer_discs(self):
        with pytest.raises(ValueError):
            GameState(2.5)


class TestGameStateMove:

    def test_move_transfers_disc_between_towers(self):
        state = GameState(3)
        state.move(0, 2)
        towers = state.all_towers()
        assert towers[0] == [3, 2]
        assert towers[2] == [1]

    def test_move_returns_moved_disc(self):
        state = GameState(3)
        disc = state.move(0, 2)
        assert disc.size == 1

    def test_move_from_empty_tower_raises(self):
        state = GameState(3)
        with pytest.raises(IndexError):
            state.move(1, 2)


class TestGameStateAllTowers:

    def test_all_towers_returns_integers(self):
        state = GameState(2)
        towers = state.all_towers()
        assert towers[0] == [2, 1]

    def test_all_towers_returns_copy(self):
        state = GameState(2)
        towers = state.all_towers()
        towers[0].append(99)
        assert state.all_towers()[0] == [2, 1]
