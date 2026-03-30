#!/usr/bin/env python3
"""Fetch adventure data from scouting.org WordPress API.

Scrapes adventure names and loop/pin image URLs for each Cub Scout rank.
Run this script when the BSA program year changes to refresh the adventure
data in src/core/adventure_data.py.

Usage:
    python scripts/fetch_adventures.py
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from dataclasses import asdict, dataclass

BASE_URL = "https://www.scouting.org/wp-json/wp/v2/pages"

RANK_SLUGS = {
    "lion": "lion",
    "tiger": "tiger",
    "wolf": "wolf",
    "bear": "bear",
    "webelos": "webelos",
    "arrow of light": "arrow-of-light",
}


@dataclass
class AdventureEntry:
    name: str
    image_url: str
    required: bool


def fetch_page_content(slug: str) -> str:
    """Fetch the rendered HTML content for a rank page via WP REST API."""
    url = f"{BASE_URL}?slug={slug}&_fields=content"
    req = urllib.request.Request(url, headers={"User-Agent": "ScoutAdvancement/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310
        data = json.loads(resp.read().decode("utf-8"))
    if not data:
        return ""
    return data[0].get("content", {}).get("rendered", "")


def parse_adventures(html: str) -> list[AdventureEntry]:
    """Parse adventure names and image URLs from the rendered HTML."""
    adventures: list[AdventureEntry] = []

    # Match image tags followed by adventure names in headings or figcaptions
    # Pattern: <img ... src="URL" ...> ... adventure name
    img_pattern = re.compile(
        r'<img[^>]+src="([^"]*loops_pins[^"]*)"[^>]*/?>',
        re.IGNORECASE,
    )
    # Adventure name in headings
    heading_pattern = re.compile(
        r"<h[2-4][^>]*>(.*?)</h[2-4]>",
        re.IGNORECASE | re.DOTALL,
    )

    # Find section boundary for required vs elective
    elective_start = html.lower().find("elective")

    images = list(img_pattern.finditer(html))
    headings = list(heading_pattern.finditer(html))

    # Simple approach: pair images with nearby heading text
    for img_match in images:
        img_url = img_match.group(1)
        img_pos = img_match.start()

        # Find the closest heading after this image
        name = ""
        for h_match in headings:
            if h_match.start() > img_pos:
                # Strip HTML tags from heading
                raw = re.sub(r"<[^>]+>", "", h_match.group(1)).strip()
                if raw and len(raw) > 2:
                    name = raw
                    break

        # If no heading found after, try before
        if not name:
            for h_match in reversed(list(headings)):
                if h_match.start() < img_pos:
                    raw = re.sub(r"<[^>]+>", "", h_match.group(1)).strip()
                    if raw and len(raw) > 2:
                        name = raw
                        break

        if not name:
            # Try figcaption or alt text
            alt_match = re.search(r'alt="([^"]+)"', html[img_pos : img_pos + 500])
            if alt_match:
                name = alt_match.group(1).strip()

        if name:
            is_required = elective_start < 0 or img_pos < elective_start
            adventures.append(
                AdventureEntry(
                    name=name,
                    image_url=img_url,
                    required=is_required,
                )
            )

    return adventures


def main() -> None:
    """Fetch and display adventure data for all ranks."""
    all_data: dict[str, list[dict[str, object]]] = {}

    for rank, slug in RANK_SLUGS.items():
        print(f"Fetching {rank} (slug: {slug})...")
        try:
            html = fetch_page_content(slug)
            adventures = parse_adventures(html)
            all_data[rank] = [asdict(a) for a in adventures]
            print(f"  Found {len(adventures)} adventures")
            for adv in adventures:
                tag = "REQ" if adv.required else "ELC"
                print(f"    [{tag}] {adv.name}")
                print(f"          {adv.image_url}")
        except Exception as e:
            print(f"  ERROR: {e}", file=sys.stderr)
            all_data[rank] = []

    # Output JSON for easy copy-paste into adventure_data.py
    output_path = "scripts/adventure_data.json"
    with open(output_path, "w") as f:
        json.dump(all_data, f, indent=2)
    print(f"\nData written to {output_path}")
    print("Review and update src/core/adventure_data.py with the new data.")


if __name__ == "__main__":
    main()
