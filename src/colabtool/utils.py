import os, time, json, hashlib, re, math, random, requests
import numpy as np, pandas as pd
from pathlib import Path
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

HTTP_MAX_RETRIES = 5
HTTP_BACKOFF = 1.25
HTTP_TIMEOUT = 40

session = requests.Session()
session.headers.update({"User-Agent": "krypto-scanner/11.6"})

CG_KEY = os.environ.get("COINGECKO_API_KEY", "").strip()
if CG_KEY:
    session.headers["x-cg-demo-api-key"] = CG_KEY

HOST_MIN_INTERVAL = {"api.coingecko.com": 2.0}
_LAST_CALL = {}

CACHE_DIR = Path("/content/drive/MyDrive/Colab results/http_cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def safe_div(a, b):
    try:
        a = float(a); b = float(b)
        return a / b if b not in (0.0, -0.0) and not math.isnan(a) and not math.isnan(b) else np.nan
    except Exception:
        return np.nan

def winsor_minmax(s, p=0.02):
    x = pd.to_numeric(s, errors='coerce')
    if x.notna().sum() < 3: return x.fillna(0)
    lo, hi = x.quantile(p), x.quantile(1-p)
    x = x.clip(lo, hi)
    sd = x.std(ddof=0)
    return (x - x.mean()) / (sd if sd > 0 else 1.0)

def _cache_key(url, params):
    base = url + "?" + "&".join(f"{k}={v}" for k,v in sorted((params or {}).items()))
    return hashlib.sha1(base.encode()).hexdigest()

def http_get_json(url: str, params: dict|None=None, ttl_sec: int=3600, use_cache: bool=True):
    params = dict(params or {})
    ck = _cache_key(url, params); cp = CACHE_DIR / f"{ck}.json"
    if use_cache and cp.exists():
        try:
            mtime = datetime.fromtimestamp(cp.stat().st_mtime).replace(tzinfo=timezone.utc)
            if datetime.now(timezone.utc) - mtime < timedelta(seconds=ttl_sec):
                with cp.open("r") as f: return json.load(f)
        except Exception: pass

    host = urlparse(url).netloc
    last_status = None; tried_qparam = False

    for attempt in range(HTTP_MAX_RETRIES):
        iv = HOST_MIN_INTERVAL.get(host, 0.0)
        if iv > 0:
            last = _LAST_CALL.get(host, 0.0)
            wait = iv - (time.time() - last)
            if wait > 0: time.sleep(wait)
        try:
            r = session.get(url, params=params, timeout=HTTP_TIMEOUT)
            last_status = r.status_code
            if r.status_code == 200:
                _LAST_CALL[host] = time.time()
                data = r.json()
                if use_cache:
                    try: cp.write_text(json.dumps(data))
                    except Exception: pass
                return data

            if r.status_code in (401,403) and (not tried_qparam) and CG_KEY and "api.coingecko.com" in url:
                tried_qparam = True
                params = dict(params); params["x_cg_demo_api_key"] = CG_KEY
                time.sleep(HTTP_BACKOFF*(attempt+1))
                continue

            if r.status_code in (429, 500, 502, 503, 504):
                ra = r.headers.get("Retry-After")
                sleep_s = float(ra) if ra else HTTP_BACKOFF*(attempt+1)*(2.0 if r.status_code==429 else 1.0)
                time.sleep(sleep_s); continue

            logging.error(f"HTTP ERROR {r.status_code} {url} | {r.text[:200]}")
            return None
        except Exception as e:
            logging.warning(f"HTTP Exception: {e}")
            time.sleep(HTTP_BACKOFF*(attempt+1))
    logging.error(f"HTTP FAIL after retries (last_status={last_status}) {url}")
    return None
