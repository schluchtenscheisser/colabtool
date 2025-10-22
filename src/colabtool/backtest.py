# modules/backtest.py
from __future__ import annotations
from typing import List
from .utils import pd, np, logging
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
        p_prev = float(prices[-(horizon+1)][1])
        if p_prev == 0:
            return np.nan
        return (p_now / p_prev - 1.0) * 100.0
    except Exception:
        return np.nan

def backtest_on_snapshot(df: pd.DataFrame, topk: int = 20, days_list: List[int] = [20,40,60], vs: str = "usd") -> pd.DataFrame:
    """
    Simpler Snapshot-Backtest:
    - Auswahl: Top-k nach 'early_score' (Fallback: 'score_segment', dann 'score_global').
    - Für jede ID: lädt 1× market_chart(days = max(days_list)+2) und berechnet rückblickende
      %-Veränderungen über 20/40/60 Tage (Approximation, da echte Zukunftsreturns erst später messbar sind).
    - Output: Tabelle mit Returns je Horizon + Basisinfos.
    Hinweis: Minimiert API-Calls (≤ topk).
    """
    df = df.copy()
    rank_cols = [c for c in ["early_score","score_segment","score_global"] if c in df.columns]
    if not rank_cols:
        logging.warning("[backtest] keine Ranking-Spalten gefunden")
        return pd.DataFrame()

    rank_col = rank_cols[0]
    picks = df.dropna(subset=[rank_col]).sort_values(rank_col, ascending=False).head(topk).copy()
    if picks.empty:
        return pd.DataFrame()

    max_h = max(days_list) if len(days_list) else 60
    rows = []
    for _, r in picks.iterrows():
        cid = str(r["id"])
        data = cg_market_chart(cid, vs=vs, days=max(200, max_h+10)) or {}
        prices = data.get("prices", [])
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
        for h in days_list:
            out[f"ret_{h}d_pct"] = _forward_return_from_chart(prices, h)
        rows.append(out)

    bt = pd.DataFrame(rows)
    # Aggregat-Zeile
    if not bt.empty:
        agg = {"id": "AGG_MEAN", "symbol": "-", "name": "-", "Segment": "-",
               "rank_col": rank_col, "rank_val": bt["rank_val"].mean(),
               "early_score": bt["early_score"].mean(), "score_segment": bt["score_segment"].mean(),
               "score_global": bt["score_global"].mean(), "mexc_pair": "-"}
        for h in days_list:
            agg[f"ret_{h}d_pct"] = bt[f"ret_{h}d_pct"].mean()
        bt = pd.concat([bt, pd.DataFrame([agg])], ignore_index=True)
    return bt

