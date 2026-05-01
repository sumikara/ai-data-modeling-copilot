# Benchmark Summary (mock)

| Case | Mode | Overall score | Passed | Grain score | Fact/dim score | Confidence score | Critical failures | Failure categories |
|---|---|---:|---|---:|---:|---:|---|---|
| case_01_transaction_line_clear | mock | 68 | False | 30 | 0 | 0 | confidence_not_allowed | missing_data_quality_risks, overconfident_reasoning, wrong_fact_dimension_classification |
| case_02_order_header_line_mixed | mock | 100 | True | 30 | 20 | 10 |  | weak_knowledge_grounding |
| case_03_inventory_snapshot_hybrid | mock | 100 | True | 30 | 20 | 10 |  | weak_knowledge_grounding |
| case_04_customer_scd_conflict | mock | 100 | True | 30 | 20 | 10 |  | weak_knowledge_grounding |
| case_05_noisy_event_log_uncertain | mock | 100 | True | 30 | 20 | 10 |  | weak_knowledge_grounding |
| case_06_accumulating_snapshot_lifecycle | mock | 100 | True | 30 | 20 | 10 |  | weak_knowledge_grounding |
| case_07_factless_fact_attendance | mock | 100 | True | 30 | 20 | 10 |  | weak_knowledge_grounding |
| case_08_bridge_many_to_many | mock | 100 | True | 30 | 20 | 10 |  | weak_knowledge_grounding |
| case_09_degenerate_dimension_invoice | mock | 100 | True | 30 | 20 | 10 |  | weak_knowledge_grounding |
| case_10_product_attribute_drift_scd | mock | 100 | True | 30 | 20 | 10 |  | weak_knowledge_grounding |