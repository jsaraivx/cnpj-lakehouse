# Environment Variables and Service Contracts

Copy `.env.example` to `.env` when you need local overrides.

## Core Variables

| Variable | Default | Contract |
|---|---|---|
| `MINIO_ROOT_USER` | `minioadmin` | MinIO admin username for local development only. |
| `MINIO_ROOT_PASSWORD` | `minioadmin` | MinIO admin password for local development only. |
| `MINIO_API_PORT` | `9000` | MinIO S3-compatible API port. |
| `MINIO_CONSOLE_PORT` | `9001` | MinIO web console port. |
| `MINIO_ENDPOINT` | `http://localhost:9000` | Endpoint used by jobs and SDK clients. |
| `MINIO_REGION` | `us-east-1` | Region sent by S3-compatible clients. |
| `BRONZE_BUCKET` | `cnpj-bronze` | Storage contract for Bronze outputs. |
| `SILVER_BUCKET` | `cnpj-silver` | Storage contract for Silver outputs. |
| `GOLD_BUCKET` | `cnpj-gold` | Storage contract for Gold outputs. |
| `CHECKPOINT_BUCKET` | `cnpj-checkpoints` | Storage contract for Spark checkpoint data. |
| `RAW_BUCKET` | `cnpj-raw` | Storage contract for raw ingested files. |
| `SPARK_MASTER` | `local[2]` | Local Spark execution master. |
| `SPARK_APP_NAME` | `cnpj-local-runtime` | Default local Spark app name. |
| `SPARK_UI_PORT` | `4040` | Spark UI port used by local sessions. |

## Runtime Contracts

- `start_local` and `start_local.ps1` must be enough to prepare the local stack.
- `local-infra/docker-compose.yml` must bootstrap MinIO and bucket structure without manual setup.
- Local smoke job must run through `python -m src.jobs.local_spark_runtime`.
- Job launcher must support `python -m src.jobs.local_job_launcher <job.py>`.

## Team Contracts

- Data engineers only need Python + Docker; no cloud credentials for P0 development.
- Every new job must declare layer input/output (`raw`, `bronze`, `silver`, `gold`) in module docstring.
- Every PR touching runtime contracts must update `README.md` and this document.
