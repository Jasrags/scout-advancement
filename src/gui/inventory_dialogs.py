"""Inventory action dialogs: deduction confirmation/summary and shopping list."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.core.inventory import DeductionResult, ShoppingListRow


class DeductionConfirmDialog(QDialog):
    """Shows proposed deductions and asks for confirmation."""

    def __init__(
        self,
        items: list[tuple[str, str, int, int]],
        parent: QWidget | None = None,
    ) -> None:
        """Args:
        items: [(rank, name, current_qty, deduct_qty), ...].
        """
        super().__init__(parent)
        self.setWindowTitle("Confirm Inventory Deduction")
        self.setMinimumSize(500, 350)
        self._setup_ui(items)

    def _setup_ui(self, items: list[tuple[str, str, int, int]]) -> None:
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("The following items will be deducted from inventory:"))

        table = QTableWidget(len(items), 4)
        table.setHorizontalHeaderLabels(["Item", "Current", "Deducting", "After"])
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for col in (1, 2, 3):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        table.verticalHeader().setVisible(False)

        total_deducting = 0
        for row, (_rank, name, current, deduct) in enumerate(items):
            actual = min(current, deduct)
            after = max(0, current - deduct)
            total_deducting += actual
            for col, text in enumerate([name, str(current), str(actual), str(after)]):
                cell = QTableWidgetItem(text)
                cell.setFlags(cell.flags() & ~Qt.ItemFlag.ItemIsEditable)
                if col > 0:
                    cell.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                    )
                table.setItem(row, col, cell)

        layout.addWidget(table, stretch=1)

        summary = QLabel(f"{len(items)} item(s), {total_deducting} total units to deduct")
        summary.setStyleSheet("font-weight: bold; margin-top: 8px;")
        layout.addWidget(summary)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        ok_btn = QPushButton("Deduct")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)


class DeductionSummaryDialog(QDialog):
    """Shows results after deduction is applied."""

    def __init__(
        self,
        result: DeductionResult,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("Deduction Complete")
        self.setMinimumWidth(400)
        self._setup_ui(result)

    def _setup_ui(self, result: DeductionResult) -> None:
        layout = QVBoxLayout(self)

        layout.addWidget(
            QLabel(f"Deducted {result.total_deducted} units across {len(result.rows)} item(s).")
        )
        if result.items_at_zero > 0:
            warn = QLabel(f"{result.items_at_zero} item(s) now at zero quantity.")
            warn.setStyleSheet("color: orange; font-weight: bold;")
            layout.addWidget(warn)

        table = QTableWidget(len(result.rows), 4)
        table.setHorizontalHeaderLabels(["Item", "Was", "Deducted", "Now"])
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for col in (1, 2, 3):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        table.verticalHeader().setVisible(False)

        for row_idx, r in enumerate(result.rows):
            for col, text in enumerate(
                [r.name, str(r.previous_qty), str(r.deducted), str(r.new_qty)]
            ):
                cell = QTableWidgetItem(text)
                cell.setFlags(cell.flags() & ~Qt.ItemFlag.ItemIsEditable)
                if col > 0:
                    cell.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                    )
                table.setItem(row_idx, col, cell)

        layout.addWidget(table, stretch=1)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)


class ShoppingListDialog(QDialog):
    """Shows a need/have/buy diff table comparing PO demand vs inventory."""

    def __init__(
        self,
        rows: list[ShoppingListRow],
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle("Check Inventory \u2014 Shopping List")
        self.setMinimumSize(550, 400)
        self._setup_ui(rows)

    def _setup_ui(self, rows: list[ShoppingListRow]) -> None:
        layout = QVBoxLayout(self)

        if not rows:
            layout.addWidget(
                QLabel(
                    "No matching items found.\n\n"
                    "Make sure the PO CSV items match known adventures, "
                    "and set up inventory via the Inventory menu."
                )
            )
            close_btn = QPushButton("Close")
            close_btn.clicked.connect(self.accept)
            layout.addWidget(close_btn)
            return

        layout.addWidget(QLabel("Compare what the PO needs against what you have in stock:"))

        table = QTableWidget(len(rows), 4)
        table.setHorizontalHeaderLabels(["Item", "Need", "Have", "Buy"])
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for col in (1, 2, 3):
            header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        table.verticalHeader().setVisible(False)

        covered_color = QColor(220, 245, 220)
        covered_text_color = QColor(100, 100, 100)

        items_to_buy = 0
        for row_idx, r in enumerate(rows):
            is_covered = r.buy == 0
            if not is_covered:
                items_to_buy += 1
            for col, text in enumerate([r.name, str(r.need), str(r.have), str(r.buy)]):
                cell = QTableWidgetItem(text)
                cell.setFlags(cell.flags() & ~Qt.ItemFlag.ItemIsEditable)
                if col > 0:
                    cell.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                    )
                if is_covered:
                    cell.setBackground(covered_color)
                    cell.setForeground(covered_text_color)
                table.setItem(row_idx, col, cell)

        layout.addWidget(table, stretch=1)

        total_buy = sum(r.buy for r in rows)
        if items_to_buy == 0:
            summary_text = "All items are fully covered by inventory!"
            summary_style = "color: green; font-weight: bold; margin-top: 8px;"
        else:
            summary_text = f"{items_to_buy} item(s) to purchase, {total_buy} total units needed."
            summary_style = "font-weight: bold; margin-top: 8px;"

        summary = QLabel(summary_text)
        summary.setStyleSheet(summary_style)
        layout.addWidget(summary)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)
