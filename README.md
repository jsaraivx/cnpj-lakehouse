# cnpj-lakehouse

A lakehouse project for the CNPJ Risk Graph Engine (ETL and graph analytics).

This repository contains tooling and jobs to ingest, process and analyze public CNPJ data.

**Start Local**

**Prerequisites:**
- Python 3.8+ available as `python`/`python3`.
- Docker Desktop (Docker Engine + Docker Compose) installed and running.

**Files created for local startup**
- [start_local](start_local#L1) — POSIX script for macOS/Linux (create venv, install local Spark stack, start MinIO).
- [start_local.ps1](start_local.ps1#L1) — PowerShell script for Windows (create venv, install local Spark stack, start MinIO).
- [local-infra/docker-compose.yml](local-infra/docker-compose.yml#L1) — Docker Compose to run MinIO locally.

**macOS / Linux**
1. Make the script executable (one-time):

```bash
chmod +x start_local
```

2. Run the helper to create/activate `.venv`, install requirements and start MinIO:

```bash
./start_local
```

The script will:
- Create `.venv` if missing and activate it in the current shell (when sourced/executed).
- Install the local stack from `local-requirements.txt` when present, including PySpark and Jupyter.
- Start MinIO using Docker Compose in `local-infra`.

**Windows (PowerShell)**
1. Open PowerShell and allow script execution for the session if required:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\start_local.ps1
```

The PowerShell script will create and activate `.venv`, install the local Spark/Jupyter stack and start MinIO via Docker Compose.

**Spark runtime**
- Local Spark UI: http://localhost:4040
- Smoke-check command:

```bash
python -m src.jobs.local_spark_runtime
```

**MinIO Access**
- Console: http://localhost:9001
- S3 API: http://localhost:9000
- Default credentials: `minioadmin` / `minioadmin`

**Notes & Troubleshooting**
- If `docker compose` is not available, scripts attempt `docker-compose` as fallback.
- If activation doesn't persist, open a new shell and source the venv manually:

macOS/Linux:
```bash
source .venv/bin/activate
```

Windows PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```

If you want a Makefile or task runner for common commands, I can add that next.
