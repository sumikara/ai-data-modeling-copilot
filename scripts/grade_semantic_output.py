import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.agents.semantic_profiling_agent import run_semantic_profiling
from src.evaluation.semantic_output_grader import grade_semantic_output
from src.retrieval.knowledge_retriever import retrieve_relevant_context


VALID_MODES = {"mock", "gemini"}


def build_report_path(mode: str) -> Path:
    return Path(f"test_outputs/evaluation/SEMANTIC_OUTPUT_GRADING_REPORT_{mode}.md")


def main() -> None:
    parser = argparse.ArgumentParser(description="Grade semantic profiling output")
    parser.add_argument("--mode", choices=sorted(VALID_MODES), default="mock", help="Execution mode: mock or gemini")
    args = parser.parse_args()
    mode = args.mode

    retrieval_query = "grain decision fact vs dimension SCD rules transaction dataset profiling duplicates keys"
    retrieved_context = retrieve_relevant_context(retrieval_query)

    payload = run_semantic_profiling("test_inputs/semantic_profiling/transaction_like_profile.json", mode=mode)

    if isinstance(payload, dict) and payload.get("error"):
        grade = {
            "overall_score": 0,
            "passed": False,
            "checks": [],
            "critical_failures": [f"semantic_profiling_execution_failed: {payload.get('error')}"],
            "recommendations": [
                "Resolve provider/API issues (credentials, quota, availability) and rerun grading.",
                "Use --mode mock for deterministic local grading when provider is unavailable.",
            ],
            "execution_error": payload,
        }
    else:
        grade = grade_semantic_output(payload, retrieved_context=retrieved_context)

    print(json.dumps(grade, indent=2, ensure_ascii=False))

    report_path = build_report_path(mode)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report = (
        f"# SEMANTIC OUTPUT GRADING REPORT ({mode})\n\n"
        f"## Mode\n- `{mode}`\n\n"
        "## Retrieval Query\n"
        f"- `{retrieval_query}`\n\n"
        "## Retrieved Context (truncated)\n\n"
        "```text\n"
        f"{retrieved_context[:2000]}\n"
        "```\n\n"
        "## Grading Result\n\n"
        "```json\n"
        f"{json.dumps(grade, indent=2, ensure_ascii=False)}\n"
        "```\n"
    )
    report_path.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
