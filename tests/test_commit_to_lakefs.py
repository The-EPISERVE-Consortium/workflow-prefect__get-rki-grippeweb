"""Unit tests for tasks/commit_to_lakefs.py."""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from tasks.commit_to_lakefs import LAKEFS_COMMIT_MESSAGE, commit_to_lakefs


def test_commit_to_lakefs_uploads_file_and_commits(tmp_path: Path):
    """commit_to_lakefs should upload the file contents and commit the change."""
    local_file = tmp_path / "grippeweb.tsv"
    local_file.write_text("col1\tcol2\n1\t2\n", encoding="utf-8")
    object_path = "RAW/RKI/grippeweb.tsv"

    mock_repository = MagicMock()
    mock_branch = MagicMock()
    mock_object = MagicMock()
    mock_repository.branch.return_value = mock_branch
    mock_branch.object.return_value = mock_object
    mock_branch.uncommitted.return_value = [SimpleNamespace(path=object_path)]
    mock_branch.commit.return_value = SimpleNamespace(id="commit-id")

    with patch("tasks.commit_to_lakefs._get_lakefs_repository", return_value=mock_repository) as mock_get_repo:
        commit_to_lakefs.fn(str(local_file), "sandbox", "main", object_path)

    mock_get_repo.assert_called_once_with("sandbox")
    mock_repository.branch.assert_called_once_with("main")
    mock_branch.object.assert_called_once_with(object_path)
    mock_object.upload.assert_called_once_with(
        data=b"col1\tcol2\n1\t2\n",
        content_type="text/tab-separated-values",
    )
    mock_branch.commit.assert_called_once_with(message=LAKEFS_COMMIT_MESSAGE)


def test_commit_to_lakefs_skips_commit_when_no_changes(tmp_path: Path):
    """commit_to_lakefs should not create a commit when lakeFS reports no changes."""
    local_file = tmp_path / "grippeweb.tsv"
    local_file.write_text("col1\tcol2\n1\t2\n", encoding="utf-8")
    object_path = "RAW/RKI/grippeweb.tsv"

    mock_repository = MagicMock()
    mock_branch = MagicMock()
    mock_repository.branch.return_value = mock_branch
    mock_branch.object.return_value = MagicMock()
    mock_branch.uncommitted.return_value = []

    with patch("tasks.commit_to_lakefs._get_lakefs_repository", return_value=mock_repository) as mock_get_repo:
        commit_to_lakefs.fn(str(local_file), "sandbox", "main", object_path)

    mock_get_repo.assert_called_once_with("sandbox")
    mock_branch.commit.assert_not_called()
