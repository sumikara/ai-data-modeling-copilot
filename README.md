# AI Data Modeling Copilot

## Deterministic profiling module

This repository includes a deterministic CSV profiling module (no AI/LLM code).

### Input
- Place one or more CSV files under `data/raw/`

### Run
```bash
python -m src.profiling.profile_runner
```

### Output
- One JSON report per table under `outputs/profiles/`:
  - `outputs/profiles/{table_name}_profile.json`
- One combined summary:
  - `outputs/profiles/profile_summary.md`

### Running Semantic Profiling
- `mock` mode works without an API key.
- `llm` mode requires `OPENAI_API_KEY`.
- See setup and safety guidance: [`docs/api-key-setup.md`](docs/api-key-setup.md).

## Evaluation Showcase

This project includes multi-case semantic profiling fixtures as an **experimental decision-assistance layer**. The goal is to test whether an AI assistant can support (not replace) data modeling reasoning through **evidence-based semantic interpretation** and **human-approved modeling decisions**.

- Evaluation philosophy: [`docs/evaluation/thinking-process.md`](docs/evaluation/thinking-process.md)
- Roadmap: [`docs/evaluation/evaluation-roadmap.md`](docs/evaluation/evaluation-roadmap.md)
- Failure analysis template: [`docs/evaluation/failure-analysis-template.md`](docs/evaluation/failure-analysis-template.md)
- Profiling fixtures: [`test_inputs/semantic_profiling/cases/`](test_inputs/semantic_profiling/cases/)
- Expected behavior contracts: [`test_inputs/semantic_profiling/expected_outputs/`](test_inputs/semantic_profiling/expected_outputs/)
