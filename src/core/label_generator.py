"""
Core label generation logic.

Reads Scoutbook CSV exports and produces Avery 6427 shipping label PDFs
(2" x 4", 10 per sheet on US Letter).
"""

from __future__ import annotations

import csv
from collections import OrderedDict
from dataclasses import dataclass

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


# --- Avery 6427 / 5163 Shipping Label Layout (US Letter) ---
PAGE_WIDTH, PAGE_HEIGHT = LETTER  # 8.5" x 11"

LABEL_WIDTH = 4.0 * inch
LABEL_HEIGHT = 2.0 * inch
COLUMNS = 2
ROWS = 5
LABELS_PER_PAGE = COLUMNS * ROWS

TOP_MARGIN = 0.5 * inch
LEFT_MARGIN = 0.15625 * inch  # 5/32"
H_GAP = 0.1875 * inch  # 3/16" gap between columns
V_GAP = 0.0  # no vertical gap

# Text inset from label edge
PAD_LEFT = 0.15 * inch
PAD_TOP = 0.15 * inch
PAD_RIGHT = 0.15 * inch
PAD_BOTTOM = 0.1 * inch

# Font sizes
NAME_FONT_SIZE = 11
AWARDS_FONT_SIZE = 8

# Den type sort order
DEN_TYPE_ORDER: dict[str, int] = {
    "lion": 1,
    "lions": 1,
    "tiger": 2,
    "tigers": 2,
    "wolf": 3,
    "wolves": 3,
    "bear": 4,
    "bears": 4,
    "webelos": 5,
    "webelos 2": 6,
    "arrow of light": 6,
    "aol": 6,
}

REQUIRED_COLUMNS = {"First Name", "Last Name", "Den Type", "Den Number", "Item Name"}


class CSVReadError(Exception):
    """Raised when a CSV file cannot be read."""


class CSVColumnError(Exception):
    """Raised when a CSV file is missing required columns."""


@dataclass(frozen=True)
class ScoutRecord:
    first: str
    last: str
    den_type: str
    den_num: str
    items: tuple[str, ...]


@dataclass(frozen=True)
class GenerationResult:
    label_count: int
    page_count: int
    output_path: str


def read_advancements(input_files: list[str]) -> list[ScoutRecord]:
    """Read CSV files and return sorted list of scout records.

    Raises:
        CSVReadError: If a file cannot be found or read.
        CSVColumnError: If a file is missing required columns.
    """
    scouts: OrderedDict[tuple[str, ...], dict[str, object]] = OrderedDict()

    for input_file in input_files:
        try:
            with open(input_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames is not None:
                    missing = REQUIRED_COLUMNS - set(reader.fieldnames)
                    if missing:
                        raise CSVColumnError(
                            f"Missing columns in '{input_file}': {', '.join(sorted(missing))}"
                        )
                for row in reader:
                    first = row["First Name"].strip()
                    last = row["Last Name"].strip()
                    den_type = row["Den Type"].strip()
                    den_num = row["Den Number"].strip()
                    item = row["Item Name"].strip()

                    key = (first, last, den_type, den_num)
                    if key not in scouts:
                        scouts[key] = {
                            "first": first,
                            "last": last,
                            "den_type": den_type,
                            "den_num": den_num,
                            "items": [],
                        }
                    scouts[key]["items"].append(item)  # type: ignore[union-attr]
        except FileNotFoundError:
            raise CSVReadError(f"Could not find '{input_file}'")
        except KeyError as e:
            raise CSVColumnError(f"Missing column {e} in '{input_file}'")

    def sort_key(record: dict[str, object]) -> tuple[int, str, str]:
        den = str(record["den_type"]).lower()
        rank = DEN_TYPE_ORDER.get(den, 999)
        return (rank, str(record["last"]).lower(), str(record["first"]).lower())

    sorted_scouts = sorted(scouts.values(), key=sort_key)
    return [
        ScoutRecord(
            first=str(s["first"]),
            last=str(s["last"]),
            den_type=str(s["den_type"]),
            den_num=str(s["den_num"]),
            items=tuple(s["items"]),  # type: ignore[arg-type]
        )
        for s in sorted_scouts
    ]


def _label_origin(index: int) -> tuple[float, float]:
    """Return (x, y) of the top-left corner of label at the given index (0-9)."""
    col = index % COLUMNS
    row = index // COLUMNS
    x = LEFT_MARGIN + col * (LABEL_WIDTH + H_GAP)
    y = PAGE_HEIGHT - TOP_MARGIN - row * (LABEL_HEIGHT + V_GAP)
    return x, y


def _wrap_text(
    c: canvas.Canvas,
    text: str,
    max_width: float,
    font_name: str,
    font_size: float,
) -> list[str]:
    """Word-wrap text to fit within max_width."""
    words = text.split()
    lines: list[str] = []
    current_line = ""
    for word in words:
        test = f"{current_line} {word}".strip() if current_line else word
        if c.stringWidth(test, font_name, font_size) <= max_width:
            current_line = test
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines


def _draw_label(c: canvas.Canvas, x: float, y: float, scout: ScoutRecord) -> None:
    """Draw a single scout label at position (x, y) = top-left of label."""
    text_x = x + PAD_LEFT
    usable_width = LABEL_WIDTH - PAD_LEFT - PAD_RIGHT

    den_display = scout.den_type.title()
    name_line = f"{scout.first} {scout.last} [{den_display} ({scout.den_num})]"

    c.setFont("Helvetica-Bold", NAME_FONT_SIZE)
    name_y = y - PAD_TOP - NAME_FONT_SIZE
    c.drawString(text_x, name_y, name_line)

    awards_text = ", ".join(scout.items)
    c.setFont("Helvetica", AWARDS_FONT_SIZE)
    lines = _wrap_text(c, awards_text, usable_width, "Helvetica", AWARDS_FONT_SIZE)

    line_height = AWARDS_FONT_SIZE + 2
    awards_start_y = name_y - line_height
    label_bottom = y - LABEL_HEIGHT + PAD_BOTTOM

    for i, line in enumerate(lines):
        line_y = awards_start_y - i * line_height
        if line_y < label_bottom:
            break
        c.drawString(text_x, line_y, line)


def generate_pdf(scouts: list[ScoutRecord], output_path: str) -> GenerationResult:
    """Generate the label PDF and return results.

    Raises:
        OSError: If the output file cannot be written.
    """
    c = canvas.Canvas(output_path, pagesize=LETTER)
    c.setTitle("Cub Scout Advancement Labels")

    for i, scout in enumerate(scouts):
        page_index = i % LABELS_PER_PAGE
        if i > 0 and page_index == 0:
            c.showPage()

        x, y = _label_origin(page_index)
        _draw_label(c, x, y, scout)

    c.save()
    page_count = (len(scouts) + LABELS_PER_PAGE - 1) // LABELS_PER_PAGE if scouts else 0

    return GenerationResult(
        label_count=len(scouts),
        page_count=page_count,
        output_path=output_path,
    )
