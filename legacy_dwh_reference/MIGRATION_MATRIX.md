# Legacy DWH Migration Matrix (Initial Assessment)

## Scope and reality check
This repository currently contains only a scaffold (folders + `.gitkeep`) and no legacy DWH source assets (SQL, pipelines, mappings, tests, docs, diagrams).

Practical implication: there is nothing substantive to migrate yet. The matrix below classifies what exists now and what must be created once the actual legacy repository content is provided.

---

## File-by-file migration matrix (current repo state)

| Current path | Recommended new path inside `ai-data-modeling-copilot` | Keep / Drop / Refactor / Merge | Reason | AI Copilot role | Priority | Notes before migration |
|---|---|---|---|---|---|---|
| `legacy_dwh_reference/README.md` | `legacy_dwh_reference/00_environment_setup/README.md` (canonical index) | Refactor + Move content | README currently just lists folders; convert into canonical corpus index with links, ownership, source system inventory, and migration status. | evidence/documentation | P0 | Add sections: scope, source systems, naming conventions, dependency graph, migration decisions log. |
| `legacy_dwh_reference/00_environment_setup/.gitkeep` | Keep as placeholder until real files arrive | Keep | Placeholder for empty directory tracking. | reference only | P2 | Replace with real setup artifacts (`env_setup.sql`, `grants.sql`, `roles.md`) once available. |
| `legacy_dwh_reference/01_data_ingestion/.gitkeep` | Keep as placeholder until real files arrive | Keep | Placeholder only; no ingestion logic exists. | reference only | P2 | Expect connectors, raw landing SQL, ingestion specs, job configs. |
| `legacy_dwh_reference/02_orchestration_logging/.gitkeep` | Keep as placeholder until real files arrive | Keep | Placeholder only; no orchestration or logging artifacts exist. | reference only | P2 | Expect DAG/workflow defs, scheduler configs, retry policies, audit schemas. |
| `legacy_dwh_reference/03_staging_layer/.gitkeep` | Keep as placeholder until real files arrive | Keep | Placeholder only; no staging DDL/DML exists. | reference only | P2 | Expect staging table DDL, load SQL, contracts, grain notes. |
| `legacy_dwh_reference/04_profiling/.gitkeep` | Keep as placeholder until real files arrive | Keep | Placeholder only; no profiling notebooks/scripts/reports exist. | reference only | P2 | Expect profiling SQL/Python and generated profile outputs. |
| `legacy_dwh_reference/05_mapping_layer/.gitkeep` | Keep as placeholder until real files arrive | Keep | Placeholder only; no source→target mapping assets exist. | reference only | P2 | Expect mapping sheets, transformation rules, code mapping dictionaries. |
| `legacy_dwh_reference/06_normalized_layer/.gitkeep` | Keep as placeholder until real files arrive | Keep | Placeholder only; no normalized-model assets exist. | reference only | P2 | Expect 3NF DDL, PK/FK constraints, integrity rules. |
| `legacy_dwh_reference/07_dimensional_layer/.gitkeep` | Keep as placeholder until real files arrive | Keep | Placeholder only; no marts/star schema SQL exists. | reference only | P2 | Expect dimension/fact DDL, semantic definitions, BI consumption notes. |
| `legacy_dwh_reference/08_scd_logic/.gitkeep` | Keep as placeholder until real files arrive | Keep | Placeholder only; no SCD implementation exists. | reference only | P2 | Expect SCD1/2 merge SQL, surrogate key policy, effective dating logic. |
| `legacy_dwh_reference/09_validation_tests/.gitkeep` | Keep as placeholder until real files arrive | Keep | Placeholder only; no data quality tests exist. | reference only | P2 | Expect row-count reconciliation, null checks, RI checks, threshold tests. |
| `legacy_dwh_reference/10_known_errors_and_fixes/.gitkeep` | Keep as placeholder until real files arrive | Keep | Placeholder only; no known-issues knowledge base exists. | reference only | P2 | Expect runbooks: symptom, cause, query to verify, fix, prevention. |

---

## Special handling decisions

### Files that should **NOT** be migrated
- `.gitkeep` files should not be treated as legacy knowledge artifacts; they are operational placeholders only.
- Any future transient files should be excluded when discovered (examples: `.log`, temporary exports, local cache, notebook checkpoints).

### Files that should be merged into one canonical document
When actual legacy files are available, merge these into canonical docs per domain:
- Multiple architecture READMEs -> `legacy_dwh_reference/00_environment_setup/architecture_overview.md`
- Multiple troubleshooting notes -> `legacy_dwh_reference/10_known_errors_and_fixes/known_issues_canonical.md`
- Multiple mapping sheets for same entities -> `legacy_dwh_reference/05_mapping_layer/source_to_target_mapping_canonical.md`

### Bad naming patterns to rename (policy)
Apply this naming policy once real files are imported:
- Replace spaces with `_`
- Use lowercase snake_case
- Prefix SQL by layer and sequence, e.g. `stg_010_customer_load.sql`, `dim_020_build_customer.sql`
- Encode SCD type in filename, e.g. `dim_customer_scd2_merge.sql`
- Rename vague names like `final.sql`, `test_new.sql`, `script1.py` to purpose-specific names.

### Missing files to create manually after migration
Create these foundational docs/scripts even if absent in legacy repo:
- `legacy_dwh_reference/00_environment_setup/migration_decisions_log.md`
- `legacy_dwh_reference/00_environment_setup/dependency_inventory.md`
- `legacy_dwh_reference/00_environment_setup/security_and_pii_notes.md`
- `legacy_dwh_reference/04_profiling/profiling_playbook.md`
- `legacy_dwh_reference/09_validation_tests/validation_test_catalog.md`
- `legacy_dwh_reference/10_known_errors_and_fixes/incident_template.md`

---

## Target matrix template for actual legacy repository ingestion
Use this template immediately after connecting the real legacy repository:

| Current path | Recommended new path | Keep/Drop/Refactor/Merge | Reason | AI Copilot role | Priority | Notes before migration |
|---|---|---|---|---|---|---|
| `<legacy/path/file.sql>` | `legacy_dwh_reference/<layer>/<new_name>.sql` | Refactor | Standardize naming + remove hardcoded schema | reusable tool logic | P0 | Validate dependencies and run order first |

---

## End-state action lists

### 1) Migrate first
1. Real architecture docs (README, ERD/schema diagrams, dependency docs) into `00_environment_setup`.
2. SQL setup and grants scripts.
3. Core ingestion and orchestration assets required to reproduce loads.
4. Critical mapping files that define source-to-target business logic.
5. Validation suites needed to prove parity.

### 2) Refactor before migrating
1. Any SQL with hardcoded environment names/schema names.
2. Duplicate mapping files with conflicting logic.
3. Ambiguous script names (`final`, `new`, `temp`, `v2`).
4. Mixed business + technical docs that should be split into runbooks vs architecture.

### 3) Do not migrate
1. Placeholder files (`.gitkeep`) as knowledge artifacts.
2. Temporary logs, ad-hoc extracts, local IDE metadata, notebook checkpoints.
3. Obsolete one-off scripts with no lineage relevance and no production usage proof.

### 4) Create manually
1. Canonical migration decisions log.
2. Canonical validation test catalog.
3. Canonical known-issues runbook template.
4. Naming convention + SQL style guide for future ingestion.
5. Data contract template for each ingestion source.

