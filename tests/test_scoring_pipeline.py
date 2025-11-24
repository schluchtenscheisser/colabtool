import pandas as pd
import numpy as np
from colabtool.scores import score_block, compute_early_score

def make_mock_df():
    np.random.seed(42)
    return pd.DataFrame({
        'id': ['coin_a', 'coin_b', 'coin_c'],
        'market_cap': [1.5e8, 3e8, 7e8],
        'price_change_percentage_7d_in_currency': [12, -5, 30],
        'price_change_percentage_30d_in_currency': [40, -20, 70],
        'volume_mc_ratio': [0.8, 1.5, 2.0],
        'ath_change_percentage': [-80, -60, -90],
        'buzz_level': [10, 3, 8],
        'buzz_acc': [5, 2, 4],
        'breakout_score': [1.2, 0.8, 1.5],
    })

def test_score_block_generates_nonzero_scores():
    df = make_mock_df()
    result = score_block(df)
    assert 'score_global' in result.columns
    assert 'score_segment' in result.columns
    assert result['score_global'].abs().sum() > 0
    assert result['score_segment'].abs().sum() > 0

def test_compute_early_score_adds_column():
    df = make_mock_df()
    result = compute_early_score(df)
    assert 'early_score' in result.columns
    assert not result['early_score'].isna().all()

def test_pipeline_scoring_consistency():
    df = make_mock_df()
    df1 = score_block(df.copy())
    df2 = compute_early_score(df1.copy())
    assert all(df2[['score_global', 'score_segment', 'early_score']].apply(lambda x: np.isfinite(x).all()))
