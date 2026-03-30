"""Main application window."""

from __future__ import annotations

import os

from PySide6.QtCore import QSettings, QUrl
from PySide6.QtGui import QAction, QDesktopServices
from PySide6.QtWidgets import (
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
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
from src.version import __version__


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Scout Advancement Labels")
        self.setMinimumSize(520, 460)
        self._settings = QSettings("ScoutAdvancement", "ScoutLabels")
        self._setup_menu()
        self._setup_ui()

    def _setup_menu(self) -> None:
        menu_bar = self.menuBar()

        # macOS puts "About" in the app menu automatically
        help_menu = menu_bar.addMenu("Help")
        about_action = QAction("About Scout Advancement Labels", self)
        about_action.setMenuRole(QAction.MenuRole.AboutRole)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _setup_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        header = QLabel("Scout Advancement Labels")
        header.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 4px;")
        layout.addWidget(header)

        subtitle = QLabel(
            "Select Scoutbook CSV exports (or drag and drop), "
            "then generate printable Avery 6427 labels."
        )
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

        last_dir = self._settings.value("last_save_dir", "")
        default_path = os.path.join(last_dir, "advancement_labels.pdf") if last_dir else "advancement_labels.pdf"

        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Labels PDF",
            default_path,
            "PDF Files (*.pdf)",
        )
        if not save_path:
            return

        # Remember the directory for next time
        self._settings.setValue("last_save_dir", os.path.dirname(save_path))

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

    def _show_about(self) -> None:
        QMessageBox.about(
            self,
            "About Scout Advancement Labels",
            f"<h3>Scout Advancement Labels</h3>"
            f"<p>Version {__version__}</p>"
            f"<p>Generates printable Avery 6427 labels from "
            f"Scoutbook advancement CSV exports.</p>"
            f"<p>Built for Cub Scout pack advancement chairs.</p>",
        )
