"""Tests for src.core.inventory."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.core.inventory import (
    DeductionResult,
    InventoryStore,
    aggregate_demand,
)
from src.core.label_generator import ItemDetail, ScoutRecord


@pytest.fixture
def store_path(tmp_path: Path) -> Path:
    return tmp_path / "inventory.json"


@pytest.fixture
def store(store_path: Path) -> InventoryStore:
    return InventoryStore(store_path)


@pytest.fixture
def sample_scouts() -> list[ScoutRecord]:
    return [
        ScoutRecord(
            first="Liam",
            last="Carter",
            den_type="Lions",
            den_num="1",
            items=(
                "Fun on the Run Adventure",
                "Mountain Lion Adventure",
            ),
            item_details=(
                ItemDetail(name="Fun on the Run Adventure", sku="646404"),
                ItemDetail(name="Mountain Lion Adventure", sku="646410"),
            ),
        ),
        ScoutRecord(
            first="Noah",
            last="Smith",
            den_type="Lions",
            den_num="1",
            items=("Fun on the Run Adventure",),
            item_details=(ItemDetail(name="Fun on the Run Adventure", sku="646404"),),
        ),
    ]


class TestQuantityAccess:
    def test_get_default_zero(self, store: InventoryStore) -> None:
        assert store.get_quantity("lion", "Fun on the Run") == 0

    def test_set_and_get(self, store: InventoryStore) -> None:
        store.set_quantity("lion", "Fun on the Run", 5)
        assert store.get_quantity("lion", "Fun on the Run") == 5

    def test_set_floors_at_zero(self, store: InventoryStore) -> None:
        store.set_quantity("lion", "Fun on the Run", -3)
        assert store.get_quantity("lion", "Fun on the Run") == 0

    def test_get_rank_quantities(self, store: InventoryStore) -> None:
        store.set_quantity("lion", "Fun on the Run", 5)
        store.set_quantity("lion", "Mountain Lion", 0)
        store.set_quantity("tiger", "Tiger Bites", 3)
        result = store.get_rank_quantities("lion")
        assert result == {"Fun on the Run": 5}

    def test_get_rank_quantities_empty(self, store: InventoryStore) -> None:
        assert store.get_rank_quantities("lion") == {}

    def test_get_all_nonzero(self, store: InventoryStore) -> None:
        store.set_quantity("lion", "Fun on the Run", 5)
        store.set_quantity("tiger", "Tiger Bites", 3)
        store.set_quantity("wolf", "Footsteps", 0)
        result = store.get_all_nonzero()
        assert result == {
            ("lion", "Fun on the Run"): 5,
            ("tiger", "Tiger Bites"): 3,
        }

    def test_get_all_nonzero_empty(self, store: InventoryStore) -> None:
        assert store.get_all_nonzero() == {}


class TestPersistence:
    def test_save_and_load_roundtrip(self, store: InventoryStore, store_path: Path) -> None:
        store.set_quantity("lion", "Fun on the Run", 5)
        store.set_quantity("tiger", "Tiger Bites", 3)
        store.save()

        loaded = InventoryStore(store_path)
        loaded.load()
        assert loaded.get_quantity("lion", "Fun on the Run") == 5
        assert loaded.get_quantity("tiger", "Tiger Bites") == 3

    def test_load_missing_file_yields_empty(self, tmp_path: Path) -> None:
        store = InventoryStore(tmp_path / "does_not_exist.json")
        store.load()
        assert store.get_all_nonzero() == {}

    def test_load_corrupt_json(self, store_path: Path) -> None:
        store_path.write_text("not valid json {{{")
        store = InventoryStore(store_path)
        store.load()
        assert store.get_all_nonzero() == {}

    def test_load_wrong_schema_version(self, store_path: Path) -> None:
        data = {"version": 999, "quantities": {}}
        store_path.write_text(json.dumps(data))
        store = InventoryStore(store_path)
        with pytest.raises(ValueError, match="version"):
            store.load()

    def test_save_creates_parent_directory(self, tmp_path: Path) -> None:
        nested = tmp_path / "sub" / "dir" / "inventory.json"
        store = InventoryStore(nested)
        store.set_quantity("lion", "Bobcat", 1)
        store.save()
        assert nested.exists()

    def test_json_structure(self, store: InventoryStore, store_path: Path) -> None:
        store.set_quantity("lion", "Fun on the Run", 3)
        store.save()
        data = json.loads(store_path.read_text())
        assert data["version"] == 1
        assert data["quantities"]["lion"]["Fun on the Run"] == 3

    def test_save_omits_zero_quantities(self, store: InventoryStore, store_path: Path) -> None:
        store.set_quantity("lion", "Fun on the Run", 5)
        store.set_quantity("lion", "Bobcat", 0)
        store.save()
        data = json.loads(store_path.read_text())
        assert "Bobcat" not in data["quantities"].get("lion", {})

    def test_reset(self, store: InventoryStore) -> None:
        store.set_quantity("lion", "Fun on the Run", 5)
        store.reset()
        assert store.get_all_nonzero() == {}


class TestBulkDecrement:
    def test_correct_deduction(self, store: InventoryStore) -> None:
        store.set_quantity("lion", "Fun on the Run", 10)
        store.set_quantity("tiger", "Tiger Bites", 5)
        demand = {
            ("lion", "Fun on the Run"): 3,
            ("tiger", "Tiger Bites"): 2,
        }
        result = store.bulk_decrement(demand)
        assert isinstance(result, DeductionResult)
        assert store.get_quantity("lion", "Fun on the Run") == 7
        assert store.get_quantity("tiger", "Tiger Bites") == 3
        assert result.total_deducted == 5

    def test_floors_at_zero(self, store: InventoryStore) -> None:
        store.set_quantity("lion", "Fun on the Run", 2)
        result = store.bulk_decrement({("lion", "Fun on the Run"): 10})
        assert store.get_quantity("lion", "Fun on the Run") == 0
        assert result.items_at_zero == 1
        assert result.rows[0].deducted == 2

    def test_skips_items_with_zero_stock(self, store: InventoryStore) -> None:
        result = store.bulk_decrement({("lion", "Unknown"): 5})
        assert len(result.rows) == 1
        assert result.rows[0].deducted == 0
        assert result.total_deducted == 0

    def test_empty_demand(self, store: InventoryStore) -> None:
        result = store.bulk_decrement({})
        assert len(result.rows) == 0
        assert result.total_deducted == 0

    def test_result_rows(self, store: InventoryStore) -> None:
        store.set_quantity("lion", "Fun on the Run", 10)
        result = store.bulk_decrement({("lion", "Fun on the Run"): 3})
        row = result.rows[0]
        assert row.rank == "lion"
        assert row.name == "Fun on the Run"
        assert row.previous_qty == 10
        assert row.deducted == 3
        assert row.new_qty == 7


class TestComputeShoppingList:
    def test_basic_diff(self) -> None:
        demand = {("lion", "Fun on the Run"): 5, ("tiger", "Tiger Bites"): 3}
        quantities = {("lion", "Fun on the Run"): 2, ("tiger", "Tiger Bites"): 10}
        rows = InventoryStore.compute_shopping_list(demand, quantities)
        by_name = {r.name: r for r in rows}
        assert by_name["Fun on the Run"].need == 5
        assert by_name["Fun on the Run"].have == 2
        assert by_name["Fun on the Run"].buy == 3
        assert by_name["Tiger Bites"].buy == 0

    def test_item_not_in_inventory(self) -> None:
        demand = {("lion", "Fun on the Run"): 5}
        rows = InventoryStore.compute_shopping_list(demand, {})
        assert len(rows) == 1
        assert rows[0].have == 0
        assert rows[0].buy == 5

    def test_empty_demand(self) -> None:
        rows = InventoryStore.compute_shopping_list({}, {})
        assert rows == []


class TestAggregateDemand:
    def test_sums_across_scouts(self, sample_scouts: list[ScoutRecord]) -> None:
        demand = aggregate_demand(sample_scouts)
        # Both Liam and Noah have "Fun on the Run Adventure" -> "Fun on the Run"
        assert demand[("lion", "Fun on the Run")] == 2
        # Only Liam has "Mountain Lion Adventure" -> "Mountain Lion"
        assert demand[("lion", "Mountain Lion")] == 1

    def test_skips_unrecognized_items(self) -> None:
        scouts = [
            ScoutRecord(
                first="A",
                last="B",
                den_type="Lions",
                den_num="1",
                items=("Totally Made Up Award",),
                item_details=(ItemDetail(name="Totally Made Up Award", sku="999"),),
            ),
        ]
        demand = aggregate_demand(scouts)
        assert demand == {}

    def test_skips_unrecognized_rank(self) -> None:
        scouts = [
            ScoutRecord(
                first="A",
                last="B",
                den_type="UnknownRank",
                den_num="1",
                items=("Fun on the Run Adventure",),
                item_details=(ItemDetail(name="Fun on the Run Adventure", sku="646404"),),
            ),
        ]
        demand = aggregate_demand(scouts)
        assert demand == {}

    def test_empty_scouts(self) -> None:
        assert aggregate_demand([]) == {}

    def test_scout_with_no_item_details(self) -> None:
        scouts = [
            ScoutRecord(
                first="A",
                last="B",
                den_type="Lions",
                den_num="1",
                items=("Test",),
            ),
        ]
        demand = aggregate_demand(scouts)
        assert demand == {}
