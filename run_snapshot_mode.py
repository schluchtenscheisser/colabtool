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
