This file defines binding rules for the AI Copilot.

# Lineage Rules

- Full source triplet lineage MUST be preserved for integrated entities:
  - source identifier
  - source system
  - source table/origin
- Joining across multi-source entities MUST NOT rely on raw IDs alone when source overlap exists.
- Derived identifiers/composites MAY be used for uniqueness, but original business keys MUST remain available for traceability.
- Mapping tables SHOULD precompute reusable key combinations for lower-cost downstream joins.
- Lineage metadata MUST survive transitions from landing to normalized to dimensional models.
- Load metadata fields (batch IDs, timestamps, file references, row numbers where available) SHOULD remain queryable for diagnostics.
