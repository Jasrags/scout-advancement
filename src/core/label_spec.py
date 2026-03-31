"""Label specifications for different Avery label types.

Each LabelSpec defines the physical layout of a label sheet: label dimensions,
margins, gaps, and grid layout. Used by the label generator to render labels
for any supported label type.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from reportlab.lib.units import inch


@dataclass(frozen=True)
class LabelSpec:
    """Physical layout specification for a label sheet."""

    name: str  # e.g. "Avery 6427"
    description: str  # e.g. "2\" x 4\" Shipping Labels"

    # Label dimensions
    label_width: float  # in points
    label_height: float  # in points

    # Grid layout
    columns: int
    rows: int

    # Page margins (from edge to first label)
    top_margin: float
    left_margin: float

    # Gaps between labels
    h_gap: float  # horizontal gap between columns
    v_gap: float  # vertical gap between rows

    @property
    def labels_per_page(self) -> int:
        return self.columns * self.rows


# ---------------------------------------------------------------------------
# Avery label catalog
# All measurements converted to points (1 inch = 72 points)
# ---------------------------------------------------------------------------

AVERY_6427 = LabelSpec(
    name="Avery 6427",
    description='2" x 4" Shipping Labels (10/sheet)',
    label_width=4.0 * inch,
    label_height=2.0 * inch,
    columns=2,
    rows=5,
    top_margin=0.5 * inch,
    left_margin=0.15625 * inch,
    h_gap=0.1875 * inch,
    v_gap=0.0,
)

AVERY_5163 = LabelSpec(
    name="Avery 5163",
    description='2" x 4" Shipping Labels (10/sheet)',
    label_width=4.0 * inch,
    label_height=2.0 * inch,
    columns=2,
    rows=5,
    top_margin=0.5 * inch,
    left_margin=0.15625 * inch,
    h_gap=0.1875 * inch,
    v_gap=0.0,
)

AVERY_5164 = LabelSpec(
    name="Avery 5164",
    description='3\u2153" x 4" Shipping Labels (6/sheet)',
    label_width=4.0 * inch,
    label_height=3.3333 * inch,
    columns=2,
    rows=3,
    top_margin=0.5 * inch,
    left_margin=0.15625 * inch,
    h_gap=0.1875 * inch,
    v_gap=0.0,
)

AVERY_5160 = LabelSpec(
    name="Avery 5160",
    description='1" x 2\u215d" Address Labels (30/sheet)',
    label_width=2.625 * inch,
    label_height=1.0 * inch,
    columns=3,
    rows=10,
    top_margin=0.5 * inch,
    left_margin=0.1875 * inch,
    h_gap=0.125 * inch,
    v_gap=0.0,
)

AVERY_5162 = LabelSpec(
    name="Avery 5162",
    description='1\u2153" x 4" Address Labels (14/sheet)',
    label_width=4.0 * inch,
    label_height=1.3333 * inch,
    columns=2,
    rows=7,
    top_margin=0.8333 * inch,
    left_margin=0.15625 * inch,
    h_gap=0.1875 * inch,
    v_gap=0.0,
)

AVERY_8163 = LabelSpec(
    name="Avery 8163",
    description='2" x 4" Shipping Labels (10/sheet)',
    label_width=4.0 * inch,
    label_height=2.0 * inch,
    columns=2,
    rows=5,
    top_margin=0.5 * inch,
    left_margin=0.15625 * inch,
    h_gap=0.1875 * inch,
    v_gap=0.0,
)

# Ordered list for the UI dropdown — most useful types first
LABEL_CATALOG: list[LabelSpec] = [
    AVERY_6427,
    AVERY_5163,
    AVERY_8163,
    AVERY_5164,
    AVERY_5162,
    AVERY_5160,
]

DEFAULT_LABEL_SPEC = AVERY_6427


@dataclass(frozen=True)
class LabelTemplate:
    """Controls what content appears on each label."""

    name_order: Literal["first_last", "last_first"] = "first_last"
    show_den_number: bool = True
    show_date_earned: bool = False
    show_sku: bool = False

    def format_name(self, first: str, last: str, den_type: str, den_num: str) -> str:
        """Format the scout name line according to template settings."""
        den_display = den_type.title()
        name = f"{last}, {first}" if self.name_order == "last_first" else f"{first} {last}"
        if self.show_den_number:
            return f"{name} [{den_display} ({den_num})]"
        return f"{name} [{den_display}]"

    def format_item(self, name: str, sku: str, date_earned: str) -> str:
        """Format a single item according to template settings."""
        parts = [name]
        if self.show_sku and sku:
            parts.append(f"[{sku}]")
        if self.show_date_earned and date_earned:
            parts.append(f"({date_earned})")
        return " ".join(parts)


DEFAULT_LABEL_TEMPLATE = LabelTemplate()


def get_label_spec(name: str) -> LabelSpec | None:
    """Look up a label spec by name (e.g. 'Avery 6427')."""
    for spec in LABEL_CATALOG:
        if spec.name == name:
            return spec
    return None
