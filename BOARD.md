# Project Board — CNPJ Lakehouse

Objetivo: entregar o pipeline de dados em PySpark para ingestão, padronização, enriquecimento e grafo de sócios, com foco em engenharia de dados e processamento local.

## Como usar
- Cada task vira uma issue pequena e autocontida.
- Cada data engineer escolhe uma task e cria `feature/<short-task-name>`.
- Ao iniciar, mover para `In Progress`.
- Ao finalizar, abrir PR e marcar como `Done`.
- Commits devem ser atômicos e focados em uma responsabilidade por vez.

## Responsáveis
- Dev 1: Spark local + Jupyter + MinIO + runtime de jobs
- Dev 2: bronze + schemas + ingestão
- Dev 3: silver + fatos + enriquecimento
- Dev 4: gold + grafo + documentação + qualidade
- Tech Lead: DevOps + infra de suporte + CI/CD + ambiente base

## Backlog de engenharia de dados (Spark-first)

### P0 — Runtime local para processamento
- [x] Issue: `Create local Spark + Jupyter runtime for data engineers`
  - Assignee: Dev 1
  - Labels: `area/spark`, `priority/high`
  - Scope: subir Spark local com Jupyter e MinIO usando `start_local`, deixando ambiente pronto para testar jobs Python.
  - Acceptance: o ambiente sobe em um único comando e o Spark UI está funcional.

- [x] Issue: `Validate local job execution and Spark UI visibility`
  - Assignee: Dev 1
  - Labels: `area/spark`, `priority/high`
  - Scope: garantir que `job.py` rode localmente e apareça no Spark UI com logs visíveis.
  - Acceptance: job simples executa com sucesso e pode ser inspecionado no UI.

- [x] Issue: `Bootstrap MinIO buckets for local data processing`
  - Assignee: Dev 1
  - Labels: `area/minio`, `priority/high`
  - Scope: criar buckets e estrutura de armazenamento local para bronze/silver/gold.
  - Acceptance: jobs escrevem em MinIO local sem intervenção manual.

- [x] Issue: `Create local job launcher for PySpark scripts`
  - Assignee: Dev 1
  - Labels: `area/spark`, `priority/high`
  - Scope: centralizar a forma de executar um job local com parâmetros simples.
  - Acceptance: qualquer dev consegue rodar `python job.py` e acompanhar no Spark UI.

### P0 — Schemas e tabelas de domínio
- [ ] Issue: `Map all CNPJ source tables and business keys`
  - Assignee: Dev 2
  - Labels: `area/schemas`, `priority/high`
  - Scope: mapear empresas, estabelecimentos, sócios, simples, municípios, países, natureza jurídica, qualificações e CNAEs.
  - Acceptance: dicionário mapeado com nomes, tipos, chaves e regras de negócio.

- [ ] Issue: `Create YAML schema templates for bronze domain tables`
  - Assignee: Dev 2
  - Labels: `area/schemas`, `priority/high`
  - Scope: criar arquivos YAML para cada tabela do CNPJ.
  - Acceptance: schemas versionados, legíveis e reusáveis em qualquer job.

- [ ] Issue: `Define type and naming convention rules for all tables`
  - Assignee: Dev 2
  - Labels: `area/schemas`, `priority/high`
  - Scope: padronizar nomes em snake_case, datas, CNPJ/CPF e campos sensíveis.
  - Acceptance: toda tabela segue o mesmo padrão no projeto.

- [ ] Issue: `Create lookup tables for municipalities, countries, CNAE and legal nature`
  - Assignee: Dev 2
  - Labels: `area/reference`, `priority/medium`
  - Scope: montar dicionários para código-descrição e joins analíticos.
  - Acceptance: tabelas de referência prontas para enriquecimento.

### P1 — Bronze ingestion jobs
- [ ] Issue: `Build bronze ingest job for companies`
  - Assignee: Dev 2
  - Labels: `area/bronze`, `priority/high`
  - Scope: ler dados brutos de empresas e gravar bronze com schema aplicado.
  - Acceptance: dados consistentes com layout original e persistidos no storage local.

