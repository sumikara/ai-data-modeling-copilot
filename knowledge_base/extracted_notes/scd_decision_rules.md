# SCD Decision Rules

## Rule
SCD strategy MUST be selected per attribute/entity using change behavior evidence and business impact.

## When to use
- During dimension design.
- When cross-source conflicts or temporal drift appear.
- When overwrite vs history trade-off impacts analytics.

## Evidence required
- Attribute volatility signals.
- Cross-source conflict rates.
- Temporal snapshots showing value change behavior.
- Reporting use-case impact of history retention.

## Copilot must NOT do
- Must NOT assign SCD type globally for all dimensions.
- Must NOT finalize Type 2 without temporal evidence.
- Must NOT overwrite historical attributes when audit/history is required.

## Human approval required
- Final SCD type selection (0/1/2) by entity/attribute.
- Survivorship rules where source conflicts exist.
