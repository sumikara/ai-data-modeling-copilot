import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.agents.semantic_profiling_agent import run_semantic_profiling
from src.validation.semantic_output_validator import validate_semantic_output

REPORT_PATH = Path("test_outputs/semantic_profiling/SEMANTIC_OUTPUT_VALIDATION_REPORT.md")


def main() -> None:
    payload = run_semantic_profiling(
        "test_inputs/semantic_profiling/transaction_like_profile.json",
        mode="mock",
    )
    result = validate_semantic_output(payload)

    print(json.dumps(result, indent=2, ensure_ascii=False))

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report = (
        "# SEMANTIC OUTPUT VALIDATION REPORT\n\n"
        "## Input\n\n"
        "- Source: `run_semantic_profiling(..., mode=\"mock\")`\n\n"
        "## Validation Result\n\n"
        "```json\n"
        f"{json.dumps(result, indent=2, ensure_ascii=False)}\n"
        "```\n"
    )
    REPORT_PATH.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
