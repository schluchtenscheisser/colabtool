# modules/features.py
from __future__ import annotations

import re
import pandas as pd
import logging
from .utilities import pd, np, logging
from colabtool.utils.validation import ensure_schema

# Manuelle Blacklist (IDs in Kleinbuchstaben)
EXCLUDE_IDS = set([
    # Beispiele; bei Bedarf pflegen
    "terra-luna", "bitcoin-wrapped", "usd-coin-bridged"
])

# ---------- Helpers ----------
def _ensure_series(x, index) -> pd.Series:
    return x if isinstance(x, pd.Series) else pd.Series([x] * len(index), index=index, dtype="float64")

def _num_series(df: pd.DataFrame, cols, default=np.nan) -> pd.Series:
    """
    Liefert IMMER eine numerische Series gleicher Länge wie df.
    Nimmt den ersten vorhandenen Spaltennamen aus cols.
    """
    if isinstance(cols, str):
        cols = [cols]
    for c in cols:
        if c in df.columns:
            s = pd.to_numeric(df[c], errors="coerce")
            return _ensure_series(s, df.index)
    return pd.Series([default] * len(df), index=df.index, dtype="float64")

def _lc(x) -> str:
    return str(x or "").strip().lower()

# ---------- Peg-/Wrapped-/Stable-Heuristiken ----------
_STABLE_HINTS = [
    r"\bstable\b", r"\busd\b", r"\busdc\b", r"\busdt\b", r"\btusd\b", r"\busdd\b",
    r"\bust\b", r"\bdai\b", r"\beur[ts]?\b", r"\btryb\b", r"\baud\b", r"\bgusd\b",
    r"\bpax\b", r"\busd-?stable\b", r"\bpeg\b"
]
_WRAPPED_HINTS = [
    r"\bwrapped\b", r"\bw\b[A-Z]{2,}\b", r"\bbridged\b", r"\bbinance-peg\b", r"\bwormhole\b", r"\banyswap\b"
]

def is_stable_like(name: str, symbol: str, cid: str) -> bool:
    n = _lc(name); s = _lc(symbol); i = _lc(cid)
    if any(h in n for h in ["stable", "usd-coin", "tether", "binance-usd", "dai", "trueusd", "usdd"]):
        return True
    if s in ("usdt", "usdc", "busd", "dai", "tusd", "usdd", "gusd"):
        return True
    if any(re.search(p, f" {n} ") for p in _STABLE_HINTS):
        return True
    if any(k in i for k in ["-stable-", "usd-", "binance-usd"]):
        return True
    return False

def is_wrapped_like(name: str, symbol: str, cid: str) -> bool:
    n = _lc(name); s = _lc(symbol); i = _lc(cid)
    if "wrapped" in n or "bridged" in n or "binance-peg" in n:
        return True
    if s.startswith("w") and len(s) >= 3:
        return True
    if any(re.search(p, f" {n} ") for p in _WRAPPED_HINTS):
        return True
    if any(k in i for k in ["wrapped", "bridged", "binance-peg"]):
        return True
    return False

def peg_like_mask(df: pd.DataFrame) -> pd.Series:
    """
    Peg-Heuristik via niedrige Bewegung:
    - 30d < 5% und 7d < 3% → Peg-verdächtig
    - Alternativ: 7d < 2% und 24h < 0.7% (falls 24h vorhanden)
    Robust gegen fehlende Spalten; Rückgabe immer Series.
    """
    p7  = _num_series(df, "price_change_percentage_7d_in_currency").abs().fillna(0.0)
    p30 = _num_series(df, "price_change_percentage_30d_in_currency").abs().fillna(0.0)
    p1  = _num_series(df, ["price_change_percentage_24h_in_currency", "price_change_percentage_24h"], default=np.nan)
    p1  = _ensure_series(p1, df.index).abs().fillna(999.0)  # fehlend ⇒ neutral

    cond_main = (p30 < 5.0) & (p7 < 3.0)
    cond_alt  = (p7 < 2.0) & (p1 < 0.7)
    out = cond_main | cond_alt
    return _ensure_series(out.astype(bool), df.index)

