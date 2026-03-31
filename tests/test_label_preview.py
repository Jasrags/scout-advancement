"""Tests for src.gui.label_preview."""

from __future__ import annotations

import sys

import pytest

from src.core.label_generator import ScoutRecord
from src.core.label_spec import AVERY_5160, AVERY_5164, AVERY_6427

# Skip entire module if PySide6 can't initialize (headless CI without EGL)
try:
    from PySide6.QtWidgets import QApplication

    _app = QApplication.instance() or QApplication(sys.argv)
    from src.gui.label_preview import LabelPreviewDialog, LabelPreviewWidget
except ImportError:
    pytest.skip("PySide6 GUI not available (headless CI)", allow_module_level=True)


@pytest.fixture(scope="module")
def sample_scouts() -> list[ScoutRecord]:
    return [
        ScoutRecord("Alice", "Smith", "lions", "1", ("Fun on the Run Adventure",)),
        ScoutRecord(
            "Bob",
            "Jones",
            "tigers",
            "2",
            ("Team Tiger Adventure", "Tiger Circles Adventure", "Safe and Smart Adventure"),
        ),
        ScoutRecord("Charlie", "Brown", "bears", "3", ("Bear Strong Adventure",)),
    ]


class TestLabelPreviewWidget:
    def test_constructs_with_scouts(self, sample_scouts: list[ScoutRecord]) -> None:
        widget = LabelPreviewWidget(sample_scouts, AVERY_6427)
        assert widget.minimumWidth() >= 400
        assert widget.minimumHeight() >= 400

    def test_constructs_with_empty_scouts(self) -> None:
        widget = LabelPreviewWidget([], AVERY_6427)
        assert widget is not None

    def test_constructs_with_different_specs(self, sample_scouts: list[ScoutRecord]) -> None:
        for spec in [AVERY_6427, AVERY_5164, AVERY_5160]:
            widget = LabelPreviewWidget(sample_scouts, spec)
            assert widget is not None

    def test_limits_to_one_page(self, sample_scouts: list[ScoutRecord]) -> None:
        many_scouts = sample_scouts * 10
        widget = LabelPreviewWidget(many_scouts, AVERY_6427)
        assert len(widget._scouts) == AVERY_6427.labels_per_page


class TestLabelPreviewDialog:
    def test_constructs(self, sample_scouts: list[ScoutRecord]) -> None:
        dialog = LabelPreviewDialog(sample_scouts, AVERY_6427)
        assert dialog.windowTitle() == "Label Preview \u2014 Avery 6427"

    def test_constructs_with_different_spec(self, sample_scouts: list[ScoutRecord]) -> None:
        dialog = LabelPreviewDialog(sample_scouts, AVERY_5164)
        assert "Avery 5164" in dialog.windowTitle()
