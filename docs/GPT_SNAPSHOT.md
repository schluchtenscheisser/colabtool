# colabtool • GPT snapshot

_Generated from commit: bad2251a7756d7c745942efb0318e1d006afb8bc_

## pyproject.toml

SHA256: `551956a7dc8730ec278037ac4aeebe7677e495e7817a2ea9c2e308b6e7ee8c4a`

```toml
[build-system]
requires = ["setuptools>=63", "wheel", "build"]
build-backend = "setuptools.build_meta"

[project]
name = "colabtool"
version = "0.1.1"
description = "Tool für Colab"
requires-python = ">=3.10"
readme = "README.md"
license = { text = "MIT" }
dependencies = [
  "numpy",
  "pandas",
  "requests",
  "feedparser",
  "xlsxwriter",
  "openpyxl",
  "nbformat"
]

[tool.setuptools.packages.find]
where = ["src"]

```

## requirements.txt

SHA256: `fe707c4e95377f8a6c3cf69e72b214634ceecb31d2eb48610639bb42cb870c56`

```text
numpy
pandas
requests
feedparser
xlsxwriter
openpyxl
nbformat

```

## README.md

SHA256: `3ca909379436a76450528b623dafce924132c80309a86ee6bd64840cc8dc3e55`

```markdown
# colabtool

`colabtool` ist eine Python-Bibliothek zur Entwicklung datengetriebener Workflows in Jupyter/Colab-Notebooks. Sie bietet ein modulares Framework zur Analyse von Kryptowährungen mit Fokus auf Scoring, Segmentierung und Visualisierung.

## Nutzung in Google Colab

Die empfohlene Methode zur Nutzung ist der direkte **Klon des Repositories** innerhalb eines Colab-Notebooks:

```python
# Zelle 1: Repo klonen oder aktualisieren
import os
REPO_DIR = "/content/colabtool"
REPO_URL = "https://github.com/schluchtenscheisser/colabtool.git"

if not os.path.exists(REPO_DIR):
    !git clone $REPO_URL $REPO_DIR
else:
    %cd $REPO_DIR
    !git pull
    %cd -


# Zelle 2: Module automatisch importieren
import sys, importlib
from pathlib import Path

MODULE_PATH = "/content/colabtool/src"
sys.path.insert(0, MODULE_PATH)

pkg_name = "colabtool"
pkg_path = Path(MODULE_PATH) / pkg_name
all_modules = [f.stem for f in pkg_path.glob("*.py") if f.name != "__init__.py"]

globals()[pkg_name] = importlib.import_module(pkg_name)
for mod_name in all_modules:
    full_mod_name = f"{pkg_name}.{mod_name}"
    globals()[mod_name] = importlib.import_module(full_mod_name)
    print(f"✅ geladen: {full_mod_name}")


# Zelle 3: Module neu laden
from pathlib import Path
import importlib, time

def reload_and_log(modname):
    if modname in sys.modules:
        mod = sys.modules[modname]
        path = Path(mod.__file__)
        mod_time = time.ctime(path.stat().st_mtime)
        importlib.reload(mod)
        print(f"✅ Reloaded {modname} | 📄 {path.name} | 🕒 {mod_time}")
    else:
        print(f"⚠️ Modul {modname} nicht geladen")

reload_and_log("colabtool")
for sub in all_modules:
    reload_and_log(f"{pkg_name}.{sub}")

    
Module
backtest: Logik für einfache Backtests oder historische Strategievergleiche
breakout: Erkennung von Ausbruchs-Signalen auf Basis technischer Metriken
buzz: News- & Buzz-Analyse, z. B. mit Hilfe von RSS-Feeds
category_providers: Zuordnung zu Coin-Gecko-Kategorien oder thematischen Gruppen
cg_cache_patch: Caching-Mechanismen und Workarounds für CoinGecko-APIs
data_sources: Zentrale Sammlung externer Datenquellen (CoinGecko, CMC etc.)
export: Excel-Export, Formatierung und Zusatzinfos wie „Meta“-Tab
export_helpers: Hilfsfunktionen zur tabellarischen Aufbereitung und Formatierung
exchanges: Filterlogik für Börsen wie MEXC (Spot-only, Paar-Präferenzen etc.)
features: Ableitung technischer Features wie Momentum, Drawdown, etc.
pre_universe: Vorbereitung des Universums vor dem eigentlichen Screening
scores: Gewichtung, Scoring und Ranking von Assets
utils: Pandas-, NumPy- und Logging-Helfer für konsistente Nutzung

Beispiel-Notebook
Ein vollständiger Workflow ist im Notebook notebooks/Scanner_v14_5.ipynb enthalten. Es führt durch alle Schritte: Datenerhebung, Feature Engineering, Filterung, Export und Visualisierung.

Setup
Benötigte Pakete sind in requirements.txt und pyproject.toml definiert.

Hinweis
Die Nutzung in Colab erfordert eine gemountete Verbindung zu Google Drive, um z. B. Excel-Dateien zu speichern.

```

## .github/workflows/ci.yml

SHA256: `d267365c5a5e20f752a0b83b81fc8f327e08ea87b06b123bdcaf9b8fee679cb4`

```yaml
name: ci
on:
  push:
  pull_request:
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - run: pip install -U pip
      - run: pip install -e .
      - run: pip install -U pytest
      - run: pytest -q

```

## src/colabtool/export.py

SHA256: `469f1e2f1e5b6343367182782cd1ae9356626de0c07e8f19073018d5a566a6f8`

```python
from __future__ import annotations
from typing import Dict, Any
from .utils import pd, np, logging
from pandas.api.types import (
    is_datetime64_any_dtype,
    is_categorical_dtype,
    is_numeric_dtype,
)

_DEF_MIN = 10
_DEF_MAX = 40
_DEF_FALLBACK = 12

EXPORT_PATH = "/content/drive/MyDrive/Colab results"

def _safe_col_width(s: pd.Series) -> int:
    if s is None or s.empty:
        return _DEF_FALLBACK
    if is_numeric_dtype(s):
        formatted = [len(f"{v:,.2f}") for v in s if pd.notna(v)]
        if not formatted:
            return _DEF_FALLBACK
        return max(_DEF_MIN, min(_DEF_MAX, int(np.nanmean(formatted) + 2)))
    if is_datetime64_any_dtype(s):
        return _DEF_MAX
    if is_categorical_dtype(s):
        return max(_DEF_MIN, min(_DEF_MAX, s.astype(str).str.len().max()))
    return max(_DEF_MIN, min(_DEF_MAX, s.astype(str).str.len().max()))

def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
    fixed_order = [
        "id", "symbol", "name", "market_cap", "score_global",
        "total_volume", "Kategorie", "Segment", "score_segment"
    ]
    available = [col for col in fixed_order if col in df.columns]
    remaining = [col for col in df.columns if col not in available]
    return df[available + remaining]

def write_sheet(df: pd.DataFrame, name: str, writer) -> None:
    df = df.copy()
    df = reorder_columns(df)
    if "score_global" in df.columns:
        df = df.sort_values("score_global", ascending=False)

    df.to_excel(writer, sheet_name=name, index=False)
    worksheet = writer.sheets[name]

    # Formate
    fmt_thousands = writer.book.add_format({"num_format": "#,##0", "align": "right"})
    fmt_percent = writer.book.add_format({"num_format": "0.00%", "align": "right"})

    for idx, col in enumerate(df.columns):
        width = _safe_col_width(df[col])
        if col in ("market_cap", "total_volume"):
            worksheet.set_column(idx, idx, width, fmt_thousands)
        elif col in ("mom_7d_pct", "mom_30d_pct"):
            worksheet.set_column(idx, idx, width, fmt_percent)
        else:
            worksheet.set_column(idx, idx, width)

def write_meta_sheet(writer, meta: Dict[str, Any]) -> None:
    meta_df = pd.DataFrame.from_dict(meta, orient="index", columns=["Value"])
    meta_df.reset_index(inplace=True)
    meta_df.columns = ["Key", "Value"]
    meta_df.to_excel(writer, sheet_name="Meta", index=False)
    worksheet = writer.sheets["Meta"]
    worksheet.set_column(0, 0, 40)
    worksheet.set_column(1, 1, 80)

```

## src/colabtool/features.py

SHA256: `4817f0db98053585f2b94a6f0d47b95d11590247a546411aefa1dafff63e9918`

```python
# modules/features.py
from __future__ import annotations

import re
from .utils import pd, np, logging

# Manuelle Blacklist (IDs in Kleinbuchstaben)
EXCLUDE_IDS = set([
    # Beispiele; bei Bedarf pflegen
    "terra-luna", "bitcoin-wrapped", "usd-coin-bridged"
])

# ---------- Helpers ----------
def _ensure_series(x, index) -> pd.Series:
    return x if isinstance(x, pd.Series) else pd.Series([x] * len(index), index=index, dtype="float64")

def _num_series(df: pd.DataFrame, cols, default=np.nan) -> pd.Series:
    """
    Liefert IMMER eine numerische Series gleicher Länge wie df.
    Nimmt den ersten vorhandenen Spaltennamen aus cols.
    """
    if isinstance(cols, str):
        cols = [cols]
    for c in cols:
        if c in df.columns:
            s = pd.to_numeric(df[c], errors="coerce")
            return _ensure_series(s, df.index)
    return pd.Series([default] * len(df), index=df.index, dtype="float64")

def _lc(x) -> str:
    return str(x or "").strip().lower()

# ---------- Peg-/Wrapped-/Stable-Heuristiken ----------
_STABLE_HINTS = [
    r"\bstable\b", r"\busd\b", r"\busdc\b", r"\busdt\b", r"\btusd\b", r"\busdd\b",
    r"\bust\b", r"\bdai\b", r"\beur[ts]?\b", r"\btryb\b", r"\baud\b", r"\bgusd\b",
    r"\bpax\b", r"\busd-?stable\b", r"\bpeg\b"
]
_WRAPPED_HINTS = [
    r"\bwrapped\b", r"\bw\b[A-Z]{2,}\b", r"\bbridged\b", r"\bbinance-peg\b", r"\bwormhole\b", r"\banyswap\b"
]

def is_stable_like(name: str, symbol: str, cid: str) -> bool:
    n = _lc(name); s = _lc(symbol); i = _lc(cid)
    if any(h in n for h in ["stable", "usd-coin", "tether", "binance-usd", "dai", "trueusd", "usdd"]):
        return True
    if s in ("usdt", "usdc", "busd", "dai", "tusd", "usdd", "gusd"):
        return True
    if any(re.search(p, f" {n} ") for p in _STABLE_HINTS):
        return True
    if any(k in i for k in ["-stable-", "usd-", "binance-usd"]):
        return True
    return False

def is_wrapped_like(name: str, symbol: str, cid: str) -> bool:
    n = _lc(name); s = _lc(symbol); i = _lc(cid)
    if "wrapped" in n or "bridged" in n or "binance-peg" in n:
        return True
    if s.startswith("w") and len(s) >= 3:
        return True
    if any(re.search(p, f" {n} ") for p in _WRAPPED_HINTS):
        return True
    if any(k in i for k in ["wrapped", "bridged", "binance-peg"]):
        return True
    return False

def peg_like_mask(df: pd.DataFrame) -> pd.Series:
    """
    Peg-Heuristik via niedrige Bewegung:
    - 30d < 5% und 7d < 3% → Peg-verdächtig
    - Alternativ: 7d < 2% und 24h < 0.7% (falls 24h vorhanden)
    Robust gegen fehlende Spalten; Rückgabe immer Series.
    """
    p7  = _num_series(df, "price_change_percentage_7d_in_currency").abs().fillna(0.0)
    p30 = _num_series(df, "price_change_percentage_30d_in_currency").abs().fillna(0.0)
    p1  = _num_series(df, ["price_change_percentage_24h_in_currency", "price_change_percentage_24h"], default=np.nan)
    p1  = _ensure_series(p1, df.index).abs().fillna(999.0)  # fehlend ⇒ neutral

    cond_main = (p30 < 5.0) & (p7 < 3.0)
    cond_alt  = (p7 < 2.0) & (p1 < 0.7)
    out = cond_main | cond_alt
    return _ensure_series(out.astype(bool), df.index)

def exclusion_mask(df: pd.DataFrame, cats: pd.Series) -> pd.Series:
    cats_l = cats.astype(str).str.lower() if isinstance(cats, pd.Series) else pd.Series([""] * len(df), index=df.index)
    m = pd.Series(False, index=df.index)

    m |= cats_l.str.contains("stable", na=False)
    m |= cats_l.str.contains("wrapped", na=False)
    m |= cats_l.str.contains("bridged", na=False)
    m |= cats_l.str.contains("binance-peg", na=False)

    m |= df.apply(lambda r: is_stable_like(r["name"], r["symbol"], r["id"]), axis=1)
    m |= df.apply(lambda r: is_wrapped_like(r["name"], r["symbol"], r["id"]), axis=1)

    m |= df["id"].astype(str).str.lower().isin(EXCLUDE_IDS)
    return _ensure_series(m.astype(bool), df.index)

