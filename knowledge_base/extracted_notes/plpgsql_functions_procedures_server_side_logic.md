# PL/pgSQL, FUNCTIONS, PROCEDURES & SERVER-SIDE LOGIC

> **AI Copilot Usage Note:** Use this document to generate safe, maintainable PostgreSQL server-side patterns for ETL and operational workflows, prioritizing correctness, observability, and set-based performance.

---

## 1. PL/pgSQL Overview

PL/pgSQL is PostgreSQL’s procedural language for implementing database-resident logic.

Typical usage:
- server-side workflow control,
- ETL orchestration,
- reusable data operations close to storage.

---

## 2. Why Use PL/pgSQL

Advantages:
- reduces client-server round trips,
- executes logic close to data,
- improves latency for multi-step operations,
- supports robust transactional workflows.

Use PL/pgSQL when orchestration or controlled side effects are required, not for simple single-statement SQL.

---

## 3. PL/pgSQL Block Structure

Canonical block form:

```sql
DO $$
DECLARE
  -- variables
BEGIN
  -- logic
END;
$$ LANGUAGE plpgsql;
```

For functions/procedures, the same `DECLARE ... BEGIN ... END` pattern applies inside the body.

---

## 4. Variables

Variables store intermediate values, counters, flags, and row records.

```sql
DECLARE
  v_count       integer := 0;
  v_started_at  timestamptz := now();
  v_row         record;
```

Prefer explicit, descriptive names and initialize where possible.

---

## 5. Control Flow

### IF Statement

```sql
IF v_count = 0 THEN
  RAISE NOTICE 'No rows to process';
ELSIF v_count < 1000 THEN
  RAISE NOTICE 'Small batch';
ELSE
  RAISE NOTICE 'Large batch';
END IF;
```

### LOOP

```sql
LOOP
  EXIT WHEN v_count >= 10;
  v_count := v_count + 1;
END LOOP;
```

### FOR Loop

```sql
FOR v_row IN
  SELECT id, status
  FROM staging_orders
LOOP
  -- process row
END LOOP;
```

Copilot should prefer set-based SQL first and loops only when row-wise logic is truly required.

---

## 6. Functions

Functions:
- return a value (scalar, row, or set),
- encapsulate reusable computation,
- can be used in SQL expressions and queries.

```sql
CREATE OR REPLACE FUNCTION get_total_orders(p_customer_id bigint)
RETURNS integer
LANGUAGE plpgsql
AS $$
DECLARE
  v_total integer;
BEGIN
  SELECT count(*)
  INTO v_total
  FROM fact_orders
  WHERE customer_id = p_customer_id;

  RETURN v_total;
END;
$$;
```

---

## 7. Procedures

Procedures:
- are invoked with `CALL`,
- are suited for multi-step operational/ETL workflows,
- can include transaction control behavior depending on invocation context and design.

```sql
CREATE OR REPLACE PROCEDURE load_daily_orders(p_batch_date date)
LANGUAGE plpgsql
AS $$
BEGIN
  -- ETL logic
  INSERT INTO fact_orders (...)
  SELECT ...
  FROM staging_orders
  WHERE order_date = p_batch_date;
END;
$$;
```

---

## 8. Difference Between Function and Procedure

Function:
- must return something,
- is used inside SQL queries,
- typically best for computation and reusable expressions.

Procedure:
- invoked as an executable unit,
- typically used for ETL/job orchestration,
- preferred for operational steps with logging and controlled side effects.

---

## 9. Exception Handling

Use exception blocks to capture and classify failures.

```sql
BEGIN
  -- logic
EXCEPTION
  WHEN unique_violation THEN
    RAISE NOTICE 'Duplicate detected, skipping batch item';
  WHEN OTHERS THEN
    RAISE;
END;
```

Avoid swallowing errors silently; log context and rethrow unless business rules explicitly allow continuation.

---

## 10. Error Logging

On failure, capture at minimum:
- SQLSTATE,
- error message,
- failing step/module,
- batch/job identifiers,
- timestamp.

```sql
INSERT INTO etl_error_log(job_name, step_name, sqlstate, error_message, logged_at)
VALUES ('load_daily_orders', 'upsert_fact_orders', SQLSTATE, SQLERRM, now());
```

---

## 11. Cursors

Cursors support controlled, incremental row processing.

