import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.agents.semantic_profiling_agent import run_semantic_profiling
from src.evaluation.semantic_output_grader import grade_semantic_output
from src.retrieval.knowledge_retriever import retrieve_relevant_context
from src.runtime.run_trace import append_trace_event, create_run_id, write_run_trace


VALID_MODES = {"mock", "gemini"}
INPUT_PATH = "test_inputs/semantic_profiling/transaction_like_profile.json"


def build_report_path(mode: str) -> Path:
    return Path(f"test_outputs/evaluation/SEMANTIC_OUTPUT_GRADING_REPORT_{mode}.md")


def parse_retrieved_sources(context: str) -> list[str]:
    return re.findall(r"^### Source: (.+)$", context, flags=re.MULTILINE)


def main() -> None:
    parser = argparse.ArgumentParser(description="Grade semantic profiling output")
    parser.add_argument("--mode", choices=sorted(VALID_MODES), default="mock", help="Execution mode: mock or gemini")
    args = parser.parse_args()
    mode = args.mode

    run_id = create_run_id()
    started_at = datetime.now(timezone.utc).isoformat()

    retrieval_query = "grain decision fact vs dimension SCD rules transaction dataset profiling duplicates keys"
    retrieved_context = retrieve_relevant_context(retrieval_query)
    retrieved_sources = parse_retrieved_sources(retrieved_context)

    trace = {
        "run_id": run_id,
        "timestamp": started_at,
        "mode": mode,
        "input_path": INPUT_PATH,
        "retrieved_context_sources": retrieved_sources,
        "events": [],
    }
    write_run_trace(run_id, trace)
    append_trace_event(run_id, "retrieval_completed", {"source_count": len(retrieved_sources), "sources": retrieved_sources})

    payload = run_semantic_profiling(INPUT_PATH, mode=mode)
    append_trace_event(run_id, "semantic_profiling_completed", {"has_error": bool(isinstance(payload, dict) and payload.get("error"))})

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
        f"## Run ID\n- `{run_id}`\n\n"
        f"## Mode\n- `{mode}`\n\n"
        f"## Input Path\n- `{INPUT_PATH}`\n\n"
        "## Retrieval Query\n"
        f"- `{retrieval_query}`\n\n"
        "## Retrieved Context Sources\n"
        + "\n".join(f"- `{s}`" for s in retrieved_sources)
        + "\n\n"
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

    append_trace_event(
        run_id,
        "grading_completed",
        {
            "semantic_output_report_path": "test_outputs/semantic_profiling/ACTUAL_SEMANTIC_OUTPUT.md",
            "grading_report_path": str(report_path),
            "overall_score": grade.get("overall_score"),
            "passed": grade.get("passed"),
            "critical_failures": grade.get("critical_failures", []),
            "errors": grade.get("execution_error", {}),
        },
    )


if __name__ == "__main__":
    main()
