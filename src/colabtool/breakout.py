
# modules/breakout.py
from __future__ import annotations

import math
import time
from typing import Dict, List, Optional, Tuple

import requests
from .utils import pd, np, logging

# --------- MEXC HTTP ---------
_MEXC_BASE = "https://api.mexc.com"
_s = requests.Session()
_s.headers.update({"Accept": "application/json", "User-Agent": "mexc-early-screener/1.0"})

def _mexc_klines(pair: str, interval: str = "1d", limit: int = 365, attempts: int = 2, sleep_s: float = 0.8):
    """Holt Klines. Rückgabe: Liste von Kerzen oder None bei Fehler."""
    url = f"{_MEXC_BASE}/api/v3/klines"
    params = {"symbol": pair, "interval": interval, "limit": int(limit)}
    for att in range(1, attempts + 1):
        try:
            r = _s.get(url, params=params, timeout=20)
            if r.status_code == 200:
                return r.json()
            if r.status_code in (400, 404):
                logging.warning(f"[breakout] {pair} klines fail: {r.status_code} {r.reason}")
                return None
            logging.warning(f"[breakout] {pair} klines HTTP {r.status_code} → retry {att}/{attempts}")
        except requests.RequestException as ex:
            logging.warning(f"[breakout] {pair} klines err: {ex} → retry {att}/{attempts}")
        time.sleep(sleep_s)
    return None

# --------- Helpers ---------
def _valid_pair(p) -> Optional[str]:
    if p is None:
        return None
    s = str(p).strip().upper()
    if not s or s == "NAN" or s == "NONE":
        return None
    # Nur USD-Stables als Quote für sauberes USD-Volumen
    if not (s.endswith("USDT") or s.endswith("USD") or s.endswith("USDC")):
        return None
    return s

def _to_df(kl: list) -> Optional[pd.DataFrame]:
    """MEXC klines → DataFrame mit ts, open, high, low, close, volume (base)"""
    if not isinstance(kl, list) or len(kl) == 0:
        return None
    cols = ["t","o","h","l","c","v","ct","qv","num","tb","tqv","ignore"]
    try:
        d = pd.DataFrame(kl, columns=cols[:len(kl[0])])
    except Exception:
        return None
    num_cols = {"o":"float64","h":"float64","l":"float64","c":"float64","v":"float64"}
    for c, t in num_cols.items():
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d["t"] = pd.to_datetime(d["t"], unit="ms", utc=True)
    d = d[["t","o","h","l","c","v"]].dropna()
    d = d.sort_values("t").reset_index(drop=True)
    return d if len(d) > 0 else None

def _pct_change(x: pd.Series) -> pd.Series:
    return x.pct_change().replace([np.inf, -np.inf], np.nan)

def _rolling_max(s: pd.Series, win: int) -> pd.Series:
    return s.rolling(win, min_periods=max(2, int(win*0.6))).max()

def _percentile_rank(a: pd.Series, value: float) -> float:
    a = pd.to_numeric(a, errors="coerce")
    a = a[np.isfinite(a)]
    if len(a) == 0:
        return np.nan
    return float((a <= value).mean() * 100.0)

def _zscore(s: pd.Series) -> pd.Series:
    x = pd.to_numeric(s, errors="coerce")
    m = x.mean()
    v = x.std(ddof=0)
    if not np.isfinite(v) or v == 0:
        return pd.Series(0.0, index=x.index, dtype="float64")
    return (x - m) / v

def _beta(ret_asset: pd.Series, ret_bench: pd.Series) -> float:
    x = pd.to_numeric(ret_asset, errors="coerce")
    y = pd.to_numeric(ret_bench, errors="coerce")
    m = pd.concat([x, y], axis=1).dropna()
    if len(m) < 20:
        return np.nan
    cov = np.cov(m.iloc[:,0], m.iloc[:,1])[0,1]
    var = np.var(m.iloc[:,1])
    if var == 0:
        return np.nan
    return float(cov / var)

