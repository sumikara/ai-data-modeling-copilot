This file defines binding rules for the AI Copilot.

# Layer Responsibilities

- Landing layer MUST:
  - ingest source data as-is,
  - apply controlled standardization,
  - enforce deterministic type/format normalization,
  - reduce obvious duplicate noise early.
- Mapping/lineage layer MUST:
  - preserve source triplet lineage (`source_id`, `source_system`, `source_table` style semantics),
  - prepare composite identifiers where natural keys are ambiguous,
  - register row signatures and load metadata for downstream controls.
- Normalized integration layer MUST:
  - resolve entities,
  - assign surrogate keys,
  - enforce referential and business constraints,
  - implement SCD behavior by entity rule.
- Dimensional layer MUST:
  - publish analytics-friendly dimensions and facts,
  - preserve declared fact grain,
  - keep reporting semantics stable for BI consumers.
- Observability/utilities MUST:
  - log orchestration steps,
  - capture row read/load outcomes,
  - preserve error diagnostics for operational audits.
