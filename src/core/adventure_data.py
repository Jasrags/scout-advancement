"""Adventure data mapping for Cub Scout ranks.

Maps adventure names to local loop/pin images. Used by the bagging guide
generator and inventory widget to show images alongside each adventure.

Images are bundled in packaging/images/<version>/ and were originally sourced
from https://www.scouting.org/programs/cub-scouts/adventures/

To refresh images when the program year changes, run:
    python scripts/fetch_adventures.py
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


def _resolve_img_root() -> Path:
    # In a PyInstaller bundle, data files live under sys._MEIPASS.
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        return Path(meipass) / "packaging" / "images"
    return Path(__file__).resolve().parent.parent.parent / "packaging" / "images"


_IMG_ROOT = _resolve_img_root()

# Module-level active version state
_active_version: str = ""


@dataclass(frozen=True)
class Adventure:
    name: str
    image_path: str
    required: bool


# ---------------------------------------------------------------------------
# Adventure definitions (name, image filename, required)
# These are version-independent — the image path is computed per version.
# ---------------------------------------------------------------------------

_ADVENTURE_DEFS: dict[str, list[tuple[str, str, bool]]] = {
    "lion": [
        ("Fun on the Run", "lion_fun_on_the_run.jpg", True),
        ("Lion's Roar", "lion_lion_s_roar.jpg", True),
        ("Lion's Pride", "lion_lion_s_pride.jpg", True),
        ("King of the Jungle", "lion_king_of_the_jungle.jpg", True),
        ("Mountain Lion", "lion_mountain_lion.jpg", True),
        ("Bobcat", "lion_bobcat.jpg", True),
        ("Build It Up, Knock It Down", "lion_build_it_up_knock_it_down.jpg", False),
        ("Champions for Nature", "lion_champions_for_nature.jpg", False),
        ("Count On Me", "lion_count_on_me.jpg", False),
        ("Everyday Tech", "lion_everyday_tech.jpg", False),
        ("Gizmos and Gadgets", "lion_gizmos_and_gadgets.jpg", False),
        ("Go Fish", "lion_go_fish.jpg", False),
        ("I'll Do It Myself", "lion_i_ll_do_it_myself.jpg", False),
        ("Let's Camp", "lion_let_s_camp.jpg", False),
        ("On a Roll", "lion_on_a_roll.jpg", False),
        ("On Your Mark", "lion_on_your_mark.jpg", False),
        ("Pick My Path", "lion_pick_my_path.jpg", False),
        ("Race Time", "lion_race_time.jpg", False),
        ("Ready, Set, Grow", "lion_ready_set_grow.jpg", False),
        ("Time to Swim", "lion_time_to_swim.jpg", False),
        ("Archery", "lion_archery.jpg", False),
        ("Slingshot", "lion_slingshot.jpg", False),
    ],
    "tiger": [
        ("Tiger Bites", "tiger_tiger_bites.jpg", True),
        ("Tiger's Roar", "tiger_tiger_s_roar.jpg", True),
        ("Tiger Circles", "tiger_tiger_circles.jpg", True),
        ("Team Tiger", "tiger_team_tiger.jpg", True),
        ("Tigers in the Wild", "tiger_tigers_in_the_wild.jpg", True),
        ("Bobcat", "tiger_bobcat.jpg", True),
        ("Champions for Nature", "tiger_champions_for_nature.jpg", False),
        (
            "Curiosity, Intrigue and Magical Mysteries",
            "tiger_curiosity_intrigue_and_magical_mysteries.jpg",
            False,
        ),
        ("Designed by Tiger", "tiger_designed_by_tiger.jpg", False),
        ("Fish On", "tiger_fish_on.jpg", False),
        ("Floats and Boats", "tiger_floats_and_boats.jpg", False),
        ("Good Knights", "tiger_good_knights.jpg", False),
        ("Let's Camp", "tiger_let_s_camp.jpg", False),
        ("Race Time", "tiger_race_time.jpg", False),
        ("Rolling Tigers", "tiger_rolling_tigers.jpg", False),
        ("Safe and Smart", "tiger_safe_and_smart.jpg", False),
        ("Sky is the Limit", "tiger_sky_is_the_limit.jpg", False),
        ("Stories in Shapes", "tiger_stories_in_shapes.jpg", False),
        ("Summertime Fun", "tiger_summertime_fun.jpg", False),
        ("Tech All Around", "tiger_tech_all_around.jpg", False),
        ("Tiger Tag", "tiger_tiger_tag.jpg", False),
        ("Tiger-iffic!", "tiger_tiger_iffic.jpg", False),
        ("Tigers in the Water", "tiger_tigers_in_the_water.jpg", False),
        ("Archery", "tiger_archery.jpg", False),
        ("Slingshot", "tiger_slingshot.jpg", False),
        ("BB", "tiger_bb.jpg", False),
    ],
    "wolf": [
        ("Running With the Pack", "wolf_running_with_the_pack.jpg", True),
        ("Safety in Numbers", "wolf_safety_in_numbers.jpg", True),
        ("Footsteps", "wolf_footsteps.jpg", True),
        ("Council Fire", "wolf_council_fire.jpg", True),
        ("Paws on the Path", "wolf_paws_on_the_path.jpg", True),
        ("Bobcat", "wolf_bobcat.jpg", True),
        ("A Wolf Goes Fishing", "wolf_a_wolf_goes_fishing.jpg", False),
        ("Adventures in Coins", "wolf_adventures_in_coins.jpg", False),
        ("Air of the Wolf", "wolf_air_of_the_wolf.jpg", False),
        ("Champions for Nature", "wolf_champions_for_nature.jpg", False),
        ("Code of the Wolf", "wolf_code_of_the_wolf.jpg", False),
        ("Computing Wolves", "wolf_computing_wolves.jpg", False),
        ("Cubs Who Care", "wolf_cubs_who_care.jpg", False),
        ("Digging in the Past", "wolf_digging_in_the_past.jpg", False),
        ("Finding Your Way", "wolf_finding_your_way.jpg", False),
        ("Germs Alive!", "wolf_germs_alive.jpg", False),
        ("Let's Camp", "wolf_let_s_camp.jpg", False),
        ("Paws for Water", "wolf_paws_for_water.jpg", False),
        ("Paws of Skill", "wolf_paws_of_skill.jpg", False),
        ("Pedal With the Pack", "wolf_pedal_with_the_pack.jpg", False),
        ("Race Time", "wolf_race_time.jpg", False),
        ("Spirit of the Water", "wolf_spirit_of_the_water.jpg", False),
        ("Summertime Fun", "wolf_summertime_fun.jpg", False),
        ("Archery", "wolf_archery.jpg", False),
        ("Slingshot", "wolf_slingshot.jpg", False),
        ("BB", "wolf_bb.jpg", False),
    ],
    "bear": [
        ("Bear Strong", "bear_bear_strong.jpg", True),
        ("Standing Tall", "bear_standing_tall.jpg", True),
        ("Fellowship", "bear_fellowship.jpg", True),
        ("Paws for Action", "bear_paws_for_action.jpg", True),
        ("Bear Habitat", "bear_bear_habitat.jpg", True),
        ("Bobcat", "bear_bobcat.jpg", True),
        ("A Bear Goes Fishing", "bear_a_bear_goes_fishing.jpg", False),
        ("Balancing Bears", "bear_balancing_bears.jpg", False),
        ("Baloo the Builder", "bear_baloo_the_builder.jpg", False),
        ("Bears Afloat", "bear_bears_afloat.jpg", False),
        ("Bears on Bikes", "bear_bears_on_bikes.jpg", False),
        ("Champions for Nature", "bear_champions_for_nature.jpg", False),
        ("Chef Tech", "bear_chef_tech.jpg", False),
        ("Critter Care", "bear_critter_care.jpg", False),
        ("Forensics", "bear_forensics.jpg", False),
        ("Let's Camp", "bear_let_s_camp.jpg", False),
        ("Marble Madness", "bear_marble_madness.jpg", False),
        ("Race Time", "bear_race_time.jpg", False),
        ("Roaring Laughter", "bear_roaring_laughter.jpg", False),
        ("Salmon Run", "bear_salmon_run.jpg", False),
        ("Summertime Fun", "bear_summertime_fun.jpg", False),
        ("Super Science", "bear_super_science.jpg", False),
        ("Whittling", "bear_whittling.jpg", False),
        ("Archery", "bear_archery.jpg", False),
        ("Slingshot", "bear_slingshot.jpg", False),
        ("BB", "bear_bb.jpg", False),
    ],
    "webelos": [
        ("Bobcat", "webelos_bobcat.jpg", True),
        ("Stronger, Faster, Higher", "webelos_stronger_faster_higher.jpg", True),
        ("My Safety", "webelos_my_safety.jpg", True),
        ("My Family", "webelos_my_family.jpg", True),
        ("My Community", "webelos_my_community.jpg", True),
        ("Webelos Walkabout", "webelos_webelos_walkabout.jpg", True),
        ("Aquanaut", "webelos_aquanaut.jpg", False),
        ("Art Explosion", "webelos_art_explosion.jpg", False),
        ("Aware and Care", "webelos_aware_and_care.jpg", False),
        ("Build It", "webelos_build_it.jpg", False),
        ("Catch the Big One", "webelos_catch_the_big_one.jpg", False),
        ("Champions for Nature", "webelos_champions_for_nature.jpg", False),
        ("Chef's Knife", "webelos_chef_s_knife.jpg", False),
        ("Earth Rocks", "webelos_earth_rocks.jpg", False),
        ("Let's Camp", "webelos_let_s_camp.jpg", False),
        ("Math on the Trail", "webelos_math_on_the_trail.jpg", False),
        ("Modular Design", "webelos_modular_design.jpg", False),
        ("Paddle Onward", "webelos_paddle_onward.jpg", False),
        ("Pedal Away", "webelos_pedal_away.jpg", False),
        ("Race Time", "webelos_race_time.jpg", False),
        ("Summertime Fun", "webelos_summertime_fun.jpg", False),
        ("Tech on the Trail", "webelos_tech_on_the_trail.jpg", False),
        ("Yo-Yo", "webelos_yo_yo.jpg", False),
        ("Archery", "webelos_archery.jpg", False),
        ("Slingshot", "webelos_slingshot.jpg", False),
        ("BB Gun", "webelos_bb_gun.jpg", False),
    ],
    "arrow of light": [
        ("Personal Fitness", "arrow_of_light_personal_fitness.jpg", True),
        ("First Aid", "arrow_of_light_first_aid.jpg", True),
        ("Duty to God", "arrow_of_light_duty_to_god.jpg", True),
        ("Citizenship", "arrow_of_light_citizenship.jpg", True),
        ("Outdoor Adventurer", "arrow_of_light_outdoor_adventurer.jpg", True),
        ("Bobcat", "arrow_of_light_bobcat.jpg", True),
        ("Champions for Nature", "arrow_of_light_champions_for_nature.jpg", False),
        ("Cycling", "arrow_of_light_cycling.jpg", False),
        ("Engineer", "arrow_of_light_engineer.jpg", False),
        ("Estimations", "arrow_of_light_estimations.jpg", False),
        ("Fishing", "arrow_of_light_fishing.jpg", False),
        ("High Tech Outdoors", "arrow_of_light_high_tech_outdoors.jpg", False),
        ("Into the Wild", "arrow_of_light_into_the_wild.jpg", False),
        ("Into the Woods", "arrow_of_light_into_the_woods.jpg", False),
        ("Knife Safety", "arrow_of_light_knife_safety.jpg", False),
        ("Paddle Craft", "arrow_of_light_paddle_craft.jpg", False),
        ("Race Time", "arrow_of_light_race_time.jpg", False),
        ("Summertime Fun", "arrow_of_light_summertime_fun.jpg", False),
        ("Swimming", "arrow_of_light_swimming.jpg", False),
        ("Archery", "arrow_of_light_archery.jpg", False),
        ("Slingshot", "arrow_of_light_slingshot.jpg", False),
        ("BB", "arrow_of_light_bb.jpg", False),
    ],
}


# ---------------------------------------------------------------------------
# Version management
# ---------------------------------------------------------------------------


def get_available_versions() -> list[str]:
    """Return sorted list of available adventure versions (e.g. ['2023_2024'])."""
    if not _IMG_ROOT.is_dir():
        return []
    return sorted(d.name for d in _IMG_ROOT.iterdir() if d.is_dir() and not d.name.startswith("."))


def get_active_version() -> str:
    """Return the currently active adventure version."""
    global _active_version  # noqa: PLW0602
    if not _active_version:
        versions = get_available_versions()
        _active_version = versions[-1] if versions else "2023_2024"
    return _active_version


def set_active_version(version: str) -> None:
    """Switch the active adventure version and rebuild ADVENTURES."""
    global _active_version, ADVENTURES
    _active_version = version
    ADVENTURES = _build_adventures(version)


def _build_adventures(version: str) -> dict[str, list[Adventure]]:
    """Build the ADVENTURES dict with image paths for the given version."""
    img_dir = _IMG_ROOT / version
    result: dict[str, list[Adventure]] = {}
    for rank, defs in _ADVENTURE_DEFS.items():
        result[rank] = [
            Adventure(name, str(img_dir / filename), required) for name, filename, required in defs
        ]
    return result


# ---------------------------------------------------------------------------
# Module-level ADVENTURES dict (initialized on import)
# ---------------------------------------------------------------------------

ADVENTURES: dict[str, list[Adventure]] = _build_adventures(get_active_version())


# ---------------------------------------------------------------------------
# Rank aliases and lookup functions
# ---------------------------------------------------------------------------

RANK_ALIASES: dict[str, str] = {
    "lion": "lion",
    "lions": "lion",
    "tiger": "tiger",
    "tigers": "tiger",
    "wolf": "wolf",
    "wolves": "wolf",
    "bear": "bear",
    "bears": "bear",
    "webelos": "webelos",
    "webelos 2": "arrow of light",
    "arrow of light": "arrow of light",
    "aol": "arrow of light",
}


def normalize_rank(den_type: str) -> str | None:
    """Convert a CSV den_type value to a canonical rank key.

    Returns None if the den_type is not recognized.
    """
    return RANK_ALIASES.get(den_type.strip().lower())


def _normalize_item_name(item_name: str) -> str:
    """Normalize a CSV Item Name for matching.

    Strips the ' Adventure' suffix and any rank qualifier like '(Lion)'.
    """
    name = item_name.strip()
    if name.lower().endswith(" adventure"):
        name = name[: -len(" adventure")]
    name = re.sub(r"\s*\([^)]+\)\s*$", "", name)
    return name.strip().lower()


def find_adventure(item_name: str, den_type: str) -> Adventure | None:
    """Look up the Adventure matching a CSV item name and den type.

    Returns None if no match is found.
    """
    rank = normalize_rank(den_type)
    if rank is None:
        return None

    adventures = ADVENTURES.get(rank, [])
    normalized = _normalize_item_name(item_name)

    for adv in adventures:
        if adv.name.lower() == normalized:
            return adv

    return None


def get_rank_adventures(den_type: str) -> list[Adventure]:
    """Return all adventures for a given rank (den type)."""
    rank = normalize_rank(den_type)
    if rank is None:
        return []
    return list(ADVENTURES.get(rank, []))
