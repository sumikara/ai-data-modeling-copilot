# Profile Artifact Schema

Standard profile artifacts for semantic reasoning across retail, e-commerce, healthcare, finance, education, logistics, and SaaS/product analytics.

## Schema sections
- `table_profile`: table metadata and row volume context.
- `columns`: per-column evidence (`null_ratio`, `distinct_ratio`, `uniqueness_ratio`, `sample_values`).
- `candidate_composite_keys`: key alternatives with null-blocking and uniqueness behavior.
- `relationship_candidates`: inferred joins and confidence hints.
- `domain_pattern_findings`: inferred behavioral patterns (event, snapshot, hybrid, conflict).
- `measure_candidates`: candidate numeric measures.
- `cross_source_conflicts`: attribute-level conflicts across systems.
- `sample_rows`: representative row examples.
- `dataset_context`: source/process caveats.

## Field guidance
For each field, capture purpose, example, modeling impact, and confidence impact.

| Field | Purpose | Example | Modeling help | Confidence impact |
|---|---|---|---|---|
| `table_profile.table_name` | identify entity context | `encounter_events` | domain/process hint | wrong naming lowers confidence |
| `table_profile.row_count` | scale signal | `250000` | distinguish master vs event tendencies | low volume can weaken inference |
| `columns.*.null_ratio` | completeness evidence | `0.35` | key viability, relationship risk | high nulls reduce confidence |
| `columns.*.uniqueness_ratio` | identity strength | `0.82` | grain/key candidacy | weak uniqueness lowers confidence |
| `candidate_composite_keys` | compare key options | `['order_id','line_no']` | grain alternatives | null blocking or low uniqueness lowers confidence |
| `relationship_candidates` | joinability hints | `customer_id -> dim_customer` | fact/dimension context | weak overlap lowers confidence |
| `domain_pattern_findings` | higher-order behavior | `periodic_snapshot` | classify fact/dim/hybrid | mixed signals lower confidence |
| `measure_candidates` | additive signal discovery | `quantity`, `charge_amount` | fact-like behavior | no measures may imply factless/hybrid |
| `cross_source_conflicts` | conformance/SCD risk | `loyalty_tier conflict_rate=0.04` | SCD candidate identification | conflicts reduce confidence |
| `sample_rows` | sanity-check semantics | short row list | detect repeated header fields | anomalies reduce confidence |
| `dataset_context` | source caveats/policy | synthetic, merged, delayed feed | governance-aware recommendations | missing context lowers confidence |

## Example snippets
### Transaction-like table
```json
{"table_name":"sales_lines","row_count":50000,"candidate_composite_keys":[{"columns":["transaction_id","product_id","transaction_dt"],"uniqueness_ratio":0.998}]}
```
### Dimension-like entity
```json
{"table_name":"customer_profile","measure_candidates":[],"cross_source_conflicts":[{"attribute":"segment","conflict_rate":0.06}]}
```
### Snapshot fact
```json
{"table_name":"inventory_snapshot","domain_pattern_findings":{"grain_signal":"periodic_snapshot"}}
```
### Noisy event log
```json
{"table_name":"web_event_log","columns":{"user_id":{"null_ratio":0.35}},"domain_pattern_findings":{"identity_reliability":"weak"}}
```
