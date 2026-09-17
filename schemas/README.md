Schemas organization
=====================

This folder contains table schema definitions organized by medallion layer.

Layout
- `schemas/bronze/`    : raw ingested table schemas (source canonical)
- `schemas/silver/`    : cleansed and standardized schemas
- `schemas/gold/`      : aggregated/business schemas and graph tables
- `schemas/templates/` : templates for schema files and examples

Conventions
- Use YAML for table schema (name, columns, types, description, partitioning).
- Name files as `<layer>.<table_name>.yml` or `<table_name>.yml` inside the layer folder.
- Keep small readable examples in `schemas/templates/` to onboard engineers.

Workflow
- Each engineer adds schema files under the appropriate layer and opens a PR.
- The tech lead reviews and approves schema changes for compatibility.
