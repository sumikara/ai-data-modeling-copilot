This file defines binding rules for the AI Copilot.

# Data Quality Rules

- Data quality controls MUST cover at least:
  - completeness
  - uniqueness
  - validity
  - consistency
  - accuracy
  - timeliness
- Deterministic NULL/default handling MUST be explicit and layer-aware.
- Referential integrity MUST be preserved with controlled default/sentinel rows when dimensions cannot be resolved.
- Integration paths SHOULD prefer row-preserving joins where business event retention is required.
- Semi-join/anti-join logic MUST be used intentionally for existence checks and incremental exclusion.
- Typing discipline MUST be enforced in integrated/reporting layers (`DATE`, numeric, key types, boolean where applicable).
- Quality rule outcomes SHOULD be logged for traceable remediation.
