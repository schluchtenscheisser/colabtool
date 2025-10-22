# modules/export_helpers.py
from __future__ import annotations
from typing import List
from .utils import pd

def _cols(dfin, names: List[str]) -> list:
    return [c for c in names if c in dfin.columns]

def make_fulldata(df_in: pd.DataFrame) -> pd.DataFrame:
    d = df_in.copy()

    basic = _cols(d, [
        "id","symbol","name","Kategorie","Segment",
        "market_cap","total_volume","circulating_supply",
        "mexc_pair","price_source"
    ])

    tvl = _cols(d, ["tvl_usd","tvl_source","llama_slug"])

    breakout = _cols(d, [
        "dist_90","dist_180","dist_365","p365","donch_width",
        "vol_acc","vol_acc_7d","vol_acc_30d",
        "z_break","z_donch","breakout_score","break_vol_mult",
        "beta_btc","beta_eth"
    ])

    buzz = _cols(d, ["buzz_48h","buzz_7d","buzz_acc"])

    scores = _cols(d, ["score_global","score_segment","early_score","early_prelim"])

    audit = _cols(d, ["risk_regime","beta_pen"])

    order = basic + tvl + breakout + buzz + scores + audit

    # Fallback: falls etwas fehlt, trotzdem returnen
    if not order:
        return d.copy()

    out = d[order].copy()
    return out

