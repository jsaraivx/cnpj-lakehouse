from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest
import yaml

from scripts import validate_schemas
from src.jobs import local_job_launcher
from src.jobs.local_spark_runtime import build_spark_session, run_sample_job


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_compose_declares_runtime_services_and_bucket_bootstrap():
    compose = yaml.safe_load(_read("local-infra/docker-compose.yml"))

    assert set(compose["services"]) == {"minio", "minio-init"}
    minio = compose["services"]["minio"]
    initializer = compose["services"]["minio-init"]

    assert minio["image"] == "quay.io/minio/minio:latest"
    assert "${MINIO_API_PORT:-9000}:9000" in minio["ports"]
    assert "${MINIO_CONSOLE_PORT:-9001}:9001" in minio["ports"]
    assert minio["healthcheck"]["test"][:3] == ["CMD", "curl", "--fail"]
    assert initializer["image"] == "quay.io/minio/mc:latest"
    assert initializer["depends_on"]["minio"]["condition"] == "service_healthy"

    entrypoint = initializer["entrypoint"]
    for bucket in ("BRONZE_BUCKET", "SILVER_BUCKET", "GOLD_BUCKET", "CHECKPOINT_BUCKET", "RAW_BUCKET"):
        assert f"$${{{bucket}}}" in entrypoint


def test_environment_example_exposes_all_runtime_contracts():
    values = {}
    for line in _read(".env.example").splitlines():
        if line and not line.startswith("#"):
            key, value = line.split("=", maxsplit=1)
            values[key] = value

    assert values["MINIO_ENDPOINT"] == "http://localhost:9000"
    assert values["MINIO_CONSOLE_ENDPOINT"] == "http://localhost:9001"
    assert values["BRONZE_BUCKET"] == "cnpj-bronze"
    assert values["SILVER_BUCKET"] == "cnpj-silver"
    assert values["GOLD_BUCKET"] == "cnpj-gold"
    assert values["CHECKPOINT_BUCKET"] == "cnpj-checkpoints"
    assert values["RAW_BUCKET"] == "cnpj-raw"
    assert values["SPARK_UI_PORT"] == "4040"


@pytest.mark.parametrize("script", ["start_local", "start_local.sh"])
def test_posix_startup_scripts_are_source_safe_and_start_compose(script: str):
    content = _read(script)

    assert "set -euo pipefail" in content
    assert "local-requirements.txt" in content
    assert "docker compose" in content
    assert "return 0 2>/dev/null || exit 0" in content


def test_powershell_startup_script_uses_root_env_file_and_reports_services():
    content = _read("start_local.ps1")

    assert "Set-StrictMode -Version Latest" in content
    assert 'Join-Path $Root ".env"' in content
    assert "--env-file" in content
    assert "local-requirements.txt" in content
    assert "Spark UI: http://localhost:4040" in content


def test_launcher_normalizes_python_job_paths():
    assert local_job_launcher._normalize_job_path("jobs/example") == "jobs/example.py"
    assert local_job_launcher._normalize_job_path("jobs/example.py") == "jobs/example.py"


def test_launcher_sets_local_ip_and_runs_existing_job(monkeypatch, tmp_path):
    job = tmp_path / "example.py"
    job.write_text("result = 42\n", encoding="utf-8")
    calls = []

    def fake_run_path(path, run_name):
        calls.append((path, run_name))

    monkeypatch.delenv("SPARK_LOCAL_IP", raising=False)
    monkeypatch.setattr(local_job_launcher.runpy, "run_path", fake_run_path)

    local_job_launcher.run_job(str(job.with_suffix("")))

    assert os.environ["SPARK_LOCAL_IP"] == "127.0.0.1"
    assert calls == [(str(job), "__main__")]


def test_launcher_rejects_missing_job():
    with pytest.raises(FileNotFoundError, match="Job file not found"):
        local_job_launcher.run_job("does-not-exist.py")


def test_launcher_main_delegates_to_selected_job(monkeypatch):
    calls = []
    monkeypatch.setattr(sys, "argv", ["local_job_launcher", "example.py"])
    monkeypatch.setattr(local_job_launcher, "run_job", calls.append)

    assert local_job_launcher.main() == 0
    assert calls == ["example.py"]


