"""Per-rank inventory management screen with adventure images."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.core.adventure_data import ADVENTURES, Adventure
from src.core.inventory import RANKS, InventoryStore

# Tab display labels matching RANKS order
_RANK_LABELS: list[str] = [
    "Lion",
    "Tiger",
    "Wolf",
    "Bear",
    "Webelos",
    "Arrow of Light",
]

_IMG_SIZE = 48


class InventoryWidget(QDialog):
    """Dialog for managing award inventory, organized by rank with images."""

    def __init__(self, store: InventoryStore, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._store = store
        # Pending edits: {(rank, adventure_name): quantity}
        self._pending: dict[tuple[str, str], int] = {}
        self._spinboxes: dict[tuple[str, str], QSpinBox] = {}
        self.setWindowTitle("Manage Inventory")
        self.setMinimumSize(640, 500)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        header = QLabel("Award Inventory")
        header.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 4px;")
        layout.addWidget(header)

        subtitle = QLabel(
            "Track leftover awards by rank. Use +/- to adjust quantities, then Save or Cancel."
        )
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        self._tabs = QTabWidget()
        for rank, label in zip(RANKS, _RANK_LABELS, strict=True):
            scroll = self._build_rank_tab(rank)
            self._tabs.addTab(scroll, label)
        layout.addWidget(self._tabs, stretch=1)

        # Footer buttons
        btn_layout = QHBoxLayout()
        reset_btn = QPushButton("Reset All")
        reset_btn.setStyleSheet("color: red;")
        reset_btn.clicked.connect(self._on_reset)
        btn_layout.addWidget(reset_btn)

        btn_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)

        save_btn = QPushButton("Save")
        save_btn.setStyleSheet(
            "background-color: #1a73e8; color: white; "
            "font-weight: bold; padding: 6px 24px; border-radius: 4px;"
        )
        save_btn.clicked.connect(self._on_save)
        btn_layout.addWidget(save_btn)

        layout.addLayout(btn_layout)

    def _build_rank_tab(self, rank: str) -> QScrollArea:
        adventures = ADVENTURES.get(rank, [])
        required = [a for a in adventures if a.required]
        elective = [
            a
            for a in adventures
            if not a.required
            and "archery" not in a.name.lower()
            and "slingshot" not in a.name.lower()
            and "bb" not in a.name.lower()
        ]
        shooting = [
            a
            for a in adventures
            if not a.required
            and (
                "archery" in a.name.lower()
                or "slingshot" in a.name.lower()
                or "bb" in a.name.lower()
            )
        ]

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(12, 8, 12, 8)

        if required:
            layout.addWidget(self._section_label("Required Adventures"))
            layout.addLayout(self._build_grid(rank, required))

        if elective:
            layout.addWidget(self._section_label("Elective Adventures"))
            layout.addLayout(self._build_grid(rank, elective))

        if shooting:
            layout.addWidget(self._section_label("Shooting Sports"))
            layout.addLayout(self._build_grid(rank, shooting))

        layout.addStretch()

        scroll = QScrollArea()
        scroll.setWidget(container)
        scroll.setWidgetResizable(True)
        return scroll

    def _section_label(self, text: str) -> QLabel:
        label = QLabel(text)
        label.setStyleSheet(
            "font-size: 11px; text-transform: uppercase; "
            "letter-spacing: 0.5px; color: #888; font-weight: bold; "
            "border-bottom: 1px solid #ddd; padding-bottom: 4px; "
            "margin-top: 8px;"
        )
        return label

    def _build_grid(self, rank: str, adventures: list[Adventure]) -> QGridLayout:
        grid = QGridLayout()
        grid.setSpacing(8)
        for i, adv in enumerate(adventures):
            card = self._build_card(rank, adv)
            grid.addWidget(card, i // 2, i % 2)
        return grid

    def _build_card(self, rank: str, adventure: Adventure) -> QWidget:
        card = QWidget()
        card.setStyleSheet(
            "QWidget { background: #fafafa; border: 1px solid #e0e0e0; border-radius: 6px; }"
        )
        layout = QHBoxLayout(card)
        layout.setContentsMargins(8, 6, 8, 6)

        # Adventure image
        img_label = QLabel()
        img_label.setFixedSize(_IMG_SIZE, _IMG_SIZE)
        img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = self._load_image(adventure.image_path)
        if pixmap:
            img_label.setPixmap(
                pixmap.scaled(
                    _IMG_SIZE,
                    _IMG_SIZE,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        else:
            img_label.setStyleSheet("background: #e0e0e0; border-radius: 4px; border: none;")
        layout.addWidget(img_label)

        # Name + quantity
        info = QVBoxLayout()
        info.setSpacing(4)

        name_label = QLabel(adventure.name)
        name_label.setStyleSheet(
            "font-size: 12px; font-weight: 500; color: #333; "
            "background: transparent; border: none;"
        )
        name_label.setWordWrap(True)
        info.addWidget(name_label)

        qty_row = QHBoxLayout()
        qty_row.setSpacing(4)

        minus_btn = QPushButton("-")
        minus_btn.setFixedSize(24, 24)
        minus_btn.setStyleSheet(
            "font-size: 14px; font-weight: bold; border: 1px solid #ccc; "
            "border-radius: 4px; background: white; color: #555;"
        )
        qty_row.addWidget(minus_btn)

        spin = QSpinBox()
        spin.setRange(0, 9999)
        spin.setValue(self._store.get_quantity(rank, adventure.name))
        spin.setFixedWidth(50)
        spin.setAlignment(Qt.AlignmentFlag.AlignCenter)
        spin.setButtonSymbols(QSpinBox.ButtonSymbols.NoButtons)
        self._spinboxes[(rank, adventure.name)] = spin
        qty_row.addWidget(spin)

        plus_btn = QPushButton("+")
        plus_btn.setFixedSize(24, 24)
        plus_btn.setStyleSheet(
            "font-size: 14px; font-weight: bold; border: 1px solid #ccc; "
            "border-radius: 4px; background: white; color: #555;"
        )
        qty_row.addWidget(plus_btn)

        qty_row.addStretch()
        info.addLayout(qty_row)

        minus_btn.clicked.connect(lambda: spin.setValue(spin.value() - 1))
        plus_btn.clicked.connect(lambda: spin.setValue(spin.value() + 1))

        layout.addLayout(info, stretch=1)
        return card

    def _load_image(self, image_path: str) -> QPixmap | None:
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            return pixmap
        return None

    def _on_save(self) -> None:
        for (rank, name), spin in self._spinboxes.items():
            self._store.set_quantity(rank, name, spin.value())
        try:
            self._store.save()
        except OSError as e:
            QMessageBox.critical(self, "Save Failed", f"Could not save inventory:\n{e}")
            return
        self.accept()

    def _on_reset(self) -> None:
        reply = QMessageBox.warning(
            self,
            "Reset Inventory",
            "This will clear all inventory quantities.\n\nAre you sure?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            for spin in self._spinboxes.values():
                spin.setValue(0)
            self._store.reset()
            try:
                self._store.save()
            except OSError as e:
                QMessageBox.critical(self, "Save Failed", f"Could not save after reset:\n{e}")
