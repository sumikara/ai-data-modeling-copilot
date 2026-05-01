# Expected Semantic Behavior: case_01_transaction_line_clear

## Purpose
Validate that the assistant prefers line-level composite grain over `transaction_id` alone in a mostly clean transaction table.

## Expected JSON behavior
```json
{
  "business_process_guess": "retail sales transaction lines",
  "entity_type_guess": "fact-like transaction line entity",
  "grain_candidates": [
    "transaction_id",
    "transaction_id + product_id + transaction_dt",
    "transaction_id + product_id + customer_id + transaction_dt"
  ],
  "recommended_grain": "transaction_id + product_id + customer_id + transaction_dt",
  "dimension_candidates": ["customer", "product", "store", "date"],
  "fact_candidates": ["sales_transaction_line"],
  "measure_candidates": ["quantity", "unit_price", "total_sales"],
  "candidate_natural_keys": ["transaction_id + product_id + customer_id + transaction_dt"],
  "data_quality_risks": ["small null ratios in key columns", "near-perfect uniqueness still needs policy review"],
  "cross_source_conflicts": [],
  "modeling_notes": ["reject transaction_id-only grain", "line-grain appears strongest"],
  "confidence_level": "medium",
  "requires_human_decision": true
}
```

## Expected reasoning
- Grain reasoning rejects header-only key and favors composite line-level key.
- Key reasoning references uniqueness and null-blocking tradeoffs.
- Fact vs dimension reasoning uses additive measures + repeated transaction IDs.
- Relationship reasoning supports customer/product/store/date dimensions.
- Data quality impact remains visible despite generally clean data.
- Unresolved questions confirm approval for final grain publication.

## What would count as a failure
- Declaring `transaction_id` as final grain.
- `requires_human_decision=false`.
- High confidence without caveats.
- SQL/DDL generation.
