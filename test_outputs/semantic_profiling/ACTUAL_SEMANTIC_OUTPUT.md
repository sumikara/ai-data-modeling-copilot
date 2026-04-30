# ACTUAL_SEMANTIC_OUTPUT

## Section 1: JSON Output

```json
{
  "business_process_guess": "transaction/event capture",
  "entity_type_guess": "fact-like transactional",
  "grain_candidates": [
    "one row per transaction_id",
    "one row per transaction_id + product_id + customer_id + transaction_dt"
  ],
  "recommended_grain": "one row per transaction_id + product_id + customer_id + transaction_dt",
  "dimension_candidates": [
    "customer",
    "product",
    "store",
    "date"
  ],
  "fact_candidates": [
    "txn_sales_line"
  ],
  "measure_candidates": [
    "quantity",
    "unit_price",
    "total_sales"
  ],
  "candidate_natural_keys": [
    "transaction_id + product_id + customer_id + transaction_dt"
  ],
  "data_quality_risks": [
    "review null ratios for key columns",
    "review parse-success gaps for numeric/date fields"
  ],
  "cross_source_conflicts": [
    "review domain_pattern_findings.cross_source_entity_conflicts for survivorship/SCD implications"
  ],
  "modeling_notes": [
    "grain_notes: mock output; replace with model-generated scored grain evidence.",
    "key_notes: mock output; evaluate uniqueness/null sensitivity/stability before acceptance.",
    "dimension_notes: mock output inferred from relationship-style columns.",
    "relationship_notes: 4 candidate relationship(s) provided.",
    "quality_notes: confirm parse/null/duplication risks from profile metrics.",
    "scd_notes: if cross-source conflicts exist, mark attributes as SCD candidates for human review.",
    "unresolved_questions: requires human decision before model finalization."
  ],
  "confidence_level": "medium",
  "requires_human_decision": true
}
```

## Section 2: Reasoning Sections

### grain reasoning
- See `modeling_notes` entries prefixed with `grain_notes`.

### key reasoning
- See `modeling_notes` entries prefixed with `key_notes`.

### dimension vs fact reasoning
- See `modeling_notes` entries prefixed with `dimension_notes`.

### relationship reasoning
- See `modeling_notes` entries prefixed with `relationship_notes`.

### data quality impact
- See `modeling_notes` entries prefixed with `quality_notes` and `scd_notes`.
