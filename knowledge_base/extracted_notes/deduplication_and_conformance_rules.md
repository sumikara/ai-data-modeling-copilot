# Deduplication and Conformance Rules

## Rule
Deduplication and conformance MUST be deterministic, multi-layered, and traceable.

## When to use
- During landing standardization.
- During mapping/integration loads.
- During incremental-safe inserts and reconciliation.

## Evidence required
- Row signature logic (including MD5 fingerprint strategy).
- Duplicate rate before/after each layer.
- Anti-join/exists checks proving idempotent behavior.
- Conformance exceptions across sources.

## Copilot must NOT do
- Must NOT rely on one-time DISTINCT-only cleanup.
- Must NOT remove near-duplicate rows without business/grain context.
- Must NOT recommend conformance merges without conflict visibility.

## Human approval required
- Conflict resolution for cross-source semantic mismatches.
- Dedup thresholds that may alter business event counts.
