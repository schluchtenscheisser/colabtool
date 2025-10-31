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
