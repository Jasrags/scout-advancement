# Scout Advancement Labels

A desktop app that turns Scoutbook advancement CSVs into printable Avery 6427 shipping labels (2" x 4", 10 per sheet) and bagging guides with adventure loop/pin images, grouped and sorted by den.

## Quick Start

Download the latest release from [GitHub Releases](../../releases):

- **macOS** — download the `-macos.zip`, unzip, and drag to Applications
- **Windows** — download the `-windows.zip`, unzip, and run `Scout Advancement Labels.exe`

Open the app, drop your CSV files, and click **Generate Labels PDF** or **Generate Bagging Guide**.

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

### Run from CLI (legacy)

```bash
python generate_labels_pdf.py <input1.csv> [input2.csv ...] [-o output.pdf]
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

Version bumps are determined by conventional commit prefixes. Use the right prefix and the version updates automatically on release:

| Commit prefix | Version bump | Example |
|---------------|-------------|---------|
| `fix:` | Patch (1.0.0 → 1.0.1) | `fix: handle empty CSV gracefully` |
| `perf:` | Patch (1.0.0 → 1.0.1) | `perf: reduce PDF generation time` |
| `feat:` | Minor (1.0.0 → 1.1.0) | `feat: add ceremony bundle export` |
| `feat!:` or `BREAKING CHANGE` | Major (1.0.0 → 2.0.0) | `feat!: new CSV format` |
| `docs:`, `test:`, `chore:`, `ci:`, `refactor:` | No bump | `docs: update README` |

The single source of truth for the version is `src/version.py` — do not edit it manually; let semantic-release handle it.

## Scoutbook Advancement Process

This tool works with documents exported from [Scoutbook (advancements.scouting.org)](https://advancements.scouting.org), Scouting America's online advancement tracking system. For the full official guide, see the [Guide to Advancement](https://www.scouting.org/resources/guide-to-advancement/).

### Roles

| Role | Responsibility |
|------|---------------|
| **Den Leader** | Records scout awards as they are earned in Scoutbook |
| **Scoutmaster / Unit Admin** | Approves advancement entries submitted by den leaders |
| **Advancement Chair** | Creates purchase orders, submits to the scout shop, generates labels for ceremonies |

### End-to-End Workflow

1. **Record** — Den leaders enter advancements in Scoutbook as scouts earn them
2. **Approve** — In Scoutbook, go to the "To Approve" tab → select item category → check off advancements → click "Approve Items"
3. **Purchase** — Go to the "To Purchase" tab (shows all approved but not yet awarded items) → check items → click "Add items to order"
4. **View Order** — Click "View Order" at the bottom of the page → download the Purchase Order and Advancement Report
5. **Submit** — Email the PO PDF and Advancement Report to the local scout shop (they typically have the order ready within 24 hours), or bring them in person
6. **Generate Labels** — Feed the Purchase Order CSV into this tool to generate printable labels
7. **Ceremony** — Present awards to scouts at the pack meeting
8. **Close** — Back in Scoutbook, close the purchase order and mark advancements as "awarded"

### Scoutbook Export Documents

When an Advancement Chair creates and views a purchase order, Scoutbook generates three documents:

**Purchase Order CSV** (`PO_P####FP_######.csv`)
The **input** to this tool. One row per scout per award. Contains columns for scout name, den type, den number, SKU, item name, price, and date earned.

**Purchase Order PDF** (`PO_P####FP_######.pdf`)
A formatted shopping list organized by SKU. Shows quantity, item name, unit price, and total price for each award type, with scout names listed underneath each item. Includes a subtotal. This is what the scout shop uses to pull the order.

**Advancement Report PDF** (`Advancement_Report_*.pdf`)
The official BSA advancement report form ([SKU 34403](https://filestore.scouting.org/filestore/pdf/34403.pdf)). Contains pack information (number, district, leader, address), a numbered list of all scouts and their awards with dates earned, signature lines for the Advancement Committee, and a summary of total youth and total awards. This is the formal record submitted to the Council Service Center and must be signed by the pack leader.

## Input Format

Your input CSV must have these columns (other columns are ignored):
- `First Name`
- `Last Name`
- `Den Type`
- `Den Number` (used by PDF generator)
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

Produces a print-ready PDF with Avery 6427 shipping labels. Each label contains:

```
First Last [Den Type (Den #)]
Award 1, Award 2, Award 3...
```

### Bagging Guide

Produces a PDF checklist to help volunteers bag the correct adventure loops and pins for each scout. Each entry shows:

- A checkbox for tracking
- The adventure loop/pin image (downloaded from scouting.org)
- The adventure name with a Required/Elective tag

Scouts flow continuously across pages to minimize paper usage. Images are cached locally after the first download.

All six Cub Scout ranks are supported: Lion, Tiger, Wolf, Bear, Webelos, and Arrow of Light.

### Sort Order

**Scouts are automatically grouped by den type in rank order:**
1. Lion (kindergarten)
2. Tiger (1st grade)
3. Wolf (2nd grade)
4. Bear (3rd grade)
5. Webelos (4th grade)
6. Webelos 2 / Arrow of Light (5th grade)

Within each den type, scouts are sorted alphabetically by last name, then first name.

The PDF is designed for direct printing on Avery 6427 label sheets — no mail merge step needed.

## Troubleshooting

**"Could not find input file"**
- Make sure your CSV file path is correct
- Try using the full path to the file

**"Missing required column in CSV"**
- Verify your CSV has the exact column names: `First Name`, `Last Name`, `Den Type`, `Item Name`
- Check for extra spaces in column headers

## Roadmap

See [ROADMAP.md](ROADMAP.md) for planned features and release milestones.