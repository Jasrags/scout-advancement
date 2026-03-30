# Cub Scout Advancement List Processor

Scripts for processing CSV files of awarded advancements and generating printable labels grouped by scout.

## Requirements

- Python 3.6 or higher
- `reportlab` (for PDF label generation)

```bash
python -m venv .venv
source .venv/bin/activate
pip install reportlab
```

## PDF Label Generator (Recommended)

Generates ready-to-print Avery 6427 shipping labels (2" x 4", 10 per sheet) directly from advancement CSVs.

```bash
python generate_labels_pdf.py <input_file1.csv> [input_file2.csv ...] [-o output.pdf]
```

### Arguments

- `input_file.csv` (required): One or more CSV files containing advancement data
- `-o output.pdf` (optional): Name for the output file (defaults to `advancement_labels.pdf`)

### Examples

```bash
# Single file
python generate_labels_pdf.py advancements.csv

# Multiple files combined
python generate_labels_pdf.py january.csv february.csv march.csv

# Custom output filename
python generate_labels_pdf.py jan.csv feb.csv -o q1_labels.pdf
```

## CSV Processor (Legacy)

Groups advancements by scout into a CSV for use with mail merge.

```bash
python advancement_processor.py <input_file1.csv> [input_file2.csv ...] [-o output_file.csv]
```

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

### PDF Labels (`generate_labels_pdf.py`)

Produces a print-ready PDF with Avery 6427 shipping labels. Each label contains:

```
First Last [Den Type (Den #)]
Award 1, Award 2, Award 3...
```

### CSV (`advancement_processor.py`)

Produces a CSV with a single column containing formatted label text for each scout:

```
[Name] - [Den Type]
[Advancements]
```

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

## Notes

- Scouts are automatically grouped by den type (Lion → Tiger → Wolf → Bear → Webelos) for easier organization
- Within each den type, scouts are sorted alphabetically by last name
- Adventures appear in the order they're listed in the input file(s)
- When processing multiple files, if the same scout appears in multiple files, all their advancements are combined
- The output CSV is ready for use in mail merge applications
- If a scout has multiple entries, all their advancements are grouped together
- You can use shell wildcards (like `*.csv`) to process all CSV files in a directory

## Troubleshooting

**"Could not find input file"**
- Make sure your CSV file path is correct
- Try using the full path to the file

**"Missing required column in CSV"**
- Verify your CSV has the exact column names: `First Name`, `Last Name`, `Den Type`, `Item Name`
- Check for extra spaces in column headers

## Roadmap

See [ROADMAP.md](ROADMAP.md) for planned features and release milestones.