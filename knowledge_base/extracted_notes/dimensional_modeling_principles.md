# Dimensional Modeling Principles

## Rule
Dimensional outputs MUST reflect stable business process semantics with explicit fact grain and conformed dimensions.

## When to use
- During star-schema recommendations.
- During dimension boundary and conformance reasoning.
- While validating measure placement and additive behavior.

## Evidence required
- Grain evidence report.
- Relationship cardinality and key coverage.
- Measure behavior profile (additive/semi-additive/non-additive).

## Copilot must NOT do
- Must NOT create dimensions/facts from naming heuristics alone.
- Must NOT mix multiple business grains in a single fact recommendation.
- Must NOT treat conformed dimensions as optional when cross-process analytics is required.

## Human approval required
- Final dimension conformance policy.
- Bridge/junk dimension decisions.
- Any fact split/merge decision affecting reporting semantics.
