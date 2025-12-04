# modules/backtest.py
from __future__ import annotations
from typing import List
from .utilities import pd, np, logging
from .data_sources import cg_market_chart


def _forward_return_from_chart(prices: List[List[float]], horizon: int) -> float:
    """
    Erwartet CoinGecko market_chart 'prices': [[ts, price], ...]
    Nutzt Schlusskurs[t] und Schlusskurs[t-horizon] → (p_t / p_{t-h} - 1)*100.
    Gibt NaN zurück, wenn zu wenige Punkte.
    """
    if not prices or len(prices) <= horizon:
        return np.nan
    try:
        p_now = float(prices[-1][1])
        p_prev = float(prices[-(horizon + 1)][1])
        if p_prev == 0:
            return np.nan
        return (p_now / p_prev - 1.0) * 100.0
    except Exception:
        return np.nan


def backtest_on_snapshot(
    df: pd.DataFrame,
    top_k: int = 20,
    horizons: List[int] = [20, 40, 60],
    vs: str = "usd"
) -> pd.DataFrame:
    """
    Simpler Snapshot-Backtest:
    - Auswahl: Top-k nach 'early_score' (Fallback: 'score_segment', dann 'score_global').
    - Für jede ID: lädt 1× market_chart(days = max(horizons)+2) und berechnet rückblickende
      %-Veränderungen über die angegebenen Horizonte (Approximation, da echte Zukunftsreturns
      erst später messbar sind).
    - Output: Tabelle mit Returns je Horizon + Basisinfos.
    Hinweis: Minimiert API-Calls (≤ top_k).
    """
    df = df.copy()
    rank_cols = [c for c in ["early_score", "score_segment", "score_global"] if c in df.columns]
    if not rank_cols:
        logging.warning("[backtest] keine Ranking-Spalten gefunden")
        return pd.DataFrame()

    rank_col = rank_cols[0]
    picks = df.dropna(subset=[rank_col]).sort_values(rank_col, ascending=False).head(top_k).copy()
    if picks.empty:
        logging.warning("[backtest] keine Kandidaten für Backtest gefunden")
        return pd.DataFrame()

    max_h = max(horizons) if len(horizons) else 60
    rows = []

    for _, r in picks.iterrows():
        cid = str(r["id"])
        try:
            data = cg_market_chart(cid, vs=vs, days=max(200, max_h + 10)) or {}
            prices = data.get("prices", [])
        except Exception as ex:
            logging.warning(f"[backtest] {cid} market_chart Fehler: {ex}")
            prices = []

        out = {
            "id": cid,
            "symbol": r.get("symbol"),
            "name": r.get("name"),
            "Segment": r.get("Segment"),
            "rank_col": rank_col,
            "rank_val": float(r.get(rank_col)) if pd.notna(r.get(rank_col)) else np.nan,
            "early_score": r.get("early_score"),
            "score_segment": r.get("score_segment"),
            "score_global": r.get("score_global"),
            "mexc_pair": r.get("mexc_pair")
        }

        for h in horizons:
            out[f"ret_{h}d_pct"] = _forward_return_from_chart(prices, h)
        rows.append(out)

    bt = pd.DataFrame(rows)

    # Aggregat-Zeile
    if not bt.empty:
        agg = {
            "id": "AGG_MEAN",
            "symbol": "-",
            "name": "-",
            "Segment": "-",
            "rank_col": rank_col,
            "rank_val": bt["rank_val"].mean(),
            "early_score": bt["early_score"].mean(),
            "score_segment": bt["score_segment"].mean(),
            "score_global": bt["score_global"].mean(),
            "mexc_pair": "-"
        }
        for h in horizons:
            col = f"ret_{h}d_pct"
            if col in bt.columns:
                agg[col] = bt[col].mean()
        bt = pd.concat([bt, pd.DataFrame([agg])], ignore_index=True)

    logging.info(f"[backtest] abgeschlossen: {len(bt)} Zeilen, Horizonte={horizons}")
    return bt
