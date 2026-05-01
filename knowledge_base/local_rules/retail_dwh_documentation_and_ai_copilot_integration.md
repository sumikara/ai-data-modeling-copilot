This file defines binding rules for the AI Copilot.

# Retail DWH Documentation and AI Copilot Integration

## Purpose
Define how Retail DWH documentation should be structured and how it should feed AI Copilot reasoning workflows.

## AI Copilot Usage Rules
AI must not:
- treat documentation as final truth when code/evidence conflicts,
- finalize customer identity conflict silently,
- hide synthetic-data limitations,
- claim full production readiness without caveats.

## Recommended README Structure

### 1) Project Overview
Describe:
- SQL-native end-to-end Retail DWH,
- hybrid Inmon-Kimball approach,
- ELT/ETL pipeline,
- PostgreSQL + PL/pgSQL,
- `file_fdw` ingestion,
- RAG-ready documentation strategy.

### 2) Why This Project Exists
Explain:
- OLTP vs OLAP separation,
- need for analytical warehouse,
- multi-source integration,
- data-quality and lineage requirements,
- reporting readiness goals.

### 3) Dataset Context
Link dataset context docs and explain:
- synthetic Kaggle source,
- online/offline split,
- 95% bulk / 5% incremental simulation,
- added synthetic entities,
- realism limitations/caveats.

### 4) Architecture
Include placeholder:
- `[Insert architecture diagram: Source CSV → SA → CL → 3NF → DM → BI]`

### 5) Data Flow
Include placeholder:
- `[Insert pipeline flow diagram]`

### 6) Layer Responsibility Table
Include layers:
- source/access,
- staging/cleansing,
- mapping,
- 3NF,
- dimensional mart,
- analytics.

### 7) Business Process Matrix
Include placeholder:
- `[Insert bus matrix: Business Process × Dimensions]`

### 8) ERD / Snowflake / Star Schema
Recommended diagram set:
- source-to-staging flow,
- 3NF normalized/snowflake schema,
- dimensional star schema,
- end-to-end lineage flow,
- fact-to-dimension relationship map.

### 9) Key Concepts Table
Include and define:
- ETL,
- ELT,
- normalization,
- denormalization,
- CIF,
- Kimball,
- Inmon,
- surrogate key,
- natural key,
- source-derived key,
- SCD0,
- SCD1,
- SCD2,
- default row,
- lineage,
- idempotency,
- `row_sig` / MD5,
- partitioning,
- indexing.

### 10) Data Profiling Summary
Document:
- transaction-line grain finding,
- entity business key decisions,
- unresolved customer decision conflict,
- employee-store synthetic realism limitation,
- promotion/delivery identity complexity.

### 11) DQ Framework
Include DQ table covering:
- completeness,
- uniqueness,
- validity,
- consistency,
- accuracy/plausibility,
- timeliness.

### 12) Implementation Highlights
Mention where implemented:
- `file_fdw` + foreign tables,
- rerunnable SQL scripts,
- `LEFT JOIN` + default rows,
- source triplet lineage,
- explicit sequences,
- ETL logging,
- employee SCD2,
- MD5 row signatures,
- range partitioning (if implemented),
- indexes.

### 13) Future Work
Possible roadmap:
- test-case expansion,
- formal DQA framework,
- KPI layer,
- Power BI dashboard,
- materialized views,
- cloud migration patterns,
- mapping for S3/Redshift/Athena/Snowflake/BigQuery.

## Entity Markdown Template
```markdown
# Entity: <Entity Name>

## Grain
One row = ...

## Source Systems
- ...

## Natural Key / Raw Key
...

## Engineered Source Key
...

## Surrogate Key
...

## SCD Type
...

## Key Attributes
| attribute | description |
|---|---|

## Data Quality Observations
...

## Lineage
CSV → foreign table → source table → mapping → NF → DIM/FACT

## Modeling Decision
...

## Known Caveats
...
```

## Troubleshooting Reference
Maintain `docs/troubleshooting.md` as the operational issue index for loading, quality, SCD, permissions, and channel-rule failures.

## AI Copilot Integration Scope
These documentation artifacts should feed:
- knowledge-base retrieval,
- decision-gate prompts,
- semantic profiling agent context,
- entity-specific reasoning,
- README-generation assistant,
- troubleshooting assistant.

## Cross-Document Harmonization Notes
- `DECISION_REQUIRED`: README placeholders use `SA/CL` layer abbreviations, while other local rules use `Raw`, `Clean Staging`, and `Mapping`. Confirm one canonical naming vocabulary for diagrams, README templates, and Copilot prompts.
