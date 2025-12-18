"""
fetch_mexc_klines.py
--------------------
Robuster API-Wrapper für historische Candle-Daten (Klines) von der MEXC-Spot-API.

Wird ausschließlich für Tages-Kerzen (interval="1d") genutzt und liefert
ein DataFrame mit standardisiertem Schema:
    [time, open, high, low, close, volume]

Verwendung:
    from colabtool.features.fetch_mexc_klines import fetch_mexc_klines
"""

from __future__ import annotations
from typing import Optional
import pandas as pd
import numpy as np
import requests
import logging

MEXC_KLINES_URL = "https://api.mexc.com/api/v3/klines"

# -------------------------------------------------------------
# 🧩 Hauptfunktion
# -------------------------------------------------------------
def fetch_mexc_klines(symbol: str, interval: str = "1d", limit: int = 60) -> Optional[pd.DataFrame]:
    """
    Ruft Candle-Daten von der MEXC-Spot-API ab.

    Args:
        symbol: z. B. "DOTUSDT" (Großschreibung empfohlen)
        interval: Candle-Intervall (Standard: "1d")
        limit: Anzahl der Kerzen (max. 1000 laut API, Default = 60)

    Returns:
        pd.DataFrame mit Spalten ["time", "open", "high", "low", "close", "volume"]
        oder None bei Fehler/ungültigem Symbol.
    """
    try:
        resp = requests.get(
            MEXC_KLINES_URL,
            params={"symbol": symbol.upper(), "interval": interval, "limit": limit},
            timeout=10,
        )

        # --- HTTP-Validierung ---
        if resp.status_code == 400:
            logging.info(f"[MEXC][fetch] ⚠️ Kein Listing für {symbol} – Fallback aktiv")
            return None
        if resp.status_code != 200:
            logging.warning(f"[MEXC][fetch] ⚠️ HTTP {resp.status_code} für {symbol}")
            return None

        data = resp.json()
        if not data or not isinstance(data, list):
            logging.warning(f"[MEXC][fetch] ❌ Ungültige API-Antwort für {symbol}")
            return None

        # --- Nur relevante Spalten behalten ---
        cleaned = [row[:6] for row in data if len(row) >= 6]
        df = pd.DataFrame(cleaned, columns=["time", "open", "high", "low", "close", "volume"])
        df["time"] = pd.to_datetime(df["time"], unit="ms", errors="coerce")

        # --- Numerische Konvertierung ---
        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df.dropna(subset=["close", "volume"], inplace=True)
        if df.empty:
            logging.warning(f"[MEXC][fetch] ❌ Keine validen Datenpunkte für {symbol}")
            return None

        logging.info(f"[MEXC][fetch] ✅ {symbol}: {len(df)} Candles geladen")
        return df.reset_index(drop=True)

    except requests.RequestException as e:
        logging.warning(f"[MEXC][fetch] ⚠️ Netzwerkfehler für {symbol}: {e}")
    except Exception as e:
        logging.error(f"[MEXC][fetch] ❌ Unerwarteter Fehler bei {symbol}: {e}", exc_info=True)

    return None
