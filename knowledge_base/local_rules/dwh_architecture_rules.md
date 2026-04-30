This file defines binding rules for the AI Copilot.

# DWH Architecture Rules

- The warehouse MUST follow layered ELT separation:
  - ingestion/landing
  - semantic alignment/lineage mapping
  - integrated normalized model
  - dimensional publishing model
- Each layer MUST have one primary responsibility; business logic leakage across layers is prohibited.
- Transformation logic MUST run inside the database engine for auditable, rerunnable behavior.
- The integration layer MUST preserve source lineage fields through downstream models.
- The dimensional layer MUST consume integrated entities, not raw ingestion tables.
- Pipeline code MUST be idempotent and rerunnable without manual cleanup.
- Architecture MUST support both bulk snapshot loads and incremental-safe loads.
- Design MUST prioritize correctness and traceability over convenience shortcuts.
- Operational metadata (batch/step/log/file-level traces) MUST be first-class architecture artifacts.
