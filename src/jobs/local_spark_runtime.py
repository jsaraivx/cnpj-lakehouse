from __future__ import annotations

import os
import sys
import time

import pyspark
from pyspark.sql import SparkSession


def _windows_short_path(path: str) -> str:
    if os.name != "nt":
        return path

    import ctypes

    buffer = ctypes.create_unicode_buffer(32768)
    length = ctypes.windll.kernel32.GetShortPathNameW(path, buffer, len(buffer))
    return buffer.value if length else path


def build_spark_session(app_name: str = "cnpj-local-runtime") -> SparkSession:
    """Create the local Spark runtime used by data engineers on their machines."""
    os.environ.setdefault("SPARK_LOCAL_IP", "127.0.0.1")
    if os.name == "nt":
        os.environ.setdefault("SPARK_HOME", _windows_short_path(str(pyspark.__path__[0])))
        python_executable = _windows_short_path(sys.executable)
    else:
        python_executable = sys.executable
    os.environ.setdefault("PYSPARK_PYTHON", python_executable)
    os.environ.setdefault("PYSPARK_DRIVER_PYTHON", python_executable)
    configured_app_name = os.getenv("SPARK_APP_NAME", app_name)
    master = os.getenv("SPARK_MASTER", "local[2]")
    ui_port = os.getenv("SPARK_UI_PORT", "4040")
    return (
        SparkSession.builder.master(master)
        .appName(configured_app_name)
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.default.parallelism", "1")
        .config("spark.ui.enabled", "true")
        .config("spark.ui.port", ui_port)
        .config("spark.sql.adaptive.enabled", "false")
        .getOrCreate()
    )


def run_sample_job(stop_session: bool = True) -> str:
    """Execute the smallest proven local Spark smoke-check."""
    spark = build_spark_session()
    row_count = spark.range(10).count()
    if stop_session:
        spark.stop()
    return f"rows={row_count}"


def main() -> None:
    print(f"Spark local runtime ready. {run_sample_job(stop_session=False)}")
    print(f"Spark UI is available at http://localhost:{os.getenv('SPARK_UI_PORT', '4040')}")

    hold_seconds = int(os.getenv("SPARK_SMOKE_HOLD_SECONDS", "0"))
    if hold_seconds > 0:
        print(f"Holding Spark UI for {hold_seconds} seconds...")
        time.sleep(hold_seconds)

    active_session = SparkSession.getActiveSession()
    if active_session is not None:
        active_session.stop()


if __name__ == "__main__":
    main()
