"""Main application window."""

from __future__ import annotations

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.core.label_generator import (
    CSVColumnError,
    CSVReadError,
    GenerationResult,
    generate_pdf,
    read_advancements,
)
from src.gui.file_list_widget import FileListWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Scout Advancement Labels")
        self.setMinimumSize(520, 460)
        self._setup_ui()

    def _setup_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        header = QLabel("Scout Advancement Labels")
        header.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 4px;")
        layout.addWidget(header)

        subtitle = QLabel("Select Scoutbook CSV exports, then generate printable Avery 6427 labels.")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        self._file_list = FileListWidget()
        self._file_list.files_changed.connect(self._on_files_changed)
        layout.addWidget(self._file_list, stretch=1)

        self._generate_btn = QPushButton("Generate Labels PDF")
        self._generate_btn.setEnabled(False)
        self._generate_btn.setMinimumHeight(36)
        self._generate_btn.clicked.connect(self._on_generate)
        layout.addWidget(self._generate_btn)

        self._status = QTextEdit()
        self._status.setReadOnly(True)
        self._status.setMaximumHeight(120)
        self._status.setPlaceholderText("Status messages will appear here...")
        layout.addWidget(self._status)

    def _on_files_changed(self, valid_count: int) -> None:
        self._generate_btn.setEnabled(valid_count > 0)

    def _on_generate(self) -> None:
        file_paths = self._file_list.get_valid_file_paths()
        if not file_paths:
            return

        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Labels PDF",
            "advancement_labels.pdf",
            "PDF Files (*.pdf)",
        )
        if not save_path:
            return

        self._status.clear()
        self._status.append(f"Processing {len(file_paths)} file(s)...")

        try:
            scouts = read_advancements(file_paths)
            result: GenerationResult = generate_pdf(scouts, save_path)
            self._status.append(
                f"Generated {result.label_count} labels on "
                f"{result.page_count} page(s)."
            )
            self._status.append(f"Saved to: {result.output_path}")
            QDesktopServices.openUrl(QUrl.fromLocalFile(result.output_path))
        except (CSVReadError, CSVColumnError) as e:
            self._status.append(f"Error: {e}")
        except OSError as e:
            self._status.append(f"Error writing PDF: {e}")
