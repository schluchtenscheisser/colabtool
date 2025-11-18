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
        formatted = [len(f"{v:,.2f}") for v in s if pd.notna(v)]
        if not formatted:
            return _DEF_FALLBACK
        return max(_DEF_MIN, min(_DEF_MAX, int(np.nanmean(formatted) + 2)))
    if is_datetime64_any_dtype(s):
        return _DEF_MAX
    if is_categorical_dtype(s):
        return max(_DEF_MIN, min(_DEF_MAX, s.astype(str).str.len().max()))
    return max(_DEF_MIN, min(_DEF_MAX, s.astype(str).str.len().max()))

def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
    fixed_order = [
        "id", "symbol", "name", "market_cap", "score_global",
        "total_volume", "Kategorie", "Segment", "score_segment"
    ]
    available = [col for col in fixed_order if col in df.columns]
    remaining = [col for col in df.columns if col not in available]
    return df[available + remaining]

def write_sheet(df: pd.DataFrame, name: str, writer) -> None:
    df = df.copy()
    df = reorder_columns(df)
    if "score_global" in df.columns:
        df = df.sort_values("score_global", ascending=False)

    df.to_excel(writer, sheet_name=name, index=False)
    worksheet = writer.sheets[name]

    # Formate
    fmt_thousands = writer.book.add_format({"num_format": "#,##0", "align": "right"})
    fmt_percent = writer.book.add_format({"num_format": "0.00%", "align": "right"})

    for idx, col in enumerate(df.columns):
        width = _safe_col_width(df[col])
        if col in ("market_cap", "total_volume"):
            worksheet.set_column(idx, idx, width, fmt_thousands)
        elif col in ("mom_7d_pct", "mom_30d_pct"):
            worksheet.set_column(idx, idx, width, fmt_percent)
        else:
            worksheet.set_column(idx, idx, width)

def write_meta_sheet(writer, meta: Dict[str, Any]) -> None:
    meta_df = pd.DataFrame.from_dict(meta, orient="index", columns=["Value"])
    meta_df.reset_index(inplace=True)
    meta_df.columns = ["Key", "Value"]
    meta_df.to_excel(writer, sheet_name="Meta", index=False)
    worksheet = writer.sheets["Meta"]
    worksheet.set_column(0, 0, 40)
    worksheet.set_column(1, 1, 80)

def create_full_excel_export(df: pd.DataFrame, output_path: str) -> None:
    """
    Erstellt vollständigen Excel-Export mit Top-Listen und Metadaten.
    """
    print(f"📊 Erzeuge Excel mit Rankings → {output_path}")

    # Top25 Global nach Score
    top25_global = df.sort_values("score_global", ascending=False).head(25)

    # Top10 Hidden Gems (MarketCap ≤ 150 Mio)
    top10_hidden = df[df["market_cap"] <= 150_000_000].sort_values("score_global", ascending=False).head(10)

    # Top10 Emerging (150–500 Mio)
    top10_emerging = df[(df["market_cap"] > 150_000_000) & (df["market_cap"] <= 500_000_000)].sort_values("score_global", ascending=False).head(10)

    # Top25 Early Signals
    top25_early = df.sort_values("early_score", ascending=False).head(25)

    # Writer öffnen
    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
        write_sheet(top25_global, "Top25_Global", writer)
        write_sheet(top10_hidden, "Top10_HiddenGem", writer)
        write_sheet(top10_emerging, "Top10_Emerging", writer)
        write_sheet(top25_early, "Top25_EarlySignals", writer)
        write_sheet(df, "FullData", writer)
        write_meta_sheet(writer, {"generated": pd.Timestamp.now()})

    print(f"✅ Excel exportiert: {output_path}")

