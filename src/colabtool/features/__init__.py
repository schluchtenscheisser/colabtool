"""
__init__.py
-----------
Bündelt alle Feature-Module und stellt Abwärtskompatibilität zur alten Struktur her.
"""

from .feature_block import compute_feature_block
from .fetch_mexc_klines import fetch_mexc_klines
from .compute_mexc_features import compute_mexc_features

import re

__all__ = [
    "compute_feature_block",
    "fetch_mexc_klines",
    "compute_mexc_features",
    "is_stable_like",
    "is_wrapped_like",
    "peg_like_mask",
]

# -------------------------------------------------------------------
# 🧩 Alte Helper-Funktionen aus dem früheren features.py
# -------------------------------------------------------------------
def is_stable_like(symbol: str) -> bool:
    """
    Prüft, ob ein Coin ein Stablecoin ist.
    Beispiele: USDT, USDC, BUSD, DAI, TUSD
    """
    if not isinstance(symbol, str):
        return False
    pattern = r"(USDT|USDC|BUSD|DAI|TUSD|FDUSD|LUSD|USD$)"
    return bool(re.search(pattern, symbol.upper()))


def is_wrapped_like(symbol: str) -> bool:
    """
    Prüft, ob ein Token ein 'Wrapped'-Token ist (z. B. WBTC, WETH).
    """
    if not isinstance(symbol, str):
        return False
    pattern = r"^(W|WB|WW|WRAPPED)"
    return bool(re.match(pattern, symbol.upper()))


def peg_like_mask(symbol: str) -> bool:
    """
    Prüft, ob ein Coin an eine andere Währung oder Asset-Klasse 'gepegt' ist.
    Beispiele: EURT, XAUT, SUSD, CUSD, GUSD
    """
    if not isinstance(symbol, str):
        return False
    pattern = r"(EUR|GBP|XAU|XAG|CUSD|GUSD|SUSD|PEG)"
    return bool(re.search(pattern, symbol.upper()))
