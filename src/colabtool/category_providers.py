# modules/category_providers.py
# Hybrid-Kategorien: CoinGecko → CoinMarketCap → Messari → CoinPaprika
# Ziel: Stable/Wrapped/Bridged zuverlässig erkennen, 429 minimieren (TTL + Delta).

from __future__ import annotations
import os, json, time, re
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

import requests
from .utils import pd, np, logging

try:
    # primär CG-Variante aus euren Datenquellen nutzen (inkl. interner CG-Ratensteuerung)
    from .data_sources import enrich_categories as cg_enrich_categories
except Exception:
    cg_enrich_categories = None

# -------- ENV / Konst --------
_CACHE_ROOT = os.path.join(os.getcwd(), "cache")
_PROV_CACHE = os.path.join(_CACHE_ROOT, "categories_cache_hybrid.json")
os.makedirs(_CACHE_ROOT, exist_ok=True)

_CMC_URL = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/info"
_MESSARI_URL = "https://data.messari.io/api/v1/assets"
_PAPRIKA_SEARCH = "https://api.coinpaprika.com/v1/search"
_PAPRIKA_COIN = "https://api.coinpaprika.com/v1/coins/{id}"

_CMC_KEY = os.getenv("CMC_API_KEY", "").strip()
_MESSARI_KEY = os.getenv("MESSARI_API_KEY", "").strip()
_PAPRIKA_KEY = os.getenv("COINPAPRIKA_API_KEY", "").strip()  # idR nicht nötig

# Budget für alle Fallback-Provider zusammen
_PROVIDERS_BUDGET_S = float(os.getenv("PROVIDERS_CATS_TIME_BUDGET_S", "90"))

# Heuristik-Mapping: Tags/Begriffe → Kategorie
_TAG_RULES = [
    (re.compile(r"stable", re.I), "Stable"),
    (re.compile(r"\bpeg|pegged|binance-peg", re.I), "Pegged"),
    (re.compile(r"wrap|wrapped|bridged|wormhole|anyswap", re.I), "Wrapped/Bridged"),
]

def _now_utc():
    return datetime.now(timezone.utc)

# -------- Cache --------
def _load_cache() -> dict:
    try:
        if os.path.isfile(_PROV_CACHE):
            return json.load(open(_PROV_CACHE, "r"))
    except Exception:
        pass
    return {}

def _save_cache(cache: dict) -> None:
    try:
        json.dump(cache, open(_PROV_CACHE, "w"))
    except Exception:
        pass

def _cache_get(cache: dict, cid: str, ttl_days: int) -> Optional[str]:
    v = cache.get(cid)
    if not isinstance(v, dict):
        return None
    try:
        ts = datetime.fromisoformat(v.get("ts"))
    except Exception:
        return None
    if (_now_utc() - ts) > timedelta(days=max(1, int(ttl_days))):
        return None
    return v.get("cat")

def _cache_set(cache: dict, cid: str, cat: str) -> None:
    cache[cid] = {"cat": cat or "Unknown", "ts": _now_utc().isoformat()}

# -------- Utils --------
def _infer_from_tags(tags: List[str]) -> Optional[str]:
    if not tags:
        return None
    txt = " ".join([str(t) for t in tags])
    for rx, lab in _TAG_RULES:
        if rx.search(txt):
            return lab
    return None

def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(s or "").lower())

# -------- Provider-Clients --------
def _cmc_get_map_by_symbols(symbols: List[str]) -> Dict[str, dict]:
    """
    CMC info by symbol. Symbole sind nicht eindeutig; wir geben Mapping symbol -> first item.
    Besser: später über Name-Similarity verfeinern.
    """
    if not _CMC_KEY or not symbols:
        return {}
    headers = {"X-CMC_PRO_API_KEY": _CMC_KEY, "Accept": "application/json"}
    out: Dict[str, dict] = {}
    # Batches à 50
    for i in range(0, len(symbols), 50):
        batch = list({s for s in symbols[i:i+50] if s})
        params = {"symbol": ",".join(batch)}
        try:
            r = requests.get(_CMC_URL, headers=headers, params=params, timeout=20)
            if r.status_code != 200:
                logging.warning(f"[cmc] HTTP {r.status_code}: {r.text[:120]}")
                continue
            j = r.json()
            data = j.get("data", {})
            for sym, lst in (data.items() if isinstance(data, dict) else []):
                if isinstance(lst, list) and lst:
                    out[sym.upper()] = lst[0]
        except Exception as ex:
            logging.warning(f"[cmc] error: {ex}")
    return out

def _messari_get_profile(slug: str) -> Optional[dict]:
    if not slug:
        return None
    headers = {"Accept": "application/json"}
    if _MESSARI_KEY:
        headers["x-messari-api-key"] = _MESSARI_KEY
    url = f"{_MESSARI_URL}/{slug}/profile"
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

def _paprika_find_id(query: str) -> Optional[str]:
    try:
        r = requests.get(_PAPRIKA_SEARCH, params={"q": query, "c": "currencies", "limit": 1}, timeout=15)
        if r.status_code != 200:
            return None
        j = r.json()
        hits = j.get("currencies") or []
        if hits:
            return hits[0].get("id")
    except Exception:
        pass
    return None

def _paprika_get_coin(cid: str) -> Optional[dict]:
    try:
        r = requests.get(_PAPRIKA_COIN.format(id=cid), timeout=15)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

