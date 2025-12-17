"""
Run Snapshot Mode → vollständige Early-Signal-Pipeline mit Backtest und Export.
Erzeugt snapshots/YYYYMMDD/ mit allen Daten und Excel-Dateien.
Unterstützt Standard-, Fast- und Offline-Modus.
"""

import os
import argparse
import logging
from datetime import datetime
from pathlib import Path
import pandas as pd

logging.info("🟢 Snapshot Mode nutzt CoinMarketCap als Primärquelle.")

# ENV-Vars & API-Verhalten (Standard-Defaults)
os.environ.update({
    "ENABLE_PIT_CATEGORIES": "1",
    "ENABLE_PIT_MEXC": "1",
    "ENABLE_PIT_ALIAS": "1",
    "CG_FORCE_FREE": "1",
    "CG_SKIP_AFTER_429": "1",
    "CG_MAX_ATTEMPTS": "1",
    "CG_MIN_INTERVAL_S": "3.5",
    "CG_CATS_TIME_BUDGET_S": "120",
    "PROVIDERS_CATS_TIME_BUDGET_S": "90",
    "REQUIRE_MEXC": "1",
    "LIGHT_BREAKOUT_ALL": "0",
    "BUZZ_HALF_LIFE_H": "48",
})

# Core-Imports
from colabtool.data_sources_cmc import fetch_cmc_markets, map_mexc_pairs, map_tvl
from colabtool.data_sources import get_alias_seed  # bleibt erhalten
from colabtool.pre_universe import apply_pre_universe_filters
from colabtool.features import compute_feature_block
from colabtool.breakout import compute_breakout_for_ids
from colabtool.buzz import add_buzz_metrics_for_candidates
from colabtool.scores import score_block, compute_early_score
from colabtool.backtest import backtest_on_snapshot
from colabtool.export_helpers import make_fulldata
from colabtool.export import create_full_excel_export
from colabtool.utils.validation import ensure_schema


# --------------------------------------------------
# Logging-Setup
# --------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


# --------------------------------------------------
# Hilfsfunktion: Score-Validierung
# --------------------------------------------------
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


