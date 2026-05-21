"""Unit tests for flows/download_tsv.py.

Tasks are called via .fn() to bypass Prefect orchestration so the tests run
without a live Prefect server.
"""

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from flows.download_tsv import fetch_tsv, save_locally, store_to_mariadb


SAMPLE_DF = pd.DataFrame(
    {
        "Kalenderwoche": ["2024-W01", "2024-W02"],
        "Inzidenz": [12.3, 14.7],
    }
)


def test_fetch_tsv_returns_dataframe():
    """fetch_tsv should return the DataFrame produced by pd.read_csv."""
    with patch("flows.download_tsv.pd.read_csv", return_value=SAMPLE_DF) as mock_read:
        result = fetch_tsv.fn("https://example.com/data.tsv")

    mock_read.assert_called_once_with("https://example.com/data.tsv", sep="\t")
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == ["Kalenderwoche", "Inzidenz"]
    assert len(result) == 2


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


@patch.dict(
    os.environ,
    {
        "MARIADB_HOST": "localhost",
        "MARIADB_USER": "user",
        "MARIADB_PASSWORD": "pass",
        "MARIADB_DATABASE": "db",
    },
)
def test_store_to_mariadb_writes_and_commits():
    """store_to_mariadb should create the table, insert rows, and commit."""
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
    mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

    with patch("flows.download_tsv.pymysql.connect", return_value=mock_conn):
        store_to_mariadb.fn(SAMPLE_DF, "grippeweb")

    assert mock_cursor.execute.call_count == 2  # DROP + CREATE
    mock_cursor.executemany.assert_called_once()
    call_args = mock_cursor.executemany.call_args
    assert "grippeweb" in call_args.args[0]
    assert len(call_args.args[1]) == len(SAMPLE_DF)
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()
