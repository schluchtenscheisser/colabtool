# modules/data_sources.py
from __future__ import annotations

import os
import json
import time
from typing import Dict, List, Optional, Union
from pathlib import Path

import requests
from .utils import pd, np, logging, CACHE_DIR as _UTILS_CACHE_DIR

__all__ = [
    "cg_markets",
    "enrich_categories",
    "map_tvl",
    "update_seen_ids",
    "cg_market_chart",
]

# ----------------------------
# ENV parsing (robust gegen Kommentare)
# ----------------------------
def _env_str(name: str, default: str = "") -> str:
    val = os.getenv(name, None)
    if val is None:
        return default
    s = str(val).strip().strip('"').strip("'")
    if not s:
        return default
    return s.split(maxsplit=1)[0]

def _env_bool(name: str, default: bool = False) -> bool:
    raw = _env_str(name, "1" if default else "0").lower()
    return raw in {"1", "true", "yes", "y", "on"}

def _env_int(name: str, default: int) -> int:
    s = _env_str(name, str(default))
    try:
        return int(float(s))
    except Exception:
        return default

def _env_float(name: str, default: float) -> float:
    s = _env_str(name, str(default))
    try:
        return float(s)
    except Exception:
        return default

def _is_colab() -> bool:
    try:
        import google.colab  # noqa: F401
        return True
    except Exception:
        return False

# ----------------------------
# ENV & Defaults
# ----------------------------
_FORCE_FREE = _env_bool("CG_FORCE_FREE", True)  # Free-API standard
_CG_KEY = _env_str("COINGECKO_API_KEY", "")
_HAS_PRO = bool(_CG_KEY) and not _FORCE_FREE

_PRO_BASE = "https://pro-api.coingecko.com/api/v3"
_FREE_BASE = "https://api.coingecko.com/api/v3"

_CG_MAX_ATTEMPTS = _env_int("CG_MAX_ATTEMPTS", 3)
_CG_SKIP_AFTER_429 = _env_int("CG_SKIP_AFTER_429", 1)
_CG_RETRY_AFTER_CAP_S = _env_float("CG_RETRY_AFTER_CAP_S", 20.0)
_CG_BACKOFF_BASE_S = _env_float("CG_BACKOFF_BASE_S", 2.0)
_CG_MIN_INTERVAL_S = _env_float("CG_MIN_INTERVAL_S", 1.5)

_CG_CATS_TIME_BUDGET_S = _env_float("CG_CATS_TIME_BUDGET_S", 300.0)

# ----------------------------
# Pfade/Cache/Seeds (CI-sicher, kein erzwungenes /content)
# ----------------------------
_CACHE_DIR: Path = Path(os.getenv("CACHE_DIR", str(_UTILS_CACHE_DIR)))

def _resolve_seed_dir() -> Path:
    env = os.getenv("SEED_DIR")
    if env:
        return Path(env)
    if _is_colab():
        return Path("/content/drive/MyDrive/crypto_tool/seeds")
    return Path.cwd() / "seeds"

_SEED_DIR: Path = _resolve_seed_dir()

# Verzeichnisse best-effort anlegen
for _p in (_CACHE_DIR, _SEED_DIR):
    try:
        _p.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

_SEEN_PATH: Path = _CACHE_DIR / "seen_ids.json"
_TVL_SEED: Path = _SEED_DIR / "seed_tvl_map.csv"

# ----------------------------
# Sessions
# ----------------------------
_session_pro = requests.Session()
_session_pro.headers.update({
    "Accept": "application/json",
    "User-Agent": "mexc-early-screener/1.0",
})
if _HAS_PRO:
    _session_pro.headers.update({"x-cg-pro-api-key": _CG_KEY})

_session_free = requests.Session()
_session_free.headers.update({
    "Accept": "application/json",
    "User-Agent": "mexc-early-screener/1.0",
})

# ----------------------------
# HTTP helpers
# ----------------------------
_last_call = 0.0

def _sleep_min_interval():
    global _last_call
    dt = time.time() - _last_call
    wait = max(0.0, _CG_MIN_INTERVAL_S - dt)
    if wait > 0:
        time.sleep(wait)

