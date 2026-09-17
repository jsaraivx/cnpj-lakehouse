#!/usr/bin/env bash
set -euo pipefail

# Creates GitHub issues from the local BOARD.md using the GitHub CLI `gh`.
# Usage: ./scripts/create_github_issues.sh [owner/repo]
# Requirements: `gh` installed and authenticated (gh auth login)

REPO=${1:-$(git remote get-url origin 2>/dev/null || echo "")} 
if [ -z "$REPO" ]; then
  echo "Usage: $0 owner/repo" >&2
  exit 1
fi

# normalize repo URL to owner/repo if git url provided
if [[ "$REPO" =~ @|:// ]]; then
  REPO=$(echo "$REPO" | sed -E 's#.*[:/]+([^/]+/[^/]+)(\.git)?#\1#')
fi

echo "Creating issues in repository: $REPO"

declare -a TITLES
declare -a BODIES
declare -a LABELS

TITLES+=("Schema: Implement YAML to PySpark StructType converter")
BODIES+=("Implement a converter that reads YAML schema files from `schemas/{bronze,silver,gold}` and generates a PySpark `StructType`.\n\nLocation: src/utils/schema_codegen.py\nEstimate: 3\nAcceptance: unit test + smoke test + README snippet explaining usage.")
LABELS+=("area/schemas,priority/high")

TITLES+=("Test: add smoke test for schema converter")
BODIES+=("Add a lightweight smoke test that imports the converter and constructs a `StructType` from the example template at `schemas/templates/table_schema_example.yml`.\n\nLocation: tests/test_schema_codegen.py\nEstimate: 1\nAcceptance: tests pass on CI locally with pytest.")
LABELS+=("area/tests,priority/high")

TITLES+=("ETL: example PySpark local ingest job for Bronze")
BODIES+=("Create an example PySpark job that reads local CSV, applies the generated StructType and writes to local MinIO as parquet/iceberg-compatible files.\n\nLocation: spark_jobs/bronze/ingest_example.py\nEstimate: 5\nAcceptance: runs locally with start_local and writes sample output to bucket.")
LABELS+=("area/etl,priority/high")

TITLES+=("MinIO: validate integration and provide create-buckets script")
BODIES+=("Add a small script that creates the expected S3 buckets in local MinIO using AWS CLI or mc and documents bucket names.\n\nLocation: scripts/create_buckets.sh\nEstimate: 1\nAcceptance: script creates buckets when MinIO is running locally.")
LABELS+=("area/infrastructure,priority/medium")

echo "Will create ${#TITLES[@]} issues. Continue? (y/N)"
read -r CONFIRM
if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
  echo "Aborted."
  exit 0
fi

ISSUE_URLS=()
for i in "${!TITLES[@]}"; do
  title=${TITLES[$i]}
  body=${BODIES[$i]}
  labels=${LABELS[$i]}
  echo "Creating issue: $title"
  url=$(gh issue create --repo "$REPO" -t "$title" -b "$body" --label "$labels" --assignee "" 2>/dev/null || gh issue create --repo "$REPO" -t "$title" -b "$body" --label "$labels")
  echo " -> $url"
  ISSUE_URLS+=("$url")
done

echo ""
echo "Created issues:"
for u in "${ISSUE_URLS[@]}"; do
  echo "$u"
done

echo ""
echo "Create a GitHub Project manually or with GH CLI and add the created issues as cards." 
echo "To create a repository project via gh:" 
echo "  gh project create --repo $REPO --name \"CNPJ Lakehouse Board\" --body \"Board created from BOARD.md\"" 
echo "After creating the project, open it in the browser and add the issues as cards (drag & drop)."

exit 0