# ---------- Feature-Block ----------
def compute_feature_block(df_in: pd.DataFrame) -> pd.DataFrame:
    d = df_in.copy()
    d["market_cap"]   = pd.to_numeric(d.get("market_cap"), errors="coerce")
    d["total_volume"] = pd.to_numeric(d.get("total_volume"), errors="coerce")
    with np.errstate(divide="ignore", invalid="ignore"):
        d["volume_mc_ratio"] = (d["total_volume"] / d["market_cap"]).replace([np.inf, -np.inf], np.nan)
    d["slope30"] = pd.to_numeric(d.get("price_change_percentage_30d_in_currency"), errors="coerce")
    d["mom_7d_pct"]  = pd.to_numeric(d.get("price_change_percentage_7d_in_currency"), errors="coerce")
    d["mom_30d_pct"] = pd.to_numeric(d.get("price_change_percentage_30d_in_currency"), errors="coerce")
    d["ath_drawdown_pct"] = pd.to_numeric(d.get("ath_change_percentage"), errors="coerce")
    d["circ_pct"] = np.nan
    return d

# ---------- Segmentierung ----------
def tag_segment(row) -> str:
    try:
        mc = float(row.get("market_cap", np.nan))
    except Exception:
        mc = np.nan
    r30 = float(row.get("price_change_percentage_30d_in_currency", 0.0) or 0.0)
    dd  = float(row.get("ath_change_percentage", row.get("ath_drawdown_pct", 0.0)) or 0.0)

    if np.isfinite(mc) and mc <= 150_000_000 and r30 >= 100.0:
        return "Momentum Gem"
    if dd <= -70.0 and r30 >= 20.0:
        return "Comeback"
    if np.isfinite(mc) and mc <= 150_000_000:
        return "Hidden Gem"
    if np.isfinite(mc) and mc <= 500_000_000:
        return "Emerging"
    return "Balanced"


```

## src/colabtool/breakout.py

SHA256: `417b2ddd175c9ac6b42d65a637e783217c57696982570f04f875bb2ff920c03b`

```python

# modules/breakout.py
from __future__ import annotations

import math
import time
from typing import Dict, List, Optional, Tuple

import requests
from .utils import pd, np, logging

# --------- MEXC HTTP ---------
_MEXC_BASE = "https://api.mexc.com"
_s = requests.Session()
_s.headers.update({"Accept": "application/json", "User-Agent": "mexc-early-screener/1.0"})

def _mexc_klines(pair: str, interval: str = "1d", limit: int = 365, attempts: int = 2, sleep_s: float = 0.8):
    """Holt Klines. Rückgabe: Liste von Kerzen oder None bei Fehler."""
    url = f"{_MEXC_BASE}/api/v3/klines"
    params = {"symbol": pair, "interval": interval, "limit": int(limit)}
    for att in range(1, attempts + 1):
        try:
            r = _s.get(url, params=params, timeout=20)
            if r.status_code == 200:
                return r.json()
            if r.status_code in (400, 404):
                logging.warning(f"[breakout] {pair} klines fail: {r.status_code} {r.reason}")
                return None
            logging.warning(f"[breakout] {pair} klines HTTP {r.status_code} → retry {att}/{attempts}")
        except requests.RequestException as ex:
            logging.warning(f"[breakout] {pair} klines err: {ex} → retry {att}/{attempts}")
        time.sleep(sleep_s)
    return None

# --------- Helpers ---------
def _valid_pair(p) -> Optional[str]:
    if p is None:
        return None
    s = str(p).strip().upper()
    if not s or s == "NAN" or s == "NONE":
        return None
    # Nur USD-Stables als Quote für sauberes USD-Volumen
    if not (s.endswith("USDT") or s.endswith("USD") or s.endswith("USDC")):
        return None
    return s

def _to_df(kl: list) -> Optional[pd.DataFrame]:
    """MEXC klines → DataFrame mit ts, open, high, low, close, volume (base)"""
    if not isinstance(kl, list) or len(kl) == 0:
        return None
    cols = ["t","o","h","l","c","v","ct","qv","num","tb","tqv","ignore"]
    try:
        d = pd.DataFrame(kl, columns=cols[:len(kl[0])])
    except Exception:
        return None
    num_cols = {"o":"float64","h":"float64","l":"float64","c":"float64","v":"float64"}
    for c, t in num_cols.items():
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d["t"] = pd.to_datetime(d["t"], unit="ms", utc=True)
    d = d[["t","o","h","l","c","v"]].dropna()
    d = d.sort_values("t").reset_index(drop=True)
    return d if len(d) > 0 else None

def _pct_change(x: pd.Series) -> pd.Series:
    return x.pct_change().replace([np.inf, -np.inf], np.nan)

def _rolling_max(s: pd.Series, win: int) -> pd.Series:
    return s.rolling(win, min_periods=max(2, int(win*0.6))).max()

def _percentile_rank(a: pd.Series, value: float) -> float:
    a = pd.to_numeric(a, errors="coerce")
    a = a[np.isfinite(a)]
    if len(a) == 0:
        return np.nan
    return float((a <= value).mean() * 100.0)

def _zscore(s: pd.Series) -> pd.Series:
    x = pd.to_numeric(s, errors="coerce")
    m = x.mean()
    v = x.std(ddof=0)
    if not np.isfinite(v) or v == 0:
        return pd.Series(0.0, index=x.index, dtype="float64")
    return (x - m) / v

def _beta(ret_asset: pd.Series, ret_bench: pd.Series) -> float:
    x = pd.to_numeric(ret_asset, errors="coerce")
    y = pd.to_numeric(ret_bench, errors="coerce")
    m = pd.concat([x, y], axis=1).dropna()
    if len(m) < 20:
        return np.nan
    cov = np.cov(m.iloc[:,0], m.iloc[:,1])[0,1]
    var = np.var(m.iloc[:,1])
    if var == 0:
        return np.nan
    return float(cov / var)

# --------- Core Feature-Berechnung pro Pair ---------
def _features_from_klines(dfk: pd.DataFrame) -> dict:
    """Berechnet Distanz zu Highs, Donchian-Width, Volumen-Acceleration (USD), p365.
       Liefert zusätzlich vol_acc_7d und vol_acc_30d als USD-MAs für Audit.
    """
    # Close und base-Volumen
    c = dfk["c"].astype(float)
    v_base = dfk["v"].astype(float)
    # USD-Volumen nur sinnvoll bei Stable-Quote → hier bereits gefiltert
    vol_usd = c * v_base

    # Donchian und Distanzen
    rmax90  = _rolling_max(c, 90)
    rmax180 = _rolling_max(c, 180)
    rmax365 = _rolling_max(c, 365)

    last = c.iloc[-1]
    dist_90  = float((last / rmax90.iloc[-1]  - 1.0)*100.0) if np.isfinite(rmax90.iloc[-1]) else np.nan
    dist_180 = float((last / rmax180.iloc[-1] - 1.0)*100.0) if np.isfinite(rmax180.iloc[-1]) else np.nan
    dist_365 = float((last / rmax365.iloc[-1] - 1.0)*100.0) if np.isfinite(rmax365.iloc[-1]) else np.nan

    # Donchian width als Proxy
    min90 = c.rolling(90, min_periods=60).min()
    max90 = rmax90
    donch_width = float((max90.iloc[-1] / min90.iloc[-1] - 1.0)*100.0) if np.isfinite(min90.iloc[-1]) and np.isfinite(max90.iloc[-1]) else np.nan

    # Perzentil des letzten Preises im 365-Tage-Fenster
    p365 = _percentile_rank(c.tail(min(365, len(c))), last)

    # Volumen-Acceleration: 7d vs 30d Wert-Volumen
    ma7  = vol_usd.rolling(7,  min_periods=5).mean()
    ma30 = vol_usd.rolling(30, min_periods=15).mean()
    ma7_last  = float(ma7.iloc[-1]) if np.isfinite(ma7.iloc[-1]) else np.nan
    ma30_last = float(ma30.iloc[-1]) if np.isfinite(ma30.iloc[-1]) else np.nan
    vol_acc = float((ma7_last / ma30_last) if (np.isfinite(ma7_last) and np.isfinite(ma30_last) and ma30_last > 0) else np.nan)

    # Breakout-Basis: Nähe zum 90-Tage-High
    breakout_base = dist_90  # in %
    return {
        "dist_90": dist_90,
        "dist_180": dist_180,
        "dist_365": dist_365,
        "donch_width": donch_width,
        "p365": p365,
        "vol_acc": vol_acc,
        "vol_acc_7d": ma7_last,
        "vol_acc_30d": ma30_last,
        "breakout_base": breakout_base,
    }

def _prep_betas(days: int = 365) -> Tuple[Optional[pd.Series], Optional[pd.Series]]:
    """BTC/ETH tägliche Renditen von MEXC (USDT-Quote)."""
    out = {}
    for sym in ["BTCUSDT", "ETHUSDT"]:
        kl = _mexc_klines(sym, "1d", min(days, 365))
        dfk = _to_df(kl) if kl else None
        if dfk is None or len(dfk) < 60:
            out[sym] = None
        else:
            out[sym] = _pct_change(dfk["c"])
    return out.get("BTCUSDT"), out.get("ETHUSDT")

# --------- Public: Breakout-Rechner ---------
def compute_breakout_for_ids(df_all: pd.DataFrame,
                             cand_ids: List[str],
                             days: int = 365,
                             progress: bool = True,
                             use_chart: bool = True,
                             light: bool = False) -> pd.DataFrame:
    """
    Berechnet Breakout/Volumen/Betas nur für valide MEXC-Paare.
    Gibt DataFrame mit Spalten:
      id, breakout_score, z_break, z_donch, dist_90, dist_180, dist_365, p365,
      vol_acc, vol_acc_7d, vol_acc_30d, break_vol_mult, donch_width, beta_btc, beta_eth, price_source
    """
    if not isinstance(df_all, pd.DataFrame) or not cand_ids:
        return pd.DataFrame(columns=[
            "id","breakout_score","z_break","z_donch","dist_90","dist_180","dist_365",
            "p365","vol_acc","vol_acc_7d","vol_acc_30d","break_vol_mult","donch_width","beta_btc","beta_eth","price_source"
        ])

    # id -> mexc_pair validieren
    sub = df_all[df_all["id"].astype(str).isin(cand_ids)].copy()
    sub["mexc_pair"] = sub["mexc_pair"].map(_valid_pair)
    sub = sub.dropna(subset=["mexc_pair"])
    if sub.empty:
        logging.info("[breakout] keine validen MEXC-Paare unter den Kandidaten")
        return pd.DataFrame(columns=[
            "id","breakout_score","z_break","z_donch","dist_90","dist_180","dist_365",
            "p365","vol_acc","vol_acc_7d","vol_acc_30d","break_vol_mult","donch_width","beta_btc","beta_eth","price_source"
        ])

    # Einmalig BTC/ETH-Betas vorbereiten
    r_btc, r_eth = _prep_betas(days=days)

    rows = []
    # Cache pro Pair, falls mehrere IDs dasselbe Pair hätten
    pair_cache: Dict[str, dict] = {}

    for _, r in sub.iterrows():
        cid = str(r["id"])
        pair = r["mexc_pair"]
        if pair in pair_cache:
            feat = pair_cache[pair]
        else:
            kl = _mexc_klines(pair, "1d", min(days, 365))
            dfk = _to_df(kl) if kl else None
            if dfk is None or len(dfk) < 60:
                # zu dünn → skip
                pair_cache[pair] = None
                if progress:
                    logging.warning(f"[breakout] {pair} zu wenig Daten")
                continue
            feat = _features_from_klines(dfk)
            # Betas
            ret = _pct_change(dfk["c"])
            b_btc = _beta(ret, r_btc) if r_btc is not None else np.nan
            b_eth = _beta(ret, r_eth) if r_eth is not None else np.nan
            feat["beta_btc"] = b_btc
            feat["beta_eth"] = b_eth
            feat["price_source"] = "mexc"
            pair_cache[pair] = feat

        if feat is None:
            continue

        rows.append({
            "id": cid,
            "dist_90": feat["dist_90"],
            "dist_180": feat["dist_180"],
            "dist_365": feat["dist_365"],
            "p365": feat["p365"],
            "vol_acc": feat["vol_acc"],
            "vol_acc_7d": feat["vol_acc_7d"],
            "vol_acc_30d": feat["vol_acc_30d"],
            "donch_width": feat["donch_width"],
            "breakout_base": feat["breakout_base"],
            "beta_btc": feat["beta_btc"],
            "beta_eth": feat["beta_eth"],
            "price_source": feat["price_source"],
        })

    if not rows:
        return pd.DataFrame(columns=[
            "id","breakout_score","z_break","z_donch","dist_90","dist_180","dist_365",
            "p365","vol_acc","vol_acc_7d","vol_acc_30d","break_vol_mult","donch_width","beta_btc","beta_eth","price_source"
        ])

    dfb = pd.DataFrame(rows)

    # Z-Norm über Kandidaten
    z_break = _zscore(pd.to_numeric(dfb["dist_90"], errors="coerce"))
    # donch score: hohe dist_90, aber schmalere Range (kleine width) besser → -width
    z_donch = _zscore(pd.to_numeric(dfb["dist_90"], errors="coerce") - 0.3 * pd.to_numeric(dfb["donch_width"], errors="coerce"))

    dfb["z_break"] = z_break
    dfb["z_donch"] = z_donch
    dfb["breakout_score"] = 0.7 * dfb["z_break"] + 0.3 * dfb["z_donch"]

    # Breakout-abhängiges Volumen-Multiplikator (Audit)
    dfb["break_vol_mult"] = pd.to_numeric(dfb["vol_acc"], errors="coerce")

    # Finales Set
    keep = [
        "id","breakout_score","z_break","z_donch","dist_90","dist_180","dist_365",
        "p365","vol_acc","vol_acc_7d","vol_acc_30d","break_vol_mult","donch_width","beta_btc","beta_eth","price_source"
    ]
    for k in keep:
        if k not in dfb.columns:
            dfb[k] = np.nan
    return dfb[keep].copy()


