"""
Run Snapshot Mode → vollständige Early-Signal-Pipeline mit Backtest und Export
Erzeugt snapshots/YYYYMMDD/ mit allen Daten und Excel-Dateien.
"""

import os
from datetime import datetime
import pandas as pd

# ENV-Vars & API-Verhalten
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
from colabtool.data_sources import cg_markets, map_mexc_pairs
from colabtool.pre_universe import apply_pre_universe_filters
from colabtool.features import compute_feature_block
from colabtool.breakout import compute_breakout_for_ids
from colabtool.buzz import add_buzz_metrics_for_candidates
from colabtool.scores import score_block, compute_early_score
from colabtool.backtest import backtest_on_snapshot
from colabtool.export_helpers import make_fulldata
from colabtool.export import create_full_excel_export
from colabtool.data_sources import get_alias_seed  # added for seed_alias.csv

# --------------------------------------------------
# Validierungs-Helper
# --------------------------------------------------
def validate_scores(df: pd.DataFrame) -> None:
    required_cols = ["score_global", "early_score"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"⚠️ Fehlende Score-Spalten: {missing}")

    nan_counts = df[required_cols].isna().sum()
    if nan_counts.any():
        print(f"⚠️ Warnung: NaN-Werte gefunden in: {nan_counts.to_dict()}")
        df.dropna(subset=required_cols, inplace=True)

    valid_count = len(df)
    if valid_count < 100:
        raise ValueError(f"⚠️ Zu wenige valide Scores: {valid_count}")

    print(f"✅ Score-Validierung bestanden ({valid_count} valide Zeilen)")


# --------------------------------------------------
# Hauptfunktion
# --------------------------------------------------
def run_snapshot(mode: str = "standard"):
    ASOF_DATE = datetime.today().strftime("%Y%m%d")
    snapshot_dir = os.path.join("snapshots", ASOF_DATE)
    os.makedirs(snapshot_dir, exist_ok=True)

    print(f"🚀 Starte vollständigen Snapshot-Lauf für {ASOF_DATE} in {snapshot_dir}")

    # 1️⃣ Universe laden (CoinGecko)
    df = cg_markets(vs="usd", pages=4)
    print(f"✅ cg_markets: {len(df)} Coins geladen")

    # 2️⃣ Filter anwenden
    df = apply_pre_universe_filters(df)
    print(f"✅ apply_pre_universe_filters: {len(df)} nach Filtern")

    # 3️⃣ Feature-Block berechnen
    df = compute_feature_block(df)
    print(f"✅ compute_feature_block abgeschlossen")

    # 4️⃣ MEXC-Paare zuordnen
    df = map_mexc_pairs(df)
    print(f"✅ map_mexc_pairs abgeschlossen")

    # 5️⃣ Breakouts
    cand_ids = df["id"].tolist()
    df = compute_breakout_for_ids(df, cand_ids)
    print(f"✅ compute_breakout_for_ids abgeschlossen")

    # 6️⃣ Buzz
    df = add_buzz_metrics_for_candidates(df)
    print(f"✅ add_buzz_metrics_for_candidates abgeschlossen")

    # 7️⃣ Scoring
    df = score_block(df)
    df = compute_early_score(df)
    print(f"✅ Scores & Early Score berechnet")

    # 8️⃣ Validierung
    validate_scores(df)

    # 9️⃣ Backtest
    backtest_results = backtest_on_snapshot(df, top_k=20, horizontes=[20, 40, 60])
    print(f"✅ Backtest abgeschlossen ({len(backtest_results)} Zeilen)")

    # 🔟 Volldatensatz für Export vorbereiten
    full_df = make_fulldata(df)

    # 1️⃣1️⃣ Exportdateien im Tagesverzeichnis speichern
    export_filename = f"{ASOF_DATE}_fullsnapshot.xlsx"
    export_path = os.path.join(snapshot_dir, export_filename)

    print(f"📦 Erzeuge Excel → {export_path}")
    create_full_excel_export(full_df, export_path, extra_sheets={"Backtest": backtest_results})

    # CSV-Dateien (CoinGecko, MEXC, seed_alias)
    cg_path = os.path.join(snapshot_dir, "cg_markets.csv")
    mexc_path = os.path.join(snapshot_dir, "mexc_pairs.csv")
    alias_path = os.path.join(snapshot_dir, "seed_alias.csv")

    df.to_csv(cg_path, index=False)
    print(f"✅ cg_markets.csv gespeichert")

    # Falls MEXC-Paare vorhanden sind, separat speichern
    if "mexc_pair" in df.columns:
        df[["id", "symbol", "mexc_pair"]].to_csv(mexc_path, index=False)
        print(f"✅ mexc_pairs.csv gespeichert")

    # seed_alias.csv sicherstellen
    if not os.path.exists(alias_path):
        seed_alias = get_alias_seed()
        seed_alias.to_csv(alias_path, index=False)
        print(f"⚠️ seed_alias.csv neu erstellt → {alias_path}")

    print(f"🎯 Snapshot abgeschlossen → {export_path}")
    return export_path


if __name__ == "__main__":
    run_snapshot("standard")
