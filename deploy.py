"""Deploy the download_tsv flow to a Prefect work pool.

Run this script once (or in CI) after the Docker image has been pushed to GHCR:

    PREFECT_API_URL=https://<your-prefect-server>/api python deploy.py
"""

import os
from json import JSONDecodeError

from config_default import (
    DEFAULT_LAKEFS_BRANCH,
    DEFAULT_LAKEFS_OBJECT_PATH,
    DEFAULT_LAKEFS_REPO,
    DEFAULT_MARIADB_DATABASE,
    DEFAULT_PATH,
    RKI_URL,
)
from flow.grippeweb_flow import run_grippeweb
from prefect.runner.storage import GitRepository

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
        deployment = run_grippeweb.from_source(
            source=GitRepository(url=GITHUB_REPO_URL, branch="main"),
            entrypoint="flow/grippeweb_flow.py:run_grippeweb",
        ).deploy(
            name=DEPLOYMENT_NAME,
            work_pool_name=WORK_POOL_NAME,
            parameters={
                "url": RKI_URL,
                "path": DEFAULT_PATH,
                "lakefs_repo": DEFAULT_LAKEFS_REPO,
                "lakefs_branch": DEFAULT_LAKEFS_BRANCH,
                "lakefs_object_path": DEFAULT_LAKEFS_OBJECT_PATH,
                "mariadb_database": DEFAULT_MARIADB_DATABASE,
            },
            job_variables={
                "image": DOCKER_IMAGE,
                "image_pull_policy": "Always",
                "env": {
                    "MARIADB_HOST": "mariadb.default.svc.cluster.local",
                    "MARIADB_USER": "mariadb",
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
