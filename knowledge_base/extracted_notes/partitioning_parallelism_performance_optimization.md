# PARTITIONING, PARALLELISM & PERFORMANCE OPTIMIZATION

> **AI Copilot Usage Note:** Use this document to produce warehouse-focused recommendations that are explainable, operationally safe, and validated against real query patterns.

---

## 1. Partitioning Overview

Partitioning splits a large logical table into smaller physical segments (partitions).

Primary goals:
- improve query performance by scanning less data,
- simplify lifecycle management,
- increase opportunities for parallel execution.

---

## 2. Why Partitioning Matters in DWH

In data warehouses:
- fact tables are typically high-volume,
- analytical queries frequently filter by time,
- load windows and maintenance operations must remain predictable.

Partition design is therefore a core performance decision, not just a storage choice.

---

## 3. Partitioning Benefits

Well-designed partitioning provides:
- faster queries via partition pruning,
- simpler retention/archival operations,
- improved bulk-load workflows,
- better parallelism for large scans.

---

## 4. Partitioning Key Selection

A partition key should:
- align with common filter predicates,
- appear frequently in `WHERE` clauses,
- significantly reduce scanned data.

Common keys:
- date/time,
- region,
- category.

Rule: choose keys from observed workload patterns, not assumptions.

---

## 5. Partitioning Types

### Range Partitioning
Split by contiguous value ranges.

Typical DWH examples:
- monthly partitions,
- yearly partitions.

### List Partitioning
Split by discrete value sets.

Typical examples:
- region,
- country.

### Inheritance-Based Partitioning
Manual legacy pattern; usually replaced by native declarative partitioning in modern PostgreSQL deployments.

---

## 6. Partitioning Rules

Enforce these invariants:
- each row maps to exactly one partition,
- partition boundaries do not overlap,
- partition key values remain stable post-insert.

Violating these rules increases correctness and maintenance risk.

---

## 7. Partition Pruning

Partition pruning means the planner scans only relevant partitions.

Prerequisite:
- query predicates must be compatible with the partition key.

```sql
EXPLAIN
SELECT *
FROM fact_sales
WHERE sale_date >= DATE '2026-01-01'
  AND sale_date <  DATE '2026-02-01';
```

Copilot should verify pruning behavior in the plan before claiming partitioning success.

---

## 8. Partition Maintenance

Standard operations:
- create future partitions,
- drop expired partitions,
- archive historical partitions.

Prefer automated, calendar-driven maintenance to avoid late partition creation during loads.

---

## 9. Partition-Based Loading

Recommended pattern:
1. load data into a target/staging table,
2. validate distribution and constraints,
3. attach/swap into the final partition structure.

Benefits:
- faster ingestion,
- reduced lock contention,
- safer rollback boundaries.

---

## 10. Partitioning in Fact Tables

Best practice:
- partition large fact tables by business-relevant time grain,
- match grain to dominant reporting windows (day/month/quarter).

Do not over-partition if query filters are coarse and data volume is modest.

---

## 11. Indexing & Partitioning

Guidance:
- design indexes at partition level based on partition-local access paths,
- avoid unnecessary index duplication across all partitions,
- continuously review index usefulness from query evidence.

Index strategy must complement partition pruning, not replace it.

---

## 12. Parallel Execution Overview

PostgreSQL can parallelize:
- table scans,
- selected joins,
- selected aggregations.

Parallel execution is cost-based and workload-dependent.

---

## 13. Parallel Query Benefits

Potential benefits:
- lower wall-clock query latency,
- better CPU utilization,
- improved throughput for analytical workloads.

---

## 14. When Parallelism Works

Parallel plans are most useful when:
- datasets are large,
- operators are parallel-safe,
- worker/process settings and hardware capacity are sufficient.

---

## 15. Parallel Execution Limitations

Parallelism may underperform when:
- datasets are small,
- operator coordination overhead dominates,
- configuration limits worker availability.

Copilot should avoid blanket “enable parallelism” advice without plan evidence.

---

## 16. Performance Optimization Principles

Prioritize:
- reducing scanned data,
- minimizing unnecessary joins,
- using selective, justified indexes,
- aligning physical design with access patterns.

Always optimize based on measured bottlenecks.

---

## 17. Bulk Load Optimization

Bulk-load best practices:
- prefer `COPY` over row-by-row `INSERT`,
- load in controlled batches/windows,
- defer non-essential index and constraint overhead,
- rebuild/validate structures after load completion.

---

## 18. COPY Command (Critical)

`COPY` is typically faster because it:
- executes as a set-oriented operation,
- reduces statement-level overhead,
- uses ingestion paths optimized for bulk data.

```sql
COPY fact_sales (sale_id, sale_date, customer_id, amount)
FROM '/data/inbound/fact_sales_2026_01.csv'
WITH (FORMAT csv, HEADER true);
```

---

## 19. Index Optimization

Index rules for high-volume pipelines:
- create or rebuild heavy indexes after major bulk loads when feasible,
- keep only indexes that support real query predicates,
- remove low-value indexes that add write/load cost.

---

## 20. Constraint Optimization

For large ingestion batches:
- apply/defer costly validations strategically,
- validate data integrity after insertion,
- avoid long-running lock-heavy constraint operations during peak windows.

---

## 21. Referential Integrity

Maintain:
- valid foreign-key relationships,
- consistent dimensional references,
- controlled handling for unknown/default dimension members.

Integrity shortcuts must be temporary and explicitly governed.

---

## 22. Mass Updates

Avoid frequent large-scale updates on warehouse fact data.

Prefer append-oriented patterns:
- insert corrected/new versions,
- isolate correction logic into controlled backfill jobs.

This reduces bloat, lock pressure, and unpredictability.

---

## 23. Data Pruning

Regularly remove or archive:
- obsolete records,
- expired partitions.

Retention policy should be explicit and enforced through automated jobs.

---

## 24. Materialized Views

Use materialized views for:
- precomputed aggregations,
- repeated expensive analytical queries.

Tradeoff:
- data freshness depends on refresh cadence.

---

## 25. Refresh Strategy

Refresh options:
- manual,
- scheduled,
- event/trigger-driven.

When supported and appropriate, use concurrent refresh patterns to reduce blocking.

```sql
-- Example pattern (engine/version dependent):
-- REFRESH MATERIALIZED VIEW CONCURRENTLY mv_sales_monthly;
```

Copilot must call out freshness-vs-latency tradeoffs in recommendations.

---

## 26. AI Copilot Rules

The Copilot must:
- recommend partitioning for large fact tables when workload evidence supports it,
- align partition keys with observed filter patterns,
- prefer `COPY` for bulk ingestion,
- avoid unnecessary mass updates on large tables,
- require partition-pruning validation in execution plans,
- evaluate parallel execution only when dataset size and plan operators justify it.

```text
Approval gate:
No optimization recommendation is final without plan evidence (EXPLAIN/ANALYZE where safe)
and measured runtime impact against a baseline.
```
