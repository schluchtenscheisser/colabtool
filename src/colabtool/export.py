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

def _safe_col_width(s: pd.Series) -> int:
    if s is None or s.empty:
        return _DEF_FALLBACK
    try:
        lens = s.astype(str).str.len()
        q = pd.to_numeric(lens, errors="coerce").quantile(0.90)
        if not np.isfinite(q):
            return _DEF_FALLBACK
        w = int(q) + 2
        return max(_DEF_MIN, min(_DEF_MAX, w))
    except Exception:
        return _DEF_FALLBACK

def _coerce_for_excel(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for c in out.columns:
        s = out[c]
        if is_datetime64_any_dtype(s):
            out[c] = pd.to_datetime(s, errors="coerce")
            continue
        if is_categorical_dtype(s):
            out[c] = s.astype(str)
            continue
        if s.dtype == "object":
            out[c] = s.apply(lambda x: ", ".join(map(str, x)) if isinstance(x, (list, tuple, set)) else x)
    return out

def write_sheet(df: pd.DataFrame, sheet_name: str, writer) -> None:
    if df is None:
        df = pd.DataFrame()
    d2 = _coerce_for_excel(df)
    if d2.empty:
        d2 = pd.DataFrame({"info": [f"Keine Daten ({sheet_name})"]})

    d2.to_excel(writer, sheet_name=sheet_name, index=False)
    wb = writer.book
    ws = writer.sheets[sheet_name]

    nrows, ncols = d2.shape
    if ncols > 0:
        ws.autofilter(0, 0, max(0, nrows), max(0, ncols - 1))
        ws.freeze_panes(1, 1)

    for i, c in enumerate(d2.columns):
        ws.set_column(i, i, _safe_col_width(d2[c]))

    try:
        num_fmt = wb.add_format({"num_format": "0.00"})
        for i, c in enumerate(d2.columns):
            cl = str(c).lower()
            if any(k in cl for k in ["score", "beta", "z_"]) and is_numeric_dtype(d2[c]):
                ws.set_column(i, i, _safe_col_width(d2[c]), num_fmt)
            if cl.endswith("_pct") and is_numeric_dtype(d2[c]):
                ws.set_column(i, i, _safe_col_width(d2[c]), num_fmt)
    except Exception:
        pass

def write_meta_sheet(writer, meta: Dict[str, Any]) -> None:
    if not isinstance(meta, dict):
        meta = {"info": "no meta"}
    dfm = pd.DataFrame({"key": list(meta.keys()), "value": list(meta.values())})
    dfm = _coerce_for_excel(dfm)
    dfm.to_excel(writer, sheet_name="Meta", index=False)
    ws = writer.sheets["Meta"]
    nrows, ncols = dfm.shape
    if ncols > 0:
        ws.autofilter(0, 0, max(0, nrows), max(0, ncols - 1))
        ws.freeze_panes(1, 1)
    for i, c in enumerate(dfm.columns):
        ws.set_column(i, i, _safe_col_width(dfm[c]))

