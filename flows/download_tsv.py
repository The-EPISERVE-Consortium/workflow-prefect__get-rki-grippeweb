"""Prefect flow for downloading and saving the RKI GrippeWeb weekly report TSV."""

import logging

import pandas as pd
from prefect import flow, task, get_run_logger
from prefect.exceptions import MissingContextError

RKI_URL = (
    "https://raw.githubusercontent.com/robert-koch-institut/"
    "GrippeWeb_Daten_des_Wochenberichts/refs/heads/main/"
    "GrippeWeb_Daten_des_Wochenberichts.tsv"
)
DEFAULT_PATH = "/tmp/grippeweb.tsv"


@task
def fetch_tsv(url: str) -> pd.DataFrame:
    """Download a TSV file from the given URL and return it as a DataFrame.

    Args:
        url: The HTTP(S) URL of the TSV file to download.

    Returns:
        A pandas DataFrame containing the parsed TSV content.
    """
    try:
        logger = get_run_logger()
    except MissingContextError:
        logger = logging.getLogger(__name__)
    logger.info("Start download %s", url)
    df = pd.read_csv(url, sep="\t")
    logger.info("Download done.")
    return df


@task
def save_locally(df: pd.DataFrame, path: str) -> None:
    """Save a DataFrame to the local filesystem as a TSV file.

    Args:
        df: The DataFrame to persist.
        path: Absolute or relative file-system path where the TSV will be written.
    """
    df.to_csv(path, sep="\t", index=False)


@flow
def download_tsv(url: str = RKI_URL, path: str = DEFAULT_PATH) -> None:
    """Fetch the GrippeWeb TSV from a URL and save it locally.

    Args:
        url: Source URL of the TSV file. Defaults to the RKI GrippeWeb dataset.
        path: Destination path on the local filesystem. Defaults to /tmp/grippeweb.tsv.
    """
    df = fetch_tsv(url)
    save_locally(df, path)


if __name__ == "__main__":
    download_tsv()