```

## src/colabtool/utils.py

SHA256: `4f1433376ee80cc99ad26b2320935c05bd026f0ee6c1dccfcbf60b820544c306`

```python
import os, time, json, hashlib, re, math, random, requests
import numpy as np, pandas as pd
from pathlib import Path
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

# --- Umgebungs-/Pfadlogik ohne Seiteneffekte außerhalb von Colab ---
def _is_colab() -> bool:
    try:
        import google.colab  # noqa: F401
        return True
    except Exception:
        return False

def _resolve_cache_dir() -> Path:
    # 1) Explizit via ENV
    env_dir = os.getenv("CACHE_DIR")
    if env_dir:
        return Path(env_dir)
    # 2) Colab-Default
    if _is_colab():
        return Path("/content/drive/MyDrive/Colab results/http_cache")
    # 3) Fallback für CI/Local
    return Path.cwd() / "cache" / "http_cache"

CACHE_DIR = _resolve_cache_dir()
try:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
except Exception:
    # In CI oder schreibgeschützten Umgebungen still tolerieren
    pass

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

def safe_div(a, b):
    try:
        a = float(a); b = float(b)
        return a / b if b not in (0.0, -0.0) and not math.isnan(a) and not math.isnan(b) else np.nan
    except Exception:
        return np.nan

def winsor_minmax(s, p=0.02):
    x = pd.to_numeric(s, errors='coerce')
    if x.notna().sum() < 3:
        return x.fillna(0)
    lo, hi = x.quantile(p), x.quantile(1 - p)
    x = x.clip(lo, hi)
    sd = x.std(ddof=0)
    return (x - x.mean()) / (sd if sd > 0 else 1.0)

def _cache_key(url, params):
    base = url + "?" + "&".join(f"{k}={v}" for k, v in sorted((params or {}).items()))
    return hashlib.sha1(base.encode()).hexdigest()

def http_get_json(url: str, params: dict | None = None, ttl_sec: int = 3600, use_cache: bool = True):
    params = dict(params or {})
    ck = _cache_key(url, params); cp = CACHE_DIR / f"{ck}.json"
    if use_cache and cp.exists():
        try:
            mtime = datetime.fromtimestamp(cp.stat().st_mtime).replace(tzinfo=timezone.utc)
            if datetime.now(timezone.utc) - mtime < timedelta(seconds=ttl_sec):
                with cp.open("r") as f:
                    return json.load(f)
        except Exception:
            pass

    host = urlparse(url).netloc
    last_status = None; tried_qparam = False

    for attempt in range(HTTP_MAX_RETRIES):
        iv = HOST_MIN_INTERVAL.get(host, 0.0)
        if iv > 0:
            last = _LAST_CALL.get(host, 0.0)
            wait = iv - (time.time() - last)
            if wait > 0:
                time.sleep(wait)
        try:
            r = session.get(url, params=params, timeout=HTTP_TIMEOUT)
            last_status = r.status_code
            if r.status_code == 200:
                _LAST_CALL[host] = time.time()
                data = r.json()
                if use_cache:
                    try:
                        cp.parent.mkdir(parents=True, exist_ok=True)
                        cp.write_text(json.dumps(data))
                    except Exception:
                        pass
                return data

            if r.status_code in (401, 403) and (not tried_qparam) and CG_KEY and "api.coingecko.com" in url:
                tried_qparam = True
                params = dict(params); params["x_cg_demo_api_key"] = CG_KEY
                time.sleep(HTTP_BACKOFF * (attempt + 1))
                continue

            if r.status_code in (429, 500, 502, 503, 504):
                ra = r.headers.get("Retry-After")
                sleep_s = float(ra) if ra else HTTP_BACKOFF * (attempt + 1) * (2.0 if r.status_code == 429 else 1.0)
                time.sleep(sleep_s)
                continue

            logging.error(f"HTTP ERROR {r.status_code} {url} | {r.text[:200]}")
            return None
        except Exception as e:
            logging.warning(f"HTTP Exception: {e}")
            time.sleep(HTTP_BACKOFF * (attempt + 1))
    logging.error(f"HTTP FAIL after retries (last_status={last_status}) {url}")
    return None

```

## src/colabtool/exchanges.py

SHA256: `9c39dc28735a5fadb0572ec977f45f04d10b47f45e30a9ef781c0e7bc52609f9`

```python
from __future__ import annotations

import os
import time
from typing import Dict, List, Optional, Tuple
from pathlib import Path

import requests
from .utils import pd, np, logging

# -------------------------
# Konstanten und Endpunkte
# -------------------------
_MEXC_BASE = "https://api.mexc.com"
_MEXC_EXCHANGE_INFO = f"{_MEXC_BASE}/api/v3/exchangeInfo"
_MEXC_TICKER_24H = f"{_MEXC_BASE}/api/v3/ticker/24hr"

# Bevorzugte Spot-Quotes
_PREFERRED_QUOTES = ["USDT", "USDC", "USD"]
# simple Hebel-/ETF-Heuristik
_LEVERAGE_SUFFIXES = ("UP", "DOWN", "3L", "3S", "4L", "4S", "5L", "5S", "BULL", "BEAR", "ETF")

# -------------------------
# Pfade (CI-/Colab-sicher)
# -------------------------
def _is_colab() -> bool:
    try:
        import google.colab  # noqa: F401
        return True
    except Exception:
        return False

def _resolve_seed_dir() -> Path:
    env = os.getenv("SEED_DIR")
    if env:
        return Path(env)
    if _is_colab():
        return Path("/content/drive/MyDrive/crypto_tool/seeds")
    return Path.cwd() / "seeds"

SEED_DIR: Path = _resolve_seed_dir()
try:
    SEED_DIR.mkdir(parents=True, exist_ok=True)
except Exception:
    # In CI oder schreibgeschützten Umgebungen still ignorieren
    pass

SEED_FILE: Path = SEED_DIR / "seed_mexc_map.csv"  # Columns: symbol, prefer_pair, bad_pairs, confidence

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
                base = ""
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
    if SEED_FILE.is_file():
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

```

## src/colabtool/buzz.py

SHA256: `4359e1f8ed3af54160fc8bea74e315b4ae2d9ae4631c9ce98e2a7beef2883ecf`

```python
# modules/buzz.py
from __future__ import annotations

import os
import re
import json
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timezone, timedelta
from pathlib import Path

import feedparser
from .utils import pd, np, logging

__all__ = ["fetch_rss_all", "add_buzz_metrics_for_candidates"]

# -------------------------------------------------
# Pfade (CI-/Colab-sicher)
# -------------------------------------------------
def _is_colab() -> bool:
    try:
        import google.colab  # noqa: F401
        return True
    except Exception:
        return False

def _resolve_seed_dir() -> Path:
    env = os.getenv("SEED_DIR")
    if env:
        return Path(env)
    if _is_colab():
        return Path("/content/drive/MyDrive/crypto_tool/seeds")
    return Path.cwd() / "seeds"

_SEED_DIR: Path = _resolve_seed_dir()
try:
    _SEED_DIR.mkdir(parents=True, exist_ok=True)
except Exception:
    # in CI ggf. kein Recht → still ignorieren
    pass

# -------------------------------------------------
# ENV
# -------------------------------------------------
def _env_str(name: str, default: str = "") -> str:
    v = os.getenv(name, default)
    return "" if v is None else str(v).strip()

def _env_float(name: str, default: float) -> float:
    s = _env_str(name, str(default)).split()[0]
    try:
        return float(s)
    except Exception:
        return default

def _env_json_dict(name: str, default: Dict[str, float]) -> Dict[str, float]:
    raw = _env_str(name, "")
    if not raw:
        return dict(default)
    try:
        j = json.loads(raw)
        if isinstance(j, dict):
            return {str(k).strip().lower(): float(v) for k, v in j.items()}
    except Exception:
        pass
    return dict(default)

HALF_LIFE_H = _env_float("BUZZ_HALF_LIFE_H", 48.0)
PUB_WEIGHTS = _env_json_dict(
    "BUZZ_PUBLISHER_WEIGHTS",
    {"coindesk": 1.0, "cointelegraph": 1.0, "theblock": 1.1, "decrypt": 0.9},
)

# -------------------------------------------------
# RSS
# -------------------------------------------------
_FEEDS = [
    ("coindesk",      "https://www.coindesk.com/arc/outboundfeeds/rss/?outputType=xml"),
    ("cointelegraph", "https://cointelegraph.com/rss"),
    ("theblock",      "https://www.theblock.co/rss"),
    ("decrypt",       "https://decrypt.co/feed"),
]

def _parse_entry(src: str, e) -> Optional[dict]:
    title = (e.get("title") or "").strip()
    summary = (e.get("summary") or e.get("description") or "").strip()
    link = (e.get("link") or "").strip()
    published = None
    for key in ("published_parsed", "updated_parsed"):
        t = e.get(key)
        if t:
            try:
                published = datetime(*t[:6], tzinfo=timezone.utc)
                break
            except Exception:
                pass
    if published is None:
        published = datetime.now(timezone.utc)
    if not title:
        return None
    return {"source": src, "title": title, "summary": summary, "link": link, "published": published}

def fetch_rss_all(max_items_per_feed: int = 300) -> List[dict]:
    out: List[dict] = []
    for src, url in _FEEDS:
        try:
            feed = feedparser.parse(url)
            entries = feed.get("entries") or []
            cnt = 0
            for e in entries:
                item = _parse_entry(src, e)
                if item:
                    out.append(item)
                    cnt += 1
                    if cnt >= max_items_per_feed:
                        break
        except Exception as ex:
            logging.warning(f"[buzz] RSS {src} fail: {ex}")
    logging.info(f"[buzz] RSS geladen: {len(out)} Artikel")
    return out

# -------------------------------------------------
# Alias-Seeds
# -------------------------------------------------
def _load_alias_seed() -> pd.DataFrame:
    """
    seed_alias.csv erwartet:
      id,symbol,name,aliases
    aliases: Pipe-separiert, z.B.: "Arbitrum|ARB"
    Rückgabe-DF: id, alias (ein Alias pro Zeile, kleinbuchstaben, getrimmt)
    """
    path = _SEED_DIR / "seed_alias.csv"
    rows = []
    if path.is_file():
        try:
            df = pd.read_csv(path)
            df["id"] = df["id"].astype(str).str.strip()
            if "symbol" in df.columns:
                df["symbol"] = df["symbol"].astype(str).str.strip()
            if "name" in df.columns:
                df["name"] = df["name"].astype(str).str.strip()
            if "aliases" not in df.columns:
                df["aliases"] = ""
            for _, r in df.iterrows():
                cid = str(r["id"]).strip()
                base_aliases = set()
                sym = str(r.get("symbol", "") or "").strip()
                nam = str(r.get("name", "") or "").strip()
                if sym:
                    base_aliases.add(sym)
                if nam:
                    base_aliases.add(nam)
                extra = str(r.get("aliases", "") or "")
                for a in extra.split("|"):
                    a = a.strip()
                    if a:
                        base_aliases.add(a)
                for a in base_aliases:
                    rows.append({"id": cid, "alias": a.lower()})
        except Exception as ex:
            logging.warning(f"[buzz] seed_alias.csv lesen fehlgeschlagen: {ex}")
    return pd.DataFrame(rows, columns=["id", "alias"])

def _compile_alias_regex(df_alias: pd.DataFrame, ids: List[str]) -> Dict[str, re.Pattern]:
    patterns: Dict[str, re.Pattern] = {}
    ids_set = set([str(x).strip() for x in ids])
    if df_alias.empty:
        return patterns
    df_alias = df_alias[df_alias["id"].astype(str).isin(ids_set)].copy()
    for cid, grp in df_alias.groupby("id"):
        alist = [str(a).strip().lower() for a in grp["alias"].tolist() if str(a).strip()]
        if not alist:
            continue
        parts = [re.escape(a) for a in sorted(set(alist), key=len, reverse=True)]
        pat = r"(?<![A-Za-z0-9])(" + "|".join(parts) + r")(?![A-Za-z0-9])"
        try:
            patterns[str(cid)] = re.compile(pat, flags=re.IGNORECASE)
        except re.error as ex:
            logging.warning(f"[buzz] Regex für {cid} fehlgeschlagen: {ex}")
    return patterns