def _one_get(session: requests.Session, base: str, path: str, params: dict, attempts: int) -> Optional[Union[dict, list]]:
    global _last_call
    url = f"{base}{path}"
    for att in range(1, attempts + 1):
        _sleep_min_interval()
        try:
            r = session.get(url, params=params, timeout=30)
            _last_call = time.time()
            if r.status_code == 200:
                return r.json()
            if r.status_code in (400, 401, 403, 404):
                logging.warning(f"[cg] GET {url} err: {r.status_code} {r.reason}")
                return None
            if r.status_code == 429:
                logging.warning(f"[cg] 429 on {url} → backoff {_CG_RETRY_AFTER_CAP_S:.2f}s, attempt {att}/{attempts}")
                if _CG_SKIP_AFTER_429 >= 1:
                    return None
                time.sleep(_CG_RETRY_AFTER_CAP_S)
                continue
            wait = min(_CG_RETRY_AFTER_CAP_S, _CG_BACKOFF_BASE_S * att)
            logging.warning(f"[cg] HTTP {r.status_code} on {url} → retry in {wait:.1f}s ({att}/{attempts})")
            time.sleep(wait)
        except requests.RequestException as ex:
            wait = min(_CG_RETRY_AFTER_CAP_S, _CG_BACKOFF_BASE_S * att)
            logging.warning(f"[cg] GET {url} err: {ex} → retry in {wait:.1f}s ({att}/{attempts})")
            time.sleep(wait)
    return None

def _sanitize_params_for_free(params: dict) -> dict:
    p = dict(params or {})
    p.pop("x_cg_pro_api_key", None)
    return p

def _cg_get(path: str, params: Optional[dict] = None, attempts: int = None) -> Optional[Union[dict, list]]:
    """Free-first. PRO nur, wenn verfügbar und Free nichts liefert."""
    max_att = attempts if attempts is not None else _CG_MAX_ATTEMPTS
    params = dict(params or {})

    # Free zuerst
    j = _one_get(_session_free, _FREE_BASE, path, _sanitize_params_for_free(params), max_att)
    if isinstance(j, (dict, list)) or not _HAS_PRO:
        return j

    # Optional PRO
    p2 = dict(params); p2["x_cg_pro_api_key"] = _CG_KEY
    j2 = _one_get(_session_pro, _PRO_BASE, path, p2, max_att)
    return j2

