#!/usr/bin/env python3
"""
Debug-Skript: CMC vs. MEXC Mapping-Analyse
------------------------------------------
Vergleicht die von CoinMarketCap geladenen Märkte mit
den auf MEXC handelbaren USDT-Paaren und erstellt zwei Reports:
- mapping_matches.csv  (Treffer)
- mapping_nomatch.csv  (keine Entsprechung auf MEXC)
"""

import os
import sys
import pandas as pd
import logging
from datetime import datetime

# ----------------------------------------------------------------------
# 🔧 Automatische Pfadkorrektur für src-basiertes Layout
# ----------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# ----------------------------------------------------------------------
# 📦 Modulimporte aus colabtool
# ----------------------------------------------------------------------
from colabtool.data_sources_cmc import fetch_cmc_markets, map_mexc_pairs  # ✅ korrekte Quelle

# ----------------------------------------------------------------------
# 🧠 Logging-Konfiguration
# ----------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)

# ----------------------------------------------------------------------
# 🧩 Hilfsfunktionen
# ----------------------------------------------------------------------
def ensure_dir(path: str):
    """Erstellt Ordner, falls er noch nicht existiert."""
    os.makedirs(path, exist_ok=True)


def save_csv(df: pd.DataFrame, name: str):
    """Speichert DataFrame in snapshots/YYYYMMDD/."""
    today = datetime.now().strftime("%Y%m%d")
    out_dir = os.path.join("snapshots", today)
    ensure_dir(out_dir)
    path = os.path.join(out_dir, name)
    df.to_csv(path, index=False)
    logging.info(f"💾 Datei gespeichert: {path} ({len(df)} Zeilen)")


# ----------------------------------------------------------------------
# 🚀 Hauptfunktion
# ----------------------------------------------------------------------
def main():
    logging.info("🚀 Starte Debug-Analyse: CMC ↔ MEXC Mapping")

    # 1️⃣ CMC-Daten abrufen
    df_cmc = fetch_cmc_markets(pages=4, limit=250)
    logging.info(f"[CMC] ✅ Empfangen: {len(df_cmc)} Einträge")

    # 2️⃣ MEXC-Mapping durchführen
    df_map = map_mexc_pairs(df_cmc)

    # 3️⃣ Aufteilen in Treffer / Nicht-Treffer
    df_match = df_map[df_map["mexc_pair"].notna()].copy()
    df_nomatch = df_map[df_map["mexc_pair"].isna()].copy()

    logging.info(f"✅ Treffer: {len(df_match)} / {len(df_map)}")
    logging.info(f"⚠️ Keine Entsprechung auf MEXC: {len(df_nomatch)}")

    if len(df_nomatch) > 0:
        logging.info("🔍 Beispiel fehlender Einträge:")
        logging.info(df_nomatch[["symbol", "slug", "name"]].head(10).to_string(index=False))

    # 4️⃣ Ergebnisse speichern
    save_csv(df_match, "mapping_matches.csv")
    save_csv(df_nomatch, "mapping_nomatch.csv")

    logging.info("🏁 Mapping-Analyse abgeschlossen.")


# ----------------------------------------------------------------------
# 🏃 Script-Entry
# ----------------------------------------------------------------------
if __name__ == "__main__":
    main()