# --------- Core Feature-Berechnung pro Pair ---------
def _features_from_klines(dfk: pd.DataFrame) -> dict:
    """Berechnet Distanz zu Highs, Donchian-Width, Volumen-Acceleration (USD), p365.
       Liefert zusätzlich vol_acc_7d und vol_acc_30d als USD-MAs für Audit.
    """
    # Close und base-Volumen
    c = dfk["c"].astype(float)
    v_base = dfk["v"].astype(float)
    # USD-Volumen nur sinnvoll bei Stable-Quote → hier bereits gefiltert
    vol_usd = c * v_base

    # Donchian und Distanzen
    rmax90  = _rolling_max(c, 90)
    rmax180 = _rolling_max(c, 180)
    rmax365 = _rolling_max(c, 365)

    last = c.iloc[-1]
    dist_90  = float((last / rmax90.iloc[-1]  - 1.0)*100.0) if np.isfinite(rmax90.iloc[-1]) else np.nan
    dist_180 = float((last / rmax180.iloc[-1] - 1.0)*100.0) if np.isfinite(rmax180.iloc[-1]) else np.nan
    dist_365 = float((last / rmax365.iloc[-1] - 1.0)*100.0) if np.isfinite(rmax365.iloc[-1]) else np.nan

    # Donchian width als Proxy
    min90 = c.rolling(90, min_periods=60).min()
    max90 = rmax90
    donch_width = float((max90.iloc[-1] / min90.iloc[-1] - 1.0)*100.0) if np.isfinite(min90.iloc[-1]) and np.isfinite(max90.iloc[-1]) else np.nan

    # Perzentil des letzten Preises im 365-Tage-Fenster
    p365 = _percentile_rank(c.tail(min(365, len(c))), last)

    # Volumen-Acceleration: 7d vs 30d Wert-Volumen
    ma7  = vol_usd.rolling(7,  min_periods=5).mean()
    ma30 = vol_usd.rolling(30, min_periods=15).mean()
    ma7_last  = float(ma7.iloc[-1]) if np.isfinite(ma7.iloc[-1]) else np.nan
    ma30_last = float(ma30.iloc[-1]) if np.isfinite(ma30.iloc[-1]) else np.nan
    vol_acc = float((ma7_last / ma30_last) if (np.isfinite(ma7_last) and np.isfinite(ma30_last) and ma30_last > 0) else np.nan)

    # Breakout-Basis: Nähe zum 90-Tage-High
    breakout_base = dist_90  # in %
    return {
        "dist_90": dist_90,
        "dist_180": dist_180,
        "dist_365": dist_365,
        "donch_width": donch_width,
        "p365": p365,
        "vol_acc": vol_acc,
        "vol_acc_7d": ma7_last,
        "vol_acc_30d": ma30_last,
        "breakout_base": breakout_base,
    }

def _prep_betas(days: int = 365) -> Tuple[Optional[pd.Series], Optional[pd.Series]]:
    """BTC/ETH tägliche Renditen von MEXC (USDT-Quote)."""
    out = {}
    for sym in ["BTCUSDT", "ETHUSDT"]:
        kl = _mexc_klines(sym, "1d", min(days, 365))
        dfk = _to_df(kl) if kl else None
        if dfk is None or len(dfk) < 60:
            out[sym] = None
        else:
            out[sym] = _pct_change(dfk["c"])
    return out.get("BTCUSDT"), out.get("ETHUSDT")

