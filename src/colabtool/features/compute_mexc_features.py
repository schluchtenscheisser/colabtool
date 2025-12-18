"""
compute_mexc_features.py
------------------------
Berechnet Feature-Metriken (Momentum, Volumenbeschleunigung, ATH-Drawdown)
aus den Candle-Daten der MEXC-Spot-API.

Verwendung:
    from colabtool.features.compute_mexc_features import compute_mexc_features
"""

from __future__ import annotations
import pandas as pd
import numpy as np
import logging
from typing import Dict

# -------------------------------------------------------------
# 🧮 Hauptfunktion
# -------------------------------------------------------------
def compute_mexc_features(df: pd.DataFrame) -> Dict[str, float]:
    """
    Berechnet Momentum, Volumenbeschleunigung und ATH-Drawdown aus MEXC-Klines.

    Args:
        df: DataFrame mit Spalten ["time", "open", "high", "low", "close", "volume"]

    Returns:
        dict mit Kennzahlen:
        {
          "mom_7d_pct": float,
          "mom_30d_pct": float,
          "vol_acc": float,
          "ath": float,
          "ath_drawdown_pct": float,
          "ath_date": pd.Timestamp
        }
    """

    # Sicherheitsprüfung
    if df is None or df.empty or len(df) < 30:
        logging.warning("[MEXC][compute] ⚠️ Zu wenige Daten für Feature-Berechnung")
        return {
            "mom_7d_pct": np.nan,
            "mom_30d_pct": np.nan,
            "vol_acc": np.nan,
            "ath": np.nan,
            "ath_drawdown_pct": np.nan,
            "ath_date": np.nan,
        }

    try:
        closes = df["close"].astype(float).to_numpy()
        volumes = df["volume"].astype(float).to_numpy()

        # Momentum-Berechnung (%)
        mom_7d_pct = (closes[-1] / closes[-8] - 1) * 100 if len(closes) >= 8 else np.nan
        mom_30d_pct = (closes[-1] / closes[-31] - 1) * 100 if len(closes) >= 31 else np.nan

        # Volumenbeschleunigung
        vol_acc = (
            np.mean(volumes[-7:]) / np.mean(volumes[-30:])
            if np.mean(volumes[-30:]) > 0
            else np.nan
        )

        # All-Time-High und Drawdown
        ath = np.nanmax(closes)
        ath_idx = int(np.nanargmax(closes))
        ath_date = df["time"].iloc[ath_idx] if "time" in df.columns else np.nan
        ath_drawdown_pct = (closes[-1] / ath - 1) * 100

        result = {
            "mom_7d_pct": mom_7d_pct,
            "mom_30d_pct": mom_30d_pct,
            "vol_acc": vol_acc,
            "ath": ath,
            "ath_drawdown_pct": ath_drawdown_pct,
            "ath_date": ath_date,
        }

        logging.debug(f"[MEXC][compute] ✅ Features berechnet ({len(df)} candles)")
        return result

    except Exception as e:
        logging.error(f"[MEXC][compute] ❌ Fehler bei Feature-Berechnung: {e}", exc_info=True)
        return {
            "mom_7d_pct": np.nan,
            "mom_30d_pct": np.nan,
            "vol_acc": np.nan,
            "ath": np.nan,
            "ath_drawdown_pct": np.nan,
            "ath_date": np.nan,
        }
