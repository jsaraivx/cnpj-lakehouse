from pathlib import Path

from scripts.validate_schemas import validate_schemas


def test_repository_schemas_follow_contract():
    root = Path(__file__).resolve().parents[1]

    assert validate_schemas(root / "schemas") == []
