"""Prefect task for downloading the RKI GrippeWeb TSV."""

import logging

import pandas as pd
from prefect import get_run_logger, task
from prefect.exceptions import MissingContextError


def _get_logger() -> logging.Logger:
    """Return a Prefect run logger when available, otherwise a standard logger."""
    try:
        return get_run_logger()
    except MissingContextError:
        return logging.getLogger(__name__)


@task
def download_tsv(url: str) -> pd.DataFrame:
    """Download a TSV file from the given URL and return it as a DataFrame."""
    logger = _get_logger()
    logger.info("Start download %s", url)
    df = pd.read_csv(url, sep="\t")
    size_kb = len(df.to_csv(sep="\t", index=False).encode()) / 1024
    logger.info("Download done. Downloaded %.1f KB", size_kb)
    return df
