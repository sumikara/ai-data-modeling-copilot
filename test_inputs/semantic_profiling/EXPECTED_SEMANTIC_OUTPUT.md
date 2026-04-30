# Expected Semantic Output (Behavior Contract)

This document defines how `semantic-profiling-skill` is expected to interpret:

- `test_inputs/semantic_profiling/transaction_like_profile.json`

> This is a human-readable expected behavior contract, not an automated assertion yet.

---

## Expected structured output

```json
{
  "business_process_guess": "retail sales transaction capture",
  "entity_type_guess": "fact-like transactional line dataset",
  "grain_candidates": [
    "one row per transaction_id",
    "one row per transaction_id + product_id + transaction_dt",
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
    "sales_transaction_line"
  ],
  "measure_candidates": [
    "quantity",
    "unit_price",
    "total_sales"
  ],
  "candidate_natural_keys": [
    "transaction_id + product_id + customer_id + transaction_dt",
    "transaction_id + product_id + transaction_dt (fallback when customer_id missing)"
  ],
  "data_quality_risks": [
    "customer_id null ratio 1.2% weakens strict key and customer conformance",
    "transaction_dt null ratio 0.2% weakens composite grain reliability",
    "unit_price numeric parse success 99.4% indicates formatting quality issues",
    "total_sales numeric parse success 99.1% indicates casting risk",
    "cross-source customer_segment conflict rate 3.7% may affect dimensional consistency",
    "product_desc duplicate descriptor rate 2.8% may indicate descriptor synonym issues"
  ],
  "cross_source_conflicts": [
    "customer_id conflicts between POS and WEB in customer_segment"
  ],
  "modeling_notes": [
    "grain reasoning: transaction_id uniqueness is 0.40, so transaction header grain is not valid for line-level facts.",
    "grain reasoning: composite (transaction_id, product_id, customer_id, transaction_dt) reaches 0.9992 uniqueness and best represents line behavior.",
    "key reasoning: customer_id and transaction_dt null blocking (1.4% combined impact) means the recommended key is strong but not absolute.",
    "dimension vs fact reasoning: repeated transaction_id plus additive-like measures (quantity, unit_price, total_sales) indicate a fact-like transaction line entity.",
    "relationship reasoning: high overlap to product/store/date dimensions (>=0.978) supports many-to-one dimensional joins; customer overlap 0.944 is usable but lower confidence.",
    "data quality impact: parse errors and cross-source segment conflicts should be remediated or explicitly tolerated before enforcing strict FK/quality gates."
  ],
  "confidence_level": "medium",
  "requires_human_decision": true
}
```

---

## Why this output is expected (evidence mapping)

### 1) business_process_guess
- `transaction_id` is highly repeated and measures exist (`quantity`, `unit_price`, `total_sales`), indicating a sales event stream at line-level granularity.

### 2) entity_type_guess
- Strong event/fact-like behavior:
  - non-unique `transaction_id` (multi-line baskets),
  - additive-like numeric fields,
  - multiple foreign-key-like relationships.

### 3) grain_candidates + recommended_grain
- Reject `transaction_id` alone due to uniqueness ratio `0.40`.
- Prefer the 4-column composite due to uniqueness `0.9992`, with caveat on null blocking.

### 4) dimension_candidates
- Relationship candidates strongly point to `dim_product`, `dim_customer`, `dim_store`, and `dim_date`.

### 5) fact_candidates + measure_candidates
- Line-level sales fact is supported by repeated transactions and transactional measures.

### 6) candidate_natural_keys
- Composite key is best supported.
- Fallback variant without `customer_id` is plausible but weaker due to reduced uniqueness.

### 7) data_quality_risks + cross_source_conflicts
- Missing IDs/dates, parse readiness gaps, descriptor duplication, and cross-source conflicts all directly impact modeling confidence.

### 8) confidence_level
- `medium` is appropriate: evidence is strong for line grain but non-trivial data quality and conflict caveats remain.

### 9) requires_human_decision
- Must remain `true` by design governance: skill proposes, human approves final modeling decisions.
