# Roadmap

## Versioning

This project uses [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`

- **MAJOR** — breaking changes to file format or workflow
- **MINOR** — new features (e.g., new label types, inventory, email tools)
- **PATCH** — bug fixes and minor improvements

The version is defined in `src/version.py` (single source of truth) and displayed in the app's About dialog. Version bumps are automated via conventional commits and `python-semantic-release` in CI.

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

### v0.2.0 — Core Refactor + GUI
- [x] Extract label generation into reusable library (`src/core/`)
- [x] CSV validation before processing
- [x] Custom exceptions instead of `sys.exit`
- [x] PySide6 GUI with file picker, generate button, status area
- [x] Auto-open PDF after generation
- [x] Unit tests (97% core coverage)
- [x] Handle plural den type names (lions, tigers, wolves, bears)
- [x] Handle AOL variations in sort order

### v0.3.0 — MVP Standalone App
- [x] PyInstaller standalone `.app` for macOS (110MB bundle)
- [x] App icon (BSA green + gold star)
- [x] Build script for reproducible builds (`scripts/build.sh`)
- [x] Drag-and-drop CSV files onto the window
- [x] Remember last-used save directory
- [x] About dialog showing version number
- [x] Version module (`src/version.py`) as single source of truth

### v0.4.0 — CI/CD & Release Automation
- [x] GitHub Actions CI pipeline (lint, type-check, test with coverage gate)
- [x] Automated semantic versioning via conventional commits
- [x] Automated macOS `.app` build in CI
- [x] GitHub Releases with attached artifacts
- [x] Changelog generation from conventional commits
- [ ] Branch protection (manual setup required in GitHub settings)

### v1.0.0 — Bagging Guide & Release Pipeline
- [x] Bagging guide PDF generator with adventure loop/pin images
- [x] Adventure data for all 6 ranks (Lion through Arrow of Light)
- [x] Condensed layout — scouts flow continuously across pages
- [x] Scraper script (`scripts/fetch_adventures.py`) for data refresh
- [x] GUI: "Generate Bagging Guide" button
- [x] Release pipeline tested end-to-end

### v1.1.0 — Configurable Labels
- [x] Catalog of Avery label types (6427, 5163, 8163, 5164, 5162, 5160)
- [x] Label type dropdown selector
- [x] Editable label templates (name order, den number, date earned, SKU)
- [x] Preview label layout before printing

### v1.2.0 — Windows Support
- [x] PyInstaller `.exe` build for Windows
- [x] GitHub Actions matrix build for macOS + Windows
- [x] VC++ runtime DLLs bundled in Windows build

---

## In Progress

### v1.3.0 — Award Inventory ([milestone](https://github.com/Jasrags/scout-advancement/milestone/4))
- [x] Inventory data model with JSON persistence (#19)
- [x] Per-rank inventory UI with adventure images and +/- controls (#20)
- [x] Auto-populate inventory from PO CSV imports (#21)
- [x] Auto-decrement inventory after bagging (#22)
- [x] Shopping list diff — need/have/buy comparison (#23)
- [x] Bundle all 139 adventure loop/pin images locally
- [ ] Adventure version selector — program year dropdown (#26)

---

## Planned

### v1.4.0 — Pack Tools ([milestone](https://github.com/Jasrags/scout-advancement/milestone/5))
- [ ] Add rank patch icons to the bagging guide (#28)
- [ ] Generate scout shop purchase email with inventory-aware pull list (#29)
- [ ] Import/export inventory file (#30)
- [ ] Generate advancement reminder email for den leaders (#31)

### Backlog
- [ ] Pack ceremony bundles — bundle all outputs into a date-stamped folder (#7)
- [ ] Pack-wide inventory summary page (#8)
- [ ] Auto-update check (#9)
- [ ] Code signing for macOS and Windows (#10)
- [ ] DMG installer with drag-to-Applications (#11)
- [ ] User documentation / quick-start guide (#12)

---

## Known Considerations

- **Den numbers** shift by pack and over time — read from CSV dynamically, never hardcoded
- **AOL representation** varies across packs — the sort map handles known variations but may need updates
- **Scoutbook export format** may change — the CSV validator provides clear error messages when columns don't match
- **Adventure images** are bundled locally in `packaging/images/` — when BSA changes the program year, new images need to be downloaded and a new version added (see #26)

## Advancement Workflow Reference

See the [Advancement Chair Guide](ONBOARDING.md) for the complete monthly ceremony workflow, or the [README](README.md) for a summary.

## References

- [Guide to Advancement 2025 — Scouting America](https://www.scouting.org/resources/guide-to-advancement/)
- [Guidelines for Advancement Committees](https://www.scouting.org/resources/guide-to-advancement/guidelines-for-advancement/)
- [Scoutbook Knowledge Base](https://help.scoutbook.scouting.org/knowledge-base/getting-a-unit-started-in-scoutbook/)
- [BSA Advancement Report Form (SKU 34403)](https://filestore.scouting.org/filestore/pdf/34403.pdf)
