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
from .utilities import pd, np, logging

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
