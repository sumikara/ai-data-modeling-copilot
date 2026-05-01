# Public Dataset References (Research Checklist)

This document is a curated checklist of **potential** public datasets to evaluate for future benchmark expansion.

> **Status note:** The datasets listed below are placeholders for research and evaluation planning. They have **not** been downloaded or added to this repository.

## Retail

- **Dataset/source name placeholder:** UCI Online Retail II / Kaggle retail transactions (placeholder)
- **What modeling problem it can test:** Basket-level sales modeling, store/product performance, seasonal demand, customer repeat behavior
- **Likely fact candidates:** `sales_line_items`, `transactions`, `returns`
- **Likely dimension candidates:** `date`, `store`, `product`, `customer`, `promotion`, `channel`
- **Likely grain ambiguity:** Line-item vs receipt-level transactions; daily snapshot vs event-level changes
- **Data quality risks:** Missing product taxonomy, canceled invoices, inconsistent customer IDs, timezone/date inconsistencies
- **Licensing/check-before-use note:** Verify commercial/research use permissions and redistribution rights; confirm any downstream source restrictions

## E-commerce

- **Dataset/source name placeholder:** Olist Brazilian E-commerce / Instacart market basket (placeholder)
- **What modeling problem it can test:** Order lifecycle analytics, fulfillment and delivery performance, cohort retention, cross-category purchasing
- **Likely fact candidates:** `orders`, `order_items`, `payments`, `shipments`, `reviews`
- **Likely dimension candidates:** `customer`, `seller`, `product`, `date`, `geography`, `order_status`
- **Likely grain ambiguity:** Order header vs item-level grain; one payment per order vs multiple payment records
- **Data quality risks:** Late-arriving shipment updates, duplicated order statuses, sparse review coverage, incomplete geo normalization
- **Licensing/check-before-use note:** Confirm if mirrored copies preserve original terms; validate whether redistribution in derived benchmark assets is allowed

## Healthcare

- **Dataset/source name placeholder:** MIMIC-IV derived public subsets / synthetic EHR benchmark sets (placeholder)
- **What modeling problem it can test:** Encounter utilization, diagnosis/procedure patterns, readmission proxy analyses, length-of-stay modeling
- **Likely fact candidates:** `encounters`, `diagnoses`, `procedures`, `medication_administrations`, `lab_results`
- **Likely dimension candidates:** `patient`, `provider`, `facility`, `diagnosis_code`, `procedure_code`, `date`
- **Likely grain ambiguity:** Encounter-level vs diagnosis-event grain; patient timeline vs visit snapshots
- **Data quality risks:** De-identification shifts (date offsets), code-system changes (ICD versions), missing outpatient context, censoring bias
- **Licensing/check-before-use note:** Verify data use agreements, credentialing/training prerequisites, and PHI-safe redistribution limits even for de-identified data

## Logistics

- **Dataset/source name placeholder:** NYC TLC trip records / open freight or last-mile delivery datasets (placeholder)
- **What modeling problem it can test:** Trip/event throughput, route efficiency proxies, dispatch timing, operational SLA tracking
- **Likely fact candidates:** `trips`, `stops`, `shipments`, `delivery_events`, `fuel_or_cost_events`
- **Likely dimension candidates:** `vehicle`, `driver`, `hub`, `route`, `date_time`, `service_level`
- **Likely grain ambiguity:** Trip-level vs stop-level records; planned route vs actual route events
- **Data quality risks:** GPS noise, missing coordinates, inconsistent local time handling, duplicate telemetry events
- **Licensing/check-before-use note:** Check municipal/open-data terms, attribution requirements, and restrictions on republishing transformed extracts

## Education

- **Dataset/source name placeholder:** Open University Learning Analytics Dataset (OULAD) / student performance datasets (placeholder)
- **What modeling problem it can test:** Course progression, assessment outcomes, engagement-to-completion relationships, intervention timing analyses
- **Likely fact candidates:** `enrollments`, `assessments`, `submissions`, `activity_events`, `attendance_or_engagement`
- **Likely dimension candidates:** `student`, `course`, `module`, `instructor`, `term`, `assessment_type`
- **Likely grain ambiguity:** Student-course-term grain vs per-assessment attempt grain; event logs vs aggregated engagement metrics
- **Data quality risks:** Survivor bias, inconsistent term definitions, missing demographic fields, policy-driven grading changes
- **Licensing/check-before-use note:** Confirm educational research clauses, anonymization guarantees, and redistribution constraints for packaged benchmark copies

## SaaS / Product Analytics

- **Dataset/source name placeholder:** Public clickstream/app event samples (e.g., Segment-style demo data) (placeholder)
- **What modeling problem it can test:** Funnel conversion, retention cohorts, feature adoption, subscription lifecycle analytics
- **Likely fact candidates:** `product_events`, `sessions`, `subscriptions`, `billing_events`, `support_tickets`
- **Likely dimension candidates:** `user`, `account`, `plan`, `feature`, `device`, `campaign`, `date`
- **Likely grain ambiguity:** Event-level vs session-level aggregation; user-level vs account-level metrics
- **Data quality risks:** Anonymous-to-known user stitching errors, bot/internal traffic contamination, schema drift in event names/properties
- **Licensing/check-before-use note:** Verify demo/sample dataset license provenance; ensure no embedded proprietary telemetry or terms limiting derivative redistribution

## Finance

- **Dataset/source name placeholder:** SEC filings structured extracts / FRED macro series / synthetic banking transactions (placeholder)
- **What modeling problem it can test:** Financial statement trend modeling, macro-factor integration, risk and exposure rollups, transaction anomaly scenarios
- **Likely fact candidates:** `ledger_entries`, `transactions`, `positions`, `balances`, `filing_metrics`
- **Likely dimension candidates:** `entity`, `account`, `instrument`, `counterparty`, `date`, `region`, `scenario`
- **Likely grain ambiguity:** Transaction date vs posting date; end-of-day balance snapshots vs intraday events
- **Data quality risks:** Restatements, survivorship bias, symbol/ticker mapping changes, timezone/currency conversion inconsistencies
- **Licensing/check-before-use note:** Validate reuse terms for derived datasets, market-data vendor restrictions, and obligations around attribution/disclaimer language

---

## Global caution

Before using any external dataset, verify license, privacy constraints, and whether it can be redistributed in this repository.
