"""Unit tests for tasks/download_tsv.py."""

from unittest.mock import patch

import pandas as pd

from tasks.download_tsv import download_tsv


SAMPLE_DF = pd.DataFrame(
    {
        "Kalenderwoche": ["2024-W01", "2024-W02"],
        "Inzidenz": [12.3, 14.7],
    }
)


def test_download_tsv_returns_dataframe():
    """download_tsv should return the DataFrame produced by pd.read_csv."""
    with patch("tasks.download_tsv.pd.read_csv", return_value=SAMPLE_DF) as mock_read:
        result = download_tsv.fn("https://example.com/data.tsv")

    mock_read.assert_called_once_with("https://example.com/data.tsv", sep="\t")
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ["Kalenderwoche", "Inzidenz"]
    assert len(result) == 2
