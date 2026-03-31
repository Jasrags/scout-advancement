"""Tests for src.core.label_spec."""

from reportlab.lib.units import inch

from src.core.label_spec import (
    AVERY_5160,
    AVERY_5163,
    AVERY_6427,
    DEFAULT_LABEL_SPEC,
    DEFAULT_LABEL_TEMPLATE,
    LABEL_CATALOG,
    LabelTemplate,
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


class TestLabelTemplate:
    def test_default_format_name(self) -> None:
        tmpl = DEFAULT_LABEL_TEMPLATE
        result = tmpl.format_name("Liam", "Carter", "lions", "2")
        assert result == "Liam Carter [Lions (2)]"

    def test_last_first_name_order(self) -> None:
        tmpl = LabelTemplate(name_order="last_first")
        result = tmpl.format_name("Liam", "Carter", "lions", "2")
        assert result == "Carter, Liam [Lions (2)]"

    def test_hide_den_number(self) -> None:
        tmpl = LabelTemplate(show_den_number=False)
        result = tmpl.format_name("Liam", "Carter", "lions", "2")
        assert result == "Liam Carter [Lions]"

    def test_format_item_default(self) -> None:
        tmpl = DEFAULT_LABEL_TEMPLATE
        result = tmpl.format_item("Fun on the Run Adventure", "646404", "2025-11-15")
        assert result == "Fun on the Run Adventure"

    def test_format_item_with_sku(self) -> None:
        tmpl = LabelTemplate(show_sku=True)
        result = tmpl.format_item("Fun on the Run Adventure", "646404", "2025-11-15")
        assert result == "Fun on the Run Adventure [646404]"

    def test_format_item_with_date(self) -> None:
        tmpl = LabelTemplate(show_date_earned=True)
        result = tmpl.format_item("Fun on the Run Adventure", "646404", "2025-11-15")
        assert result == "Fun on the Run Adventure (2025-11-15)"

    def test_format_item_with_all(self) -> None:
        tmpl = LabelTemplate(show_sku=True, show_date_earned=True)
        result = tmpl.format_item("Fun on the Run Adventure", "646404", "2025-11-15")
        assert result == "Fun on the Run Adventure [646404] (2025-11-15)"

    def test_format_item_empty_sku_skipped(self) -> None:
        tmpl = LabelTemplate(show_sku=True)
        result = tmpl.format_item("Fun on the Run Adventure", "", "2025-11-15")
        assert result == "Fun on the Run Adventure"
