# Evaluation Roadmap

## Milestone 1 — Multi-case static evaluation
- Add five profiling fixtures
- Add expected behavior docs
- Run mock mode
- Store actual outputs
- Compare against expected behavior manually

## Milestone 2 — Automated semantic grading expansion
Future grader checks:
- confidence must be low/medium when `recommended_grain=uncertain`
- confidence cannot be high when `cross_source_conflicts` is non-empty
- SCD type finalization should be a critical failure
- fact/dimension classification should align with measures and repeated event behavior
- noisy event logs should require unresolved questions
- expected outputs can later become machine-readable assertions

## Milestone 3 — Portfolio/Medium evidence package
Artifacts to show:
- architecture diagram
- one successful case
- one ambiguous case
- one failure case
- before/after prompt improvement
- discussion of human-in-the-loop decision design
