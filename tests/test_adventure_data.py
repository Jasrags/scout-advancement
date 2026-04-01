"""Tests for src.core.adventure_data."""

from pathlib import Path

import pytest

from src.core.adventure_data import (
    ADVENTURES,
    Adventure,
    _normalize_item_name,
    find_adventure,
    get_rank_adventures,
    normalize_rank,
)


class TestNormalizeRank:
    @pytest.mark.parametrize(
        "den_type,expected",
        [
            ("lion", "lion"),
            ("lions", "lion"),
            ("Lion", "lion"),
            ("LIONS", "lion"),
            ("tiger", "tiger"),
            ("tigers", "tiger"),
            ("wolf", "wolf"),
            ("wolves", "wolf"),
            ("bear", "bear"),
            ("bears", "bear"),
            ("webelos", "webelos"),
            ("aol", "arrow of light"),
            ("AOL", "arrow of light"),
            ("arrow of light", "arrow of light"),
            ("webelos 2", "arrow of light"),
        ],
    )
    def test_known_ranks(self, den_type: str, expected: str) -> None:
        assert normalize_rank(den_type) == expected

    def test_unknown_rank_returns_none(self) -> None:
        assert normalize_rank("unknown") is None

    def test_whitespace_stripped(self) -> None:
        assert normalize_rank("  lion  ") == "lion"


class TestNormalizeItemName:
    @pytest.mark.parametrize(
        "item_name,expected",
        [
            ("Fun on the Run Adventure", "fun on the run"),
            ("Archery (Lion) Adventure", "archery"),
            ("BB (Tiger) Adventure", "bb"),
            ("BB Gun (Webelos) Adventure", "bb gun"),
            ("Slingshot (Bear) Adventure", "slingshot"),
            ("Bobcat (Wolf) Adventure", "bobcat"),
            ("Mountain Lion Adventure", "mountain lion"),
            ("King of the Jungle Adventure", "king of the jungle"),
            ("Build It Up, Knock It Down Adventure", "build it up, knock it down"),
            ("  Council Fire Adventure  ", "council fire"),
            ("Tigers in the Water Adventure", "tigers in the water"),
            ("BB (Bears) Adventure", "bb"),
        ],
    )
    def test_normalization(self, item_name: str, expected: str) -> None:
        assert _normalize_item_name(item_name) == expected


class TestFindAdventure:
    def test_finds_required_adventure(self) -> None:
        result = find_adventure("Fun on the Run Adventure", "lions")
        assert result is not None
        assert result.name == "Fun on the Run"
        assert result.required is True
        assert "fun_on_the_run" in result.image_path

    def test_finds_elective_adventure(self) -> None:
        result = find_adventure("Build It Up, Knock It Down Adventure", "lion")
        assert result is not None
        assert result.name == "Build It Up, Knock It Down"
        assert result.required is False

    def test_finds_bobcat_per_rank(self) -> None:
        lion_bobcat = find_adventure("Bobcat Adventure", "lion")
        wolf_bobcat = find_adventure("Bobcat (Wolf) Adventure", "wolves")
        assert lion_bobcat is not None
        assert wolf_bobcat is not None
        assert lion_bobcat.image_path != wolf_bobcat.image_path

    def test_shooting_sport_matches(self) -> None:
        result = find_adventure("Archery (Lion) Adventure", "lions")
        assert result is not None
        assert result.name == "Archery"
        assert "archery" in result.image_path

    def test_unknown_adventure_returns_none(self) -> None:
        result = find_adventure("Nonexistent Adventure", "lion")
        assert result is None

    def test_unknown_rank_returns_none(self) -> None:
        result = find_adventure("Fun on the Run Adventure", "unknown")
        assert result is None

    def test_finds_tiger_adventure(self) -> None:
        result = find_adventure("Team Tiger Adventure", "tigers")
        assert result is not None
        assert result.name == "Team Tiger"

    def test_finds_webelos_adventure(self) -> None:
        result = find_adventure("My Community Adventure", "webelos")
        assert result is not None
        assert result.name == "My Community"

    def test_finds_aol_adventure(self) -> None:
        result = find_adventure("Citizenship Adventure", "aol")
        assert result is not None
        assert result.name == "Citizenship"


class TestGetRankAdventures:
    def test_returns_adventures_for_valid_rank(self) -> None:
        adventures = get_rank_adventures("lion")
        assert len(adventures) > 0
        assert all(isinstance(a, Adventure) for a in adventures)

    def test_returns_empty_for_unknown_rank(self) -> None:
        assert get_rank_adventures("unknown") == []

    def test_returns_copy(self) -> None:
        a = get_rank_adventures("lion")
        b = get_rank_adventures("lion")
        assert a is not b


class TestAdventureData:
    def test_all_ranks_have_adventures(self) -> None:
        for rank in ["lion", "tiger", "wolf", "bear", "webelos", "arrow of light"]:
            assert rank in ADVENTURES
            assert len(ADVENTURES[rank]) > 0

    def test_all_adventures_have_local_images(self) -> None:
        for rank, adventures in ADVENTURES.items():
            for adv in adventures:
                assert Path(adv.image_path).exists(), (
                    f"{rank}/{adv.name} image missing: {adv.image_path}"
                )

    def test_all_ranks_have_required_adventures(self) -> None:
        for rank, adventures in ADVENTURES.items():
            required = [a for a in adventures if a.required]
            assert len(required) >= 5, f"{rank} has fewer than 5 required adventures"
