"""Label template settings dialog.

Lets users customize what appears on each label: name order,
den number, date earned, SKU.
"""

from __future__ import annotations

from PySide6.QtCore import QSettings
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.core.label_spec import LabelTemplate


class LabelSettingsDialog(QDialog):
    """Dialog for editing label template settings."""

    def __init__(self, settings: QSettings, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Label Settings")
        self._settings = settings
        self._setup_ui()
        self._load_settings()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        form = QFormLayout()

        self._name_order = QComboBox()
        self._name_order.addItem("First Last (e.g. Liam Carter)", "first_last")
        self._name_order.addItem("Last, First (e.g. Carter, Liam)", "last_first")
        form.addRow("Name order:", self._name_order)

        self._show_den = QCheckBox("Show den number")
        form.addRow("", self._show_den)

        self._show_date = QCheckBox("Show date earned")
        form.addRow("", self._show_date)

        self._show_sku = QCheckBox("Show SKU")
        form.addRow("", self._show_sku)

        layout.addLayout(form)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self._on_save)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

    def _load_settings(self) -> None:
        name_order = str(self._settings.value("template/name_order", "first_last"))
        idx = self._name_order.findData(name_order)
        if idx >= 0:
            self._name_order.setCurrentIndex(idx)

        self._show_den.setChecked(
            bool(self._settings.value("template/show_den_number", True, type=bool))
        )
        self._show_date.setChecked(
            bool(self._settings.value("template/show_date_earned", False, type=bool))
        )
        self._show_sku.setChecked(
            bool(self._settings.value("template/show_sku", False, type=bool))
        )

    def _on_save(self) -> None:
        self._settings.setValue("template/name_order", self._name_order.currentData())
        self._settings.setValue("template/show_den_number", self._show_den.isChecked())
        self._settings.setValue("template/show_date_earned", self._show_date.isChecked())
        self._settings.setValue("template/show_sku", self._show_sku.isChecked())
        self.accept()


def load_template_from_settings(settings: QSettings) -> LabelTemplate:
    """Load a LabelTemplate from QSettings."""
    raw_order = str(settings.value("template/name_order", "first_last"))
    name_order = raw_order if raw_order in ("first_last", "last_first") else "first_last"
    return LabelTemplate(
        name_order=name_order,  # type: ignore[arg-type]
        show_den_number=bool(settings.value("template/show_den_number", True, type=bool)),
        show_date_earned=bool(settings.value("template/show_date_earned", False, type=bool)),
        show_sku=bool(settings.value("template/show_sku", False, type=bool)),
    )
