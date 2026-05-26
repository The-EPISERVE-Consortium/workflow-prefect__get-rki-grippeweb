"""Deploy the download_tsv flow to a Prefect work pool.

Run this script once (or in CI) after the Docker image has been pushed to GHCR:

    PREFECT_API_URL=https://<your-prefect-server>/api python deploy.py
"""

import os
from json import JSONDecodeError

from prefect.runner.storage import GitRepository
from flows.download_tsv import download_tsv, RKI_URL, DEFAULT_PATH

GITHUB_REPO_URL = "https://github.com/The-EPISERVE-Consortium/workflow-prefect__get-rki-grippeweb"

DOCKER_IMAGE = "ghcr.io/the-episerve-consortium/workflow-prefect__get-rki-grippeweb:latest"

WORK_POOL_NAME = "kubernetes-pool"

DEPLOYMENT_NAME = "grippeweb-downloader"

# ---------------------------------------------------------------------------
# Read PREFECT_API_URL from the environment and configure the client
# ---------------------------------------------------------------------------

prefect_api_url = os.environ.get("PREFECT_API_URL")
if not prefect_api_url:
    raise EnvironmentError(
        "PREFECT_API_URL environment variable is not set. "
        "Export it before running this script, e.g.:\n"
        "  export PREFECT_API_URL=https://<your-prefect-server>/api"
    )

os.environ["PREFECT_API_URL"] = prefect_api_url

# ---------------------------------------------------------------------------
# Build and apply the deployment
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    try:
        deployment = download_tsv.from_source(
            source=GitRepository(url=GITHUB_REPO_URL, branch="main"),
            entrypoint="flows/download_tsv.py:download_tsv",
        ).deploy(
            name=DEPLOYMENT_NAME,
            work_pool_name=WORK_POOL_NAME,
            parameters={
                "url": RKI_URL,
                "path": DEFAULT_PATH,
            },
            job_variables={
                "image": DOCKER_IMAGE,
                "image_pull_policy": "Always",
                "env": {
                    "MARIADB_HOST": "mariadb.default.svc.cluster.local",
                    "MARIADB_USER": "mariadb",
                    "MARIADB_DATABASE": "test",
                },
            },
        )
    except JSONDecodeError as exc:
        raise RuntimeError(
            "PREFECT_API_URL does not appear to point to a Prefect API endpoint. "
            f"Got a non-JSON response from {prefect_api_url!r}. "
            "Use the Prefect API URL, for example: "
            "'PREFECT_API_URL=https://prefect.medicalbioinformatics.de/api python deploy.py'."
        ) from exc
    print(f"Deployment '{DEPLOYMENT_NAME}' applied successfully.")
