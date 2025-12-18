"""
token_utils.py
--------------
Hilfsfunktionen zur Erkennung von Stablecoins, Wrapped Tokens und Pegged Assets.
Diese Logik stammt ursprünglich aus der alten features.py und wird hier
zentralisiert, um die Architektur klarer zu trennen.

Verwendung:
    from colabtool.features.token_utils import is_stable_like, is_wrapped_like, peg_like_mask
"""

import re
from typing import Union

# -------------------------------------------------------------------
# 🪙 Stablecoin-Erkennung
# -------------------------------------------------------------------
def is_stable_like(symbol: Union[str, None]) -> bool:
    """
    Prüft, ob ein Symbol einem Stablecoin entspricht.
    Beispiele: USDT, USDC, BUSD, DAI, TUSD, FDUSD, LUSD, PYUSD

    Args:
        symbol: Token-Symbol (z. B. 'USDT')

    Returns:
        bool: True, wenn es sich um ein Stablecoin-Symbol handelt.
    """
    if not isinstance(symbol, str) or not symbol:
        return False
    pattern = r"(USDT|USDC|BUSD|DAI|TUSD|FDUSD|LUSD|PYUSD|USD$)"
    return bool(re.search(pattern, symbol.upper()))


# -------------------------------------------------------------------
# 🪙 Wrapped Token-Erkennung
# -------------------------------------------------------------------
def is_wrapped_like(symbol: Union[str, None]) -> bool:
    """
    Prüft, ob ein Token ein Wrapped-Asset ist.
    Beispiele: WBTC, WETH, WWDOGE, WRAPPEDBTC

    Args:
        symbol: Token-Symbol (z. B. 'WBTC')

    Returns:
        bool: True, wenn das Symbol auf ein Wrapped-Asset hindeutet.
    """
    if not isinstance(symbol, str) or not symbol:
        return False
    pattern = r"^(W|WB|WW|WRAPPED)"
    return bool(re.match(pattern, symbol.upper()))


# -------------------------------------------------------------------
# 🪙 Pegged Asset-Erkennung
# -------------------------------------------------------------------
def peg_like_mask(symbol: Union[str, None]) -> bool:
    """
    Prüft, ob ein Token an eine Fiatwährung oder ein Rohstoff-Asset gekoppelt ist.
    Beispiele: EURT, XAUT, SUSD, CUSD, GUSD, PEG-Token

    Args:
        symbol: Token-Symbol (z. B. 'EURT')

    Returns:
        bool: True, wenn das Symbol auf ein Pegged Asset hinweist.
    """
    if not isinstance(symbol, str) or not symbol:
        return False
    pattern = r"(EUR|GBP|XAU|XAG|CUSD|GUSD|SUSD|PEG)"
    return bool(re.search(pattern, symbol.upper()))


# ============================================================================
# 🧩 Erweiterte Klassifizierungsfunktionen (aus legacy features.py übernommen)
# ============================================================================

import pandas as pd

def exclusion_mask(df: pd.DataFrame, cats: pd.Series) -> pd.Series:
    """
    Erzeugt eine Maske für den Ausschluss bestimmter Kategorien.
    Stable-, Wrapped-, PEG- und Leverage-Coins werden ausgeschlossen.
    """
    if 'category' not in df.columns:
        return pd.Series(False, index=df.index)
    cat_lower = cats.str.lower()
    return cat_lower.str.contains('stable|wrapped|peg|leverage|index|tokenized', regex=True, na=False)


def tag_segment(row: dict) -> str:
    """
    Weist einem Coin eine logische Segment-Kategorie zu.
    (z. B. 'stable', 'wrapped', 'meme', 'core', 'defi', etc.)
    """
    name = str(row.get("name", "")).lower()
    symbol = str(row.get("symbol", "")).lower()
    slug = str(row.get("slug", "")).lower()

    if any(k in symbol for k in ["usd", "usdt", "usdc", "busd", "eur"]):
        return "stable"
    if any(k in symbol for k in ["wbtc", "weth", "wrapped"]):
        return "wrapped"
    if any(k in slug for k in ["meme", "doge", "shib", "floki"]):
        return "meme"
    if any(k in slug for k in ["defi", "dex", "swap", "finance"]):
        return "defi"
    if any(k in slug for k in ["eth", "btc", "sol", "avax", "dot"]):
        return "core"
    return "other"