def exclusion_mask(df: pd.DataFrame, cats: pd.Series) -> pd.Series:
    cats_l = cats.astype(str).str.lower() if isinstance(cats, pd.Series) else pd.Series([""] * len(df), index=df.index)
    m = pd.Series(False, index=df.index)

    m |= cats_l.str.contains("stable", na=False)
    m |= cats_l.str.contains("wrapped", na=False)
    m |= cats_l.str.contains("bridged", na=False)
    m |= cats_l.str.contains("binance-peg", na=False)

    m |= df.apply(lambda r: is_stable_like(r["name"], r["symbol"], r["id"]), axis=1)
    m |= df.apply(lambda r: is_wrapped_like(r["name"], r["symbol"], r["id"]), axis=1)

    m |= df["id"].astype(str).str.lower().isin(EXCLUDE_IDS)
    return _ensure_series(m.astype(bool), df.index)

# ---------- Feature-Block ----------
# ---------------------------------------------------------------------
# 📊 Neue Hybrid-Feature-Logik: MEXC-Klines + CMC-Fallback
# ---------------------------------------------------------------------
import requests
import numpy as np
import pandas as pd
import logging
from typing import Optional, Dict, Any, List

MEXC_KLINES_URL = "https://api.mexc.com/api/v3/klines"

def fetch_mexc_klines(symbol: str, interval: str = "1d", limit: int = 60) -> Optional[pd.DataFrame]:
    """
    Holt historische Candle-Daten von MEXC.
    Gibt DataFrame mit Spalten [time, open, high, low, close, volume] zurück.
    Gibt None zurück, wenn kein Pair existiert (HTTP 400).
    """
    try:
        resp = requests.get(
            MEXC_KLINES_URL,
            params={"symbol": symbol.upper(), "interval": interval, "limit": limit},
            timeout=10
        )

        # --- Kein Handelspaar vorhanden ---
        if resp.status_code == 400:
            logging.info(f"[MEXC] Kein Klines-Listing für {symbol} – Fallback auf CMC aktiv.")
            return None

        if resp.status_code != 200:
            logging.warning(f"[MEXC] Klines-Fehler {symbol}: {resp.status_code}")
            return None

        data = resp.json()
        if not data or not isinstance(data, list):
            logging.warning(f"[MEXC] Klines-Response leer oder ungültig für {symbol}")
            return None

        # --- Nur relevante Spalten extrahieren (erste 6 Werte) ---
        cleaned_data = [row[:6] for row in data if len(row) >= 6]
        df = pd.DataFrame(cleaned_data, columns=["time", "open", "high", "low", "close", "volume"])
        df["time"] = pd.to_datetime(df["time"], unit="ms")

        return df

    except Exception as e:
        logging.warning(f"[MEXC] Klines-Abfrage fehlgeschlagen ({symbol}): {e}")
        return None

def compute_mexc_features(df: pd.DataFrame) -> Dict[str, float]:
    """Berechnet Momentum, Volumenbeschleunigung, ATH-Drawdown aus MEXC-Klines"""
    if df is None or df.empty:
        return {"mom_7d_pct": np.nan, "mom_30d_pct": np.nan, "vol_acc": np.nan, "ath_drawdown_pct": np.nan}

    closes = df["close"].values
    vols = df["volume"].values
    if len(closes) < 30:
        return {"mom_7d_pct": np.nan, "mom_30d_pct": np.nan, "vol_acc": np.nan, "ath_drawdown_pct": np.nan}

    mom_7d_pct = (closes[-1] / closes[-8] - 1) * 100
    mom_30d_pct = (closes[-1] / closes[-31] - 1) * 100
    vol_acc = np.mean(vols[-7:]) / np.mean(vols[-30:]) if np.mean(vols[-30:]) > 0 else np.nan
    ath = np.max(closes)
    ath_idx = int(np.argmax(closes))
    ath_date = df["time"].iloc[ath_idx]
    ath_drawdown_pct = (closes[-1] / ath - 1) * 100

    return {
        "mom_7d_pct": mom_7d_pct,
        "mom_30d_pct": mom_30d_pct,
        "vol_acc": vol_acc,
        "ath": ath,
        "ath_date": ath_date,
        "ath_drawdown_pct": ath_drawdown_pct,
    }


