This file defines binding rules for the AI Copilot.

# Deduplication Rules

- Deduplication MUST be treated as a pipeline-wide strategy, not a single query step.
- Duplicate controls MUST be applied at multiple checkpoints:
  - post-ingestion standardization,
  - mapping/integration filters,
  - target insert guards.
- Incremental-safe insertion MUST use deterministic SQL patterns such as:
  - `WHERE NOT EXISTS`
  - anti-join patterns (`LEFT JOIN ... IS NULL`)
  - `ON CONFLICT DO NOTHING` where unique constraints exist
- Content-based row signatures MUST be used for transaction-grain duplicate protection.
- MD5 row signature logic MUST remain part of the deduplication contract.
- Re-running with unchanged source inputs SHOULD produce zero net new rows for incremental paths.
- Deduplication design MUST preserve business events and avoid destructive record loss.
