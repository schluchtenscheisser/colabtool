# colabtool • GPT snapshot

_Generated from commit: d6ed84b5d88fb336e7210604ec64678feb801949_

## pyproject.toml

SHA256: `4ad6c74c5b0639d83699d6cf11bc36ee17654d340422f01bea9be3f6f1fe6aeb`

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
  "nbformat",
  "python-dotenv"
]

[tool.setuptools.packages.find]
where = ["src"]

```

## requirements.txt

SHA256: `9bca092dfcb091f3acb991735b88c36a98b781fad57a4a6e41d368e4676652fd`

```text
numpy
pandas
requests
feedparser
xlsxwriter
openpyxl
nbformat
python-dotenv>=1.0.0

```

## README.md

SHA256: `c8b861e7fba26ae282ef0e167f7638f5761ec299a82d4b242238b92a69d32db6`

```markdown

<!-- ChatGPT Context Overview -->

> ⚙️ **Hinweis für ChatGPT**  
> Diese README dient als **zentrale Wissensquelle** („Single Source of Truth“)  
> für das Repository [`schluchtenscheisser/colabtool`](https://github.com/schluchtenscheisser/colabtool).  
> GPT-Instanzen sollen diese Datei **zuerst vollständig lesen**, bevor sie Code ändern oder Fragen beantworten.  
> Ergänzende technische Details stehen in [`docs/GPT_SNAPSHOT.md`](docs/GPT_SNAPSHOT.md).


# 🧠 Early Signal Altcoin Scanner ("colabtool")

Ein automatisiertes Research-Tool zur **Identifikation früher Momentum-Signale bei Altcoins**  
(Horizont: Wochen–Monate).  
Fokus: Mid-Caps, Volumenbeschleunigung, Breakout-Nähe und Buzz-Aktivität.

---

## 1️⃣ Ziel und Zweck

Das Tool analysiert Altcoin-Marktdaten (CoinMarketCap, MEXC, DeFiLlama, CryptoPanic)  
und erkennt potenzielle „Hidden Gems“ oder Comebacks anhand von  
Momentum, Volumenbeschleunigung, Breakout-Distanz und Buzz-Dynamik.

---

## 2️⃣ Architekturüberblick

```text
CoinMarketCap Markets → Filter & Exclusions → MEXC Mapping
      ↓
Feature Engine (MEXC-Klines & CMC-Fallback: Momentum, VolAcc, ATH-Drawdown, Buzz)
      ↓
Scoring & Segmentierung → Backtest → Snapshot Export
```

👉 **Aktueller Code- und Modulstatus:**  
Siehe [📄 docs/GPT_SNAPSHOT.md](docs/GPT_SNAPSHOT.md)  
> Diese Datei wird **automatisch nach jedem Commit** aktualisiert  
> und enthält die aktuelle Modul- und Funktionsübersicht („ChatGPT Context Map“).

## 🧭 Systemarchitektur auf einen Blick

```plaintext
 ┌────────────────────────────┐
 │    CoinMarketCap API       │
 │ → Listings, Volumen, Preise│
 └────────────┬───────────────┘
              │
              ▼
 ┌────────────────────────────┐
 │   Pre-Universe Filtering   │
 │ MarketCap, Volumen, Range  │
 │ Ausschlüsse: Stable/Wrapped│
 └────────────┬───────────────┘
              │
              ▼
 ┌────────────────────────────┐
 │     MEXC Mapping & Filter  │
 │   Quelle: exchanges.py     │
 └────────────┬───────────────┘
              │
              ▼
 ┌────────────────────────────┐
 │ Feature Engine (CMC+MEXC)  │
 │ Momentum, VolAcc, ATH-DD   │
 └────────────┬───────────────┘
              │
              ▼
 ┌────────────────────────────┐
 │ Scoring & Segmentierung    │
 │ Z-Norm, Regime, Beta-Pen   │
 └────────────┬───────────────┘
              │
              ▼
 ┌────────────────────────────┐
 │ Breakout & Buzz Analysis   │
 │ MEXC-Klines + Newsfeeds    │
 └────────────┬───────────────┘
              │
              ▼
 ┌────────────────────────────┐
 │ Backtesting & Validation   │
 │ Returns 20/40/60 Tage      │
 └────────────┬───────────────┘
              │
              ▼
 ┌────────────────────────────┐
 │ Excel Export & Snapshots   │
 │ (Top25, FullData, Backtest)│
 └────────────┬───────────────┘
              │
              ▼
 ┌────────────────────────────┐
 │ GPT Snapshot Workflow      │
 │ docs/GPT_SNAPSHOT.md       │
 └────────────────────────────┘
```

---

## 3️⃣ Run-Modes

| Mode | Beschreibung |
|------|---------------|
| fast | 1 Page · 180 Tage · kein CryptoPanic · kein Backtest |
| standard | 4 Pages · 365 Tage · CryptoPanic aktiv · Backtest aktiv |
| offline | Mock-Daten · keine API-Calls |

---

## 4️⃣ Wichtige ENV-Variablen

| Variable | Bedeutung |
|-----------|-----------|
| `REQUIRE_MEXC` | Nur Coins mit MEXC-Listing |
| `LIGHT_BREAKOUT_ALL` | Breakout-Scan für alle oder nur Kandidaten |
| `SKIP_CATEGORIES` | Überspringt CoinMarketCap-Kategorisierung |
| `CRYPTOPANIC_API_KEY` | Optional für Buzz-Daten |
| `CG_MIN_INTERVAL_S` | Rate-Limit für CoinMarketCap-API |
| `CMC_API_KEY` | CoinMarketCap API-Key (Pflicht) |

---

## 5️⃣ Entwicklungs- und Änderungsrichtlinien (für ChatGPT)

1. **Vor jeder Änderung:**  
   Immer zuerst den aktuellen Code über  
   ```python
   getContent(owner="schluchtenscheisser", repo="colabtool", path="<datei>", ref="main")
   ```  
   laden.
2. **Dann Änderungsvorschlag präzise formulieren:**  
   - Welche Funktion / Zeilen betroffen  
   - Wodurch ersetzt wird  
3. **Keine Code-Änderung ohne vorherigen Kontext-Check.**
4. **Maximal 3 Dateien / 200 Diff-Zeilen pro Änderung.**
5. **Tests:**  
   Immer mit `pytest` (Mock-Daten und Excel-Audit).
6. **Changelog:**  
   Jede Änderung → `Added`, `Changed`, `Fixed` im Änderungslog.

---

## 6️⃣ Automatischer GPT-Snapshot-Workflow

Der Workflow [`.github/workflows/gpt-snapshot.yml`](.github/workflows/gpt-snapshot.yml)
läuft nach jedem Commit und führt automatisch aus:

- ✅ Erstellung von `docs/GPT_SNAPSHOT.md`  
  (inkl. Hash-Signaturen und **automatischer Modul- & Funktionsübersicht**)  
- ✅ Speicherung von Daten-Snapshots in `snapshots/YYYYMMDD/`  
- ✅ Automatischer Commit mit `chore: update GPT_SNAPSHOT.md`

Damit ist der **aktuelle Systemzustand jederzeit rekonstruierbar** –  
für dich und für ChatGPT in neuen Sessions.

---

## 7️⃣ Projektstruktur (statisch)

| Verzeichnis | Zweck |
|--------------|-------|
| `src/` | Quellcode: Datenabruf, Pipeline, Feature-Engine, Scoring, Export |
| `snapshots/` | Tägliche Analyse- und Backtest-Outputs |
| `scripts/` | Hilfs- und Wartungsskripte |
| `tests/` | Unit- und Integrationstests |
| `docs/` | Dokumentation und GPT-Snapshots |
| `.github/workflows/` | Automatisierte CI-/CD-Pipelines |

---

## 8️⃣ Beispiel-Output

**Pfad:** `snapshots/YYYYMMDD/<datum>_fullsnapshot.xlsx`  

**Sheets:**  
- `Top25_Global`  
- `Top10_<Segment>`  
- `FullData`  
- `Backtest`  
- `Meta`

Begleitdateien:  
`cg_markets.csv`, `mexc_pairs.csv`, `seed_alias.csv`

---

### 🔄 CODE_MAP-Aktualisierung
Nach jeder Codeänderung ausführen:
```bash
python tools/update_codemap.py
```

---

## 9️⃣ Lizenz & Haftung

Dieses Tool dient ausschließlich **Research-Zwecken**.  
Es stellt **keine Finanzberatung** dar. Nutzung auf eigenes Risiko.

---

## 🔁 Quick-Reference (für ChatGPT)

**Primäre Einstiegspunkte:**
- `src/colabtool/data_sources_cmc.py` → CMC-Datenquelle (ersetzt CoinGecko)
- `src/colabtool/exchanges.py` → MEXC-Pairing und Filterlogik
- `src/colabtool/run_snapshot_mode.py` → vollständiger Pipeline-Run & CLI
- `src/colabtool/export.py` → Export mit Rankings & Legacy-Kompatibilität

**Wenn eine Funktion unklar ist:**  
→ Zuerst in `src/pipeline/` suchen  
→ Dann `getContent()` nutzen, um Quelltext zu prüfen.

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

## src/colabtool/data_sources_cmc.py

SHA256: `0439f9d53b6c34732621d7c2a2009716b0f2aa0c478be8e6794f42809f03d4db`

```python
"""
data_sources_cmc.py
-------------------
CoinMarketCap + MEXC basierte Datenquelle für colabtool.

Ersetzt vollständig die CoinGecko-Abhängigkeit.
Erzeugt ein DataFrame mit identischem Schema wie fetch_cg_markets():
[
  "id", "symbol", "name",
  "current_price", "market_cap", "total_volume",
  "price_change_percentage_7d_in_currency",
  "price_change_percentage_30d_in_currency",
  "ath", "ath_date"
]

- nutzt CMC `/v1/cryptocurrency/listings/latest`
- liest API-Key aus .env (CMC_API_KEY)
- robustes Retry-System mit Backoff (30 → 60 → 120s)
- Cache unter snapshots/YYYYMMDD/cmc_markets.csv
"""

import os
import time
import json
import logging
import requests
import pandas as pd
import numpy as np
from datetime import datetime
from dotenv import load_dotenv
from typing import Optional, Dict, Any, List

# Lade Umgebungsvariablen
load_dotenv()

CMC_API_KEY = os.getenv("CMC_API_KEY")
if not CMC_API_KEY:
    raise EnvironmentError("❌ Kein CMC_API_KEY in .env gefunden – bitte eintragen.")

CMC_BASE_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
MEXC_BASE_URL = "https://api.mexc.com/api/v3/exchangeInfo"

# Logging Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


# ---------------------------------------------------------------------
# 🧩 Hilfsfunktionen: Logging, Retry, Throttling
# ---------------------------------------------------------------------

def _log(msg: str) -> None:
    print(f"[CMC] {msg}")


def _on_get(url: str, headers: Dict[str, str], params: Dict[str, Any], max_retries: int = 3) -> Optional[requests.Response]:
    """Zentrale GET-Request-Funktion mit Retry/Backoff-Handling"""
    backoff = [30, 60, 120]
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=20)
            if resp.status_code == 200:
                return resp
            elif resp.status_code == 429:
                wait = backoff[min(attempt, len(backoff)-1)]
                _log(f"⚠️  Rate limit erreicht (429). Warte {wait}s ...")
                time.sleep(wait)
            else:
                _log(f"⚠️  Fehlercode {resp.status_code}: {resp.text[:100]}")
                time.sleep(5)
        except requests.RequestException as e:
            _log(f"⚠️  Netzwerkfehler: {e}. Warte 10s ...")
            time.sleep(10)
    _log("❌ Max. Retries erreicht – Abbruch.")
    return None


# ---------------------------------------------------------------------
# 📊 Hauptfunktion: fetch_cmc_markets()
# ---------------------------------------------------------------------

def fetch_cmc_markets(pages: int = 8, limit: int = 250, cache_dir: str = "snapshots") -> pd.DataFrame:
    """
    Holt aktuelle Markt- und Preisdaten von CoinMarketCap.
    Strukturell kompatibel zu fetch_cg_markets().
    """
    headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY, "Accept": "application/json"}
    all_rows = []

    for page in range(pages):
        start = page * limit + 1
        params = {"start": start, "limit": limit, "convert": "USD"}
        _log(f"Fetching listings page {page+1}/{pages} ...")

        resp = _on_get(CMC_BASE_URL, headers, params)
        if resp is None:
            _log(f"⚠️  Seite {page+1} konnte nicht geladen werden – Abbruch.")
            break

        data = resp.json().get("data", [])
        _log(f"✅ Empfangen: {len(data)} Einträge von CMC.")

        for coin in data:
            quote = coin.get("quote", {}).get("USD", {})
            all_rows.append({
                "id": str(coin.get("id")),
                "symbol": coin.get("symbol"),
                "name": coin.get("name"),
                "current_price": quote.get("price"),
                "market_cap": quote.get("market_cap"),
                "total_volume": quote.get("volume_24h"),
                "price_change_percentage_7d_in_currency": quote.get("percent_change_7d"),
                "price_change_percentage_30d_in_currency": quote.get("percent_change_30d"),
                "ath": quote.get("price"),  # Platzhalter, echte ATH-Berechnung via Klines
                "ath_date": None,           # Kein ATH-Datum in CMC verfügbar
            })

        time.sleep(1.5)  # Throttling
      
    df = pd.DataFrame(all_rows)

    # --- Volume/MarketCap-Ratio (robust berechnet) ---
    if "quote.USD.volume_24h" in df.columns and "quote.USD.market_cap" in df.columns:
        df["volume_mc_ratio"] = np.where(
            (df["quote.USD.market_cap"] > 0) & (df["quote.USD.volume_24h"] > 0),
            df["quote.USD.volume_24h"] / df["quote.USD.market_cap"],
            np.nan
        )
    else:
        logging.warning("[CMC] ⚠️ volume_24h oder market_cap fehlt – volume_mc_ratio = NaN")
        df["volume_mc_ratio"] = np.nan
    
    # --- Sichere Berechnung der Umlaufquote (circ_pct) ---
    if "circulating_supply" in df.columns and "max_supply" in df.columns:
        df["circ_pct"] = df["circulating_supply"] / df["max_supply"]
    else:
        logging.warning("[CMC] ⚠️ circulating_supply oder max_supply fehlt – circ_pct = NaN")
        df["circ_pct"] = np.nan


    # Slug sicherstellen (CMC benötigt ihn für Mapping)
    if "slug" not in df.columns:
        df["slug"] = [None] * len(df)

    # BTC/ETH explizit beibehalten (nur später auswerten)
    # -> kein Filter hier!

    # Cache schreiben
    today = datetime.now().strftime("%Y%m%d")
    os.makedirs(f"{cache_dir}/{today}", exist_ok=True)
    cache_path = f"{cache_dir}/{today}/cmc_markets.csv"
    df.to_csv(cache_path, index=False)

    _log(f"💾 Cache gespeichert unter: {cache_path}")
  
    # ---------------------------------------------------------------------
    # 🧮 Ergänze Prozentänderungen (7d / 30d) analog zur CoinGecko-Struktur
    # ---------------------------------------------------------------------

    # CoinMarketCap liefert pro Coin ein Feld "quote.USD.percent_change_7d" usw.
    # Diese Spalten müssen explizit extrahiert werden, damit compute_feature_block()
    # Momentum-Werte korrekt berechnen oder darauf zurückfallen kann.

    if "quote.USD.percent_change_7d" in df.columns:
        df["price_change_percentage_7d_in_currency"] = df["quote.USD.percent_change_7d"]
    else:
        df["price_change_percentage_7d_in_currency"] = np.nan

    if "quote.USD.percent_change_30d" in df.columns:
        df["price_change_percentage_30d_in_currency"] = df["quote.USD.percent_change_30d"]
    else:
        df["price_change_percentage_30d_in_currency"] = np.nan

    # CoinMarketCap liefert häufig auch "percent_change_24h", das du optional übernehmen kannst
    if "quote.USD.percent_change_24h" in df.columns:
        df["price_change_percentage_24h_in_currency"] = df["quote.USD.percent_change_24h"]

    # Logging zur Kontrolle
    logging.info(
        f"[CMC] Momentum-Spalten ergänzt – 7d: {df['price_change_percentage_7d_in_currency'].notnull().sum()} / "
        f"30d: {df['price_change_percentage_30d_in_currency'].notnull().sum()}"
    )

    return df


# ---------------------------------------------------------------------
# 🔁 MEXC Mapping
# ---------------------------------------------------------------------

def _fetch_mexc_pairs(retries: int = 3, delay: float = 2.0) -> list:
    """
    Lädt alle Spot-Paare von der MEXC-API (USDT-Basispaare).
    Inklusive Retry-Logik bei temporären Fehlern.
    """
    url = "https://api.mexc.com/api/v3/exchangeInfo"
    headers = {"User-Agent": "colabtool/1.0"}

    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=headers, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                pairs = data.get("symbols", [])
                if not pairs:
                    logging.warning("[MEXC] ⚠️ Keine Handelspaare in API-Antwort gefunden.")
                return pairs
            else:
                logging.warning(f"[MEXC] ⚠️ Unerwarteter Statuscode {resp.status_code}, Versuch {attempt+1}/{retries}")
        except Exception as e:
            logging.warning(f"[MEXC] ⚠️ Verbindungsfehler (Versuch {attempt+1}/{retries}): {e}")
        time.sleep(delay)

    logging.error("[MEXC] ❌ API-Abruf nach mehreren Versuchen fehlgeschlagen.")
    return []


def map_mexc_pairs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Verknüpft CMC-Marktdaten mit MEXC-Handelspaaren (USDT).
    Fügt Spalte 'mexc_pair' hinzu.
    """
    logging.info("[MEXC] 🔍 Lade MEXC-Handelspaare ...")
    pairs = _fetch_mexc_pairs()

    if not pairs:
        logging.warning("[MEXC] ⚠️ Keine MEXC-Paare erhalten – Mapping übersprungen.")
        df["mexc_pair"] = None
        return df

    # Vergleichsmenge vorbereiten
    mexc_symbols = {p["baseAsset"].upper() for p in pairs if p.get("quoteAsset") == "USDT"}
    logging.info(f"[MEXC] 🔍 Vergleichsmenge: {len(mexc_symbols)} Symbole geladen.")

    # Symbol-Vergleich robust (Großschreibung)
    df["symbol_upper"] = df["symbol"].astype(str).str.upper()
    df["mexc_pair"] = df["symbol_upper"].apply(
        lambda s: f"{s}USDT" if s in mexc_symbols else None
    )

    hits = df["mexc_pair"].notna().sum()
    logging.info(f"[MEXC] ✅ Mapping abgeschlossen ({hits} Treffer).")
    return df


# ---------------------------------------------------------------------
# 💰 TVL Mapping (optional, unverändert)
# ---------------------------------------------------------------------

def map_tvl(df: pd.DataFrame, seed_tvl_path: str = "seed_tvl_map.csv") -> pd.DataFrame:
    """Fügt TVL-Daten hinzu, falls Seed-Datei vorhanden"""
    if os.path.exists(seed_tvl_path):
        try:
            tvl_df = pd.read_csv(seed_tvl_path)
            df = df.merge(tvl_df, on="id", how="left")
            _log(f"💧 TVL-Mapping erfolgreich: {len(tvl_df)} Einträge.")
        except Exception as e:
            _log(f"⚠️  Fehler beim TVL-Mapping: {e}")
    else:
        _log("ℹ️  Keine TVL-Seed-Datei gefunden.")
    return df


# ---------------------------------------------------------------------
# 💾 Cache-Helper
# ---------------------------------------------------------------------

def load_or_fetch_markets(force_refresh: bool = False) -> pd.DataFrame:
    """Lädt CMC-Markt-Cache oder ruft neu ab"""
    today = datetime.now().strftime("%Y%m%d")
    cache_path = f"snapshots/{today}/cmc_markets.csv"

    if not force_refresh and os.path.exists(cache_path):
        _log(f"📂 Lade Cache aus {cache_path}")
        return pd.read_csv(cache_path)

    _log("🌐 Kein Cache vorhanden oder Refresh angefordert – lade neu von CMC ...")
    return fetch_cmc_markets()


def write_cache(df: pd.DataFrame, name: str) -> None:
    """Schreibt generischen Snapshot-Cache"""
    today = datetime.now().strftime("%Y%m%d")
    os.makedirs(f"snapshots/{today}", exist_ok=True)
    path = f"snapshots/{today}/{name}.csv"
    df.to_csv(path, index=False)
    _log(f"💾 Cache geschrieben: {path}")


# ---------------------------------------------------------------------
# 🧪 Test-Entry-Point
# ---------------------------------------------------------------------

if __name__ == "__main__":
    _log("Starte CMC-Datenabruf ...")
    df = fetch_cmc_markets()
    df = map_mexc_pairs(df)
    df = map_tvl(df)
    _log(f"🏁 Fertig. {len(df)} Einträge geladen.")
    print(df.head(5))

```

## src/colabtool/run_snapshot_mode.py

SHA256: `67a76acb656f2994a6c4fb666d02f08925fea0284dd81697991fbcde0cf98a39`

```python
"""
Run Snapshot Mode – Vereinfachte Pipeline (CMC → MEXC → Feature → Scoring → Backtest → Export)
Nur regulärer Snapshot-Lauf, keine Modi.
"""

import logging
from datetime import datetime
from pathlib import Path
import pandas as pd

from colabtool.data_sources_cmc import fetch_cmc_markets, map_mexc_pairs
from colabtool.data_sources import get_alias_seed
from colabtool.pre_universe import apply_pre_universe_filters
from colabtool.features import compute_feature_block
from colabtool.breakout import compute_breakout_for_ids
from colabtool.buzz import add_buzz_metrics_for_candidates
from colabtool.scores import score_block, compute_early_score
from colabtool.backtest import backtest_on_snapshot
from colabtool.export_helpers import make_fulldata
from colabtool.export import create_full_excel_export
from colabtool.utils.validation import ensure_schema

# ---------------------------------------------------------------------------
# Logging Setup
# ---------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


# ---------------------------------------------------------------------------
# Hilfsfunktion: Score-Validierung
# ---------------------------------------------------------------------------
def validate_scores(df: pd.DataFrame) -> None:
    required_cols = ["early_score", "breakout_score"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"⚠️ Fehlende Score-Spalten: {missing}")

    nan_counts = df[required_cols].isna().sum()
    if nan_counts.any():
        logging.warning(f"NaN-Werte in Scores: {nan_counts.to_dict()}")
        df.dropna(subset=required_cols, inplace=True)

    valid_count = len(df)
    if valid_count < 100:
        raise ValueError(f"⚠️ Zu wenige valide Scores: {valid_count}")

    logging.info(f"✅ Score-Validierung bestanden ({valid_count} valide Zeilen)")


# ---------------------------------------------------------------------------
# Hauptfunktion: Snapshot-Pipeline
# ---------------------------------------------------------------------------
def run_snapshot() -> Path:
    """Führt den vollständigen Snapshot-Lauf aus (CMC → MEXC → Feature → Scoring → Backtest → Export)."""

    ASOF_DATE = datetime.today().strftime("%Y%m%d")
    snapshot_dir = Path("snapshots") / ASOF_DATE
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    logging.info(f"🚀 Starte Snapshot-Lauf für {ASOF_DATE}")

    # 1️⃣ Universe laden (CMC)
    df = fetch_cmc_markets(pages=8, limit=250)
    logging.info(f"✅ [CMC] {len(df)} Coins geladen, Columns: {list(df.columns)}")

    # 2️⃣ MEXC Mapping
    logging.info("[TRACE] Starte map_mexc_pairs() in Snapshot-Pipeline")
    try:
        df = map_mexc_pairs(df)
        hits = df["mexc_pair"].notna().sum()
        logging.info(f"[MEXC] ✅ Mapping abgeschlossen ({hits} Treffer von {len(df)}).")
        if hits == 0:
            logging.warning("[MEXC] ⚠️ Keine Treffer beim Mapping – prüfe API oder Symbolabgleich.")
    except Exception as e:
        logging.error(f"[MEXC] ❌ Fehler beim Mapping: {e}", exc_info=True)

    logging.info(f"[MEXC] 🔍 Vor Filterung: {df['mexc_pair'].notna().sum()} Coins mit MEXC-Paar")

    # 3️⃣ Schema-Validierung
    SCHEMA_MAP = {
        "id": str,
        "symbol": str,
        "market_cap": float,
        "total_volume": float,
        "early_score": float,
        "breakout_score": float,
        "mexc_pair": str,
        "ath": float,
        "current_price": float,
    }
    df = ensure_schema(df, SCHEMA_MAP)
    logging.info(f"[TRACE] Nach ensure_schema: {len(df)} Zeilen, Columns: {list(df.columns)}")

    # 4️⃣ Feature- & Momentum-Berechnung
    logging.info(f"[TRACE] Vor apply_pre_universe_filters: {len(df)} Zeilen")
    df = apply_pre_universe_filters(df)
    logging.info(f"✅ apply_pre_universe_filters: {len(df)} nach Filtern")

    df = compute_feature_block(df)
    logging.info("✅ compute_feature_block abgeschlossen")

    cand_ids = df["id"].tolist()
    df = compute_breakout_for_ids(df, cand_ids)
    logging.info("✅ compute_breakout_for_ids abgeschlossen")

    df = add_buzz_metrics_for_candidates(df)
    logging.info("✅ add_buzz_metrics_for_candidates abgeschlossen")

    # 5️⃣ Scoring
    logging.info(f"[TRACE] Vor Scoring: {len(df)} Zeilen")
    df = score_block(df)
    df = compute_early_score(df)
    logging.info("✅ Scores & Early Score berechnet")

    # 6️⃣ Validierung & Backtest
    validate_scores(df)
    backtest_results = backtest_on_snapshot(df, top_k=20, horizons=[20, 40, 60])
    logging.info(f"✅ Backtest abgeschlossen ({len(backtest_results)} Zeilen)")

    # 7️⃣ Export
    full_df = make_fulldata(df)
    export_filename = f"{ASOF_DATE}_fullsnapshot.xlsx"
    export_path = snapshot_dir / export_filename

    logging.info(f"📦 Erzeuge Excel → {export_path}")
    create_full_excel_export(full_df, export_path, extra_sheets={"Backtest": backtest_results})

    # 8️⃣ CSV-Exports
    cg_path = snapshot_dir / "cmc_markets.csv"
    mexc_path = snapshot_dir / "mexc_pairs.csv"
    alias_path = snapshot_dir / "seed_alias.csv"

    df.to_csv(cg_path, index=False)
    logging.info(f"✅ cmc_markets.csv gespeichert ({cg_path})")

    if "mexc_pair" in df.columns:
        df[["id", "symbol", "mexc_pair"]].to_csv(mexc_path, index=False)
        logging.info(f"✅ mexc_pairs.csv gespeichert ({mexc_path})")

    if not alias_path.exists():
        seed_alias = get_alias_seed()
        seed_alias.to_csv(alias_path, index=False)
        logging.info(f"⚠️ seed_alias.csv neu erstellt → {alias_path}")

    logging.info(f"🎯 Snapshot abgeschlossen → {export_path}")
    return export_path


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    logging.info("🚀 Starte regulären Snapshot-Lauf (kein Modus-System mehr aktiv).")
    run_snapshot()

```

## src/colabtool/export.py

SHA256: `5861961362a5a58ae15d0838f82ba58d7bb141501f65f481d998297a05333533`

```python
from __future__ import annotations
from typing import Dict, Any
from .utilities import pd, np, logging
from pandas.api.types import (
    is_datetime64_any_dtype,
    is_categorical_dtype,
    is_numeric_dtype,
)

_DEF_MIN = 10
_DEF_MAX = 40
_DEF_FALLBACK = 12

EXPORT_PATH = "/content/drive/MyDrive/Colab results"


# -----------------------------------------------------
# Hilfsfunktionen für Spaltenformatierung
# -----------------------------------------------------
def _safe_col_width(s: pd.Series) -> int:
    if s is None or s.empty:
        return _DEF_FALLBACK
    if is_numeric_dtype(s):
        formatted = [len(f"{v:.2f}") for v in s if pd.notna(v)]
        if not formatted:
            return _DEF_FALLBACK
        return max(_DEF_MIN, min(_DEF_MAX, int(np.nanmean(formatted) + 2)))
    if is_datetime64_any_dtype(s):
        return _DEF_MAX
    if is_categorical_dtype(s):
        return max(_DEF_MIN, min(_DEF_MAX, s.astype(str).str.len().max()))
    return max(_DEF_MIN, min(_DEF_MAX, s.astype(str).str.len().max()))


# -----------------------------------------------------
# Spalten-Reihenfolge (fixiert Score-Spalten frühzeitig)
# -----------------------------------------------------
def reorder_columns(df: pd.DataFrame) -> pd.DataFrame:
    fixed_order = [
        "id", "symbol", "name", "market_cap",
        "score_global", "score_segment", "early_score",
        "total_volume", "Kategorie", "Segment"
    ]
    available = [col for col in fixed_order if col in df.columns]
    remaining = [col for col in df.columns if col not in available]
    return df[available + remaining]


# -----------------------------------------------------
# Haupt-Exportsheet
# -----------------------------------------------------
def write_sheet(df: pd.DataFrame, name: str, writer) -> None:
    df = df.copy()
    df = reorder_columns(df)

    # Sicherstellen, dass Score-Spalten existieren
    required_cols = ["score_global", "score_segment", "early_score"]
    for col in required_cols:
        if col not in df.columns:
            logging.warning(f"⚠️ Spalte {col} fehlt im Export – wird mit NaN ergänzt.")
            df[col] = np.nan

    # Sortierung nach globalem Score, falls vorhanden
    if "score_global" in df.columns:
        try:
            df = df.sort_values("score_global", ascending=False)
        except Exception as ex:
            logging.warning(f"⚠️ Sortierung nach score_global fehlgeschlagen: {ex}")

    df.to_excel(writer, sheet_name=name, index=False)
    worksheet = writer.sheets[name]

    fmt_thousands = None
    fmt_percent = None
    try:
        if hasattr(writer, "book") and hasattr(writer.book, "add_format"):
            fmt_thousands = writer.book.add_format({"num_format": "#,##0", "align": "right"})
            fmt_percent = writer.book.add_format({"num_format": "0.00%", "align": "right"})
    except Exception as ex:
        print(f"⚠️ Formatierungswarnung (non-fatal): {ex}")

    use_xlsxwriter = hasattr(worksheet, "set_column")

    for idx, col in enumerate(df.columns):
        width = _safe_col_width(df[col])
        if use_xlsxwriter:
            if col in ("market_cap", "total_volume"):
                worksheet.set_column(idx, idx, width, fmt_thousands)
            elif col in ("mom_7d_pct", "mom_30d_pct"):
                worksheet.set_column(idx, idx, width, fmt_percent)
            else:
                worksheet.set_column(idx, idx, width)
        else:
            try:
                col_letter = worksheet.cell(row=1, column=idx + 1).column_letter
                worksheet.column_dimensions[col_letter].width = width
            except Exception as ex:
                print(f"⚠️ Spaltenbreite konnte nicht gesetzt werden ({col}): {ex}")


# -----------------------------------------------------
# Meta-Sheet
# -----------------------------------------------------
def write_meta_sheet(writer, meta: Dict[str, Any]) -> None:
    meta_df = pd.DataFrame.from_dict(meta, orient="index", columns=["Value"])
    meta_df.reset_index(inplace=True)
    meta_df.columns = ["Key", "Value"]
    meta_df.to_excel(writer, sheet_name="Meta", index=False)
    worksheet = writer.sheets["Meta"]
    worksheet.set_column(0, 0, 40)
    worksheet.set_column(1, 1, 80)


# -----------------------------------------------------
# Vollständiger Excel-Export (inkl. Zusatz-Sheets)
# -----------------------------------------------------
def create_full_excel_export(
    df: pd.DataFrame,
    output_path: str,
    extra_sheets: dict[str, pd.DataFrame] | None = None
) -> None:
    """
    Erstellt vollständigen Excel-Export mit Rankings, FullData und optionalen Zusatz-Sheets (z. B. Backtest).
    """
    logging.info(f"📊 Erzeuge Excel mit Rankings → {output_path}")

    # Sicherstellen, dass Score-Spalten existieren
    required_cols = ["score_global", "score_segment", "early_score"]
    for col in required_cols:
        if col not in df.columns:
            logging.warning(f"⚠️ Spalte {col} fehlt in DataFrame – wird mit NaN ergänzt.")
            df[col] = np.nan

    # Rankings
    top25_global = df.sort_values("score_global", ascending=False).head(25)
    top10_hidden = df[df["market_cap"] <= 150_000_000].sort_values("score_global", ascending=False).head(10)
    top10_emerging = df[
        (df["market_cap"] > 150_000_000) & (df["market_cap"] <= 500_000_000)
    ].sort_values("score_global", ascending=False).head(10)
    top25_early = df.sort_values("early_score", ascending=False).head(25)

    # Excel exportieren
    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
        write_sheet(top25_global, "Top25_Global", writer)
        write_sheet(top10_hidden, "Top10_HiddenGem", writer)
        write_sheet(top10_emerging, "Top10_Emerging", writer)
        write_sheet(top25_early, "Top25_EarlySignals", writer)
        write_sheet(df, "FullData", writer)
        write_meta_sheet(writer, {"generated": pd.Timestamp.now()})

        # 🔹 Zusatz-Sheets (z. B. Backtest)
        if extra_sheets:
            for sheet_name, sheet_df in extra_sheets.items():
                if sheet_df is not None and not sheet_df.empty:
                    write_sheet(sheet_df, sheet_name, writer)

    logging.info(f"✅ Excel erfolgreich exportiert: {output_path}")

# Alte Funktion export-snapshot wiederherstellen
def export_snapshot(df, export_path: str | None = None):
    """
    Legacy wrapper for backward compatibility.
    Delegates to create_full_excel_export() using make_fulldata().
    """
    import os
    import logging
    from datetime import datetime
    from .export_helpers import make_fulldata

    if export_path is None:
        asof = datetime.today().strftime("%Y%m%d")
        snapshot_dir = os.path.join("snapshots", asof)
        os.makedirs(snapshot_dir, exist_ok=True)
        export_path = os.path.join(snapshot_dir, f"{asof}_fullsnapshot.xlsx")

    full_df = make_fulldata(df)

    try:
        create_full_excel_export(full_df, export_path)
        logging.info(f"✅ Exported snapshot to {export_path}")
    except Exception as e:
        logging.exception(f"❌ export_snapshot failed: {e}")
        raise

    return export_path



```

## src/colabtool/features.py

SHA256: `eb9e4943fcaf2c401bb5e128e8d2189c8682eaf0a240e53087414137ae2d7e69`

```python
# modules/features.py
from __future__ import annotations

import re
import pandas as pd
import logging
from .utilities import pd, np, logging
from colabtool.utils.validation import ensure_schema

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
# ---------------------------------------------------------------------
# 📊 Neue Hybrid-Feature-Logik: MEXC-Klines + CMC-Fallback
# ---------------------------------------------------------------------
import requests
import numpy as np
import pandas as pd
import logging
from typing import Optional, Dict, Any, List

MEXC_KLINES_URL = "https://api.mexc.com/api/v3/klines"

def fetch_mexc_klines(symbol: str, interval: str = "1d", limit: int = 60) -> Optional[pd.DataFrame]:
    """
    Holt historische Candle-Daten (Klines) von der MEXC Spot API.
    Rückgabeformat: DataFrame mit Spalten [time, open, high, low, close, volume].
    Gibt None zurück, wenn keine Daten oder ein HTTP-Fehler auftritt.
    """
    try:
        resp = requests.get(
            "https://api.mexc.com/api/v3/klines",
            params={"symbol": symbol.upper(), "interval": interval, "limit": limit},
            timeout=10
        )

        # --- Kein Handelspaar vorhanden oder API-Fehler ---
        if resp.status_code == 400:
            logging.info(f"[MEXC] Kein Klines-Listing für {symbol} – Fallback auf CMC aktiv.")
            return None
        if resp.status_code != 200:
            logging.warning(f"[MEXC] Klines-Fehler {symbol}: {resp.status_code}")
            return None

        data = resp.json()
        if not data or not isinstance(data, list):
            logging.warning(f"[MEXC] Klines-Response leer oder ungültig für {symbol}")
            return None

        # --- Laut API: [open_time, open, high, low, close, volume, close_time, quote_volume]
        # Wir extrahieren nur die relevanten OHLCV-Spalten.
        cleaned_data = [row[:6] for row in data if len(row) >= 6]

        df = pd.DataFrame(cleaned_data, columns=["time", "open", "high", "low", "close", "volume"])
        df["time"] = pd.to_datetime(df["time"], unit="ms")

        # --- Typkonvertierung sicherstellen ---
        for col in ["open", "high", "low", "close", "volume"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # --- Debug-Logging ---
        logging.debug(f"[MEXC] {symbol}: {len(df)} Candles geladen, Spalten: {list(df.columns)}")

        return df

    except Exception as e:
        logging.warning(f"[MEXC] Klines-Abfrage fehlgeschlagen ({symbol}): {e}")
        return None

def compute_mexc_features(df: pd.DataFrame) -> Dict[str, float]:
    """Berechnet Momentum, Volumenbeschleunigung, ATH-Drawdown aus MEXC-Klines"""
    if df is None or df.empty:
        return {"mom_7d_pct": np.nan, "mom_30d_pct": np.nan, "vol_acc": np.nan, "ath_drawdown_pct": np.nan}

    closes = df["close"].values
    vols = df["volume"].values
    if len(closes) < 30:
        return {"mom_7d_pct": np.nan, "mom_30d_pct": np.nan, "vol_acc": np.nan, "ath_drawdown_pct": np.nan}

    mom_7d_pct = (closes[-1] / closes[-8] - 1) * 100
    mom_30d_pct = (closes[-1] / closes[-31] - 1) * 100
    vol_acc = np.mean(vols[-7:]) / np.mean(vols[-30:]) if np.mean(vols[-30:]) > 0 else np.nan
    ath = np.max(closes)
    ath_idx = int(np.argmax(closes))
    ath_date = df["time"].iloc[ath_idx]
    ath_drawdown_pct = (closes[-1] / ath - 1) * 100

    return {
        "mom_7d_pct": mom_7d_pct,
        "mom_30d_pct": mom_30d_pct,
        "vol_acc": vol_acc,
        "ath": ath,
        "ath_date": ath_date,
        "ath_drawdown_pct": ath_drawdown_pct,
    }


def compute_feature_block(df_in: pd.DataFrame) -> pd.DataFrame:
    """
    Neues Feature-Block-Modul:
    - bevorzugt Momentum & Volumen aus MEXC-Klines
    - fallback auf CMC-Prozentwerte
    """
    logging.info("🧩 Starte compute_feature_block() ...")

    # Ergebnislisten initialisieren (Hotfix gegen NameError)
    mom7 = []
    mom30 = []
    vol_acc = []
    ath_dd = []
    ath_vals = []
    ath_dates = []
    price_sources = []

    df = df_in.copy()

    for _, row in df.iterrows():
        # --- Symbol ermitteln & validieren ---
        symbol = str(row.get("symbol", "")).strip().upper()
        if not symbol:
            logging.warning("[MEXC] ⚠️ Kein Symbol in Zeile gefunden – übersprungen.")
            mom7.append(np.nan)
            mom30.append(np.nan)
            vol_acc.append(np.nan)
            ath_dd.append(np.nan)
            ath_vals.append(np.nan)
            ath_dates.append(np.nan)
            price_sources.append("CMC")
            continue
    
        # MEXC-Pairs enden üblicherweise auf USDT
        pair = f"{symbol}USDT"
    
        # --- Versuche Klines abzurufen ---
        kl = fetch_mexc_klines(pair)
        if kl is not None and len(kl) >= 5:
            try:
                f = compute_mexc_features(kl)
                mom7.append(f.get("mom_7d_pct", np.nan))
                mom30.append(f.get("mom_30d_pct", np.nan))
                vol_acc.append(f.get("vol_acc", np.nan))
                ath_dd.append(f.get("ath_drawdown_pct", np.nan))
                # Neue Felder
                ath_vals.append(f.get("ath", np.nan))
                ath_dates.append(f.get("ath_date", np.nan))
                price_sources.append("MEXC")
                logging.debug(f"[MEXC] ✅ Klines verarbeitet: {pair}")
            except Exception as e:
                logging.warning(f"[MEXC] ⚠️ Fehler bei Feature-Berechnung {pair}: {e}")
                mom7.append(np.nan)
                mom30.append(np.nan)
                vol_acc.append(np.nan)
                ath_dd.append(np.nan)
                ath_vals.append(np.nan)
                ath_dates.append(np.nan)
                price_sources.append("CMC")
        else:
            # --- Fallback auf CMC-Prozentwerte ---
            mom7.append(row.get("price_change_percentage_7d_in_currency", np.nan))
            mom30.append(row.get("price_change_percentage_30d_in_currency", np.nan))
            vol_acc.append(np.nan)
            ath_dd.append(np.nan)
            ath_vals.append(np.nan)
            ath_dates.append(np.nan)
            price_sources.append("CMC")
            logging.info(f"[MEXC] ⚙️ Fallback auf CMC-Daten: {pair}")


    df["mom_7d_pct"] = mom7
    df["mom_30d_pct"] = mom30
    df["vol_acc"] = vol_acc
    df["ath_drawdown_pct"] = ath_dd

    # --- Schema-Validierung & Typkonvertierung ---
    schema_map = {
        "mom_7d_pct": float,
        "mom_30d_pct": float,
        "vol_acc": float,
        "ath": float,
        "ath_date": "datetime64[ns]",
        "ath_drawdown_pct": float,
        "volume_mc_ratio": float,
        "circ_pct": float,
        "price_source": str,
    }

    df = ensure_schema(df, schema_map)
    
    logging.info(f"[features] 🧮 compute_feature_block abgeschlossen – {len(df)} Zeilen verarbeitet")
    logging.info(f"[features] Beispiel-Ausgabe: mom_7d={len(mom7)}, ath_vals={len(ath_vals)}, price_sources={len(price_sources)}")
    
    return df
    
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

SHA256: `00f22d8e56a1ea954f2918816c5308f264e691da66de72d9ccaa19495835a75f`

```python

# modules/breakout.py
from __future__ import annotations

import math
import time
from typing import Dict, List, Optional, Tuple

import requests
from .utilities import pd, np, logging

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
    # Zusätzliche Metadaten aus Ursprungs-DF übernehmen
    meta_cols = ["market_cap", "symbol"]
    for mc in meta_cols:
        if mc in df_all.columns:
            dfb = dfb.merge(df_all[["id", mc]], on="id", how="left")

    keep = [
        "id","symbol","market_cap",
        "breakout_score","z_break","z_donch","dist_90","dist_180","dist_365",
        "p365","vol_acc","vol_acc_7d","vol_acc_30d","break_vol_mult","donch_width","beta_btc","beta_eth","price_source"
    ]
    for k in keep:
        if k not in dfb.columns:
            dfb[k] = np.nan
    return dfb[keep].copy()



```

## src/colabtool/exchanges.py

SHA256: `3c11a937734f3a73827fcc8eef497659bfed031a595d12cb764f017d41d688bf`

```python
from __future__ import annotations

import os
import time
from typing import Dict, List, Optional, Tuple
from pathlib import Path

import requests
from .utilities import pd, np, logging

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

def fetch_mexc_pairs(force: bool = False) -> pd.DataFrame:
    """
    Lädt alle verfügbaren Handelspaare live von der MEXC-API.
    Nutzt /api/v3/exchangeInfo und erstellt DataFrame mit Basis, Quote, Symbol.
    """
    try:
        df = _load_mexc_listing()
        if df is None or df.empty:
            raise RuntimeError("MEXC returned no data.")
        print(f"✅ fetch_mexc_pairs: {len(df)} Handelspaare live von MEXC geladen.")
        return df

    except Exception as e:
        print(f"[warn] fetch_mexc_pairs fehlgeschlagen: {e}")
        return pd.DataFrame(columns=["base", "quote", "symbol"])

```

## src/colabtool/utilities.py

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

## src/colabtool/buzz.py

SHA256: `2e81f6f7e5caceb0abbf26b011022bb096aefc0765f2ad49bb0ec8b728ed8d84`

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

```

## src/colabtool/data_sources.py

SHA256: `8d1b6cc710d257e3477de4326ff80c4e4e3f6887538779bdfc7acb40f2074cd5`

```python
# modules/data_sources.py
from __future__ import annotations

import os
import json
import time
from typing import Dict, List, Optional, Union
from pathlib import Path

import requests
from .utilities import pd, np, logging, CACHE_DIR as _UTILS_CACHE_DIR

__all__ = [
    "cg_markets",
    "enrich_categories",
    "map_tvl",
    "update_seen_ids",
    "cg_market_chart",
    "persist_pit_snapshot",
    "map_mexc_pairs",
    "get_alias_seed",
    "ensure_seed_alias_exists",
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
_CG_RETRY_AFTER_CAP_S = _env_float("CG_RETRY_AFTER_CAP_S", 60.0)
_CG_BACKOFF_BASE_S = _env_float("CG_BACKOFF_BASE_S", 2.0)
_CG_MIN_INTERVAL_S = _env_float("CG_MIN_INTERVAL_S", 10)

_CG_CATS_TIME_BUDGET_S = _env_float("CG_CATS_TIME_BUDGET_S", 300.0)

# ----------------------------
# CoinGecko Rate-Limit Handling
# ----------------------------
import time

_last_cg_request = 0.0

def _cg_throttle():
    """Begrenzt Aufrufrate der CoinGecko-API, um 429-Fehler zu vermeiden."""
    global _last_cg_request
    now = time.time()
    delta = now - _last_cg_request
    if delta < _CG_MIN_INTERVAL_S:
        wait = _CG_MIN_INTERVAL_S - delta
        print(f"⏳ Warte {wait:.1f}s, um CoinGecko-Rate-Limit einzuhalten ...")
        time.sleep(wait)
    _last_cg_request = time.time()

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

    j = _one_get(_session_free, _FREE_BASE, path, _sanitize_params_for_free(params), max_att)
    if isinstance(j, (dict, list)) or not _HAS_PRO:
        return j

    p2 = dict(params)
    p2["x_cg_pro_api_key"] = _CG_KEY
    return _one_get(_session_pro, _PRO_BASE, path, p2, max_att)


# ----------------------------
# Public API
# ----------------------------
import pandas as pd
from datetime import datetime


def _get_snapshot_dir() -> str:
    """Erzeugt und gibt das Tagesverzeichnis unter snapshots/YYYYMMDD zurück."""
    today = datetime.today().strftime("%Y%m%d")
    path = os.path.join("snapshots", today)
    os.makedirs(path, exist_ok=True)
    return path


def _make_cache_path(filename: str) -> str:
    """Erzeugt einen absoluten Pfad im Tagesverzeichnis."""
    return os.path.join(_get_snapshot_dir(), filename)


def _chart_cache_path(coin_id: str, vs: str, days: int, interval: str) -> Path:
    """Erzeugt einen Cache-Pfad für historische Kursdaten."""
    fn = f"cg_chart_{coin_id}_{vs}_{days}_{interval}.json".replace("/", "_")
    p = Path(_make_cache_path(fn))
    try:
        p.parent.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass
    return p


def cg_markets(vs: str = "usd", pages: int = 4, cache_hours: int = 24) -> pd.DataFrame:
    """
    Lädt CoinGecko-Markt-Daten mit automatischem Cache-Mechanismus.
    - nutzt lokalen Cache (snapshots/cg_markets.csv), wenn <cache_hours alt
    - sonst lädt Live-Daten von der CoinGecko API
    """
    cache_path = _make_cache_path("cg_markets.csv")
    use_live = True

    if os.path.exists(cache_path):
        mtime = datetime.fromtimestamp(os.path.getmtime(cache_path))
        age_hours = (datetime.now() - mtime).total_seconds() / 3600
        if age_hours <= cache_hours:
            print(f"✅ Verwende gecachte CoinGecko-Daten ({age_hours:.1f}h alt)")
            df = pd.read_csv(cache_path)
            use_live = False
        else:
            print(f"⚠️ Cache älter als {cache_hours}h – hole Live-Daten von CoinGecko ...")

    if use_live:
        all_pages = []
        for page in range(1, pages + 1):
            url = (
                f"https://api.coingecko.com/api/v3/coins/markets?"
                f"vs_currency={vs}&order=market_cap_desc&per_page=250&page={page}"
                f"&sparkline=false&price_change_percentage=1h,24h,7d,30d"
            )
            print(f"🔄 Hole CoinGecko Seite {page}/{pages} ...")
            try:
                _cg_throttle()
                resp = requests.get(url, timeout=15)
                if resp.status_code == 429:
                    print("⏳ Rate limit erreicht – warte 30s ...")
                    time.sleep(30)
                    resp = requests.get(url, timeout=15)
                resp.raise_for_status()
                data = resp.json()
                all_pages.extend(data)
                # --- Sicherstellen, dass Momentum-Felder in allen Seiten beibehalten werden ---
                for entry in data:
                    for key in [
                        "price_change_percentage_1h_in_currency",
                        "price_change_percentage_24h_in_currency",
                        "price_change_percentage_7d_in_currency",
                        "price_change_percentage_30d_in_currency",
                    ]:
                        if key not in entry:
                            entry[key] = None
            except Exception as e:
                raise ValueError(f"❌ Fehler beim Laden von CoinGecko Seite {page}: {e}")

        df = pd.DataFrame(all_pages)
        # --- Sicherstellen, dass Momentum-Felder aus CoinGecko erhalten bleiben ---
        momentum_cols = [
            "price_change_percentage_1h_in_currency",
            "price_change_percentage_24h_in_currency",
            "price_change_percentage_7d_in_currency",
            "price_change_percentage_30d_in_currency",
        ]

        # CoinGecko liefert diese Felder manchmal nur für Teilmengen – fehlende Spalten ergänzen:
        for col in momentum_cols:
            if col not in df.columns:
                df[col] = np.nan
                
        df.to_csv(cache_path, index=False)
        print(f"✅ Live CoinGecko-Daten geladen ({len(df)} Einträge) und gecached")

    if "total_volume" not in df.columns:
        alt_cols = [c for c in df.columns if "volume" in c.lower()]
        if alt_cols:
            logging.warning(f"⚠️ 'total_volume' nicht gefunden – verwende Ersatzspalte '{alt_cols[0]}'")
            df["total_volume"] = df[alt_cols[0]]
        else:
            df["total_volume"] = 0

    df = df[df["market_cap"].notna() & df["total_volume"].notna()]
    print(f"[INFO] cg_markets: {len(df)} valide Coins nach Filterung")
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
        if sleep_s:
            time.sleep(sleep_s)
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


def cg_market_chart(coin_id: str, vs: str = "usd", days: int = 60, interval: str = "daily", ttl_s: int = 6 * 3600) -> dict:
    """
    Robust fetch for /coins/{id}/market_chart
    Includes retries, rate-limit handling, and local cache validation.
    Used primarily for momentum fallback.
    """
    import json, os, time, requests
    from datetime import datetime

    coin_id = str(coin_id).strip().lower()
    vs = str(vs).strip().lower() or "usd"
    days = int(max(1, min(days, 3650)))
    interval = "daily" if str(interval).lower() not in ["hourly"] else interval

    cpath = _chart_cache_path(coin_id, vs, days, interval)

    # --- Step 1: Cache verwenden, wenn frisch ---
    if cpath.is_file():
        try:
            age_h = (time.time() - cpath.stat().st_mtime) / 3600
            if age_h < (ttl_s / 3600):
                with cpath.open("r") as f:
                    data = json.load(f)
                if isinstance(data, dict) and "prices" in data and len(data["prices"]) > 0:
                    return data
        except Exception:
            pass

    # --- Step 2: Live-Daten von CoinGecko abrufen ---
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": vs, "days": days, "interval": interval}

    for attempt in range(3):
        try:
            _cg_throttle()
            resp = requests.get(url, params=params, timeout=20)
            if resp.status_code == 429:
                print(f"⏳ Rate limit (429) bei {coin_id} – warte 30s ...")
                time.sleep(30)
                continue
            resp.raise_for_status()
            data = resp.json()

            # Sicherstellen, dass Daten vorhanden sind
            if not isinstance(data, dict) or "prices" not in data or len(data["prices"]) == 0:
                print(f"⚠️ Keine gültigen Preise für {coin_id} erhalten (Versuch {attempt+1})")
                time.sleep(3)
                continue

            # Cache schreiben
            try:
                cpath.parent.mkdir(parents=True, exist_ok=True)
                with cpath.open("w") as f:
                    json.dump(data, f)
            except Exception:
                pass

            return data

        except Exception as e:
            print(f"⚠️ Fehler beim Abruf von cg_market_chart({coin_id}): {e}")
            time.sleep(3)

    # --- Step 3: Fallback, wenn gar nichts klappt ---
    print(f"❌ Kein gültiges Chart für {coin_id} verfügbar – gebe leeren Preisverlauf zurück.")
    return {"prices": []}


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


def get_alias_seed() -> pd.DataFrame:
    """
    Lädt Alias-Daten live von CoinGecko.
    Erstellt eine Alias-Tabelle (alias = Name, coin_id = CoinGecko-ID)
    und liefert sie als DataFrame zurück.
    """
    try:
        from colabtool.category_providers import get_cg_categories
        cg_data = get_cg_categories()
        if not cg_data:
            print("[warn] Keine CoinGecko-Daten empfangen – leere Tabelle wird erzeugt")
            return pd.DataFrame(columns=["alias", "coin_id"])

        aliases = []
        for c in cg_data:
            if isinstance(c, dict) and "id" in c and "name" in c:
                aliases.append({"alias": c["name"], "coin_id": c["id"]})

        df = pd.DataFrame(aliases)
        print(f"✅ get_alias_seed: {len(df)} Einträge von CoinGecko geladen.")
        return df

    except Exception as e:
        print(f"[warn] get_alias_seed fehlgeschlagen: {e}")
        return pd.DataFrame(columns=["alias", "coin_id"])


# ----------------------------
# MEXC Mapping (verbessert)
# ----------------------------
def map_mexc_pairs(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ergänzt die Spalte 'mexc_pair' basierend auf der offiziellen MEXC Spot API v3.

    Ablauf:
    1. Versucht, gecachte Daten (max. 24h alt) aus snapshots/ zu laden.
    2. Wenn kein Cache oder veraltet → lädt Live-Daten von MEXC:
       - /api/v3/exchangeInfo (offizielle Quelle)
       - Fallbacks: /api/v3/defaultSymbols und /open/api/v2/market/symbols
    3. Extrahiert 'base' und 'quote' robust (unterstützt baseAsset/quoteAsset oder parsing aus 'symbol').
    4. Normalisiert Symbole und mappt CoinGecko-Symbole zu MEXC-Paaren.
    5. Gibt das ursprüngliche DataFrame mit neuer Spalte 'mexc_pair' zurück.
    """
    import pandas as pd
    import requests

    cache_path = _make_cache_path("mexc_pairs.csv")
    use_live = True
    mexc_pairs = None

    # === 1️⃣ Cache prüfen ===
    if os.path.exists(cache_path):
        mtime = datetime.fromtimestamp(os.path.getmtime(cache_path))
        age_hours = (datetime.now() - mtime).total_seconds() / 3600
        if age_hours <= 24:
            print(f"✅ Verwende gecachte MEXC-Daten ({age_hours:.1f}h alt)")
            mexc_pairs = pd.read_csv(cache_path)
            use_live = False
        else:
            print("⚠️ Cache älter als 24h – hole Live-Daten ...")

    # === 2️⃣ Live-Daten laden ===
    if use_live:
        data = []
        try:
            # Offizielle API (Spot v3)
            url = "https://api.mexc.com/api/v3/exchangeInfo"
            resp = requests.get(url, timeout=20)
            resp.raise_for_status()
            data = resp.json().get("symbols", [])
            if not data:
                print("⚠️ exchangeInfo leer – Fallback auf /api/v3/defaultSymbols ...")
                resp2 = requests.get("https://api.mexc.com/api/v3/defaultSymbols", timeout=10)
                resp2.raise_for_status()
                symbols = resp2.json()
                data = [
                    {"symbol": s, "baseAsset": s.split('_')[0], "quoteAsset": s.split('_')[1]}
                    for s in symbols if "_" in s
                ]
            if not data:
                print("⚠️ /defaultSymbols leer – Fallback auf /open/api/v2/market/symbols ...")
                resp3 = requests.get("https://www.mexc.com/open/api/v2/market/symbols", timeout=10)
                resp3.raise_for_status()
                data2 = resp3.json().get("data", [])
                data = [
                    {
                        "symbol": d.get("symbol"),
                        "baseAsset": d.get("symbol", "").split("_")[0] if "_" in d.get("symbol", "") else d.get("symbol"),
                        "quoteAsset": d.get("symbol", "").split("_")[1] if "_" in d.get("symbol", "") else "USDT",
                    }
                    for d in data2 if isinstance(d, dict) and "symbol" in d
                ]
        except Exception as e:
            print(f"⚠️ MEXC API-Fehler: {e}")
            data = []

        if data:
            mexc_pairs = pd.DataFrame(data)
            os.makedirs("snapshots", exist_ok=True)
            mexc_pairs.to_csv(cache_path, index=False)
            print(f"✅ Live MEXC-Daten geladen ({len(mexc_pairs)} Paare) und gecached")
        else:
            print("⚠️ Keine MEXC-Daten verfügbar – Mapping übersprungen.")
            df["mexc_pair"] = None
            return df

    # === 3️⃣ Robustheit: Spalten vereinheitlichen ===
    rename_map = {
        "baseAsset": "base",
        "quoteAsset": "quote",
        "baseCurrency": "base",
        "quoteCurrency": "quote",
    }
    mexc_pairs = mexc_pairs.rename(columns=rename_map, errors="ignore")

    if "base" not in mexc_pairs.columns or "quote" not in mexc_pairs.columns:
        # Fallback: parse aus symbol falls nötig
        if "symbol" in mexc_pairs.columns:
            mexc_pairs["base"] = mexc_pairs["symbol"].str.replace("-", "_").str.replace("/", "_").str.split("_").str[0]
            mexc_pairs["quote"] = mexc_pairs["symbol"].str.replace("-", "_").str.replace("/", "_").str.split("_").str[1]
            print("⚙️ 'base'/'quote' aus 'symbol' extrahiert (Fallback).")
        else:
            logging.warning("⚠️ Keine Basisdaten in MEXC-Pairs – Dummy-Werte gesetzt.")
            df["mexc_pair"] = None
            return df

    # === 4️⃣ Datenbereinigung ===
    for col in ["base", "quote"]:
        mexc_pairs[col] = mexc_pairs[col].astype(str).str.upper().str.strip()

    # Nur relevante Stablecoin-Quotes
    mexc_pairs = mexc_pairs[mexc_pairs["quote"].isin(["USDT", "USDC", "USD"])]

    # === 5️⃣ Normalisierung & Mapping ===
    def normalize_symbol(sym):
        if not isinstance(sym, str):
            return ""
        sym = sym.upper().strip()
        sym = sym.replace("-", "_").replace("/", "_")
        return sym

    df["symbol"] = df["symbol"].astype(str).str.upper()
    mexc_pairs["base_norm"] = mexc_pairs["base"].apply(normalize_symbol)
    mapping = dict(zip(mexc_pairs["base_norm"], mexc_pairs["symbol"]))

    df["mexc_pair"] = df["symbol"].map(mapping)
    found = df["mexc_pair"].notna().sum()

    ratio = (found / len(df) * 100) if len(df) else 0
    print(f"✅ map_mexc_pairs: {found} gültige Paare gefunden ({found}/{len(df)} = {ratio:.2f}%)")

    if found == 0:
        print("⚠️ Keine MEXC-Paare gemappt – bitte Symbol-Format prüfen oder Normalisierung erweitern.")

    return df

def ensure_seed_alias_exists():
    """Sorgt dafür, dass im aktuellen Snapshot-Verzeichnis eine seed_alias.csv liegt."""
    alias_path = _make_cache_path("seed_alias.csv")
    if not os.path.exists(alias_path):
        pd.DataFrame(columns=["alias", "coin_id"]).to_csv(alias_path, index=False)
        print(f"⚠️ seed_alias.csv neu erstellt → {alias_path}")

```

## src/colabtool/pre_universe.py

SHA256: `58e4bcf7a180cb07af85de8d97b083c9a126f8619a0722195305cb475ef4e6e6`

```python
# modules/pre_universe.py
from __future__ import annotations

import re
from typing import Tuple
from .utilities import pd, np, logging
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
    """Erkennt ETF/Leveraged Tokens anhand Symbol oder Name."""
    s = str(symbol or "").upper()
    n = str(name or "").upper()
    if any(s.endswith(suf) for suf in _LEVERAGE_SUFFIXES):
        return True
    if " LEVERAGED" in n or " ETF" in n:
        return True
    return False


def apply_pre_universe_filters(df_in: pd.DataFrame, min_volume_usd: float = 300_000.0) -> pd.DataFrame:
    """P1-Hard-Filter vor MEXC/Kategorien:
    - market_cap > 0
    - total_volume >= min_volume_usd
    - Stable/Pegged/Wrapped per Heuristik
    - BTC/ETH und gängige Derivate/Wraps
    - Hebel/ETF-Tokens
    """
    logging.info("[pre] ==== STARTE apply_pre_universe_filters ====")
    logging.info(f"[pre] Eingangsgröße: {len(df_in)} Zeilen, Columns: {list(df_in.columns)}")

    d = df_in.copy()

    # Basis
    d["market_cap"] = pd.to_numeric(d.get("market_cap"), errors="coerce")
    d["total_volume"] = pd.to_numeric(d.get("total_volume"), errors="coerce")

    logging.info(
        f"[pre] Vor Rangefilter: gültige MarketCap={d['market_cap'].notna().sum()}, "
        f"gültige Volume={d['total_volume'].notna().sum()}"
    )

    # Market Cap Range: 100 Mio < MC < 3 Mrd
    d = d[
        (d["market_cap"] > 100_000_000)
        & (d["market_cap"] < 3_000_000_000)
        & (d["total_volume"] >= float(min_volume_usd))
    ].copy()
    logging.info(f"[pre] Nach Rangefilter (MC + Volumen): {len(d)} Zeilen übrig")

    if d.empty:
        logging.warning("[pre] ⚠️ Keine Zeilen nach Rangefilter — prüfe MarketCap/Volumen-Spalten!")
        return d

    # Heuristiken
    logging.info("[pre] Berechne heuristische Masken (Stable, Wrapped, PEG, Leverage, Core) ...")
    m_stable = d.apply(lambda r: is_stable_like(r.get("name",""), r.get("symbol",""), r.get("id","")), axis=1)
    m_wrapped = d.apply(lambda r: is_wrapped_like(r.get("name",""), r.get("symbol",""), r.get("id","")), axis=1)
    m_peg_lowvar = peg_like_mask(d)  # vorsichtig
    m_lever = d.apply(lambda r: _is_leveraged(r.get("name",""), r.get("symbol","")), axis=1)
    ids = d["id"].astype(str).str.lower()
    m_core = ids.isin(_CORE_EXCLUDE_IDS)

    logging.info(
        f"[pre] Maskenzusammenfassung → "
        f"Stable={m_stable.sum()}, Wrapped={m_wrapped.sum()}, PEG={m_peg_lowvar.sum()}, "
        f"Leveraged={m_lever.sum()}, Core={m_core.sum()}"
    )

    # Debug: Beispiele zeigen
    for mask_name, mask_series in {
        "Stable": m_stable,
        "Wrapped": m_wrapped,
        "PEG": m_peg_lowvar,
        "Leveraged": m_lever,
        "Core": m_core,
    }.items():
        examples = d.loc[mask_series, ["id", "symbol", "name"]].head(3).to_dict("records")
        if examples:
            logging.info(f"[pre] Beispiele {mask_name}: {examples}")

    # ⚠️ Temporär PEG/Leverage-Filter deaktiviert (Debug)
    logging.warning("[pre] PEG- und Leveraged-Filter vorübergehend deaktiviert (Debug-Modus aktiv)")
    m_any = m_stable | m_wrapped | m_core
    kept = d.loc[~m_any].copy()

    logging.info(f"[pre] Hard-Filter: {len(d)} -> {len(kept)} (nach Ausschlussmasken)")
    if kept.empty:
        logging.warning("[pre] ⚠️ Nach allen Filtern keine Zeilen mehr – prüfe Heuristik und Rangegrenzen!")

    logging.info("[pre] ==== ENDE apply_pre_universe_filters ====")
    return kept


def attach_categories(df_in: pd.DataFrame, sleep_s: float = 0.0) -> pd.DataFrame:
    """Füllt/erstellt die Spalte 'Kategorie' über CoinGecko /coins/{id}."""
    d = df_in.copy()
    ids = d["id"].astype(str).tolist()
    cat_map = enrich_categories(ids, sleep_s=sleep_s)
    d["Kategorie"] = d["id"].astype(str).map(cat_map).fillna("Unknown")
    logging.info(f"[pre] attach_categories abgeschlossen – {len(d)} Zeilen mit Kategorie")
    return d

```

## src/colabtool/scores.py

SHA256: `72ca41fc92f33ce80a27704a9218ec3bb25b0e49edc215ef13c495fe66eee98f`

```python

# modules/scores.py
from __future__ import annotations

from typing import Optional
from .utilities import pd, np, logging

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

# ================================================================
# 🧠 SCORE_BLOCK – Global & Segment Scoring mit Regime und Dämpfung
# ================================================================
def score_block(df_in: pd.DataFrame, regime_info: dict | None = None) -> pd.DataFrame:
    """
    Berechnet den globalen und segmentbasierten Score für alle Assets.
    Nutzt Z-Norm-Werte aus Momentum, Volumen, Drawdown und Breakout.
    Regime-Logik & Beta-Dämpfung integriert.
    """
    df = df_in.copy()

    # ------------------------------------------------------------
    # Sicherstellen, dass benötigte Felder existieren
    # ------------------------------------------------------------
    required_cols = [
        "mom_7d_pct", "mom_30d_pct", "volume_mc_ratio",
        "ath_drawdown_pct", "beta_btc", "beta_eth"
    ]
    for col in required_cols:
        if col not in df.columns:
            df[col] = np.nan

    # ------------------------------------------------------------
    # Z-Normalisierung mit Winsorizing
    # ------------------------------------------------------------
    def _z(series: pd.Series) -> pd.Series:
        if series.std(ddof=0) == 0 or series.isna().all():
            return pd.Series(0, index=series.index)
        z = (series - series.mean()) / (series.std(ddof=0) + 1e-9)
        return np.clip(z, -2.5, 2.5)

    df["z_mom7"] = _z(df["mom_7d_pct"])
    df["z_mom30"] = _z(df["mom_30d_pct"])
    df["z_vmc"] = _z(df["volume_mc_ratio"])
    df["z_dd"] = -_z(df["ath_drawdown_pct"].abs())  # stärkerer Drawdown = negativer Score

    # ------------------------------------------------------------
    # Regime- & Beta-Dämpfung
    # ------------------------------------------------------------
    # Berechne Beta-Penalty als Mittelwert ggü. BTC & ETH
    df["beta_pen"] = 1.0 - np.minimum(1.0, 0.5 * (df["beta_btc"].fillna(1) + df["beta_eth"].fillna(1)) / 2)
    df["beta_pen"] = np.clip(df["beta_pen"], 0.5, 1.0)

    # ------------------------------------------------------------
    # Globaler Score (Momentum + Volumen + Drawdown)
    # ------------------------------------------------------------
    score_global = (
        0.40 * df["z_mom30"] +
        0.25 * df["z_mom7"] +
        0.25 * df["z_vmc"] +
        0.10 * df["z_dd"]
    )

    # Dämpfung bei überhitzten Coins (≥ +250% in 30d)
    overheat_mask = df["mom_30d_pct"].fillna(0) >= 250
    score_global = score_global * np.where(overheat_mask, 0.5, 1.0)

    # Beta-Dämpfung anwenden
    score_global = score_global * df["beta_pen"]

    # ------------------------------------------------------------
    # Ergebnis speichern
    # ------------------------------------------------------------
    df["score_global"] = score_global.fillna(0)
    df["score_segment"] = df["score_global"]  # segmentabhängig erweiterbar

    return df


# ================================================================
# 🚀 COMPUTE_EARLY_SCORE – Früherkennungsscore gemäß Zielbild
# ================================================================
def compute_early_score(df_in: pd.DataFrame) -> pd.DataFrame:
    """
    Berechnet den Early-Signal-Score zur Früherkennung starker Momentumbewegungen.
    Features: z_slope, z_volacc, z_break, z_buzz_level/acc (kombiniert)
    """
    df = df_in.copy()

    # ------------------------------------------------------------
    # Sicherstellen, dass benötigte Felder existieren
    # ------------------------------------------------------------
    required_cols = ["z_slope", "z_volacc", "z_break", "z_buzz_level", "z_buzz_acc", "mom_30d_pct"]
    for col in required_cols:
        if col not in df.columns:
            df[col] = 0

    # Kombinierter Buzz (max zwischen Level und Acceleration)
    df["z_buzz_combined"] = df[["z_buzz_level", "z_buzz_acc"]].max(axis=1)

    # Dämpfung bei überhitzten Coins (≥ +250% in 30d)
    damp_factor = np.where(df["mom_30d_pct"].fillna(0) >= 250, 0.5, 1.0)

    # Early Score gemäß Zielbild
    early = (
        0.30 * np.clip(df["z_slope"], -2.5, 2.5) +
        0.30 * df["z_volacc"] +
        0.30 * df["z_break"] +
        0.10 * df["z_buzz_combined"]
    ) * damp_factor

    df["early_score"] = np.clip(early, -3, 3).fillna(0)

    return df
    
# Wrapper ergänzen
def compute_scores(df):
    """
    Legacy wrapper for backward compatibility.
    Delegates to score_block() + compute_early_score().
    """
    try:
        df = score_block(df)
        df = compute_early_score(df)
        return df
    except Exception as e:
        import logging
        logging.exception(f"compute_scores failed: {e}")
        raise


```

## src/colabtool/run_snapshot_mode_patch.py

SHA256: `1db01a358bdcf6ca9ccdca96074fe66d9c388177c62ce09e3969b3721a355eef`

```python
"""
Patch-Modul: Integration der Scoring-Funktionen in die Snapshot-Pipeline.
Erstellt zur sicheren Aktivierung von score_block() und compute_early_score().
"""

import logging
from src.colabtool.scores import score_block, compute_early_score
from src.colabtool.export import export_to_excel

def run_with_scoring(df, meta, breakout_mode=True):
    """
    Wrapper um den bestehenden Pipeline-Prozess.
    Führt nach der Breakout-Berechnung die Scoring-Funktionen aus.
    """
    logging.info("🔍 Starte Scoring-Integration...")

    try:
        # 1️⃣ Globale Score-Berechnung
        df = score_block(df)
        logging.info("✅ score_block erfolgreich berechnet.")

        # 2️⃣ Early-Score-Berechnung
        df = compute_early_score(df)
        logging.info("✅ compute_early_score erfolgreich berechnet.")

        meta["score_valid"] = True

    except Exception as e:
        logging.warning(f"⚠️ Scoring skipped due to error: {e}")
        meta["score_valid"] = False

    # 3️⃣ Excel-Export (unverändert)
    export_to_excel(df, meta)
    logging.info("📦 Export abgeschlossen.")

    return df, meta


if __name__ == "__main__":
    # Nur zu Testzwecken direkt ausführbar
    import pandas as pd

    dummy = pd.DataFrame({
        "id": ["coin_a", "coin_b"],
        "market_cap": [2e8, 4e8],
        "price_change_percentage_7d_in_currency": [10, -5],
        "price_change_percentage_30d_in_currency": [25, 40],
        "volume_mc_ratio": [1.0, 1.8],
        "ath_change_percentage": [-70, -80],
    })

    meta = {}
    df, meta = run_with_scoring(dummy, meta)
    print(df[["id", "score_global", "score_segment", "early_score"]])

```

## src/colabtool/category_providers.py

SHA256: `e33a41675a5df8a014574e8bb45040334d5ee510cd7cdf31ad9311ce3b68fb04`

```python
# modules/category_providers.py
# Hybrid-Kategorien: CoinGecko → CoinMarketCap → Messari → CoinPaprika
# Ziel: Stable/Wrapped/Bridged zuverlässig erkennen, 429 minimieren (TTL + Delta).

from __future__ import annotations
import os, json, time, re
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

import requests
from .utilities import pd, np, logging

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

# === CoinGecko-Kategorien laden ===
def get_cg_categories() -> list[dict]:
    """
    Lädt CoinGecko-Kategorien live über die öffentliche API.
    Gibt eine Liste von Dikt-Einträgen mit id und name zurück.
    """
    try:
        import requests
        url = "https://api.coingecko.com/api/v3/coins/categories"
        response = requests.get(url, timeout=30)
        if response.status_code != 200:
            print(f"[warn] CoinGecko categories request failed: {response.status_code}")
            return []
        
        data = response.json()
        categories = []
        for entry in data:
            if "id" in entry and "name" in entry:
                categories.append({"id": entry["id"], "name": entry["name"]})

        print(f"✅ get_cg_categories: {len(categories)} Kategorien live von CoinGecko geladen.")
        return categories

    except Exception as e:
        print(f"[warn] get_cg_categories fehlgeschlagen: {e}")
        return []


```

## src/colabtool/cg_cache_patch.py

SHA256: `a360ec9469a326446420771042abba5adde9414936c3ff831af5c620085edf26`

```python
# modules/cg_cache_patch.py
from __future__ import annotations
import os, json, time, hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional, Callable
from .utilities import logging

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

SHA256: `1c50c5e17048e190c4573ec038f941ed9c8125361c59b73e7521599c02a466ed`

```python
# modules/export_helpers.py
from __future__ import annotations
from typing import List
from .utilities import pd

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

## src/colabtool/pit_snapshot.py

SHA256: `d3f76d350b62dd29dd569f9ad1286b145a7a5c23919cb769dca84477b2c2f6c2`

```python
import os
import datetime
import pandas as pd
from pathlib import Path

from colabtool.export import write_sheet, write_meta_sheet

# from colabtool.data_sources import (
#     get_cg_categories,
#     fetch_mexc_pairs,
#     get_alias_seed
# )

def save_snapshot(df: pd.DataFrame, name: str, snapshot_dir: Path) -> None:
    """Speichert ein DataFrame als CSV-Datei im Snapshot-Verzeichnis."""
    path = snapshot_dir / f"{name}.csv"
    df.to_csv(path, index=False)
    print(f"💾 Saved {name} snapshot: {path}")

def export_excel_snapshot(snapshot_dir: Path) -> None:
    """
    Erzeugt eine Excel-Datei (YYYYMMDD_snapshot.xlsx) im Snapshot-Verzeichnis
    und integriert alle vorhandenen CSV-Dateien als einzelne Sheets.
    """
    excel_path = snapshot_dir / f"{snapshot_dir.name}_snapshot.xlsx"
    csv_files = list(snapshot_dir.glob("*.csv"))

    if not csv_files:
        print("⚠️ Keine CSV-Dateien gefunden – Excel-Snapshot wird übersprungen.")
        return

    with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
        for csv_file in csv_files:
            try:
                sheet_name = csv_file.stem[:31]  # Excel-Limit
                df = pd.read_csv(csv_file)
                write_sheet(df, sheet_name, writer)
                print(f"📄 Added sheet: {sheet_name} ({len(df)} rows)")
            except Exception as e:
                print(f"[warn] Fehler beim Hinzufügen von {csv_file.name}: {e}")

        # Meta-Informationen
        meta_info = {
            "Snapshot_Date": snapshot_dir.name,
            "File_Count": len(csv_files),
            "Generated_UTC": datetime.datetime.utcnow().isoformat(timespec='seconds')
        }
        write_meta_sheet(writer, meta_info)

    print(f"✅ Excel-Snapshot erstellt: {excel_path}")

def run() -> None:
    """Erzeugt Tages-Snapshots und exportiert sie als Excel-Datei."""
    today = datetime.datetime.utcnow().date().strftime("%Y%m%d")
    snapshot_dir = Path("snapshots") / today
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    # --- CoinGecko Categories ---
    if os.getenv("ENABLE_PIT_CATEGORIES", "1") == "1":
        try:
            from colabtool.category_providers import get_cg_categories
            cg_categories = get_cg_categories()
            save_snapshot(pd.DataFrame(cg_categories), "cg_categories", snapshot_dir)
        except Exception as e:
            print(f"[warn] cg_categories failed: {e}")

    # --- MEXC Pairs ---
    if os.getenv("ENABLE_PIT_MEXC", "1") == "1":
        try:
            from colabtool.exchanges import fetch_mexc_pairs
            mexc_df = fetch_mexc_pairs(force=True)
            save_snapshot(mexc_df, "mexc_pairs", snapshot_dir)
        except Exception as e:
            print(f"[warn] mexc_pairs failed: {e}")

    # --- Alias Seed ---
    if os.getenv("ENABLE_PIT_ALIAS", "1") == "1":
        try:
            from colabtool.data_sources import get_alias_seed
            alias_df = get_alias_seed()
            if alias_df is not None:
                save_snapshot(alias_df, "seed_alias", snapshot_dir)
        except Exception as e:
            print(f"[warn] alias_seed failed: {e}")

    # --- Excel Export ---
    try:
        export_excel_snapshot(snapshot_dir)
    except Exception as e:
        print(f"[warn] Excel-Export fehlgeschlagen: {e}")

    print("📦 Snapshot completed successfully.")

if __name__ == "__main__":
    run()

```

## src/colabtool/backtest.py

SHA256: `4752fe56aeed1f62f7365d9720f85a14205f38826e8e4f1ae8a775801e1f98a0`

```python
# modules/backtest.py
from __future__ import annotations
from typing import List
from .utilities import pd, np, logging
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
        p_prev = float(prices[-(horizon + 1)][1])
        if p_prev == 0:
            return np.nan
        return (p_now / p_prev - 1.0) * 100.0
    except Exception:
        return np.nan


def backtest_on_snapshot(
    df: pd.DataFrame,
    top_k: int = 20,
    horizons: List[int] = [20, 40, 60],
    vs: str = "usd"
) -> pd.DataFrame:
    """
    Simpler Snapshot-Backtest:
    - Auswahl: Top-k nach 'early_score' (Fallback: 'score_segment', dann 'score_global').
    - Für jede ID: lädt 1× market_chart(days = max(horizons)+2) und berechnet rückblickende
      %-Veränderungen über die angegebenen Horizonte (Approximation, da echte Zukunftsreturns
      erst später messbar sind).
    - Output: Tabelle mit Returns je Horizon + Basisinfos.
    Hinweis: Minimiert API-Calls (≤ top_k).
    """
    df = df.copy()
    rank_cols = [c for c in ["early_score", "score_segment", "score_global"] if c in df.columns]
    if not rank_cols:
        logging.warning("[backtest] keine Ranking-Spalten gefunden")
        return pd.DataFrame()

    rank_col = rank_cols[0]
    picks = df.dropna(subset=[rank_col]).sort_values(rank_col, ascending=False).head(top_k).copy()
    if picks.empty:
        logging.warning("[backtest] keine Kandidaten für Backtest gefunden")
        return pd.DataFrame()

    max_h = max(horizons) if len(horizons) else 60
    rows = []

    for _, r in picks.iterrows():
        cid = str(r["id"])
        try:
            data = cg_market_chart(cid, vs=vs, days=max(200, max_h + 10)) or {}
            prices = data.get("prices", [])
        except Exception as ex:
            logging.warning(f"[backtest] {cid} market_chart Fehler: {ex}")
            prices = []

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

        for h in horizons:
            out[f"ret_{h}d_pct"] = _forward_return_from_chart(prices, h)
        rows.append(out)

    bt = pd.DataFrame(rows)

    # Aggregat-Zeile
    if not bt.empty:
        agg = {
            "id": "AGG_MEAN",
            "symbol": "-",
            "name": "-",
            "Segment": "-",
            "rank_col": rank_col,
            "rank_val": bt["rank_val"].mean(),
            "early_score": bt["early_score"].mean(),
            "score_segment": bt["score_segment"].mean(),
            "score_global": bt["score_global"].mean(),
            "mexc_pair": "-"
        }
        for h in horizons:
            col = f"ret_{h}d_pct"
            if col in bt.columns:
                agg[col] = bt[col].mean()
        bt = pd.concat([bt, pd.DataFrame([agg])], ignore_index=True)

    logging.info(f"[backtest] abgeschlossen: {len(bt)} Zeilen, Horizonte={horizons}")
    return bt

```

## src/colabtool/__init__.py

SHA256: `01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b`

```python


```

## src/colabtool/utils/validation.py

SHA256: `059cb0f0047798828503fbaa2981adff031d2f6349f1cbaa5a5053ae5b99e9fa`

```python
"""
validation.py — Preflight-Schema-Check für Snapshot-Daten

Stellt sicher, dass DataFrames die erwartete Struktur haben.
Fehlende Spalten werden automatisch ergänzt, Typen geprüft.
"""

import pandas as pd
import logging
from typing import Dict, Type


def ensure_schema(df: pd.DataFrame, schema_map: Dict[str, Type]) -> pd.DataFrame:
    """
    Ensures that the given DataFrame matches the expected schema.
    - Adds missing columns with default values
    - Coerces datatypes if possible
    - Logs any inconsistencies
    """
    if df is None or not isinstance(df, pd.DataFrame):
        raise ValueError("ensure_schema: input is not a valid DataFrame")

    for col, dtype in schema_map.items():
        if col not in df.columns:
            logging.warning(f"[ensure_schema] Adding missing column: {col}")
            # assign sensible default based on dtype
            if dtype in (float, int):
                df[col] = 0
            elif dtype is bool:
                df[col] = False
            else:
                df[col] = None

        # type coercion (non-fatal)
        try:
            df[col] = df[col].astype(dtype, errors="ignore")
        except Exception as e:
            logging.warning(f"[ensure_schema] Failed to coerce {col} to {dtype}: {e}")

    # remove unexpected columns (optional, keep for audit)
    extra_cols = [c for c in df.columns if c not in schema_map]
    if extra_cols:
        logging.info(f"[ensure_schema] Extra columns present: {extra_cols}")

    return df


def validate_required_columns(df: pd.DataFrame, required: list[str]) -> None:
    """Raises ValueError if required columns are missing."""
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")


def validate_nonempty(df: pd.DataFrame, min_rows: int = 1) -> None:
    """Ensures that the DataFrame has at least `min_rows`."""
    if df.empty or len(df) < min_rows:
        raise ValueError(f"DataFrame has insufficient rows: {len(df)} < {min_rows}")

```

## src/colabtool/utils/__init__.py

SHA256: `b5636b2d1ac4d48d53c195371b0e49a81b1d5eab175e38d5e5644e55b4e0df56`

```python
# Platzhalter

```

## notebooks/crypto_scanner_main_PIT (2).ipynb • code cells

SHA256: `da5b31f1e92f0975a2b34ef0623fbd5c3ef5dd3a1d5f0744a9b00577a6f00e80`

```python
# cell 0
# Google Drive Bibliothek installieren
!pip install -U google-api-python-client google-auth google-auth-httplib2 google-auth-oauthlib


# cell 1
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

# cell 2
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


# cell 3
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


# cell 4
import inspect
from colabtool.export import _safe_col_width
print(inspect.getsource(_safe_col_width))

# cell 5
import inspect
from colabtool import export
print(inspect.getsource(export))


# cell 6
import inspect
from colabtool.features import compute_feature_block

print(inspect.getsource(compute_feature_block))


# cell 7
# Upload-Code um Dateien hochzuladen (bei Bedarf auskommentieren)

# from google.colab import files
# files.upload()


# cell 8
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

# ASOF_Date definieren
from datetime import datetime
ASOF_DATE = datetime.today().strftime("%Y%m%d")

# Lokaler Cache statt Google Drive
os.environ["CACHE_DIR"] = "/content/cache/http_cache"

# Pfade und Verzeichnisse
import os
#from google.colab import drive
#
#MOUNTPOINT = "/content/drive"
#
# Wenn bereits gemountet: nicht erneut mounten
#if not os.path.ismount(MOUNTPOINT):
    # Wenn dort Dateien liegen → manuelles Cleanup erforderlich
    #if os.path.exists(MOUNTPOINT) and os.listdir(MOUNTPOINT):
        #raise RuntimeError(f"❌ Fehler: {MOUNTPOINT} enthält bereits Dateien. Bitte Notebook neu starten.")

    #drive.mount(MOUNTPOINT, force_remount=True)

# Temporäre Pfade und Verzeichnisse

EXPORT_DIR = "/content/snapshots/exports"
CACHE_DIR  = "/content/snapshots/cache"

os.makedirs(EXPORT_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

assert os.path.exists(EXPORT_DIR), f"❌ Export-Verzeichnis nicht gefunden: {EXPORT_DIR}"
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
_STAMP = (_dt.now(_TZ) if _TZ else _dt.now()).strftime("%Y-%m-%d - %H-%M")
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
    df.attrs["asof_date"] = ASOF_DATE
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

# ------------------
# [20] Neuer Export in kryptotreiber Google Drive
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_drive(service_account_file: str, folder_id: str, local_file_path: str):
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file,
        scopes=["https://www.googleapis.com/auth/drive"]
    )
    service = build("drive", "v3", credentials=credentials)

    file_metadata = {
        "name": os.path.basename(local_file_path),
        "parents": [folder_id]
    }
    media = MediaFileUpload(local_file_path, resumable=True)
    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    print(f"✅ Datei hochgeladen – File ID: {uploaded_file.get('id')}")

# Aufruf aus Notebook
# Beispielpfade anpassen:
SERVICE_ACCOUNT_FILE = "/content/crypto-drive-export-96ab6bcd019b.json"  # Pfad zur JSON-Datei
FOLDER_ID = "1Kl29WBUsWBLPMcDyBZ9WBRAvSNzpjSkd"  # Deine Drive-Ordner-ID
EXPORT_FILE = EXPORT_PATH  # Verweist auf die tatsächlich erzeugte Datei

upload_to_drive(SERVICE_ACCOUNT_FILE, FOLDER_ID, EXPORT_FILE)

# Ende neuer Export
# ------------------

print("Export:", EXPORT_PATH)
import os
print("EXISTIERT:", os.path.exists(EXPORT_PATH))
print("EXPORT_PATH:", EXPORT_PATH)

try:
    display(top25_early.head(10)); display(full_data.head(10))
except Exception:
    pass


# cell 9
!ls -l /content/snapshots/exports


# cell 10

```

## notebooks/archive/crypto_scanner_main_PIT(def).ipynb • code cells

SHA256: `b3a23031162ed10502b8791cea18a361e5e6be34cb6b69e5f5dc1c8d1d6b5c67`

_nb read error: Notebook does not appear to be JSON: '{\n "cells": [\n  {\n   "cell_type": "c..._

## notebooks/archive/crypto_scanner_main_PIT_2.ipynb • code cells

SHA256: `b3a23031162ed10502b8791cea18a361e5e6be34cb6b69e5f5dc1c8d1d6b5c67`

_nb read error: Notebook does not appear to be JSON: '{\n "cells": [\n  {\n   "cell_type": "c..._

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

## notebooks/archive/crypto_scanner_main_v14.5.1.ipynb • code cells

SHA256: `e59ba2e53222651576f4825cd90d0d7c4b83de4a9d46f63a21dad260bf2cf694`

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
import os
from google.colab import drive

MOUNTPOINT = "/content/drive"

# Wenn bereits gemountet: nicht erneut mounten
if not os.path.ismount(MOUNTPOINT):
    # Wenn dort Dateien liegen → manuelles Cleanup erforderlich
    if os.path.exists(MOUNTPOINT) and os.listdir(MOUNTPOINT):
        raise RuntimeError(f"❌ Fehler: {MOUNTPOINT} enthält bereits Dateien. Bitte Notebook neu starten.")

    drive.mount(MOUNTPOINT, force_remount=True)

EXPORT_DIR = f"{MOUNTPOINT}/MyDrive/Colab results"
CACHE_DIR  = f"{MOUNTPOINT}/MyDrive/crypto_tool/cache"

assert os.path.exists(EXPORT_DIR), f"❌ Export-Verzeichnis nicht gefunden: {EXPORT_DIR}"
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
_STAMP = (_dt.now(_TZ) if _TZ else _dt.now()).strftime("%Y-%m-%d - %H-%M")
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

```

## notebooks/archive/crypto_scanner_main_local.ipynb • code cells

SHA256: `c168993a01d5484994b3abc9bb594b95781a498fe260b016efa30f073e16c95f`

```python
# cell 0

import os
from datetime import datetime

ASOF_DATE = os.environ.get("ASOF_DATE", datetime.today().strftime("%Y%m%d"))
EXPORT_PATH_LOCAL = f"output/Scanner_export_{ASOF_DATE}.xlsx"
os.makedirs("output", exist_ok=True)


# cell 1
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

# cell 2
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


# cell 3
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


# cell 4
import inspect
from colabtool.export import _safe_col_width
print(inspect.getsource(_safe_col_width))

# cell 5
import inspect
from colabtool import export
print(inspect.getsource(export))


# cell 6
import inspect
from colabtool.features import compute_feature_block

print(inspect.getsource(compute_feature_block))

```

## notebooks/archive/crypto_scanner_main_v14.4.ipynb • code cells

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


## 🧩 Modul- & Funktionsübersicht (ChatGPT Context Map)
| Modul | Funktionen | Klassen |
|-------|-------------|----------|
| `src/colabtool/data_sources_cmc.py` | _log, _on_get, fetch_cmc_markets, _fetch_mexc_pairs, map_mexc_pairs, map_tvl, load_or_fetch_markets, write_cache | - |
| `src/colabtool/run_snapshot_mode.py` | validate_scores, run_snapshot | - |
| `src/colabtool/export.py` | _safe_col_width, reorder_columns, write_sheet, write_meta_sheet, create_full_excel_export, export_snapshot | - |
| `src/colabtool/features.py` | _ensure_series, _num_series, _lc, is_stable_like, is_wrapped_like, peg_like_mask, exclusion_mask, fetch_mexc_klines, compute_mexc_features, compute_feature_block, tag_segment | - |
| `src/colabtool/breakout.py` | _mexc_klines, _valid_pair, _to_df, _pct_change, _rolling_max, _percentile_rank, _zscore, _beta, _features_from_klines, _prep_betas, compute_breakout_for_ids | - |
| `src/colabtool/exchanges.py` | _is_colab, _resolve_seed_dir, _is_leveraged_symbol, _http_json, _listing_from_exchange_info, _listing_from_ticker24, _load_mexc_listing, _load_seed_overrides, _apply_overrides, _choose_preferred_pair, _collect_collisions_in_listing, apply_mexc_filter, export_mexc_seed_template, fetch_mexc_pairs | - |
| `src/colabtool/utilities.py` | _is_colab, _resolve_cache_dir, safe_div, winsor_minmax, _cache_key, http_get_json | - |
| `src/colabtool/buzz.py` | _is_colab, _resolve_seed_dir, _env_str, _env_float, _env_json_dict, _parse_entry, fetch_rss_all, _load_alias_seed, _compile_alias_regex, _age_weight, _pub_weight, _match_article, _collect_scores_for_ids, add_buzz_metrics_for_candidates | - |
| `src/colabtool/data_sources.py` | _env_str, _env_bool, _env_int, _env_float, _is_colab, _cg_throttle, _resolve_seed_dir, _sleep_min_interval, _one_get, _sanitize_params_for_free, _cg_get, _get_snapshot_dir, _make_cache_path, _chart_cache_path, cg_markets, enrich_categories, map_tvl, update_seen_ids, cg_market_chart, persist_pit_snapshot, get_alias_seed, map_mexc_pairs, ensure_seed_alias_exists | - |
| `src/colabtool/pre_universe.py` | _is_leveraged, apply_pre_universe_filters, attach_categories | - |
| `src/colabtool/scores.py` | _ensure_series, _winsorize, _mc_bucket, _z_by_bucket, _safe_num, _align_bool_mask, score_block, compute_early_score, compute_scores | - |
| `src/colabtool/run_snapshot_mode_patch.py` | run_with_scoring | - |
| `src/colabtool/category_providers.py` | _now_utc, _load_cache, _save_cache, _cache_get, _cache_set, _infer_from_tags, _norm, _cmc_get_map_by_symbols, _messari_get_profile, _paprika_find_id, _paprika_get_coin, enrich_categories_hybrid, get_cg_categories | - |
| `src/colabtool/cg_cache_patch.py` | setup_cg_chart_cache | - |
| `src/colabtool/export_helpers.py` | _cols, make_fulldata | - |
| `src/colabtool/pit_snapshot.py` | save_snapshot, export_excel_snapshot, run | - |
| `src/colabtool/backtest.py` | _forward_return_from_chart, backtest_on_snapshot | - |
| `src/colabtool/__init__.py` | - | - |
| `src/colabtool/utils/validation.py` | ensure_schema, validate_required_columns, validate_nonempty | - |
| `src/colabtool/utils/__init__.py` | - | - |
