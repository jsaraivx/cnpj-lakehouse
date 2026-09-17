from __future__ import annotations

import argparse
import os
import runpy
from pathlib import Path


def _normalize_job_path(job: str) -> str:
    if job.endswith(".py"):
        return job
    return f"{job}.py"


def run_job(job: str) -> None:
    job_path = _normalize_job_path(job)
    if not Path(job_path).exists():
        raise FileNotFoundError(f"Job file not found: {job_path}")

    os.environ.setdefault("SPARK_LOCAL_IP", "127.0.0.1")
    runpy.run_path(job_path, run_name="__main__")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a local PySpark job with project runtime defaults."
    )
    parser.add_argument(
        "job",
        help="Path to a Python job file. Example: src/jobs/local_spark_runtime.py",
    )
    args = parser.parse_args()

    run_job(args.job)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
