# Default Row Strategy

## Rule
Default/sentinel rows MUST preserve referential integrity when dimension lookup resolution fails.

## When to use
- During fact loading with unresolved foreign keys.
- During late-arriving dimension scenarios.
- During incremental loads where dimension timing lags fact ingestion.

## Evidence required
- Lookup miss rates by dimension.
- Explicit default-row contract (key value + semantic label).
- Data quality impact of unresolved references.

## Copilot must NOT do
- Must NOT drop fact rows silently due to unresolved dimension keys.
- Must NOT use defaults without traceability tags.
- Must NOT treat default-row routing as a permanent substitute for data repair.

## Human approval required
- Sentinel key conventions and labels.
- Thresholds that trigger data remediation vs tolerated default routing.
