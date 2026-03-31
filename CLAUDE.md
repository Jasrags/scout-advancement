# Project: Scout Advancement Labels

Desktop app (PySide6) that generates printable Avery 6427 labels from Scoutbook CSV exports.

## Tech Stack

- Python 3.10+, PySide6 (GUI), ReportLab (PDF generation)
- PyInstaller for macOS .app and Windows .exe bundling
- pytest + pytest-cov for testing (80% coverage gate on `src/core`)

## Development Commands

A `Makefile` provides all common tasks:

```bash
make install    # create venv and install deps
make run        # launch the GUI
make test       # pytest with coverage (80% gate)
make lint       # ruff check + format check + mypy
make format     # auto-format with ruff
make build      # PyInstaller app (macOS .app / Windows .exe)
make release    # trigger GitHub release workflow
make clean      # remove build artifacts and caches
make help       # list all targets
```

## Versioning

Version lives in `src/version.py` (single source of truth). **Never edit it manually** — `python-semantic-release` updates it automatically during the release workflow.

### Commit prefix → version bump

- `fix:` / `perf:` → patch (1.0.0 → 1.0.1)
- `feat:` → minor (1.0.0 → 1.1.0)
- `feat!:` or `BREAKING CHANGE` footer → major (1.0.0 → 2.0.0)
- `docs:`, `test:`, `chore:`, `ci:`, `refactor:` → no version bump

### Release process

Releases are triggered manually via the GitHub Actions "Release" workflow (`gh workflow run release.yml` or Actions tab). The workflow:

1. Runs CI (lint, type-check, tests)
2. Determines version bump from commit history
3. Updates `src/version.py`, commits, and tags
4. Builds macOS `.app` and Windows `.exe` on platform-specific runners
5. Creates a GitHub Release with both platform zips and changelog

## Project Structure

```
src/
  core/           # CSV parsing + PDF label generation (tested, 80%+ coverage)
  gui/            # PySide6 GUI (main_window, file_list_widget)
  main.py         # GUI entry point
  version.py      # Version (auto-managed by semantic-release)
tests/            # pytest tests for src/core
scripts/build.sh  # PyInstaller build script (macOS/Linux)
scripts/build.ps1 # PyInstaller build script (Windows)
packaging/        # .spec file and platform icons (.icns, .ico)
sample_data/      # Example CSVs for testing
```

## CI/CD

- `.github/workflows/ci.yml` — runs on push/PR to main: ruff, mypy, pytest (ubuntu + windows matrix)
- `.github/workflows/release.yml` — manual trigger: semantic-release + macOS/Windows builds + GitHub Release
