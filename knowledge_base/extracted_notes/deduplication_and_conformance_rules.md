# DATA QUALITY, DEDUPLICATION & LINEAGE

> **AI Copilot Usage Note:** Use this document to enforce quality controls, deterministic deduplication, lineage traceability, and conflict-safe reconciliation.

---

## 1. Data Quality Overview

Data quality ensures data is:
- accurate
- complete
- consistent
- unique
- valid

Poor quality leads to:
- incorrect reporting
- unstable joins
- unreliable business decisions

---

## 2. Core Data Quality Dimensions

### Accuracy
Data represents real-world truth for the intended business process.

### Completeness
Critical fields are present for downstream use.

### Consistency
Equivalent business concepts are represented uniformly across sources/layers.

### Uniqueness
Rows are unique at the declared grain.

### Validity
Values comply with required format/type/domain constraints.

---

## 3. Data Quality Responsibilities

Quality ownership by layer:
- **Landing** → format-level and ingestion sanity checks
- **Staging** → cleaning, normalization, standardization
- **Core** → business-rule and integrity enforcement
- **Data Mart** → reporting-readiness validation

Copilot should always map recommendations to the correct layer responsibility.

---

## 4. Deduplication Overview

Deduplication removes unintended duplicates while preserving valid business events.

Primary goals:
- prevent double counting
- preserve metric correctness
- ensure stable aggregation behavior

---

## 5. Deduplication Strategies

### Strategy 1 — DISTINCT
Use when duplicate rows are fully identical.

```sql
SELECT DISTINCT *
FROM table_name;
```

### Strategy 2 — ROW_NUMBER
Use when duplicate candidates require ranking policy.

```sql
WITH ranked AS (
  SELECT *,
         ROW_NUMBER() OVER (PARTITION BY business_key ORDER BY updated_at DESC) AS rn
  FROM table_name
)
SELECT *
FROM ranked
WHERE rn = 1;
```

### Strategy 3 — Hash-Based Deduplication
Use when duplicates are multi-column and complex.

```text
row_signature = MD5(canonicalized_row_content)
```

---

## 6. Transaction-Level Deduplication

For fact/event tables:
- derive deterministic row signature
- enforce uniqueness at fact grain

```text
Example signature inputs:
transaction_id + product_id + event_timestamp (+ source triplet where needed)
```

---

## 7. Deduplication Rules

- Must be deterministic and rerunnable.
- Must be grain-aware.
- Must be consistent across pipeline layers.
- Must not discard valid business events.
- Must be auditable (criteria and exclusion logic are traceable).

---

## 8. Source Triplet (Critical)

Each integrated row should preserve:
- `source_system`
- `source_table`
- `source_id`

---

## 9. Source Triplet Purpose

- lineage tracking
- debugging and root-cause analysis
- cross-source disambiguation
- reconciliation and audit readiness

---

## 10. Source Triplet Rules

- Always present in integration pathways.
- Stable text-compatible representation.
- Never uncontrolled NULL in required lineage scope.
- Naming must be consistent across layers.

---

## 11. Data Lineage

Lineage describes the trace path:

```text
Source -> Transformation -> Target
```

It must be queryable and explainable for each materialized dataset.

---

## 12. Lineage Goals

- trace origin of every critical attribute
- explain transformation decisions
- accelerate debugging
- satisfy audit/governance requirements

---

## 13. Lineage Implementation

Lineage artifacts should include:
- source references
- transformation rule references
- mapping documentation
- load/batch context metadata

---

## 14. Mapping Layer Responsibilities

Mapping layer must provide:
- semantic alignment across sources
- key derivation logic
- lineage preservation
- deterministic bridge from source keys to target keys

---

## 15. Mapping Layer Techniques

Typical techniques:
- multi-source joins with explicit precedence
- format/semantic standardization
- business/composite key derivation
- row-level count/checkpoint tracking

---

## 16. Data Reconciliation

Reconciliation verifies source-target consistency.

Required checks:
- row-count comparisons
- key coverage
- missing/unmatched record analysis

---

## 17. Data Validation Rules

Validate at minimum:
- nullability constraints
- data types
- value ranges
- referential integrity

Validation outcomes should be logged with actionable diagnostics.

---

## 18. Handling Null Values

- Avoid unresolved NULL foreign keys in fact/integration outputs.
- Use approved default/sentinel member strategy where required.
- Track and monitor unresolved mappings as quality issues.

---

## 19. Data Standardization

Standardization must enforce:
- consistent formats
- normalized values
- unified naming conventions
- deterministic casting behavior

---

## 20. Cross-Source Conflicts

When sources disagree:
- apply approved source-priority rules
- log conflicts explicitly
- apply reconciliation policy with traceability

No silent conflict suppression.

---

## 21. Duplicate Detection Signals

Common indicators:
- repeated business keys at unexpected frequency
- identical content signatures
- abnormal event frequency spikes
- key+timestamp collision patterns

---

## 22. Data Integrity Rules

Integrity controls must ensure:
- no orphan records
- valid relationships
- stable and reproducible joins

---

## 23. Error Handling

On processing error:
- capture detailed diagnostics
- isolate impacted rows/batches when possible
- continue safe processing where policy allows
- never lose observability context

---

## 24. Data Quality Monitoring

Continuously track:
- error rates
- duplicate rates
- null ratios
- reconciliation deltas

Use thresholds to trigger remediation/escalation.

---

## 25. Testing Strategy

Minimum test suite must validate:
- uniqueness at declared grain
- completeness of critical fields
- referential integrity
- source-to-target reconciliation coverage

---

## 26. AI Copilot Rules

The Copilot must:
- never ignore duplicate signals,
- validate grain before deduplication actions,
- preserve and reference lineage,
- never drop records silently,
- require human approval for cross-source conflict resolution.

```text
Approval gate:
No irreversible conflict-resolution policy should be finalized without human sign-off.
```
