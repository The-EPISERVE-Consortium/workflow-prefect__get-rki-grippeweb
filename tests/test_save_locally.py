"""Unit tests for flows/save_locally.py."""

from pathlib import Path

import pandas as pd

from flows.save_locally import save_locally


SAMPLE_DF = pd.DataFrame(
    {
        "Kalenderwoche": ["2024-W01", "2024-W02"],
        "Inzidenz": [12.3, 14.7],
    }
)


def test_save_locally_creates_nonempty_file(tmp_path: Path):
    """save_locally should write a non-empty TSV file at the given path."""
    dest = tmp_path / "output.tsv"

    save_locally.fn(SAMPLE_DF, str(dest))

    assert dest.exists(), "Output file was not created"
    assert dest.stat().st_size > 0, "Output file is empty"


def test_save_locally_content_is_valid_tsv(tmp_path: Path):
    """save_locally should write content that can be read back as a TSV."""
    dest = tmp_path / "output.tsv"

    save_locally.fn(SAMPLE_DF, str(dest))

    reloaded = pd.read_csv(dest, sep="\t")
    pd.testing.assert_frame_equal(reloaded, SAMPLE_DF)
