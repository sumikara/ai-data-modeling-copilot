# Expected Semantic Behavior: case_02_mixed_header_line

## Purpose
Case for mixed_header_line.

## Expected JSON behavior
`requires_human_decision` must remain true and confidence should stay low/medium.

## Expected reasoning
Include grain reasoning, key reasoning, fact vs dimension reasoning, relationship reasoning, data-quality impact, SCD notes when relevant, unresolved questions.

## What would count as a failure
- Overconfident unsupported grain
- SQL/DDL generation
- Missing risk discussion
- `requires_human_decision=false`
