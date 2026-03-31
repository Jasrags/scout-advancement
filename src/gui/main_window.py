"""Main application window."""

from __future__ import annotations

import os

from PySide6.QtCore import QSettings, QUrl
from PySide6.QtGui import QAction, QDesktopServices
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from src.core.bagging_guide import BaggingGuideResult, generate_bagging_guide
from src.core.label_generator import (
    CSVColumnError,
    CSVReadError,
    GenerationResult,
    generate_pdf,
    read_advancements,
)
from src.core.label_spec import (
    DEFAULT_LABEL_SPEC,
    LABEL_CATALOG,
    LabelSpec,
    LabelTemplate,
    get_label_spec,
)
from src.gui.file_list_widget import FileListWidget
from src.gui.label_preview import LabelPreviewDialog
from src.gui.label_settings import LabelSettingsDialog, load_template_from_settings
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
            "then generate printable labels or a bagging guide."
        )
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        self._file_list = FileListWidget()
        self._file_list.files_changed.connect(self._on_files_changed)
        layout.addWidget(self._file_list, stretch=1)

        # Label type selector
        label_layout = QHBoxLayout()
        label_layout.addWidget(QLabel("Label type:"))
        self._label_combo = QComboBox()
        for spec in LABEL_CATALOG:
            self._label_combo.addItem(f"{spec.name} — {spec.description}", spec.name)
        saved_label = str(self._settings.value("label_type", DEFAULT_LABEL_SPEC.name))
        idx = self._label_combo.findData(saved_label)
        if idx >= 0:
            self._label_combo.setCurrentIndex(idx)
        self._label_combo.currentIndexChanged.connect(self._on_label_type_changed)
        label_layout.addWidget(self._label_combo, stretch=1)

        self._settings_btn = QPushButton("Settings...")
        self._settings_btn.clicked.connect(self._on_settings)
        label_layout.addWidget(self._settings_btn)

        layout.addLayout(label_layout)

        # Action buttons
        btn_layout = QHBoxLayout()

        self._preview_btn = QPushButton("Preview")
        self._preview_btn.setEnabled(False)
        self._preview_btn.setMinimumHeight(36)
        self._preview_btn.clicked.connect(self._on_preview)
        btn_layout.addWidget(self._preview_btn)

        self._generate_btn = QPushButton("Generate Labels PDF")
        self._generate_btn.setEnabled(False)
        self._generate_btn.setMinimumHeight(36)
        self._generate_btn.clicked.connect(self._on_generate)
        btn_layout.addWidget(self._generate_btn)

        self._bagging_btn = QPushButton("Generate Bagging Guide")
        self._bagging_btn.setEnabled(False)
        self._bagging_btn.setMinimumHeight(36)
        self._bagging_btn.clicked.connect(self._on_generate_bagging_guide)
        btn_layout.addWidget(self._bagging_btn)

        layout.addLayout(btn_layout)

        self._status = QTextEdit()
        self._status.setReadOnly(True)
        self._status.setMaximumHeight(120)
        self._status.setPlaceholderText("Status messages will appear here...")
        layout.addWidget(self._status)

    def _on_files_changed(self, valid_count: int) -> None:
        has_files = valid_count > 0
        self._preview_btn.setEnabled(has_files)
        self._generate_btn.setEnabled(has_files)
        self._bagging_btn.setEnabled(has_files)

    def _on_label_type_changed(self, _index: int) -> None:
        name = self._label_combo.currentData()
        self._settings.setValue("label_type", name)

    def _on_settings(self) -> None:
        dialog = LabelSettingsDialog(self._settings, parent=self)
        dialog.exec()

    def _selected_label_spec(self) -> LabelSpec:
        name = self._label_combo.currentData()
        return get_label_spec(name) or DEFAULT_LABEL_SPEC

    def _selected_template(self) -> LabelTemplate:
        return load_template_from_settings(self._settings)

    def _on_preview(self) -> None:
        file_paths = self._file_list.get_valid_file_paths()
        if not file_paths:
            return

        try:
            scouts = read_advancements(file_paths)
            spec = self._selected_label_spec()
            tmpl = self._selected_template()
            dialog = LabelPreviewDialog(scouts, spec, tmpl, parent=self)
            dialog.exec()
        except (CSVReadError, CSVColumnError) as e:
            self._status.clear()
            self._status.append(f"Error: {e}")

    def _on_generate(self) -> None:
        file_paths = self._file_list.get_valid_file_paths()
        if not file_paths:
            return

        last_dir = str(self._settings.value("last_save_dir", ""))
        default_name = "advancement_labels.pdf"
        default_path = os.path.join(last_dir, default_name) if last_dir else default_name

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

        spec = self._selected_label_spec()
        tmpl = self._selected_template()
        self._status.clear()
        self._status.append(f"Processing {len(file_paths)} file(s) with {spec.name}...")

        try:
            scouts = read_advancements(file_paths)
            result: GenerationResult = generate_pdf(
                scouts, save_path, label_spec=spec, label_template=tmpl
            )
            self._status.append(
                f"Generated {result.label_count} labels on {result.page_count} page(s)."
            )
            self._status.append(f"Saved to: {result.output_path}")
            QDesktopServices.openUrl(QUrl.fromLocalFile(result.output_path))
        except (CSVReadError, CSVColumnError) as e:
            self._status.append(f"Error: {e}")
        except OSError as e:
            self._status.append(f"Error writing PDF: {e}")

    def _on_generate_bagging_guide(self) -> None:
        file_paths = self._file_list.get_valid_file_paths()
        if not file_paths:
            return

        last_dir = str(self._settings.value("last_save_dir", ""))
        default_name = "bagging_guide.pdf"
        default_path = os.path.join(last_dir, default_name) if last_dir else default_name

        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Bagging Guide PDF",
            default_path,
            "PDF Files (*.pdf)",
        )
        if not save_path:
            return

        self._settings.setValue("last_save_dir", os.path.dirname(save_path))

        self._status.clear()
        self._status.append(f"Processing {len(file_paths)} file(s)...")
        self._status.append("Downloading adventure images (first run may take a moment)...")

        try:
            scouts = read_advancements(file_paths)
            result: BaggingGuideResult = generate_bagging_guide(scouts, save_path)
            self._status.append(
                f"Generated bagging guide for {result.scout_count} scout(s) "
                f"on {result.page_count} page(s)."
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
            f"<p>Generates printable Avery labels from "
            f"Scoutbook advancement CSV exports.</p>"
            f"<p>Built for Cub Scout pack advancement chairs.</p>",
        )
