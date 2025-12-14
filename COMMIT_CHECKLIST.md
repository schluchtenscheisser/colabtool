
<!-- ChatGPT Commit Checklist -->

# ✅ Selbst-Checkliste vor jedem Commit

> 🧠 **Zweck:** Sicherstellen, dass README, Snapshot und GPT-Kontext immer aktuell bleiben  
> 🧩 **Gilt für:** manuelle Commits **und** GitHub-Actions

---

## 1️⃣ Inhaltliche Änderungen

| Änderungstyp | Was prüfen / anpassen |
|---------------|-----------------------|
| **Neue Funktion, Klasse oder Modul** | Läuft der GPT-Snapshot-Workflow erfolgreich und hat `docs/GPT_SNAPSHOT.md` aktualisiert? |
| **Neue ENV-Variable** | In `README.md` unter Abschnitt *„Wichtige ENV-Variablen“* ergänzen |
| **Neue Feature- oder Scoring-Logik** | Kurzbeschreibung und Formel im Abschnitt *„Features“* oder *„Scores“* der README aktualisieren |
| **Neue Segment- oder Regime-Definition** | Tabelle *Segmentierung* in README prüfen und ggf. anpassen |
| **Neue externe Datenquelle / API** | README unter *„Architekturüberblick“* ergänzen |
| **Neue Pipeline-Schritte** | `README.md` → Diagramm unter *„Architekturüberblick“* anpassen |

---

## 2️⃣ Technische Änderungen

| Änderungstyp | Aktion |
|---------------|--------|
| Änderungen an Workflows (`.github/workflows/`) | Prüfen, ob der Snapshot-Job weiter funktioniert und `docs/GPT_SNAPSHOT.md` schreibt |
| Neue Abhängigkeit (neues Package) | `requirements.txt` und ggf. `pyproject.toml` updaten |
| Anpassung an Pfadstruktur | Pfade in `README.md` unter *„Projektstruktur (statisch)“* aktualisieren |

---

## 3️⃣ Dokumentation & Meta

| Punkt | Check |
|-------|-------|
| `README.md` enthält neuen Kontext? | 🔹 Ja / 🔸 Nein |
| GPT-Hinweisblock (`⚙️ Hinweis für ChatGPT`) bleibt unverändert | 🔹 Ja |
| `docs/GPT_SNAPSHOT.md` vorhanden & aktuell | 🔹 Ja |
| Commit-Message beschreibt Änderung verständlich | 🔹 Ja |
| Falls Verhalten sich ändert: `CHANGELOG.md` → Eintrag mit `Added`, `Changed`, `Fixed` | 🔹 Ja |

---

## 4️⃣ Nach dem Commit

✅ Verifiziere, dass:
- Der GitHub-Action-Run „GPT-Snapshot“ **grün** abgeschlossen ist  
- `docs/GPT_SNAPSHOT.md` den neuen Funktions- oder Modul-Eintrag enthält  
- Keine ungewollten Änderungen im README durch CI-Tools erfolgt sind  

---

## 5️⃣ Quick-Command-Reminders

```bash
# Lokalen Test des Snapshots (optional)
python .github/scripts/gpt_snapshot.py

# Prüfen, ob README-Änderungen noch Markdown-valid sind
markdownlint README.md

# Tests mit Mocks und Excel-Ausgabe
pytest -q --disable-warnings
```

---

## 🧭 Tipp

Füge diesen Header-Kommentar ein, damit GPT diese Datei automatisch erkennt:

```markdown
<!-- ChatGPT Commit Checklist -->
```

Dann kann ChatGPT bei neuen Sessions diese Datei auslesen und prüfen,  
ob geplante Änderungen mit der Dokumentation und dem Snapshot-System übereinstimmen.
