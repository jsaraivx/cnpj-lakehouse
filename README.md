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

## Development Pattern

Develop one small, independently verifiable board task at a time. Data engineers work on PySpark processing; infrastructure changes belong to the Tech Lead track.

### Repository Structure

```text
src/
  jobs/                 shared local runtime and job launchers
  ingestion/            source ingestion modules
  utils/                reusable processing utilities
schemas/
  templates/            schema examples and templates
  bronze/               source-aligned schemas
  silver/               standardized schemas
  gold/                 business and graph schemas
tests/                  unit, contract and smoke tests
local-infra/            Docker Compose and MinIO configuration
docs/devops/            runtime, contracts and troubleshooting guides
scripts/                repository validation utilities
```

### Medallion Job Pattern

Jobs must make their layer, input and output explicit in the module docstring and follow this flow:

1. **Raw**: preserve downloaded source files in `s3a://cnpj-raw/` without business transformations.
2. **Bronze**: apply the source schema and write source-aligned data to `s3a://cnpj-bronze/`.
3. **Silver**: normalize, type, deduplicate and validate data in `s3a://cnpj-silver/`.
4. **Gold**: publish facts, dimensions, risk scores and graph datasets to `s3a://cnpj-gold/`.

Use partitioned paths and idempotent writes. Do not overwrite an entire bucket for a single partition or commit source datasets to Git.

### Job Conventions

- Use a callable entry point for reusable transformations and a small `if __name__ == "__main__":` runner.
- Accept input/output paths and execution options as arguments instead of hard-coding machine-specific paths.
- Use `python -m src.jobs.local_job_launcher path/to/job.py` for local execution.
- Keep Spark session creation in the shared runtime unless a job has a documented exception.
- Log the application name, input path, output path, partition and row-count checkpoints.
- Stop the Spark session in a `finally` block when a job owns the session.
- Never commit credentials, `.env`, downloaded CNPJ archives or generated outputs.

### Schema Conventions

- Store schemas as YAML under the appropriate medallion directory.
- Use `snake_case` for table and column names.
- Declare `table_name`, `description`, `columns`, column descriptions and Spark-compatible types.
- Declare only existing columns in `partitions`.
- Treat CNPJ/CPF values as strings to preserve leading zeroes.
- Add or update a schema test whenever a schema contract changes.

### Test Pattern

Every new job or infrastructure contract should include the smallest useful test:

- Unit test pure transformations and argument handling.
- Contract test schemas, Compose configuration, environment variables and startup scripts.
- Smoke test a representative Spark operation with a small in-memory dataset.
- Do not require Docker or large CNPJ files in unit tests; use fixtures and mocks for external services.
- Add integration evidence in the PR when the change depends on MinIO or the Spark UI.

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

Validation is intentionally local-first. After running `start_local`, execute the full validation path with the same PySpark, Jupyter and MinIO dependencies used by development:

```bash
python scripts/validate_schemas.py
pytest -q --cov=src.jobs.local_job_launcher --cov=src.jobs.local_spark_runtime --cov=scripts.validate_schemas --cov-report=term-missing --cov-fail-under=85
python -m compileall -q src scripts tests
python -m src.jobs.local_spark_runtime
docker compose -f local-infra/docker-compose.yml ps
```

The test suite includes Spark runtime tests when PySpark is installed. The smoke job confirms Spark execution and the Compose status confirms the local MinIO service. No GitHub Actions workflow is configured for the current case-study phase, so this validation does not incur hosted CI minutes or download the heavy local stack twice.

Production CI/CD is intentionally deferred until the project migrates to AWS with Terraform. At that point, add a separate production workflow for infrastructure plans, deployment checks and cloud smoke tests; do not make local development depend on it.

## Collaboration Workflow

Use one feature branch per board task:

```bash
git switch main
git pull --ff-only
git switch -c feature/<short-task-name>
```

Move the board task to `In Progress`, implement only that task, and keep the branch focused. Make atomic commits using the repository convention, for example:

```text
feat(infra): bootstrap local lake buckets
test(infra): cover local runtime contracts
```

Before opening a PR, run the validation commands above and check the relevant local acceptance criteria. Open a PR into the repository integration branch (`develop` when configured, otherwise `main`) with:

- the board task or issue reference;
- a concise description of the change;
- commands run and their results;
- MinIO, Spark UI or output evidence when applicable;
- known limitations and follow-up work.

Require passing local validation and one approval before merge. After merge, mark the board task `Done`. See [repository flow](docs/devops/repository-flow.md) for the complete policy.
