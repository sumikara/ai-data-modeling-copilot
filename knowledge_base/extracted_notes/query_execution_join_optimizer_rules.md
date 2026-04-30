# QUERY EXECUTION, JOIN STRATEGIES & OPTIMIZER

> **AI Copilot Usage Note:** Use this document to generate query-performance guidance that is explainable, evidence-based, and compatible with warehouse-scale workloads.

---

## 1. Query Execution Overview

A PostgreSQL query lifecycle has three core phases:

1. **Parsing** → syntax/semantic validation  
2. **Planning** → execution strategy generation  
3. **Execution** → physical data processing

Copilot recommendations should align with this lifecycle instead of treating SQL as a black box.

---

## 2. Query Planner (Optimizer)

The planner decides:
- table access paths
- index usage
- join order
- join algorithm

Primary objective:
- minimize estimated execution cost while preserving correctness.

---

## 3. Cost-Based Optimization

Planner cost estimates are driven by:
- table/cardinality statistics
- row-count estimates
- selectivity of predicates/indexes

Outdated statistics can produce poor plans even for correct SQL.

---

## 4. Execution Plan

Execution plan defines:
- operation sequence
- data movement between operators
- selected join/scan strategy

Typical operator chain:

```text
Seq Scan -> Hash Join -> Aggregate
```

---

## 5. EXPLAIN Command

Use EXPLAIN to inspect planned behavior before tuning.

```sql
EXPLAIN SELECT * FROM table_name;
```

For runtime truth, use execution-aware analysis (`EXPLAIN ANALYZE`) where safe.

---

## 6. Sequential Scan

Reads full table pages.

Appropriate when:
- table is small,
- predicate is not selective,
- index access would be more expensive.

---

## 7. Index Scan

Uses index lookup to reach qualifying rows.

Appropriate when:
- predicate selectivity is high,
- index key order matches filtering path.

---

## 8. Bitmap Scan

Combines index evidence before heap access.

Appropriate when:
- multiple predicates are present,
- many rows qualify but still fewer than full table scan.

---

## 9. Join Types (Logical)

### Inner Join
- returns only matched rows.

### Left Join
- preserves all rows from left input.

### Right Join
- preserves all rows from right input.

### Full Join
- preserves all rows from both inputs.

Copilot must choose logical join type by semantic requirement, not convenience.

---

## 10. Join Strategies (Physical)

### Nested Loop Join
- iterates outer rows and probes inner relation.
- best for small outer sets or index-assisted probes.

### Merge Join
- merges sorted inputs on join keys.
- best for large sorted streams.

### Hash Join
- builds hash structure for one input, probes with other.
- best for large equi-joins without strong index benefit.

---

## 11. Join Selection Rules

Planner selects physical join strategy using:
- input cardinalities
- available indexes/sort order
- join predicate type
- memory/cost estimates

Copilot should validate expected vs actual cardinality when plan choice looks wrong.

---

## 12. Join Order Importance

Join order strongly affects:
- intermediate result size
- memory pressure
- total runtime

Early reduction of high-cardinality branches is usually beneficial.

---

## 13. Filter Pushdown

Apply selective predicates as early as possible.

Benefits:
- lower row volume through joins
- reduced intermediate state
- faster execution

---

## 14. Aggregation

Common aggregations:
- `SUM`
- `COUNT`
- `AVG`

Prefer filtering before aggregation unless semantic order requires otherwise.

---

## 15. Sorting

Sorting is expensive (CPU + memory + potential disk spill).

Use only when:
- user result order is required,
- merge operations explicitly benefit,
- window/frame semantics require ordering.

---

## 16. Parallel Execution

PostgreSQL may parallelize:
- scans
- joins
- aggregations

Parallel gains depend on dataset size, operator eligibility, and system settings.

---

## 17. Statistics & ANALYZE

Planner quality depends on current statistics.

```sql
ANALYZE table_name;
```

Run statistics maintenance after major data distribution changes.

---

## 18. Common Performance Issues

- missing or misaligned indexes
- inefficient join order/cardinality explosion
- oversized intermediate results
- stale statistics
- implicit casts preventing index usage

---

## 19. Query Optimization Techniques

- index for actual predicate/join usage
- push selective filters early
- project only required columns
- remove unnecessary joins
- avoid function-wrapped predicate columns where possible

---

## 20. Anti-Patterns

Avoid:
- `SELECT *` in wide/large analytic paths
- joins without clear necessity
- non-sargable predicates (functions on indexed filter columns)
- implicit type casting on join/filter keys

---

## 21. Execution Plan Reading

High-risk indicators:
- sequential scan on very large tables where selective filters exist
- expensive nested loops over large cardinalities
- unexpectedly high estimated/actual row gaps
- repeated re-check or spill-heavy operators

---

## 22. Partition Pruning

With partitioned tables, effective predicates should restrict scans to relevant partitions.

If pruning does not occur, inspect predicate form and partition key alignment.

---

## 23. Index-Only Scan

Can avoid heap access when index contains all needed columns and visibility conditions are met.

Useful for high-frequency lookup/report queries with covering-index design.

---

## 24. Query Rewriting

Rewrite when beneficial to:
- reduce intermediate cardinality
- improve predicate sargability
- simplify join graph for better planner choices

Always verify with EXPLAIN before/after.

---

## 25. Performance Monitoring

Track at minimum:
- query latency
- CPU utilization
- I/O behavior
- plan regression trends

Combine planner inspection with runtime metrics for reliable optimization.

---

## 26. AI Copilot Rules

The Copilot must:
- choose join logic from business semantics first,
- consider physical join strategy from cardinality/index evidence,
- enforce early filter pushdown where valid,
- avoid unnecessary scans and projections,
- require EXPLAIN-based validation before optimization claims.

```text
Approval gate:
No performance recommendation is final without plan evidence and measured runtime impact.
```
