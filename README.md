# cnpj-lakehouse

Lakehouse project for the CNPJ Risk Graph Engine. The repository provides a local Spark-first platform for four data engineers to develop ingestion, standardization, enrichment and graph-processing jobs.

## Local Stack

- PySpark for local batch processing.
- Jupyter for interactive development.
- MinIO as the local S3-compatible data lake.
- Pytest and schema validation as the minimum quality gate.

The topology, service contracts and troubleshooting flow are documented in:

- [Local runtime topology](docs/devops/local-runtime-topology.md)
- [Environment variables and service contracts](docs/devops/environment-contracts.md)
- [Observability and troubleshooting playbook](docs/devops/observability-playbook.md)
- [Repository flow](docs/devops/repository-flow.md)

## Prerequisites

- Python 3.8+ available as `python` or `python3`.
- Docker Desktop with Docker Compose installed and running.
- Git.

## Start Local

### macOS/Linux or Git Bash

```bash
chmod +x start_local
source ./start_local
```

Use `./start_local` when activation persistence is not needed; source the script to keep `.venv` active in the current shell.

### Windows PowerShell

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\start_local.ps1
```

The startup helper creates `.venv`, installs `local-requirements.txt`, starts MinIO and bootstraps these buckets without manual intervention:

- `cnpj-raw`
- `cnpj-bronze`
- `cnpj-silver`
- `cnpj-gold`
- `cnpj-checkpoints`

To override local credentials, ports or bucket names, copy `.env.example` to `.env` before starting the stack. Never commit `.env` or real credentials.

## Run Jobs

Activate the environment if the startup script was executed in a separate shell:

```bash
source .venv/bin/activate
```

Run the Spark smoke job:

```bash
python -m src.jobs.local_spark_runtime
```

Run any PySpark script through the shared launcher:

```bash
python -m src.jobs.local_job_launcher path/to/job.py
```

Keep the Spark UI open for inspection during a smoke run:

```bash
SPARK_SMOKE_HOLD_SECONDS=30 python -m src.jobs.local_spark_runtime
```

On PowerShell:

```powershell
$env:SPARK_SMOKE_HOLD_SECONDS = "30"
python -m src.jobs.local_spark_runtime
```

Open the Spark UI at <http://localhost:4040>. Jupyter is available after setup with:

```bash
jupyter lab
```

## MinIO Access

- Console: <http://localhost:9001>
- S3 API: <http://localhost:9000>
- Default local credentials: `minioadmin` / `minioadmin`
- Health endpoint: <http://localhost:9000/minio/health/live>

Inspect the stack with:

```bash
docker compose -f local-infra/docker-compose.yml ps
docker logs cnpj_minio_init
```

Stop the stack with:

```bash
docker compose -f local-infra/docker-compose.yml down
```

## Validation

Run the same checks used by GitHub Actions:

```bash
python scripts/validate_schemas.py
pytest -q
python -m src.jobs.local_spark_runtime
```

CI runs on pull requests and pushes to `main`/`develop`. It validates every YAML schema, executes tests and runs the Spark smoke job.

## Collaboration Workflow

Use one feature branch per board task:

```bash
git switch main
```

Make atomic commits using the repository convention, for example:

```text
feat(infra): bootstrap local lake buckets
test(ci): validate schema contracts
```

Open a PR into the repository integration branch (`develop` when configured, otherwise `main`) with the task, acceptance evidence, commands run and any local limitations. Require green CI and one approval before merge. See [repository flow](docs/devops/repository-flow.md) for the complete policy.
