"""Shared deployment helper for dataset-specific Prefect deployments."""

import os
from json import JSONDecodeError

from prefect.runner.storage import GitRepository

GITHUB_REPO_URL = "https://github.com/The-EPISERVE-Consortium/workflow-prefect__dataset-downloader"
DOCKER_IMAGE = "ghcr.io/the-episerve-consortium/workflow-prefect__dataset-downloader:latest"
WORK_POOL_NAME = "kubernetes-pool"
JOB_ENV = {
    "MARIADB_HOST": "mariadb.default.svc.cluster.local",
    "MARIADB_USER": "mariadb",
}


def deploy_dataset(flow_fn, deployment_name: str, parameters: dict[str, str]) -> None:
    """Deploy a dataset-specific flow configuration to the shared work pool."""
    prefect_api_url = os.environ.get("PREFECT_API_URL")
    if not prefect_api_url:
        raise EnvironmentError(
            "PREFECT_API_URL environment variable is not set. "
            "Export it before running this script, e.g.:\n"
            "  export PREFECT_API_URL=https://<your-prefect-server>/api"
        )

    os.environ["PREFECT_API_URL"] = prefect_api_url

    try:
        flow_fn.from_source(
            source=GitRepository(url=GITHUB_REPO_URL, branch="main"),
            entrypoint="flow/dataset_flow.py:run_dataset",
        ).deploy(
            name=deployment_name,
            work_pool_name=WORK_POOL_NAME,
            parameters=parameters,
            job_variables={
                "image": DOCKER_IMAGE,
                "image_pull_policy": "Always",
                "env": JOB_ENV,
            },
        )
    except JSONDecodeError as exc:
        raise RuntimeError(
            "PREFECT_API_URL does not appear to point to a Prefect API endpoint. "
            f"Got a non-JSON response from {prefect_api_url!r}. "
            "Use the Prefect API URL, for example: "
            "'PREFECT_API_URL=https://prefect.medicalbioinformatics.de/api python -m deploy.grippeweb'."
        ) from exc
