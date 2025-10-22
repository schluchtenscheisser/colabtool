from __future__ import annotations

import os
import time
from typing import Dict, List, Optional, Tuple

import requests
from .utils import pd, np, logging

# -------------------------
# Konstanten und Pfade
# -------------------------
_MEXC_BASE = "https://api.mexc.com"
_MEXC_EXCHANGE_INFO = f"{_MEXC_BASE}/api/v3/exchangeInfo"
_MEXC_TICKER_24H = f"{_MEXC_BASE}/api/v3/ticker/24hr"

SEED_DIR = "/content/drive/MyDrive/crypto_tool/seeds"
os.makedirs(SEED_DIR, exist_ok=True)
SEED_FILE = os.path.join(SEED_DIR, "seed_mexc_map.csv")  # Columns: symbol, prefer_pair, bad_pairs, confidence

# Bevorzugte Spot-Quotes
_PREFERRED_QUOTES = ["USDT", "USDC", "USD"]
# simple Hebel-/ETF-Heuristik
_LEVERAGE_SUFFIXES = ("UP", "DOWN", "3L", "3S", "4L", "4S", "5L", "5S", "BULL", "BEAR", "ETF")


# -------------------------
# Helpers
# -------------------------
def _is_leveraged_symbol(base: str, full_symbol: str) -> bool:
    b = str(base or "").upper()
    s = str(full_symbol or "").upper()
    return any(b.endswith(suf) or s.endswith(suf) for suf in _LEVERAGE_SUFFIXES)


def _http_json(url: str, params: Optional[dict] = None, tries: int = 3, timeout: int = 20):
    last_err = None
    for i in range(tries):
        try:
            r = requests.get(url, params=params, timeout=timeout)
            if r.status_code == 200:
                return r.json()
            last_err = f"HTTP {r.status_code}"
        except Exception as ex:
            last_err = str(ex)
        time.sleep(min(5 * (i + 1), 10))
    logging.warning(f"[mexc] GET fail {url} | last={last_err}")
    return None


# -------------------------
# Listing-Beschaffung
# -------------------------
def _listing_from_exchange_info() -> pd.DataFrame:
    j = _http_json(_MEXC_EXCHANGE_INFO)
    rows: List[Tuple[str, str, str]] = []
    if j and isinstance(j, dict) and "symbols" in j:
        for sym in j["symbols"]:
            try:
                status = str(sym.get("status", "")).upper()
                if status not in ("TRADING", "ENABLED"):
                    continue
                base = str(sym.get("baseAsset", "")).upper()
                quote = str(sym.get("quoteAsset", "")).upper()
                symbol = str(sym.get("symbol", "")).upper()
                if not base or not quote or not symbol:
                    continue
                if quote not in _PREFERRED_QUOTES:
                    continue
                if _is_leveraged_symbol(base, symbol):
                    continue
                rows.append((base, quote, symbol))
            except Exception:
                continue
    return pd.DataFrame(rows, columns=["base", "quote", "symbol"]).drop_duplicates()


def _listing_from_ticker24() -> pd.DataFrame:
    """
    Fallback: /api/v3/ticker/24hr liefert nur 'symbol'.
    Wir leiten base/quote aus dem Suffix ab: ...USDT | ...USDC | ...USD
    """
    j = _http_json(_MEXC_TICKER_24H)
    rows: List[Tuple[str, str, str]] = []
    if isinstance(j, list):
        for it in j:
            try:
                sym = str(it.get("symbol", "")).upper()
                if not sym:
                    continue
                quote = None
                for q in _PREFERRED_QUOTES:
                    if sym.endswith(q):
                        quote = q
                        base = sym[: -len(q)]
                        break
                if not quote:
                    continue
                base = base.upper()
                if not base:
                    continue
                if _is_leveraged_symbol(base, sym):
                    continue
                rows.append((base, quote, sym))
            except Exception:
                continue
    return pd.DataFrame(rows, columns=["base", "quote", "symbol"]).drop_duplicates()


def _load_mexc_listing() -> pd.DataFrame:
    df = _listing_from_exchange_info()
    if df.empty:
        logging.info("[mexc] exchangeInfo leer → Fallback ticker/24hr")
        df = _listing_from_ticker24()
    if df.empty:
        logging.error("[mexc] kein Spot-Listing (exchangeInfo und ticker/24hr leer)")
    return df


