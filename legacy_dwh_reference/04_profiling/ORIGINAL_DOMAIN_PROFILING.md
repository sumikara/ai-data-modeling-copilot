# Original Domain Profiling

## Purpose

This folder stores the original SQL profiling pack created during the manual Retail DWH project.

The goal of this profiling pack was not generic EDA.
It was used to understand source data quality and support data warehouse modeling decisions.

## What this profiling covers

- External table smoke tests
- Source table validation
- EXT vs SRC reconciliation
- Critical ID blank checks
- Date format quality
- Numeric-like text quality
- Duplicate transaction analysis
- Candidate line-grain checks
- Customer overlap and conflicts across sources
- Product descriptor duplication
- Product descriptor hash comparison
- Geography consistency and business key checks
- Cardinality snapshots
- Top frequency/category inspections

## Why this matters for the AI Data Modeling Copilot

These queries represent domain-specific profiling logic that can guide:

- grain discovery
- candidate key detection
- source-to-target mapping
- fact/dimension reasoning
- natural key selection
- data quality rule generation
- validation test design

## Reuse decision

Do not replace this logic with generic profiling.

This file should be used as a domain-aware reference and later refactored into:

- reusable profiling SQL templates
- Python profiling runners
- JSON profiling outputs
- modeling decision reports

## Current limitation

The original SQL contains useful profiling logic, but it is not yet machine-readable as an AI workflow artifact.

Missing items:

- saved profiling result outputs
- JSON profile reports
- entity-level summaries
- explicit grain decision report
- source-to-target mapping connection
- validation registry
