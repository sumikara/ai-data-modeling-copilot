# Methodology Summary (External Concepts)

## ELT vs ETL
- ELT: data is loaded first, then transformed inside the target engine.
- ETL: transformation occurs before loading into target storage.

## Inmon vs Kimball
- Inmon/CIF: integrated normalized enterprise model first.
- Kimball: dimensional/star structures for analytics consumption.
- Hybrid approach: maintain both normalized integration and dimensional publishing layers.

## SCD Types
- Type 0: fixed attributes, no post-load change.
- Type 1: overwrite current value, no history.
- Type 2: preserve history via versioned rows and validity windows.

## Data Quality Dimensions
- Completeness: required values are present.
- Uniqueness: no unintended duplicates at declared grain.
- Validity: values conform to format/range/type expectations.
- Consistency: values align across systems and transformations.
- Accuracy: values represent intended business reality.
- Timeliness: data is delivered within expected latency windows.

## Join Strategy Concepts
- Left joins preserve driving rows and reduce silent data loss in integration contexts.
- Semi-join style existence checks filter by match presence without row multiplication.
- Anti-join style exclusion finds records missing from the target for incremental-safe loading.

## Idempotent Load Concepts
- Rerunnable pipelines rely on deterministic exclusion and conflict-safe insertion patterns.
- Snapshot and incremental modes require explicit, auditable load semantics.
