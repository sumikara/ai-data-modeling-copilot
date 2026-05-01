# Retail DWH Troubleshooting Guide

## Purpose
Quick diagnostic reference for common Retail DWH pipeline, modeling, and governance issues.

## 1) `file_fdw` Path Errors
**Symptoms**
- Foreign table query fails with file/path access errors.

**Checks**
- Validate server-side absolute path.
- Confirm DB server process can access path.
- Verify file exists and extension/path match foreign table options.

**Actions**
- Correct file path in foreign table definition.
- Move file into approved DB-readable directory.
- Re-run source-ingestion sanity checks.

## 2) Missing Foreign Table
**Symptoms**
- `relation does not exist` for expected external table.

**Checks**
- Confirm foreign server and user mapping exist.
- Confirm schema/table name is correct and lowercase.

**Actions**
- Recreate foreign table in expected schema.
- Reapply grants for ETL runner role.

## 3) Row Count Mismatch
**Symptoms**
- External/source/mapping/NF/fact row counts diverge unexpectedly.

**Checks**
- Compare counts by layer and load batch.
- Validate `SELECT DISTINCT` vs `WHERE NOT EXISTS` behavior.

**Actions**
- Identify expected drop/add points by rule.
- Raise `DECISION_REQUIRED` when divergence conflicts with declared grain.

## 4) Date Parse Failures
**Symptoms**
- cast/parsing errors or high null parse output for date columns.

**Checks**
- Review date formats per source file.
- Validate standardization functions in clean staging.

**Actions**
- Normalize date parsing expressions.
- Log parse-failure rates before re-run.

## 5) Numeric Cast Failures
**Symptoms**
- errors casting numeric-like text columns.

**Checks**
- Detect commas/symbols/blank-like placeholders.
- Validate regex/replace standardization sequence.

**Actions**
- Apply deterministic cleaning before cast.
- Re-profile cast-readiness metrics.

## 6) Unexpected Duplicate Rows
**Symptoms**
- duplicate rows after incremental runs.

**Checks**
- Validate row-grain definition and duplicate policy.
- Confirm `row_sig` or composite-grain exclusion logic is active.

**Actions**
- Correct dedup condition placement.
- Re-run idempotency check (second run should be zero-net-change).

## 7) Default Row Overuse
**Symptoms**
- high percentage of FK = `-1` in facts.

**Checks**
- Review late-arriving dimension coverage.
- Inspect lookup join conditions by source channel.

**Actions**
- Fix lookup mapping where possible.
- Keep unresolved rows loadable, but raise quality alert.

## 8) FK Resolution Failures
**Symptoms**
- unresolved foreign keys or orphan fact rows.

**Checks**
- Validate lineage key availability (`*_nk`, `*_src_id`).
- Validate dimension load order and batch timing.

**Actions**
- Reconcile key-generation sequence across mapping/3NF.
- Reprocess failed batches after dimension correction.

## 9) Online/Offline Channel Rule Violations
**Symptoms**
- online records include store/employee keys,
- offline records include engagement keys.

**Checks**
- Validate channel-specific mapping filters.
- Verify source split assumptions and file routing.

**Actions**
- Apply channel-specific validation constraints.
- Backfill/repair affected records with audited scripts.

## 10) SCD2 Multiple Active Rows
**Symptoms**
- more than one active dimension row per business key.

**Checks**
- Validate expire-then-insert order.
- Validate `is_active` and `end_dt` update logic.

**Actions**
- Repair overlapping versions.
- Add guard check in SCD2 procedure logging.

## 11) Generated Column Immutable-Expression Error
**Symptoms**
- PostgreSQL rejects STORED generated column definition.

**Checks**
- Confirm expression is immutable.
- Remove runtime-dependent functions (e.g., `CURRENT_DATE`).

**Actions**
- Move dynamic logic to view/materialized view.
- Keep generated columns for deterministic expressions only.

## 12) Missing Sequence Permissions
**Symptoms**
- insert fails due to sequence usage privilege errors.

**Checks**
- Verify ETL role has `USAGE`/`SELECT` on sequence.

**Actions**
- Grant sequence privileges to ETL runner.
- Re-run failed load step.

## 13) Role/Permission Errors
**Symptoms**
- analysts cannot query required mart objects,
- ETL runner cannot write pipeline layers.

**Checks**
- Validate schema/table grants by role.
- Validate role inheritance and default privileges.

**Actions**
- Apply schema-based access policy.
- Separate analyst read grants from ETL write grants.

## Escalation Rule
When issue resolution requires policy choice (identity, SCD, grain, or governance conflict), mark it as:
- `DECISION_REQUIRED`
