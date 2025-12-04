"""
validation.py — Preflight-Schema-Check für Snapshot-Daten

Stellt sicher, dass DataFrames die erwartete Struktur haben.
Fehlende Spalten werden automatisch ergänzt, Typen geprüft.
"""

import pandas as pd
import logging
from typing import Dict, Type


def ensure_schema(df: pd.DataFrame, schema_map: Dict[str, Type]) -> pd.DataFrame:
    """
    Ensures that the given DataFrame matches the expected schema.
    - Adds missing columns with default values
    - Coerces datatypes if possible
    - Logs any inconsistencies
    """
    if df is None or not isinstance(df, pd.DataFrame):
        raise ValueError("ensure_schema: input is not a valid DataFrame")

    for col, dtype in schema_map.items():
        if col not in df.columns:
            logging.warning(f"[ensure_schema] Adding missing column: {col}")
            # assign sensible default based on dtype
            if dtype in (float, int):
                df[col] = 0
            elif dtype is bool:
                df[col] = False
            else:
                df[col] = None

        # type coercion (non-fatal)
        try:
            df[col] = df[col].astype(dtype, errors="ignore")
        except Exception as e:
            logging.warning(f"[ensure_schema] Failed to coerce {col} to {dtype}: {e}")

    # remove unexpected columns (optional, keep for audit)
    extra_cols = [c for c in df.columns if c not in schema_map]
    if extra_cols:
        logging.info(f"[ensure_schema] Extra columns present: {extra_cols}")

    return df


def validate_required_columns(df: pd.DataFrame, required: list[str]) -> None:
    """Raises ValueError if required columns are missing."""
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def validate_nonempty(df: pd.DataFrame, min_rows: int = 1) -> None:
    """Ensures that the DataFrame has at least `min_rows`."""
    if df.empty or len(df) < min_rows:
        raise ValueError(f"DataFrame has insufficient rows: {len(df)} < {min_rows}")
