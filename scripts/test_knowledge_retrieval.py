import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.retrieval.knowledge_retriever import retrieve_relevant_context

QUERIES = [
    "grain decision fact dimension transaction dataset",
    "SCD type 2 natural key surrogate key customer attributes",
    "source triplet lineage source_system source_table source_id",
    "default row unknown member null foreign key",
    "partitioning fact table monthly refresh performance",
]


def parse_sources(context: str) -> list[str]:
    return re.findall(r"^### Source: (.+)$", context, flags=re.MULTILINE)


def parse_scores_and_reasons(context: str) -> list[tuple[str, str]]:
    scores = re.findall(r"^score=(.+)$", context, flags=re.MULTILINE)
    reasons = re.findall(r"^why_selected=(.+)$", context, flags=re.MULTILINE)
    length = min(len(scores), len(reasons))
    return list(zip(scores[:length], reasons[:length]))


def main() -> None:
    for idx, query in enumerate(QUERIES, start=1):
        context = retrieve_relevant_context(query)
        sources = parse_sources(context)
        scored = parse_scores_and_reasons(context)

        print("=" * 90)
        print(f"Query {idx}: {query}")
        print("Top retrieved sources:")
        if sources:
            for i, s in enumerate(sources):
                print(f"- {s}")
                if i < len(scored):
                    score, why = scored[i]
                    print(f"  score: {score}")
                    print(f"  why_selected: {why}")
        else:
            print("- (none)")

        preview = context[:500]
        print("\nContext preview (first 500 chars):")
        print(preview)
        print()


if __name__ == "__main__":
    main()
