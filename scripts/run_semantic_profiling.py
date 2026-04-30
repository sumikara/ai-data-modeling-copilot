import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.agents.semantic_profiling_agent import run_semantic_profiling


def main() -> None:
    fixture = "test_inputs/semantic_profiling/transaction_like_profile.json"

    for mode in ("mock", "llm", "gemini"):
        print(f"\n=== Running semantic profiling in mode={mode} ===")
        result = run_semantic_profiling(fixture, mode=mode)
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
