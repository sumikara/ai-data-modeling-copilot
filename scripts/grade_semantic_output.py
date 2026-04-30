import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.agents.semantic_profiling_agent import run_semantic_profiling
from src.evaluation.semantic_output_grader import grade_semantic_output
from src.retrieval.knowledge_retriever import retrieve_relevant_context

REPORT_PATH = Path("test_outputs/evaluation/SEMANTIC_OUTPUT_GRADING_REPORT.md")


def main() -> None:
    output = run_semantic_profiling("test_inputs/semantic_profiling/transaction_like_profile.json", mode="mock")

    retrieval_query = "grain decision fact vs dimension SCD rules transaction dataset profiling duplicates keys"
    retrieved_context = retrieve_relevant_context(retrieval_query)

    grade = grade_semantic_output(output, retrieved_context=retrieved_context)
    print(json.dumps(grade, indent=2, ensure_ascii=False))

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    report = (
        "# SEMANTIC OUTPUT GRADING REPORT\n\n"
        "## Mode\n- `mock`\n\n"
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
    REPORT_PATH.write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
