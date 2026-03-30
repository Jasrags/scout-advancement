# Project: Scout Advancement Labels

Desktop app (PySide6) that generates printable Avery 6427 labels from Scoutbook CSV exports.

## Tech Stack

- Python 3.10+, PySide6 (GUI), ReportLab (PDF generation)
- PyInstaller for macOS .app bundling
- pytest + pytest-cov for testing (80% coverage gate on `src/core`)

## Development Commands

```bash
source .venv/bin/activate
ruff check src/ tests/          # lint
ruff format src/ tests/         # auto-format
mypy src/                       # type-check
python -m pytest --cov=src/core --cov-report=term-missing  # test
bash scripts/build.sh           # build macOS .app
```

## Versioning

Version lives in `src/version.py` (single source of truth). **Never edit it manually** — `python-semantic-release` updates it automatically during the release workflow.

### Commit prefix → version bump

- `fix:` / `perf:` → patch (0.4.0 → 0.4.1)
- `feat:` → minor (0.4.1 → 0.5.0)
- `feat!:` or `BREAKING CHANGE` footer → major (0.x → 1.0.0)
- `docs:`, `test:`, `chore:`, `ci:`, `refactor:` → no version bump

**Important:** `major_on_zero = false` is set in `pyproject.toml`, so `feat:` on `0.x` bumps minor only. A major bump to `1.0.0` requires an explicit breaking change marker.

### Release process

Releases are triggered manually via the GitHub Actions "Release" workflow (`gh workflow run release.yml` or Actions tab). The workflow:

1. Runs CI (lint, type-check, tests)
2. Determines version bump from commit history
3. Updates `src/version.py`, commits, and tags
4. Builds macOS `.app` on a GitHub runner
5. Creates a GitHub Release with the `.app` zip and changelog

## Project Structure

```
src/
  core/           # CSV parsing + PDF label generation (tested, 80%+ coverage)
  gui/            # PySide6 GUI (main_window, file_list_widget)
  main.py         # GUI entry point
  version.py      # Version (auto-managed by semantic-release)
tests/            # pytest tests for src/core
scripts/build.sh  # PyInstaller build script
packaging/        # .spec file and app icon
sample_data/      # Example CSVs for testing
```

## CI/CD

- `.github/workflows/ci.yml` — runs on push/PR to main: ruff, mypy, pytest
- `.github/workflows/release.yml` — manual trigger: semantic-release + macOS build + GitHub Release
