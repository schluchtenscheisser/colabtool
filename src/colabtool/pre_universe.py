
# modules/pre_universe.py
from __future__ import annotations

import re
from typing import Tuple
from .utilities import pd, np, logging
from .features import is_stable_like, is_wrapped_like, peg_like_mask
from .data_sources import enrich_categories

# Heuristik-Suffixe für Hebel-ETFs
_LEVERAGE_SUFFIXES = ("UP", "DOWN", "3L", "3S", "4L", "4S", "5L", "5S", "BULL", "BEAR", "ETF")

# BTC/ETH und gängige Derivate/Wraps (IDs von CoinGecko)
_CORE_EXCLUDE_IDS = {
    "bitcoin", "ethereum",
    "wrapped-bitcoin", "wbtc", "huobi-btc", "bitcoin-bep2",
    "lido-staked-ether", "staked-ether", "rocket-pool-eth", "reth", "cbeth", "ankreth",
    "weth", "weth-2", "wrapped-ether",
}

def _is_leveraged(name: str, symbol: str) -> bool:
    s = str(symbol or "").upper()
    n = str(name or "").upper()
    if any(s.endswith(suf) for suf in _LEVERAGE_SUFFIXES):
        return True
    if " LEVERAGED" in n or " ETF" in n:
        return True
    return False

def apply_pre_universe_filters(df_in: pd.DataFrame, min_volume_usd: float = 1_000_000.0) -> pd.DataFrame:
    """P1-Hard-Filter vor MEXC/Kategorien:
    - market_cap > 0
    - total_volume >= min_volume_usd
    - Stable/Pegged/Wrapped per Heuristik
    - BTC/ETH und gängige Derivate/Wraps
    - Hebel/ETF-Tokens
    """
    d = df_in.copy()
    # Basis
    d["market_cap"] = pd.to_numeric(d.get("market_cap"), errors="coerce")
    d["total_volume"] = pd.to_numeric(d.get("total_volume"), errors="coerce")
    # Market Cap Range: 100 Mio < MC < 3 Mrd
    d = d[
        (d["market_cap"] > 100_000_000) &
        (d["market_cap"] < 3_000_000_000) &
        (d["total_volume"] >= float(min_volume_usd))
    ].copy()

    # Heuristiken
    m_stable = d.apply(lambda r: is_stable_like(r.get("name",""), r.get("symbol",""), r.get("id","")), axis=1)
    m_wrapped = d.apply(lambda r: is_wrapped_like(r.get("name",""), r.get("symbol",""), r.get("id","")), axis=1)
    m_peg_lowvar = peg_like_mask(d)  # vorsichtig
    m_lever = d.apply(lambda r: _is_leveraged(r.get("name",""), r.get("symbol","")), axis=1)
    ids = d["id"].astype(str).str.lower()
    m_core = ids.isin(_CORE_EXCLUDE_IDS)

    m_any = m_stable | m_wrapped | m_peg_lowvar | m_lever | m_core
    kept = d.loc[~m_any].copy()
    logging.info(f"[pre] Hard-Filter: {len(d)} -> {len(kept)}")

    return kept

def attach_categories(df_in: pd.DataFrame, sleep_s: float = 0.0) -> pd.DataFrame:
    """Füllt/erstellt die Spalte 'Kategorie' über CoinGecko /coins/{id}."""
    d = df_in.copy()
    ids = d["id"].astype(str).tolist()
    cat_map = enrich_categories(ids, sleep_s=sleep_s)
    d["Kategorie"] = d["id"].astype(str).map(cat_map).fillna("Unknown")
    return d