# -------- Public: Hybrid-Enrichment --------
def enrich_categories_hybrid(
    df_in: pd.DataFrame,
    ids: List[str],
    ttl_days: int = 10,
    max_fetch: int = 300,
    prefer_cg_first: bool = True
) -> Dict[str, str]:
    """
    Liefert {id: Kategorie}. Reihenfolge:
      1) Cache (TTL)
      2) CoinGecko (falls prefer_cg_first)
      3) CMC (tags), Messari (tags/sector), Paprika (tags)
    Nur Delta wird je Provider angefragt. 'max_fetch' limitiert Anfragen je Run.
    """
    ids = [str(x) for x in (ids or [])]
    if not ids:
        return {}

    cache = _load_cache()
    out: Dict[str, str] = {}
    pending: List[str] = []

    # 1) Cache
    for cid in ids:
        hit = _cache_get(cache, cid, ttl_days)
        if hit:
            out[cid] = hit
        else:
            pending.append(cid)

    if not pending:
        return out

    # 2) CoinGecko zuerst (falls gewünscht)
    budget_s = _PROVIDERS_BUDGET_S
    t0 = time.perf_counter()

    def _within_budget() -> bool:
        return (time.perf_counter() - t0) < budget_s

    def _set_many(m: Dict[str, str]):
        for k, v in (m or {}).items():
            out[k] = v or "Unknown"
            _cache_set(cache, k, out[k])

    if prefer_cg_first and cg_enrich_categories:
        try:
            cg_ids = pending[:max_fetch]
            _set_many(cg_enrich_categories(cg_ids, sleep_s=0.0))
            pending = [cid for cid in pending if cid not in out]
        except Exception as ex:
            logging.warning(f"[hybrid] CG enrich err: {ex}")

    if not pending:
        _save_cache(cache)
        return out

    # Für Fallbacks brauchen wir symbol+name
    df = df_in[df_in["id"].astype(str).isin(pending)].copy()
    df["symbol"] = df["symbol"].astype(str).str.upper()
    df["name"] = df["name"].astype(str)

    # 3) CMC (tags) – by symbol, bei Kollision Name vergleichen
    if _CMC_KEY and _within_budget():
        try:
            symbols = df["symbol"].unique().tolist()
            m = _cmc_get_map_by_symbols(symbols)
            for _, r in df.iterrows():
                if r["id"] in out:
                    continue
                sym = r["symbol"].upper()
                meta = m.get(sym)
                if not meta:
                    continue
                tags = meta.get("tags") or []
                cat = _infer_from_tags(tags) or (tags[0] if tags else None)
                if not cat:
                    continue
                # grobe Namensprüfung (falls Duplikate)
                cname = meta.get("name", "")
                if cname and _norm(cname)[:6] != _norm(r["name"])[:6]:
                    # mögliches anderes Asset mit gleichem Symbol
                    continue
                out[r["id"]] = cat
                _cache_set(cache, r["id"], cat)
                if len(out) >= len(ids):
                    break
        except Exception as ex:
            logging.warning(f"[hybrid] CMC err: {ex}")

    pending = [cid for cid in pending if cid not in out]
    if not pending or not _within_budget():
        _save_cache(cache)
        return out

    # 4) Messari (sector/tags) – heuristisch über slug aus Symbol
    if _within_budget():
        try:
            for _, r in df.iterrows():
                if r["id"] in out:
                    continue
                slug = r["symbol"].lower()
                j = _messari_get_profile(slug)
                if not j:
                    # Fallback Versuch mit namelower ohne Sonderzeichen
                    slug2 = _norm(r["name"])
                    if slug2:
                        j = _messari_get_profile(slug2)
                if not j:
                    continue
                prof = j.get("data", {}).get("profile", {})
                sect = prof.get("sector")
                tags = prof.get("tags") or []
                cat = _infer_from_tags(tags) or sect
                if not cat:
                    continue
                out[r["id"]] = cat
                _cache_set(cache, r["id"], cat)
                if not _within_budget():
                    break
        except Exception as ex:
            logging.warning(f"[hybrid] Messari err: {ex}")

    pending = [cid for cid in pending if cid not in out]
    if not pending or not _within_budget():
        _save_cache(cache)
        return out

    # 5) CoinPaprika (tags via search→coin)
    try:
        for _, r in df.iterrows():
            if r["id"] in out:
                continue
            pid = _paprika_find_id(r["name"])
            if not pid:
                pid = _paprika_find_id(r["symbol"])
            if not pid:
                continue
            meta = _paprika_get_coin(pid) or {}
            tags = [t.get("name","") for t in (meta.get("tags") or [])]
            cat = _infer_from_tags(tags) or (tags[0] if tags else None)
            if not cat:
                continue
            out[r["id"]] = cat
            _cache_set(cache, r["id"], cat)
            if not _within_budget():
                break
    except Exception as ex:
        logging.warning(f"[hybrid] Paprika err: {ex}")

    _save_cache(cache)

    # NEU: PIT-Snapshot schreiben, falls asof_date gesetzt
    if "asof_date" in df_in.attrs and len(out) > 0:
        try:
            from colabtool.data_sources import persist_pit_snapshot
            snapshot_df = pd.DataFrame([
                {"id": k, "category": v} for k, v in out.items()
            ])
            persist_pit_snapshot(snapshot_df, kind="cg_categories", date=df_in.attrs["asof_date"])
        except Exception as ex:
            logging.warning(f"[pit] Failed to snapshot categories: {ex}")

    return out

# === Dummy-Fallback für PIT-Snapshot ===
def get_cg_categories() -> list[dict]:
    """Dummy-Version für PIT-Snapshot – liefert minimale Kategorien"""
    return [
        {"id": "defi", "name": "Decentralized Finance"},
        {"id": "nft", "name": "NFT"},
        {"id": "gaming", "name": "Gaming"},
    ]
