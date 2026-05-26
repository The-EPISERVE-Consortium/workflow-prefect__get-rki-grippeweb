# workflow-prefect__dataset-downloader

Prefect 3 workflow code for downloading TSV datasets from Git-backed sources, saving them locally, publishing them to lakeFS, and loading them into MariaDB. Dataset-specific deployments live under `deploy/`.

## Structure

| Path | Purpose |
|---|---|
| `flow/dataset_flow.py` | Generic Prefect flow orchestration |
| `tasks/*.py` | Individual Prefect tasks |
| `deploy/common.py` | Shared Prefect deployment helper |
| `deploy/*.py` | Dataset-specific deployment modules |
| `tests/` | Unit tests (pytest) |
| `Dockerfile` | Image based on `prefecthq/prefect:3.7.1-python3.11` |

## Run locally

```bash
pip install -r requirements.txt
pytest tests/
```

Run the generic flow directly by supplying all required parameters from Python. For example, `deploy/grippeweb.py` shows the complete parameter set for one dataset-specific deployment.

## Deploy

Deploy the GrippeWeb dataset:

```bash
PREFECT_API_URL=https://<your-prefect-server>/api python -m deploy.grippeweb
```

Deploy the Germany COVID incidence dataset:

```bash
PREFECT_API_URL=https://<your-prefect-server>/api python -m deploy.corona_incidence_germany
```

Deploy the state-level Germany COVID incidence dataset:

```bash
PREFECT_API_URL=https://<your-prefect-server>/api python -m deploy.corona_incidence_states
```

Add more dataset deployments by creating additional modules under `deploy/` that call `deploy_dataset(...)` with a new parameter set.

## CI

Pushing to `main` builds and pushes the image to GHCR, then runs the test suite inside the built image.
