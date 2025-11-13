import os
import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import patch

from colabtool.pit_snapshot import run

SNAPSHOT_DIR = Path("snapshots/20251112")  # anpassen je nach Datum

@pytest.fixture(autouse=True)
def enable_all_sources(monkeypatch):
    monkeypatch.setenv("ENABLE_PIT_CATEGORIES", "1")
    monkeypatch.setenv("ENABLE_PIT_MEXC", "1")
    monkeypatch.setenv("ENABLE_PIT_ALIAS", "1")

def test_run_creates_snapshots(tmp_path, monkeypatch):
    monkeypatch.setattr("colabtool.pit_snapshot.Path", lambda x=None: tmp_path / today)

    with patch("colabtool.category_providers.get_cg_categories", return_value=[{"id": "defi"}]), \
         patch("colabtool.exchanges.fetch_mexc_pairs", return_value=pd.DataFrame([{"symbol": "ABC_USDT"}])), \
         patch("colabtool.data_sources.get_alias_seed", return_value=pd.DataFrame([{"alias": "ABC", "coin_id": "abc"}])):
        
        run()

        from datetime import datetime
        today = datetime.utcnow().date().strftime("%Y%m%d")
        files = list((tmp_path / today).glob("*.csv"))
        names = [f.name for f in files]
        assert "cg_categories.csv" in names
        assert "mexc_pairs.csv" in names
        assert "seed_alias.csv" in names

        for file in files:
            df = pd.read_csv(file)
            assert not df.empty