def compute_feature_block(df_in: pd.DataFrame) -> pd.DataFrame:
    """
    Neues Feature-Block-Modul:
    - bevorzugt Momentum & Volumen aus MEXC-Klines
    - fallback auf CMC-Prozentwerte
    """
    logging.info("🔧 compute_feature_block (Hybrid CMC+MEXC) gestartet ...")
    df = df_in.copy()

    mom7, mom30, vol_acc, ath_dd = [], [], [], []

    for _, row in df.iterrows():
        # --- Symbol ermitteln & validieren ---
        symbol = str(row.get("symbol", "")).strip().upper()
        if not symbol:
            logging.warning("[MEXC] ⚠️ Kein Symbol in Zeile gefunden – übersprungen.")
            mom7.append(np.nan)
            mom30.append(np.nan)
            vol_acc.append(np.nan)
            ath_dd.append(np.nan)
            ath_vals.append(np.nan)
            ath_dates.append(np.nan)
            price_sources.append("CMC")
            continue
    
        # MEXC-Pairs enden üblicherweise auf USDT
        pair = f"{symbol}USDT"
    
        # --- Versuche Klines abzurufen ---
        kl = fetch_mexc_klines(pair)
        if kl is not None and len(kl) >= 5:
            try:
                f = compute_mexc_features(kl)
                mom7.append(f.get("mom_7d_pct", np.nan))
                mom30.append(f.get("mom_30d_pct", np.nan))
                vol_acc.append(f.get("vol_acc", np.nan))
                ath_dd.append(f.get("ath_drawdown_pct", np.nan))
                # Neue Felder
                ath_vals.append(f.get("ath", np.nan))
                ath_dates.append(f.get("ath_date", np.nan))
                price_sources.append("MEXC")
                logging.debug(f"[MEXC] ✅ Klines verarbeitet: {pair}")
            except Exception as e:
                logging.warning(f"[MEXC] ⚠️ Fehler bei Feature-Berechnung {pair}: {e}")
                mom7.append(np.nan)
                mom30.append(np.nan)
                vol_acc.append(np.nan)
                ath_dd.append(np.nan)
                ath_vals.append(np.nan)
                ath_dates.append(np.nan)
                price_sources.append("CMC")
        else:
            # --- Fallback auf CMC-Prozentwerte ---
            mom7.append(row.get("price_change_percentage_7d_in_currency", np.nan))
            mom30.append(row.get("price_change_percentage_30d_in_currency", np.nan))
            vol_acc.append(np.nan)
            ath_dd.append(np.nan)
            ath_vals.append(np.nan)
            ath_dates.append(np.nan)
            price_sources.append("CMC")
            logging.info(f"[MEXC] ⚙️ Fallback auf CMC-Daten: {pair}")


    df["mom_7d_pct"] = mom7
    df["mom_30d_pct"] = mom30
    df["vol_acc"] = vol_acc
    df["ath_drawdown_pct"] = ath_dd

    # --- Schema-Validierung & Typkonvertierung ---
    schema_map = {
        "mom_7d_pct": float,
        "mom_30d_pct": float,
        "vol_acc": float,
        "ath": float,
        "ath_date": "datetime64[ns]",
        "ath_drawdown_pct": float,
        "volume_mc_ratio": float,
        "circ_pct": float,
        "price_source": str,
    }

    df = ensure_schema(df, schema_map)
    
    logging.info(f"✅ compute_feature_block abgeschlossen – {len(df)} Coins verarbeitet.")
    return df
    
# ---------- Segmentierung ----------
def tag_segment(row) -> str:
    try:
        mc = float(row.get("market_cap", np.nan))
    except Exception:
        mc = np.nan
    r30 = float(row.get("price_change_percentage_30d_in_currency", 0.0) or 0.0)
    dd  = float(row.get("ath_change_percentage", row.get("ath_drawdown_pct", 0.0)) or 0.0)

    if np.isfinite(mc) and mc <= 150_000_000 and r30 >= 100.0:
        return "Momentum Gem"
    if dd <= -70.0 and r30 >= 20.0:
        return "Comeback"
    if np.isfinite(mc) and mc <= 150_000_000:
        return "Hidden Gem"
    if np.isfinite(mc) and mc <= 500_000_000:
        return "Emerging"
    return "Balanced"

