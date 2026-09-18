# Repository Conventions: Branch, PR and Release

## Branching

- Main integration branch: `main` (or `develop` if configured by repository admin).
- Feature branch format: `feature/<scope>-<short-name>`.
- Bugfix branch format: `fix/<scope>-<short-name>`.
- Hotfix branch format: `hotfix/<short-name>`.

## Commit Strategy

- Use atomic commits: one responsibility per commit.
- Conventional messages:
  - `feat(scope): ...`
  - `fix(scope): ...`
  - `docs(scope): ...`
  - `chore(scope): ...`

## Pull Request Flow

- Rebase or merge latest target branch before opening PR.
- PR template must include:
  - task/issue id
  - local validation commands
  - acceptance criteria evidence
- Require the documented local validation commands to pass before merge.
- Require at least one approval.

## Release Flow

- Merge completed features into integration branch continuously.
- Cut release branch as needed: `release/<yyyy-mm-dd>-<tag>`.
- Tag release after smoke validation in protected branch.

## Minimum Quality Gate for Infra and Data PRs

- `python scripts/validate_schemas.py`
- `pytest -q --cov=src.jobs.local_job_launcher --cov=src.jobs.local_spark_runtime --cov=scripts.validate_schemas --cov-fail-under=85`
- `python -m src.jobs.local_spark_runtime`
- `docker compose -f local-infra/docker-compose.yml ps`
- README/docs updated when behavior or contracts change.

GitHub Actions and hosted CI are intentionally deferred until the AWS/Terraform production migration. Local development must not depend on hosted CI or cloud resources.
