# API Key Setup for Semantic Profiling

This project supports two execution modes for semantic profiling:

- **mock mode**: no API key needed
- **llm mode**: requires `OPENAI_API_KEY`

## Set the environment variable locally

### Linux/macOS

```bash
export OPENAI_API_KEY="your_key_here"
```

### Windows PowerShell

```powershell
$env:OPENAI_API_KEY="your_key_here"
```

## Run semantic profiling

```bash
python scripts/run_semantic_profiling.py
```

## Security warnings

- Never commit real API keys.
- Keep `.env` out of Git.
- Use GitHub Secrets for GitHub Actions.
- Rotate the key immediately if exposed.

## Troubleshooting

- If you see `Missing OPENAI_API_KEY`, `llm` mode cannot run.
- `mock` mode should still run successfully without an API key.
