This file defines binding rules for the AI Copilot.

# Data Quality and Cross-Entity Profiling Framework

## Purpose
This document defines profiling checks used before and after modeling decisions.

## AI Copilot Usage Rules
AI should convert profiling findings into:
- modeling risks,
- key reliability assessment,
- source realism caveats,
- decision gates,
- README-ready evidence summaries.

When evidence is conflicting or incomplete, output `DECISION_REQUIRED` rather than silently resolving.

## DQ Dimensions
Recommended data quality dimensions:
- completeness,
- uniqueness,
- validity,
- consistency,
- accuracy/plausibility,
- timeliness/temporal logic.

## Source-Ingestion Sanity Checks
Validate ingestion readiness and landing integrity:
- external/foreign table exists,
- persistent source table exists,
- expected column order,
- source and landed row counts,
- representative sample rows,
- file options/configuration,
- external vs source reconciliation,
- blank critical-key detection.

## Completeness Checks
Check blank/null rates for:
- `transaction_id`,
- `customer_id`,
- `product_id`,
- `promotion_id`,
- `delivery_id`,
- `engagement_id`,
- store columns,
- employee columns.

## Date Format Quality
Check parse readiness for:
- `transaction_date`,
- `date_of_birth`,
- `membership_date`,
- `product_manufacture_date`,
- `product_expiry_date`,
- `employee_hire_date`,
- `promotion_start_date`,
- `promotion_end_date`.

## Numeric-Like Text Quality
Check cast readiness for:
- `quantity`,
- `unit_price`,
- `discount_applied`,
- `total_sales`,
- `employee_salary`,
- `app_usage`,
- `website_visits`,
- `social_media_engagement`,
- `customer_support_calls`.

## Distinct Value Inspection
Check case, spacing, and wording variation for:
- `gender`,
- `marital_status`,
- `payment_method`,
- `delivery_status`,
- `promotion_type`,
- `shipping_partner`,
- `product_category`.

## Cross-Entity Integrity Checks

### Location
- city maps to multiple states,
- zip maps to multiple city/state pairs,
- city/state maps to multiple zips,
- customer geography vs store geography overlap behavior.

### Employee / Store
- distinct employees per store,
- distinct stores per employee,
- positions per store,
- salary distribution by position,
- hire date greater than transaction date anomalies.

### Product
- `product_id` maps to multiple names/categories/materials,
- distinctness of category/name/brand/material combinations,
- manufacture date greater than expiry date anomalies,
- expired product sold checks.

### Customer
- one `customer_id` linked to multiple demographics/geographies,
- membership date greater than transaction date anomalies,
- `last_purchase_date` consistency,
- transaction-count-per-customer distribution.

### Delivery
- one `delivery_id` linked to multiple profiles,
- delivery status without shipping partner,
- delivery timestamp before transaction timestamp anomalies.

### Promotion
- transaction date within promotion start/end window,
- promotion channel vs source channel compatibility,
- promotion_id with zero discount scenarios,
- overlapping promotion windows.

## Cross-Document Harmonization Notes
- `DECISION_REQUIRED`: `last_purchase_date` and some timestamp fields referenced in profiling checks may not always be present in the finalized source-column sets. Confirm which optional fields are mandatory in the active ingestion contract before turning these checks into hard-fail validations.
