"""Tests for the Tower entity."""

import pytest

from domain.disc import Disc
from domain.torre import Tower


class TestTowerCreation:

    def test_creates_empty_tower(self):
        tower = Tower()
        assert len(tower) == 0

    def test_creates_tower_with_initial_discs(self):
        tower = Tower([Disc(3), Disc(2), Disc(1)])
        assert len(tower) == 3

    def test_initial_discs_are_copied(self):
        discs = [Disc(3), Disc(2), Disc(1)]
        tower = Tower(discs)
        discs.append(Disc(4))
        assert len(tower) == 3


class TestTowerPush:

    def test_push_increases_length(self):
        tower = Tower()
        tower.push(Disc(1))
        assert len(tower) == 1

    def test_push_places_disc_on_top(self):
        tower = Tower()
        tower.push(Disc(3))
        tower.push(Disc(1))
        assert tower.top.size == 1


class TestTowerPop:

    def test_pop_removes_top_disc(self):
        tower = Tower([Disc(3), Disc(1)])
        tower.pop()
        assert len(tower) == 1

    def test_pop_returns_top_disc(self):
        tower = Tower([Disc(3), Disc(1)])
        disc = tower.pop()
        assert disc.size == 1

    def test_pop_on_empty_tower_raises(self):
        tower = Tower()
        with pytest.raises(IndexError):
            tower.pop()

    def test_push_and_pop_are_lifo(self):
        tower = Tower()
        tower.push(Disc(3))
        tower.push(Disc(2))
        tower.push(Disc(1))
        assert tower.pop().size == 1
        assert tower.pop().size == 2
        assert tower.pop().size == 3


class TestTowerTop:

    def test_top_returns_none_on_empty_tower(self):
        tower = Tower()
        assert tower.top is None

    def test_top_does_not_remove_disc(self):
        tower = Tower([Disc(1)])
        tower.top
        assert len(tower) == 1


class TestTowerDiscs:

    def test_discs_returns_all_discs(self):
        tower = Tower([Disc(3), Disc(2), Disc(1)])
        assert [d.size for d in tower.discs] == [3, 2, 1]

    def test_discs_returns_copy(self):
        tower = Tower([Disc(1)])
        copy = tower.discs
        copy.append(Disc(2))
        assert len(tower) == 1
