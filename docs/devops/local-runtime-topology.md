# Local Runtime Topology

This project runs a local Spark-first development stack focused on fast iteration for data engineers.

## Components

- Python virtual environment (`.venv`): isolated runtime for PySpark jobs and tests.
- PySpark local runtime: job execution in `local[*]` mode with Spark UI enabled.
- Jupyter: interactive notebook support for schema and transformation exploration.
- MinIO: local S3-compatible object store for medallion datasets.

## Service Topology

```text
Developer shell
  -> start_local / start_local.ps1
      -> create+activate .venv
      -> install local-requirements.txt
      -> docker compose up -d (local-infra)
          -> minio (S3 API:9000, Console:9001)
          -> minio-init (one-shot bucket bootstrap)

PySpark job
  -> reads/writes s3a://<bucket>/...
  -> Spark UI exposed on http://localhost:4040
```

## Data Buckets

- `cnpj-raw`: raw extracted files.
- `cnpj-bronze`: ingested source-aligned datasets.
- `cnpj-silver`: cleaned and standardized datasets.
- `cnpj-gold`: business facts, dimensions and graph-ready outputs.
- `cnpj-checkpoints`: Spark checkpoints and job state.

## Run Rules

- Always initialize local stack with `start_local` before running jobs.
- Keep jobs idempotent by partition path/date, avoiding blind overwrite on entire buckets.
- Prefer small smoke inputs while developing and validating schemas.
