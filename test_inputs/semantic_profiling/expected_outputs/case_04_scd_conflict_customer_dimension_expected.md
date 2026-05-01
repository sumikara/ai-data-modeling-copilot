# Expected Semantic Behavior: case_04_scd_conflict_customer_dimension

## Purpose
Validate SCD awareness with explicit non-finalization of SCD type under cross-source customer conflicts.

## Expected JSON behavior
```json
{
  "business_process_guess": "customer profile conformance",
  "entity_type_guess": "dimension-like customer entity",
  "grain_candidates": [
    "customer_id",
    "customer_id + source_system"
  ],
  "recommended_grain": "uncertain (depends on conformance policy)",
  "dimension_candidates": ["customer"],
  "fact_candidates": [],
  "measure_candidates": [],
  "candidate_natural_keys": ["customer_id", "customer_id + source_system"],
  "data_quality_risks": ["duplicate customer_id across sources", "email unreliability", "descriptive conflicts"],
  "cross_source_conflicts": ["customer_segment", "loyalty_tier", "city/state"],
  "modeling_notes": ["SCD attributes detected", "Type 1 vs Type 2 requires business + temporal approval"],
  "confidence_level": "low",
  "requires_human_decision": true
}
```

## Expected reasoning
- Grain reasoning should remain policy-dependent.
- Key reasoning should compare conformed vs source-scoped identity.
- SCD notes must flag candidates but stop before final type selection.
- Unresolved questions should request business/temporal policy.

## What would count as a failure
- Finalizing SCD Type 1 or Type 2.
- High confidence despite active conflicts.
- `requires_human_decision=false`.
