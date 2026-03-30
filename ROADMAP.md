# Roadmap

## Versioning

This project uses [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`

- **MAJOR** — breaking changes to file format or workflow
- **MINOR** — new features (e.g., new label types, ceremony bundles)
- **PATCH** — bug fixes and minor improvements

The version is defined in `pyproject.toml` and will be displayed in the app's About dialog.

---

## Completed

### v0.1.0 — CLI Foundation
- [x] CSV parser for Scoutbook advancement exports
- [x] Avery 6427 label PDF generation (2" x 4", 10 per sheet)
- [x] Multi-file input with scout deduplication
- [x] Den type sort order: Lion → Tiger → Wolf → Bear → Webelos → AOL
- [x] Alphabetical sort within each den
- [x] Word-wrapping for long award lists
- [x] Sample data with fictitious scouts for testing

### v0.2.0 — Core Refactor + GUI (in progress)
- [x] Extract label generation into reusable library (`src/core/`)
- [x] CSV validation before processing
- [x] Custom exceptions instead of `sys.exit`
- [x] PySide6 GUI with file picker, generate button, status area
- [x] Auto-open PDF after generation
- [x] Unit tests (97% core coverage)
- [x] Handle plural den type names (lions, tigers, wolves, bears)
- [x] Handle AOL variations in sort order

---

## MVP — v0.3.0

### Packaging
- [ ] PyInstaller standalone `.app` for macOS
- [ ] App icon
- [ ] Build script for reproducible builds
- [ ] Test on clean Mac (no Python installed)
- [ ] Document Gatekeeper workaround (right-click → Open)

### Usability
- [ ] Drag-and-drop CSV files onto the window
- [ ] Remember last-used save directory
- [ ] About dialog showing version number

---

## Post-MVP

### v0.4.0 — Configurable Labels
- [ ] Build a catalog of Avery label types in the same size range as 6427
- [ ] Let user select label type from a dropdown
- [ ] Editable label templates — customize which CSV columns appear on the label and how they are formatted (e.g., include/exclude den number, change name order, add date earned, show SKU)
- [ ] Preview label layout before printing

### v0.5.0 — Pack Ceremony Bundles
- [ ] Create a "ceremony day" bundle containing all Scoutbook outputs plus generated labels:
  - Purchase Order CSV (`PO_P####FP_######.csv`) — source data
  - Purchase Order PDF (`PO_P####FP_######.pdf`) — item order list for scout shop
  - Advancement Report PDF (`Advancement_Report_*.pdf`) — official BSA form for Council
  - Generated label PDF — output from this tool
- [ ] Pre-defined folder structure for saving ceremony bundles (e.g., `YYYY-MM-DD - Ceremony/`)
- [ ] Date-stamped output directories

### v0.6.0 — Windows Support
- [ ] PyInstaller `.exe` build for Windows
- [ ] GitHub Actions CI for cross-platform builds
- [ ] Windows installer or portable `.exe`

### v1.0.0 — Production Release
- [ ] Auto-update check (notify when new version is available)
- [ ] Code signing for macOS (Developer ID) and Windows
- [ ] DMG installer with drag-to-Applications
- [ ] User documentation / quick-start guide for new advancement chairs

---

## Known Considerations

- **Den numbers** shift by pack and over time — they are read from the CSV dynamically, never hardcoded
- **AOL representation** varies across packs: sometimes "Webelo 2 (AOL)", sometimes "Arrow of Light (AOL)" — the sort map handles known variations but may need updates
- **Scoutbook export format** may change over time — the CSV validator provides clear error messages when columns don't match

## Advancement Workflow Reference

For the full workflow detail, see the [Scoutbook Advancement Process](README.md#scoutbook-advancement-process) section in the README.

In short: Den leaders record → Scoutmaster approves → Advancement Chair creates purchase order → downloads CSV/PDFs → submits to scout shop → **this tool generates labels from the CSV** → awards presented at ceremony → PO closed in Scoutbook.

## References

- [Guide to Advancement 2025 — Scouting America](https://www.scouting.org/resources/guide-to-advancement/)
- [Guidelines for Advancement Committees](https://www.scouting.org/resources/guide-to-advancement/guidelines-for-advancement/)
- [Scoutbook Knowledge Base](https://help.scoutbook.scouting.org/knowledge-base/getting-a-unit-started-in-scoutbook/)
- [BSA Advancement Report Form (SKU 34403)](https://filestore.scouting.org/filestore/pdf/34403.pdf)
