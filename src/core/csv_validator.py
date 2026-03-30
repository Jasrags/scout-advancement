"""CSV validation for Scoutbook advancement exports."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from src.core.label_generator import REQUIRED_COLUMNS


@dataclass(frozen=True)
class ValidationResult:
    is_valid: bool
    error: str | None
    row_count: int


def validate_csv(file_path: str) -> ValidationResult:
    """Validate that a CSV file is a readable Scoutbook advancement export.

    Checks:
    - File exists
    - File is parseable CSV with headers
    - Required columns are present
    - At least one data row exists
    """
    path = Path(file_path)

    if not path.exists():
        return ValidationResult(is_valid=False, error=f"File not found: {path.name}", row_count=0)

    if not path.is_file():
        return ValidationResult(is_valid=False, error=f"Not a file: {path.name}", row_count=0)

    try:
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)

            if reader.fieldnames is None:
                return ValidationResult(
                    is_valid=False, error=f"Empty or unreadable CSV: {path.name}", row_count=0
                )

            missing = REQUIRED_COLUMNS - set(reader.fieldnames)
            if missing:
                return ValidationResult(
                    is_valid=False,
                    error=f"Missing columns: {', '.join(sorted(missing))}",
                    row_count=0,
                )

            row_count = sum(1 for _ in reader)
            if row_count == 0:
                return ValidationResult(
                    is_valid=False, error=f"No data rows in: {path.name}", row_count=0
                )

            return ValidationResult(is_valid=True, error=None, row_count=row_count)

    except (csv.Error, UnicodeDecodeError) as e:
        return ValidationResult(is_valid=False, error=f"Cannot parse CSV: {e}", row_count=0)
