
<!-- ChatGPT Context Overview -->

# 🧠 Early Signal Altcoin Scanner ("colabtool")

Ein automatisiertes Research-Tool zur **Identifikation früher Momentum-Signale bei Altcoins**  
(Horizont: Wochen–Monate).  
Fokus: Mid-Caps, Volumenbeschleunigung, Breakout-Nähe und Buzz-Aktivität.

---

## 1️⃣ Ziel und Zweck

Das Tool analysiert Altcoin-Marktdaten (CoinGecko, MEXC, DeFiLlama, CryptoPanic)  
und erkennt potenzielle „Hidden Gems“ oder Comebacks anhand von  
Momentum, Volumenbeschleunigung, Breakout-Distanz und Buzz-Dynamik.

---

## 2️⃣ Architekturüberblick

```text
CoinGecko Markets → Filter & Exclusions → MEXC Mapping
      ↓
Feature Engine (Momentum, VolAcc, Breakout, Buzz)
      ↓
Scoring & Segmentierung → Backtest → Snapshot Export
```

👉 **Aktueller Code- und Modulstatus:**  
Siehe [📄 docs/GPT_SNAPSHOT.md](docs/GPT_SNAPSHOT.md)  
> Diese Datei wird **automatisch nach jedem Commit** aktualisiert  
> und enthält die aktuelle Modul- und Funktionsübersicht („ChatGPT Context Map“).

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
| `SKIP_CATEGORIES` | Überspringt CoinGecko-Kategorisierung |
| `CRYPTOPANIC_API_KEY` | Optional für Buzz-Daten |
| `CG_MIN_INTERVAL_S` | Rate-Limit für CoinGecko-API |

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

## 9️⃣ Lizenz & Haftung

Dieses Tool dient ausschließlich **Research-Zwecken**.  
Es stellt **keine Finanzberatung** dar. Nutzung auf eigenes Risiko.

---

## 🔁 Quick-Reference (für ChatGPT)

**Primäre Einstiegspunkte:**
- `main.py` → Pipeline-Controller  
- `src/pipeline/features.py` → Feature-Berechnung  
- `src/pipeline/scoring.py` → Scoring / Segmentierung  
- `src/export/excel_writer.py` → Excel-Export  

**Wenn eine Funktion unklar ist:**  
→ Zuerst in `src/pipeline/` suchen  
→ Dann `getContent()` nutzen, um Quelltext zu prüfen.