# -------------------------------------------------
# Scoring
# -------------------------------------------------
def _age_weight(published: datetime, now: datetime, half_life_h: float) -> float:
    dh = max(0.0, (now - published).total_seconds() / 3600.0)
    return 0.5 ** (dh / max(0.1, half_life_h))

def _pub_weight(source: str) -> float:
    return float(PUB_WEIGHTS.get(str(source).strip().lower(), 1.0))

def _match_article(text: str, rx: re.Pattern) -> bool:
    if not text:
        return False
    return bool(rx.search(text))

def _collect_scores_for_ids(
    ids: List[str],
    rx_map: Dict[str, re.Pattern],
    articles: List[dict],
    half_life_h: float,
    now: datetime
) -> Dict[str, Dict[str, float]]:
    out: Dict[str, Dict[str, float]] = {cid: {"w_48h": 0.0, "w_7d": 0.0, "count_48h": 0.0, "count_7d": 0.0} for cid in ids}
    for art in articles or []:
        title = art.get("title", "")
        summary = art.get("summary", "")
        src = art.get("source", "")
        pub = art.get("published", now)
        pw = _pub_weight(src)
        dec = _age_weight(pub, now, half_life_h)
        age_h = (now - pub).total_seconds() / 3600.0
        in48 = age_h <= 48.0
        in7d = age_h <= 7 * 24.0
        if not in7d:
            continue
        txt = f"{title} {summary}"
        for cid, rx in rx_map.items():
            if _match_article(txt, rx):
                if in7d:
                    out[cid]["w_7d"] += pw * dec
                    out[cid]["count_7d"] += 1.0
                if in48:
                    out[cid]["w_48h"] += pw * dec
                    out[cid]["count_48h"] += 1.0
    return out

# -------------------------------------------------
# Public API
# -------------------------------------------------
def add_buzz_metrics_for_candidates(
    df_in: pd.DataFrame,
    top_n: int = 200,
    use_cp: bool = False,
    mask_pegged: Optional[pd.Series] = None,
    rss_news: Optional[List[dict]] = None,
    cp_api_key: Optional[str] = None
) -> pd.DataFrame:
    """
    Fügt Spalten hinzu: buzz_48h, buzz_7d, buzz_acc, buzz_level.
    Pegged/Wrapped → Buzz=0.
    """
    d = df_in.copy()
    if d.empty:
        for c in ["buzz_48h", "buzz_7d", "buzz_acc", "buzz_level"]:
            d[c] = np.nan
        return d

    # Kandidaten bestimmen
    if "score_global" in d.columns:
        sub = d.sort_values("score_global", ascending=False).head(int(min(top_n, len(d)))).copy()
    else:
        sub = d.sort_values("market_cap", ascending=False).head(int(min(top_n, len(d)))).copy()

    cand_ids = sub["id"].astype(str).tolist()

    # Aliase laden und Regexe kompilieren
    alias_df = _load_alias_seed()
    if alias_df.empty:
        logging.warning("[buzz] seed_alias.csv leer oder fehlt → Buzz wird konservativ")
        tmp = []
        for _, r in sub.iterrows():
            tmp.append({"id": str(r["id"]), "alias": str(r.get("symbol", "") or "").strip().lower()})
            tmp.append({"id": str(r["id"]), "alias": str(r.get("name", "") or "").strip().lower()})
        alias_df = pd.DataFrame(tmp, columns=["id", "alias"])
        alias_df = alias_df.dropna()
        alias_df = alias_df[alias_df["alias"].astype(str) != ""]

    rx_map = _compile_alias_regex(alias_df, cand_ids)

    # Artikel laden
    articles = rss_news if isinstance(rss_news, list) else []
    if not articles:
        articles = fetch_rss_all()

    now = datetime.now(timezone.utc)
    scores = _collect_scores_for_ids(cand_ids, rx_map, articles, HALF_LIFE_H, now)

    # In DataFrame gießen
    buzz_rows = []
    for cid in cand_ids:
        s = scores.get(cid, {})
        w48 = float(s.get("w_48h", 0.0) or 0.0)
        w7d = float(s.get("w_7d", 0.0) or 0.0)
        level = w7d
        baseline = (w7d / 7.0) * 2.0 if w7d > 0 else 0.0
        acc = w48 / max(1e-6, baseline) if baseline > 0 else 0.0
        buzz_rows.append({"id": cid, "buzz_48h": w48, "buzz_7d": w7d, "buzz_level": level, "buzz_acc": acc})

    df_buzz = pd.DataFrame(buzz_rows)
    if df_buzz.empty:
        for c in ["buzz_48h", "buzz_7d", "buzz_acc", "buzz_level"]:
            d[c] = 0.0
    else:
        d = d.merge(df_buzz, on="id", how="left")
        for c in ["buzz_48h", "buzz_7d", "buzz_acc", "buzz_level"]:
            if c not in d.columns:
                d[c] = 0.0
            d[c] = pd.to_numeric(d[c], errors="coerce").fillna(0.0)

    # Pegged/Wrapped → Buzz=0
    if isinstance(mask_pegged, pd.Series) and len(mask_pegged) == len(d):
        m = mask_pegged.astype(bool).fillna(False).values
        d.loc[m, ["buzz_48h", "buzz_7d", "buzz_acc", "buzz_level"]] = 0.0

    return d

```

## src/colabtool/data_sources.py

SHA256: `88eccd4e655a453daf93f25a63e9f84472c1dd3a8fdd487ccb02d33caef435c2`

```python
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

```

## src/colabtool/pre_universe.py

SHA256: `010af63a3614bb46a38d243673f050616ff0e5f9c9c000b17554ad460611b2a2`

```python

# modules/pre_universe.py
from __future__ import annotations

import re
from typing import Tuple
from .utils import pd, np, logging
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
    s = str(symbol or "").upper()
    n = str(name or "").upper()
    if any(s.endswith(suf) for suf in _LEVERAGE_SUFFIXES):
        return True
    if " LEVERAGED" in n or " ETF" in n:
        return True
    return False

def apply_pre_universe_filters(df_in: pd.DataFrame, min_volume_usd: float = 1_000_000.0) -> pd.DataFrame:
    """P1-Hard-Filter vor MEXC/Kategorien:
    - market_cap > 0
    - total_volume >= min_volume_usd
    - Stable/Pegged/Wrapped per Heuristik
    - BTC/ETH und gängige Derivate/Wraps
    - Hebel/ETF-Tokens
    """
    d = df_in.copy()
    # Basis
    d["market_cap"] = pd.to_numeric(d.get("market_cap"), errors="coerce")
    d["total_volume"] = pd.to_numeric(d.get("total_volume"), errors="coerce")
    d = d[(d["market_cap"] > 0) & (d["total_volume"] >= float(min_volume_usd))].copy()

    # Heuristiken
    m_stable = d.apply(lambda r: is_stable_like(r.get("name",""), r.get("symbol",""), r.get("id","")), axis=1)
    m_wrapped = d.apply(lambda r: is_wrapped_like(r.get("name",""), r.get("symbol",""), r.get("id","")), axis=1)
    m_peg_lowvar = peg_like_mask(d)  # vorsichtig
    m_lever = d.apply(lambda r: _is_leveraged(r.get("name",""), r.get("symbol","")), axis=1)
    ids = d["id"].astype(str).str.lower()
    m_core = ids.isin(_CORE_EXCLUDE_IDS)

    m_any = m_stable | m_wrapped | m_peg_lowvar | m_lever | m_core
    kept = d.loc[~m_any].copy()
    logging.info(f"[pre] Hard-Filter: {len(d)} -> {len(kept)}")

    return kept

def attach_categories(df_in: pd.DataFrame, sleep_s: float = 0.0) -> pd.DataFrame:
    """Füllt/erstellt die Spalte 'Kategorie' über CoinGecko /coins/{id}."""
    d = df_in.copy()
    ids = d["id"].astype(str).tolist()
    cat_map = enrich_categories(ids, sleep_s=sleep_s)
    d["Kategorie"] = d["id"].astype(str).map(cat_map).fillna("Unknown")
    return d


```

## src/colabtool/scores.py

SHA256: `35ca633d9f1753a767c16c71323229a17b254520dfee7bcc6ac34b1ca4fe0a3f`

```python

# modules/scores.py
from __future__ import annotations

from typing import Optional
from .utils import pd, np, logging

# ----------------------------
# Helpers
# ----------------------------
def _ensure_series(x, index) -> pd.Series:
    return x if isinstance(x, pd.Series) else pd.Series([x] * len(index), index=index, dtype="float64")

def _winsorize(s: pd.Series, lim: float = 3.0) -> pd.Series:
    s = pd.to_numeric(s, errors="coerce")
    return s.clip(lower=-abs(lim), upper=abs(lim))

def _mc_bucket(mc: pd.Series) -> pd.Series:
    mc = pd.to_numeric(mc, errors="coerce")
    b = pd.Series("gt2b", index=mc.index, dtype="object")
    b.loc[mc <= 2_000_000_000] = "500m_2b"
    b.loc[mc <= 500_000_000] = "150m_500m"
    b.loc[mc <= 150_000_000] = "le150m"
    return b

def _z_by_bucket(series: pd.Series, bucket: pd.Series, winsor: float = 3.0) -> pd.Series:
    x = pd.to_numeric(series, errors="coerce")
    b = bucket.astype("object")
    out = pd.Series(np.nan, index=x.index, dtype="float64")
    for k, idx in b.groupby(b).groups.items():
        vals = x.loc[idx]
        vals = vals[np.isfinite(vals)]
        if len(vals) < 2 or vals.std(ddof=0) == 0:
            out.loc[idx] = 0.0
        else:
            m = vals.mean()
            s = vals.std(ddof=0)
            out.loc[idx] = (x.loc[idx] - m) / s
    return _winsorize(out, winsor)

def _safe_num(df: pd.DataFrame, col: str, default: float = np.nan) -> pd.Series:
    if col in df.columns:
        return pd.to_numeric(df[col], errors="coerce")
    return pd.Series([default] * len(df), index=df.index, dtype="float64")

def _align_bool_mask(mask_in, idx) -> pd.Series:
    if isinstance(mask_in, pd.Series):
        m = mask_in.astype(bool)
        if len(m) != len(idx):
            return pd.Series([False] * len(idx), index=idx, dtype="bool")
        if not m.index.equals(idx):
            return pd.Series(m.to_numpy(), index=idx, dtype="bool")
        return m.fillna(False)
    try:
        arr = pd.Series(mask_in)
        if len(arr) != len(idx):
            return pd.Series([False] * len(idx), index=idx, dtype="bool")
        return pd.Series(arr.astype(bool).to_numpy(), index=idx, dtype="bool").fillna(False)
    except Exception:
        return pd.Series([False] * len(idx), index=idx, dtype="bool")

# ----------------------------
# Global/Segment Score (Basis)
# ----------------------------
def score_block(df_in: pd.DataFrame, regime_info: Optional[dict] = None) -> pd.DataFrame:
    d = df_in.copy()
    d["market_cap"] = pd.to_numeric(d.get("market_cap"), errors="coerce")
    d["mc_bucket"] = _mc_bucket(d["market_cap"])

    mom30 = _safe_num(d, "price_change_percentage_30d_in_currency", 0.0)
    mom7  = _safe_num(d, "price_change_percentage_7d_in_currency", 0.0)
    vmc   = _safe_num(d, "volume_mc_ratio", np.nan)
    dd    = _safe_num(d, "ath_change_percentage", np.nan)

    z_mom30 = _z_by_bucket(mom30, d["mc_bucket"])
    z_mom7  = _z_by_bucket(mom7, d["mc_bucket"])
    z_vmc   = _z_by_bucket(vmc, d["mc_bucket"])
    z_dd    = _z_by_bucket(dd, d["mc_bucket"])

    score_global = 0.40 * z_mom30 + 0.25 * z_mom7 + 0.25 * z_vmc - 0.10 * z_dd
    d["score_global"] = score_global.fillna(0.0)
    d["score_segment"] = d["score_global"]
    return d

