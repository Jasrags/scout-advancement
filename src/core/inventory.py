"""Award inventory management with JSON persistence.

Tracks leftover awards by adventure name and rank so the pack can see
what's in stock before placing a new order. The catalog is driven by
the adventure database in adventure_data.py — every known adventure is
always visible in the UI. All inventory actions are user-triggered;
the core CSV-to-labels flow is never altered.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path

from src.core.adventure_data import find_adventure, normalize_rank
from src.core.label_generator import ScoutRecord

logger = logging.getLogger(__name__)

SCHEMA_VERSION = 1

# Canonical rank order for display
RANKS: list[str] = ["lion", "tiger", "wolf", "bear", "webelos", "arrow of light"]


# ---------------------------------------------------------------------------
# Data classes (frozen / immutable)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DeductionRow:
    rank: str
    name: str
    previous_qty: int
    deducted: int
    new_qty: int


@dataclass(frozen=True)
class DeductionResult:
    rows: tuple[DeductionRow, ...]
    total_deducted: int
    items_at_zero: int


@dataclass(frozen=True)
class ShoppingListRow:
    name: str
    rank: str
    need: int
    have: int
    buy: int  # max(0, need - have)


# ---------------------------------------------------------------------------
# Free function
# ---------------------------------------------------------------------------


def aggregate_demand(
    scouts: list[ScoutRecord],
) -> dict[tuple[str, str], int]:
    """Sum item quantities across all scouts, keyed by (rank, adventure_name).

    Uses find_adventure() to match CSV item names to the adventure catalog.
    Items that don't match any known adventure are skipped.
    """
    demand: dict[tuple[str, str], int] = {}
    for scout in scouts:
        rank = normalize_rank(scout.den_type)
        if rank is None:
            continue
        for detail in scout.item_details:
            adventure = find_adventure(detail.name, scout.den_type)
            if adventure is None:
                continue
            key = (rank, adventure.name)
            demand[key] = demand.get(key, 0) + 1
    return demand


# ---------------------------------------------------------------------------
# Inventory store
# ---------------------------------------------------------------------------


class InventoryStore:
    """Manages a JSON-backed inventory of award quantities.

    Quantities are stored per (rank, adventure_name). The adventure catalog
    comes from adventure_data.ADVENTURES — the store only tracks counts.
    """

    def __init__(self, path: Path) -> None:
        self._path = path
        # {rank: {adventure_name: quantity}}
        self._quantities: dict[str, dict[str, int]] = {}

    # -- Quantity access ----------------------------------------------------

    def get_quantity(self, rank: str, adventure_name: str) -> int:
        return self._quantities.get(rank, {}).get(adventure_name, 0)

    def set_quantity(self, rank: str, adventure_name: str, quantity: int) -> None:
        if rank not in self._quantities:
            self._quantities[rank] = {}
        self._quantities[rank][adventure_name] = max(0, quantity)

    def get_rank_quantities(self, rank: str) -> dict[str, int]:
        """Return {adventure_name: quantity} for a rank. Only non-zero entries."""
        return {k: v for k, v in self._quantities.get(rank, {}).items() if v > 0}

    def get_all_nonzero(self) -> dict[tuple[str, str], int]:
        """Return {(rank, adventure_name): quantity} for all non-zero entries."""
        result: dict[tuple[str, str], int] = {}
        for rank, adventures in self._quantities.items():
            for name, qty in adventures.items():
                if qty > 0:
                    result[(rank, name)] = qty
        return result

    # -- Bulk operations ----------------------------------------------------

    def bulk_decrement(self, demand: dict[tuple[str, str], int]) -> DeductionResult:
        """Deduct quantities for each (rank, adventure) in demand. Floors at 0."""
        rows: list[DeductionRow] = []
        total_deducted = 0
        items_at_zero = 0
        for (rank, name), qty_needed in demand.items():
            previous = self.get_quantity(rank, name)
            actual_deduction = min(previous, qty_needed)
            new_qty = previous - actual_deduction
            self.set_quantity(rank, name, new_qty)
            total_deducted += actual_deduction
            if new_qty == 0 and actual_deduction > 0:
                items_at_zero += 1
            rows.append(
                DeductionRow(
                    rank=rank,
                    name=name,
                    previous_qty=previous,
                    deducted=actual_deduction,
                    new_qty=new_qty,
                )
            )
        return DeductionResult(
            rows=tuple(rows),
            total_deducted=total_deducted,
            items_at_zero=items_at_zero,
        )

    # -- Shopping list diff -------------------------------------------------

    @staticmethod
    def compute_shopping_list(
        demand: dict[tuple[str, str], int],
        quantities: dict[tuple[str, str], int],
    ) -> list[ShoppingListRow]:
        """Compare demand against inventory, return need/have/buy rows."""
        rows: list[ShoppingListRow] = []
        for (rank, name), need in demand.items():
            have = quantities.get((rank, name), 0)
            buy = max(0, need - have)
            rows.append(ShoppingListRow(name=name, rank=rank, need=need, have=have, buy=buy))
        return rows

    # -- Persistence --------------------------------------------------------

    def load(self) -> None:
        """Load inventory from JSON file. Missing file -> empty store."""
        if not self._path.exists():
            return
        try:
            data = json.loads(self._path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            logger.warning("Corrupt inventory file at %s - starting empty", self._path)
            self._quantities = {}
            return

        version = data.get("version", 0)
        if version != SCHEMA_VERSION:
            raise ValueError(
                f"Unsupported inventory schema version {version} (expected {SCHEMA_VERSION})"
            )

        self._quantities = {}
        for rank, adventures in data.get("quantities", {}).items():
            self._quantities[rank] = {name: qty for name, qty in adventures.items() if qty > 0}

    def save(self) -> None:
        """Persist inventory to JSON file."""
        self._path.parent.mkdir(parents=True, exist_ok=True)
        # Only persist non-zero quantities
        quantities_out: dict[str, dict[str, int]] = {}
        for rank, adventures in self._quantities.items():
            nonzero = {n: q for n, q in adventures.items() if q > 0}
            if nonzero:
                quantities_out[rank] = nonzero
        data = {"version": SCHEMA_VERSION, "quantities": quantities_out}
        self._path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def reset(self) -> None:
        """Clear all inventory quantities."""
        self._quantities = {}
