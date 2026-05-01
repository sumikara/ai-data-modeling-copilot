This file defines binding rules for the AI Copilot.

# Mapping Layer vs 3NF Responsibility Split

## Purpose
Define the responsibility boundary between mapping and 3NF so identity, deduplication, and survivorship logic remain explainable, testable, and auditable.

## AI Copilot Usage Rules
When reviewing or generating mapping/3NF logic, the AI must verify:
- identity is decided before 3NF,
- `*_src_id` is defined in mapping,
- mapping is not over-resolving entities,
- 3NF applies survivorship only after identity is defined.

If these checks fail, the AI must emit `DECISION_REQUIRED` instead of silently proceeding.

## Core Rule
- Mapping is a transaction-grain standardized preservation layer.
- 3NF is the entity-resolution and relationship-truth layer.

## Mapping Layer Responsibilities
Mapping should:
- preserve cleaned source evidence,
- retain raw business keys for lineage,
- generate stable `*_src_id`,
- remove exact standardized row duplicates,
- avoid final survivorship,
- avoid aggressive entity consolidation.

## What Mapping Must Not Do
Mapping must not:
- choose final entity winners,
- enforce full business survivorship,
- behave like final dimensions,
- collapse meaningful source variation too early.

## Why Mapping Preserves Variation
The dominant source behavior is transaction-line data.
Keeping source variation visible in mapping preserves downstream explainability and auditability.

## SELECT DISTINCT vs WHERE NOT EXISTS
These controls solve different problems and are not interchangeable.

### SELECT DISTINCT
- Removes duplicates within the current standardized source result set.

### WHERE NOT EXISTS
- Prevents reinserting rows that already exist in the target table.

## Row Signature in `mapping_transactions`
`mapping_transactions` uses `row_sig` as a transaction-grain technical fingerprint.

Purpose:
- detect already-loaded standardized transaction rows,
- prevent row-level duplicate insertion,
- support incremental overlap handling.

Rule:
- `row_sig` is a technical fingerprint, not a business key.

## `*_src_id` Precomputation
### Preferred Option
Generate `*_src_id` in mapping after profiling.

Benefits:
- clear separation of concerns,
- reusable identity artifacts,
- stronger traceability,
- easier debugging,
- reduced repetition of key logic in 3NF.

### Alternative Option
Inline full attribute-based partition logic in 3NF.

Drawbacks:
- repeated logic,
- harder maintenance,
- weaker lineage visibility,
- higher inconsistency risk.

## 3NF Responsibilities
3NF should:
- resolve business entities,
- apply survivorship,
- generate surrogate keys,
- apply SCD behavior,
- enforce referential relationships,
- preserve lineage.

## `ROW_NUMBER()` in 3NF
Use `ROW_NUMBER()` for:
- winner selection per `*_src_id`,
- exact-version deduplication,
- survivorship logic.

Do not use `ROW_NUMBER()` to invent identity when profiling has not defined business-key semantics.

## Cross-Document Harmonization Notes
- `DECISION_REQUIRED`: Existing local rules reference “mapping/lineage” and “normalized integration” responsibilities, but do not currently formalize `row_sig` expectations by table pattern. Confirm whether `row_sig` guidance should remain limited to `mapping_transactions` or be generalized as a mapping-layer standard.
