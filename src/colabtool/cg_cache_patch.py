# modules/cg_cache_patch.py
from __future__ import annotations
import os, json, time, hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional, Callable
from .utils import logging

def setup_cg_chart_cache(cache_dir: Optional[str] = None, ttl_hours: int = 24) -> None:
    """
    Wrappt modules.data_sources.cg_market_chart mit einem On-Disk-Cache.
    Cache-Key: (coin_id, vs, days). TTL default 24h.
    """
    try:
        from . import data_sources as ds
    except Exception as ex:
        logging.warning(f"[cg-cache] data_sources import fail: {ex}")
        return

    orig: Callable = getattr(ds, "cg_market_chart", None)
    if not callable(orig):
        logging.warning("[cg-cache] cg_market_chart not callable → skip")
        return

    root = cache_dir or os.path.join(os.getcwd(), "cache", "cg_chart")
    os.makedirs(root, exist_ok=True)
    ttl = timedelta(hours=max(1, int(ttl_hours)))

    def _path(coin_id: str, vs: str, days: int) -> str:
        key = f"{coin_id}|{vs}|{int(days)}".encode("utf-8")
        h = hashlib.sha1(key).hexdigest()
        return os.path.join(root, f"{h}.json")

    def _fresh(p: str) -> bool:
        try:
            st = os.stat(p)
            mtime = datetime.fromtimestamp(st.st_mtime, timezone.utc)
            return datetime.now(timezone.utc) - mtime <= ttl
        except Exception:
            return False

    def wrapper(coin_id: str, vs: str = "usd", days: int = 365):
        p = _path(str(coin_id), str(vs), int(days))
        if os.path.isfile(p) and _fresh(p):
            try:
                return json.load(open(p, "r"))
            except Exception:
                pass
        j = {}
        try:
            j = orig(coin_id=coin_id, vs=vs, days=days)
        except Exception as ex:
            logging.warning(f"[cg-cache] fallback to stale for {coin_id}: {ex}")
            if os.path.isfile(p):
                try:
                    return json.load(open(p, "r"))
                except Exception:
                    return {}
            return {}
        try:
            json.dump(j, open(p, "w"))
        except Exception:
            pass
        return j

    setattr(ds, "cg_market_chart", wrapper)
    logging.info(f"[cg-cache] enabled at {root} ttl={ttl_hours}h")
