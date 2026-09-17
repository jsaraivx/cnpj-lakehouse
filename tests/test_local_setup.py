from pathlib import Path


def test_local_startup_files_exist():
    root = Path(__file__).resolve().parents[1]

    assert (root / "start_local.ps1").exists()
    assert (root / "start_local").exists()
    assert (root / "local-infra" / "docker-compose.yml").exists()


def test_local_compose_is_minio_based():
    root = Path(__file__).resolve().parents[1]
    compose = (root / "local-infra" / "docker-compose.yml").read_text(encoding="utf-8")

    assert "minio:" in compose
    assert "9000:9000" in compose
    assert "9001:9001" in compose
    assert "minio-init:" in compose
    assert "cnpj-bronze" in compose
    assert "cnpj-silver" in compose
    assert "cnpj-gold" in compose
    assert "cnpj-checkpoints" in compose


def test_readme_documents_local_commands():
    root = Path(__file__).resolve().parents[1]
    readme = (root / "README.md").read_text(encoding="utf-8")

    assert "./start_local" in readme
    assert "start_local.ps1" in readme
    assert "local_job_launcher" in readme
    assert "validate_schemas.py" in readme
