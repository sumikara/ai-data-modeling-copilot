This file defines binding rules for the AI Copilot.

# Profiling Methodology and Grain Decision Rules

## Purpose
This document defines the profiling-led modeling sequence required before mapping, 3NF, and dimensional design decisions are finalized.

## AI Copilot Usage Rules
- Do not infer final grain from naming conventions alone (for example, `transaction_id`).
- Keep grain declaration separate from duplicate-removal mechanics.
- Explain when repeated IDs represent structural business behavior rather than data defects.
- Recommend line-level retail transaction grain unless evidence from current profiling artifacts contradicts it.
- Require explicit human approval before final grain sign-off.

## Core Sequence
The required sequence is:

```text
clean staging
→ profiling
→ business key decision
→ t_map *_src_id creation
→ 3NF ROW_NUMBER() survivorship
→ dimensional modeling
```

## Why This Order Matters
If identity definition is postponed to 3NF, then `ROW_NUMBER()` is forced to play two roles at once:
1. identity selection,
2. deduplication/survivorship selection.

That coupling weakens explainability and governance.

Preferred pattern:
- profiling determines candidate business key(s),
- mapping generates stable `*_src_id`,
- 3NF applies `ROW_NUMBER()` only for survivorship/winner selection under a pre-defined identity contract.

## General Profiling Logic
For each entity, compare these evidence checks:

1. raw row volume,
2. distinct count of candidate source key,
3. distinct count of descriptive-attribute combinations,
4. duplicate groups by source key,
5. duplicate groups ignoring source key,
6. cross-source conflicts,
7. temporal consistency,
8. candidate composite-key uniqueness.

Guiding questions:
- Is the raw source key trustworthy?
- Which attributes define business identity?
- Are repeated rows defects or valid business variation?
- Does the entity behave as event, profile, dimension, or fact?
- Should history be preserved?

## Transaction Grain Profiling
### Key Findings
- Total rows observed in profiling sample: **475,000 per source**.
- `transaction_id` distinct count is lower than total rows.
- `transaction_id` repetition is structural.
- Repetition is driven by multi-line purchases, not duplicate defects.
- A single transaction can include multiple products.
- Therefore, `transaction_id` alone does not express row-level grain.

### Validated Candidate Grain
`transaction_id + product_id + customer_id + transaction_dt`

### Conclusion
The source behaves as **transaction-line grain**.

Interpretation:
- one row represents one product-level line within a transaction/basket event.

## Critical Rule
Repeated `transaction_id` values are structural business behavior, not standalone duplicate evidence.

## Four-Step Dimensional Design Mapping

### Step 1: Select Business Process
Retail sales transaction / sales-line event.

### Step 2: Declare Grain
One row = one transaction line (product-level sales event).

### Step 3: Identify Dimensions
Likely dimensions:
- customer
- product
- promotion
- delivery
- date
- store
- employee
- engagement

### Step 4: Identify Facts
Candidate measures:
- quantity
- unit_price
- discount_applied
- total_sales
- gross_revenue
- net_revenue

## Cross-Document Harmonization Notes
- `DECISION_REQUIRED`: `knowledge_base/local_rules/retail_dataset_context_and_source_simulation.md` documents a 500,000-per-source split for simulation, while this guidance references profiling findings of 475,000 rows per source. Confirm whether 475,000 is a filtered profiling scope or whether source-count documentation must be reconciled.
