"""
Run Snapshot Mode – Vereinfachte Pipeline (CMC → MEXC → Feature → Scoring → Backtest → Export)
Nur regulärer Snapshot-Lauf, keine Modi.
"""

import logging
from datetime import datetime
from pathlib import Path
import pandas as pd

from colabtool.data_sources_cmc import fetch_cmc_markets, map_mexc_pairs
from colabtool.data_sources import get_alias_seed
from colabtool.pre_universe import apply_pre_universe_filters
from colabtool.features import compute_feature_block
from colabtool.breakout import compute_breakout_for_ids
from colabtool.buzz import add_buzz_metrics_for_candidates
from colabtool.scores import score_block, compute_early_score
from colabtool.backtest import backtest_on_snapshot
from colabtool.export_helpers import make_fulldata
from colabtool.export import create_full_excel_export
from colabtool.utils.validation import ensure_schema

# ---------------------------------------------------------------------------
# Logging Setup
# ---------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


# ---------------------------------------------------------------------------
# Hilfsfunktion: Score-Validierung
# ---------------------------------------------------------------------------
def validate_scores(df: pd.DataFrame) -> None:
    required_cols = ["early_score", "breakout_score"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"⚠️ Fehlende Score-Spalten: {missing}")

    nan_counts = df[required_cols].isna().sum()
    if nan_counts.any():
        logging.warning(f"NaN-Werte in Scores: {nan_counts.to_dict()}")
        df.dropna(subset=required_cols, inplace=True)

    valid_count = len(df)
    if valid_count < 100:
        raise ValueError(f"⚠️ Zu wenige valide Scores: {valid_count}")

    logging.info(f"✅ Score-Validierung bestanden ({valid_count} valide Zeilen)")


# ---------------------------------------------------------------------------
# Hauptfunktion: Snapshot-Pipeline
# ---------------------------------------------------------------------------
def run_snapshot() -> Path:
    """Führt den vollständigen Snapshot-Lauf aus (CMC → MEXC → Feature → Scoring → Backtest → Export)."""

    ASOF_DATE = datetime.today().strftime("%Y%m%d")
    snapshot_dir = Path("snapshots") / ASOF_DATE
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    logging.info(f"🚀 Starte Snapshot-Lauf für {ASOF_DATE}")

    # 1️⃣ Universe laden (CMC)
    df = fetch_cmc_markets(pages=8, limit=250)
    logging.info(f"✅ [CMC] {len(df)} Coins geladen, Columns: {list(df.columns)}")

    # 2️⃣ MEXC Mapping
    logging.info("[TRACE] Starte map_mexc_pairs() in Snapshot-Pipeline")
    try:
        df = map_mexc_pairs(df)
        hits = df["mexc_pair"].notna().sum()
        logging.info(f"[MEXC] ✅ Mapping abgeschlossen ({hits} Treffer von {len(df)}).")
        if hits == 0:
            logging.warning("[MEXC] ⚠️ Keine Treffer beim Mapping – prüfe API oder Symbolabgleich.")
    except Exception as e:
        logging.error(f"[MEXC] ❌ Fehler beim Mapping: {e}", exc_info=True)

    logging.info(f"[MEXC] 🔍 Vor Filterung: {df['mexc_pair'].notna().sum()} Coins mit MEXC-Paar")

    # 3️⃣ Schema-Validierung
    SCHEMA_MAP = {
        "id": str,
        "symbol": str,
        "market_cap": float,
        "total_volume": float,
        "early_score": float,
        "breakout_score": float,
        "mexc_pair": str,
        "ath": float,
        "current_price": float,
    }
    df = ensure_schema(df, SCHEMA_MAP)
    logging.info(f"[TRACE] Nach ensure_schema: {len(df)} Zeilen, Columns: {list(df.columns)}")

    # 4️⃣ Feature- & Momentum-Berechnung
    logging.info(f"[TRACE] Vor apply_pre_universe_filters: {len(df)} Zeilen")
    df = apply_pre_universe_filters(df)
    logging.info(f"✅ apply_pre_universe_filters: {len(df)} nach Filtern")

    df = compute_feature_block(df)
    logging.info("✅ compute_feature_block abgeschlossen")

    cand_ids = df["id"].tolist()
    df = compute_breakout_for_ids(df, cand_ids)
    logging.info("✅ compute_breakout_for_ids abgeschlossen")

    df = add_buzz_metrics_for_candidates(df)
    logging.info("✅ add_buzz_metrics_for_candidates abgeschlossen")

    # 5️⃣ Scoring
    logging.info(f"[TRACE] Vor Scoring: {len(df)} Zeilen")
    df = score_block(df)
    df = compute_early_score(df)
    logging.info("✅ Scores & Early Score berechnet")

    # 6️⃣ Validierung & Backtest
    validate_scores(df)
    backtest_results = backtest_on_snapshot(df, top_k=20, horizons=[20, 40, 60])
    logging.info(f"✅ Backtest abgeschlossen ({len(backtest_results)} Zeilen)")

    # 7️⃣ Export
    full_df = make_fulldata(df)
    export_filename = f"{ASOF_DATE}_fullsnapshot.xlsx"
    export_path = snapshot_dir / export_filename

    logging.info(f"📦 Erzeuge Excel → {export_path}")
    create_full_excel_export(full_df, export_path, extra_sheets={"Backtest": backtest_results})

    # 8️⃣ CSV-Exports
    cg_path = snapshot_dir / "cmc_markets.csv"
    mexc_path = snapshot_dir / "mexc_pairs.csv"
    alias_path = snapshot_dir / "seed_alias.csv"

    df.to_csv(cg_path, index=False)
    logging.info(f"✅ cmc_markets.csv gespeichert ({cg_path})")

    if "mexc_pair" in df.columns:
        df[["id", "symbol", "mexc_pair"]].to_csv(mexc_path, index=False)
        logging.info(f"✅ mexc_pairs.csv gespeichert ({mexc_path})")

    if not alias_path.exists():
        seed_alias = get_alias_seed()
        seed_alias.to_csv(alias_path, index=False)
        logging.info(f"⚠️ seed_alias.csv neu erstellt → {alias_path}")

    logging.info(f"🎯 Snapshot abgeschlossen → {export_path}")
    return export_path


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    logging.info("🚀 Starte regulären Snapshot-Lauf (kein Modus-System mehr aktiv).")
    run_snapshot()
