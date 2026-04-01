# Scout Advancement Labels

A desktop app that turns Scoutbook advancement CSVs into printable Avery labels and bagging guides with adventure loop/pin images, plus optional award inventory tracking. Built for Cub Scout pack advancement chairs.

**New to the advancement chair role?** See the [Advancement Chair Guide](ONBOARDING.md) for a complete walkthrough.

## Quick Start

Download the latest release from [GitHub Releases](../../releases):

- **macOS** — download the `-macos.zip`, unzip, and drag to Applications
- **Windows** — download the `-windows.zip`, unzip, and run `Scout Advancement Labels.exe`

Open the app, drop your CSV files, and click **Generate Labels PDF** or **Generate Bagging Guide**.

## Features

- **Label generation** — printable Avery labels (6427, 5163, 8163, 5164, 5162, 5160) with configurable templates
- **Bagging guide** — per-scout checklist with adventure loop/pin images and Required/Elective tags
- **Award inventory** — track leftover awards by rank, check what to buy vs what's in stock, deduct after bagging
- **Label preview** — see how labels will look before printing
- **Multi-file support** — load multiple PO CSVs with automatic scout deduplication
- **Cross-platform** — macOS and Windows

## Monthly Ceremony Workflow

This tool supports steps 5-11 of the monthly advancement ceremony process:

1. Den leaders track progress in Scoutbook
2. Scoutmaster approves advancements
3. Advancement chair sends reminder email to den leaders
4. Advancement chair creates purchase order in Scoutbook, downloads CSV/PDFs
5. **Emails scout shop** with PO and advancement report PDFs
6. **Loads PO CSV into this app**
7. **Checks inventory** — sees what to buy vs what's in stock
8. Picks up awards from scout shop (only buying what's needed)
9. **Generates labels + bagging guide PDFs**
10. Bags awards using the bagging guide
11. **Deducts from inventory** after bagging
12. Holds ceremony, hands out bags

For the complete workflow with templates and screenshots, see the [Advancement Chair Guide](ONBOARDING.md).

## Development Setup

Requires Python 3.10+ and `make`.

```bash
make install    # create venv and install deps
make run        # launch the GUI
```

### Common Commands

```bash
make test       # run tests with 80% coverage gate
make lint       # ruff check + format check + mypy
make format     # auto-format code
make build      # build app (macOS .app / Windows .exe)
make release    # trigger GitHub release workflow
make clean      # remove build artifacts and caches
make help       # list all targets
```

## CI/CD

GitHub Actions runs on every push and PR to `main`:

- **Lint & Type Check** — ruff + mypy
- **Test & Coverage** — pytest with 80% coverage gate on `src/core` (ubuntu + windows matrix)

On merge to `main`, if conventional commits indicate a version bump (`feat:` → minor, `fix:` → patch), the release workflow automatically:
1. Bumps `src/version.py` and creates a git tag
2. Builds the macOS `.app` and Windows `.exe` on platform-specific runners
3. Creates a GitHub Release with both platform zips and changelog

Versioning is managed by [python-semantic-release](https://python-semantic-release.readthedocs.io/). The release workflow is manual — trigger it from the Actions tab or via `gh workflow run release.yml`.

### Version Bumps via Commit Prefixes

| Commit prefix | Version bump | Example |
|---------------|-------------|---------|
| `fix:` | Patch (1.0.0 → 1.0.1) | `fix: handle empty CSV gracefully` |
| `feat:` | Minor (1.0.0 → 1.1.0) | `feat: add inventory management` |
| `feat!:` or `BREAKING CHANGE` | Major (1.0.0 → 2.0.0) | `feat!: new CSV format` |
| `docs:`, `test:`, `chore:`, `ci:`, `refactor:` | No bump | `docs: update README` |

## Input Format

Your input CSV must have these columns (other columns are ignored):
- `First Name`
- `Last Name`
- `Den Type`
- `Den Number`
- `Item Name`

The `sample_data/` directory contains example CSVs with fictitious scout names for testing. These match the format exported by Scoutbook.

Example input:
```csv
First Name,Last Name,Den Type,Den Number,Quantity,SKU,Item Type,Price,Item Name,Date Earned
Liam,Carter,lions,2,1,646404,Adventure,2.19,Fun on the Run Adventure,2025-11-15
Liam,Carter,lions,2,1,646406,Adventure,2.19,Mountain Lion Adventure,2025-12-10
```

## Output

### PDF Labels

Produces a print-ready PDF with Avery shipping labels. Each label contains:

```
First Last [Den Type (Den #)]
Award 1, Award 2, Award 3...
```

### Bagging Guide

Produces a PDF checklist to help volunteers bag the correct adventure loops and pins for each scout. Each entry shows a checkbox, the adventure loop/pin image, and the adventure name with a Required/Elective tag. Scouts flow continuously across pages to minimize paper usage.

### Sort Order

Scouts are automatically grouped by den type in rank order:
1. Lion (kindergarten)
2. Tiger (1st grade)
3. Wolf (2nd grade)
4. Bear (3rd grade)
5. Webelos (4th grade)
6. Webelos 2 / Arrow of Light (5th grade)

Within each den type, scouts are sorted alphabetically by last name, then first name.

## Roadmap

See [ROADMAP.md](ROADMAP.md) for planned features and release milestones.

## Troubleshooting

**"Could not find input file"**
- Make sure your CSV file path is correct

**"Missing required column in CSV"**
- Verify your CSV has the exact column names: `First Name`, `Last Name`, `Den Type`, `Item Name`
- Check for extra spaces in column headers

**Adventure images not showing**
- Make sure the app was installed correctly with the `packaging/images/` directory
