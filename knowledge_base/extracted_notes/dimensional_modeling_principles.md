# DIMENSIONAL MODELING — CORE PRINCIPLES

> **AI Copilot Usage Note:** Use this document to constrain fact/dimension recommendations, grain declaration, and star-schema reasoning. Do not finalize model design without evidence.

---

## 1. Dimensional Modeling Overview

Dimensional modeling structures warehouse data for analytical performance and interpretability.

It separates data into:
- **Facts** → measurable business events
- **Dimensions** → descriptive context

Primary optimization goals:
- fast BI queries
- reliable aggregation
- intuitive filtering/grouping

---

## 2. Fact Tables

A fact table stores quantitative metrics for a defined business process event stream.

### Key Properties
- Contains numeric/semi-numeric measurements
- Represents one declared business process scope
- Requires explicit grain before column design
- Usually largest table family in the model

---

## 3. Fact Table Rules

- Each row MUST represent one event instance at declared grain.
- Grain MUST be uniform across all rows.
- Fact metrics should be classified before use:
  - additive (preferred)
  - semi-additive (time-aware treatment)
  - non-additive (special handling)

```text
Rule check:
[ ] one process
[ ] one grain
[ ] metric additivity tagged
```

---

## 4. Types of Facts

### Additive Facts
- Summable across all dimensions.
- Typical examples: revenue, quantity.

### Semi-Additive Facts
- Summable across some dimensions, not all (commonly not across time).
- Typical example: balance snapshots.

### Non-Additive Facts
- Not directly summable.
- Typical examples: ratios, percentages, rates.

---

## 5. Dimension Tables

Dimensions provide descriptive context for fact analysis.

### Properties
- Store descriptive attributes
- Generally smaller than fact tables
- Enable filtering, grouping, labeling, drill-down

---

## 6. Dimension Structure

Each dimension should include:
- **Surrogate Key** (warehouse primary key)
- **Natural Key** (source business identifier)
- **Descriptive Attributes** (analysis context)

---

## 7. Surrogate vs Natural Key

### Surrogate Key
- System-generated and warehouse-controlled
- Join key for facts
- Stable across source-system volatility

### Natural Key
- Comes from source system
- Required for mapping, lineage, conformance
- May drift/change over time

```text
Copilot rule:
Use surrogate keys for star joins.
Preserve natural keys for traceability and reconciliation.
```

---

## 8. Star Schema

Star schema pattern:
- one central fact table
- multiple denormalized surrounding dimensions

Advantages:
- simpler query patterns
- faster aggregate query paths
- high analyst usability

---

## 9. Snowflake Schema

Snowflake schema normalizes one or more dimensions.

Characteristics:
- reduced attribute redundancy
- more joins
- higher query/model complexity

Use when governance/reuse needs outweigh query simplicity.

---

## 10. Fact-Dimension Relationship

Fact tables reference dimensions via foreign keys.

```text
fact_sales
- customer_key -> dim_customer
- product_key  -> dim_product
- date_key     -> dim_date
```

Relationship quality must be validated (coverage, unknown/default routing, conformance).

---

## 11. Grain Definition (Critical)

Grain defines exactly what one row means.

Examples:
- one row per transaction
- one row per product per day
- one row per customer per month

No downstream modeling decision is valid without explicit grain.

---

## 12. Grain Rules

Grain must be:
- declared before selecting facts/dimensions
- explicit (human-readable statement)
- consistent (single row meaning)
- aligned with business process semantics

---

## 13. Grain Violations

Invalid patterns:
- multiple grains in one fact table
- ambiguous row meaning
- mixed raw and pre-aggregated metrics in same grain context

If detected, split or re-model before publication.

---

## 14. Four-Step Design Process

1. Select business process
2. Declare grain
3. Identify dimensions
4. Identify facts

```text
Do not reorder this sequence in Copilot recommendations.
```

---

## 15. Business Process Selection

Business process selection determines event scope and analytic intent.

Defines:
- what event is modeled
- what outcomes/metrics matter

Typical process classes:
- transactions
- inventory movement
- customer interactions

---

## 16. Dimension Identification

Dimensions answer context questions:
- who?
- what?
- where?
- when?

Typical entities:
- customer
- product
- location
- date

Copilot should prioritize reusable/conformed context candidates.

---

## 17. Fact Identification

Facts answer magnitude questions:
- how much?
- how many?

Typical examples:
- quantity
- revenue
- discount amount

Facts must be mapped to additivity class and grain compatibility.

---

## 18. Degenerate Dimensions

A degenerate dimension is a business identifier kept in fact without a separate dimension table.

Typical example:
- transaction/invoice/order number

Use when identifier is analytically useful but has no stable descriptive attribute set.

---

## 19. Conformed Dimensions

Conformed dimensions are reused across multiple facts/processes with consistent semantics.

Typical example:
- shared date dimension across sales, inventory, shipments

Conformance enables cross-process comparability and unified reporting.

---

## 20. Design Constraints

- No uncontrolled NULL foreign keys in facts; use approved default/unknown member policy.
- Every fact row should resolve to dimension context (or explicit default member).
- Grain consistency is mandatory.
- Dimension attributes should be stable under declared SCD policy.

```text
Final Copilot gate:
[ ] process selected
[ ] grain declared and tested
[ ] dimensions identified and conformed where needed
[ ] facts classified and grain-compatible
[ ] FK/default policy enforced
```
