
# modules/scores.py
from __future__ import annotations

from typing import Optional
from .utils import pd, np, logging

# ----------------------------
# Helpers
# ----------------------------
def _ensure_series(x, index) -> pd.Series:
    return x if isinstance(x, pd.Series) else pd.Series([x] * len(index), index=index, dtype="float64")

def _winsorize(s: pd.Series, lim: float = 3.0) -> pd.Series:
    s = pd.to_numeric(s, errors="coerce")
    return s.clip(lower=-abs(lim), upper=abs(lim))

def _mc_bucket(mc: pd.Series) -> pd.Series:
    mc = pd.to_numeric(mc, errors="coerce")
    b = pd.Series("gt2b", index=mc.index, dtype="object")
    b.loc[mc <= 2_000_000_000] = "500m_2b"
    b.loc[mc <= 500_000_000] = "150m_500m"
    b.loc[mc <= 150_000_000] = "le150m"
    return b

def _z_by_bucket(series: pd.Series, bucket: pd.Series, winsor: float = 3.0) -> pd.Series:
    x = pd.to_numeric(series, errors="coerce")
    b = bucket.astype("object")
    out = pd.Series(np.nan, index=x.index, dtype="float64")
    for k, idx in b.groupby(b).groups.items():
        vals = x.loc[idx]
        vals = vals[np.isfinite(vals)]
        if len(vals) < 2 or vals.std(ddof=0) == 0:
            out.loc[idx] = 0.0
        else:
            m = vals.mean()
            s = vals.std(ddof=0)
            out.loc[idx] = (x.loc[idx] - m) / s
    return _winsorize(out, winsor)

def _safe_num(df: pd.DataFrame, col: str, default: float = np.nan) -> pd.Series:
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce")
    return pd.Series([default] * len(df), index=df.index, dtype="float64")

def _align_bool_mask(mask_in, idx) -> pd.Series:
    if isinstance(mask_in, pd.Series):
        m = mask_in.astype(bool)
        if len(m) != len(idx):
            return pd.Series([False] * len(idx), index=idx, dtype="bool")
        if not m.index.equals(idx):
            return pd.Series(m.to_numpy(), index=idx, dtype="bool")
        return m.fillna(False)
    try:
        arr = pd.Series(mask_in)
        if len(arr) != len(idx):
            return pd.Series([False] * len(idx), index=idx, dtype="bool")
        return pd.Series(arr.astype(bool).to_numpy(), index=idx, dtype="bool").fillna(False)
    except Exception:
        return pd.Series([False] * len(idx), index=idx, dtype="bool")

# ----------------------------
# Global/Segment Score (Basis)
# ----------------------------
def score_block(df_in: pd.DataFrame, regime_info: Optional[dict] = None) -> pd.DataFrame:
    d = df_in.copy()
    d["market_cap"] = pd.to_numeric(d.get("market_cap"), errors="coerce")
    d["mc_bucket"] = _mc_bucket(d["market_cap"])

    mom30 = _safe_num(d, "price_change_percentage_30d_in_currency", 0.0)
    mom7  = _safe_num(d, "price_change_percentage_7d_in_currency", 0.0)
    vmc   = _safe_num(d, "volume_mc_ratio", np.nan)
    dd    = _safe_num(d, "ath_change_percentage", np.nan)

    z_mom30 = _z_by_bucket(mom30, d["mc_bucket"])
    z_mom7  = _z_by_bucket(mom7, d["mc_bucket"])
    z_vmc   = _z_by_bucket(vmc, d["mc_bucket"])
    z_dd    = _z_by_bucket(dd, d["mc_bucket"])

    score_global = 0.40 * z_mom30 + 0.25 * z_mom7 + 0.25 * z_vmc - 0.10 * z_dd
    d["score_global"] = score_global.fillna(0.0)
    d["score_segment"] = d["score_global"]
    return d

# ----------------------------
# Early Score
# ----------------------------
def compute_early_score(df_in: pd.DataFrame, peg_mask: Optional[pd.Series] = None, regime_info: Optional[dict] = None) -> pd.DataFrame:
    """Early-Score inkl. Auditspalten risk_regime und beta_pen."""
    d = df_in.copy()
    idx = d.index

    d["market_cap"] = pd.to_numeric(d.get("market_cap"), errors="coerce")
    d["mc_bucket"] = _mc_bucket(d["market_cap"])

    slope_raw = _safe_num(d, "price_change_percentage_30d_in_currency", np.nan)
    volacc    = _safe_num(d, "vol_acc", np.nan)
    breaksc   = _safe_num(d, "breakout_score", np.nan)
    level     = _safe_num(d, "buzz_level", np.nan)
    buzzacc   = _safe_num(d, "buzz_acc", np.nan)

    z_slope = _z_by_bucket(slope_raw, d["mc_bucket"], winsor=2.5)
    z_vol   = _z_by_bucket(volacc,    d["mc_bucket"])
    z_brk   = _z_by_bucket(breaksc,   d["mc_bucket"])
    z_blvl  = _z_by_bucket(level,     d["mc_bucket"])
    z_bacc  = _z_by_bucket(buzzacc,   d["mc_bucket"])

    z_buzz = pd.concat([z_blvl, z_bacc], axis=1).max(axis=1)

    z_slope = _ensure_series(z_slope, idx).fillna(0.0)
    z_vol   = _ensure_series(z_vol,   idx).fillna(0.0)
    z_brk   = _ensure_series(z_brk,   idx).fillna(0.0)
    z_buzz  = _ensure_series(z_buzz,  idx).fillna(0.0)

    early = 0.30 * z_slope + 0.30 * z_vol + 0.30 * z_brk + 0.10 * z_buzz

    overext = slope_raw.fillna(0.0) >= 250.0
    early.loc[overext] = early.loc[overext] * 0.5

    beta_btc = _safe_num(d, "beta_btc", np.nan)
    beta_eth = _safe_num(d, "beta_eth", np.nan)
    beta_eff = pd.concat([beta_btc, beta_eth], axis=1).max(axis=1)

    # Audit defaults
    risk_regime = "neutral"
    beta_pen = pd.Series(1.0, index=idx, dtype="float64")

    if isinstance(regime_info, dict):
        btc_mom30 = float(regime_info.get("btc_mom30", 0.0) or 0.0)
        eth_mom30 = float(regime_info.get("eth_mom30", 0.0) or 0.0)
        risk_off = (btc_mom30 < 0.0) and (eth_mom30 < 0.0)
        risk_regime = "risk_off" if risk_off else "risk_on"
        if risk_off:
            hb = beta_eff - 1.0
            hb = hb.clip(lower=0.0).fillna(0.0)
            damp = 1.0 - 0.15 * hb.clip(upper=2.0)
            beta_pen = damp
            early = early * damp

    if peg_mask is not None:
        m = _align_bool_mask(peg_mask, idx)
        early.values[m.values] = np.nan

    d["early_score"] = early
    d["risk_regime"] = risk_regime if isinstance(risk_regime, str) else str(risk_regime)
    d["beta_pen"] = pd.to_numeric(beta_pen, errors="coerce") if isinstance(beta_pen, pd.Series) else float(beta_pen)
    return d

