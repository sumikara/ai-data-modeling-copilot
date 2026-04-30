# ACTUAL_SEMANTIC_OUTPUT

## Section 1: JSON Output

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
    "customer_id null ratio 1.2% reduces strict customer conformance and weakens fully strict composite key enforcement",
    "transaction_dt null ratio 0.2% introduces residual key incompleteness risk",
    "unit_price numeric parse success 99.4% indicates format normalization issues (e.g., comma decimal)",
    "total_sales numeric parse success 99.1% indicates measure-casting risk in a small but non-zero row set",
    "cross-source customer_segment conflict rate 3.7% may affect dimension conformance behavior",
    "product descriptor duplicate rate 2.8% suggests synonym/alias risk in product identity"
  ],
  "cross_source_conflicts": [
    "customer_id overlaps across POS and WEB show customer_segment conflicts"
  ],
  "modeling_notes": [
    "grain reasoning: transaction_id uniqueness is 0.40 with duplicate ratio 0.60, so transaction header-level grain is not supported for line-fact behavior.",
    "grain reasoning: composite (transaction_id, product_id, customer_id, transaction_dt) has 0.9992 uniqueness and is the strongest observed candidate despite null blocking.",
    "key reasoning: composite key is near-unique but not absolute because customer_id and transaction_dt have non-zero null ratios; strict key enforcement needs a null-handling policy.",
    "dimension vs fact reasoning: repeated transaction signatures plus measure-like columns (quantity, unit_price, total_sales) indicate event/fact-like behavior.",
    "relationship reasoning: high overlap to dim_product (0.982), dim_store (0.978), and dim_date (0.991) supports many-to-one dimensional joins; dim_customer overlap (0.944) is usable but lower confidence.",
    "data quality impact: parse errors, null blocking, and cross-source segment conflicts reduce confidence from high to medium and require human policy decisions before hard validation gates."
  ],
  "confidence_level": "medium",
  "requires_human_decision": true
}
```

## Section 2: Reasoning Sections

### grain reasoning
- `transaction_id` alone is not grain-safe (`unique_ratio=0.40`, duplicate-heavy behavior).
- The best candidate is `(transaction_id, product_id, customer_id, transaction_dt)` with `uniqueness_ratio=0.9992`.
- Residual uncertainty remains because `customer_id` and `transaction_dt` are null-blocking columns in part of the data.

### key reasoning
- No single-column primary key candidate is present.
- Composite key evidence is strong but not perfect due to null-blocking ratio (`0.014`).
- A fallback natural key without `customer_id` exists but is weaker (`uniqueness_ratio=0.971`).

### dimension vs fact reasoning
- The table behaves like a transaction line fact:
  - repeated transaction identifiers,
  - many-to-one links to product/customer/store/date entities,
  - measure-like numeric fields (`quantity`, `unit_price`, `total_sales`).
- Dimension candidates are inferred from relationship evidence, not from naming alone.

### relationship reasoning
- Relationship candidates support a star-like interpretation with strong overlaps:
  - `product_id -> dim_product.product_id` (`0.982`, high confidence)
  - `store_id -> dim_store.store_id` (`0.978`, high confidence)
  - `transaction_dt -> dim_date.calendar_dt` (`0.991`, high confidence)
  - `customer_id -> dim_customer.customer_id` (`0.944`, medium confidence)
- Customer relationship is directionally valid but more vulnerable to completeness/conflict issues.

### data quality impact
- `customer_id` nulls (`1.2%`) create customer conformance and key integrity edge cases.
- Numeric parse readiness is high but not perfect (`unit_price=0.994`, `total_sales=0.991`), so cleansing policy is still needed.
- Cross-source `customer_segment` conflicts (`3.7%`) create semantic consistency risk for customer dimension attributes.
- Product descriptor duplicate signal (`2.8%`) suggests identity harmonization needs.

## Section 3: Self-check

Compared reference:
- `test_inputs/semantic_profiling/EXPECTED_SEMANTIC_OUTPUT.md`

### where output matches
- Same required schema and all expected top-level fields are present.
- Same core interpretation:
  - business process = retail sales transaction capture,
  - entity type = fact-like transactional line dataset,
  - recommended grain = 4-column composite,
  - dimension candidates = customer/product/store/date,
  - measures = quantity/unit_price/total_sales,
  - confidence = medium,
  - `requires_human_decision = true`.
- Reasoning sections are all included and evidence-based.

### where it differs
- Wording differences in risk statements and cross-source conflict phrasing.
- Modeling notes are semantically equivalent but not verbatim identical.
- This run explicitly mentions null-handling policy and strict gate implications with slightly stronger governance language.

### what is weaker
- Does not explicitly restate `currency_cd` distribution impact (USD/EUR skew), which could matter for downstream conformance checks.
- Does not quantify exact row counts impacted by parse failures; only ratio-based risk is cited.

### what is missing
- No additional missing required fields.
- Optional enhancement missing: a short unresolved-questions bullet list for human reviewers (e.g., guest checkout policy for null customer IDs).

### confidence gap
- Expected output confidence: `medium`.
- Actual output confidence: `medium`.
- Gap: none on label; minor narrative difference only (actual output emphasizes governance caveats slightly more).
