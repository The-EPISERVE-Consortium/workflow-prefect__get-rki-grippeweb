"""Shared logging helpers for Prefect tasks."""

import logging

from prefect import get_run_logger
from prefect.exceptions import MissingContextError


def get_logger(name: str) -> logging.Logger:
    """Return a Prefect run logger when available, otherwise a standard logger."""
    try:
        return get_run_logger()
    except MissingContextError:
        return logging.getLogger(name)
