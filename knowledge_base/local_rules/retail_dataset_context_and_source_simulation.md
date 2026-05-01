This file defines binding rules for the AI Copilot.

# Retail Dataset Context and Source Simulation

## Purpose
This document defines dataset context, simulation constraints, and source-shaping assumptions for the Retail DWH reference project. The AI Copilot must use this as project-local guidance when generating models, ETL logic, and explanations.

## AI Copilot Usage Rules
- Always identify this dataset as synthetic/simulated, not operational production truth.
- Treat online and offline feeds as simulated source systems created for architecture exercises.
- Preserve explicit caveats when explaining anomalies (for example, unrealistic relationships).
- Do not classify source-generation artifacts as ETL defects without evidence.

## Dataset Source
- Base dataset origin: Kaggle, **Large Retail Data Set for EDA**.
- The source includes retail-oriented fields spanning customer, transactions, product, promotion, geography, behavior, and sales context.

## Dataset Nature
- Dataset classification: **synthetic / simulated**.
- It does not represent a real retail operational system.
- Certain columns and value combinations may behave unrealistically because the dataset was generated for analysis practice rather than production-grade DWH fidelity.

## Original Dataset Domains

### Customer Information
- `customer_id`
- `age`
- `gender`
- `income_bracket`
- `loyalty_program`
- `membership_years`
- `churned`
- `marital_status`
- `number_of_children`
- `education_level`
- `occupation`

### Transactional Data
- `transaction_id`
- `transaction_date`
- `product_id`
- `product_category`
- `quantity`
- `unit_price`
- `discount_applied`
- `payment_method`
- `store_location`

### Product Information
- `product_name`
- `product_brand`
- `product_stock`
- `product_material`
- `product_manufacture_date`
- `product_expiry_date`

### Promotion Information
- `promotion_id`
- `promotion_type`
- `promotion_start_date`
- `promotion_end_date`
- `promotion_channel`

### Geography
- `customer_zip_code`
- `customer_city`
- `customer_state`
- `store_zip_code`
- `store_city`
- `store_state`

### Customer Interaction
- `customer_support_calls`
- `app_usage`
- `website_visits`
- `social_media_engagement`

## Project-Specific Dataset Transformation
The 1,000,000-row dataset was split to simulate two source systems.

| Source | Rows | Meaning |
|---|---:|---|
| Online retail | 500,000 | Simulated online channel |
| Offline retail | 500,000 | Simulated offline/store channel |

Each source was then split by load mode:
- 95% bulk load
- 5% incremental load simulation

Transformation goals:
- demonstrate initial historical bulk loading,
- simulate later-arriving incremental data,
- support SCD, reload, and idempotency validation scenarios.

## Added Synthetic Entity Columns

### Common / Shared Additions
- `delivery_id`
- `delivery_type`
- `delivery_status`
- `shipping_partner`

### Offline-Only Additions
- `store_zip_code`
- `store_city`
- `store_state`
- `store_location`
- `employee_name`
- `employee_position`
- `employee_salary`
- `employee_hire_date`

### Online-Only Additions
- `engagement_id`
- `website_address`
- `order_channel`
- `customer_support_method`
- `issue_status`
- `app_usage`
- `website_visits`
- `social_media_engagement`

## Final Online Source Columns
```text
customer_id
age
gender
income_bracket
loyalty_program
membership_years
churned
marital_status
number_of_children
education_level
occupation
transaction_id
transaction_date
product_id
product_category
quantity
unit_price
discount_applied
payment_method
promotion_id
promotion_type
promotion_start_date
promotion_end_date
promotion_channel
customer_zip_code
customer_city
customer_state
customer_support_calls
product_name
product_brand
product_stock
product_material
product_manufacture_date
product_expiry_date
delivery_id
delivery_type
delivery_status
shipping_partner
engagement_id
website_address
order_channel
customer_support_method
issue_status
app_usage
website_visits
social_media_engagement
```

## Final Offline Source Columns
```text
customer_id
age
gender
income_bracket
loyalty_program
membership_years
churned
marital_status
number_of_children
education_level
occupation
transaction_id
transaction_date
product_id
product_category
quantity
unit_price
discount_applied
payment_method
promotion_id
promotion_type
promotion_start_date
promotion_end_date
promotion_channel
customer_zip_code
customer_city
customer_state
customer_support_calls
product_name
product_brand
product_stock
product_material
product_manufacture_date
product_expiry_date
delivery_id
delivery_type
delivery_status
shipping_partner
store_zip_code
store_city
store_state
store_location
employee_name
employee_position
employee_salary
employee_hire_date
```

## Modeling Rationale
Precomputed analytics and derived columns from the raw synthetic source were intentionally excluded when they were not operational signals.

Reasons:
- derived metrics should be recalculated in mart/reporting layers,
- the DWH project should demonstrate transformation, aggregation, and reporting logic,
- raw-vs-analytics responsibilities remain clearly separated.

## Cross-Document Harmonization Notes
- `DECISION_REQUIRED`: This document formalizes a strict synthetic-data caveat as a local rule. Confirm whether this should remain project-specific (`local_rules`) only, or also be mirrored in worked example narrative guidance.
