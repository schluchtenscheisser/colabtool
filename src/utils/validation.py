diff --git a/src/utils/validation.py b/src/utils/validation.py
new file mode 100644
index 0000000..a9b6b8e
--- /dev/null
+++ b/src/utils/validation.py
@@
+"""
+validation.py — Preflight-Schema-Check für Snapshot-Daten
+
+Stellt sicher, dass DataFrames die erwartete Struktur haben.
+Fehlende Spalten werden automatisch ergänzt, Typen geprüft.
+"""
+
+import pandas as pd
+import logging
+from typing import Dict, Type
+
+
+def ensure_schema(df: pd.DataFrame, schema_map: Dict[str, Type]) -> pd.DataFrame:
+    """
+    Ensures that the given DataFrame matches the expected schema.
+    - Adds missing columns with default values
+    - Coerces datatypes if possible
+    - Logs any inconsistencies
+    """
+    if df is None or not isinstance(df, pd.DataFrame):
+        raise ValueError("ensure_schema: input is not a valid DataFrame")
+
+    for col, dtype in schema_map.items():
+        if col not in df.columns:
+            logging.warning(f"[ensure_schema] Adding missing column: {col}")
+            # assign sensible default based on dtype
+            if dtype in (float, int):
+                df[col] = 0
+            elif dtype is bool:
+                df[col] = False
+            else:
+                df[col] = None
+
+        # type coercion (non-fatal)
+        try:
+            df[col] = df[col].astype(dtype, errors="ignore")
+        except Exception as e:
+            logging.warning(f"[ensure_schema] Failed to coerce {col} to {dtype}: {e}")
+
+    # remove unexpected columns (optional, keep for audit)
+    extra_cols = [c for c in df.columns if c not in schema_map]
+    if extra_cols:
+        logging.info(f"[ensure_schema] Extra columns present: {extra_cols}")
+
+    return df
+
+
+def validate_required_columns(df: pd.DataFrame, required: list[str]) -> None:
+    """Raises ValueError if required columns are missing."""
+    missing = [c for c in required if c not in df.columns]
+    if missing:
+        raise ValueError(f"Missing required columns: {missing}")
+
+
+def validate_nonempty(df: pd.DataFrame, min_rows: int = 1) -> None:
+    """Ensures that the DataFrame has at least `min_rows`."""
+    if df.empty or len(df) < min_rows:
+        raise ValueError(f"DataFrame has insufficient rows: {len(df)} < {min_rows}")

diff --git a/src/run_snapshot_mode.py b/src/run_snapshot_mode.py
index 8a7b21f..dc9d0ce 100644
--- a/src/run_snapshot_mode.py
+++ b/src/run_snapshot_mode.py
@@
 import logging
 import pandas as pd
 from datetime import datetime
 from src.scores import compute_scores
 from src.export import export_snapshot
@@
 def run_snapshot_mode(mode: str = "standard"):
     """
     Führt den vollständigen Snapshot-Lauf aus:
     - Datenerhebung (CoinGecko, MEXC)
     - Scoring
     - Export
     """
-    logging.info(f"Starting snapshot in mode={mode}")
-
-    df = assemble_snapshot_data(mode=mode)
-
-    df = compute_scores(df)
-    export_snapshot(df)
-    logging.info("Snapshot completed successfully.")
+    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
+    logging.info(f"Starting snapshot in mode={mode}")
+
+    from src.utils.validation import ensure_schema
+
+    # --- 1. Assemble or mock data ---
+    df = assemble_snapshot_data(mode=mode)
+
+    # --- 2. Preflight validation ---
+    SCHEMA_MAP = {
+        "id": str,
+        "symbol": str,
+        "market_cap": float,
+        "total_volume": float,
+        "early_score": float,
+        "breakout_score": float,
+        "mexc_pair": str,
+        "ath": float,
+        "current_price": float,
+    }
+
+    df = ensure_schema(df, SCHEMA_MAP)
+
+    # --- 3. Compute scores ---
+    df = compute_scores(df)
+
+    # --- 4. Export results ---
+    export_snapshot(df)
+
+    logging.info(f"Snapshot completed successfully with {len(df)} assets.")

