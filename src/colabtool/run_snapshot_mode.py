"""
Run Snapshot Mode – vollständige Early-Signal-Pipeline mit Backtest
Erzeugt snapshots/YYYYMMDD_fullsnapshot.xlsx
"""

import os
from datetime import datetime
import pandas as pd

# === ENV Variablen und API-Verhalten ===
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

# === Imports ===
from colabtool.data_sources import cg_markets
from colabtool.pre_universe import apply_pre_universe_filters
from colabtool.features import compute_feature_block
from colabtool.breakout import compute_breakout_for_ids
from colabtool.buzz import add_buzz_metrics_for_candidates
from colabtool.scores import score_block, compute_early_score
from colabtool.backtest import backtest_on_snapshot
from colabtool.export_helpers import make_fulldata
from colabtool.export import create_full_excel_export, write_sheet  # <-- wichtig: neue Funktion importiert

# === Hauptfunktion ===
def run_snapshot(mode: str = "standard"):
    ASOF_DATE = datetime.today().strftime("%Y%m%d")
    print(f"🚀 Starte vollständigen Snapshot-Lauf für {ASOF_DATE}")

    # 1️⃣ Universum laden (CoinGecko)
    df = cg_markets(vs="usd", pages=4)
    print(f"✅ cg_markets: {len(df)} Coins geladen")

    # 2️⃣ Vorfilter anwenden
    df = apply_pre_universe_filters(df)
    print(f"✅ apply_pre_universe_filters: {len(df)} nach Filtern")

    # 3️⃣ Features berechnen
    df = compute_feature_block(df)
    print(f"✅ compute_feature_block abgeschlossen")

    # 4️⃣ Breakouts (Donchian, ATH-Distanz)
    df = compute_breakout_for_ids(df)
    print(f"✅ compute_breakout_for_ids abgeschlossen")

    # 5️⃣ Buzz (News & Sentiment)
    df = add_buzz_metrics_for_candidates(df)
    print(f"✅ add_buzz_metrics_for_candidates abgeschlossen")

    # 6️⃣ Scoring
    df = score_block(df)
    df = compute_early_score(df)
    print(f"✅ Scores & Early Score berechnet")

    # 7️⃣ Backtest
    backtest_results = backtest_on_snapshot(df, top_k=20, horizons=[20, 40, 60])
    print(f"✅ Backtest abgeschlossen ({len(backtest_results)} Zeilen)")

    # 8️⃣ Vollständigen DataFrame für Export vorbereiten
    full_df = make_fulldata(df)

    # 9️⃣ Excel-Export
    export_filename = f"{ASOF_DATE}_fullsnapshot.xlsx"
    export_path = os.path.join("snapshots", export_filename)
    os.makedirs("snapshots", exist_ok=True)

    print(f"📦 Erzeuge Excel: {export_path}")

    # Excel mit allen Rankings erzeugen
    create_full_excel_export(full_df, export_path)

    # Backtest nachträglich anhängen
    with pd.ExcelWriter(export_path, engine="openpyxl", mode="a") as writer:
        write_sheet(backtest_results, "Backtest", writer)

    print(f"🎯 Snapshot abgeschlossen → {export_path}")
    return export_path


if __name__ == "__main__":
    run_snapshot("standard")
