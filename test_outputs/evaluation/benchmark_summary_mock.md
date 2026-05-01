# Benchmark Summary (mock)

| Case | Mode | Overall score | Passed | Grain score | Fact/dim score | Confidence score | Critical failures | Failure categories |
|---|---|---:|---|---:|---:|---:|---|---|
| case_01_transaction_line_clear | mock | 96 | True | 30 | 20 | 10 |  | missing_data_quality_risks |
| case_02_order_header_line_mixed | mock | 98 | True | 30 | 20 | 10 |  | missing_data_quality_risks |
| case_03_inventory_snapshot_hybrid | mock | 96 | True | 30 | 20 | 10 |  | ignored_null_or_duplicate_evidence, missing_data_quality_risks |
| case_04_customer_scd_conflict | mock | 98 | True | 30 | 20 | 10 |  | missing_data_quality_risks |
| case_05_noisy_event_log_uncertain | mock | 100 | True | 30 | 20 | 10 |  | weak_knowledge_grounding |
| case_06_accumulating_snapshot_lifecycle | mock | 98 | True | 30 | 20 | 10 |  | missing_data_quality_risks |
| case_07_factless_fact_attendance | mock | 96 | True | 30 | 20 | 10 |  | ignored_null_or_duplicate_evidence, missing_data_quality_risks |
| case_08_bridge_many_to_many | mock | 96 | True | 30 | 20 | 10 |  | missing_data_quality_risks |
| case_09_degenerate_dimension_invoice | mock | 96 | True | 30 | 20 | 10 |  | ignored_null_or_duplicate_evidence, missing_data_quality_risks |
| case_10_product_attribute_drift_scd | mock | 96 | True | 30 | 20 | 10 |  | ignored_null_or_duplicate_evidence, missing_data_quality_risks |