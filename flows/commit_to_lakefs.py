"""Prefect task for uploading the saved TSV to lakeFS and committing it."""

import logging
import os
from pathlib import Path

from prefect import get_run_logger, task
from prefect.exceptions import MissingContextError

LAKEFS_REPO = "sandbox"
LAKEFS_BRANCH = "main"
LAKEFS_OBJECT_PATH = "RAW/RKI/grippeweb.tsv"
LAKEFS_COMMIT_MESSAGE = "new version from RKI"


def _get_logger() -> logging.Logger:
    """Return a Prefect run logger when available, otherwise a standard logger."""
    try:
        return get_run_logger()
    except MissingContextError:
        return logging.getLogger(__name__)


def _get_lakefs_branch():
    """Create a lakeFS branch handle from environment-based connection settings."""
    try:
        import lakefs
        from lakefs.client import Client
    except ImportError as exc:
        raise RuntimeError("The 'lakefs' package must be installed to upload to lakeFS.") from exc

    client = Client(
        host=os.environ["LAKEFS_HOST"],
        username=os.environ["LAKEFS_ACCESS_KEY"],
        password=os.environ["LAKEFS_SECRET_KEY"],
    )
    return lakefs.repository(LAKEFS_REPO, client=client).branch(LAKEFS_BRANCH)


@task
def commit_to_lakefs(path: str) -> None:
    """Upload the saved TSV to lakeFS and create a commit on the target branch."""
    logger = _get_logger()
    branch = _get_lakefs_branch()
    local_path = Path(path)

    logger.info("Uploading %s to lakeFS %s/%s/%s", local_path, LAKEFS_REPO, LAKEFS_BRANCH, LAKEFS_OBJECT_PATH)
    with local_path.open("rb") as infile:
        branch.object(LAKEFS_OBJECT_PATH).upload(
            data=infile.read(),
            content_type="text/tab-separated-values",
        )

    changes = list(branch.uncommitted())
    if not changes:
        logger.info("No uncommitted lakeFS changes detected on %s/%s", LAKEFS_REPO, LAKEFS_BRANCH)
        return

    ref = branch.commit(message=LAKEFS_COMMIT_MESSAGE)
    logger.info("Committed lakeFS change %s on %s/%s", getattr(ref, "id", "<unknown>"), LAKEFS_REPO, LAKEFS_BRANCH)
