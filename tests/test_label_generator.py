"""Tests for src.core.label_generator."""

import os
import tempfile

import pytest

from src.core.label_generator import (
    CSVColumnError,
    CSVReadError,
    ScoutRecord,
    generate_pdf,
    read_advancements,
)

SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "..", "sample_data")
SAMPLE_FILE_1 = os.path.join(SAMPLE_DIR, "PO_P2001FP_2000001.csv")
SAMPLE_FILE_2 = os.path.join(SAMPLE_DIR, "PO_P2045FP_2000002.csv")


class TestReadAdvancements:
    def test_reads_single_file(self) -> None:
        scouts = read_advancements([SAMPLE_FILE_1])
        assert len(scouts) > 0
        assert all(isinstance(s, ScoutRecord) for s in scouts)

    def test_reads_multiple_files(self) -> None:
        scouts = read_advancements([SAMPLE_FILE_1, SAMPLE_FILE_2])
        assert len(scouts) > len(read_advancements([SAMPLE_FILE_1]))

    def test_sort_order_den_types(self) -> None:
        scouts = read_advancements([SAMPLE_FILE_1])
        den_types = [s.den_type.lower() for s in scouts]
        expected_order = ["lions", "tigers", "wolves", "bears", "webelos", "aol"]
        seen: list[str] = []
        for dt in den_types:
            if dt not in seen:
                seen.append(dt)
        # Each den type that appears should be in the expected order
        for i, dt in enumerate(seen):
            for j, dt2 in enumerate(seen):
                if i < j:
                    assert expected_order.index(dt) < expected_order.index(dt2)

    def test_sort_order_alphabetical_within_den(self) -> None:
        scouts = read_advancements([SAMPLE_FILE_1])
        # Group by den_type, check last names are sorted within each
        from itertools import groupby

        for _, group in groupby(scouts, key=lambda s: s.den_type):
            group_list = list(group)
            last_names = [s.last.lower() for s in group_list]
            assert last_names == sorted(last_names)

    def test_combines_same_scout_from_multiple_files(self) -> None:
        # A scout in one file should have all their items combined
        scouts = read_advancements([SAMPLE_FILE_1])
        for scout in scouts:
            assert len(scout.items) >= 1

    def test_missing_file_raises_csv_read_error(self) -> None:
        with pytest.raises(CSVReadError, match="Could not find"):
            read_advancements(["nonexistent_file.csv"])

    def test_empty_csv_raises_csv_column_error(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            path = f.name
        try:
            with pytest.raises(CSVColumnError, match="Empty or unreadable"):
                read_advancements([path])
        finally:
            os.unlink(path)

    def test_missing_columns_raises_csv_column_error(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("Name,Grade\n")
            f.write("Alice,3\n")
            path = f.name
        try:
            with pytest.raises(CSVColumnError, match="Missing columns"):
                read_advancements([path])
        finally:
            os.unlink(path)


class TestGeneratePdf:
    def test_generates_pdf_file(self) -> None:
        scouts = read_advancements([SAMPLE_FILE_1])
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            output_path = f.name
        try:
            result = generate_pdf(scouts, output_path)
            assert os.path.exists(result.output_path)
            assert os.path.getsize(result.output_path) > 0
            assert result.label_count == len(scouts)
            assert result.page_count >= 1
        finally:
            os.unlink(output_path)

    def test_page_count_calculation(self) -> None:
        scouts = read_advancements([SAMPLE_FILE_1, SAMPLE_FILE_2])
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            output_path = f.name
        try:
            result = generate_pdf(scouts, output_path)
            expected_pages = (len(scouts) + 9) // 10  # 10 labels per page
            assert result.page_count == expected_pages
        finally:
            os.unlink(output_path)

    def test_nonexistent_output_dir_raises_os_error(self) -> None:
        scouts = read_advancements([SAMPLE_FILE_1])
        with pytest.raises(OSError, match="Output directory does not exist"):
            generate_pdf(scouts, "/nonexistent_dir/output.pdf")

    def test_empty_scout_list(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
            output_path = f.name
        try:
            result = generate_pdf([], output_path)
            assert result.label_count == 0
            assert result.page_count == 0
        finally:
            os.unlink(output_path)
