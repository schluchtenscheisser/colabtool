"""
__init__.py
-----------
Zentrale Export-Schnittstelle für das Modul `colabtool.features`.
Bündelt alle Submodule und erhält Abwärtskompatibilität zur alten Struktur.
"""

from .feature_block import compute_feature_block
from .fetch_mexc_klines import fetch_mexc_klines
from .compute_mexc_features import compute_mexc_features
from .token_utils import is_stable_like, is_wrapped_like, peg_like_mask

__all__ = [
    "compute_feature_block",
    "fetch_mexc_klines",
    "compute_mexc_features",
    "is_stable_like",
    "is_wrapped_like",
    "peg_like_mask",
]
