from pathlib import Path


def test_local_requirements_include_spark_and_jupyter():
    root = Path(__file__).resolve().parents[1]
    requirements = (root / "local-requirements.txt").read_text(encoding="utf-8")

    assert "pyspark==3.5.0" in requirements
    assert "jupyter" in requirements.lower()


def test_local_spark_runtime_module_exists():
    root = Path(__file__).resolve().parents[1]
    job_file = root / "src" / "jobs" / "local_spark_runtime.py"

    assert job_file.exists()
    content = job_file.read_text(encoding="utf-8")
    assert "SparkSession" in content
    assert "build_spark_session" in content
    assert "run_sample_job" in content


def test_local_runtime_supports_minio_and_spark_ui_ready_state():
    root = Path(__file__).resolve().parents[1]
    compose = (root / "local-infra" / "docker-compose.yml").read_text(encoding="utf-8")
    start_local = (root / "start_local").read_text(encoding="utf-8")
    start_local_ps1 = (root / "start_local.ps1").read_text(encoding="utf-8")

    assert "9001:9001" in compose
    assert "Spark UI" in start_local or "spark" in start_local.lower()
    assert "local-requirements" in start_local_ps1.lower()
