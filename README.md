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
data_sources: Marktdaten von CoinGecko, MEXC etc.
features: Feature Engineering inkl. Momentum, Volumenrelation etc.
metrics: Statistische Kennzahlen wie Volatilität, Drawdowns etc.
filters: Scoring-basierte Filterlogik.
viz: Visualisierungen.
export: Excel-Export mit Formatierung.
buzz: Verarbeitung externer Newsfeeds.
category_providers: Sektorbasierte Gruppierung.
utils: Hilfsfunktionen, Logging.

Beispiel-Notebook
Ein vollständiger Workflow ist im Notebook notebooks/Scanner_v14_5.ipynb enthalten. Es führt durch alle Schritte: Datenerhebung, Feature Engineering, Filterung, Export und Visualisierung.

Setup
Benötigte Pakete sind in requirements.txt und pyproject.toml definiert.

Hinweis
Die Nutzung in Colab erfordert eine gemountete Verbindung zu Google Drive, um z. B. Excel-Dateien zu speichern.
