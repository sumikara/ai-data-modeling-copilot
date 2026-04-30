# Source Triplet and Lineage Rules

## Rule
Source lineage MUST preserve source identifier, source system, and source object context for every integrated entity.

## When to use
- During multi-source integration.
- During natural key ambiguity handling.
- During reconciliation and conflict diagnostics.

## Evidence required
- Source-triplet fields in staging/integration artifacts.
- Mapping trace from source rows to target entities.
- Batch/file metadata and load timestamps.

## Copilot must NOT do
- Must NOT join cross-source entities by ID alone when IDs are non-global.
- Must NOT drop original business identifiers after deriving surrogate/composite keys.
- Must NOT recommend irreversible lineage loss.

## Human approval required
- Any lineage compression that reduces traceability.
- Exceptions to triplet preservation for privacy/security constraints.
