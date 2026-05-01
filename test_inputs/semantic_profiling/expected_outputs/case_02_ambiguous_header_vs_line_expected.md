# Expected Semantic Behavior: case_02_ambiguous_header_vs_line

## Purpose
Test whether the assistant preserves ambiguity for mixed header/line signals.

## Expected JSON behavior
```json
{
  "business_process_guess": "order capture with mixed granularity",
  "entity_type_guess": "hybrid/unclear",
  "grain_candidates": [
    "order_id",
    "order_id + product_id",
    "order_id + line_number"
  ],
  "recommended_grain": "uncertain",
  "dimension_candidates": ["customer", "product", "date"],
  "fact_candidates": ["order_line_candidate"],
  "measure_candidates": ["quantity", "unit_price", "line_total"],
  "candidate_natural_keys": ["order_id + line_number (null-sensitive)"],
  "data_quality_risks": ["mixed grain signals", "repeated total_order_amount", "line_number null ratio"],
  "cross_source_conflicts": [],
  "modeling_notes": ["split into order_header and order_line may be required"],
  "confidence_level": "low",
  "requires_human_decision": true
}
```

## Expected reasoning
- Grain reasoning must keep alternatives open.
- Key reasoning highlights null-sensitive line-number candidate.
- Fact vs dimension reasoning explains collision of header and line fields.
- Data quality impact calls out repeated order-level measures in line context.
- Unresolved questions ask whether to split table.

## What would count as a failure
- High-confidence `order_id` (or `order_id + product_id`) finalization.
- No unresolved questions.
- `requires_human_decision=false`.