# ----------------------------
# Early Score
# ----------------------------
def compute_early_score(df_in: pd.DataFrame, peg_mask: Optional[pd.Series] = None, regime_info: Optional[dict] = None) -> pd.DataFrame:
    """Early-Score inkl. Auditspalten risk_regime und beta_pen."""
    d = df_in.copy()
    idx = d.index

    d["market_cap"] = pd.to_numeric(d.get("market_cap"), errors="coerce")
    d["mc_bucket"] = _mc_bucket(d["market_cap"])

    slope_raw = _safe_num(d, "price_change_percentage_30d_in_currency", np.nan)
    volacc    = _safe_num(d, "vol_acc", np.nan)
    breaksc   = _safe_num(d, "breakout_score", np.nan)
    level     = _safe_num(d, "buzz_level", np.nan)
    buzzacc   = _safe_num(d, "buzz_acc", np.nan)

    z_slope = _z_by_bucket(slope_raw, d["mc_bucket"], winsor=2.5)
    z_vol   = _z_by_bucket(volacc,    d["mc_bucket"])
    z_brk   = _z_by_bucket(breaksc,   d["mc_bucket"])
    z_blvl  = _z_by_bucket(level,     d["mc_bucket"])
    z_bacc  = _z_by_bucket(buzzacc,   d["mc_bucket"])

    z_buzz = pd.concat([z_blvl, z_bacc], axis=1).max(axis=1)

    z_slope = _ensure_series(z_slope, idx).fillna(0.0)
    z_vol   = _ensure_series(z_vol,   idx).fillna(0.0)
    z_brk   = _ensure_series(z_brk,   idx).fillna(0.0)
    z_buzz  = _ensure_series(z_buzz,  idx).fillna(0.0)

    early = 0.30 * z_slope + 0.30 * z_vol + 0.30 * z_brk + 0.10 * z_buzz

    overext = slope_raw.fillna(0.0) >= 250.0
    early.loc[overext] = early.loc[overext] * 0.5

    beta_btc = _safe_num(d, "beta_btc", np.nan)
    beta_eth = _safe_num(d, "beta_eth", np.nan)
    beta_eff = pd.concat([beta_btc, beta_eth], axis=1).max(axis=1)

    # Audit defaults
    risk_regime = "neutral"
    beta_pen = pd.Series(1.0, index=idx, dtype="float64")

    if isinstance(regime_info, dict):
        btc_mom30 = float(regime_info.get("btc_mom30", 0.0) or 0.0)
        eth_mom30 = float(regime_info.get("eth_mom30", 0.0) or 0.0)
        risk_off = (btc_mom30 < 0.0) and (eth_mom30 < 0.0)
        risk_regime = "risk_off" if risk_off else "risk_on"
        if risk_off:
            hb = beta_eff - 1.0
            hb = hb.clip(lower=0.0).fillna(0.0)
            damp = 1.0 - 0.15 * hb.clip(upper=2.0)
            beta_pen = damp
            early = early * damp

    if peg_mask is not None:
        m = _align_bool_mask(peg_mask, idx)
        early.values[m.values] = np.nan

    d["early_score"] = early
    d["risk_regime"] = risk_regime if isinstance(risk_regime, str) else str(risk_regime)
    d["beta_pen"] = pd.to_numeric(beta_pen, errors="coerce") if isinstance(beta_pen, pd.Series) else float(beta_pen)
    return d


```

## src/colabtool/category_providers.py

SHA256: `cc399459d4ff7f9f707012fc8b8b3d126abef4610c04e00ca5faa322da292580`

```python
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
    return out

```

## src/colabtool/cg_cache_patch.py

SHA256: `7c2818b24a4756a7976a6cf5b03766a54931832bbe55844ca2568550fa0593ed`

```python
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

```

## src/colabtool/export_helpers.py

SHA256: `f6144d01a35529af09c478a520eea0e71dcaddc52510319c6c2e14fa921ff155`

```python
# modules/export_helpers.py
from __future__ import annotations
from typing import List
from .utils import pd

def _cols(dfin, names: List[str]) -> list:
    return [c for c in names if c in dfin.columns]

def make_fulldata(df_in: pd.DataFrame) -> pd.DataFrame:
    d = df_in.copy()

    basic = _cols(d, [
        "id","symbol","name","Kategorie","Segment",
        "market_cap","total_volume","circulating_supply",
        "mexc_pair","price_source"
    ])

    tvl = _cols(d, ["tvl_usd","tvl_source","llama_slug"])

    breakout = _cols(d, [
        "dist_90","dist_180","dist_365","p365","donch_width",
        "vol_acc","vol_acc_7d","vol_acc_30d",
        "z_break","z_donch","breakout_score","break_vol_mult",
        "beta_btc","beta_eth"
    ])

    buzz = _cols(d, ["buzz_48h","buzz_7d","buzz_acc"])

    scores = _cols(d, ["score_global", "score_segment", "early_score", "early_prelim", "mom_7d_pct", "mom_30d_pct"])

    audit = _cols(d, ["risk_regime","beta_pen"])

    order = basic + tvl + breakout + buzz + scores + audit

    # Fallback: falls etwas fehlt, trotzdem returnen
    if not order:
        return d.copy()

    out = d[order].copy()
    return out


```

## src/colabtool/backtest.py

SHA256: `b9724bd3706a6139467583105866fa27650b2ae331801271ab3b878c544b53a6`

```python
# modules/backtest.py
from __future__ import annotations
from typing import List
from .utils import pd, np, logging
from .data_sources import cg_market_chart

def _forward_return_from_chart(prices: List[List[float]], horizon: int) -> float:
    """
    Erwartet CoinGecko market_chart 'prices': [[ts, price], ...]
    Nutzt Schlusskurs[t] und Schlusskurs[t-horizon] → (p_t / p_{t-h} - 1)*100.
    Gibt NaN zurück, wenn zu wenige Punkte.
    """
    if not prices or len(prices) <= horizon:
        return np.nan
    try:
        p_now = float(prices[-1][1])
        p_prev = float(prices[-(horizon+1)][1])
        if p_prev == 0:
            return np.nan
        return (p_now / p_prev - 1.0) * 100.0
    except Exception:
        return np.nan

def backtest_on_snapshot(df: pd.DataFrame, topk: int = 20, days_list: List[int] = [20,40,60], vs: str = "usd") -> pd.DataFrame:
    """
    Simpler Snapshot-Backtest:
    - Auswahl: Top-k nach 'early_score' (Fallback: 'score_segment', dann 'score_global').
    - Für jede ID: lädt 1× market_chart(days = max(days_list)+2) und berechnet rückblickende
      %-Veränderungen über 20/40/60 Tage (Approximation, da echte Zukunftsreturns erst später messbar sind).
    - Output: Tabelle mit Returns je Horizon + Basisinfos.
    Hinweis: Minimiert API-Calls (≤ topk).
    """
    df = df.copy()
    rank_cols = [c for c in ["early_score","score_segment","score_global"] if c in df.columns]
    if not rank_cols:
        logging.warning("[backtest] keine Ranking-Spalten gefunden")
        return pd.DataFrame()

    rank_col = rank_cols[0]
    picks = df.dropna(subset=[rank_col]).sort_values(rank_col, ascending=False).head(topk).copy()
    if picks.empty:
        return pd.DataFrame()

    max_h = max(days_list) if len(days_list) else 60
    rows = []
    for _, r in picks.iterrows():
        cid = str(r["id"])
        data = cg_market_chart(cid, vs=vs, days=max(200, max_h+10)) or {}
        prices = data.get("prices", [])
        out = {
            "id": cid,
            "symbol": r.get("symbol"),
            "name": r.get("name"),
            "Segment": r.get("Segment"),
            "rank_col": rank_col,
            "rank_val": float(r.get(rank_col)) if pd.notna(r.get(rank_col)) else np.nan,
            "early_score": r.get("early_score"),
            "score_segment": r.get("score_segment"),
            "score_global": r.get("score_global"),
            "mexc_pair": r.get("mexc_pair")
        }
        for h in days_list:
            out[f"ret_{h}d_pct"] = _forward_return_from_chart(prices, h)
        rows.append(out)

    bt = pd.DataFrame(rows)
    # Aggregat-Zeile
    if not bt.empty:
        agg = {"id": "AGG_MEAN", "symbol": "-", "name": "-", "Segment": "-",
               "rank_col": rank_col, "rank_val": bt["rank_val"].mean(),
               "early_score": bt["early_score"].mean(), "score_segment": bt["score_segment"].mean(),
               "score_global": bt["score_global"].mean(), "mexc_pair": "-"}
        for h in days_list:
            agg[f"ret_{h}d_pct"] = bt[f"ret_{h}d_pct"].mean()
        bt = pd.concat([bt, pd.DataFrame([agg])], ignore_index=True)
    return bt


```

## src/colabtool/__init__.py

SHA256: `01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b`

```python


```

## notebooks/archive/crypto_scanner_main_v14.5.ipynb • code cells

SHA256: `a9aae5decfed8d60f3f58f07c66298ab5f7bbc5dcdc374a48107a816f90c057f`

```python
# cell 0
# 1 Repo klonen oder aktualisieren

import os

REPO_DIR = "/content/colabtool"
REPO_URL = "https://github.com/schluchtenscheisser/colabtool.git"

if not os.path.exists(REPO_DIR):
    !git clone $REPO_URL $REPO_DIR
else:
    %cd $REPO_DIR
    !git pull
    %cd -
!pip install -r /content/colabtool/requirements.txt

# Alte Zelle
# %pip install -U "git+https://github.com/schluchtenscheisser/colabtool@main"
# import importlib, colabtool
# importlib.reload(colabtool)
# print("installiert:", colabtool.__file__)
# import os
# print("Geladen aus:", os.path.abspath(colabtool.__file__))

# cell 1
# 2 Module importieren
import sys
import importlib
from pathlib import Path

# Pfad zu deinem Repo
MODULE_PATH = "/content/colabtool/src"
sys.path.insert(0, MODULE_PATH)

# Automatisch alle .py-Dateien in colabtool importieren
pkg_name = "colabtool"
pkg_path = Path(MODULE_PATH) / pkg_name
all_modules = [f.stem for f in pkg_path.glob("*.py") if f.name != "__init__.py"]

globals()[pkg_name] = importlib.import_module(pkg_name)
for mod_name in all_modules:
    full_mod_name = f"{pkg_name}.{mod_name}"
    globals()[mod_name] = importlib.import_module(full_mod_name)
    print(f"✅ geladen: {full_mod_name}")


# cell 2
# 3 Modul-Version validieren
from pathlib import Path
import importlib
import sys
import time

def reload_and_log(modname: str):
    if modname in sys.modules:
        mod = sys.modules[modname]
        path = Path(mod.__file__)
        mod_time = time.ctime(path.stat().st_mtime)
        importlib.reload(mod)
        print(f"🔁 Reloaded {modname} | 📄 {path.name} | 🕒 {mod_time}")
    else:
        print(f"⚠️ Modul {modname} nicht geladen")

# Hauptmodul zuerst
reload_and_log("colabtool")

# Alle geladenen colabtool-Submodule reloaded dynamisch
pkg_prefix = "colabtool."
for name in sorted(sys.modules):
    if name.startswith(pkg_prefix) and name != "colabtool":
        reload_and_log(name)


# cell 3
import inspect
from colabtool.export import _safe_col_width
print(inspect.getsource(_safe_col_width))

# cell 4
import inspect
from colabtool import export
print(inspect.getsource(export))


# cell 5
import inspect
from colabtool.features import compute_feature_block

print(inspect.getsource(compute_feature_block))


# cell 6
# Crypto-Scanner Main (v14.5) — Free-CG stabil, Chart-Cache, Hybrid-Kategorien, Cap 50–1000 Mio, Buzz-Audit

# === Bootstrap: Pakete, Drive, Pfade ===
import os

