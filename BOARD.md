# Project Board — CNPJ Lakehouse

Objetivo: priorizar trabalho para desenvolvimento local e lógica de processamento de dados.

Como usar
- Cada engenheiro escolhe uma task, cria branch `feature/<short>-<task>` e abre um PR.
- Mantenha commits atômicos e aponte o PR para `develop` (ou branch principal do time).
- Marque o cartão como `In Progress` ao começar e `Done` ao finalizar e abrir PR aprovado.

Branch naming
- `feature/<short>-<description>` (ex.: `feature/schema-converter`)

Prioridade alta — começar aqui

- [ ] Schema: implementar conversor YAML → `StructType` (`src/utils/schema_codegen.py`) — Est: 3
  - Descrição: ler arquivos em `schemas/*/*.yml` e gerar `StructType` no runtime.
  - Branch sugerida: `feature/schema-converter`

- [ ] Test: adicionar smoke test para conversor (`tests/test_schema_codegen.py`) — Est: 1

- [ ] ETL local runner: exemplo PySpark job que lê dados brutos e aplica schema (`spark_jobs/bronze/ingest_example.py`) — Est: 5

- [ ] MinIO: validar integração e criar instruções de buckets (ex.: script `scripts/create_buckets.sh`) — Est: 1

Próximo nível — cross-team

- [ ] CI: validar YAML schemas em PR (parser + generate StructType) — Est: 2

- [ ] DBT/docs: esqueleto de modelos Gold com dependência do schema — Est: 3

- [ ] Graph job: exemplo com GraphFrames que cria matriz arestas — Est: 5

Backlog / melhorias

- [ ] Linter de schemas e checklist de PR para esquemas (contribuição) — Est: 1
- [ ] Adicionar exemplos de datasets de teste (pequenos CSVs) para execução local — Est: 2

Regras de aceitação (para cada task)
- Código funcionando localmente com `start_local` ativo (venv + MinIO).
- Testes mínimos adicionados e passando (`pytest`).
- PR com descrição clara, exemplos de uso, e labels: `area/schemas`, `area/etl`, `priority/high`.

Comunicação
- Use o canal do Slack/Teams do projeto para avisar sobre PRs e bloqueios.
