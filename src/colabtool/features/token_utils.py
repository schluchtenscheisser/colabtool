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
