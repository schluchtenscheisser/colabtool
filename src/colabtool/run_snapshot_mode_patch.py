"""
Patch-Modul: Integration der Scoring-Funktionen in die Snapshot-Pipeline.
Erstellt zur sicheren Aktivierung von score_block() und compute_early_score().
"""

import logging
from src.colabtool.scores import score_block, compute_early_score
from src.colabtool.export import export_to_excel

def run_with_scoring(df, meta, breakout_mode=True):
    """
    Wrapper um den bestehenden Pipeline-Prozess.
    Führt nach der Breakout-Berechnung die Scoring-Funktionen aus.
    """
    logging.info("🔍 Starte Scoring-Integration...")

    try:
        # 1️⃣ Globale Score-Berechnung
        df = score_block(df)
        logging.info("✅ score_block erfolgreich berechnet.")

        # 2️⃣ Early-Score-Berechnung
        df = compute_early_score(df)
        logging.info("✅ compute_early_score erfolgreich berechnet.")

        meta["score_valid"] = True

    except Exception as e:
        logging.warning(f"⚠️ Scoring skipped due to error: {e}")
        meta["score_valid"] = False

    # 3️⃣ Excel-Export (unverändert)
    export_to_excel(df, meta)
    logging.info("📦 Export abgeschlossen.")

    return df, meta


if __name__ == "__main__":
    # Nur zu Testzwecken direkt ausführbar
    import pandas as pd

    dummy = pd.DataFrame({
        "id": ["coin_a", "coin_b"],
        "market_cap": [2e8, 4e8],
        "price_change_percentage_7d_in_currency": [10, -5],
        "price_change_percentage_30d_in_currency": [25, 40],
        "volume_mc_ratio": [1.0, 1.8],
        "ath_change_percentage": [-70, -80],
    })

    meta = {}
    df, meta = run_with_scoring(dummy, meta)
    print(df[["id", "score_global", "score_segment", "early_score"]])
