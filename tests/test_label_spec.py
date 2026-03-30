"""Tests for src.core.label_spec."""

from reportlab.lib.units import inch

from src.core.label_spec import (
    AVERY_5160,
    AVERY_5163,
    AVERY_6427,
    DEFAULT_LABEL_SPEC,
    LABEL_CATALOG,
    get_label_spec,
)


class TestLabelSpec:
    def test_labels_per_page(self) -> None:
        assert AVERY_6427.labels_per_page == 10
        assert AVERY_5160.labels_per_page == 30
        assert AVERY_5163.labels_per_page == 10

    def test_frozen(self) -> None:
        import pytest

        with pytest.raises(AttributeError):
            AVERY_6427.label_width = 5.0 * inch  # type: ignore[misc]

    def test_default_is_6427(self) -> None:
        assert DEFAULT_LABEL_SPEC is AVERY_6427


class TestLabelCatalog:
    def test_catalog_not_empty(self) -> None:
        assert len(LABEL_CATALOG) >= 4

    def test_all_specs_have_valid_dimensions(self) -> None:
        for spec in LABEL_CATALOG:
            assert spec.label_width > 0
            assert spec.label_height > 0
            assert spec.columns >= 1
            assert spec.rows >= 1
            assert spec.labels_per_page >= 1

    def test_all_specs_have_names(self) -> None:
        for spec in LABEL_CATALOG:
            assert spec.name
            assert spec.description

    def test_no_duplicate_names(self) -> None:
        names = [spec.name for spec in LABEL_CATALOG]
        assert len(names) == len(set(names))


class TestGetLabelSpec:
    def test_finds_by_name(self) -> None:
        spec = get_label_spec("Avery 6427")
        assert spec is AVERY_6427

    def test_returns_none_for_unknown(self) -> None:
        assert get_label_spec("Unknown Label") is None
