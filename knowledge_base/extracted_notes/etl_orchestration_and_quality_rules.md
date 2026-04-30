# ETL Orchestration and Quality Rules

## Rule
ETL orchestration MUST be observable, rerunnable, and quality-gated with structured logging.

## When to use
- During procedure/workflow design.
- During failure handling and restart logic.
- During quality checkpoint definition across stages.

## Evidence required
- Batch/step execution logs with status and row metrics.
- Error diagnostics captured from exception paths.
- Input-to-output reconciliation statistics.
- Quality gate outcomes per stage.

## Copilot must NOT do
- Must NOT recommend opaque workflows without log coverage.
- Must NOT ignore partial-failure rollback/compensation needs.
- Must NOT claim quality success without measurable checks.

## Human approval required
- SLA/threshold policies for failure and quality tolerances.
- Escalation rules for rerun vs rollback decisions.
