"""Tests for the Disc value object."""

import warnings
import pytest

from domain.disc import Disc


class TestDiscCreation:

    def test_creates_disc_with_valid_size(self):
        disc = Disc(3)
        assert disc.size == 3

    def test_creates_disc_with_size_one(self):
        disc = Disc(1)
        assert disc.size == 1

    def test_raises_on_zero_size(self):
        with pytest.raises(ValueError):
            Disc(0)

    def test_raises_on_negative_size(self):
        with pytest.raises(ValueError):
            Disc(-1)

    def test_raises_on_non_integer_size(self):
        with pytest.raises(ValueError):
            Disc(1.5)


class TestDiscImmutability:

    def test_size_is_read_only(self):
        disc = Disc(3)
        with pytest.raises(AttributeError):
            disc.size = 5


class TestDiscEquality:

    def test_equal_discs_have_same_size(self):
        assert Disc(3) == Disc(3)

    def test_different_discs_have_different_size(self):
        assert Disc(3) != Disc(4)

    @pytest.mark.filterwarnings("ignore::UserWarning")
    def test_comparing_with_non_disc_returns_false(self):
        assert Disc(3) != 3

    def test_comparing_with_non_disc_emits_warning(self):
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            Disc(3) == 3
            assert len(caught) == 1
            assert issubclass(caught[0].category, UserWarning)


class TestDiscRepr:

    def test_repr_contains_size(self):
        assert repr(Disc(3)) == "Disc(3)"
