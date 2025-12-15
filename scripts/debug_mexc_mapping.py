import pandas as pd
from colabtool.data_sources_cmc import fetch_cmc_markets
from colabtool.data_sources_mexc import fetch_mexc_pairs
import sys
import os

# Ermöglicht das Importieren aus src/
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

# 1️⃣ Daten abziehen
df_cmc = fetch_cmc_markets(pages=2, limit=250)  # begrenzt für Debug
df_mexc = fetch_mexc_pairs()

# 2️⃣ Relevante Spalten auswählen
cmc_cols = ["id", "symbol", "slug", "name", "quote.USD.market_cap"]
mexc_cols = ["symbol", "baseAsset", "quoteAsset"]

df_cmc = df_cmc[cmc_cols].drop_duplicates()
df_mexc = df_mexc[mexc_cols].drop_duplicates()

# 3️⃣ Normalisieren
df_cmc["symbol_norm"] = df_cmc["symbol"].str.upper().str.strip()
df_mexc["base_norm"] = df_mexc["baseAsset"].str.upper().str.strip()

# 4️⃣ Vergleich / Schnittmenge
matches = df_cmc[df_cmc["symbol_norm"].isin(df_mexc["base_norm"])]
no_match = df_cmc[~df_cmc["symbol_norm"].isin(df_mexc["base_norm"])]

print(f"✅ Treffer: {len(matches)} / {len(df_cmc)}")
print(f"⚠️ Keine Entsprechung auf MEXC: {len(no_match)}")

# 5️⃣ Ergebnisse speichern
matches.to_csv("snapshots/20251215/mapping_matches.csv", index=False)
no_match.to_csv("snapshots/20251215/mapping_nomatch.csv", index=False)

print("\nBeispiel fehlender Einträge:")
print(no_match.head(20))