- [ ] Issue: `Build bronze ingest job for establishments`
  - Assignee: Dev 2
  - Labels: `area/bronze`, `priority/high`
  - Scope: processar estabelecimentos, endereço, município e CNAE fiscal.
  - Acceptance: bronze de estabelecimentos pronto para silver.

- [ ] Issue: `Build bronze ingest job for partners`
  - Assignee: Dev 2
  - Labels: `area/bronze`, `priority/high`
  - Scope: processar sócios, representantes legais e dados de entrada na sociedade.
  - Acceptance: bronze de sócios pronto e sem perdas de campos essenciais.

- [ ] Issue: `Build bronze ingest job for Simples and MEI data`
  - Assignee: Dev 2
  - Labels: `area/bronze`, `priority/high`
  - Scope: processar Simples e MEI com histórico e datas relevantes.
  - Acceptance: tabela carregada corretamente e pronta para silver.

- [ ] Issue: `Build bronze ingest job for reference tables`
  - Assignee: Dev 2
  - Labels: `area/bronze`, `priority/medium`
  - Scope: importar países, municípios, qualificações, naturezas e CNAEs.
  - Acceptance: dicionários de domínio carregados e validados.

### P1 — StructType and validation
- [ ] Issue: `Implement YAML to PySpark StructType converter`
  - Assignee: Dev 2
  - Labels: `area/schemas`, `priority/high`
  - Scope: converter YAML em `StructType` para uso nos jobs Spark.
  - Acceptance: converter validado em pelo menos um job real e com teste de smoke.

- [ ] Issue: `Add schema smoke tests`
  - Assignee: Dev 2
  - Labels: `area/tests`, `priority/high`
  - Scope: validar leitura do YAML, nomes, tipos e campos obrigatórios.
  - Acceptance: `pytest` passa no cenário mínimo.

### P2 — Silver layer and data quality
- [ ] Issue: `Normalize companies in silver layer`
  - Assignee: Dev 3
  - Labels: `area/silver`, `priority/high`
  - Scope: limpar natureza jurídica, porte, capital social, EFR e status cadastral.
  - Acceptance: dados de empresa padronizados e prontos para negócio.

- [ ] Issue: `Normalize establishments in silver layer`
  - Assignee: Dev 3
  - Labels: `area/silver`, `priority/high`
  - Scope: tratar endereço, município, CEP, DDD, telefone, e-mail e CNAE secundário.
  - Acceptance: dados de estabelecimento prontos para joins analíticos.

- [ ] Issue: `Normalize partner data in silver layer`
  - Assignee: Dev 3
  - Labels: `area/silver`, `priority/high`
  - Scope: limpar CPF/CNPJ, faixa etária, país e representante legal.
  - Acceptance: sócios com campos sensíveis descaracterizados conforme regra do projeto.

- [ ] Issue: `Normalize Simples and MEI in silver layer`
  - Assignee: Dev 3
  - Labels: `area/silver`, `priority/medium`
  - Scope: padronizar indicadores de Simples e MEI.
  - Acceptance: dados prontos para agregação analítica.

- [ ] Issue: `Deduplicate and validate silver datasets`
  - Assignee: Dev 3
  - Labels: `area/silver`, `priority/high`
  - Scope: remover duplicados e validar nulos, campos obrigatórios e inconsistências por tabela.
  - Acceptance: camada silver com qualidade mínima aceitável para downstream.

### P2 — Enrichment and business facts
- [ ] Issue: `Create enriched company and establishment fact table`
  - Assignee: Dev 3
  - Labels: `area/facts`, `priority/high`
  - Scope: montar tabela de fatos com dados de empresa + estabelecimento + endereço + atividade.
  - Acceptance: base útil para análise e dashboard.

- [ ] Issue: `Create partner-company relationship fact table`
  - Assignee: Dev 3
  - Labels: `area/facts`, `priority/high`
  - Scope: relacionar sócio à empresa e gerar chaves de conexão.
  - Acceptance: dataset pronto para grafo e redes societárias.

- [ ] Issue: `Create risk score fact table`
  - Assignee: Dev 3
  - Labels: `area/gold`, `priority/high`
  - Scope: gerar score básico de risco com sexo, porte, atividade, situação cadastral e histórico.
  - Acceptance: tabela pronta para uso analítico e validação posterior.