```sql
DECLARE
  cur_orders CURSOR FOR
    SELECT order_id, customer_id
    FROM staging_orders;
```

Use cursors when you need ordered, stepwise handling that is hard to express set-wise.

---

## 12. Cursor Use Cases

Appropriate use cases:
- very large datasets requiring controlled memory patterns,
- external side-effect processing per row,
- sequential dependency between processed rows.

If set-based SQL can express the logic safely, prefer set-based SQL.

---

## 13. Dynamic SQL

Dynamic SQL executes statements built at runtime.

```sql
EXECUTE format(
  'INSERT INTO %I (id, value) SELECT id, value FROM %I',
  'fact_orders',
  'staging_orders'
);
```

Prefer `format()` with `%I` / `%L` and parameter binding to reduce injection risk.

---

## 14. Dynamic SQL Use Cases

Use dynamic SQL for:
- variable table/schema targets,
- metadata-driven ETL,
- runtime-selected partition objects.

Never concatenate untrusted input directly into executable SQL.

---

## 15. Triggers

Triggers execute automatically on table events:
- `INSERT`,
- `UPDATE`,
- `DELETE`.

Use sparingly in high-volume pipelines because hidden side effects can complicate performance and debugging.

---

## 16. Trigger Use Cases

Good use cases:
- audit trail capture,
- lightweight validation,
- derived-column maintenance when centralized enforcement is required.

Avoid heavy business logic in triggers for large fact loads.

---

## 17. Transaction Control

Transaction control preserves consistency across multi-step operations.

```sql
BEGIN;
-- staging load
-- validation
-- merge/upsert
COMMIT;
```

On failure, ensure rollback and error logging paths are explicit.

---

## 18. ETL with Procedures

Procedure-driven ETL should:
- decompose pipeline stages (ingest, validate, load, reconcile),
- apply consistent logging/checkpoint standards,
- expose clear inputs/outputs per stage.

This improves restartability and operational support.

---

## 19. Modular Design

Design principles:
- small, single-purpose routines,
- shared utility functions for repeated patterns,
- orchestration procedure that coordinates modules.

Modularity improves testability and change safety.

---

## 20. Parameterized Procedures

Parameters increase reuse and operational flexibility.

```sql
CREATE OR REPLACE PROCEDURE run_fact_load(
  p_batch_id uuid,
  p_batch_date date,
  p_source_system text
)
LANGUAGE plpgsql
AS $$
BEGIN
  -- use parameters in controlled ETL flow
END;
$$;
```

Use strong types and document parameter semantics.

---

## 21. Performance Considerations

Key rules:
- avoid unnecessary row-by-row loops,
- favor set-based `INSERT ... SELECT`, `MERGE`, and bulk operations,
- ensure indexes support lookup/merge predicates,
- profile query plans for heavy SQL blocks.

Copilot must justify procedural design against measurable bottlenecks.

---

## 22. Logging in Procedures

Each production ETL procedure should log:
- start event,
- end event,
- row counts by critical step,
- warnings/errors with context.

```sql
INSERT INTO etl_job_log(job_name, batch_id, status, row_count, logged_at)
VALUES ('run_fact_load', p_batch_id, 'STARTED', NULL, now());
```

---

## 23. Idempotent Procedures

Idempotency means re-running the same batch does not corrupt results.

Patterns:
- deterministic natural/business keys,
- `MERGE`/upsert strategies,
- deduplication guards,
- batch markers/checkpoints.

Idempotency is mandatory for resilient ETL retry behavior.

---

## 24. Debugging

Practical debugging approach:
- use structured logs and step identifiers,
- execute component queries independently,
- replay small controlled batches,
- isolate failures by stage.

Avoid ad-hoc print-only debugging in production workflows.

---

## 25. Best Practices

Use these defaults:
- clear naming conventions,
- modular and testable routines,
- explicit exception handling,
- consistent operational logging,
- documentation for assumptions and side effects.

---

## 26. AI Copilot Rules

The Copilot must:
- prefer procedures for multi-step ETL orchestration,
- include explicit exception-handling strategy,
- use dynamic SQL only when structural variability requires it,
- avoid row-by-row patterns unless justified,
- enforce start/end/row-count/error logging for every critical ETL step.

```text
Approval gate:
No server-side logic recommendation is final without validation of correctness,
idempotency behavior, and observed runtime impact.
```
