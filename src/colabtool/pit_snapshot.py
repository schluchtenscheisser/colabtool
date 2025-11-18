import os
import datetime
import pandas as pd
from pathlib import Path

# from colabtool.data_sources import (
    # get_cg_categories,
    # fetch_mexc_pairs,
    # get_alias_seed
# )

def save_snapshot(df: pd.DataFrame, name: str, snapshot_dir: Path) -> None:
    path = snapshot_dir / f"{name}.csv"
    df.to_csv(path, index=False)
    print(f"Saved {name} snapshot: {path}")

def run():
    today = datetime.datetime.utcnow().date().strftime("%Y%m%d")
    snapshot_dir = Path("snapshots") / today
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    
    # TEMP: Dummy-Snapshot erzeugen
    # dummy = pd.DataFrame({"timestamp": [today], "info": ["snapshot test"]})
    # save_snapshot(dummy, "dummy_snapshot", snapshot_dir)
    
    # CoinGecko Categories
    if os.getenv("ENABLE_PIT_CATEGORIES", "1") == "1":
        try:
            from colabtool.category_providers import get_cg_categories
            cg_categories = get_cg_categories()
            save_snapshot(pd.DataFrame(cg_categories), "cg_categories", snapshot_dir)
        except Exception as e:
            print(f"[warn] cg_categories failed: {e}")

    # MEXC Pairs
    if os.getenv("ENABLE_PIT_MEXC", "1") == "1":
        try:
            from colabtool.exchanges import fetch_mexc_pairs
            mexc_df = fetch_mexc_pairs(force=True)
            save_snapshot(mexc_df, "mexc_pairs", snapshot_dir)
        except Exception as e:
            print(f"[warn] mexc_pairs failed: {e}")

    # Alias Seed
    if os.getenv("ENABLE_PIT_ALIAS", "1") == "1":
        try:
            from colabtool.data_sources import get_alias_seed
            alias_df = get_alias_seed()
            if alias_df is not None:
                save_snapshot(alias_df, "seed_alias", snapshot_dir)
        except Exception as e:
            print(f"[warn] alias_seed failed: {e}")

    print("Snapshot completed.")

if __name__ == "__main__":
    run()
    
from pathlib import Path
import pandas as pd
from colabtool.export import write_sheet, write_meta_sheet

def export_excel_snapshot(snapshot_dir: Path):
    
    # Aggregiert CSVs aus dem Snapshot-Verzeichnis zu einer Excel-Datei.
    # Erwartet, dass FullData.csv und Meta-Daten vorhanden sind.
    
    excel_path = snapshot_dir / f"{snapshot_dir.name}_snapshot.xlsx"
    with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
        # Hauptdatenblatt (falls vorhanden)
        full_data_path = snapshot_dir / "FullData.csv"
        if full_data_path.exists():
            df = pd.read_csv(full_data_path)
            write_sheet(df, "FullData", writer)
        else:
            print("⚠️ FullData.csv nicht gefunden, überspringe diesen Tab.")

        # Meta-Daten (optional)
        meta_path = snapshot_dir / "meta.json"
        if meta_path.exists():
            meta = pd.read_json(meta_path, typ="series")
            write_meta_sheet(writer, meta.to_dict())
        else:
            print("⚠️ meta.json nicht gefunden, kein Meta-Sheet erstellt.")

    print(f"✅ Excel-Snapshot gespeichert: {excel_path}")


