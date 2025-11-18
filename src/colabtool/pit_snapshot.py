import os
import datetime
import pandas as pd
from pathlib import Path

from colabtool.export import write_sheet, write_meta_sheet

# from colabtool.data_sources import (
#     get_cg_categories,
#     fetch_mexc_pairs,
#     get_alias_seed
# )

def save_snapshot(df: pd.DataFrame, name: str, snapshot_dir: Path) -> None:
    """Speichert ein DataFrame als CSV-Datei im Snapshot-Verzeichnis."""
    path = snapshot_dir / f"{name}.csv"
    df.to_csv(path, index=False)
    print(f"💾 Saved {name} snapshot: {path}")

def export_excel_snapshot(snapshot_dir: Path) -> None:
    """
    Erzeugt eine Excel-Datei (YYYYMMDD_snapshot.xlsx) im Snapshot-Verzeichnis
    und integriert alle vorhandenen CSV-Dateien als einzelne Sheets.
    """
    excel_path = snapshot_dir / f"{snapshot_dir.name}_snapshot.xlsx"
    csv_files = list(snapshot_dir.glob("*.csv"))

    if not csv_files:
        print("⚠️ Keine CSV-Dateien gefunden – Excel-Snapshot wird übersprungen.")
        return

    with pd.ExcelWriter(excel_path, engine="xlsxwriter") as writer:
        for csv_file in csv_files:
            try:
                sheet_name = csv_file.stem[:31]  # Excel-Limit
                df = pd.read_csv(csv_file)
                write_sheet(df, sheet_name, writer)
                print(f"📄 Added sheet: {sheet_name} ({len(df)} rows)")
            except Exception as e:
                print(f"[warn] Fehler beim Hinzufügen von {csv_file.name}: {e}")

        # Meta-Informationen
        meta_info = {
            "Snapshot_Date": snapshot_dir.name,
            "File_Count": len(csv_files),
            "Generated_UTC": datetime.datetime.utcnow().isoformat(timespec='seconds')
        }
        write_meta_sheet(writer, meta_info)

    print(f"✅ Excel-Snapshot erstellt: {excel_path}")

def run() -> None:
    """Erzeugt Tages-Snapshots und exportiert sie als Excel-Datei."""
    today = datetime.datetime.utcnow().date().strftime("%Y%m%d")
    snapshot_dir = Path("snapshots") / today
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    # --- CoinGecko Categories ---
    if os.getenv("ENABLE_PIT_CATEGORIES", "1") == "1":
        try:
            from colabtool.category_providers import get_cg_categories
            cg_categories = get_cg_categories()
            save_snapshot(pd.DataFrame(cg_categories), "cg_categories", snapshot_dir)
        except Exception as e:
            print(f"[warn] cg_categories failed: {e}")

    # --- MEXC Pairs ---
    if os.getenv("ENABLE_PIT_MEXC", "1") == "1":
        try:
            from colabtool.exchanges import fetch_mexc_pairs
            mexc_df = fetch_mexc_pairs(force=True)
            save_snapshot(mexc_df, "mexc_pairs", snapshot_dir)
        except Exception as e:
            print(f"[warn] mexc_pairs failed: {e}")

    # --- Alias Seed ---
    if os.getenv("ENABLE_PIT_ALIAS", "1") == "1":
        try:
            from colabtool.data_sources import get_alias_seed
            alias_df = get_alias_seed()
            if alias_df is not None:
                save_snapshot(alias_df, "seed_alias", snapshot_dir)
        except Exception as e:
            print(f"[warn] alias_seed failed: {e}")

    # --- Excel Export ---
    try:
        export_excel_snapshot(snapshot_dir)
    except Exception as e:
        print(f"[warn] Excel-Export fehlgeschlagen: {e}")

    print("📦 Snapshot completed successfully.")

if __name__ == "__main__":
    run()
