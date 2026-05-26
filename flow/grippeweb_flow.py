"""Prefect flow for downloading and publishing the RKI GrippeWeb TSV."""

from prefect import flow

from config_default import (
    DEFAULT_LAKEFS_BRANCH,
    DEFAULT_LAKEFS_OBJECT_PATH,
    DEFAULT_LAKEFS_REPO,
    DEFAULT_MARIADB_DATABASE,
    DEFAULT_PATH,
    RKI_URL,
)
from tasks.commit_to_lakefs import commit_to_lakefs
from tasks.download_tsv import download_tsv
from tasks.save_locally import save_locally
from tasks.store_to_mariadb import store_to_mariadb


@flow
def run_grippeweb(
    url: str = RKI_URL,
    path: str = DEFAULT_PATH,
    lakefs_repo: str = DEFAULT_LAKEFS_REPO,
    lakefs_branch: str = DEFAULT_LAKEFS_BRANCH,
    lakefs_object_path: str = DEFAULT_LAKEFS_OBJECT_PATH,
    mariadb_database: str = DEFAULT_MARIADB_DATABASE,
) -> None:
    """Fetch the GrippeWeb TSV, persist it locally, and publish it downstream."""
    df = download_tsv(url)
    save_locally(df, path)
    commit_to_lakefs(path, lakefs_repo, lakefs_branch, lakefs_object_path)
    store_to_mariadb(df, "grippeweb", mariadb_database)


if __name__ == "__main__":
    run_grippeweb()
