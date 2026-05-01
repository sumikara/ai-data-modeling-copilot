This file defines binding rules for the AI Copilot.

# Retail DWH Core Design Principles

## Purpose
This document defines core architectural principles for the Retail Data Warehouse (DWH) reference project. The AI Data Modeling Copilot must use these principles as local, project-specific guidance for modeling, SQL generation, and design review.

## AI Copilot Usage Rules
- Treat this document as normative for retail DWH architectural reasoning.
- Preserve the distinction between key types, layer duties, and behavior contracts.
- Do not collapse governance controls into convenience shortcuts.
- If an implementation tradeoff conflicts with these rules, raise `DECISION_REQUIRED` with explicit options.

## 1) Identity Governance
Never conflate the following identity types:

| Identity Type | Pattern | Meaning | Lifecycle |
|---|---|---|---|
| Raw/Natural Key | `*_nk` | Source-origin business identifier captured for traceability | Preserved from source | 
| Source-Derived Semantic Key | `*_src_id` | Engineered semantic identifier built after profiling/standardization | Created in mapping layer |
| Warehouse Surrogate Key | `*_id` or `*_key` | Internal relational key for warehouse integrity and joins | Created in NF/DM layers |

Rules:
- `*_nk` preserves raw source traceability.
- `*_src_id` is generated in mapping after profiling and expresses semantic identity.
- Surrogate keys are generated in NF/DM to support relational consistency.
- Source keys must not be accepted as enterprise identity keys without reconciliation.

AI reasoning rule:
- Always reason separately about raw source key, engineered semantic source key, and surrogate warehouse key.

## 2) Layer Responsibility
Each layer has one primary responsibility.

| Layer | Responsibility |
|---|---|
| Raw / External | Land source data as-is |
| Clean Staging | Standardize text, parse types, and normalize null handling |
| Mapping | Create entity candidates, preserve lineage, generate `*_src_id` |
| 3NF / NF | Resolve entities, enforce relationships, apply SCD behavior |
| Dimensional / Mart | Serve reporting and analytics |

Rules:
- Do not mix cleansing, identity creation, FK resolution, and reporting in one layer.
- Keep transformations aligned to layer purpose to preserve auditability and rerun safety.

## 3) Fault-Tolerant Loading
`LEFT JOIN` is a controlled error-tolerance strategy for fact loading.

Required pattern:
1. `LEFT JOIN` to dimensions
2. Fallback to a governed default row
3. `COALESCE(..., -1)` (or project-approved default key)

Rules:
- Fact-like records must not be dropped solely due to dimension lookup misses.
- Default rows are governance objects and must be curated, not treated as null padding.

## 4) Behavior-First Modeling
Define SCD behavior before writing procedure logic.

Rules:
- SCD type selection is a business behavior decision.
- Full vs incremental execution mode must not alter entity meaning.
- Procedures implement pre-defined behavior contracts; they must not invent behavior.

## 5) Deduplication Strategy
`ROW_NUMBER()` serves two architectural roles:

1. Operational deduplication when multiple valid candidates exist.
2. Standardized design pattern for reusable automation.

Rules:
- Deduplication must explicitly document winner-selection criteria.
- Deterministic ordering attributes must be declared for replay-safe outcomes.

## 6) Lineage and Auditability
Every layer must preserve provenance metadata.

Required provenance fields:
- `source_system`
- `source_table`
- `source_file_name`
- `batch_id`
- `load_type`
- `insert_dt`
- `update_dt`

Rule:
- Lineage columns are model-governance requirements, not optional decorations.

## 7) Logging and Orchestration
Each procedure must emit execution observability.

Minimum execution trail:
- success
- no change
- failure
- row counts
- error diagnostics

Common operational tables may include:
- `etl_batch_run`
- `etl_step_run`
- `etl_file_registry`
- `etl_log`

## 8) Mapping Layer Strategy
The mapping layer is semantic reconciliation, not final survivorship.

It should:
- preserve standardized source evidence,
- generate `*_src_id`,
- avoid premature final survivorship decisions,
- support downstream 3NF entity resolution.

## 9) Referential Modeling
3NF expresses relationship truth, not reporting convenience.

Rules:
- Fact-like normalized transaction structures should resolve surrogate keys.
- Normalized transaction structures must still retain source lineage for traceability.

## 10) Design Philosophy
Prefer explicit design contracts over implicit assumptions.

Every solution must document:
- key formation,
- deduplication logic,
- unknown/default handling,
- SCD behavior,
- lineage,
- logging.

## Cross-Document Harmonization Notes
The following items appear potentially inconsistent with existing local rules and require confirmation before unification:

- `DECISION_REQUIRED`: Existing `knowledge_base/local_rules/layer_responsibilities.md` states landing includes controlled standardization and early duplicate reduction, while this document separates those concerns into a dedicated clean staging layer. Confirm canonical boundary between landing and staging.
