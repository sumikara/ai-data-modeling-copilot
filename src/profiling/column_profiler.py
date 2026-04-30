from __future__ import annotations

from typing import Any, Dict

import pandas as pd


def _safe_ratio(numerator: int, denominator: int) -> float:
    if denominator == 0:
        return 0.0
    return round(numerator / denominator, 6)


def _to_serializable(value: Any) -> Any:
    if pd.isna(value):
        return None
    if hasattr(value, "isoformat"):
        try:
            return value.isoformat()
        except Exception:
            return str(value)
    return value if isinstance(value, (str, int, float, bool)) else str(value)


def profile_columns(df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """Profile each column in a deterministic and beginner-friendly way."""
    column_profiles: Dict[str, Dict[str, Any]] = {}
    row_count = len(df)

    for column in df.columns:
        series = df[column]
        non_null = series.dropna()

        null_count = int(series.isna().sum())
        distinct_count = int(non_null.nunique(dropna=True))
        duplicate_value_count = max(int(non_null.size - distinct_count), 0)

        numeric_parsed = pd.to_numeric(non_null, errors="coerce")
        date_parsed = pd.to_datetime(non_null, errors="coerce")

        min_value = None
        max_value = None
        try:
            if not non_null.empty:
                min_value = _to_serializable(non_null.min())
                max_value = _to_serializable(non_null.max())
        except Exception:
            min_value = None
            max_value = None

        top_values_raw = non_null.value_counts().head(5)
        top_values = [
            {"value": _to_serializable(idx), "count": int(count)}
            for idx, count in top_values_raw.items()
        ]

        sample_values = [_to_serializable(v) for v in non_null.head(5).tolist()]

        column_profiles[str(column)] = {
            "dtype": str(series.dtype),
            "row_count": int(row_count),
            "null_count": null_count,
            "null_ratio": _safe_ratio(null_count, row_count),
            "distinct_count": distinct_count,
            "unique_ratio": _safe_ratio(distinct_count, row_count),
            "duplicate_value_count": duplicate_value_count,
            "sample_values": sample_values,
            "min_value": min_value,
            "max_value": max_value,
            "numeric_parse_success_ratio": _safe_ratio(int(numeric_parsed.notna().sum()), int(non_null.size)),
            "date_parse_success_ratio": _safe_ratio(int(date_parsed.notna().sum()), int(non_null.size)),
            "top_values": top_values,
        }

    return column_profiles
