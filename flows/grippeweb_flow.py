"""Prefect flow for downloading and publishing the RKI GrippeWeb TSV."""

from prefect import flow

from flows.commit_to_lakefs import commit_to_lakefs
from flows.download_tsv import download_tsv
from flows.save_locally import save_locally
from flows.store_to_mariadb import store_to_mariadb

RKI_URL = (
    "https://raw.githubusercontent.com/robert-koch-institut/"
    "GrippeWeb_Daten_des_Wochenberichts/refs/heads/main/"
    "GrippeWeb_Daten_des_Wochenberichts.tsv"
)
DEFAULT_PATH = "/tmp/grippeweb.tsv"


@flow
def run_grippeweb(url: str = RKI_URL, path: str = DEFAULT_PATH) -> None:
    """Fetch the GrippeWeb TSV, persist it locally, and publish it downstream."""
    df = download_tsv(url)
    save_locally(df, path)
    commit_to_lakefs(path)
    store_to_mariadb(df, "grippeweb")


if __name__ == "__main__":
    run_grippeweb()
