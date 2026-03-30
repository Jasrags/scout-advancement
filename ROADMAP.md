# Roadmap

## Versioning

This project uses [Semantic Versioning](https://semver.org/): `MAJOR.MINOR.PATCH`

- **MAJOR** — breaking changes to file format or workflow
- **MINOR** — new features (e.g., new label types, ceremony bundles)
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

---

## Post-MVP

### v0.4.0 — CI/CD & Release Automation
- [x] GitHub Actions CI pipeline (`.github/workflows/ci.yml`):
  - Lint (ruff) and type-check (mypy) on every push/PR
  - Run pytest with coverage gate (80%+ on `src/core`)
  - Fail PR if tests or coverage regress
- [x] Automated semantic versioning (`python-semantic-release`):
  - Version bumps derived from conventional commit prefixes (`feat:` → minor, `fix:` → patch, `feat!:` / `BREAKING CHANGE` → major)
  - Single source of truth remains `src/version.py`, auto-updated by CI
  - Git tags created on release (e.g., `v0.4.0`)
- [x] Automated macOS `.app` build in CI (PyInstaller on GitHub-hosted `macos-latest` runner)
- [x] GitHub Releases with attached `.app` zip artifact on each tagged version (`.github/workflows/release.yml`)
- [x] Changelog generation from conventional commits (auto-populated in release notes)
- [ ] Branch protection: require passing CI before merge to `main`
  - **Manual setup required** in GitHub → Settings → Branches → Add rule for `main`:
    - Require status checks: `Lint & Type Check`, `Test & Coverage`
    - Require branches to be up to date before merging
    - Optionally require PR reviews

### v1.0.0 — Bagging Guide & Release Pipeline
- [x] Bagging guide PDF generator:
  - Per-scout checklist with checkboxes, adventure loop/pin images, and Required/Elective tags
  - Adventure data for all 6 ranks (Lion through Arrow of Light) sourced from scouting.org
  - Images downloaded and cached locally from scouting.org WordPress API
  - Condensed layout — scouts flow continuously across pages to minimize paper usage
  - Scraper script (`scripts/fetch_adventures.py`) to refresh data when program year changes
- [x] GUI: "Generate Bagging Guide" button alongside existing "Generate Labels PDF"
- [x] Release pipeline fixed and tested end-to-end
- [x] Idempotent release workflow (handles re-runs without failing)

---

## Planned

### v1.1.0 — Configurable Labels
- [ ] Build a catalog of Avery label types in the same size range as 6427
- [ ] Let user select label type from a dropdown
- [ ] Editable label templates — customize which CSV columns appear on the label and how they are formatted (e.g., include/exclude den number, change name order, add date earned, show SKU)
- [ ] Preview label layout before printing

### v1.2.0 — Windows Support
- [ ] PyInstaller `.exe` build for Windows
- [ ] GitHub Actions matrix build for macOS + Windows
- [ ] Windows installer or portable `.exe`

### Backlog
- [ ] Pack ceremony bundles — bundle all Scoutbook outputs (PO CSV, PO PDF, Advancement Report) plus generated labels and bagging guide into a date-stamped folder
- [ ] Pack-wide inventory summary page (total item counts across all scouts)
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