# ----------------------------
# Public API
# ----------------------------
def cg_markets(vs: str = "usd", per_page: int = 250, pages: int = 1) -> pd.DataFrame:
    out: List[pd.DataFrame] = []
    for p in range(1, int(pages) + 1):
        params = {
            "vs_currency": str(vs or "usd").lower(),
            "order": "market_cap_desc",
            "per_page": int(per_page),
            "page": int(p),
            "sparkline": "false",
            "price_change_percentage": "7d,30d",
        }
        j = _cg_get("/coins/markets", params=params)
        if not isinstance(j, list) or not j:
            if p == 1:
                logging.warning("[cg] /coins/markets leer oder Fehler")
            break
        dfp = pd.json_normalize(j)
        keep = [
            "id","symbol","name","market_cap","total_volume",
            "price_change_percentage_7d_in_currency","price_change_percentage_30d_in_currency",
            "ath_change_percentage"
        ]
        for k in keep:
            if k not in dfp.columns:
                dfp[k] = np.nan
        out.append(dfp[keep].copy())

    if not out:
        return pd.DataFrame(columns=[
            "id","symbol","name","market_cap","total_volume",
            "price_change_percentage_7d_in_currency","price_change_percentage_30d_in_currency",
            "ath_change_percentage"
        ])

    df = pd.concat(out, ignore_index=True)
    for c in ["market_cap","total_volume","price_change_percentage_7d_in_currency","price_change_percentage_30d_in_currency","ath_change_percentage"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

def enrich_categories(ids: List[str], sleep_s: float = 0.0) -> Dict[str, str]:
    """Grobe Kategorien je Coin. Zeitbudget; 400/404 → Unknown."""
    ids = [str(x) for x in (ids or [])]
    if not ids:
        return {}
    budget_end = time.time() + _CG_CATS_TIME_BUDGET_S
    out: Dict[str, str] = {}
    for cid in ids:
        if time.time() > budget_end:
            logging.info("[cg] Kategorien-Budget erreicht → Rest Unknown")
            break
        params = {
            "localization": "false",
            "tickers": "false",
            "market_data": "false",
            "community_data": "false",
            "developer_data": "false",
            "sparkline": "false",
        }
        j = _cg_get(f"/coins/{cid}", params=params, attempts=max(1, _CG_MAX_ATTEMPTS))
        if isinstance(j, dict):
            cats = j.get("categories") or []
            val = cats[0] if isinstance(cats, list) and cats else None
            out[cid] = (str(val)[:80]) if val else "Unknown"
        else:
            out[cid] = "Unknown"
        if sleep_s and sleep_s > 0:
            time.sleep(float(sleep_s))
    for cid in ids:
        out.setdefault(cid, "Unknown")
    return out

def map_tvl(df: pd.DataFrame) -> pd.DataFrame:
    """Seed-basierte TVL-Mappung (seed_tvl_map.csv: id, tvl_usd, llama_slug)."""
    d = df.copy()
    d["tvl_usd"] = np.nan
    if _TVL_SEED.is_file():
        try:
            sm = pd.read_csv(_TVL_SEED)
            sm["id"] = sm["id"].astype(str)
            if "tvl_usd" in sm.columns:
                sm["tvl_usd"] = pd.to_numeric(sm["tvl_usd"], errors="coerce")
            else:
                sm["tvl_usd"] = np.nan
            m = sm.set_index("id")["tvl_usd"].to_dict()
            d["tvl_usd"] = d["id"].astype(str).map(m)
        except Exception as ex:
            logging.warning(f"[tvl] Seed-Map lesen fehlgeschlagen: {ex}")
    return d

def update_seen_ids(ids: List[str]) -> Dict[str, int]:
    """Persistente Liste gesehener CoinGecko-IDs zur Erkennung von New-Listings."""
    ids = [str(x) for x in (ids or [])]
    try:
        seen = json.load(_SEEN_PATH.open("r")) if _SEEN_PATH.is_file() else []
    except Exception:
        seen = []
    sset = set(seen)
    new = 0
    for cid in ids:
        if cid not in sset:
            sset.add(cid)
            new += 1
    try:
        json.dump(sorted(list(sset)), _SEEN_PATH.open("w"))
    except Exception:
        pass
    return {"total_seen": len(sset), "added": new}

# ----------------------------
# Charts für Backtest
# ----------------------------
def _chart_cache_path(coin_id: str, vs: str, days: int, interval: str) -> Path:
    fn = f"cg_chart_{coin_id}_{vs}_{days}_{interval}.json".replace("/", "_")
    p = _CACHE_DIR / fn
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    return p

def cg_market_chart(coin_id: str, vs: str = "usd", days: int = 60, interval: str = "daily", ttl_s: int = 6*3600) -> Optional[dict]:
    """
    Wrapper für /coins/{id}/market_chart
    Free-first; optional PRO wenn verfügbar.
    Lokaler Cache.
    """
    coin_id = str(coin_id).strip().lower()
    vs = str(vs).strip().lower() or "usd"
    days = int(max(1, min(days, 3650)))
    interval = "daily" if str(interval).lower() != "hourly" else "hourly"

    cpath = _chart_cache_path(coin_id, vs, days, interval)
    try:
        if cpath.is_file() and (time.time() - cpath.stat().st_mtime < ttl_s):
            return json.load(cpath.open("r"))
    except Exception:
        pass

    params = {"vs_currency": vs, "days": days, "interval": interval}
    j = _one_get(_session_free, _FREE_BASE, f"/coins/{coin_id}/market_chart", params, max(1, _CG_MAX_ATTEMPTS))
    if not isinstance(j, dict) or not any(k in j for k in ("prices", "market_caps", "total_volumes")):
        if _HAS_PRO:
            p2 = dict(params); p2["x_cg_pro_api_key"] = _CG_KEY
            j = _one_get(_session_pro, _PRO_BASE, f"/coins/{coin_id}/market_chart", p2, max(1, _CG_MAX_ATTEMPTS))
    if isinstance(j, dict) and ("prices" in j or "market_caps" in j or "total_volumes" in j):
        try:
            json.dump(j, cpath.open("w"))
        except Exception:
            pass
        return j
    return {"prices": []}

# ----------------------------
# Implementierung PIT-HIstorie
# ----------------------------
def persist_pit_snapshot(data: pd.DataFrame, kind: str, date: Optional[str] = None) -> None:
    """
    Speichert ein DataFrame als PIT-Snapshot unter /snapshots/<kind>/yyyymmdd.json
    """
    date_str = date or time.strftime("%Y%m%d")
    path = Path("snapshots") / kind
    path.mkdir(parents=True, exist_ok=True)
    file = path / f"{date_str}.json"
    try:
        data.to_json(file, orient="records", indent=2)
    except Exception as ex:
        logging.warning(f"[pit] Failed to write snapshot {file}: {ex}")

# === Dummy-Fallback für PIT-Snapshot ===
def get_alias_seed() -> pd.DataFrame:
    """Dummy-Version für PIT-Snapshot – liefert minimale Alias-Zuordnung"""
    return pd.DataFrame([
        {"alias": "ABC", "coin_id": "abc"}
    ])

