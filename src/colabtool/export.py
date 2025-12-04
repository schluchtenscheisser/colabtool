from __future__ import annotations
from typing import Dict, Any
from .utilities import pd, np, logging
from pandas.api.types import (
    is_datetime64_any_dtype,
    is_categorical_dtype,
    is_numeric_dtype,
)

_DEF_MIN = 10
_DEF_MAX = 40
_DEF_FALLBACK = 12

EXPORT_PATH = "/content/drive/MyDrive/Colab results"


# -----------------------------------------------------
# Hilfsfunktionen für Spaltenformatierung
# -----------------------------------------------------
def _safe_col_width(s: pd.Series) -> int:
    if s is None or s.empty:
        return _DEF_FALLBACK
    if is_numeric_dtype(s):
        formatted = [len(f"{v:.2f}") for v in s if pd.notna(v)]
        if not formatted:
            return _DEF_FALLBACK
        return max(_DEF_MIN, min(_DEF_MAX, int(np.nanmean(formatted) + 2)))
    if is_datetime64_any_dtype(s):
        return _DEF_MAX
    if is_categorical_dtype(s):
        return max(_DEF_MIN, min(_DEF_MAX, s.astype(str).str.len().max()))
    return max(_DEF_MIN, min(_DEF_MAX, s.astype(str).str.len().max()))


# -----------------------------------------------------
# Spalten-Reihenfolge (fixiert Score-Spalten frühzeitig)
# -----------------------------------------------------
def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
    fixed_order = [
        "id", "symbol", "name", "market_cap",
        "score_global", "score_segment", "early_score",
        "total_volume", "Kategorie", "Segment"
    ]
    available = [col for col in fixed_order if col in df.columns]
    remaining = [col for col in df.columns if col not in available]
    return df[available + remaining]


# -----------------------------------------------------
# Haupt-Exportsheet
# -----------------------------------------------------
def write_sheet(df: pd.DataFrame, name: str, writer) -> None:
    df = df.copy()
    df = reorder_columns(df)

    # Sicherstellen, dass Score-Spalten existieren
    required_cols = ["score_global", "score_segment", "early_score"]
    for col in required_cols:
        if col not in df.columns:
            logging.warning(f"⚠️ Spalte {col} fehlt im Export – wird mit NaN ergänzt.")
            df[col] = np.nan

    # Sortierung nach globalem Score, falls vorhanden
    if "score_global" in df.columns:
        try:
            df = df.sort_values("score_global", ascending=False)
        except Exception as ex:
            logging.warning(f"⚠️ Sortierung nach score_global fehlgeschlagen: {ex}")

    df.to_excel(writer, sheet_name=name, index=False)
    worksheet = writer.sheets[name]

    fmt_thousands = None
    fmt_percent = None
    try:
        if hasattr(writer, "book") and hasattr(writer.book, "add_format"):
            fmt_thousands = writer.book.add_format({"num_format": "#,##0", "align": "right"})
            fmt_percent = writer.book.add_format({"num_format": "0.00%", "align": "right"})
    except Exception as ex:
        print(f"⚠️ Formatierungswarnung (non-fatal): {ex}")

    use_xlsxwriter = hasattr(worksheet, "set_column")

    for idx, col in enumerate(df.columns):
        width = _safe_col_width(df[col])
        if use_xlsxwriter:
            if col in ("market_cap", "total_volume"):
                worksheet.set_column(idx, idx, width, fmt_thousands)
            elif col in ("mom_7d_pct", "mom_30d_pct"):
                worksheet.set_column(idx, idx, width, fmt_percent)
            else:
                worksheet.set_column(idx, idx, width)
        else:
            try:
                col_letter = worksheet.cell(row=1, column=idx + 1).column_letter
                worksheet.column_dimensions[col_letter].width = width
            except Exception as ex:
                print(f"⚠️ Spaltenbreite konnte nicht gesetzt werden ({col}): {ex}")


# -----------------------------------------------------
# Meta-Sheet
# -----------------------------------------------------
def write_meta_sheet(writer, meta: Dict[str, Any]) -> None:
    meta_df = pd.DataFrame.from_dict(meta, orient="index", columns=["Value"])
    meta_df.reset_index(inplace=True)
    meta_df.columns = ["Key", "Value"]
    meta_df.to_excel(writer, sheet_name="Meta", index=False)
    worksheet = writer.sheets["Meta"]
    worksheet.set_column(0, 0, 40)
    worksheet.set_column(1, 1, 80)


# -----------------------------------------------------
# Vollständiger Excel-Export (inkl. Zusatz-Sheets)
# -----------------------------------------------------
def create_full_excel_export(
    df: pd.DataFrame,
    output_path: str,
    extra_sheets: dict[str, pd.DataFrame] | None = None
) -> None:
    """
    Erstellt vollständigen Excel-Export mit Rankings, FullData und optionalen Zusatz-Sheets (z. B. Backtest).
    """
    logging.info(f"📊 Erzeuge Excel mit Rankings → {output_path}")

    # Sicherstellen, dass Score-Spalten existieren
    required_cols = ["score_global", "score_segment", "early_score"]
    for col in required_cols:
        if col not in df.columns:
            logging.warning(f"⚠️ Spalte {col} fehlt in DataFrame – wird mit NaN ergänzt.")
            df[col] = np.nan

    # Rankings
    top25_global = df.sort_values("score_global", ascending=False).head(25)
    top10_hidden = df[df["market_cap"] <= 150_000_000].sort_values("score_global", ascending=False).head(10)
    top10_emerging = df[
        (df["market_cap"] > 150_000_000) & (df["market_cap"] <= 500_000_000)
    ].sort_values("score_global", ascending=False).head(10)
    top25_early = df.sort_values("early_score", ascending=False).head(25)

    # Excel exportieren
    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
        write_sheet(top25_global, "Top25_Global", writer)
        write_sheet(top10_hidden, "Top10_HiddenGem", writer)
        write_sheet(top10_emerging, "Top10_Emerging", writer)
        write_sheet(top25_early, "Top25_EarlySignals", writer)
        write_sheet(df, "FullData", writer)
        write_meta_sheet(writer, {"generated": pd.Timestamp.now()})

        # 🔹 Zusatz-Sheets (z. B. Backtest)
        if extra_sheets:
            for sheet_name, sheet_df in extra_sheets.items():
                if sheet_df is not None and not sheet_df.empty:
                    write_sheet(sheet_df, sheet_name, writer)

    logging.info(f"✅ Excel erfolgreich exportiert: {output_path}")
