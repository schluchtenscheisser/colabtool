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

def _fetch_mexc_pairs() -> List[Dict[str, Any]]:
    """Lädt MEXC Spot-Paare"""
    try:
        resp = requests.get(MEXC_BASE_URL, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("symbols", [])
        _log(f"⚠️  Fehler beim Laden der MEXC-Paare: {resp.status_code}")
    except Exception as e:
        _log(f"⚠️  MEXC-Verbindungsfehler: {e}")
    return []


def map_mexc_pairs(df: pd.DataFrame) -> pd.DataFrame:
    """Markiert, ob Coin bei MEXC handelbar ist"""
    _log("🔍 Lade MEXC-Handelspaare ...")
    pairs = _fetch_mexc_pairs()
    mexc_symbols = {p["baseAsset"].upper() for p in pairs}
    df["mexc_pair"] = df["symbol"].apply(lambda s: s.upper() in mexc_symbols)
    _log(f"✅ MEXC Mapping abgeschlossen ({df['mexc_pair'].sum()} Treffer).")
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