# --------- Public: Breakout-Rechner ---------
def compute_breakout_for_ids(df_all: pd.DataFrame,
                             cand_ids: List[str],
                             days: int = 365,
                             progress: bool = True,
                             use_chart: bool = True,
                             light: bool = False) -> pd.DataFrame:
    """
    Berechnet Breakout/Volumen/Betas nur für valide MEXC-Paare.
    Gibt DataFrame mit Spalten:
      id, breakout_score, z_break, z_donch, dist_90, dist_180, dist_365, p365,
      vol_acc, vol_acc_7d, vol_acc_30d, break_vol_mult, donch_width, beta_btc, beta_eth, price_source
    """
    if not isinstance(df_all, pd.DataFrame) or not cand_ids:
        return pd.DataFrame(columns=[
            "id","breakout_score","z_break","z_donch","dist_90","dist_180","dist_365",
            "p365","vol_acc","vol_acc_7d","vol_acc_30d","break_vol_mult","donch_width","beta_btc","beta_eth","price_source"
        ])

    # id -> mexc_pair validieren
    sub = df_all[df_all["id"].astype(str).isin(cand_ids)].copy()
    sub["mexc_pair"] = sub["mexc_pair"].map(_valid_pair)
    sub = sub.dropna(subset=["mexc_pair"])
    if sub.empty:
        logging.info("[breakout] keine validen MEXC-Paare unter den Kandidaten")
        return pd.DataFrame(columns=[
            "id","breakout_score","z_break","z_donch","dist_90","dist_180","dist_365",
            "p365","vol_acc","vol_acc_7d","vol_acc_30d","break_vol_mult","donch_width","beta_btc","beta_eth","price_source"
        ])

    # Einmalig BTC/ETH-Betas vorbereiten
    r_btc, r_eth = _prep_betas(days=days)

    rows = []
    # Cache pro Pair, falls mehrere IDs dasselbe Pair hätten
    pair_cache: Dict[str, dict] = {}

    for _, r in sub.iterrows():
        cid = str(r["id"])
        pair = r["mexc_pair"]
        if pair in pair_cache:
            feat = pair_cache[pair]
        else:
            kl = _mexc_klines(pair, "1d", min(days, 365))
            dfk = _to_df(kl) if kl else None
            if dfk is None or len(dfk) < 60:
                # zu dünn → skip
                pair_cache[pair] = None
                if progress:
                    logging.warning(f"[breakout] {pair} zu wenig Daten")
                continue
            feat = _features_from_klines(dfk)
            # Betas
            ret = _pct_change(dfk["c"])
            b_btc = _beta(ret, r_btc) if r_btc is not None else np.nan
            b_eth = _beta(ret, r_eth) if r_eth is not None else np.nan
            feat["beta_btc"] = b_btc
            feat["beta_eth"] = b_eth
            feat["price_source"] = "mexc"
            pair_cache[pair] = feat

        if feat is None:
            continue

        rows.append({
            "id": cid,
            "dist_90": feat["dist_90"],
            "dist_180": feat["dist_180"],
            "dist_365": feat["dist_365"],
            "p365": feat["p365"],
            "vol_acc": feat["vol_acc"],
            "vol_acc_7d": feat["vol_acc_7d"],
            "vol_acc_30d": feat["vol_acc_30d"],
            "donch_width": feat["donch_width"],
            "breakout_base": feat["breakout_base"],
            "beta_btc": feat["beta_btc"],
            "beta_eth": feat["beta_eth"],
            "price_source": feat["price_source"],
        })

    if not rows:
        return pd.DataFrame(columns=[
            "id","breakout_score","z_break","z_donch","dist_90","dist_180","dist_365",
            "p365","vol_acc","vol_acc_7d","vol_acc_30d","break_vol_mult","donch_width","beta_btc","beta_eth","price_source"
        ])

    dfb = pd.DataFrame(rows)

    # Z-Norm über Kandidaten
    z_break = _zscore(pd.to_numeric(dfb["dist_90"], errors="coerce"))
    # donch score: hohe dist_90, aber schmalere Range (kleine width) besser → -width
    z_donch = _zscore(pd.to_numeric(dfb["dist_90"], errors="coerce") - 0.3 * pd.to_numeric(dfb["donch_width"], errors="coerce"))

    dfb["z_break"] = z_break
    dfb["z_donch"] = z_donch
    dfb["breakout_score"] = 0.7 * dfb["z_break"] + 0.3 * dfb["z_donch"]

    # Breakout-abhängiges Volumen-Multiplikator (Audit)
    dfb["break_vol_mult"] = pd.to_numeric(dfb["vol_acc"], errors="coerce")

    # Finales Set
    keep = [
        "id","breakout_score","z_break","z_donch","dist_90","dist_180","dist_365",
        "p365","vol_acc","vol_acc_7d","vol_acc_30d","break_vol_mult","donch_width","beta_btc","beta_eth","price_source"
    ]
    for k in keep:
        if k not in dfb.columns:
            dfb[k] = np.nan
    return dfb[keep].copy()

