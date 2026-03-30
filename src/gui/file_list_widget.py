"""File list widget for selecting and managing CSV files."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.core.csv_validator import validate_csv


class FileListWidget(QWidget):
    """Widget for selecting, validating, and managing CSV files."""

    files_changed = Signal(int)  # emits current count of valid files

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._file_paths: list[str] = []
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self._list_widget = QListWidget()
        self._list_widget.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        layout.addWidget(self._list_widget)

        button_row = QHBoxLayout()
        self._add_btn = QPushButton("Add Files...")
        self._remove_btn = QPushButton("Remove")
        self._clear_btn = QPushButton("Clear All")

        self._remove_btn.setEnabled(False)
        self._clear_btn.setEnabled(False)

        self._add_btn.clicked.connect(self._on_add_files)
        self._remove_btn.clicked.connect(self._on_remove)
        self._clear_btn.clicked.connect(self._on_clear)
        self._list_widget.currentRowChanged.connect(self._on_selection_changed)

        button_row.addWidget(self._add_btn)
        button_row.addWidget(self._remove_btn)
        button_row.addWidget(self._clear_btn)
        button_row.addStretch()
        layout.addLayout(button_row)

    def _on_add_files(self) -> None:
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Advancement CSV Files",
            "",
            "CSV Files (*.csv);;All Files (*)",
        )
        for file_path in files:
            if file_path not in self._file_paths:
                self._add_file(file_path)
        self._update_buttons()
        self.files_changed.emit(self.valid_file_count())

    def _add_file(self, file_path: str) -> None:
        result = validate_csv(file_path)
        name = Path(file_path).name

        item = QListWidgetItem()
        if result.is_valid:
            item.setText(f"{name}  ({result.row_count} rows)")
        else:
            item.setText(f"{name}  — {result.error}")
            item.setForeground(item.listWidget().palette().mid().color() if item.listWidget() else None)  # type: ignore[arg-type]

        item.setData(256, file_path)  # Qt.UserRole = 256
        item.setData(257, result.is_valid)  # Qt.UserRole + 1

        self._file_paths.append(file_path)
        self._list_widget.addItem(item)

    def _on_remove(self) -> None:
        row = self._list_widget.currentRow()
        if row >= 0:
            item = self._list_widget.takeItem(row)
            if item:
                path = item.data(256)
                if path in self._file_paths:
                    self._file_paths.remove(path)
        self._update_buttons()
        self.files_changed.emit(self.valid_file_count())

    def _on_clear(self) -> None:
        self._list_widget.clear()
        self._file_paths.clear()
        self._update_buttons()
        self.files_changed.emit(0)

    def _on_selection_changed(self, row: int) -> None:
        self._remove_btn.setEnabled(row >= 0)

    def _update_buttons(self) -> None:
        has_files = self._list_widget.count() > 0
        self._clear_btn.setEnabled(has_files)
        self._remove_btn.setEnabled(self._list_widget.currentRow() >= 0)

    def valid_file_count(self) -> int:
        """Return the number of files that passed validation."""
        count = 0
        for i in range(self._list_widget.count()):
            item = self._list_widget.item(i)
            if item and item.data(257):
                count += 1
        return count

    def get_valid_file_paths(self) -> list[str]:
        """Return paths of files that passed validation."""
        paths: list[str] = []
        for i in range(self._list_widget.count()):
            item = self._list_widget.item(i)
            if item and item.data(257):
                paths.append(item.data(256))
        return paths
