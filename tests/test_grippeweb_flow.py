"""Unit tests for flow/grippeweb_flow.py."""

from unittest.mock import patch

import pandas as pd

from flow.grippeweb_flow import run_grippeweb


SAMPLE_DF = pd.DataFrame(
    {
        "Kalenderwoche": ["2024-W01", "2024-W02"],
        "Inzidenz": [12.3, 14.7],
    }
)


def test_run_grippeweb_runs_steps_in_order():
    """run_grippeweb should save locally, then upload to lakeFS, then store in MariaDB."""
    call_order = []

    with (
        patch("flow.grippeweb_flow.download_tsv", return_value=SAMPLE_DF),
        patch("flow.grippeweb_flow.save_locally", side_effect=lambda df, path: call_order.append(("save", path))),
        patch(
            "flow.grippeweb_flow.commit_to_lakefs",
            side_effect=lambda path, repo, branch, object_path: call_order.append(("lakefs", path, repo, branch, object_path)),
        ),
        patch(
            "flow.grippeweb_flow.store_to_mariadb",
            side_effect=lambda df, table, database: call_order.append(("mariadb", table, database)),
        ),
    ):
        run_grippeweb(url="https://example.com/data.tsv", path="/tmp/grippeweb.tsv")

    assert call_order == [
        ("save", "/tmp/grippeweb.tsv"),
        ("lakefs", "/tmp/grippeweb.tsv", "sandbox", "main", "RAW/RKI/grippeweb.tsv"),
        ("mariadb", "grippeweb", "test"),
    ]
