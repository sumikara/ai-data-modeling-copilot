# Expected Semantic Behavior: case_10_encounter_fact

## Purpose
Case for encounter_fact.

## Expected JSON behavior
`requires_human_decision` must remain true and confidence should stay low/medium.

## Expected reasoning
Include grain reasoning, key reasoning, fact vs dimension reasoning, relationship reasoning, data-quality impact, SCD notes when relevant, unresolved questions.

## What would count as a failure
- Overconfident unsupported grain
- SQL/DDL generation
- Missing risk discussion
- `requires_human_decision=false`
