This file defines binding rules for the AI Copilot.

# SCD Rules

- SCD behavior MUST be defined per entity, not globally.
- Type 0 entities:
  - immutable once loaded,
  - no overwrite/versioning.
- Type 1 entities:
  - overwrite in-place,
  - no historical version retention.
- Type 2 entities:
  - expire previous active row,
  - insert new version with start/end dating,
  - maintain active-flag semantics.
- SCD operations MUST be idempotent and safe for repeated incremental execution.
- SCD logic MUST follow business meaning, not generic merge shortcuts.
- Type 2 versioning MUST preserve historical truth and auditable change timelines.
