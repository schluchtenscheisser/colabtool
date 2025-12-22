
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
Wichtig: Das Tool dient nur zu Research-Zwecken und stellt keine Anlageberatung dar!

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
