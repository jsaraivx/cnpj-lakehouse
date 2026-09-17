COLLABORATION GUIDE
===================

This document describes collaboration rules and workflows for contributors.

1. Branches
- Use feature branches: `feature/<short>-<description>` (example: `feature/schema-converter`).
- Keep branches small and focused; one logical change per branch.

2. Commits
- Make commits atomic and focused. Use present-tense, lower-case, conventional messages: `feat(...)`, `fix(...)`, `chore(...)`, `docs(...)`.

3. Pull Requests
- Target branch: `develop` (or the repo main development branch).
- Include a short description, motivation, how to run locally, and the acceptance criteria.
- Include smoke instructions where applicable (commands to run locally).

4. Code Review
- At least one approving review required before merge.
- Reviewers should verify: tests pass, code is readable, no secrets or large dataset files committed.

5. Issues and Board
- Create an issue per task and move it to the board column. Use labels: `area/schemas`, `area/etl`, `area/tests`, `priority/high`.

6. Testing & Local Development
- Use `./start_local` (macOS/Linux) or `.\start_local.ps1` (Windows) to prepare local environment and start MinIO.
- Tests: run `pytest -q` from the repository root. Add smoke tests for new functionality.

7. Schema Changes
- Edit YAML files under `schemas/{bronze,silver,gold}`.
- Update or add converter usage in `src/utils/schema_codegen.py` if types change.
- Include a unit or smoke test that imports the schema and generates a `StructType`.

8. Pull Request Checklist (add to PR description)
- [ ] The change is covered by tests (unit or smoke).
- [ ] Local `start_local` run (if infra needed) works.
- [ ] README or docs updated if public behavior changed.
- [ ] Labels added: `area/*`, `priority/*`.

9. Onboarding
- New engineers should run `./start_local` and then `pytest -q`.
- Read `schemas/README.md` for schema editing conventions.

10. Communication
- Use project Slack/Teams channel for blockers and PR notifications.