def test_spark_runtime_honors_environment_contract(monkeypatch):
    monkeypatch.setenv("SPARK_MASTER", "local[1]")
    monkeypatch.setenv("SPARK_APP_NAME", "infrastructure-test")
    monkeypatch.setenv("SPARK_UI_PORT", "4051")

    spark = build_spark_session()
    try:
        assert spark.sparkContext.master == "local[1]"
        assert spark.sparkContext.appName == "infrastructure-test"
        assert spark.conf.get("spark.ui.enabled") == "true"
        assert spark.conf.get("spark.ui.port") == "4051"
    finally:
        spark.stop()


def test_spark_sample_job_returns_expected_count():
    assert run_sample_job() == "rows=10"


def test_spark_runtime_main_holds_ui_and_stops_session(monkeypatch, capsys):
    from src.jobs import local_spark_runtime

    monkeypatch.setenv("SPARK_SMOKE_HOLD_SECONDS", "1")
    local_spark_runtime.main()

    output = capsys.readouterr().out
    assert "Spark local runtime ready. rows=10" in output
    assert "Holding Spark UI for 1 seconds" in output


def test_schema_validator_reports_missing_schema_directory(tmp_path):
    assert validate_schemas.validate_schemas(tmp_path) == [
        f"{tmp_path}: no YAML schema files found"
    ]


def test_schema_validator_reports_malformed_yaml(tmp_path):
    malformed_schema = tmp_path / "malformed.yml"
    malformed_schema.write_text("table_name: [", encoding="utf-8")

    errors = validate_schemas.validate_schemas(tmp_path)

    assert "cannot parse YAML" in errors[0]


def test_schema_validator_reports_non_mapping_root(tmp_path):
    scalar_schema = tmp_path / "scalar.yml"
    scalar_schema.write_text("just-a-value", encoding="utf-8")

    errors = validate_schemas.validate_schemas(tmp_path)

    assert errors == [f"{scalar_schema}: root must be a YAML mapping"]


def test_schema_validator_reports_invalid_columns_and_partitions(tmp_path):
    invalid_schema = tmp_path / "invalid-columns.yml"
    invalid_schema.write_text(
        """
table_name: valid_table
description: valid description
columns: []
partitions: not-a-list
""",
        encoding="utf-8",
    )
    empty_columns_errors = validate_schemas.validate_schemas(tmp_path)
    assert any("columns must be a non-empty list" in error for error in empty_columns_errors)

    invalid_schema.write_text(
        """
table_name: valid_table
description: valid description
columns:
  - not-a-mapping
partitions: not-a-list
""",
        encoding="utf-8",
    )
    invalid_column_errors = validate_schemas.validate_schemas(tmp_path)
    assert any("columns[0] must be a mapping" in error for error in invalid_column_errors)
    assert any("partitions must be a list" in error for error in invalid_column_errors)


def test_schema_validator_main_returns_failure_for_invalid_root(monkeypatch, tmp_path, capsys):
    invalid_schema = tmp_path / "invalid.yml"
    invalid_schema.write_text("invalid: true", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["validate_schemas", str(tmp_path)])

    assert validate_schemas.main() == 1
    assert "ERROR:" in capsys.readouterr().out


def test_schema_validator_reports_contract_errors(tmp_path):
    invalid_schema = tmp_path / "invalid.yml"
    invalid_schema.write_text(
        """
table_name: InvalidName
description: 42
columns:
  - name: bad Name
    type: unknown
  - name: duplicate
    type: string
    description: first
  - name: duplicate
    type: string
    description: second
partitions:
  - missing_column
""",
        encoding="utf-8",
    )

    errors = validate_schemas.validate_schemas(tmp_path)

    assert any("table_name must use snake_case" in error for error in errors)
    assert any("description is required" in error for error in errors)
    assert any("columns[0].name must use snake_case" in error for error in errors)
    assert any("columns[0].type must be one of" in error for error in errors)
    assert any("columns[2].name is duplicated" in error for error in errors)
    assert any("partition is not a declared column" in error for error in errors)
