"""Tests for src.core.csv_validator."""

import os
import tempfile

from src.core.csv_validator import validate_csv

SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "..", "sample_data")
SAMPLE_FILE = os.path.join(SAMPLE_DIR, "PO_P2001FP_2000001.csv")


class TestValidateCsv:
    def test_valid_file(self) -> None:
        result = validate_csv(SAMPLE_FILE)
        assert result.is_valid is True
        assert result.error is None
        assert result.row_count > 0

    def test_nonexistent_file(self) -> None:
        result = validate_csv("/tmp/does_not_exist_12345.csv")
        assert result.is_valid is False
        assert "not found" in result.error.lower()

    def test_missing_columns(self) -> None:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as f:
            f.write("Name,Grade\nAlice,3\n")
            path = f.name
        try:
            result = validate_csv(path)
            assert result.is_valid is False
            assert "Missing columns" in result.error
        finally:
            os.unlink(path)

    def test_empty_csv_headers_only(self) -> None:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as f:
            f.write('"First Name","Last Name","Den Type","Den Number","Item Name"\n')
            path = f.name
        try:
            result = validate_csv(path)
            assert result.is_valid is False
            assert "No data rows" in result.error
        finally:
            os.unlink(path)

    def test_completely_empty_file(self) -> None:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False
        ) as f:
            path = f.name
        try:
            result = validate_csv(path)
            assert result.is_valid is False
        finally:
            os.unlink(path)

    def test_directory_instead_of_file(self) -> None:
        result = validate_csv(SAMPLE_DIR)
        assert result.is_valid is False
        assert "Not a file" in result.error
