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
