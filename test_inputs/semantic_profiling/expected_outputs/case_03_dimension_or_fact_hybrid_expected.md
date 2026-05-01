# Expected Semantic Behavior: case_03_dimension_or_fact_hybrid

## Purpose
Test whether the assistant identifies periodic snapshot fact behavior with embedded descriptors.

## Expected JSON behavior
```json
{
  "business_process_guess": "inventory snapshot tracking",
  "entity_type_guess": "periodic snapshot fact-like table with embedded dimension descriptors",
  "grain_candidates": [
    "product_id",
    "product_id + warehouse_id + snapshot_date"
  ],
  "recommended_grain": "product_id + warehouse_id + snapshot_date",
  "dimension_candidates": ["product", "warehouse", "date"],
  "fact_candidates": ["inventory_snapshot_fact"],
  "measure_candidates": ["stock_on_hand", "reorder_level", "inventory_value"],
  "candidate_natural_keys": ["product_id + warehouse_id + snapshot_date"],
  "data_quality_risks": ["embedded product descriptors may drift", "possible product SCD implications"],
  "cross_source_conflicts": [],
  "modeling_notes": ["do not collapse into pure product dimension"],
  "confidence_level": "medium",
  "requires_human_decision": true
}
```

## Expected reasoning
- Grain reasoning uses repeated product across dates.
- Key reasoning favors 3-column snapshot key.
- Fact vs dimension reasoning separates descriptors from snapshot measures.
- SCD notes flag descriptor drift for policy follow-up.

## What would count as a failure
- Classifying as only a product dimension.
- Ignoring descriptor drift risk.
- `requires_human_decision=false`.
