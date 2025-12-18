"""
feature_block.py
----------------
Orchestriert die Feature-Berechnung über das gesamte Universe-DataFrame.
Verwendet:
  - fetch_mexc_klines() für API-Daten
  - compute_mexc_features() für Berechnung
  - Fallback auf CMC-Prozentwerte bei Fehlern
"""

from __future__ import annotations
import logging
import pandas as pd
import numpy as np
from typing import Any, Dict

from colabtool.utils.validation import ensure_schema
from colabtool.features.fetch_mexc_klines import fetch_mexc_klines
from colabtool.features.compute_mexc_features import compute_mexc_features

# -------------------------------------------------------------
# 🧮 Hauptfunktion
# -------------------------------------------------------------
def compute_feature_block(df_in: pd.DataFrame) -> pd.DataFrame:
    """
    Berechnet Momentum-, Volumen- und ATH-bezogene Features für alle Coins.

    Args:
        df_in: DataFrame mit mind. Spalten ['symbol', 'price_change_percentage_7d_in_currency', 'price_change_percentage_30d_in_currency']

    Returns:
        DataFrame mit neuen Spalten:
        ['mom_7d_pct', 'mom_30d_pct', 'vol_acc', 'ath', 'ath_date', 'ath_drawdown_pct', 'price_source']
    """

    logging.info("🧩 Starte compute_feature_block() ...")
    df = df_in.copy()

    # Ergebnis-Container vorbereiten
    mom7, mom30, vol_accs, ath_vals, ath_dds, ath_dates, price_sources = (
        [], [], [], [], [], [], []
    )

    total = len(df)
    success = 0
    fallback = 0

    for idx, row in df.iterrows():
        symbol = str(row.get("symbol", "")).strip().upper()
        pair = f"{symbol}USDT"

        if not symbol:
            logging.warning(f"[features] ⚠️ Kein Symbol in Zeile {idx} – übersprungen.")
            mom7.append(np.nan)
            mom30.append(np.nan)
            vol_accs.append(np.nan)
            ath_vals.append(np.nan)
            ath_dds.append(np.nan)
            ath_dates.append(np.nan)
            price_sources.append("None")
            continue

        # --- Versuche Daten von MEXC zu holen ---
        klines = fetch_mexc_klines(pair)
        if klines is not None and len(klines) >= 30:
            try:
                feats = compute_mexc_features(klines)
                mom7.append(feats.get("mom_7d_pct", np.nan))
                mom30.append(feats.get("mom_30d_pct", np.nan))
                vol_accs.append(feats.get("vol_acc", np.nan))
                ath_vals.append(feats.get("ath", np.nan))
                ath_dds.append(feats.get("ath_drawdown_pct", np.nan))
                ath_dates.append(feats.get("ath_date", np.nan))
                price_sources.append("MEXC")
                success += 1
                logging.debug(f"[MEXC] ✅ {pair} Features berechnet")
            except Exception as e:
                logging.warning(f"[MEXC] ⚠️ Fehler bei {pair}: {e}")
                mom7.append(np.nan)
                mom30.append(np.nan)
                vol_accs.append(np.nan)
                ath_vals.append(np.nan)
                ath_dds.append(np.nan)
                ath_dates.append(np.nan)
                price_sources.append("CMC")
                fallback += 1
        else:
            # --- Fallback auf CMC-Prozentwerte ---
            mom7.append(row.get("price_change_percentage_7d_in_currency", np.nan))
            mom30.append(row.get("price_change_percentage_30d_in_currency", np.nan))
            vol_accs.append(np.nan)
            ath_vals.append(np.nan)
            ath_dds.append(np.nan)
            ath_dates.append(np.nan)
            price_sources.append("CMC")
            fallback += 1
            logging.info(f"[MEXC][fallback] ⚙️ {pair} → CMC-Werte verwendet")

    # Ergebnisse in DataFrame schreiben
    df["mom_7d_pct"] = mom7
    df["mom_30d_pct"] = mom30
    df["vol_acc"] = vol_accs
    df["ath"] = ath_vals
    df["ath_date"] = ath_dates
    df["ath_drawdown_pct"] = ath_dds
    df["price_source"] = price_sources

    # Typprüfung und Schema-Angleichung
    schema_map = {
        "mom_7d_pct": float,
        "mom_30d_pct": float,
        "vol_acc": float,
        "ath": float,
        "ath_date": "datetime64[ns]",
        "ath_drawdown_pct": float,
        "price_source": str,
    }
    df = ensure_schema(df, schema_map)

    # Logging: Zusammenfassung
    logging.info(f"[features] ✅ compute_feature_block abgeschlossen – {success}/{total} erfolgreich, {fallback} Fallbacks")
    logging.debug(f"[features] Spalten: {list(df.columns)}")

    return df
