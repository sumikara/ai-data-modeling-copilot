This file defines binding rules for the AI Copilot.

# Architecture, Naming, Tools, and Governance

## Purpose
Define project-level architecture flow, naming conventions, tooling boundaries, and governance controls for the Retail DWH reference implementation.

## AI Copilot Usage Rules
AI should:
- recommend schema-based access control,
- separate analyst access from ETL access,
- prefer views to hide sensitive columns,
- treat governance as a first-class architecture concern.

## Architecture Overview
High-level warehouse flow:

```text
Source CSV files
→ file_fdw foreign tables
→ SA (source access layer)
→ CL (cleansing/mapping layer)
→ 3NF integration layer
→ DM dimensional layer
→ Power BI/reporting
```

## Architecture Goals
- clarity,
- scalability,
- maintainability,
- traceability,
- rerunnability,
- modularity.

## Tooling

### PostgreSQL
Core relational engine for schemas, tables, roles, metadata, and warehouse SQL logic.

### pgAdmin
Administration surface used for:
- server connectivity,
- database creation,
- restore operations,
- role management,
- metadata/system inspection.

### DBeaver
Development surface used for:
- SQL authoring,
- query execution,
- script organization,
- catalog browsing.

### Python / VS Code / Colab / Drive
Used for:
- raw dataset preparation,
- online/offline source splitting,
- synthetic-column generation,
- local/Colab experimentation,
- moving CSV files into DB-readable paths.

## Why pgAdmin and DBeaver Together
- pgAdmin answers: **How is the database platform configured and administered?**
- DBeaver answers: **How do developers work with SQL and data inside that platform?**

## Naming Standards
Rules:
- lowercase identifiers,
- `snake_case`,
- no quoted identifiers,
- no spaces,
- no special characters.

## Key Naming
| Key Type | Preferred Pattern |
|---|---|
| raw key | `*_nk` or `*_raw_id` |
| source-derived key | `*_src_id` |
| 3NF surrogate key | `*_id` |
| dimensional surrogate key | `*_key` or `*_surr_id` |

## Metrics Naming
| Metric Semantic | Suffix |
|---|---|
| quantity | `_qty` |
| amount | `_amt` |
| count | `_cnt` |
| percent | `_pct` |

## Sequence Policy
- Use explicit sequences.
- Do not use `SERIAL`.

## Security and Governance
### Role Model
- analyst (read-only),
- ETL runner,
- DBA.

### Access Principles
- Analysts read DM and selected NF objects.
- Analysts should not access raw/staging directly.
- ETL runner writes pipeline layers.
- Sensitive columns may be masked through views.
- Optional RLS can be applied for sensitive employee/customer attributes.

## Audit Expectations
Security and ETL audit trails should capture:
- user,
- timestamp,
- schema/table,
- operation,
- row identifier,
- old/new values where applicable.

## Cross-Document Harmonization Notes
- `DECISION_REQUIRED`: This document uses `SA` and `CL` abbreviations for early layers, while existing local rules describe `Raw/External`, `Clean Staging`, and `Mapping`. Confirm canonical layer taxonomy/abbreviation standard for repository-wide documentation consistency.
