"""Prefect flow for downloading and publishing the RKI GrippeWeb TSV."""

from prefect import flow

from tasks.commit_to_lakefs import commit_to_lakefs
from tasks.download_tsv import download_tsv
from tasks.save_locally import save_locally
from tasks.store_to_mariadb import store_to_mariadb

RKI_URL = (
    "https://raw.githubusercontent.com/robert-koch-institut/"
    "GrippeWeb_Daten_des_Wochenberichts/refs/heads/main/"
    "GrippeWeb_Daten_des_Wochenberichts.tsv"
)
DEFAULT_PATH = "/tmp/grippeweb.tsv"
DEFAULT_LAKEFS_REPO = "sandbox"
DEFAULT_LAKEFS_BRANCH = "main"
DEFAULT_LAKEFS_OBJECT_PATH = "RAW/RKI/grippeweb.tsv"
DEFAULT_MARIADB_DATABASE = "test"


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
