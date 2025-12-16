"""
Kurzer Funktionstest für fetch_mexc_klines() + compute_mexc_features()
Ziel: Prüfen, ob MEXC-Klinedaten abrufbar sind und Momentum korrekt berechnet wird.
"""

import sys
import logging
from pathlib import Path
import pandas as pd

# Autodetektion der src/colabtool-Struktur
ROOT = Path(__file__).resolve().parents[1]
if (ROOT / "src" / "colabtool").exists():
    sys.path.insert(0, str(ROOT / "src"))
else:
    sys.path.insert(0, str(ROOT))
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# --- Imports aus deiner Pipeline ---
from colabtool.data_sources_cmc import fetch_mexc_klines
from colabtool.features import compute_mexc_features


# --- Test-Setup ---
TEST_SYMBOLS = ["INJUSDT", "ARUSDT", "MANTAUSDT"]

logging.info("🚀 Starte MEXC-Kline-Test für ausgewählte Symbole.")
results = []

for sym in TEST_SYMBOLS:
    try:
        kl = fetch_mexc_klines(sym)
        if kl is None or len(kl) < 5:
            logging.warning(f"[MEXC] ⚠️ Keine oder zu wenige Daten für {sym}.")
            results.append({"symbol": sym, "rows": 0, "mom_30d_pct": None, "vol_acc": None, "ath_dd": None})
            continue

        features = compute_mexc_features(kl)
        res = {
            "symbol": sym,
            "rows": len(kl),
            "mom_7d_pct": features.get("mom_7d_pct"),
            "mom_30d_pct": features.get("mom_30d_pct"),
            "vol_acc": features.get("vol_acc"),
            "ath_drawdown_pct": features.get("ath_drawdown_pct"),
        }
        results.append(res)
        logging.info(
            f"[MEXC] ✅ {sym}: {len(kl)} Candles | mom_30d={res['mom_30d_pct']:.2f}% | "
            f"vol_acc={res['vol_acc']:.2f} | drawdown={res['ath_drawdown_pct']:.2f}%"
        )
    except Exception as e:
        logging.error(f"[MEXC] ❌ Fehler bei {sym}: {e}")

# --- Zusammenfassung ---
df = pd.DataFrame(results)
summary_path = Path("snapshots") / "mexc_klines_test_results.csv"
summary_path.parent.mkdir(exist_ok=True, parents=True)
df.to_csv(summary_path, index=False)

logging.info(f"📊 Test abgeschlossen – Ergebnisse gespeichert unter: {summary_path}")
print(df)
