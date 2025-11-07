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

    # CoinGecko Categories
    # cg_categories = get_cg_categories()
    # save_snapshot(pd.DataFrame(cg_categories), "cg_categories", snapshot_dir)

    # MEXC Pairs
    # mexc_df = fetch_mexc_pairs(force=True)
    # save_snapshot(mexc_df, "mexc_pairs", snapshot_dir)

    # Alias Seed (if exists)
    # alias_df = get_alias_seed()
    # if alias_df is not None:
    #     save_snapshot(alias_df, "seed_alias", snapshot_dir)

    print("Snapshot completed.")


if __name__ == "__main__":
    run()
