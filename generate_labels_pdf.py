#!/usr/bin/env python3
"""
Cub Scout Advancement Label PDF Generator

Generates printable Avery 6427 shipping labels (2" x 4", 10 per sheet)
from one or more advancement CSV files.

Usage:
    python generate_labels_pdf.py <input1.csv> [input2.csv ...] [-o output.pdf]
"""

import csv
import sys
from collections import OrderedDict

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
DEN_TYPE_ORDER = {
    "lion": 1,
    "tiger": 2,
    "wolf": 3,
    "bear": 4,
    "webelos": 5,
    "webelos 2": 6,
    "arrow of light": 6,
}


def read_advancements(input_files: list[str]) -> list[dict]:
    """Read CSV files and return sorted list of scout records."""
    scouts: OrderedDict[tuple, dict] = OrderedDict()

    for input_file in input_files:
        try:
            print(f"  Reading: {input_file}")
            with open(input_file, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                row_count = 0
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
                    scouts[key]["items"].append(item)
                    row_count += 1
                print(f"    Found {row_count} advancements")
        except FileNotFoundError:
            print(f"  Error: Could not find '{input_file}'")
            sys.exit(1)
        except KeyError as e:
            print(f"  Error: Missing column {e}")
            sys.exit(1)

    def sort_key(record: dict) -> tuple:
        rank = DEN_TYPE_ORDER.get(record["den_type"].lower(), 999)
        return (rank, record["last"].lower(), record["first"].lower())

    return sorted(scouts.values(), key=sort_key)


def label_origin(index: int) -> tuple[float, float]:
    """Return (x, y) of the top-left corner of label at the given index (0-9)."""
    col = index % COLUMNS
    row = index // COLUMNS
    x = LEFT_MARGIN + col * (LABEL_WIDTH + H_GAP)
    # y from top of page, converted to reportlab bottom-up coords
    y = PAGE_HEIGHT - TOP_MARGIN - row * (LABEL_HEIGHT + V_GAP)
    return x, y


def wrap_text(c: canvas.Canvas, text: str, max_width: float, font_name: str, font_size: float) -> list[str]:
    """Word-wrap text to fit within max_width, returns list of lines."""
    words = text.split()
    lines = []
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


def draw_label(c: canvas.Canvas, x: float, y: float, scout: dict) -> None:
    """Draw a single scout label at position (x, y) = top-left of label."""
    text_x = x + PAD_LEFT
    usable_width = LABEL_WIDTH - PAD_LEFT - PAD_RIGHT

    # --- Name line: "First Last [Den Type (Den #)]" ---
    den_display = scout["den_type"].title()
    name_line = f"{scout['first']} {scout['last']} [{den_display} ({scout['den_num']})]"

    c.setFont("Helvetica-Bold", NAME_FONT_SIZE)
    name_y = y - PAD_TOP - NAME_FONT_SIZE
    c.drawString(text_x, name_y, name_line)

    # --- Awards text, top-aligned directly under name ---
    awards_text = ", ".join(scout["items"])
    c.setFont("Helvetica", AWARDS_FONT_SIZE)
    lines = wrap_text(c, awards_text, usable_width, "Helvetica", AWARDS_FONT_SIZE)

    line_height = AWARDS_FONT_SIZE + 2
    awards_start_y = name_y - line_height  # start immediately below name
    label_bottom = y - LABEL_HEIGHT + PAD_BOTTOM

    for i, line in enumerate(lines):
        line_y = awards_start_y - i * line_height
        if line_y < label_bottom:
            break
        c.drawString(text_x, line_y, line)


def generate_pdf(scouts: list[dict], output_path: str) -> None:
    """Generate the label PDF."""
    c = canvas.Canvas(output_path, pagesize=LETTER)
    c.setTitle("Cub Scout Advancement Labels")

    for i, scout in enumerate(scouts):
        page_index = i % LABELS_PER_PAGE
        if i > 0 and page_index == 0:
            c.showPage()

        x, y = label_origin(page_index)
        draw_label(c, x, y, scout)

    c.save()
    pages = (len(scouts) + LABELS_PER_PAGE - 1) // LABELS_PER_PAGE
    print(f"\nGenerated {output_path}")
    print(f"  {len(scouts)} labels on {pages} page(s)")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python generate_labels_pdf.py <input1.csv> [input2.csv ...] [-o output.pdf]")
        sys.exit(1)

    args = sys.argv[1:]
    output_file = "advancement_labels.pdf"
    input_files = []

    if "-o" in args:
        o_index = args.index("-o")
        if o_index + 1 >= len(args):
            print("Error: -o flag requires an output filename")
            sys.exit(1)
        output_file = args[o_index + 1]
        input_files = args[:o_index] + args[o_index + 2:]
    else:
        input_files = args

    if not input_files:
        print("Error: At least one input file is required")
        sys.exit(1)

    print(f"Processing {len(input_files)} file(s)")
    print("-" * 40)

    scouts = read_advancements(input_files)
    generate_pdf(scouts, output_file)


if __name__ == "__main__":
    main()
