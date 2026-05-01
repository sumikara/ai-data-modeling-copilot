# Model Providers

Supported provider modes: `mock`, `llm` (OpenAI), `gemini`, `anthropic`.

## Setup
- `OPENAI_API_KEY`
- `GEMINI_API_KEY`
- `ANTHROPIC_API_KEY`

Model defaults are in `config/models.yaml`.

## Benchmark usage
- `python scripts/run_benchmark.py --mode mock`
- `python scripts/run_benchmark.py --mode llm`
- `python scripts/run_benchmark.py --mode gemini`
- `python scripts/run_benchmark.py --mode anthropic`
- `python scripts/run_benchmark.py --mode all`

Provider modes without keys are skipped gracefully.

## Why multi-model
Multiple providers help compare reasoning consistency, calibration, and failure patterns.

## Governance
Human approval remains mandatory. Model outputs are evidence-assisted recommendations, not final modeling truth.
