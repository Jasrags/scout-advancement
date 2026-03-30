"""
Core label generation logic.

Reads Scoutbook CSV exports and produces label PDFs for any supported
Avery label type (default: Avery 6427 shipping labels, 2" x 4", 10 per sheet).
"""

from __future__ import annotations

import csv
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path

from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from src.core.label_spec import DEFAULT_LABEL_SPEC, LabelSpec

# --- Page size ---
PAGE_WIDTH, PAGE_HEIGHT = LETTER  # 8.5" x 11"

# --- Legacy module-level constants (kept for backward compatibility) ---
LABEL_WIDTH = DEFAULT_LABEL_SPEC.label_width
LABEL_HEIGHT = DEFAULT_LABEL_SPEC.label_height
COLUMNS = DEFAULT_LABEL_SPEC.columns
ROWS = DEFAULT_LABEL_SPEC.rows
LABELS_PER_PAGE = DEFAULT_LABEL_SPEC.labels_per_page
TOP_MARGIN = DEFAULT_LABEL_SPEC.top_margin
LEFT_MARGIN = DEFAULT_LABEL_SPEC.left_margin
H_GAP = DEFAULT_LABEL_SPEC.h_gap
V_GAP = DEFAULT_LABEL_SPEC.v_gap

# Text inset from label edge
PAD_LEFT = 0.15 * inch
PAD_TOP = 0.15 * inch
PAD_RIGHT = 0.15 * inch
PAD_BOTTOM = 0.1 * inch

# Font sizes — scale down for smaller labels
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

# Field length limits to prevent malformed CSVs from overflowing labels
MAX_NAME_LEN = 50
MAX_DEN_TYPE_LEN = 30
MAX_ITEM_NAME_LEN = 100


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
            with open(input_file, encoding="utf-8") as f:
                reader = csv.DictReader(f)
                if reader.fieldnames is None:
                    raise CSVColumnError(f"Empty or unreadable CSV: '{input_file}'")
                missing = REQUIRED_COLUMNS - set(reader.fieldnames)
                if missing:
                    raise CSVColumnError(
                        f"Missing columns in '{input_file}': {', '.join(sorted(missing))}"
                    )
                for row in reader:
                    first = row["First Name"].strip()[:MAX_NAME_LEN]
                    last = row["Last Name"].strip()[:MAX_NAME_LEN]
                    den_type = row["Den Type"].strip()[:MAX_DEN_TYPE_LEN]
                    den_num = row["Den Number"].strip()[:MAX_DEN_TYPE_LEN]
                    item = row["Item Name"].strip()[:MAX_ITEM_NAME_LEN]

                    key = (first, last, den_type, den_num)
                    if key not in scouts:
                        scouts[key] = {
                            "first": first,
                            "last": last,
                            "den_type": den_type,
                            "den_num": den_num,
                            "items": [],
                        }
                    scouts[key]["items"].append(item)  # type: ignore[union-attr,attr-defined]
        except FileNotFoundError:
            raise CSVReadError(f"Could not find '{input_file}'") from None
        except KeyError as e:
            raise CSVColumnError(f"Missing column {e} in '{input_file}'") from e

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


def _font_sizes(spec: LabelSpec) -> tuple[float, float]:
    """Return (name_font_size, awards_font_size) scaled to label height."""
    # Scale relative to the 2" reference height of Avery 6427
    ref_height = 2.0 * inch
    scale = min(spec.label_height / ref_height, 1.0)
    name_size = max(NAME_FONT_SIZE * scale, 6.0)
    awards_size = max(AWARDS_FONT_SIZE * scale, 5.0)
    return name_size, awards_size


def _label_origin(index: int, spec: LabelSpec) -> tuple[float, float]:
    """Return (x, y) of the top-left corner of label at the given index."""
    col = index % spec.columns
    row = index // spec.columns
    x = spec.left_margin + col * (spec.label_width + spec.h_gap)
    y = PAGE_HEIGHT - spec.top_margin - row * (spec.label_height + spec.v_gap)
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


def _draw_label(c: canvas.Canvas, x: float, y: float, scout: ScoutRecord, spec: LabelSpec) -> None:
    """Draw a single scout label at position (x, y) = top-left of label."""
    name_size, awards_size = _font_sizes(spec)
    text_x = x + PAD_LEFT
    usable_width = spec.label_width - PAD_LEFT - PAD_RIGHT

    den_display = scout.den_type.title()
    name_line = f"{scout.first} {scout.last} [{den_display} ({scout.den_num})]"

    c.setFont("Helvetica-Bold", name_size)
    # Truncate name if it overflows the label width
    while (
        c.stringWidth(name_line, "Helvetica-Bold", name_size) > usable_width
        and len(name_line) > 10
    ):
        name_line = name_line[:-4] + "..."
    name_y = y - PAD_TOP - name_size
    c.drawString(text_x, name_y, name_line)

    awards_text = ", ".join(scout.items)
    c.setFont("Helvetica", awards_size)
    lines = _wrap_text(c, awards_text, usable_width, "Helvetica", awards_size)

    line_height = awards_size + 2
    awards_start_y = name_y - line_height
    label_bottom = y - spec.label_height + PAD_BOTTOM

    for i, line in enumerate(lines):
        line_y = awards_start_y - i * line_height
        if line_y < label_bottom:
            break
        c.drawString(text_x, line_y, line)


def generate_pdf(
    scouts: list[ScoutRecord],
    output_path: str,
    *,
    label_spec: LabelSpec | None = None,
) -> GenerationResult:
    """Generate the label PDF and return results.

    Args:
        scouts: List of scout records to generate labels for.
        output_path: Path for the output PDF file.
        label_spec: Label layout specification. Defaults to Avery 6427.

    Raises:
        OSError: If the output file cannot be written.
    """
    spec = label_spec or DEFAULT_LABEL_SPEC

    resolved = Path(output_path).resolve()
    if resolved.suffix.lower() != ".pdf":
        raise OSError(f"Output path must end with .pdf: {resolved.name}")
    parent = resolved.parent
    if not parent.exists():
        raise OSError(f"Output directory does not exist: {parent}")
    output_path = str(resolved)

    c = canvas.Canvas(output_path, pagesize=LETTER)
    c.setTitle("Cub Scout Advancement Labels")

    for i, scout in enumerate(scouts):
        page_index = i % spec.labels_per_page
        if i > 0 and page_index == 0:
            c.showPage()

        x, y = _label_origin(page_index, spec)
        _draw_label(c, x, y, scout, spec)

    c.save()
    page_count = (len(scouts) + spec.labels_per_page - 1) // spec.labels_per_page if scouts else 0

    return GenerationResult(
        label_count=len(scouts),
        page_count=page_count,
        output_path=output_path,
    )
