from __future__ import annotations

from itertools import combinations
from typing import Any, Dict, List

import pandas as pd

ID_PATTERNS = ("id", "_id", "key", "code", "number", "num")


def detect_keys(df: pd.DataFrame, column_profiles: Dict[str, Dict[str, Any]]) -> Dict[str, List[Any]]:
    row_count = len(df)
    single_candidate_keys: List[str] = []

    for col, profile in column_profiles.items():
        if profile["unique_ratio"] == 1.0 and profile["null_ratio"] == 0.0:
            single_candidate_keys.append(col)

    composite_candidate_keys: List[List[str]] = []
    if not single_candidate_keys and row_count > 0:
        cols = list(df.columns)
        for c1, c2 in combinations(cols, 2):
            combo_unique = df[[c1, c2]].dropna().drop_duplicates().shape[0]
            if combo_unique == row_count:
                composite_candidate_keys.append([str(c1), str(c2)])

    possible_natural_keys: List[str] = []
    categorical_columns: List[str] = []

    for col, profile in column_profiles.items():
        name = col.lower()
        is_id_looking = any(token in name for token in ID_PATTERNS)

        if profile["unique_ratio"] >= 0.9 and profile["null_ratio"] <= 0.05 and not is_id_looking:
            possible_natural_keys.append(col)

        if profile["distinct_count"] <= 50 and profile["unique_ratio"] <= 0.2:
            categorical_columns.append(col)

    return {
        "candidate_primary_keys": single_candidate_keys + composite_candidate_keys,
        "possible_natural_keys": possible_natural_keys,
        "categorical_columns": categorical_columns,
    }
