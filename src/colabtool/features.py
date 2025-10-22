# modules/features.py
from __future__ import annotations

import re
from .utils import pd, np, logging

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
def compute_feature_block(df_in: pd.DataFrame) -> pd.DataFrame:
    d = df_in.copy()
    d["market_cap"]   = pd.to_numeric(d.get("market_cap"), errors="coerce")
    d["total_volume"] = pd.to_numeric(d.get("total_volume"), errors="coerce")
    with np.errstate(divide="ignore", invalid="ignore"):
        d["volume_mc_ratio"] = (d["total_volume"] / d["market_cap"]).replace([np.inf, -np.inf], np.nan)
    d["slope30"] = pd.to_numeric(d.get("price_change_percentage_30d_in_currency"), errors="coerce")
    d["ath_drawdown_pct"] = pd.to_numeric(d.get("ath_change_percentage"), errors="coerce")
    d["circ_pct"] = np.nan
    return d

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

