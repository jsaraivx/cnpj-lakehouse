from __future__ import annotations

from pathlib import Path

from pyspark.sql import SparkSession


def build_spark_session(app_name: str = "cnpj-local-runtime") -> SparkSession:
    """Create the local Spark runtime used by data engineers on their machines."""
    return (
        SparkSession.builder.master("local[1]")
        .appName(app_name)
        .config("spark.sql.shuffle.partitions", "1")
        .config("spark.default.parallelism", "1")
        .config("spark.ui.enabled", "true")
        .config("spark.sql.adaptive.enabled", "false")
        .getOrCreate()
    )


def run_sample_job() -> str:
    """Execute the smallest proven local Spark smoke-check."""
    spark = build_spark_session()
    row_count = spark.range(10).count()
    spark.stop()
    return f"rows={row_count}"


if __name__ == "__main__":
    print(f"Spark local runtime ready. {run_sample_job()}")
    print("Spark UI is available at http://localhost:4040")