# -------------------------
# Seed-Overrides
# -------------------------
def _load_seed_overrides() -> pd.DataFrame:
    if os.path.isfile(SEED_FILE):
        try:
            df = pd.read_csv(SEED_FILE)
            for col in ["symbol", "prefer_pair", "bad_pairs", "confidence"]:
                if col not in df.columns:
                    df[col] = np.nan
            df["symbol"] = df["symbol"].astype(str).str.upper()
            df["prefer_pair"] = df["prefer_pair"].astype(str).str.upper()
            return df
        except Exception as ex:
            logging.warning(f"[mexc] Seed lesen fehlgeschlagen: {ex}")
    return pd.DataFrame(columns=["symbol", "prefer_pair", "bad_pairs", "confidence"])


def _apply_overrides(df_pairs: pd.DataFrame, seed: pd.DataFrame) -> pd.DataFrame:
    if seed.empty:
        return df_pairs
    seed = seed.dropna(subset=["symbol"]).copy()
    seed["symbol"] = seed["symbol"].astype(str).str.upper()
    seed["prefer_pair"] = seed["prefer_pair"].astype(str).str.upper()
    m = seed.set_index("symbol")["prefer_pair"].to_dict()
    df_pairs["mexc_pair"] = df_pairs.apply(
        lambda r: m.get(r["base_symbol"], r["mexc_pair"]), axis=1
    )
    return df_pairs


def _choose_preferred_pair(rows: pd.DataFrame) -> str:
    # Quote-Priorität: USDT > USDC > USD
    for q in _PREFERRED_QUOTES:
        hit = rows[rows["quote"] == q]
        if not hit.empty:
            return hit.iloc[0]["symbol"]
    return rows.iloc[0]["symbol"]


def _collect_collisions_in_listing(listing: pd.DataFrame) -> Dict[str, int]:
    """Mehrere Paare für gleiche Base → Kollisionen"""
    vc = listing["base"].value_counts()
    d = vc[vc > 1].to_dict()
    if d:
        logging.info(f"[mexc] Base-Kollisionen (mehrere Paare pro Base): {len(d)}")
    return d


# -------------------------
# Öffentliche API
# -------------------------
def apply_mexc_filter(df_in: pd.DataFrame, require_mexc: bool = True) -> pd.DataFrame:
    """
    Filtert Universe auf MEXC-spot-handelbare Assets und mappt auf bevorzugtes Handelspaar.
    Mapping-Heuristik:
      - Nutze CG 'symbol' als MEXC 'base'
      - Wähle pro Base bevorzugtes Paar nach Quote-Priorität
      - Seed-Overrides ermöglichen explizite Paarwahl pro Base
    """
    df = df_in.copy()
    df["symbol"] = df["symbol"].astype(str).str.upper()

    listing = _load_mexc_listing()
    if listing is None or listing.empty:
        if require_mexc:
            raise RuntimeError("MEXC Spot-Listing leer. API down oder Netzwerkproblem.")
        logging.warning("[mexc] Listing leer → kein Filter möglich")
        df["mexc_pair"] = np.nan
        return df

    _ = _collect_collisions_in_listing(listing)

    grouped = listing.groupby("base")
    pair_map = {b: _choose_preferred_pair(g) for b, g in grouped}

    # rohes Mapping: CG-Symbol → Base
    df["base_symbol"] = df["symbol"]
    df["mexc_pair"] = df["base_symbol"].map(pair_map)

    # Seed-Overrides anwenden
    seed = _load_seed_overrides()
    df = _apply_overrides(df, seed)

    if require_mexc:
        before = len(df)
        df = df[~df["mexc_pair"].isna()].copy()
        logging.info(f"[mexc] Require MEXC: {before} -> {len(df)}")

    return df.drop(columns=["base_symbol"], errors="ignore")


def export_mexc_seed_template(df: pd.DataFrame, collisions_only: bool = True) -> None:
    """
    Exportiert Seed-Template für Ticker-Kollisionen und Paar-Präferenzen.
    - collisions_only=True: nur Bases mit mehreren möglichen Paaren
    """
    try:
        listing = _load_mexc_listing()
        if listing is None or listing.empty:
            return
    except Exception:
        return

    coll_bases = set(listing["base"].value_counts()[lambda s: s > 1].index.tolist())
    cand = df.copy()
    cand["symbol"] = cand["symbol"].astype(str).str.upper()
    if collisions_only:
        cand = cand[cand["symbol"].isin(coll_bases)]

    out = pd.DataFrame({
        "symbol": sorted(cand["symbol"].unique()),
        "prefer_pair": "",
        "bad_pairs": "",
        "confidence": ""
    })

    try:
        out.to_csv(SEED_FILE, index=False)
        logging.info(f"[mexc] Seed-Template exportiert: {SEED_FILE} ({len(out)} Zeilen)")
    except Exception as ex:
        logging.warning(f"[mexc] Seed-Export fehlgeschlagen: {ex}")

