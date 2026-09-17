# Local Observability and Troubleshooting Playbook

## Health Checks

- MinIO API health: `http://localhost:9000/minio/health/live`
- MinIO console: `http://localhost:9001`
- Spark UI: `http://localhost:4040`

## Quick Diagnosis Flow

1. Start stack: `./start_local` or `./start_local.ps1`.
2. Check containers: `docker compose -f local-infra/docker-compose.yml ps`.
3. Run smoke job: `python -m src.jobs.local_spark_runtime`.
4. Open Spark UI and confirm app/job/stages appear.
5. Verify bucket outputs in MinIO console.

## Common Failures

### Docker compose command not found

- Confirm Docker Desktop is running.
- Try `docker-compose` fallback.

### Port conflict (`9000`, `9001`, `4040`)

- Update `.env` (`MINIO_API_PORT`, `MINIO_CONSOLE_PORT`, `SPARK_UI_PORT`).
- Restart stack after changes.

### Spark UI does not appear

- Ensure job is running long enough to open UI.
- Confirm no existing Spark process is occupying `SPARK_UI_PORT`.

### Bucket does not exist

- Verify `minio-init` ran successfully in compose logs.
- Re-run: `docker compose -f local-infra/docker-compose.yml up -d`.

## Logs and Commands

- MinIO logs: `docker logs cnpj_minio`
- MinIO init logs: `docker logs cnpj_minio_init`
- Stop stack: `docker compose -f local-infra/docker-compose.yml down`
- Full reset (local only): `docker compose -f local-infra/docker-compose.yml down -v`
