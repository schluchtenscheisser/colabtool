
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

# ================================================================
# 🧠 SCORE_BLOCK – Global & Segment Scoring mit Regime und Dämpfung
# ================================================================
def score_block(df_in: pd.DataFrame, regime_info: dict | None = None) -> pd.DataFrame:
    """
    Berechnet den globalen und segmentbasierten Score für alle Assets.
    Nutzt Z-Norm-Werte aus Momentum, Volumen, Drawdown und Breakout.
    Regime-Logik & Beta-Dämpfung integriert.
    """
    df = df_in.copy()

    # ------------------------------------------------------------
    # Sicherstellen, dass benötigte Felder existieren
    # ------------------------------------------------------------
    required_cols = [
        "mom_7d_pct", "mom_30d_pct", "volume_mc_ratio",
        "ath_drawdown_pct", "beta_btc", "beta_eth"
    ]
    for col in required_cols:
        if col not in df.columns:
            df[col] = np.nan

    # ------------------------------------------------------------
    # Z-Normalisierung mit Winsorizing
    # ------------------------------------------------------------
    def _z(series: pd.Series) -> pd.Series:
        if series.std(ddof=0) == 0 or series.isna().all():
            return pd.Series(0, index=series.index)
        z = (series - series.mean()) / (series.std(ddof=0) + 1e-9)
        return np.clip(z, -2.5, 2.5)

    df["z_mom7"] = _z(df["mom_7d_pct"])
    df["z_mom30"] = _z(df["mom_30d_pct"])
    df["z_vmc"] = _z(df["volume_mc_ratio"])
    df["z_dd"] = -_z(df["ath_drawdown_pct"].abs())  # stärkerer Drawdown = negativer Score

    # ------------------------------------------------------------
    # Regime- & Beta-Dämpfung
    # ------------------------------------------------------------
    # Berechne Beta-Penalty als Mittelwert ggü. BTC & ETH
    df["beta_pen"] = 1.0 - np.minimum(1.0, 0.5 * (df["beta_btc"].fillna(1) + df["beta_eth"].fillna(1)) / 2)
    df["beta_pen"] = np.clip(df["beta_pen"], 0.5, 1.0)

    # ------------------------------------------------------------
    # Globaler Score (Momentum + Volumen + Drawdown)
    # ------------------------------------------------------------
    score_global = (
        0.40 * df["z_mom30"] +
        0.25 * df["z_mom7"] +
        0.25 * df["z_vmc"] +
        0.10 * df["z_dd"]
    )

    # Dämpfung bei überhitzten Coins (≥ +250% in 30d)
    overheat_mask = df["mom_30d_pct"].fillna(0) >= 250
    score_global = score_global * np.where(overheat_mask, 0.5, 1.0)

    # Beta-Dämpfung anwenden
    score_global = score_global * df["beta_pen"]

    # ------------------------------------------------------------
    # Ergebnis speichern
    # ------------------------------------------------------------
    df["score_global"] = score_global.fillna(0)
    df["score_segment"] = df["score_global"]  # segmentabhängig erweiterbar

    return df


# ================================================================
# 🚀 COMPUTE_EARLY_SCORE – Früherkennungsscore gemäß Zielbild
# ================================================================
def compute_early_score(df_in: pd.DataFrame) -> pd.DataFrame:
    """
    Berechnet den Early-Signal-Score zur Früherkennung starker Momentumbewegungen.
    Features: z_slope, z_volacc, z_break, z_buzz_level/acc (kombiniert)
    """
    df = df_in.copy()

    # ------------------------------------------------------------
    # Sicherstellen, dass benötigte Felder existieren
    # ------------------------------------------------------------
    required_cols = ["z_slope", "z_volacc", "z_break", "z_buzz_level", "z_buzz_acc", "mom_30d_pct"]
    for col in required_cols:
        if col not in df.columns:
            df[col] = 0

    # Kombinierter Buzz (max zwischen Level und Acceleration)
    df["z_buzz_combined"] = df[["z_buzz_level", "z_buzz_acc"]].max(axis=1)

    # Dämpfung bei überhitzten Coins (≥ +250% in 30d)
    damp_factor = np.where(df["mom_30d_pct"].fillna(0) >= 250, 0.5, 1.0)

    # Early Score gemäß Zielbild
    early = (
        0.30 * np.clip(df["z_slope"], -2.5, 2.5) +
        0.30 * df["z_volacc"] +
        0.30 * df["z_break"] +
        0.10 * df["z_buzz_combined"]
    ) * damp_factor

    df["early_score"] = np.clip(early, -3, 3).fillna(0)

    return df
