"""Label preview widget and dialog.

Renders a scaled preview of one page of labels using QPainter,
matching the layout from label_generator.py.
"""

from __future__ import annotations

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QFont, QFontMetricsF, QPainter, QPen
from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.core.label_generator import ScoutRecord
from src.core.label_spec import LabelSpec

# US Letter in points (same as reportlab)
_PAGE_W = 612.0  # 8.5 * 72
_PAGE_H = 792.0  # 11 * 72

# Text padding inside each label (matches label_generator.py)
_PAD_LEFT = 10.8  # 0.15 * 72
_PAD_TOP = 10.8
_PAD_RIGHT = 10.8
_PAD_BOTTOM = 7.2  # 0.1 * 72

# Reference font sizes (at 2" label height)
_NAME_SIZE = 11.0
_AWARDS_SIZE = 8.0


def _scaled_fonts(spec: LabelSpec) -> tuple[float, float]:
    """Return (name_size, awards_size) scaled to label height."""
    ref = 144.0  # 2 inches in points
    scale = min(spec.label_height / ref, 1.0)
    return max(_NAME_SIZE * scale, 6.0), max(_AWARDS_SIZE * scale, 5.0)


class LabelPreviewWidget(QWidget):
    """Paints a scaled preview of one page of labels."""

    def __init__(
        self,
        scouts: list[ScoutRecord],
        spec: LabelSpec,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._scouts = scouts[: spec.labels_per_page]  # first page only
        self._spec = spec
        # Set a fixed aspect ratio matching US Letter
        self.setMinimumSize(400, 518)  # ~400 wide, letter ratio

    def paintEvent(self, _event: object) -> None:  # type: ignore[override]
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Scale from page points to widget pixels
        w = self.width()
        h = self.height()
        sx = w / _PAGE_W
        sy = h / _PAGE_H
        scale = min(sx, sy)

        # Center the page in the widget
        offset_x = (w - _PAGE_W * scale) / 2
        offset_y = (h - _PAGE_H * scale) / 2

        painter.translate(offset_x, offset_y)
        painter.scale(scale, scale)

        # Draw page background
        painter.fillRect(QRectF(0, 0, _PAGE_W, _PAGE_H), QColor(255, 255, 255))

        # Draw page border
        painter.setPen(QPen(QColor(200, 200, 200), 0.5))
        painter.drawRect(QRectF(0, 0, _PAGE_W, _PAGE_H))

        spec = self._spec
        name_size, awards_size = _scaled_fonts(spec)

        for idx in range(spec.labels_per_page):
            col = idx % spec.columns
            row = idx // spec.columns
            lx = spec.left_margin + col * (spec.label_width + spec.h_gap)
            # QPainter y goes down from top (unlike reportlab which goes up)
            ly = spec.top_margin + row * (spec.label_height + spec.v_gap)

            label_rect = QRectF(lx, ly, spec.label_width, spec.label_height)

            # Label border (dashed to indicate cut lines)
            painter.setPen(QPen(QColor(180, 180, 180), 0.5, Qt.PenStyle.DashLine))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(label_rect)

            if idx < len(self._scouts):
                self._draw_label(painter, lx, ly, self._scouts[idx], name_size, awards_size)

        painter.end()

    def _draw_label(
        self,
        p: QPainter,
        x: float,
        y: float,
        scout: ScoutRecord,
        name_size: float,
        awards_size: float,
    ) -> None:
        spec = self._spec
        text_x = x + _PAD_LEFT
        usable_w = spec.label_width - _PAD_LEFT - _PAD_RIGHT
        label_bottom = y + spec.label_height - _PAD_BOTTOM

        # Scout name
        den_display = scout.den_type.title()
        name_line = f"{scout.first} {scout.last} [{den_display} ({scout.den_num})]"

        name_font = QFont("Helvetica", int(name_size))
        name_font.setBold(True)
        p.setFont(name_font)
        p.setPen(QPen(QColor(0, 0, 0)))

        fm = QFontMetricsF(name_font)
        # Truncate if needed
        name_line = fm.elidedText(name_line, Qt.TextElideMode.ElideRight, usable_w)

        text_y = y + _PAD_TOP + fm.ascent()
        p.drawText(QRectF(text_x, y + _PAD_TOP, usable_w, fm.height()), 0, name_line)

        # Awards
        awards_text = ", ".join(scout.items)
        awards_font = QFont("Helvetica", int(awards_size))
        p.setFont(awards_font)
        afm = QFontMetricsF(awards_font)

        line_h = afm.height()
        current_y = text_y + fm.descent() + 2

        # Word-wrap awards
        words = awards_text.split()
        current_line = ""
        for word in words:
            test = f"{current_line} {word}".strip() if current_line else word
            if afm.horizontalAdvance(test) <= usable_w:
                current_line = test
            else:
                if current_line and current_y + line_h <= label_bottom:
                    p.drawText(QRectF(text_x, current_y, usable_w, line_h), 0, current_line)
                    current_y += line_h
                current_line = word
            if current_y + line_h > label_bottom:
                break
        # Draw remaining line
        if current_line and current_y + line_h <= label_bottom:
            p.drawText(QRectF(text_x, current_y, usable_w, line_h), 0, current_line)


class LabelPreviewDialog(QDialog):
    """Dialog showing a label preview with page info."""

    def __init__(
        self,
        scouts: list[ScoutRecord],
        spec: LabelSpec,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setWindowTitle(f"Label Preview — {spec.name}")
        self.setMinimumSize(480, 660)
        self.resize(520, 700)

        layout = QVBoxLayout(self)

        # Info bar
        total = len(scouts)
        per_page = spec.labels_per_page
        pages = (total + per_page - 1) // per_page if total else 0
        showing = min(total, per_page)
        info = QLabel(
            f"{spec.name} — {total} label{'s' if total != 1 else ''}, "
            f"{pages} page{'s' if pages != 1 else ''} "
            f"(showing first {showing})"
        )
        info.setStyleSheet("color: #555; margin-bottom: 4px;")
        layout.addWidget(info)

        # Preview widget
        preview = LabelPreviewWidget(scouts, spec)
        layout.addWidget(preview, stretch=1)

        # Close button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)
