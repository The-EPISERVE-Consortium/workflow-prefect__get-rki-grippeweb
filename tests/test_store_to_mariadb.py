"""Unit tests for tasks/store_to_mariadb.py."""

import os
from unittest.mock import MagicMock, patch

import pandas as pd

from tasks.store_to_mariadb import store_to_mariadb


SAMPLE_DF = pd.DataFrame(
    {
        "Kalenderwoche": ["2024-W01", "2024-W02"],
        "Inzidenz": [12.3, 14.7],
    }
)


@patch.dict(
    os.environ,
    {
        "MARIADB_HOST": "localhost",
        "MARIADB_USER": "user",
        "MARIADB_PASSWORD": "pass",
    },
)
def test_store_to_mariadb_writes_and_commits():
    """store_to_mariadb should create the table, insert rows, and commit."""
    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
    mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

    with patch("tasks.store_to_mariadb.pymysql.connect", return_value=mock_conn):
        store_to_mariadb.fn(SAMPLE_DF, "grippeweb", "db")

    assert mock_cursor.execute.call_count == 4  # CREATE DATABASE, USE, DROP TABLE, CREATE TABLE
    mock_cursor.executemany.assert_called_once()
    call_args = mock_cursor.executemany.call_args
    assert "grippeweb" in call_args.args[0]
    assert len(call_args.args[1]) == len(SAMPLE_DF)
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()
