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
    """Erkennt ETF/Leveraged Tokens anhand Symbol oder Name."""
    s = str(symbol or "").upper()
    n = str(name or "").upper()
    if any(s.endswith(suf) for suf in _LEVERAGE_SUFFIXES):
        return True
    if " LEVERAGED" in n or " ETF" in n:
        return True
    return False


def apply_pre_universe_filters(df_in: pd.DataFrame, min_volume_usd: float = 300_000.0) -> pd.DataFrame:
    """P1-Hard-Filter vor MEXC/Kategorien:
    - market_cap > 0
    - total_volume >= min_volume_usd
    - Stable/Pegged/Wrapped per Heuristik
    - BTC/ETH und gängige Derivate/Wraps
    - Hebel/ETF-Tokens
    """
    logging.info("[pre] ==== STARTE apply_pre_universe_filters ====")
    logging.info(f"[pre] Eingangsgröße: {len(df_in)} Zeilen, Columns: {list(df_in.columns)}")

    d = df_in.copy()

    # Basis
    d["market_cap"] = pd.to_numeric(d.get("market_cap"), errors="coerce")
    d["total_volume"] = pd.to_numeric(d.get("total_volume"), errors="coerce")

    logging.info(
        f"[pre] Vor Rangefilter: gültige MarketCap={d['market_cap'].notna().sum()}, "
        f"gültige Volume={d['total_volume'].notna().sum()}"
    )

    # Market Cap Range: 100 Mio < MC < 3 Mrd
    d = d[
        (d["market_cap"] > 100_000_000)
        & (d["market_cap"] < 3_000_000_000)
        & (d["total_volume"] >= float(min_volume_usd))
    ].copy()
    logging.info(f"[pre] Nach Rangefilter (MC + Volumen): {len(d)} Zeilen übrig")

    if d.empty:
        logging.warning("[pre] ⚠️ Keine Zeilen nach Rangefilter — prüfe MarketCap/Volumen-Spalten!")
        return d

    # Heuristiken
    logging.info("[pre] Berechne heuristische Masken (Stable, Wrapped, PEG, Leverage, Core) ...")
    m_stable = d.apply(lambda r: is_stable_like(r.get("name",""), r.get("symbol",""), r.get("id","")), axis=1)
    m_wrapped = d.apply(lambda r: is_wrapped_like(r.get("name",""), r.get("symbol",""), r.get("id","")), axis=1)
    m_peg_lowvar = peg_like_mask(d)  # vorsichtig
    m_lever = d.apply(lambda r: _is_leveraged(r.get("name",""), r.get("symbol","")), axis=1)
    ids = d["id"].astype(str).str.lower()
    m_core = ids.isin(_CORE_EXCLUDE_IDS)

    logging.info(
        f"[pre] Maskenzusammenfassung → "
        f"Stable={m_stable.sum()}, Wrapped={m_wrapped.sum()}, PEG={m_peg_lowvar.sum()}, "
        f"Leveraged={m_lever.sum()}, Core={m_core.sum()}"
    )

    # Debug: Beispiele zeigen
    for mask_name, mask_series in {
        "Stable": m_stable,
        "Wrapped": m_wrapped,
        "PEG": m_peg_lowvar,
        "Leveraged": m_lever,
        "Core": m_core,
    }.items():
        examples = d.loc[mask_series, ["id", "symbol", "name"]].head(3).to_dict("records")
        if examples:
            logging.info(f"[pre] Beispiele {mask_name}: {examples}")

    # ⚠️ Temporär PEG/Leverage-Filter deaktiviert (Debug)
    logging.warning("[pre] PEG- und Leveraged-Filter vorübergehend deaktiviert (Debug-Modus aktiv)")
    m_any = m_stable | m_wrapped | m_core
    kept = d.loc[~m_any].copy()

    logging.info(f"[pre] Hard-Filter: {len(d)} -> {len(kept)} (nach Ausschlussmasken)")
    if kept.empty:
        logging.warning("[pre] ⚠️ Nach allen Filtern keine Zeilen mehr – prüfe Heuristik und Rangegrenzen!")

    logging.info("[pre] ==== ENDE apply_pre_universe_filters ====")
    return kept


def attach_categories(df_in: pd.DataFrame, sleep_s: float = 0.0) -> pd.DataFrame:
    """Füllt/erstellt die Spalte 'Kategorie' über CoinGecko /coins/{id}."""
    d = df_in.copy()
    ids = d["id"].astype(str).tolist()
    cat_map = enrich_categories(ids, sleep_s=sleep_s)
    d["Kategorie"] = d["id"].astype(str).map(cat_map).fillna("Unknown")
    logging.info(f"[pre] attach_categories abgeschlossen – {len(d)} Zeilen mit Kategorie")
    return d
