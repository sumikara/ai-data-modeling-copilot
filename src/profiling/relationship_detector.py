from __future__ import annotations

from typing import Any, Dict, List

import pandas as pd


def _normalized_non_null_values(series: pd.Series) -> set[str]:
    return {str(v).strip().lower() for v in series.dropna().tolist()}


def detect_relationships(tables: Dict[str, pd.DataFrame]) -> Dict[str, List[Dict[str, Any]]]:
    """Detect simple relationship candidates across all tables."""
    table_names = sorted(tables.keys())
    relationships: Dict[str, List[Dict[str, Any]]] = {t: [] for t in table_names}

    for child_name in table_names:
        child_df = tables[child_name]
        for parent_name in table_names:
            if parent_name == child_name:
                continue
            parent_df = tables[parent_name]

            for child_col in child_df.columns:
                child_col_lower = str(child_col).lower()
                for parent_col in parent_df.columns:
                    parent_col_lower = str(parent_col).lower()

                    name_match = child_col_lower == parent_col_lower
                    id_pattern_match = child_col_lower.endswith("_id") and (
                        child_col_lower.replace("_id", "") in parent_name
                        or parent_col_lower.endswith("_id")
                        or parent_col_lower == "id"
                    )

                    if not (name_match or id_pattern_match):
                        continue

                    child_values = _normalized_non_null_values(child_df[child_col])
                    parent_values = _normalized_non_null_values(parent_df[parent_col])
                    if not child_values or not parent_values:
                        continue

                    overlap = child_values.intersection(parent_values)
                    overlap_ratio = round(len(overlap) / len(child_values), 6)

                    if overlap_ratio >= 0.5:
                        relationships[child_name].append(
                            {
                                "parent_table": parent_name,
                                "child_column": str(child_col),
                                "parent_column": str(parent_col),
                                "name_match": name_match,
                                "id_pattern_match": id_pattern_match,
                                "overlap_ratio": overlap_ratio,
                                "suggestion": f"{child_name}.{child_col} may reference {parent_name}.{parent_col}",
                            }
                        )

    return relationships
