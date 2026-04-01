"""Adventure data mapping for Cub Scout ranks.

Maps adventure names to local loop/pin images. Used by the bagging guide
generator and inventory widget to show images alongside each adventure.

Images are bundled in packaging/images/ and were originally sourced from
https://www.scouting.org/programs/cub-scouts/adventures/

To refresh images when the program year changes, run:
    python scripts/fetch_adventures.py
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

# Bundled adventure images directory
_IMG_DIR = Path(__file__).resolve().parent.parent.parent / "packaging" / "images"


@dataclass(frozen=True)
class Adventure:
    name: str
    image_path: str
    required: bool


# ---------------------------------------------------------------------------
# Adventure data by rank (2023-2024 program year)
# ---------------------------------------------------------------------------

ADVENTURES: dict[str, list[Adventure]] = {
    "lion": [
        # Required (6)
        Adventure("Fun on the Run", str(_IMG_DIR / "lion_fun_on_the_run.jpg"), True),
        Adventure("Lion's Roar", str(_IMG_DIR / "lion_lion_s_roar.jpg"), True),
        Adventure("Lion's Pride", str(_IMG_DIR / "lion_lion_s_pride.jpg"), True),
        Adventure("King of the Jungle", str(_IMG_DIR / "lion_king_of_the_jungle.jpg"), True),
        Adventure("Mountain Lion", str(_IMG_DIR / "lion_mountain_lion.jpg"), True),
        Adventure("Bobcat", str(_IMG_DIR / "lion_bobcat.jpg"), True),
        # Elective
        Adventure(
            "Build It Up, Knock It Down",
            str(_IMG_DIR / "lion_build_it_up_knock_it_down.jpg"),
            False,
        ),
        Adventure("Champions for Nature", str(_IMG_DIR / "lion_champions_for_nature.jpg"), False),
        Adventure("Count On Me", str(_IMG_DIR / "lion_count_on_me.jpg"), False),
        Adventure("Everyday Tech", str(_IMG_DIR / "lion_everyday_tech.jpg"), False),
        Adventure("Gizmos and Gadgets", str(_IMG_DIR / "lion_gizmos_and_gadgets.jpg"), False),
        Adventure("Go Fish", str(_IMG_DIR / "lion_go_fish.jpg"), False),
        Adventure("I'll Do It Myself", str(_IMG_DIR / "lion_i_ll_do_it_myself.jpg"), False),
        Adventure("Let's Camp", str(_IMG_DIR / "lion_let_s_camp.jpg"), False),
        Adventure("On a Roll", str(_IMG_DIR / "lion_on_a_roll.jpg"), False),
        Adventure("On Your Mark", str(_IMG_DIR / "lion_on_your_mark.jpg"), False),
        Adventure("Pick My Path", str(_IMG_DIR / "lion_pick_my_path.jpg"), False),
        Adventure("Race Time", str(_IMG_DIR / "lion_race_time.jpg"), False),
        Adventure("Ready, Set, Grow", str(_IMG_DIR / "lion_ready_set_grow.jpg"), False),
        Adventure("Time to Swim", str(_IMG_DIR / "lion_time_to_swim.jpg"), False),
        # Shooting sports
        Adventure("Archery", str(_IMG_DIR / "lion_archery.jpg"), False),
        Adventure("Slingshot", str(_IMG_DIR / "lion_slingshot.jpg"), False),
    ],
    "tiger": [
        # Required (6)
        Adventure("Tiger Bites", str(_IMG_DIR / "tiger_tiger_bites.jpg"), True),
        Adventure("Tiger's Roar", str(_IMG_DIR / "tiger_tiger_s_roar.jpg"), True),
        Adventure("Tiger Circles", str(_IMG_DIR / "tiger_tiger_circles.jpg"), True),
        Adventure("Team Tiger", str(_IMG_DIR / "tiger_team_tiger.jpg"), True),
        Adventure("Tigers in the Wild", str(_IMG_DIR / "tiger_tigers_in_the_wild.jpg"), True),
        Adventure("Bobcat", str(_IMG_DIR / "tiger_bobcat.jpg"), True),
        # Elective
        Adventure("Champions for Nature", str(_IMG_DIR / "tiger_champions_for_nature.jpg"), False),
        Adventure(
            "Curiosity, Intrigue and Magical Mysteries",
            str(_IMG_DIR / "tiger_curiosity_intrigue_and_magical_mysteries.jpg"),
            False,
        ),
        Adventure("Designed by Tiger", str(_IMG_DIR / "tiger_designed_by_tiger.jpg"), False),
        Adventure("Fish On", str(_IMG_DIR / "tiger_fish_on.jpg"), False),
        Adventure("Floats and Boats", str(_IMG_DIR / "tiger_floats_and_boats.jpg"), False),
        Adventure("Good Knights", str(_IMG_DIR / "tiger_good_knights.jpg"), False),
        Adventure("Let's Camp", str(_IMG_DIR / "tiger_let_s_camp.jpg"), False),
        Adventure("Race Time", str(_IMG_DIR / "tiger_race_time.jpg"), False),
        Adventure("Rolling Tigers", str(_IMG_DIR / "tiger_rolling_tigers.jpg"), False),
        Adventure("Safe and Smart", str(_IMG_DIR / "tiger_safe_and_smart.jpg"), False),
        Adventure("Sky is the Limit", str(_IMG_DIR / "tiger_sky_is_the_limit.jpg"), False),
        Adventure("Stories in Shapes", str(_IMG_DIR / "tiger_stories_in_shapes.jpg"), False),
        Adventure("Summertime Fun", str(_IMG_DIR / "tiger_summertime_fun.jpg"), False),
        Adventure("Tech All Around", str(_IMG_DIR / "tiger_tech_all_around.jpg"), False),
        Adventure("Tiger Tag", str(_IMG_DIR / "tiger_tiger_tag.jpg"), False),
        Adventure("Tiger-iffic!", str(_IMG_DIR / "tiger_tiger_iffic.jpg"), False),
        Adventure("Tigers in the Water", str(_IMG_DIR / "tiger_tigers_in_the_water.jpg"), False),
        # Shooting sports
        Adventure("Archery", str(_IMG_DIR / "tiger_archery.jpg"), False),
        Adventure("Slingshot", str(_IMG_DIR / "tiger_slingshot.jpg"), False),
        Adventure("BB", str(_IMG_DIR / "tiger_bb.jpg"), False),
    ],
    "wolf": [
        # Required (6)
        Adventure("Running With the Pack", str(_IMG_DIR / "wolf_running_with_the_pack.jpg"), True),
        Adventure("Safety in Numbers", str(_IMG_DIR / "wolf_safety_in_numbers.jpg"), True),
        Adventure("Footsteps", str(_IMG_DIR / "wolf_footsteps.jpg"), True),
        Adventure("Council Fire", str(_IMG_DIR / "wolf_council_fire.jpg"), True),
        Adventure("Paws on the Path", str(_IMG_DIR / "wolf_paws_on_the_path.jpg"), True),
        Adventure("Bobcat", str(_IMG_DIR / "wolf_bobcat.jpg"), True),
        # Elective
        Adventure("A Wolf Goes Fishing", str(_IMG_DIR / "wolf_a_wolf_goes_fishing.jpg"), False),
        Adventure("Adventures in Coins", str(_IMG_DIR / "wolf_adventures_in_coins.jpg"), False),
        Adventure("Air of the Wolf", str(_IMG_DIR / "wolf_air_of_the_wolf.jpg"), False),
        Adventure("Champions for Nature", str(_IMG_DIR / "wolf_champions_for_nature.jpg"), False),
        Adventure("Code of the Wolf", str(_IMG_DIR / "wolf_code_of_the_wolf.jpg"), False),
        Adventure("Computing Wolves", str(_IMG_DIR / "wolf_computing_wolves.jpg"), False),
        Adventure("Cubs Who Care", str(_IMG_DIR / "wolf_cubs_who_care.jpg"), False),
        Adventure("Digging in the Past", str(_IMG_DIR / "wolf_digging_in_the_past.jpg"), False),
        Adventure("Finding Your Way", str(_IMG_DIR / "wolf_finding_your_way.jpg"), False),
        Adventure("Germs Alive!", str(_IMG_DIR / "wolf_germs_alive.jpg"), False),
        Adventure("Let's Camp", str(_IMG_DIR / "wolf_let_s_camp.jpg"), False),
        Adventure("Paws for Water", str(_IMG_DIR / "wolf_paws_for_water.jpg"), False),
        Adventure("Paws of Skill", str(_IMG_DIR / "wolf_paws_of_skill.jpg"), False),
        Adventure("Pedal With the Pack", str(_IMG_DIR / "wolf_pedal_with_the_pack.jpg"), False),
        Adventure("Race Time", str(_IMG_DIR / "wolf_race_time.jpg"), False),
        Adventure("Spirit of the Water", str(_IMG_DIR / "wolf_spirit_of_the_water.jpg"), False),
        Adventure("Summertime Fun", str(_IMG_DIR / "wolf_summertime_fun.jpg"), False),
        # Shooting sports
        Adventure("Archery", str(_IMG_DIR / "wolf_archery.jpg"), False),
        Adventure("Slingshot", str(_IMG_DIR / "wolf_slingshot.jpg"), False),
        Adventure("BB", str(_IMG_DIR / "wolf_bb.jpg"), False),
    ],
    "bear": [
        # Required (6)
        Adventure("Bear Strong", str(_IMG_DIR / "bear_bear_strong.jpg"), True),
        Adventure("Standing Tall", str(_IMG_DIR / "bear_standing_tall.jpg"), True),
        Adventure("Fellowship", str(_IMG_DIR / "bear_fellowship.jpg"), True),
        Adventure("Paws for Action", str(_IMG_DIR / "bear_paws_for_action.jpg"), True),
        Adventure("Bear Habitat", str(_IMG_DIR / "bear_bear_habitat.jpg"), True),
        Adventure("Bobcat", str(_IMG_DIR / "bear_bobcat.jpg"), True),
        # Elective
        Adventure("A Bear Goes Fishing", str(_IMG_DIR / "bear_a_bear_goes_fishing.jpg"), False),
        Adventure("Balancing Bears", str(_IMG_DIR / "bear_balancing_bears.jpg"), False),
        Adventure("Baloo the Builder", str(_IMG_DIR / "bear_baloo_the_builder.jpg"), False),
        Adventure("Bears Afloat", str(_IMG_DIR / "bear_bears_afloat.jpg"), False),
        Adventure("Bears on Bikes", str(_IMG_DIR / "bear_bears_on_bikes.jpg"), False),
        Adventure("Champions for Nature", str(_IMG_DIR / "bear_champions_for_nature.jpg"), False),
        Adventure("Chef Tech", str(_IMG_DIR / "bear_chef_tech.jpg"), False),
        Adventure("Critter Care", str(_IMG_DIR / "bear_critter_care.jpg"), False),
        Adventure("Forensics", str(_IMG_DIR / "bear_forensics.jpg"), False),
        Adventure("Let's Camp", str(_IMG_DIR / "bear_let_s_camp.jpg"), False),
        Adventure("Marble Madness", str(_IMG_DIR / "bear_marble_madness.jpg"), False),
        Adventure("Race Time", str(_IMG_DIR / "bear_race_time.jpg"), False),
        Adventure("Roaring Laughter", str(_IMG_DIR / "bear_roaring_laughter.jpg"), False),
        Adventure("Salmon Run", str(_IMG_DIR / "bear_salmon_run.jpg"), False),
        Adventure("Summertime Fun", str(_IMG_DIR / "bear_summertime_fun.jpg"), False),
        Adventure("Super Science", str(_IMG_DIR / "bear_super_science.jpg"), False),
        Adventure("Whittling", str(_IMG_DIR / "bear_whittling.jpg"), False),
        # Shooting sports
        Adventure("Archery", str(_IMG_DIR / "bear_archery.jpg"), False),
        Adventure("Slingshot", str(_IMG_DIR / "bear_slingshot.jpg"), False),
        Adventure("BB", str(_IMG_DIR / "bear_bb.jpg"), False),
    ],
    "webelos": [
        # Required (6)
        Adventure("Bobcat", str(_IMG_DIR / "webelos_bobcat.jpg"), True),
        Adventure(
            "Stronger, Faster, Higher",
            str(_IMG_DIR / "webelos_stronger_faster_higher.jpg"),
            True,
        ),
        Adventure("My Safety", str(_IMG_DIR / "webelos_my_safety.jpg"), True),
        Adventure("My Family", str(_IMG_DIR / "webelos_my_family.jpg"), True),
        Adventure("My Community", str(_IMG_DIR / "webelos_my_community.jpg"), True),
        Adventure("Webelos Walkabout", str(_IMG_DIR / "webelos_webelos_walkabout.jpg"), True),
        # Elective
        Adventure("Aquanaut", str(_IMG_DIR / "webelos_aquanaut.jpg"), False),
        Adventure("Art Explosion", str(_IMG_DIR / "webelos_art_explosion.jpg"), False),
        Adventure("Aware and Care", str(_IMG_DIR / "webelos_aware_and_care.jpg"), False),
        Adventure("Build It", str(_IMG_DIR / "webelos_build_it.jpg"), False),
        Adventure("Catch the Big One", str(_IMG_DIR / "webelos_catch_the_big_one.jpg"), False),
        Adventure(
            "Champions for Nature", str(_IMG_DIR / "webelos_champions_for_nature.jpg"), False
        ),
        Adventure("Chef's Knife", str(_IMG_DIR / "webelos_chef_s_knife.jpg"), False),
        Adventure("Earth Rocks", str(_IMG_DIR / "webelos_earth_rocks.jpg"), False),
        Adventure("Let's Camp", str(_IMG_DIR / "webelos_let_s_camp.jpg"), False),
        Adventure("Math on the Trail", str(_IMG_DIR / "webelos_math_on_the_trail.jpg"), False),
        Adventure("Modular Design", str(_IMG_DIR / "webelos_modular_design.jpg"), False),
        Adventure("Paddle Onward", str(_IMG_DIR / "webelos_paddle_onward.jpg"), False),
        Adventure("Pedal Away", str(_IMG_DIR / "webelos_pedal_away.jpg"), False),
        Adventure("Race Time", str(_IMG_DIR / "webelos_race_time.jpg"), False),
        Adventure("Summertime Fun", str(_IMG_DIR / "webelos_summertime_fun.jpg"), False),
        Adventure("Tech on the Trail", str(_IMG_DIR / "webelos_tech_on_the_trail.jpg"), False),
        Adventure("Yo-Yo", str(_IMG_DIR / "webelos_yo_yo.jpg"), False),
        # Shooting sports
        Adventure("Archery", str(_IMG_DIR / "webelos_archery.jpg"), False),
        Adventure("Slingshot", str(_IMG_DIR / "webelos_slingshot.jpg"), False),
        Adventure("BB Gun", str(_IMG_DIR / "webelos_bb_gun.jpg"), False),
    ],
    "arrow of light": [
        # Required (6)
        Adventure(
            "Personal Fitness",
            str(_IMG_DIR / "arrow_of_light_personal_fitness.jpg"),
            True,
        ),
        Adventure("First Aid", str(_IMG_DIR / "arrow_of_light_first_aid.jpg"), True),
        Adventure("Duty to God", str(_IMG_DIR / "arrow_of_light_duty_to_god.jpg"), True),
        Adventure("Citizenship", str(_IMG_DIR / "arrow_of_light_citizenship.jpg"), True),
        Adventure(
            "Outdoor Adventurer",
            str(_IMG_DIR / "arrow_of_light_outdoor_adventurer.jpg"),
            True,
        ),
        Adventure("Bobcat", str(_IMG_DIR / "arrow_of_light_bobcat.jpg"), True),
        # Elective
        Adventure(
            "Champions for Nature",
            str(_IMG_DIR / "arrow_of_light_champions_for_nature.jpg"),
            False,
        ),
        Adventure("Cycling", str(_IMG_DIR / "arrow_of_light_cycling.jpg"), False),
        Adventure("Engineer", str(_IMG_DIR / "arrow_of_light_engineer.jpg"), False),
        Adventure("Estimations", str(_IMG_DIR / "arrow_of_light_estimations.jpg"), False),
        Adventure("Fishing", str(_IMG_DIR / "arrow_of_light_fishing.jpg"), False),
        Adventure(
            "High Tech Outdoors",
            str(_IMG_DIR / "arrow_of_light_high_tech_outdoors.jpg"),
            False,
        ),
        Adventure("Into the Wild", str(_IMG_DIR / "arrow_of_light_into_the_wild.jpg"), False),
        Adventure("Into the Woods", str(_IMG_DIR / "arrow_of_light_into_the_woods.jpg"), False),
        Adventure("Knife Safety", str(_IMG_DIR / "arrow_of_light_knife_safety.jpg"), False),
        Adventure("Paddle Craft", str(_IMG_DIR / "arrow_of_light_paddle_craft.jpg"), False),
        Adventure("Race Time", str(_IMG_DIR / "arrow_of_light_race_time.jpg"), False),
        Adventure("Summertime Fun", str(_IMG_DIR / "arrow_of_light_summertime_fun.jpg"), False),
        Adventure("Swimming", str(_IMG_DIR / "arrow_of_light_swimming.jpg"), False),
        # Shooting sports
        Adventure("Archery", str(_IMG_DIR / "arrow_of_light_archery.jpg"), False),
        Adventure("Slingshot", str(_IMG_DIR / "arrow_of_light_slingshot.jpg"), False),
        Adventure("BB", str(_IMG_DIR / "arrow_of_light_bb.jpg"), False),
    ],
}

# Rank aliases used in Scoutbook CSV exports -> canonical rank keys
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
    Examples:
        'Fun on the Run Adventure' -> 'fun on the run'
        'Archery (Lion) Adventure' -> 'archery'
        'Bobcat (Wolf) Adventure'  -> 'bobcat'
        'BB (Bears) Adventure'     -> 'bb'
        'BB Gun (Webelos) Adventure' -> 'bb gun'
    """
    name = item_name.strip()
    # Remove trailing ' Adventure'
    if name.lower().endswith(" adventure"):
        name = name[: -len(" adventure")]
    # Remove rank qualifier: '(Lion)', '(Tigers)', '(Wolf)', '(Bears)', '(Webelos)', etc.
    name = re.sub(r"\s*\([^)]+\)\s*$", "", name)
    return name.strip().lower()


def find_adventure(item_name: str, den_type: str) -> Adventure | None:
    """Look up the Adventure matching a CSV item name and den type.

    Returns None if no match is found (adventure may not be in our database yet).
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
