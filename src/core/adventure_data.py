"""Adventure data mapping for Cub Scout ranks.

Maps adventure names to image URLs from scouting.org. Used by the bagging
guide generator to show loop/pin images alongside each adventure.

Data sourced from: https://www.scouting.org/programs/cub-scouts/adventures/
via the WordPress REST API (wp-json/wp/v2/pages?slug=<rank>).

To refresh this data when the program year changes, run:
    python scripts/fetch_adventures.py
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_IMG = "https://www.scouting.org/wp-content/uploads"


@dataclass(frozen=True)
class Adventure:
    name: str
    image_url: str
    required: bool


# ---------------------------------------------------------------------------
# Adventure data by rank (2023-2024 program year)
# ---------------------------------------------------------------------------

ADVENTURES: dict[str, list[Adventure]] = {
    "lion": [
        # Required (6)
        Adventure(
            "Fun on the Run", f"{_IMG}/2024/01/2023_2024_loops_pins_Fun_On_The_Run.jpg", True
        ),
        Adventure("Lion's Roar", f"{_IMG}/2024/01/2023_2024_loops_pins_Lions_Roar.jpg", True),
        Adventure("Lion's Pride", f"{_IMG}/2024/01/2023_2024_loops_pins_Lions_Pride.jpg", True),
        Adventure(
            "King of the Jungle",
            f"{_IMG}/2024/01/2023_2024_loops_pins_King_of_The_Jungle.jpg",
            True,
        ),
        Adventure("Mountain Lion", f"{_IMG}/2024/01/2023_2024_loops_pins_Mountain_Lion.jpg", True),
        Adventure("Bobcat", f"{_IMG}/2024/01/2023_2024_loops_pins_Lion_Bobcat.jpg", True),
        # Elective
        Adventure(
            "Build It Up, Knock It Down",
            f"{_IMG}/2024/03/2023_2024_loops_pins_Build_It_Up_Knock_It_Down-1.jpg",
            False,
        ),
        Adventure(
            "Champions for Nature",
            f"{_IMG}/2024/03/2023_2024_loops_pins_Champions_of_Nature-1.jpg",
            False,
        ),
        Adventure("Count On Me", f"{_IMG}/2024/03/2023_2024_loops_pins_Count_On_Me-1.jpg", False),
        Adventure(
            "Everyday Tech", f"{_IMG}/2024/03/2023_2024_loops_pins_Everyday_Tech-1.jpg", False
        ),
        Adventure(
            "Gizmos and Gadgets",
            f"{_IMG}/2024/01/2023_2024_loops_pins_Gizmos_and_Gadgets.jpg",
            False,
        ),
        Adventure("Go Fish", f"{_IMG}/2024/01/2023_2024_loops_pins_Go_Fish.jpg", False),
        Adventure(
            "I'll Do It Myself", f"{_IMG}/2024/01/2023_2024_loops_pins_Ill_Do_It_Myself.jpg", False
        ),
        Adventure("Let's Camp", f"{_IMG}/2024/01/2023_2024_loops_pins_Lets_Camp-1.jpg", False),
        Adventure("On a Roll", f"{_IMG}/2024/01/2023_2024_loops_pins_On_a_Roll.jpg", False),
        Adventure("On Your Mark", f"{_IMG}/2024/01/2023_2024_loops_pins_On_Your_Mark.jpg", False),
        Adventure("Pick My Path", f"{_IMG}/2024/03/2023_2024_loops_pins_Pick_My_Path.jpg", False),
        Adventure("Race Time", f"{_IMG}/2024/01/2023_2024_loops_pins_Race_Time-1.jpg", False),
        Adventure(
            "Ready, Set, Grow", f"{_IMG}/2024/01/2023_2024_loops_pins_Ready_Set_Grow.jpg", False
        ),
        Adventure("Time to Swim", f"{_IMG}/2024/01/2023_2024_loops_pins_Time_to_Swim.jpg", False),
        # Shooting sports
        Adventure("Archery", f"{_IMG}/2024/08/2023_2024_loops_pins_Archery.jpg", False),
        Adventure("Slingshot", f"{_IMG}/2024/08/2023_2024_loops_pins_Slingshot.jpg", False),
    ],
    "tiger": [
        # Required (6)
        Adventure("Tiger Bites", f"{_IMG}/2024/04/2023_2024_loops_pins_Tiger_Bites.jpg", True),
        Adventure("Tiger's Roar", f"{_IMG}/2024/04/2023_2024_loops_pins_Tigers-Roar.jpg", True),
        Adventure("Tiger Circles", f"{_IMG}/2024/04/2023_2024_loops_pins_Tiger_Circles.jpg", True),
        Adventure("Team Tiger", f"{_IMG}/2024/04/2023_2024_loops_pins_Team_Tiger.jpg", True),
        Adventure(
            "Tigers in the Wild",
            f"{_IMG}/2024/04/2023_2024_loops_pins_Tigers_in_the_Wild.jpg",
            True,
        ),
        Adventure("Bobcat", f"{_IMG}/2024/04/2023_2024_loops_pins_Tiger-Bobcat.jpg", True),
        # Elective
        Adventure(
            "Champions for Nature",
            f"{_IMG}/2024/01/2023_2024_loops_pins_Champions_of_Nature.jpg",
            False,
        ),
        Adventure(
            "Curiosity, Intrigue and Magical Mysteries",
            f"{_IMG}/2024/01/2023_2024_loops_pins_Curiosity_Intrigue_and_Magical_Mysteries.jpg",
            False,
        ),
        Adventure(
            "Designed by Tiger",
            f"{_IMG}/2024/01/2023_2024_loops_pins_Designed_by_Tiger.jpg",
            False,
        ),
        Adventure("Fish On", f"{_IMG}/2024/01/2023_2024_loops_pins_Fish_On.jpg", False),
        Adventure(
            "Floats and Boats", f"{_IMG}/2024/01/2023_2024_loops_pins_Floats_and_Boats.jpg", False
        ),
        Adventure("Good Knights", f"{_IMG}/2024/01/2023_2024_loops_pins_Good_Knights.jpg", False),
        Adventure("Let's Camp", f"{_IMG}/2024/01/2023_2024_loops_pins_Lets_Camp.jpg", False),
        Adventure("Race Time", f"{_IMG}/2024/01/2023_2024_loops_pins_Race_Time.jpg", False),
        Adventure(
            "Rolling Tigers", f"{_IMG}/2024/01/2023_2024_loops_pins_Rolling_Tigers.jpg", False
        ),
        Adventure(
            "Safe and Smart",
            f"{_IMG}/2024/01/2023_2024_loops_pins_Tiger_Safe_and_Smart.jpg",
            False,
        ),
        Adventure(
            "Sky is the Limit", f"{_IMG}/2024/01/2023_2024_loops_pins_Sky_is_the_Limit.jpg", False
        ),
        Adventure(
            "Stories in Shapes",
            f"{_IMG}/2024/01/2023_2024_loops_pins_Stories_in_Shapes.jpg",
            False,
        ),
        Adventure(
            "Summertime Fun", f"{_IMG}/2024/01/2023_2024_loops_pins_Summertime_Fun.jpg", False
        ),
        Adventure(
            "Tech All Around", f"{_IMG}/2024/02/2023_2024_loops_pins_Tech_All_Around.jpg", False
        ),
        Adventure("Tiger Tag", f"{_IMG}/2024/01/2023_2024_loops_pins_Tigers_Tag.jpg", False),
        Adventure(
            "Tiger-iffic!", f"{_IMG}/2024/01/2023_2024_loops_pins_Tiger_rrrrific.jpg", False
        ),
        Adventure(
            "Tigers in the Water",
            f"{_IMG}/2024/03/2023_2024_loops_pins_Tigers_in_the_Water.jpg",
            False,
        ),
        # Shooting sports
        Adventure("Archery", f"{_IMG}/2024/08/2023_2024_loops_pins_Archery-1.jpg", False),
        Adventure("Slingshot", f"{_IMG}/2024/08/2023_2024_loops_pins_Slingshot-1.jpg", False),
        Adventure("BB", f"{_IMG}/2024/08/2023_2024_loops_pins_BB_Guns.jpg", False),
    ],
    "wolf": [
        # Required (6)
        Adventure(
            "Running With the Pack",
            f"{_IMG}/2024/04/2023_2024_loops_pins_Running_With_the_Pack.jpg",
            True,
        ),
        Adventure(
            "Safety in Numbers", f"{_IMG}/2024/04/2023_2024_loops_pins_Safety_in_Numbers.jpg", True
        ),
        Adventure("Footsteps", f"{_IMG}/2024/04/2023_2024_loops_pins_Footsteps.jpg", True),
        Adventure("Council Fire", f"{_IMG}/2024/04/2023_2024_loops_pins_Council_Fire.jpg", True),
        Adventure(
            "Paws on the Path", f"{_IMG}/2024/04/2023_2024_loops_pins_Paws_on_the_Path.jpg", True
        ),
        Adventure("Bobcat", f"{_IMG}/2024/04/2023_2024_loops_pins_Wolf_Bobcat.jpg", True),
        # Elective
        Adventure(
            "A Wolf Goes Fishing",
            f"{_IMG}/2023/11/2023_2024_loops_pins_A_Wolf_Goes_Fishing-1.jpg",
            False,
        ),
        Adventure(
            "Adventures in Coins",
            f"{_IMG}/2024/02/2023_2024_loops_pins_Adventures_in_Coins.jpg",
            False,
        ),
        Adventure(
            "Air of the Wolf", f"{_IMG}/2024/02/2023_2024_loops_pins_Air_of_the_Wolf.jpg", False
        ),
        Adventure(
            "Champions for Nature",
            f"{_IMG}/2024/02/2023_2024_loops_pins_Champions_of_Nature.jpg",
            False,
        ),
        Adventure(
            "Code of the Wolf", f"{_IMG}/2024/02/2023_2024_loops_pins_Code_of_the_Wolf.jpg", False
        ),
        Adventure(
            "Computing Wolves", f"{_IMG}/2023/11/2023_2024_loops_pins_Computing_Wolves.jpg", False
        ),
        Adventure(
            "Cubs Who Care", f"{_IMG}/2023/11/2023_2024_loops_pins_Cubs_Who_Care.jpg", False
        ),
        Adventure(
            "Digging in the Past",
            f"{_IMG}/2023/11/2023_2024_loops_pins_Digging_Into_the_Past.jpg",
            False,
        ),
        Adventure(
            "Finding Your Way", f"{_IMG}/2023/11/2023_2024_loops_pins_Finding_Your_Way.jpg", False
        ),
        Adventure("Germs Alive!", f"{_IMG}/2023/11/2023_2024_loops_pins_Germs_Alive.jpg", False),
        Adventure("Let's Camp", f"{_IMG}/2024/02/2023_2024_loops_pins_Lets_Camp.jpg", False),
        Adventure(
            "Paws for Water", f"{_IMG}/2023/11/2023_2024_loops_pins_Paws_For_Water.jpg", False
        ),
        Adventure(
            "Paws of Skill", f"{_IMG}/2023/11/2023_2024_loops_pins_Paws_of_Skill.jpg", False
        ),
        Adventure(
            "Pedal With the Pack",
            f"{_IMG}/2023/11/2023_2024_loops_pins_Pedal_With_the_Pack.jpg",
            False,
        ),
        Adventure("Race Time", f"{_IMG}/2023/11/2023_2024_loops_pins_Race_Time.jpg", False),
        Adventure(
            "Spirit of the Water",
            f"{_IMG}/2023/11/2023_2024_loops_pins_Spirit_of_the_Water.jpg",
            False,
        ),
        Adventure(
            "Summertime Fun", f"{_IMG}/2023/11/2023_2024_loops_pins_Summertime_Fun.jpg", False
        ),
        # Shooting sports
        Adventure("Archery", f"{_IMG}/2024/08/2023_2024_loops_pins_Archery-2.jpg", False),
        Adventure("Slingshot", f"{_IMG}/2024/08/2023_2024_loops_pins_Slingshot-2.jpg", False),
        Adventure("BB", f"{_IMG}/2024/08/2023_2024_loops_pins_BB_Guns-1.jpg", False),
    ],
    "bear": [
        # Required (6)
        Adventure("Bear Strong", f"{_IMG}/2024/02/2023_2024_loops_pins_Bear_Strong.jpg", True),
        Adventure("Standing Tall", f"{_IMG}/2024/01/2023_2024_loops_pins_Standing_Tall.jpg", True),
        Adventure("Fellowship", f"{_IMG}/2024/02/2023_2024_loops_pins_Fellowship.jpg", True),
        Adventure(
            "Paws for Action", f"{_IMG}/2024/01/2023_2024_loops_pins_Paws_For_Action.jpg", True
        ),
        Adventure("Bear Habitat", f"{_IMG}/2024/02/2023_2024_loops_pins_Bear_Habitat.jpg", True),
        Adventure("Bobcat", f"{_IMG}/2024/01/2023_2024_loops_pins_Bear_Bobcat-1.jpg", True),
        # Elective
        Adventure(
            "A Bear Goes Fishing",
            f"{_IMG}/2024/01/2023_2024_loops_pins_A_Bear_Goes_Fishing.jpg",
            False,
        ),
        Adventure(
            "Balancing Bears", f"{_IMG}/2024/01/2023_2024_loops_pins_Balancing_Bears.jpg", False
        ),
        Adventure(
            "Baloo the Builder",
            f"{_IMG}/2024/01/2023_2024_loops_pins_Baloo_the_Builder.jpg",
            False,
        ),
        Adventure("Bears Afloat", f"{_IMG}/2024/01/2023_2024_loops_pins_Bears_Afloat.jpg", False),
        Adventure(
            "Bears on Bikes", f"{_IMG}/2024/01/2023_2024_loops_pins_Bears_on_Bikes.jpg", False
        ),
        Adventure(
            "Champions for Nature",
            f"{_IMG}/2024/01/2023_2024_loops_pins_Champions_of_Nature-1.jpg",
            False,
        ),
        Adventure("Chef Tech", f"{_IMG}/2024/01/2023_2024_loops_pins_Chef_Tech.jpg", False),
        Adventure("Critter Care", f"{_IMG}/2024/01/2023_2024_loops_pins_Critter_Care.jpg", False),
        Adventure("Forensics", f"{_IMG}/2024/01/2023_2024_loops_pins_Forensics.jpg", False),
        Adventure("Let's Camp", f"{_IMG}/2024/01/2023_2024_loops_pins_Lets_Camp-2.jpg", False),
        Adventure(
            "Marble Madness", f"{_IMG}/2024/01/2023_2024_loops_pins_Marble_Madness.jpg", False
        ),
        Adventure("Race Time", f"{_IMG}/2024/01/2023_2024_loops_pins_Race_Time-2.jpg", False),
        Adventure(
            "Roaring Laughter", f"{_IMG}/2024/01/2023_2024_loops_pins_Roaring_Laughter.jpg", False
        ),
        Adventure("Salmon Run", f"{_IMG}/2024/01/2023_2024_loops_pins_Salmon_Run.jpg", False),
        Adventure(
            "Summertime Fun", f"{_IMG}/2024/01/2023_2024_loops_pins_Summertime_Fun-1.jpg", False
        ),
        Adventure(
            "Super Science", f"{_IMG}/2024/01/2023_2024_loops_pins_Super_Science.jpg", False
        ),
        Adventure("Whittling", f"{_IMG}/2024/01/2023_2024_loops_pins_Whittling.jpg", False),
        # Shooting sports
        Adventure("Archery", f"{_IMG}/2024/08/2023_2024_loops_pins_Archery-3.jpg", False),
        Adventure("Slingshot", f"{_IMG}/2024/08/2023_2024_loops_pins_Slingshot-3.jpg", False),
        Adventure("BB", f"{_IMG}/2024/08/2023_2024_loops_pins_BB_Guns-2.jpg", False),
    ],
    "webelos": [
        # Required (6)
        Adventure("Bobcat", f"{_IMG}/2024/01/2023_2024_loops_pins_Webelos_Bobcat_edit.jpg", True),
        Adventure(
            "Stronger, Faster, Higher",
            f"{_IMG}/2024/01/2023_2024_loops_pins_Stronger_Faster_Higher.jpg",
            True,
        ),
        Adventure("My Safety", f"{_IMG}/2024/02/2023_2024_loops_pins_My_Safety.jpg", True),
        Adventure("My Family", f"{_IMG}/2024/01/2023_2024_loops_pins_My_Family.jpg", True),
        Adventure("My Community", f"{_IMG}/2024/01/2023_2024_loops_pins_My_Community.jpg", True),
        Adventure(
            "Webelos Walkabout", f"{_IMG}/2024/01/2023_2024_loops_pins_Webelos_Walkabout.jpg", True
        ),
        # Elective
        Adventure("Aquanaut", f"{_IMG}/2024/01/2023_2024_loops_pins_Aquanaut.jpg", False),
        Adventure(
            "Art Explosion", f"{_IMG}/2024/01/2023_2024_loops_pins_Art_Explosion.jpg", False
        ),
        Adventure(
            "Aware and Care", f"{_IMG}/2024/01/2023_2024_loops_pins_Aware_and_Care.jpg", False
        ),
        Adventure("Build It", f"{_IMG}/2024/01/2023_2024_loops_pins_Build_It.jpg", False),
        Adventure(
            "Catch the Big One",
            f"{_IMG}/2024/01/2023_2024_loops_pins_Catch_the_Big_One.jpg",
            False,
        ),
        Adventure(
            "Champions for Nature",
            f"{_IMG}/2024/01/2023_2024_loops_pins_Champions_of_Nature-2.jpg",
            False,
        ),
        Adventure("Chef's Knife", f"{_IMG}/2024/01/2023_2024_loops_pins_ChefsKnife.jpg", False),
        Adventure("Earth Rocks", f"{_IMG}/2024/01/2023_2024_loops_pins_Earth_Rocks.jpg", False),
        Adventure("Let's Camp", f"{_IMG}/2024/01/2023_2024_loops_pins_Lets_Camp-3.jpg", False),
        Adventure(
            "Math on the Trail",
            f"{_IMG}/2024/01/2023_2024_loops_pins_Math_on_the_Trail.jpg",
            False,
        ),
        Adventure(
            "Modular Design", f"{_IMG}/2024/05/2023_2024_loops_pins_Modular_Design.jpg", False
        ),
        Adventure(
            "Paddle Onward", f"{_IMG}/2024/01/2023_2024_loops_pins_Paddle_Onward.jpg", False
        ),
        Adventure("Pedal Away", f"{_IMG}/2024/01/2023_2024_loops_pins_Pedal_Away.jpg", False),
        Adventure("Race Time", f"{_IMG}/2024/01/2023_2024_loops_pins_Race_Time-3.jpg", False),
        Adventure(
            "Summertime Fun", f"{_IMG}/2024/01/2023_2024_loops_pins_Summertime_Fun-2.jpg", False
        ),
        Adventure(
            "Tech on the Trail",
            f"{_IMG}/2024/01/2023_2024_loops_pins_Tech_on_the_Trail.jpg",
            False,
        ),
        Adventure("Yo-Yo", f"{_IMG}/2024/01/2023_2024_loops_pins_Yo_Yo.jpg", False),
        # Shooting sports
        Adventure("Archery", f"{_IMG}/2024/08/2023_2024_loops_pins_Archery-4.jpg", False),
        Adventure("Slingshot", f"{_IMG}/2024/08/2023_2024_loops_pins_Slingshot-4.jpg", False),
        Adventure("BB Gun", f"{_IMG}/2024/08/2023_2024_loops_pins_BB_Guns-3.jpg", False),
    ],
    "arrow of light": [
        # Required (6)
        Adventure(
            "Personal Fitness", f"{_IMG}/2024/04/2023_2024_loops_pins_Personal_Fitness.jpg", True
        ),
        Adventure("First Aid", f"{_IMG}/2024/04/2023_2024_loops_pins_First_Aid.jpg", True),
        Adventure("Duty to God", f"{_IMG}/2024/04/2023_2024_loops_pins_AOL_Duty_to_God.jpg", True),
        Adventure("Citizenship", f"{_IMG}/2024/04/2023_2024_loops_pins_Citizenship.jpg", True),
        Adventure(
            "Outdoor Adventurer",
            f"{_IMG}/2024/04/2023_2024_loops_pins_AOL_Outdoor_Adventurer.jpg",
            True,
        ),
        Adventure("Bobcat", f"{_IMG}/2024/04/2023_2024_loops_pins_AOL_Bobcat.jpg", True),
        # Elective
        Adventure(
            "Champions for Nature",
            f"{_IMG}/2024/05/2023_2024_loops_pins_Champions_of_Nature.jpg",
            False,
        ),
        Adventure("Cycling", f"{_IMG}/2024/05/2023_2024_loops_pins_Cycling.jpg", False),
        Adventure("Engineer", f"{_IMG}/2024/05/2023_2024_loops_pins_Engineering.jpg", False),
        Adventure("Estimations", f"{_IMG}/2024/05/2023_2024_loops_pins_Estimations.jpg", False),
        Adventure("Fishing", f"{_IMG}/2024/05/2023_2024_loops_pins_Fishing.jpg", False),
        Adventure(
            "High Tech Outdoors",
            f"{_IMG}/2024/05/2023_2024_loops_pins_High_Tech_Outdoors.jpg",
            False,
        ),
        Adventure(
            "Into the Wild", f"{_IMG}/2024/05/2023_2024_loops_pins_Into_the_Wild.jpg", False
        ),
        Adventure(
            "Into the Woods", f"{_IMG}/2024/05/2023_2024_loops_pins_Into_the_Woods.jpg", False
        ),
        Adventure("Knife Safety", f"{_IMG}/2024/05/2023_2024_loops_pins_Knife_Safety.jpg", False),
        Adventure("Paddle Craft", f"{_IMG}/2024/05/2023_2024_loops_pins_Paddle_Craft.jpg", False),
        Adventure("Race Time", f"{_IMG}/2024/05/2023_2024_loops_pins_Race_Time.jpg", False),
        Adventure(
            "Summertime Fun", f"{_IMG}/2024/05/2023_2024_loops_pins_Summertime_Fun.jpg", False
        ),
        Adventure("Swimming", f"{_IMG}/2024/05/2023_2024_loops_pins_Swimming.jpg", False),
        # Shooting sports
        Adventure("Archery", f"{_IMG}/2024/08/2023_2024_loops_pins_Archery-5.jpg", False),
        Adventure("Slingshot", f"{_IMG}/2024/08/2023_2024_loops_pins_Slingshot-5.jpg", False),
        Adventure("BB", f"{_IMG}/2024/08/2023_2024_loops_pins_BB_Guns-4.jpg", False),
    ],
}

# Rank aliases used in Scoutbook CSV exports → canonical rank keys
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
        'Fun on the Run Adventure' → 'fun on the run'
        'Archery (Lion) Adventure' → 'archery'
        'Bobcat (Wolf) Adventure'  → 'bobcat'
        'BB (Bears) Adventure'     → 'bb'
        'BB Gun (Webelos) Adventure' → 'bb gun'
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
