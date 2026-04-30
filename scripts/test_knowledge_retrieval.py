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


def main() -> None:
    for idx, query in enumerate(QUERIES, start=1):
        context = retrieve_relevant_context(query)
        sources = parse_sources(context)

        print("=" * 90)
        print(f"Query {idx}: {query}")
        print("Top retrieved sources:")
        if sources:
            for s in sources:
                print(f"- {s}")
        else:
            print("- (none)")

        preview = context[:500]
        print("\nContext preview (first 500 chars):")
        print(preview)
        print()


if __name__ == "__main__":
    main()
