"""Bagging guide PDF generator.

Produces a continuous checklist PDF showing each scout's adventures with
loop/pin images, designed to help volunteers bag the correct items.
Scouts flow continuously to minimize paper usage.
"""

from __future__ import annotations

import contextlib
import hashlib
import tempfile
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from src.core.adventure_data import Adventure, find_adventure
from src.core.label_generator import ScoutRecord

PAGE_WIDTH, PAGE_HEIGHT = LETTER

# Layout constants
MARGIN_LEFT = 0.5 * inch
MARGIN_RIGHT = 0.5 * inch
MARGIN_TOP = 0.5 * inch
MARGIN_BOTTOM = 0.5 * inch

USABLE_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT

# Per-item row layout
IMAGE_SIZE = 0.45 * inch
ROW_HEIGHT = 0.5 * inch
CHECKBOX_SIZE = 10
TEXT_LEFT = MARGIN_LEFT + CHECKBOX_SIZE + 6 + IMAGE_SIZE + 6

# Scout header height (name + sub + divider)
HEADER_HEIGHT = 36

# Space between scouts
SCOUT_GAP = 14

# Fonts
HEADER_FONT_SIZE = 12
SUBHEADER_FONT_SIZE = 9
ITEM_FONT_SIZE = 9
TAG_FONT_SIZE = 7


@dataclass(frozen=True)
class BaggingGuideResult:
    scout_count: int
    page_count: int
    output_path: str


def _cache_dir() -> Path:
    """Return (and create) a cache directory for downloaded adventure images."""
    cache = Path(tempfile.gettempdir()) / "scout_advancement_images"
    cache.mkdir(exist_ok=True)
    return cache


def _download_image(url: str) -> Path | None:
    """Download an image to the cache directory. Returns the local path or None."""
    cache = _cache_dir()
    url_hash = hashlib.sha256(url.encode()).hexdigest()[:16]
    allowed = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    suffix = Path(url).suffix.lower()
    if suffix not in allowed:
        suffix = ".jpg"
    local_path = cache / f"{url_hash}{suffix}"

    if local_path.exists():
        return local_path

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ScoutAdvancement/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:  # noqa: S310
            data = resp.read()
        local_path.write_bytes(data)
        return local_path
    except (urllib.error.URLError, OSError):
        return None


def _new_page(c: canvas.Canvas) -> float:
    """Start a new page and return the starting y position."""
    c.showPage()
    return PAGE_HEIGHT - MARGIN_TOP


def _draw_scout_header(
    c: canvas.Canvas,
    y: float,
    scout: ScoutRecord,
    item_count: int,
) -> float:
    """Draw the scout name header. Returns the new y position."""
    den_display = scout.den_type.title()
    header = f"{scout.first} {scout.last}"
    plural = "s" if item_count != 1 else ""
    sub = f"{den_display} (Den {scout.den_num}) \u2014 {item_count} item{plural}"

    c.setFont("Helvetica-Bold", HEADER_FONT_SIZE)
    c.drawString(MARGIN_LEFT, y, header)

    # Item count on the right side
    c.setFont("Helvetica", SUBHEADER_FONT_SIZE)
    c.setFillColor(colors.HexColor("#555555"))
    count_width = c.stringWidth(sub, "Helvetica", SUBHEADER_FONT_SIZE)
    c.drawString(PAGE_WIDTH - MARGIN_RIGHT - count_width, y + 2, sub)
    c.setFillColor(colors.black)
    y -= HEADER_FONT_SIZE + 4

    # Divider line
    c.setStrokeColor(colors.HexColor("#CCCCCC"))
    c.setLineWidth(0.5)
    c.line(MARGIN_LEFT, y, PAGE_WIDTH - MARGIN_RIGHT, y)
    y -= 6

    return y


