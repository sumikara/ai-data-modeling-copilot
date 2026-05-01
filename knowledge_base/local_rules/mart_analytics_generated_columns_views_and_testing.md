This file defines binding rules for the AI Copilot.

# Mart, Analytics, Generated Columns, Views, and Testing

## Purpose
Define analytical enhancements planned for the DM/mart layer.

## AI Copilot Usage Rules
AI should:
- distinguish DE pipeline work from analytics/mart work,
- recommend generated columns only for immutable expressions,
- recommend views/materialized views for dynamic logic,
- propose KPI and materialized-view candidates only after fact grain is approved.

## Mart Layer Role
DM/mart supports:
- reporting,
- BI tools,
- KPI calculation,
- aggregate facts,
- analytical views,
- materialized views.

Rule:
- Core business logic should reside in SQL warehouse layers, not Power BI transformations.

## Generated Columns

### `dim_dates`
Candidate generated columns:
- `fiscal_quarter`,
- `season`,
- `yyyymm_label`.

Constraint:
- Generated columns must use immutable expressions.
- Runtime functions such as `CURRENT_DATE` are invalid for STORED generated columns.

### `fct_transactions`
Candidate generated columns:
- `gross_revenue = unit_price * quantity`,
- `net_revenue = unit_price * quantity * (1 - discount_applied / 100)`.

## Views Instead of Generated Columns
Use views/materialized views for:
- `customer_tenure_days`,
- `age_band`,
- dynamic current-date logic,
- rolling analytics.

## Analytical Views (Recommended)
- `dim.v_monthly_sales_summary`
- `dim.v_customer_360`
- `dim.v_product_performance`
- `dim.v_store_sales_summary`
- `dim.v_delivery_performance`
- `dim.v_promotion_effectiveness`

## Materialized Views (Recommended)
- monthly sales summary,
- product/store/month sales,
- customer segment performance,
- promotion channel performance.

## Window Functions
Use for:
- product revenue ranking,
- customer purchase frequency,
- store performance ranking,
- running monthly revenue,
- moving averages,
- top-N products per category,
- customer recency/frequency metrics.

## Testing Framework

### Idempotency
Second run should produce:
- `0 inserted`,
- `0 updated`,
unless a full reload is intentionally executed.

### Reconciliation
Check:
- source row counts,
- mapping row counts,
- NF transaction row counts,
- fact row counts.

### Referential Integrity
Check:
- unresolved FK counts,
- default-row usage,
- orphan facts,
- channel-specific FK population.

### Example Channel Checks
- online rows should not have `store_id`/`employee_id`,
- offline rows should not have `engagement_id`,
- online rows can have `city_id` through customer geography,
- employee-store realism limitations should be documented separately.

## Cross-Document Harmonization Notes
- `DECISION_REQUIRED`: Existing architecture rules describe dimensional objects under `dimensional/mart` terminology, while view examples here use `dim.` schema naming. Confirm canonical schema placement for analytical views/materialized views (`dim`, `mart`, or both).