# --------------------------------------------------
# Hauptfunktion: Snapshot Pipeline
# --------------------------------------------------
def run_snapshot(mode: str = "standard", offline: bool = False) -> Path:
    """
    Führt den vollständigen Snapshot-Lauf aus.
    mode: 'standard' | 'fast' | 'offline'
    offline=True erzwingt synthetische Mock-Daten (keine API-Aufrufe)
    """

    ASOF_DATE = datetime.today().strftime("%Y%m%d")
    snapshot_dir = Path("snapshots") / ASOF_DATE
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    effective_mode = "offline" if offline or mode == "offline" else mode
    logging.info(f"🚀 Starte Snapshot-Lauf ({effective_mode}) für {ASOF_DATE}")

    # ------------------------------
    # 1️⃣ Universe laden (API oder Mock)
    # ------------------------------
    # if effective_mode == "offline":
    #     logging.info("⚙️ OFFLINE-MODUS: Verwende synthetische Mock-Daten (kein API-Zugriff).")
    #     df = pd.DataFrame([
    #         {
    #             "id": "alpha",
    #             "symbol": "alp",
    #             "market_cap": 200_000_000,
    #             "total_volume": 5_000_000,
    #             "current_price": 0.8,
    #            "ath": 1.0,
    #             "price_change_percentage_30d_in_currency": 25.0,
    #         },
    #         {
    #             "id": "beta",
    #             "symbol": "bet",
    #             "market_cap": 350_000_000,
    #             "total_volume": 12_000_000,
    #             "current_price": 0.5,
    #             "ath": 0.9,
    #             "price_change_percentage_30d_in_currency": -5.0,
    #         },
    #     ])
    # else:
    df = fetch_cmc_markets(pages=8, limit=250)
    logging.info(f"✅ fetch_cmc_markets: {len(df)} Coins geladen, Columns: {list(df.columns)}")

    # ------------------------------
    # 1b️⃣ MEXC Mapping (global, unabhängig vom Modus)
    # ------------------------------
    print(">>> reached mapping block <<<")
    logging.info("[TRACE] >>> Starte map_mexc_pairs() in Snapshot-Pipeline")
    try:
        df = map_mexc_pairs(df)
        hits = df["mexc_pair"].notna().sum()
        logging.info(f"[MEXC] ✅ Mapping abgeschlossen ({hits} Treffer von {len(df)}).")
        if hits == 0:
            logging.warning("[MEXC] ⚠️ Keine Treffer beim Mapping – prüfe API oder Symbolabgleich.")
        logging.info(f"[TRACE] map_mexc_pairs: {hits} gültige Paare, Beispiele: {df[['symbol','mexc_pair']].head(5).to_dict('records')}")
    except Exception as e:
        logging.error(f"[MEXC] ❌ Fehler beim Mapping: {e}", exc_info=True)

    logging.info(f"[MEXC] 🔍 Vor Filterung: {df['mexc_pair'].notna().sum()} Coins mit MEXC-Paar")

    # ------------------------------
    # 2️⃣ Schema-Validierung
    # ------------------------------
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

    # ------------------------------
    # 3️⃣ Haupt-Pipeline (nur Live)
    # ------------------------------
    if effective_mode != "offline":
        logging.info(f"[TRACE] Vor apply_pre_universe_filters: {len(df)} Zeilen")
        df = apply_pre_universe_filters(df)
        logging.info(f"✅ apply_pre_universe_filters: {len(df)} nach Filtern")

        df = compute_feature_block(df)
        logging.info("✅ compute_feature_block abgeschlossen")
        logging.info(f"[TRACE] Spalten nach compute_feature_block → {list(df.columns)}")
        logging.info(f"[TRACE] mom_30d_pct valide Werte: {df['mom_30d_pct'].notna().sum() if 'mom_30d_pct' in df.columns else 0}")

        cand_ids = df["id"].tolist()
        df = compute_breakout_for_ids(df, cand_ids)
        logging.info("✅ compute_breakout_for_ids abgeschlossen")
        logging.info(f"[TRACE] Nach compute_breakout_for_ids: {len(df)} Zeilen")

        df = add_buzz_metrics_for_candidates(df)
        logging.info("✅ add_buzz_metrics_for_candidates abgeschlossen")
        logging.info(f"[TRACE] Nach add_buzz_metrics_for_candidates: {len(df)} Zeilen")

    # ------------------------------
    # 4️⃣ Scoring
    # ------------------------------
    logging.info(f"[TRACE] Vor Scoring: {len(df)} Zeilen, Columns: {list(df.columns)}")
    df = score_block(df)
    df = compute_early_score(df)
    logging.info("✅ Scores & Early Score berechnet")
    logging.info(f"[TRACE] Nach Scoring: early_score {df['early_score'].notna().sum()}, breakout_score {df['breakout_score'].notna().sum()}")

    # ------------------------------
    # 5️⃣ Validierung & Backtest
    # ------------------------------
    if effective_mode != "offline":
        logging.info(f"[TRACE] Vor validate_scores: {len(df)} Zeilen, early_score NaN={df['early_score'].isna().sum()}, breakout_score NaN={df['breakout_score'].isna().sum()}")
        validate_scores(df)
        backtest_results = backtest_on_snapshot(df, top_k=20, horizons=[20, 40, 60])
        logging.info(f"✅ Backtest abgeschlossen ({len(backtest_results)} Zeilen)")
    else:
        backtest_results = pd.DataFrame()
        logging.info("ℹ️ Offline-Modus: Score-Validierung & Backtest übersprungen")

    # ------------------------------
    # 6️⃣ Export
    # ------------------------------
    logging.info(f"[TRACE] Vor Export: {len(df)} Zeilen, Columns: {list(df.columns)}")
    full_df = make_fulldata(df)

    export_filename = (
        f"{ASOF_DATE}_offline_fullsnapshot.xlsx"
        if effective_mode == "offline"
        else f"{ASOF_DATE}_fullsnapshot.xlsx"
    )
    export_path = snapshot_dir / export_filename

    logging.info(f"📦 Erzeuge Excel → {export_path}")
    create_full_excel_export(full_df, export_path, extra_sheets={"Backtest": backtest_results})

    # ------------------------------
    # 7️⃣ CSV-Dateien (nur Live)
    # ------------------------------
    if effective_mode != "offline":
        cg_path = snapshot_dir / "cmc_markets.csv"
        mexc_path = snapshot_dir / "mexc_pairs.csv"
        alias_path = snapshot_dir / "seed_alias.csv"

        df.to_csv(cg_path, index=False)
        logging.info(f"✅ cg_markets.csv gespeichert ({cg_path})")

        if "mexc_pair" in df.columns:
            df[["id", "symbol", "mexc_pair"]].to_csv(mexc_path, index=False)
            logging.info(f"✅ mexc_pairs.csv gespeichert ({mexc_path})")

        if not alias_path.exists():
            seed_alias = get_alias_seed()
            seed_alias.to_csv(alias_path, index=False)
            logging.info(f"⚠️ seed_alias.csv neu erstellt → {alias_path}")

    logging.info(f"🎯 Snapshot abgeschlossen → {export_path}")
    return export_path


# --------------------------------------------------
# CLI Entry Point
# --------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run snapshot pipeline (Early Signal Engine)")
    parser.add_argument(
        "--mode",
        choices=["standard", "fast", "offline"],
        default="standard",
        help="Snapshot-Modus: standard, fast oder offline (Mock-Daten)",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Direkter Shortcut für Offline-Modus (synthetische Daten, kein API-Zugriff)",
    )

    args = parser.parse_args()

    mode = "offline" if args.offline else args.mode
    logging.info(f"🚀 Starte CLI-Snapshot mit Modus: {mode}")
    run_snapshot(mode=mode, offline=args.offline)
