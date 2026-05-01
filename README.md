# AI Data Modeling Copilot

## 1. Project summary
AI-assisted, evidence-driven data modeling decision support for CSV datasets. This system helps engineers reason about grain, keys, fact/dimension options, and risks while keeping final decisions human-approved.

## 2. What problem this solves
Data-modeling decisions are ambiguous and context-heavy. The project combines deterministic profiling + retrieval-grounded semantic reasoning + evaluation guardrails.

## 3. What this assistant can do
- infer likely domain/process signals
- propose grain/key alternatives
- suggest fact/dimension/hybrid/snapshot/bridge candidates
- surface data-quality and cross-source conflicts
- suggest analytics/star/snowflake directions with caveats
- require unresolved questions and human decision gates

## 4. What this assistant cannot do
- finalize autonomous warehouse design
- replace data engineers
- guarantee model correctness
- publish production DDL/SQL from semantic reasoning stage

## 5. Technical architecture
See [`docs/architecture/technical-flow.md`](docs/architecture/technical-flow.md).

## 6. Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## 7. Run deterministic profiling
```bash
python -m src.profiling.profile_runner
```

## 8. Run semantic profiling
```bash
python scripts/run_semantic_profiling_mock.py
python scripts/run_semantic_profiling.py
```

## 9. Run benchmark
```bash
python scripts/run_benchmark.py --mode mock
python scripts/run_benchmark.py --mode llm
python scripts/run_benchmark.py --mode gemini
python scripts/run_benchmark.py --mode all
```

## 10. Evaluation evidence
- [`docs/evaluation/benchmark-methodology.md`](docs/evaluation/benchmark-methodology.md)
- [`docs/evidence/evidence-package.md`](docs/evidence/evidence-package.md)
- [`test_inputs/semantic_profiling/cases/`](test_inputs/semantic_profiling/cases/)
- [`test_inputs/semantic_profiling/golden/`](test_inputs/semantic_profiling/golden/)
- `test_outputs/evaluation/`

## 11. Human-in-the-loop governance
All semantic outputs must preserve `requires_human_decision=true`. Outputs are decision support only.

## 12. Limitations
- synthetic fixtures can’t represent all production edge cases
- LLM reasoning can be inconsistent without retrieval and grader rails
- ambiguous cases intentionally remain unresolved pending human/business approval

## 13. Roadmap
See [`docs/evaluation/evaluation-roadmap.md`](docs/evaluation/evaluation-roadmap.md) and provider setup at [`docs/model-providers.md`](docs/model-providers.md).


## Evaluation Benchmark

This repository includes an **AI-assisted semantic modeling benchmark** focused on decision support, evidence-based reasoning, and human-approved modeling decisions.

- Multi-case semantic modeling benchmark
- Golden expected outputs
- Semantic diff comparator
- Failure taxonomy
- Benchmark runner
- Human-in-the-loop decision gate
- Evidence package

Key assets:
- `test_inputs/semantic_profiling/cases/`
- `test_inputs/semantic_profiling/golden/`
- `docs/evaluation/test-case-design.md`
- `docs/evaluation/benchmark-methodology.md`
- `docs/evaluation/failure-analysis-template.md`
- `docs/evaluation/model-comparison-report.md`
