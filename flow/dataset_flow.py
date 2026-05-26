"""Generic Prefect flow for downloading, storing, and publishing TSV datasets."""

from prefect import flow

from tasks.commit_to_lakefs import commit_to_lakefs
from tasks.download_tsv import download_tsv
from tasks.save_locally import save_locally
from tasks.store_to_mariadb import store_to_mariadb


def _validate_required_parameters(params: dict[str, str]) -> None:
    """Raise a clear error if a required flow parameter is missing or blank."""
    missing = [name for name, value in params.items() if not str(value).strip()]
    if missing:
        missing_list = ", ".join(sorted(missing))
        raise ValueError(
            f"Missing required flow parameter(s): {missing_list}. "
            "Provide all dataset-specific parameters in the deployment configuration or run request."
        )


@flow
def run_dataset(
    source_url: str,
    local_path: str,
    lakefs_repo: str,
    lakefs_branch: str,
    lakefs_object_path: str,
    lakefs_commit_message: str,
    mariadb_table: str,
    mariadb_database: str,
) -> None:
    """Fetch a TSV dataset, persist it locally, and publish it downstream."""
    _validate_required_parameters(
        {
            "source_url": source_url,
            "local_path": local_path,
            "lakefs_repo": lakefs_repo,
            "lakefs_branch": lakefs_branch,
            "lakefs_object_path": lakefs_object_path,
            "lakefs_commit_message": lakefs_commit_message,
            "mariadb_table": mariadb_table,
            "mariadb_database": mariadb_database,
        }
    )
    df = download_tsv(source_url)
    save_locally(df, local_path)
    commit_to_lakefs(local_path, lakefs_repo, lakefs_branch, lakefs_object_path, lakefs_commit_message)
    store_to_mariadb(df, mariadb_table, mariadb_database)
