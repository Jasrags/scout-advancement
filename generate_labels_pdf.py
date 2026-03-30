#!/usr/bin/env python3
"""
Cub Scout Advancement Label PDF Generator

Generates printable Avery 6427 shipping labels (2" x 4", 10 per sheet)
from one or more advancement CSV files.

Usage:
    python generate_labels_pdf.py <input1.csv> [input2.csv ...] [-o output.pdf]
"""

import sys

from src.core.label_generator import (
    CSVColumnError,
    CSVReadError,
    read_advancements,
    generate_pdf,
)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python generate_labels_pdf.py <input1.csv> [input2.csv ...] [-o output.pdf]")
        sys.exit(1)

    args = sys.argv[1:]
    output_file = "advancement_labels.pdf"
    input_files: list[str] = []

    if "-o" in args:
        o_index = args.index("-o")
        if o_index + 1 >= len(args):
            print("Error: -o flag requires an output filename")
            sys.exit(1)
        output_file = args[o_index + 1]
        input_files = args[:o_index] + args[o_index + 2:]
    else:
        input_files = args

    if not input_files:
        print("Error: At least one input file is required")
        sys.exit(1)

    print(f"Processing {len(input_files)} file(s)")
    print("-" * 40)

    try:
        for f in input_files:
            print(f"  Reading: {f}")
        scouts = read_advancements(input_files)
        result = generate_pdf(scouts, output_file)
        print(f"\nGenerated {result.output_path}")
        print(f"  {result.label_count} labels on {result.page_count} page(s)")
    except (CSVReadError, CSVColumnError) as e:
        print(f"  Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