### P3 — Gold and graph analytics
- [ ] Issue: `Create gold dimensions for companies, establishments and partners`
  - Assignee: Dev 4
  - Labels: `area/gold`, `priority/high`
  - Scope: materializar dim_empresas, dim_estabelecimentos e dim_socios.
  - Acceptance: dimensões prontas para consumo por outros jobs e dashboards.

- [ ] Issue: `Create graph edges from partner-company relations`
  - Assignee: Dev 4
  - Labels: `area/graph`, `priority/high`
  - Scope: criar vertices e arestas para grafo de sócios e empresas.
  - Acceptance: estrutura do grafo montada e validada com amostra de dados.

- [ ] Issue: `Compute second and third degree connections`
  - Assignee: Dev 4
  - Labels: `area/graph`, `priority/high`
  - Scope: calcular ligações indiretas entre sócios e empresas.
  - Acceptance: grafo produz resultados de relacionamento de 2º e 3º grau.

- [ ] Issue: `Create network metrics summary`
  - Assignee: Dev 4
  - Labels: `area/graph`, `priority/medium`
  - Scope: gerar centralidade, densidade e resumos por rede societária.
  - Acceptance: métricas de rede disponíveis em gold/summaries.

### P3 — Quality and documentation
- [ ] Issue: `Define data quality checks per layer`
  - Assignee: Dev 4
  - Labels: `area/quality`, `priority/high`
  - Scope: definir validação de nulos, campos obrigatórios, datas e campos sensíveis por camada.
  - Acceptance: checklist de qualidade documentado e usado em PRs.

- [ ] Issue: `Write local execution guide for Windows and macOS/Linux`
  - Assignee: Dev 4
  - Labels: `area/docs`, `priority/high`
  - Scope: documentar start_local, execução de jobs e observabilidade local.
  - Acceptance: qualquer dev consegue rodar a stack sem ajuda externa.

- [ ] Issue: `Document job conventions and debugging workflow`
  - Assignee: Dev 4
  - Labels: `area/docs`, `priority/medium`
  - Scope: explicar padrões de job, inputs/outputs e troubleshooting do Spark local.
  - Acceptance: cada pipeline tem convenção explícita e fácil de repetir.

## DevOps / tech-lead track (responsabilidade do Tech Lead)
- [x] Tech Lead: `Design and document the local runtime topology`
  - Labels: `area/devops`, `priority/high`
  - Scope: diagramar stack local e regras de build/run.

- [x] Tech Lead: `Define environment variables and service contracts`
  - Labels: `area/devops`, `priority/high`
  - Scope: padronizar ports, endpoints, bucket names e configurações do ambiente.

- [ ] Tech Lead: `Create CI pipeline for schema validation and smoke tests`
  - Labels: `area/devops`, `priority/high`
  - Scope: validar YAML, parse de schemas e job mínimo em PR.
  - Status: deferred until the AWS/Terraform production migration; current validation runs locally.

- [x] Tech Lead: `Define repository conventions for branch, PR and release flow`
  - Labels: `area/devops`, `priority/medium`
  - Scope: garantir fluxo de colaboração e standards de qualidade.

- [x] Tech Lead: `Create local observability and troubleshooting playbook`
  - Labels: `area/devops`, `priority/medium`
  - Scope: documentar Spark UI, logs, health checks e diagnóstico de falhas locais.

## Regras de aceitação por task
- O job roda localmente com `start_local` ativo.
- A saída é verificável em MinIO ou em tabela local.
- Quando aplicável, existe teste mínimo de smoke.
- PR com descrição clara e evidência local.
- Labels consistentes com área e prioridade.

## Ordem recomendada
1. Spark local + Jupyter + MinIO
2. Schemas e mapeamento
3. Bronze
4. Silver
5. Fatos e enriquecimento
6. Gold e grafo
7. Qualidade e docs
8. DevOps e CI/CD

## Status do board
- [x] Backlog inicial
- [x] P0 local runtime foundation complete
- [ ] P1 em andamento
- [ ] P2 pendente
- [ ] P3 pendente
- [x] DevOps local foundation complete
- [ ] Production CI/CD deferred until AWS/Terraform migration
- [ ] Done
