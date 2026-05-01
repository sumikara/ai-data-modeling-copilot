# Education Modeling Patterns

## Common business processes
- Representative operational events in this domain.

## Common fact tables
- Transaction/event facts
- Snapshot facts where applicable

## Common dimensions
- Party, product/service, date/time, location/channel

## Common grains
- event-level, line-level, snapshot-level depending process

## Common tricky cases
- mixed grains, reused identifiers, late-arriving dimensions, cross-source conflicts

## Common data quality risks
- null keys, duplicates, inconsistent codes, temporal anomalies

## Human decision questions
- final grain, key policy, SCD policy, conformance boundary

## Example business questions
- trend, performance, segment, conversion, risk, utilization questions

## Caveats
- patterns are guidance only; dataset-specific evidence and human approval are required.
