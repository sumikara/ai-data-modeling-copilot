# Benchmark Methodology

This benchmark measures evidence-grounded semantic reasoning quality, not SQL generation.

- Exact string matching is insufficient because multiple grains/fact-dim options can be valid.
- Golden files use semantic constraints (allowed confidence, required keywords, forbidden outcomes).
- Grain/fact/dimension scoring uses overlap and constraint checks.
- Confidence calibration penalizes overconfidence under ambiguity/conflicts.
- `requires_human_decision=true` is enforced as a governance gate.
- Failure analysis feeds improvements to prompts, knowledge base rules, grader checks, and fixtures.
