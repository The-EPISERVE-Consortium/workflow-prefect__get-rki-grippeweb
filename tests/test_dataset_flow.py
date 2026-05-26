"""Unit tests for flow/dataset_flow.py."""

import pytest
from unittest.mock import patch

import pandas as pd

from flow.dataset_flow import run_dataset


SAMPLE_DF = pd.DataFrame(
    {
        "Kalenderwoche": ["2024-W01", "2024-W02"],
        "Inzidenz": [12.3, 14.7],
    }
)


def test_run_dataset_runs_steps_in_order():
    """run_dataset should save locally, then upload to lakeFS, then store in MariaDB."""
    call_order = []

    with (
        patch("flow.dataset_flow.download_tsv", return_value=SAMPLE_DF),
        patch("flow.dataset_flow.save_locally", side_effect=lambda df, path: call_order.append(("save", path))),
        patch(
            "flow.dataset_flow.commit_to_lakefs",
            side_effect=lambda path, repo, branch, object_path, commit_message: call_order.append(
                ("lakefs", path, repo, branch, object_path, commit_message)
            ),
        ),
        patch(
            "flow.dataset_flow.store_to_mariadb",
            side_effect=lambda df, table, database: call_order.append(("mariadb", table, database)),
        ),
    ):
        run_dataset(
            source_url="https://example.com/data.tsv",
            local_path="/tmp/grippeweb.tsv",
            lakefs_repo="sandbox",
            lakefs_branch="main",
            lakefs_object_path="RAW/RKI/grippeweb.tsv",
            lakefs_commit_message="new version from RKI",
            mariadb_table="grippeweb",
            mariadb_database="test",
        )

    assert call_order == [
        ("save", "/tmp/grippeweb.tsv"),
        ("lakefs", "/tmp/grippeweb.tsv", "sandbox", "main", "RAW/RKI/grippeweb.tsv", "new version from RKI"),
        ("mariadb", "grippeweb", "test"),
    ]


def test_run_dataset_rejects_blank_required_parameters():
    """run_dataset should fail early with a clear error when a required parameter is blank."""
    with pytest.raises(ValueError, match="Missing required flow parameter\\(s\\): source_url"):
        run_dataset(
            source_url="",
            local_path="/tmp/grippeweb.tsv",
            lakefs_repo="sandbox",
            lakefs_branch="main",
            lakefs_object_path="RAW/RKI/grippeweb.tsv",
            lakefs_commit_message="new version from RKI",
            mariadb_table="grippeweb",
            mariadb_database="test",
        )
