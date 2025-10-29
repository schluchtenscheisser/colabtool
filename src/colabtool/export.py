from __future__ import annotations
from typing import Dict, Any
from .utils import pd, np, logging
from pandas.api.types import (
    is_datetime64_any_dtype,
    is_categorical_dtype,
    is_numeric_dtype,
)

_DEF_MIN = 10
_DEF_MAX = 40
_DEF_FALLBACK = 12

EXPORT_PATH = "/content/drive/MyDrive/Colab results"

def _safe_col_width(s: pd.Series) -> int:
    if s is None or s.empty:
        return _DEF_FALLBACK
    if is_numeric_dtype(s):
        return max(_DEF_MIN, min(_DEF_MAX, int(np.nanmean([len(f"{v:.2f}") for v in s if pd.notna(v)]) + 2)))
    if is_datetime64_any_dtype(s):
        return _DEF_MAX
    if is_categorical_dtype(s):
        return max(_DEF_MIN, min(_DEF_MAX, s.astype(str).str.len().max()))
    return max(_DEF_MIN, min(_DEF_MAX, s.astype(str).str.len().max()))

def write_sheet(df: pd.DataFrame, name: str, writer) -> None:
    df = df.copy()
    try:
        df = df.sort_values("early_score", ascending=False)
    except Exception:
        pass

    # Konvertierung für lesbare Ausgabe
    for col in ["mom_7d_pct", "mom_30d_pct"]:
        if col in df.columns:
            df[col] = df[col].map(lambda x: f"{x:.2f}%" if pd.notna(x) else "")

    df.to_excel(writer, sheet_name=name, index=False)
    worksheet = writer.sheets[name]
    for i, col in enumerate(df.columns):
        width = _safe_col_width(df[col])
        worksheet.set_column(i, i, width)

def write_meta_sheet(writer, meta: Dict[str, Any]) -> None:
    meta_df = pd.DataFrame.from_dict(meta, orient="index", columns=["Value"])
    meta_df.reset_index(inplace=True)
    meta_df.columns = ["Key", "Value"]
    meta_df.to_excel(writer, sheet_name="Meta", index=False)
    worksheet = writer.sheets["Meta"]
    worksheet.set_column(0, 0, 40)
    worksheet.set_column(1, 1, 80)