# === Logging/Warnungen ===
import logging as _rootlog, warnings, numpy as _np, pandas as _pd
_rootlog.basicConfig(level=_rootlog.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')
warnings.filterwarnings("ignore", category=RuntimeWarning)
_pd.options.mode.chained_assignment = None
_np.seterr(all="ignore")

# === ENV (Free-Plan) ===
os.environ.update({
    "COINGECKO_API_KEY": "CG-iM4aTeNWTc2kR2DSLEsTXWui",
    "CG_FORCE_FREE": "1",
    "CG_SKIP_AFTER_429": "1",
    "CG_MAX_ATTEMPTS": "1",
    "CG_MIN_INTERVAL_S": "3.5",
    "CG_CATS_TIME_BUDGET_S": "120",
    "PROVIDERS_CATS_TIME_BUDGET_S": "90",
    "SKIP_CATEGORIES": os.getenv("SKIP_CATEGORIES", "0"),
    "REQUIRE_MEXC": os.getenv("REQUIRE_MEXC", "1"),
    "LIGHT_BREAKOUT_ALL": os.getenv("LIGHT_BREAKOUT_ALL", "0"),
    "ALLOW_CG_FALLBACK": os.getenv("ALLOW_CG_FALLBACK", "0"),
    "BUZZ_HALF_LIFE_H": os.getenv("BUZZ_HALF_LIFE_H", "48"),
    "BUZZ_PUBLISHER_WEIGHTS": os.getenv("BUZZ_PUBLISHER_WEIGHTS", '{"coindesk":1.0,"cointelegraph":1.0,"theblock":1.1,"decrypt":0.9}')
})
# Optional Fallback-Provider:
# os.environ["CMC_API_KEY"] = "..."
# os.environ["MESSARI_API_KEY"] = "..."
# os.environ["COINPAPRIKA_API_KEY"] = "..."

# === Imports aus Modulen ===
from colabtool.utils import logging, time, datetime, timezone, pd, np
from colabtool.data_sources import cg_markets, map_tvl, update_seen_ids, cg_market_chart
from colabtool.pre_universe import apply_pre_universe_filters
from colabtool.exchanges import apply_mexc_filter, export_mexc_seed_template
from colabtool.features import compute_feature_block, exclusion_mask, peg_like_mask, tag_segment
from colabtool.scores import score_block, compute_early_score
from colabtool.breakout import compute_breakout_for_ids
from colabtool.buzz import add_buzz_metrics_for_candidates
from colabtool.backtest import backtest_on_snapshot
from colabtool.export import write_sheet, write_meta_sheet
from colabtool.export_helpers import make_fulldata
from colabtool.category_providers import enrich_categories_hybrid
from colabtool.cg_cache_patch import setup_cg_chart_cache

# Pfade und Verzeichnisse
try:
    from google.colab import drive
    drive.mount("/content/drive")
    MODULE_DIR = "/content/drive/MyDrive/crypto_tool/"
    EXPORT_DIR = "/content/drive/MyDrive/Colab results"
    CACHE_DIR  = "/content/drive/MyDrive/crypto_tool/cache"
except Exception:
    MODULE_DIR = os.getcwd()
    EXPORT_DIR = os.path.join(os.getcwd(), "exports")
    CACHE_DIR  = os.path.join(os.getcwd(), "cache")

os.makedirs(EXPORT_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

# === CG: /coins/{id}/market_chart Cache aktivieren (24h) ===
setup_cg_chart_cache(cache_dir=os.path.join(CACHE_DIR, "cg_chart"), ttl_hours=24)

# === CG Smart-Get: Robust gegen Reload & Rekursion ===
import time as _time, requests as _requests
from colabtool import data_sources as ds

# Nur patchen, wenn noch nicht gepatcht
if not hasattr(ds, "_ORIG_CG_GET"):
    ds._ORIG_CG_GET = ds._cg_get  # Original sichern (nur 1x)

def _cg_get_smart(path, params=None):
    if path.strip().lower() == "/coins/markets":
        return ds._ORIG_CG_GET(path, params=params)
    key = os.getenv("COINGECKO_API_KEY", "").strip()
    free = os.getenv("CG_FORCE_FREE", "1") == "1" or not key
    base = "https://api.coingecko.com/api/v3" if free else "https://pro-api.coingecko.com/api/v3"
    headers = {"Accept": "application/json", "User-Agent": "cg-screener/1.0"}
    if not free and key:
        headers["x-cg-pro-api-key"] = key
    q = dict(params or {})
    min_interval = float(os.getenv("CG_MIN_INTERVAL_S", "3.5"))
    last = getattr(ds, "_CG_LAST_CALL_TS", None)
    if last is not None:
        delta = _time.perf_counter() - last
        if delta < min_interval:
            _time.sleep(min_interval - delta)
    url = f"{base}{path}"
    try:
        sess = getattr(ds, "_SESSION", None)
        r = (sess or _requests).get(url, headers=headers, params=q, timeout=20)
        ds._CG_LAST_CALL_TS = _time.perf_counter()
    except Exception as ex:
        ds.logging.warning(f"[cg-smart] net err on {url}: {ex}")
        return {}
    if r.status_code == 429:
        ds.logging.warning(f"[cg-smart] 429 on {url} → skip")
        return {}
    if r.status_code != 200:
        ds.logging.warning(f"[cg-smart] HTTP {r.status_code} on {url}")
        try:
            return r.json() if r.content else {}
        except Exception:
            return {}
    try:
        return r.json()
    except Exception:
        return {}

# Patch aktivieren
ds._cg_get = _cg_get_smart


# === Lokaler Fallback für /coins/markets ===
import requests
def _cg_markets_fallback(vs="usd", per_page=250, pages=1):
    rows = []
    headers = {"Accept":"application/json","User-Agent":"cg-screener/1.0"}
    base = "https://api.coingecko.com/api/v3"
    for page in range(1, int(pages)+1):
        params = {
            "vs_currency": vs, "order": "market_cap_desc",
            "per_page": int(per_page), "page": int(page),
            "sparkline": "false", "price_change_percentage": "7d,30d"
        }
        r = requests.get(f"{base}/coins/markets", headers=headers, params=params, timeout=25)
        if r.status_code != 200:
            logging.warning(f"[cg-fb] HTTP {r.status_code} /coins/markets page={page}"); continue
        try: data = r.json()
        except Exception: data = []
        if isinstance(data, list): rows.extend(data)
    if not rows: return pd.DataFrame()
    df = pd.json_normalize(rows, sep="_")
    want = ["id","symbol","name","market_cap","total_volume",
            "price_change_percentage_7d_in_currency","price_change_percentage_30d_in_currency",
            "ath_change_percentage","circulating_supply"]
    return df[[c for c in want if c in df.columns]].copy()

# === Konfiguration ===
RUN_MODE = os.environ.get("RUN_MODE", "standard").strip().lower()
CFG = {
    "fast":     {"PAGES":1, "BREAKOUT_PER_SEGMENT":{"Hidden Gem":30,"Emerging":20,"Comeback":15,"Momentum Gem":15,"Balanced":20}, "BUZZ_TOPN":120, "DAYS":180, "USE_CP":False, "NEW_LISTINGS":True,  "BACKTEST":False},
    "standard": {"PAGES":4, "BREAKOUT_PER_SEGMENT":{"Hidden Gem":60,"Emerging":50,"Comeback":40,"Momentum Gem":40,"Balanced":40}, "BUZZ_TOPN":200, "DAYS":365, "USE_CP":True,  "NEW_LISTINGS":False, "BACKTEST":True}
}[RUN_MODE]

VS = os.environ.get("VS", "usd")
MIN_VOLUME_USD = float(os.environ.get("MIN_VOLUME_USD", "1000000"))
REQUIRE_MEXC = os.environ.get("REQUIRE_MEXC", "1") == "1"
SKIP_CATEGORIES = os.environ.get("SKIP_CATEGORIES", "0") == "1"

# LIGHT_BREAKOUT_ALL je Mode (env kann übersteuern)
LIGHT_BREAKOUT_ALL = True if RUN_MODE == "fast" else False
_env_lba = os.environ.get("LIGHT_BREAKOUT_ALL", None)
if _env_lba in ("0","1"):
    LIGHT_BREAKOUT_ALL = (_env_lba == "1")

USE_CRYPTOPANIC = CFG["USE_CP"]
CAP_MIN = 50_000_000
CAP_MAX = 1_000_000_000

# Zeitstempel (Berlin)
from datetime import datetime as _dt
try:
    from zoneinfo import ZoneInfo
    _TZ = ZoneInfo("Europe/Berlin")
except Exception:
    _TZ = None
_STAMP = (_dt.now(_TZ) if _TZ else _dt.now()).strftime("%Y%m%d%H%M")
EXPORT_NAME = f"Scanner_v14_5_output_{RUN_MODE}_{_STAMP}.xlsx"
EXPORT_PATH = os.path.join(EXPORT_DIR, EXPORT_NAME)

_pd.set_option("display.max_columns", 160); _pd.set_option("display.width", 220)

# === Regime-Helper ===
def _mom30_from_chart(prices):
    if not prices or len(prices) < 31: return np.nan
    p_now = float(prices[-1][1]); p_30 = float(prices[-31][1]); return (p_now/p_30 - 1.0)*100.0
def _dd_pct(prices):
    if not prices or len(prices) < 2: return np.nan
    arr = [float(p[1]) for p in prices]; p_now = arr[-1]; p_max = max(arr); return (p_now/p_max - 1.0)*100.0 if p_max>0 else np.nan
def _regime():
    try:
        btc = cg_market_chart("bitcoin", vs=VS, days=max(365, CFG["DAYS"]))
        eth = cg_market_chart("ethereum", vs=VS, days=max(365, CFG["DAYS"]))
        return {"btc_mom30": _mom30_from_chart(btc.get("prices",[])),
                "btc_dd": _dd_pct(btc.get("prices",[])),
                "eth_mom30": _mom30_from_chart(eth.get("prices",[])),
                "eth_dd": _dd_pct(eth.get("prices",[]))}
    except Exception as ex:
        logging.warning(f"[regime] {ex}")
        return {"btc_mom30": np.nan,"btc_dd": np.nan,"eth_mom30": np.nan,"eth_dd": np.nan}

# =========================
#          PIPELINE
# =========================
t_all = time.perf_counter()
logging.info(f"[0] Start {datetime.now(timezone.utc).isoformat()} | MODE={RUN_MODE} | PAGES={CFG['PAGES']}")

# [1] Universe (+Fallback)
t0 = time.perf_counter()
df = cg_markets(vs=VS, per_page=250, pages=CFG["PAGES"])
if df is None or df.empty:
    logging.warning("[main] cg_markets leer → Fallback nutzt direkten /coins/markets Abruf")
    df = _cg_markets_fallback(vs=VS, per_page=250, pages=CFG["PAGES"])
if df is None or df.empty:
    raise RuntimeError("cg_markets leer (Fallback ebenfalls leer)")
logging.info(f"[1] Märkte: {len(df)} Zeilen in {time.perf_counter()-t0:.2f}s")
print("Input-Spalten (price_change_*):", [c for c in df.columns if "price_change_percentage" in c])

# [2] Pre + Cap-Range
t0 = time.perf_counter()
df = apply_pre_universe_filters(df, min_volume_usd=MIN_VOLUME_USD)
df["market_cap"] = pd.to_numeric(df["market_cap"], errors="coerce")
df = df[(df["market_cap"] >= CAP_MIN) & (df["market_cap"] <= CAP_MAX)].copy()
logging.info(f"[2] Pre+CapRange: übrig {len(df)} in {time.perf_counter()-t0:.2f}s")

# [3] MEXC
t0 = time.perf_counter()
df = apply_mexc_filter(df, require_mexc=REQUIRE_MEXC)
try: export_mexc_seed_template(df, collisions_only=True)
except Exception: pass
if len(df) == 0 and REQUIRE_MEXC:
    raise RuntimeError("Nach MEXC-Schnitt 0 Zeilen.")
logging.info(f"[3] MEXC ok: {len(df)} in {time.perf_counter()-t0:.2f}s")

# Optional: New Listings
if CFG.get("NEW_LISTINGS", False):
    _ = update_seen_ids(df["id"].astype(str).tolist())

# [4] Kategorien (Hybrid, CG NICHT bevorzugt) + TVL
t0 = time.perf_counter()
if os.getenv("SKIP_CATEGORIES","0") != "1":
    df_tmp = df.copy()
    df_tmp["Segment"] = df_tmp.apply(tag_segment, axis=1)
    df_tmp["market_cap"] = pd.to_numeric(df_tmp["market_cap"], errors="coerce")
    df_tmp = df_tmp.sort_values("market_cap", ascending=True)
    seg_quota_for_cats = {"Hidden Gem":120, "Emerging":90, "Comeback":50, "Momentum Gem":30, "Balanced":10}
    ids_cat = []
    for seg, q in seg_quota_for_cats.items():
        ids_cat.extend(df_tmp[df_tmp["Segment"]==seg].head(q)["id"].astype(str).tolist())
    if len(ids_cat) < 300:
        extra = df_tmp[~df_tmp["id"].astype(str).isin(ids_cat)].head(300 - len(ids_cat))
        ids_cat.extend(extra["id"].astype(str).tolist())
    ids_cat = list(dict.fromkeys(ids_cat))[:300]
    cat_map = enrich_categories_hybrid(df, ids_cat, ttl_days=14, max_fetch=200, prefer_cg_first=False)
    df["Kategorie"] = df["id"].astype(str).map(cat_map).fillna("Unknown")
else:
    df["Kategorie"] = "Unknown"
df = map_tvl(df)
logging.info(f"[4] Kategorien/TVL ok in {time.perf_counter()-t0:.2f}s")

# [5] Features
t0 = time.perf_counter()
df = compute_feature_block(df)
logging.info(f"[5] Features ok in {time.perf_counter()-t0:.2f}s")
print("Nach Features‑Block:", df.columns.tolist()[:50])
print("Spaltenpreise:", [c for c in df.columns if "price_change_percentage" in c])

# [6] Segmente
df["Segment"] = df.apply(tag_segment, axis=1)

# [7] Regime
regime_info = _regime()

# [8] Peg/Wrapped/Stable-Maske
peg_mask = exclusion_mask(df, df.get("Kategorie", pd.Series()))

# [9] Scores
df = score_block(df, regime_info=regime_info)

# [10] Early Pass1
df_p1 = df.copy()
df_p1["breakout_score"] = np.nan
df_p1["vol_acc"] = 1.0
df_p1 = compute_early_score(df_p1, peg_mask=peg_mask, regime_info=regime_info)
df["early_prelim"] = df_p1["early_score"]

# [11] Kandidaten
def _pick_candidates(dfin, per_segment):
    out=[]
    for s, n in per_segment.items():
        sub = dfin[dfin["Segment"]==s].copy()
        if sub.empty: continue
        sub = sub.sort_values(["early_prelim","score_segment"], ascending=[False,False]).head(int(n))
        out.append(sub)
    return pd.concat(out, ignore_index=True) if out else dfin.head(0)
if LIGHT_BREAKOUT_ALL:
    cand_ids = df.loc[~df["mexc_pair"].isna(), "id"].astype(str).tolist()
else:
    cand_ids = _pick_candidates(df, CFG["BREAKOUT_PER_SEGMENT"])["id"].astype(str).tolist()

# [12] Breakout
t0 = time.perf_counter()
br = compute_breakout_for_ids(df, cand_ids, days=CFG["DAYS"], progress=True, light=bool(LIGHT_BREAKOUT_ALL))
if isinstance(br, pd.DataFrame) and not br.empty:
    df = df.merge(br, on="id", how="left")
else:
    for c in ["dist_90","dist_180","dist_365","p365","donch_width","vol_acc","vol_acc_7d","vol_acc_30d","z_break","z_donch","breakout_score","beta_btc","beta_eth","break_vol_mult","price_source"]:
        if c not in df.columns: df[c] = np.nan
df["price_source"] = df["price_source"].fillna("cg")
logging.info(f"[12] Breakout ok in {time.perf_counter()-t0:.2f}s")

# [13] Buzz
t0 = time.perf_counter()
df = add_buzz_metrics_for_candidates(
    df_in=df,
    top_n=min(CFG["BUZZ_TOPN"], len(df)),
    use_cp=USE_CRYPTOPANIC,
    mask_pegged=peg_mask,
    rss_news=None,
    cp_api_key=os.getenv("CRYPTOPANIC_API_KEY")
)
logging.info(f"[13] Buzz ok in {time.perf_counter()-t0:.2f}s")

# [14] Early final
t0 = time.perf_counter()
df = compute_early_score(df, peg_mask=peg_mask, regime_info=regime_info)
logging.info(f"[14] Early final ok in {time.perf_counter()-t0:.2f}s")

# [15] Rankings
def _keep_cols(dfin, extra=None):
    base = ["id","symbol","name","Segment","market_cap","total_volume","mexc_pair","score_global","score_segment","early_score"]
    ext = extra or []
    cols = [c for c in base+ext if c in dfin.columns]
    return dfin[cols].copy()
top25_global = df.sort_values("score_global", ascending=False).head(25)
top25_early  = df.sort_values("early_score", ascending=False).head(25)
seg_names = ["Hidden Gem","Emerging","Comeback","Momentum Gem","Balanced"]
top10_segments = {}
for s in seg_names:
    sub = df[df["Segment"]==s].copy()
    if not sub.empty: top10_segments[s] = sub.sort_values("early_score", ascending=False).head(10)
top10_all = pd.concat([v for v in top10_segments.values()], ignore_index=True) if top10_segments else df.head(0)

# [16] FullData (mit Buzz-Spalten)
print("mom_7d_pct in df:", "mom_7d_pct" in df.columns)
print("mom_30d_pct in df:", "mom_30d_pct" in df.columns)
full_data = make_fulldata(df)
print("mom_7d_pct in full_data:", "mom_7d_pct" in full_data.columns)
print("mom_30d_pct in full_data:", "mom_30d_pct" in full_data.columns)

# [17] Backtest
bt = pd.DataFrame()
if CFG.get("BACKTEST", False):
    bt = backtest_on_snapshot(df.sort_values("early_score", ascending=False), topk=20, days_list=[20,40,60], vs=VS)

# [18] Meta
from datetime import datetime as _dtu
meta = {
    "version": f"v14.5-{RUN_MODE}",
    "vs": VS,
    "min_volume_usd": str(int(MIN_VOLUME_USD)),
    "cap_min": str(CAP_MIN),
    "cap_max": str(CAP_MAX),
    "pages": str(CFG["PAGES"]),
    "breakout_per_segment": str(CFG["BREAKOUT_PER_SEGMENT"]),
    "buzz_topn": str(CFG["BUZZ_TOPN"]),
    "days": str(CFG["DAYS"]),
    "use_cryptopanic": str(USE_CRYPTOPANIC),
    "require_mexc": str(REQUIRE_MEXC),
    "light_breakout_all": "1" if LIGHT_BREAKOUT_ALL else "0",
    "allow_cg_fallback": os.getenv("ALLOW_CG_FALLBACK","0"),
    "buzz_half_life_h": os.getenv("BUZZ_HALF_LIFE_H","48"),
    "publisher_weights": os.getenv("BUZZ_PUBLISHER_WEIGHTS","{}"),
    "timestamp_utc": _dtu.now(timezone.utc).isoformat(),
}

# [19] Export
with pd.ExcelWriter(EXPORT_PATH, engine="xlsxwriter") as w:
    write_sheet(top25_global, "Top25_Global", w)
    for s, dseg in top10_segments.items():
        write_sheet(dseg, f"Top10_{s.replace(' ', '_')}", w)
    if not top10_all.empty:
        write_sheet(top10_all, "Top10_AllSegments", w)
    write_sheet(top25_early, "Top25_EarlySignals", w)
    write_sheet(full_data, "FullData", w)
    if CFG.get("BACKTEST", False) and not bt.empty:
        write_sheet(bt, "Backtest", w)
    write_meta_sheet(w, meta)

print("Export:", EXPORT_PATH)
import os
print("EXISTIERT:", os.path.exists(EXPORT_PATH))
print("EXPORT_PATH:", EXPORT_PATH)

try:
    display(top25_early.head(10)); display(full_data.head(10))
except Exception:
    pass


# cell 7

```

## notebooks/achive/crypto_scanner_main_v14.4.ipynb • code cells

SHA256: `e764f15de61623e684b606811f3d9b97525349d0c75f653095b84308638ad4d1`

```python
# cell 0
%pip install -U "git+https://github.com/schluchtenscheisser/colabtool@20596fb6c68aef50650f2dfc2ce7bdb0c6049b2d"
import importlib, colabtool
importlib.reload(colabtool)
print("installiert:", colabtool.__file__)

# cell 1
# Krypto-Scanner Main (v14.5) — Free-CG stabil, Chart-Cache, Hybrid-Kategorien, Cap 50–1000 Mio, Buzz-Audit

# === Bootstrap: Pakete, Drive, Pfade ===
import os

# === Logging/Warnungen ===
import logging as _rootlog, warnings, numpy as _np, pandas as _pd
_rootlog.basicConfig(level=_rootlog.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s')
warnings.filterwarnings("ignore", category=RuntimeWarning)
_pd.options.mode.chained_assignment = None
_np.seterr(all="ignore")

# === ENV (Free-Plan) ===
os.environ.update({
    "COINGECKO_API_KEY": "CG-iM4aTeNWTc2kR2DSLEsTXWui",
    "CG_FORCE_FREE": "1",
    "CG_SKIP_AFTER_429": "1",
    "CG_MAX_ATTEMPTS": "1",
    "CG_MIN_INTERVAL_S": "3.5",
    "CG_CATS_TIME_BUDGET_S": "120",
    "PROVIDERS_CATS_TIME_BUDGET_S": "90",
    "SKIP_CATEGORIES": os.getenv("SKIP_CATEGORIES", "0"),
    "REQUIRE_MEXC": os.getenv("REQUIRE_MEXC", "1"),
    "LIGHT_BREAKOUT_ALL": os.getenv("LIGHT_BREAKOUT_ALL", "0"),
    "ALLOW_CG_FALLBACK": os.getenv("ALLOW_CG_FALLBACK", "0"),
    "BUZZ_HALF_LIFE_H": os.getenv("BUZZ_HALF_LIFE_H", "48"),
    "BUZZ_PUBLISHER_WEIGHTS": os.getenv("BUZZ_PUBLISHER_WEIGHTS", '{"coindesk":1.0,"cointelegraph":1.0,"theblock":1.1,"decrypt":0.9}')
})
# Optional Fallback-Provider:
# os.environ["CMC_API_KEY"] = "..."
# os.environ["MESSARI_API_KEY"] = "..."
# os.environ["COINPAPRIKA_API_KEY"] = "..."

# === Imports aus Modulen ===
from colabtool.utils import logging, time, datetime, timezone, pd, np
from colabtool.data_sources import cg_markets, map_tvl, update_seen_ids, cg_market_chart
from colabtool.pre_universe import apply_pre_universe_filters
from colabtool.exchanges import apply_mexc_filter, export_mexc_seed_template
from colabtool.features import compute_feature_block, exclusion_mask, peg_like_mask, tag_segment
from colabtool.scores import score_block, compute_early_score
from colabtool.breakout import compute_breakout_for_ids
from colabtool.buzz import add_buzz_metrics_for_candidates
from colabtool.backtest import backtest_on_snapshot
from colabtool.export import write_sheet, write_meta_sheet
from colabtool.export_helpers import make_fulldata
from colabtool.category_providers import enrich_categories_hybrid
from colabtool.cg_cache_patch import setup_cg_chart_cache

# Pfade und Verzeichnisse
try:
    from google.colab import drive
    drive.mount("/content/drive")
    MODULE_DIR = "/content/drive/MyDrive/crypto_tool/"
    EXPORT_DIR = "/content/drive/MyDrive/Colab results"
    CACHE_DIR  = "/content/drive/MyDrive/crypto_tool/cache"
except Exception:
    MODULE_DIR = os.getcwd()
    EXPORT_DIR = os.path.join(os.getcwd(), "exports")
    CACHE_DIR  = os.path.join(os.getcwd(), "cache")

os.makedirs(EXPORT_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

# === CG: /coins/{id}/market_chart Cache aktivieren (24h) ===
setup_cg_chart_cache(cache_dir=os.path.join(CACHE_DIR, "cg_chart"), ttl_hours=24)

# === CG Smart-Get: /markets unverändert, andere Endpunkte sanft drosseln ===
import time as _time, requests as _requests
from colabtool import data_sources as ds
_ORIG_CG_GET = getattr(ds, "_cg_get", None)
def _cg_get_smart(path, params=None):
    if path.strip().lower() == "/coins/markets" and callable(_ORIG_CG_GET):
        return _ORIG_CG_GET(path, params=params)
    key = os.getenv("COINGECKO_API_KEY","").strip()
    free = os.getenv("CG_FORCE_FREE","1") == "1" or not key
    base = "https://api.coingecko.com/api/v3" if free else "https://pro-api.coingecko.com/api/v3"
    headers = {"Accept":"application/json","User-Agent":"cg-screener/1.0"}
    if not free and key:
        headers["x-cg-pro-api-key"] = key
    q = dict(params or {})
    min_interval = float(os.getenv("CG_MIN_INTERVAL_S","3.5"))
    last = getattr(ds, "_CG_LAST_CALL_TS", None)
    if last is not None:
        delta = _time.perf_counter() - last
        if delta < min_interval: _time.sleep(min_interval - delta)
    url = f"{base}{path}"
    try:
        sess = getattr(ds, "_SESSION", None)
        r = (sess or _requests).get(url, headers=headers, params=q, timeout=20)
        ds._CG_LAST_CALL_TS = _time.perf_counter()
    except Exception as ex:
        ds.logging.warning(f"[cg-smart] net err on {url}: {ex}")
        return {}
    if r.status_code == 429:
        ds.logging.warning(f"[cg-smart] 429 on {url} → skip"); return {}
    if r.status_code != 200:
        ds.logging.warning(f"[cg-smart] HTTP {r.status_code} on {url}")
        try: return r.json() if r.content else {}
        except Exception: return {}
    try: return r.json()
    except Exception: return {}
if callable(_ORIG_CG_GET):
    ds._cg_get = _cg_get_smart

# === Lokaler Fallback für /coins/markets ===
import requests
def _cg_markets_fallback(vs="usd", per_page=250, pages=1):
    rows = []
    headers = {"Accept":"application/json","User-Agent":"cg-screener/1.0"}
    base = "https://api.coingecko.com/api/v3"
    for page in range(1, int(pages)+1):
        params = {
            "vs_currency": vs, "order": "market_cap_desc",
            "per_page": int(per_page), "page": int(page),
            "sparkline": "false", "price_change_percentage": "7d,30d"
        }
        r = requests.get(f"{base}/coins/markets", headers=headers, params=params, timeout=25)
        if r.status_code != 200:
            logging.warning(f"[cg-fb] HTTP {r.status_code} /coins/markets page={page}"); continue
        try: data = r.json()
        except Exception: data = []
        if isinstance(data, list): rows.extend(data)
    if not rows: return pd.DataFrame()
    df = pd.json_normalize(rows, sep="_")
    want = ["id","symbol","name","market_cap","total_volume",
            "price_change_percentage_7d_in_currency","price_change_percentage_30d_in_currency",
            "ath_change_percentage","circulating_supply"]
    return df[[c for c in want if c in df.columns]].copy()

# === Konfiguration ===
RUN_MODE = os.environ.get("RUN_MODE", "standard").strip().lower()
CFG = {
    "fast":     {"PAGES":1, "BREAKOUT_PER_SEGMENT":{"Hidden Gem":30,"Emerging":20,"Comeback":15,"Momentum Gem":15,"Balanced":20}, "BUZZ_TOPN":120, "DAYS":180, "USE_CP":False, "NEW_LISTINGS":True,  "BACKTEST":False},
    "standard": {"PAGES":4, "BREAKOUT_PER_SEGMENT":{"Hidden Gem":60,"Emerging":50,"Comeback":40,"Momentum Gem":40,"Balanced":40}, "BUZZ_TOPN":200, "DAYS":365, "USE_CP":True,  "NEW_LISTINGS":False, "BACKTEST":True}
}[RUN_MODE]

VS = os.environ.get("VS", "usd")
MIN_VOLUME_USD = float(os.environ.get("MIN_VOLUME_USD", "1000000"))
REQUIRE_MEXC = os.environ.get("REQUIRE_MEXC", "1") == "1"
SKIP_CATEGORIES = os.environ.get("SKIP_CATEGORIES", "0") == "1"

# LIGHT_BREAKOUT_ALL je Mode (env kann übersteuern)
LIGHT_BREAKOUT_ALL = True if RUN_MODE == "fast" else False
_env_lba = os.environ.get("LIGHT_BREAKOUT_ALL", None)
if _env_lba in ("0","1"):
    LIGHT_BREAKOUT_ALL = (_env_lba == "1")

USE_CRYPTOPANIC = CFG["USE_CP"]
CAP_MIN = 50_000_000
CAP_MAX = 1_000_000_000

# Zeitstempel (Berlin)
from datetime import datetime as _dt
try:
    from zoneinfo import ZoneInfo
    _TZ = ZoneInfo("Europe/Berlin")
except Exception:
    _TZ = None
_STAMP = (_dt.now(_TZ) if _TZ else _dt.now()).strftime("%Y%m%d%H%M")
EXPORT_NAME = f"Scanner_v14_5_output_{RUN_MODE}_{_STAMP}.xlsx"
EXPORT_PATH = os.path.join(EXPORT_DIR, EXPORT_NAME)

_pd.set_option("display.max_columns", 160); _pd.set_option("display.width", 220)

# === Regime-Helper ===
def _mom30_from_chart(prices):
    if not prices or len(prices) < 31: return np.nan
    p_now = float(prices[-1][1]); p_30 = float(prices[-31][1]); return (p_now/p_30 - 1.0)*100.0
def _dd_pct(prices):
    if not prices or len(prices) < 2: return np.nan
    arr = [float(p[1]) for p in prices]; p_now = arr[-1]; p_max = max(arr); return (p_now/p_max - 1.0)*100.0 if p_max>0 else np.nan
def _regime():
    try:
        btc = cg_market_chart("bitcoin", vs=VS, days=max(365, CFG["DAYS"]))
        eth = cg_market_chart("ethereum", vs=VS, days=max(365, CFG["DAYS"]))
        return {"btc_mom30": _mom30_from_chart(btc.get("prices",[])),
                "btc_dd": _dd_pct(btc.get("prices",[])),
                "eth_mom30": _mom30_from_chart(eth.get("prices",[])),
                "eth_dd": _dd_pct(eth.get("prices",[]))}
    except Exception as ex:
        logging.warning(f"[regime] {ex}")
        return {"btc_mom30": np.nan,"btc_dd": np.nan,"eth_mom30": np.nan,"eth_dd": np.nan}

# =========================
#          PIPELINE
# =========================
t_all = time.perf_counter()
logging.info(f"[0] Start {datetime.now(timezone.utc).isoformat()} | MODE={RUN_MODE} | PAGES={CFG['PAGES']}")

# [1] Universe (+Fallback)
t0 = time.perf_counter()
df = cg_markets(vs=VS, per_page=250, pages=CFG["PAGES"])
if df is None or df.empty:
    logging.warning("[main] cg_markets leer → Fallback nutzt direkten /coins/markets Abruf")
    df = _cg_markets_fallback(vs=VS, per_page=250, pages=CFG["PAGES"])
if df is None or df.empty:
    raise RuntimeError("cg_markets leer (Fallback ebenfalls leer)")
logging.info(f"[1] Märkte: {len(df)} Zeilen in {time.perf_counter()-t0:.2f}s")

# [2] Pre + Cap-Range
t0 = time.perf_counter()
df = apply_pre_universe_filters(df, min_volume_usd=MIN_VOLUME_USD)
df["market_cap"] = pd.to_numeric(df["market_cap"], errors="coerce")
df = df[(df["market_cap"] >= CAP_MIN) & (df["market_cap"] <= CAP_MAX)].copy()
logging.info(f"[2] Pre+CapRange: übrig {len(df)} in {time.perf_counter()-t0:.2f}s")

# [3] MEXC
t0 = time.perf_counter()
df = apply_mexc_filter(df, require_mexc=REQUIRE_MEXC)
try: export_mexc_seed_template(df, collisions_only=True)
except Exception: pass
if len(df) == 0 and REQUIRE_MEXC:
    raise RuntimeError("Nach MEXC-Schnitt 0 Zeilen.")
logging.info(f"[3] MEXC ok: {len(df)} in {time.perf_counter()-t0:.2f}s")

# Optional: New Listings
if CFG.get("NEW_LISTINGS", False):
    _ = update_seen_ids(df["id"].astype(str).tolist())

# [4] Kategorien (Hybrid, CG NICHT bevorzugt) + TVL
t0 = time.perf_counter()
if os.getenv("SKIP_CATEGORIES","0") != "1":
    df_tmp = df.copy()
    df_tmp["Segment"] = df_tmp.apply(tag_segment, axis=1)
    df_tmp["market_cap"] = pd.to_numeric(df_tmp["market_cap"], errors="coerce")
    df_tmp = df_tmp.sort_values("market_cap", ascending=True)
    seg_quota_for_cats = {"Hidden Gem":120, "Emerging":90, "Comeback":50, "Momentum Gem":30, "Balanced":10}
    ids_cat = []
    for seg, q in seg_quota_for_cats.items():
        ids_cat.extend(df_tmp[df_tmp["Segment"]==seg].head(q)["id"].astype(str).tolist())
    if len(ids_cat) < 300:
        extra = df_tmp[~df_tmp["id"].astype(str).isin(ids_cat)].head(300 - len(ids_cat))
        ids_cat.extend(extra["id"].astype(str).tolist())
    ids_cat = list(dict.fromkeys(ids_cat))[:300]
    cat_map = enrich_categories_hybrid(df, ids_cat, ttl_days=14, max_fetch=200, prefer_cg_first=False)
    df["Kategorie"] = df["id"].astype(str).map(cat_map).fillna("Unknown")
else:
    df["Kategorie"] = "Unknown"
df = map_tvl(df)
logging.info(f"[4] Kategorien/TVL ok in {time.perf_counter()-t0:.2f}s")

# [5] Features
t0 = time.perf_counter()
df = compute_feature_block(df)
logging.info(f"[5] Features ok in {time.perf_counter()-t0:.2f}s")

# [6] Segmente
df["Segment"] = df.apply(tag_segment, axis=1)

# [7] Regime
regime_info = _regime()

# [8] Peg/Wrapped/Stable-Maske
peg_mask = exclusion_mask(df, df.get("Kategorie", pd.Series()))

# [9] Scores
df = score_block(df, regime_info=regime_info)

# [10] Early Pass1
df_p1 = df.copy()
df_p1["breakout_score"] = np.nan
df_p1["vol_acc"] = 1.0
df_p1 = compute_early_score(df_p1, peg_mask=peg_mask, regime_info=regime_info)
df["early_prelim"] = df_p1["early_score"]

# [11] Kandidaten
def _pick_candidates(dfin, per_segment):
    out=[]
    for s, n in per_segment.items():
        sub = dfin[dfin["Segment"]==s].copy()
        if sub.empty: continue
        sub = sub.sort_values(["early_prelim","score_segment"], ascending=[False,False]).head(int(n))
        out.append(sub)
    return pd.concat(out, ignore_index=True) if out else dfin.head(0)
if LIGHT_BREAKOUT_ALL:
    cand_ids = df.loc[~df["mexc_pair"].isna(), "id"].astype(str).tolist()
else:
    cand_ids = _pick_candidates(df, CFG["BREAKOUT_PER_SEGMENT"])["id"].astype(str).tolist()

# [12] Breakout
t0 = time.perf_counter()
br = compute_breakout_for_ids(df, cand_ids, days=CFG["DAYS"], progress=True, light=bool(LIGHT_BREAKOUT_ALL))
if isinstance(br, pd.DataFrame) and not br.empty:
    df = df.merge(br, on="id", how="left")
else:
    for c in ["dist_90","dist_180","dist_365","p365","donch_width","vol_acc","vol_acc_7d","vol_acc_30d","z_break","z_donch","breakout_score","beta_btc","beta_eth","break_vol_mult","price_source"]:
        if c not in df.columns: df[c] = np.nan
df["price_source"] = df["price_source"].fillna("cg")
logging.info(f"[12] Breakout ok in {time.perf_counter()-t0:.2f}s")

# [13] Buzz
t0 = time.perf_counter()
df = add_buzz_metrics_for_candidates(
    df_in=df,
    top_n=min(CFG["BUZZ_TOPN"], len(df)),
    use_cp=USE_CRYPTOPANIC,
    mask_pegged=peg_mask,
    rss_news=None,
    cp_api_key=os.getenv("CRYPTOPANIC_API_KEY")
)
logging.info(f"[13] Buzz ok in {time.perf_counter()-t0:.2f}s")

# [14] Early final
t0 = time.perf_counter()
df = compute_early_score(df, peg_mask=peg_mask, regime_info=regime_info)
logging.info(f"[14] Early final ok in {time.perf_counter()-t0:.2f}s")

# [15] Rankings
def _keep_cols(dfin, extra=None):
    base = ["id","symbol","name","Segment","market_cap","total_volume","mexc_pair","score_global","score_segment","early_score"]
    ext = extra or []
    cols = [c for c in base+ext if c in dfin.columns]
    return dfin[cols].copy()
top25_global = df.sort_values("score_global", ascending=False).head(25)
top25_early  = df.sort_values("early_score", ascending=False).head(25)
seg_names = ["Hidden Gem","Emerging","Comeback","Momentum Gem","Balanced"]
top10_segments = {}
for s in seg_names:
    sub = df[df["Segment"]==s].copy()
    if not sub.empty: top10_segments[s] = sub.sort_values("early_score", ascending=False).head(10)
top10_all = pd.concat([v for v in top10_segments.values()], ignore_index=True) if top10_segments else df.head(0)

# [16] FullData (mit Buzz-Spalten)
full_data = make_fulldata(df)

# [17] Backtest
bt = pd.DataFrame()
if CFG.get("BACKTEST", False):
    bt = backtest_on_snapshot(df.sort_values("early_score", ascending=False), topk=20, days_list=[20,40,60], vs=VS)

# [18] Meta
from datetime import datetime as _dtu
meta = {
    "version": f"v14.5-{RUN_MODE}",
    "vs": VS,
    "min_volume_usd": str(int(MIN_VOLUME_USD)),
    "cap_min": str(CAP_MIN),
    "cap_max": str(CAP_MAX),
    "pages": str(CFG["PAGES"]),
    "breakout_per_segment": str(CFG["BREAKOUT_PER_SEGMENT"]),
    "buzz_topn": str(CFG["BUZZ_TOPN"]),
    "days": str(CFG["DAYS"]),
    "use_cryptopanic": str(USE_CRYPTOPANIC),
    "require_mexc": str(REQUIRE_MEXC),
    "light_breakout_all": "1" if LIGHT_BREAKOUT_ALL else "0",
    "allow_cg_fallback": os.getenv("ALLOW_CG_FALLBACK","0"),
    "buzz_half_life_h": os.getenv("BUZZ_HALF_LIFE_H","48"),
    "publisher_weights": os.getenv("BUZZ_PUBLISHER_WEIGHTS","{}"),
    "timestamp_utc": _dtu.now(timezone.utc).isoformat(),
}

# [19] Export
with pd.ExcelWriter(EXPORT_PATH, engine="xlsxwriter") as w:
    write_sheet(top25_global, "Top25_Global", w)
    for s, dseg in top10_segments.items():
        write_sheet(dseg, f"Top10_{s.replace(' ', '_')}", w)
    if not top10_all.empty:
        write_sheet(top10_all, "Top10_AllSegments", w)
    write_sheet(top25_early, "Top25_EarlySignals", w)
    write_sheet(full_data, "FullData", w)
    if CFG.get("BACKTEST", False) and not bt.empty:
        write_sheet(bt, "Backtest", w)
    write_meta_sheet(w, meta)

print("Export:", EXPORT_PATH)
try:
    display(top25_early.head(10)); display(full_data.head(10))
except Exception:
    pass


# cell 2

```

