from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from .column_profiler import profile_columns
from .csv_reader import read_all_csv_files
from .key_detector import detect_keys
from .relationship_detector import detect_relationships

OUTPUT_DIR = Path("outputs/profiles")


def _write_json(path: Path, content: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(content, f, indent=2, ensure_ascii=False)


def _write_summary_markdown(path: Path, reports: List[Dict[str, Any]]) -> None:
    lines = ["# Profile Summary", ""]

    if not reports:
        lines.append("No CSV files found under `data/raw/`.")
    else:
        for report in reports:
            lines.extend(
                [
                    f"## Table: {report['table_name']}",
                    f"- Row count: {report['row_count']}",
                    f"- Column count: {report['column_count']}",
                    f"- Candidate primary keys: {report['candidate_primary_keys']}",
                    f"- Possible natural keys: {report['possible_natural_keys']}",
                    f"- Categorical columns: {report['categorical_columns']}",
                    f"- Relationship candidates: {len(report['relationship_candidates'])}",
                    "",
                ]
            )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def run_profiling() -> List[Dict[str, Any]]:
    tables = read_all_csv_files()
    relationships = detect_relationships(tables)

    reports: List[Dict[str, Any]] = []

    for table_name, df in tables.items():
        columns = profile_columns(df)
        key_info = detect_keys(df, columns)

        report: Dict[str, Any] = {
            "table_name": table_name,
            "row_count": int(len(df)),
            "column_count": int(len(df.columns)),
            "columns": columns,
            "candidate_primary_keys": key_info["candidate_primary_keys"],
            "possible_natural_keys": key_info["possible_natural_keys"],
            "categorical_columns": key_info["categorical_columns"],
            "relationship_candidates": relationships.get(table_name, []),
            "profiling_notes": [
                "Heuristics-based deterministic profiling run completed.",
                "Review candidate keys/relationships before modeling decisions.",
            ],
        }

        output_path = OUTPUT_DIR / f"{table_name}_profile.json"
        _write_json(output_path, report)
        reports.append(report)

    _write_summary_markdown(OUTPUT_DIR / "profile_summary.md", reports)
    return reports


if __name__ == "__main__":
    try:
        generated = run_profiling()
        print(f"Generated {len(generated)} profile report(s) in {OUTPUT_DIR}.")
    except Exception as exc:
        print(f"Profiling failed: {exc}")
        raise
