# workflow-prefect__dataset-downloader

Prefect 3 workflow code for downloading delimited datasets from Git-backed sources, saving them locally as TSV, publishing them to lakeFS, and loading them into MariaDB. Dataset deployment settings live in `deploy/datasets.yaml`.

## Structure

| Path | Purpose |
|---|---|
| `flow/dataset_flow.py` | Generic Prefect flow orchestration |
| `tasks/*.py` | Individual Prefect tasks |
| `deploy/__main__.py` | Single deployment CLI entrypoint |
| `deploy/common.py` | YAML-backed Prefect deployment helper |
| `deploy/datasets.yaml` | Dataset-specific deployment parameters |
| `tests/` | Unit tests (pytest) |
| `Dockerfile` | Image based on `prefecthq/prefect:3.7.1-python3.11` |

## Run locally

```bash
pip install -r requirements.txt
pytest tests/
```

Run the generic flow directly by supplying all required parameters from Python. The deployment registry in `deploy/datasets.yaml` shows the full parameter set for each dataset.

## Deploy

Deploy one dataset by key:

```bash
PREFECT_API_URL=https://<your-prefect-server>/api python -m deploy grippeweb
```

Deploy all enabled datasets from `deploy/datasets.yaml`:

```bash
PREFECT_API_URL=https://<your-prefect-server>/api python -m deploy --all
```

Add or change deployments by editing `deploy/datasets.yaml`.

## CI

Pushing to `main` builds and pushes the image to GHCR, then runs the test suite inside the built image.
