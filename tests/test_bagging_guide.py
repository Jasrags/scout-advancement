"""Tests for src.core.bagging_guide."""

import os
import tempfile

import pytest

from src.core.bagging_guide import BaggingGuideResult, generate_bagging_guide
from src.core.label_generator import ScoutRecord, read_advancements

SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "..", "sample_data")
SAMPLE_FILE = os.path.join(SAMPLE_DIR, "PO_P2001FP_2000001.csv")


class TestGenerateBaggingGuide:
    def test_generates_pdf(self) -> None:
        scouts = read_advancements([SAMPLE_FILE])
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "guide.pdf")
            result = generate_bagging_guide(scouts, out, download_images=False)
            assert isinstance(result, BaggingGuideResult)
            assert result.scout_count == len(scouts)
            assert result.page_count >= 1
            assert os.path.exists(result.output_path)
            assert os.path.getsize(result.output_path) > 0

    def test_condensed_layout_uses_fewer_pages(self) -> None:
        scouts = read_advancements([SAMPLE_FILE])
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "guide.pdf")
            result = generate_bagging_guide(scouts, out, download_images=False)
            # Condensed layout: multiple scouts per page
            assert result.page_count < result.scout_count

    def test_empty_scouts_produces_empty_pdf(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "guide.pdf")
            result = generate_bagging_guide([], out, download_images=False)
            assert result.scout_count == 0
            assert result.page_count == 0

    def test_single_scout(self) -> None:
        scout = ScoutRecord(
            first="Test",
            last="Scout",
            den_type="lions",
            den_num="1",
            items=("Fun on the Run Adventure", "Mountain Lion Adventure"),
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "guide.pdf")
            result = generate_bagging_guide([scout], out, download_images=False)
            assert result.scout_count == 1
            assert result.page_count == 1

    def test_rejects_non_pdf_extension(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "guide.txt")
            with pytest.raises(OSError, match="must end with .pdf"):
                generate_bagging_guide([], out, download_images=False)

    def test_rejects_nonexistent_directory(self) -> None:
        with pytest.raises(OSError, match="does not exist"):
            generate_bagging_guide([], "/no/such/dir/guide.pdf", download_images=False)

    def test_scout_with_many_items_spans_pages(self) -> None:
        # A scout with many items should produce multiple pages
        items = tuple(f"Adventure {i}" for i in range(30))
        scout = ScoutRecord(
            first="Busy",
            last="Scout",
            den_type="bears",
            den_num="5",
            items=items,
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, "guide.pdf")
            result = generate_bagging_guide([scout], out, download_images=False)
            assert result.page_count > 1
