# workflow-prefect__get-rki-grippeweb

Prefect 3 workflow that downloads the [RKI GrippeWeb weekly report](https://github.com/robert-koch-institut/GrippeWeb_Daten_des_Wochenberichts) TSV and saves it locally.

## Structure

| Path | Purpose |
|---|---|
| `flows/download_tsv.py` | Prefect flow + tasks |
| `tests/test_download_tsv.py` | Unit tests (pytest) |
| `deploy.py` | Programmatic deployment to `kubernetes-pool` |
| `Dockerfile` | Image based on `prefecthq/prefect:3.7.1-python3.11` |

## Run locally

```bash
pip install -r requirements.txt
python flows/download_tsv.py        # writes /tmp/grippeweb.tsv
pytest tests/
```

## Deploy

```bash
PREFECT_API_URL=https://<your-prefect-server>/api python deploy.py
```

## CI

Pushing to `main` builds and pushes the image to GHCR, then runs the test suite inside the built image.