def _draw_item_row(
    c: canvas.Canvas,
    y: float,
    item_name: str,
    adventure: Adventure | None,
    image_path: Path | None,
) -> float:
    """Draw a single adventure item row with checkbox, image, and name."""
    row_top = y

    # Checkbox — vertically centered in the row
    checkbox_y = row_top - (ROW_HEIGHT + CHECKBOX_SIZE) / 2
    c.setStrokeColor(colors.black)
    c.setLineWidth(0.75)
    c.rect(MARGIN_LEFT, checkbox_y, CHECKBOX_SIZE, CHECKBOX_SIZE, stroke=1, fill=0)

    # Image — vertically centered in the row
    img_x = MARGIN_LEFT + CHECKBOX_SIZE + 6
    img_y = row_top - (ROW_HEIGHT + IMAGE_SIZE) / 2
    if image_path is not None:
        with contextlib.suppress(Exception):
            c.drawImage(
                str(image_path),
                img_x,
                img_y,
                width=IMAGE_SIZE,
                height=IMAGE_SIZE,
                preserveAspectRatio=True,
                mask="auto",
            )

    # Adventure name — vertically centered
    c.setFont("Helvetica", ITEM_FONT_SIZE)
    c.setFillColor(colors.black)
    text_y = row_top - ROW_HEIGHT / 2 + ITEM_FONT_SIZE / 3

    # Show required/elective tag inline
    if adventure is not None:
        tag = " (Req)" if adventure.required else " (Elc)"
        c.drawString(TEXT_LEFT, text_y, item_name)
        tag_color = (
            colors.HexColor("#2E7D32") if adventure.required else colors.HexColor("#1565C0")
        )
        name_width = c.stringWidth(item_name, "Helvetica", ITEM_FONT_SIZE)
        c.setFont("Helvetica-Oblique", TAG_FONT_SIZE)
        c.setFillColor(tag_color)
        c.drawString(TEXT_LEFT + name_width + 4, text_y, tag)
        c.setFillColor(colors.black)
    else:
        c.drawString(TEXT_LEFT, text_y, item_name)

    return row_top - ROW_HEIGHT


def _space_needed_for_scout(scout: ScoutRecord) -> float:
    """Minimum space needed: header + at least 1 item row."""
    return HEADER_HEIGHT + ROW_HEIGHT


def generate_bagging_guide(
    scouts: list[ScoutRecord],
    output_path: str,
    *,
    download_images: bool = True,
) -> BaggingGuideResult:
    """Generate a bagging guide PDF for the given scouts.

    Scouts flow continuously across pages to minimize paper usage.

    Args:
        scouts: List of scout records (from read_advancements).
        output_path: Path for the output PDF.
        download_images: If True, download adventure images from scouting.org.
            Set to False for faster generation without images.

    Returns:
        BaggingGuideResult with counts and output path.

    Raises:
        OSError: If the output file cannot be written.
    """
    resolved = Path(output_path).resolve()
    if resolved.suffix.lower() != ".pdf":
        raise OSError(f"Output path must end with .pdf: {resolved.name}")
    parent = resolved.parent
    if not parent.exists():
        raise OSError(f"Output directory does not exist: {parent}")
    output_path = str(resolved)

    c = canvas.Canvas(output_path, pagesize=LETTER)
    c.setTitle("Cub Scout Bagging Guide")

    page_count = 0
    y = MARGIN_BOTTOM  # Force a new page on first scout

    for scout_idx, scout in enumerate(scouts):
        # Add gap between scouts (not before the first)
        if scout_idx > 0:
            y -= SCOUT_GAP

        # Check if we have room for at least the header + 1 item
        if y < MARGIN_BOTTOM + _space_needed_for_scout(scout):
            y = _new_page(c) if page_count > 0 else PAGE_HEIGHT - MARGIN_TOP
            page_count += 1

        y = _draw_scout_header(c, y, scout, len(scout.items))

        for item_name in sorted(scout.items):
            if y < MARGIN_BOTTOM + ROW_HEIGHT:
                y = _new_page(c)
                page_count += 1

            adventure = find_adventure(item_name, scout.den_type)
            image_path = None
            if download_images and adventure is not None:
                image_path = _download_image(adventure.image_url)

            y = _draw_item_row(c, y, item_name, adventure, image_path)

    if scouts:
        c.save()

    return BaggingGuideResult(
        scout_count=len(scouts),
        page_count=page_count,
        output_path=output_path,
    )
