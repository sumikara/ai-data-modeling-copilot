from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd

RAW_DATA_DIR = Path("data/raw")
SUPPORTED_ENCODINGS = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]


def _infer_table_name(file_path: Path) -> str:
    return file_path.stem.lower().strip().replace(" ", "_")


def _read_csv_with_fallbacks(file_path: Path) -> pd.DataFrame:
    last_error: Exception | None = None
    for encoding in SUPPORTED_ENCODINGS:
        try:
            return pd.read_csv(file_path, encoding=encoding)
        except Exception as exc:  # beginner-friendly broad handling
            last_error = exc
    raise ValueError(f"Failed to read {file_path} with supported encodings.") from last_error


def read_all_csv_files(raw_dir: Path = RAW_DATA_DIR) -> Dict[str, pd.DataFrame]:
    """Read all CSV files under data/raw and return {table_name: dataframe}."""
    if not raw_dir.exists():
        return {}

    tables: Dict[str, pd.DataFrame] = {}
    for file_path in sorted(raw_dir.glob("*.csv")):
        table_name = _infer_table_name(file_path)
        tables[table_name] = _read_csv_with_fallbacks(file_path)

    return tables
