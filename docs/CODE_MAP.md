# 📘 CODE_MAP.md – Automatisch generiert
> Repository: schluchtenscheisser/colabtool  
> Letzte Aktualisierung: 2026-01-12 20:22 UTC

---

## 🧩 Modulübersicht

### 📄 `__init__.py`

**Funktionen:** –

**Variablen:** –

**Imports:** –

---

### 📄 `_legacy/features_legacy.py`

**Funktionen:** _ensure_series, _lc, _num_series, compute_feature_block, compute_mexc_features, exclusion_mask, fetch_mexc_klines, is_stable_like, is_wrapped_like, peg_like_mask, tag_segment

**Variablen:** EXCLUDE_IDS, MEXC_KLINES_URL, ath, ath_date, ath_dates, ath_dd, ath_drawdown_pct, ath_idx, ath_vals, cats_l, cleaned_data, closes, cols, cond_alt, cond_main, data, dd, df, f, i, kl, m, mc, mom30, mom7, mom_30d_pct, mom_7d_pct, n, out, p1, p30, p7, pair, price_sources, r30, resp, s, schema_map, symbol, vol_acc, vols

**Imports:** __future__, colabtool.utils.validation, logging, numpy, pandas, re, requests, typing, utilities

---

### 📄 `backtest.py`

**Funktionen:** _forward_return_from_chart, backtest_on_snapshot

**Variablen:** agg, bt, cid, col, data, df, max_h, out, p_now, p_prev, picks, prices, rank_col, rank_cols, rows

**Imports:** __future__, data_sources, typing, utilities

---

### 📄 `breakout.py`

**Funktionen:** _beta, _features_from_klines, _mexc_klines, _pct_change, _percentile_rank, _prep_betas, _rolling_max, _to_df, _valid_pair, _zscore, compute_breakout_for_ids

**Variablen:** a, b_btc, b_eth, breakout_base, c, cid, cols, cov, d, dfb, dfk, dist_180, dist_365, dist_90, donch_width, feat, keep, kl, last, m, ma30, ma30_last, ma7, ma7_last, max90, meta_cols, min90, num_cols, out, p365, pair, params, r, ret, rmax180, rmax365, rmax90, rows, s, sub, url, v, v_base, var, vol_acc, vol_usd, x, y, z_break, z_donch

**Imports:** __future__, math, requests, time, typing, utilities

---

### 📄 `buzz.py`

**Funktionen:** _age_weight, _collect_scores_for_ids, _compile_alias_regex, _env_float, _env_json_dict, _env_str, _is_colab, _load_alias_seed, _match_article, _parse_entry, _pub_weight, _resolve_seed_dir, add_buzz_metrics_for_candidates, fetch_rss_all

**Variablen:** HALF_LIFE_H, PUB_WEIGHTS, a, acc, age_h, alias_df, alist, articles, base_aliases, baseline, buzz_rows, cand_ids, cid, cnt, d, dec, df, df_alias, df_buzz, dh, entries, env, extra, feed, ids_set, in48, in7d, item, j, level, link, m, nam, now, parts, pat, path, pub, published, pw, raw, rows, rx_map, s, scores, src, sub, summary, sym, t, title, tmp, txt, v, w48, w7d

**Imports:** __future__, datetime, feedparser, google.colab, json, os, pathlib, re, time, typing, utilities

---

### 📄 `category_providers.py`

**Funktionen:** _cache_get, _cache_set, _cmc_get_map_by_symbols, _infer_from_tags, _load_cache, _messari_get_profile, _norm, _now_utc, _paprika_find_id, _paprika_get_coin, _save_cache, _set_many, _within_budget, enrich_categories_hybrid, get_cg_categories

**Variablen:** batch, budget_s, cache, cat, categories, cg_enrich_categories, cg_ids, cname, data, df, headers, hit, hits, ids, j, m, meta, params, pending, pid, prof, r, response, sect, slug, slug2, snapshot_df, sym, symbols, t0, tags, ts, txt, url, v

**Imports:** __future__, colabtool.data_sources, data_sources, datetime, json, os, re, requests, time, typing, utilities

---

### 📄 `cg_cache_patch.py`

**Funktionen:** _fresh, _path, setup_cg_chart_cache, wrapper

**Variablen:** h, j, key, mtime, p, root, st, ttl

**Imports:** __future__, datetime, hashlib, json, os, time, typing, utilities

---

### 📄 `data_sources.py`

**Funktionen:** _cg_get, _cg_throttle, _chart_cache_path, _env_bool, _env_float, _env_int, _env_str, _get_snapshot_dir, _is_colab, _make_cache_path, _one_get, _resolve_seed_dir, _sanitize_params_for_free, _sleep_min_interval, cg_market_chart, cg_markets, enrich_categories, ensure_seed_alias_exists, get_alias_seed, map_mexc_pairs, map_tvl, normalize_symbol, persist_pit_snapshot, update_seen_ids

**Variablen:** age_h, age_hours, alias_path, aliases, all_pages, alt_cols, budget_end, cache_path, cats, cg_data, coin_id, cpath, d, data, data2, date_str, days, delta, df, dt, env, file, fn, found, ids, interval, j, m, mapping, max_att, mexc_pairs, momentum_cols, mtime, new, now, p, p2, params, path, r, ratio, raw, rename_map, resp, resp2, resp3, s, seen, sm, sset, sym, symbols, today, url, use_live, val, vs, wait

**Imports:** __future__, colabtool.category_providers, datetime, google.colab, json, os, pandas, pathlib, requests, time, typing, utilities

---

### 📄 `data_sources_cmc.py`

**Funktionen:** _fetch_mexc_pairs, _log, _on_get, fetch_cmc_markets, load_or_fetch_markets, map_mexc_pairs, map_tvl, write_cache

**Variablen:** CMC_API_KEY, CMC_BASE_URL, MEXC_BASE_URL, all_rows, backoff, cache_path, data, df, headers, hits, mexc_symbols, pairs, params, path, quote, resp, start, today, tvl_df, url, wait

**Imports:** datetime, dotenv, json, logging, numpy, os, pandas, requests, time, typing

---

### 📄 `exchanges.py`

**Funktionen:** _apply_overrides, _choose_preferred_pair, _collect_collisions_in_listing, _http_json, _is_colab, _is_leveraged_symbol, _listing_from_exchange_info, _listing_from_ticker24, _load_mexc_listing, _load_seed_overrides, _resolve_seed_dir, apply_mexc_filter, export_mexc_seed_template, fetch_mexc_pairs

**Variablen:** b, base, before, cand, coll_bases, d, df, env, grouped, hit, j, last_err, listing, m, out, pair_map, quote, r, s, seed, status, sym, symbol, vc

**Imports:** __future__, google.colab, os, pathlib, requests, time, typing, utilities

---

### 📄 `export.py`

**Funktionen:** _safe_col_width, create_full_excel_export, export_snapshot, reorder_columns, write_meta_sheet, write_sheet

**Variablen:** EXPORT_PATH, asof, available, col_letter, df, export_path, fixed_order, fmt_percent, fmt_thousands, formatted, full_df, meta_df, remaining, required_cols, snapshot_dir, top10_emerging, top10_hidden, top25_early, top25_global, use_xlsxwriter, width, worksheet

**Imports:** __future__, datetime, export_helpers, logging, os, pandas.api.types, typing, utilities

---

### 📄 `export_helpers.py`

**Funktionen:** _cols, make_fulldata

**Variablen:** audit, basic, breakout, buzz, d, order, out, scores, tvl

**Imports:** __future__, typing, utilities

---

### 📄 `features/__init__.py`

**Funktionen:** –

**Variablen:** –

**Imports:** compute_mexc_features, feature_block, fetch_mexc_klines, token_utils

---

### 📄 `features/compute_mexc_features.py`

**Funktionen:** _ensure_series, _lc, _num_series, compute_mexc_features

**Variablen:** ath, ath_date, ath_drawdown_pct, ath_idx, closes, cols, mom_30d_pct, mom_7d_pct, result, vol_acc, volumes

**Imports:** __future__, logging, numpy, pandas, typing

---

### 📄 `features/feature_block.py`

**Funktionen:** compute_feature_block

**Variablen:** df, fallback, feats, klines, pair, schema_map, success, symbol, total

**Imports:** __future__, colabtool.features.compute_mexc_features, colabtool.features.fetch_mexc_klines, colabtool.utils.validation, logging, numpy, pandas, typing

---

### 📄 `features/fetch_mexc_klines.py`

**Funktionen:** fetch_mexc_klines

**Variablen:** MEXC_KLINES_URL, cleaned, data, df, resp

**Imports:** __future__, logging, numpy, pandas, requests, typing

---

### 📄 `features/token_utils.py`

**Funktionen:** exclusion_mask, is_stable_like, is_wrapped_like, peg_like_mask, tag_segment

**Variablen:** cat_lower, name, pattern, slug, symbol

**Imports:** pandas, re, typing

---

### 📄 `pit_snapshot.py`

**Funktionen:** export_excel_snapshot, run, save_snapshot

**Variablen:** alias_df, cg_categories, csv_files, df, excel_path, meta_info, mexc_df, path, sheet_name, snapshot_dir, today

**Imports:** colabtool.category_providers, colabtool.data_sources, colabtool.exchanges, colabtool.export, datetime, os, pandas, pathlib

---

### 📄 `pre_universe.py`

**Funktionen:** _is_leveraged, apply_pre_universe_filters, attach_categories

**Variablen:** cat_map, d, examples, ids, kept, m_any, m_core, m_lever, m_peg_lowvar, m_stable, m_wrapped, n, s

**Imports:** __future__, data_sources, features, re, typing, utilities

---

### 📄 `run_snapshot_mode.py`

**Funktionen:** run_snapshot, validate_scores

**Variablen:** ASOF_DATE, SCHEMA_MAP, alias_path, backtest_results, cand_ids, cg_path, df, export_filename, export_path, full_df, hits, mexc_path, missing, nan_counts, required_cols, seed_alias, snapshot_dir, valid_count

**Imports:** colabtool.backtest, colabtool.breakout, colabtool.buzz, colabtool.data_sources, colabtool.data_sources_cmc, colabtool.export, colabtool.export_helpers, colabtool.features, colabtool.pre_universe, colabtool.scores, colabtool.utils.validation, datetime, logging, pandas, pathlib

---

### 📄 `run_snapshot_mode_patch.py`

**Funktionen:** run_with_scoring

**Variablen:** df, dummy, meta

**Imports:** logging, pandas, src.colabtool.export, src.colabtool.scores

---

### 📄 `scores.py`

**Funktionen:** _align_bool_mask, _ensure_series, _mc_bucket, _safe_num, _winsorize, _z, _z_by_bucket, compute_early_score, compute_scores, score_block

**Variablen:** arr, b, damp_factor, df, early, m, mc, out, overheat_mask, required_cols, s, score_global, vals, x, z

**Imports:** __future__, logging, typing, utilities

---

### 📄 `utilities.py`

**Funktionen:** _cache_key, _is_colab, _resolve_cache_dir, http_get_json, safe_div, winsor_minmax

**Variablen:** CACHE_DIR, CG_KEY, HOST_MIN_INTERVAL, HTTP_BACKOFF, HTTP_MAX_RETRIES, HTTP_TIMEOUT, a, b, base, ck, cp, data, env_dir, host, iv, last, last_status, mtime, params, r, ra, sd, session, sleep_s, tried_qparam, wait, x

**Imports:** datetime, google.colab, hashlib, json, logging, math, numpy, os, pandas, pathlib, random, re, requests, time, urllib.parse

---

### 📄 `utils/__init__.py`

**Funktionen:** –

**Variablen:** –

**Imports:** –

---

### 📄 `utils/validation.py`

**Funktionen:** ensure_schema, validate_nonempty, validate_required_columns

**Variablen:** extra_cols, missing

**Imports:** logging, pandas, typing

---


## 🔗 Funktionsabhängigkeiten (Call Graph)


### 📄 _legacy/features_legacy.py

| Aufrufende Funktion | Interne Aufrufe | Externe Aufrufe |

|----------------------|------------------|------------------|

| `_ensure_series` | – | Series |

| `_lc` | – | lower, strip |

| `_num_series` | _ensure_series | Series, to_numeric |

| `compute_feature_block` | compute_mexc_features, fetch_mexc_klines | append, copy, debug, ensure_schema, get, info, iterrows, strip, upper, warning |

| `compute_mexc_features` | – | argmax, mean |

| `exclusion_mask` | _ensure_series, is_stable_like, is_wrapped_like | Series, apply, astype, contains, isin, lower |

| `fetch_mexc_klines` | – | DataFrame, debug, get, info, json, to_datetime, to_numeric, upper, warning |

| `is_stable_like` | _lc | search |

| `is_wrapped_like` | _lc | search, startswith |

| `peg_like_mask` | _ensure_series, _num_series | astype, fillna |

| `tag_segment` | – | get, isfinite |


### 📄 backtest.py

| Aufrufende Funktion | Interne Aufrufe | Externe Aufrufe |

|----------------------|------------------|------------------|

| `backtest_on_snapshot` | _forward_return_from_chart | DataFrame, append, cg_market_chart, concat, copy, dropna, get, head, info, iterrows, mean, notna, sort_values, warning |


### 📄 breakout.py

| Aufrufende Funktion | Interne Aufrufe | Externe Aufrufe |

|----------------------|------------------|------------------|

| `_beta` | – | concat, cov, dropna, to_numeric, var |

| `_features_from_klines` | _percentile_rank, _rolling_max | astype, isfinite, mean, rolling, tail |

| `_mexc_klines` | – | get, json, sleep, warning |

| `_pct_change` | – | pct_change, replace |

| `_percentile_rank` | – | isfinite, mean, to_numeric |

| `_prep_betas` | _mexc_klines, _pct_change, _to_df | get |

| `_rolling_max` | – | rolling |

| `_to_df` | – | DataFrame, dropna, items, reset_index, sort_values, to_datetime, to_numeric |

| `_valid_pair` | – | endswith, strip, upper |

| `_zscore` | – | Series, isfinite, mean, std, to_numeric |

| `compute_breakout_for_ids` | _beta, _features_from_klines, _mexc_klines, _pct_change, _prep_betas, _to_df, _zscore | DataFrame, append, astype, copy, dropna, info, isin, iterrows, merge, to_numeric, warning |


### 📄 buzz.py

| Aufrufende Funktion | Interne Aufrufe | Externe Aufrufe |

|----------------------|------------------|------------------|

| `_age_weight` | – | total_seconds |

| `_collect_scores_for_ids` | _age_weight, _match_article, _pub_weight | get, items, total_seconds |

| `_compile_alias_regex` | – | astype, compile, copy, escape, groupby, isin, join, lower, strip, tolist, warning |

| `_env_float` | _env_str | split |

| `_env_json_dict` | _env_str | items, loads, lower, strip |

| `_env_str` | – | getenv, strip |

| `_load_alias_seed` | – | DataFrame, add, append, astype, get, is_file, iterrows, lower, read_csv, split, strip, warning |

| `_match_article` | – | bool, search |

| `_parse_entry` | – | datetime, get, now, strip |

| `_pub_weight` | – | get, lower, strip |

| `_resolve_seed_dir` | _is_colab | Path, cwd, getenv |

| `add_buzz_metrics_for_candidates` | _collect_scores_for_ids, _compile_alias_regex, _load_alias_seed, fetch_rss_all | DataFrame, append, astype, copy, dropna, fillna, get, head, iterrows, lower, merge, now, sort_values, strip, to_numeric, tolist, warning |

| `fetch_rss_all` | _parse_entry | append, get, info, parse, warning |


### 📄 category_providers.py

| Aufrufende Funktion | Interne Aufrufe | Externe Aufrufe |

|----------------------|------------------|------------------|

| `_cache_get` | _now_utc | fromisoformat, get, timedelta |

| `_cache_set` | _now_utc | isoformat |

| `_cmc_get_map_by_symbols` | – | get, items, join, json, upper, warning |

| `_infer_from_tags` | – | join, search |

| `_load_cache` | – | isfile, load |

| `_messari_get_profile` | – | get, json |

| `_norm` | – | lower, sub |

| `_now_utc` | – | now |

| `_paprika_find_id` | – | get, json |

| `_paprika_get_coin` | – | format, get, json |

| `_save_cache` | – | dump |

| `_set_many` | _cache_set | items |

| `_within_budget` | – | perf_counter |

| `enrich_categories_hybrid` | _cache_get, _cache_set, _cmc_get_map_by_symbols, _infer_from_tags, _load_cache, _messari_get_profile, _norm, _paprika_find_id, _paprika_get_coin, _save_cache, _set_many, _within_budget | DataFrame, append, astype, cg_enrich_categories, copy, get, isin, items, iterrows, lower, perf_counter, persist_pit_snapshot, tolist, unique, upper, warning |

| `get_cg_categories` | – | append, get, json |


### 📄 cg_cache_patch.py

| Aufrufende Funktion | Interne Aufrufe | Externe Aufrufe |

|----------------------|------------------|------------------|

| `_fresh` | – | fromtimestamp, now, stat |

| `_path` | – | encode, hexdigest, join, sha1 |

| `setup_cg_chart_cache` | – | callable, getcwd, info, join, makedirs, timedelta, warning |

| `wrapper` | _fresh, _path | dump, isfile, load, orig, warning |


### 📄 data_sources.py

| Aufrufende Funktion | Interne Aufrufe | Externe Aufrufe |

|----------------------|------------------|------------------|

| `_cg_get` | _one_get, _sanitize_params_for_free | – |

| `_cg_throttle` | – | sleep, time |

| `_chart_cache_path` | _make_cache_path | Path, mkdir, replace |

| `_env_bool` | _env_str | lower |

| `_env_float` | _env_str | – |

| `_env_int` | _env_str | – |

| `_env_str` | – | getenv, split, strip |

| `_get_snapshot_dir` | – | join, makedirs, strftime, today |

| `_make_cache_path` | _get_snapshot_dir | join |

| `_one_get` | _sleep_min_interval | get, json, sleep, time, warning |

| `_resolve_seed_dir` | _is_colab | Path, cwd, getenv |

| `_sanitize_params_for_free` | – | pop |

| `_sleep_min_interval` | – | sleep, time |

| `cg_market_chart` | _cg_throttle, _chart_cache_path | dump, get, is_file, json, load, lower, mkdir, raise_for_status, sleep, stat, strip, time |

| `cg_markets` | _cg_throttle, _make_cache_path | DataFrame, ValueError, exists, extend, fromtimestamp, get, getmtime, json, lower, notna, now, raise_for_status, read_csv, sleep, to_csv, total_seconds, warning |

| `enrich_categories` | _cg_get | get, info, setdefault, sleep, time |

| `ensure_seed_alias_exists` | _make_cache_path | DataFrame, exists, to_csv |

| `get_alias_seed` | – | DataFrame, append, get_cg_categories |

| `map_mexc_pairs` | _make_cache_path | DataFrame, apply, astype, exists, fromtimestamp, get, getmtime, isin, json, makedirs, notna, now, raise_for_status, read_csv, rename, replace, split, strip, to_csv, total_seconds, upper, warning |

| `map_tvl` | – | astype, copy, is_file, read_csv, set_index, to_dict, to_numeric, warning |

| `normalize_symbol` | – | replace, strip, upper |

| `persist_pit_snapshot` | – | Path, mkdir, strftime, to_json, warning |

| `update_seen_ids` | – | add, dump, is_file, load |


### 📄 data_sources_cmc.py

| Aufrufende Funktion | Interne Aufrufe | Externe Aufrufe |

|----------------------|------------------|------------------|

| `_fetch_mexc_pairs` | – | error, get, json, sleep, warning |

| `_on_get` | _log | get, sleep |

| `fetch_cmc_markets` | _log, _on_get | DataFrame, append, get, info, json, makedirs, notnull, now, sleep, strftime, to_csv, warning, where |

| `load_or_fetch_markets` | _log, fetch_cmc_markets | exists, now, read_csv, strftime |

| `map_mexc_pairs` | _fetch_mexc_pairs | apply, astype, get, info, notna, upper, warning |

| `map_tvl` | _log | exists, merge, read_csv |

| `write_cache` | _log | makedirs, now, strftime, to_csv |


### 📄 exchanges.py

| Aufrufende Funktion | Interne Aufrufe | Externe Aufrufe |

|----------------------|------------------|------------------|

| `_apply_overrides` | – | apply, astype, copy, dropna, get, set_index, to_dict, upper |

| `_collect_collisions_in_listing` | – | info, to_dict, value_counts |

| `_http_json` | – | get, json, sleep, warning |

| `_is_leveraged_symbol` | – | endswith, upper |

| `_listing_from_exchange_info` | _http_json, _is_leveraged_symbol | DataFrame, append, drop_duplicates, get, upper |

| `_listing_from_ticker24` | _http_json, _is_leveraged_symbol | DataFrame, append, drop_duplicates, endswith, get, upper |

| `_load_mexc_listing` | _listing_from_exchange_info, _listing_from_ticker24 | error, info |

| `_load_seed_overrides` | – | DataFrame, astype, is_file, read_csv, upper, warning |

| `_resolve_seed_dir` | _is_colab | Path, cwd, getenv |

| `apply_mexc_filter` | _apply_overrides, _choose_preferred_pair, _collect_collisions_in_listing, _load_mexc_listing, _load_seed_overrides | RuntimeError, astype, copy, drop, groupby, info, isna, upper, warning |

| `export_mexc_seed_template` | _load_mexc_listing | DataFrame, astype, copy, info, isin, to_csv, tolist, unique, upper, value_counts, warning |

| `fetch_mexc_pairs` | _load_mexc_listing | DataFrame, RuntimeError |


### 📄 export.py

| Aufrufende Funktion | Interne Aufrufe | Externe Aufrufe |

|----------------------|------------------|------------------|

| `_safe_col_width` | – | astype, is_categorical_dtype, is_datetime64_any_dtype, is_numeric_dtype, nanmean, notna |

| `create_full_excel_export` | write_meta_sheet, write_sheet | ExcelWriter, head, info, items, now, sort_values, warning |

| `export_snapshot` | create_full_excel_export | exception, info, join, make_fulldata, makedirs, strftime, today |

| `write_meta_sheet` | – | from_dict, reset_index, set_column, to_excel |

| `write_sheet` | _safe_col_width, reorder_columns | add_format, cell, copy, set_column, sort_values, to_excel, warning |


### 📄 export_helpers.py

| Aufrufende Funktion | Interne Aufrufe | Externe Aufrufe |

|----------------------|------------------|------------------|

| `make_fulldata` | _cols | copy |


### 📄 features/compute_mexc_features.py

| Aufrufende Funktion | Interne Aufrufe | Externe Aufrufe |

|----------------------|------------------|------------------|

| `_ensure_series` | – | Series |

| `_lc` | – | lower, strip |

| `_num_series` | – | fillna, to_numeric |

| `compute_mexc_features` | – | astype, debug, error, mean, nanargmax, nanmax, to_numpy, warning |


### 📄 features/feature_block.py

| Aufrufende Funktion | Interne Aufrufe | Externe Aufrufe |

|----------------------|------------------|------------------|

| `compute_feature_block` | – | append, compute_mexc_features, copy, debug, ensure_schema, fetch_mexc_klines, get, info, iterrows, strip, upper, warning |


### 📄 features/fetch_mexc_klines.py

| Aufrufende Funktion | Interne Aufrufe | Externe Aufrufe |

|----------------------|------------------|------------------|

| `fetch_mexc_klines` | – | DataFrame, dropna, error, get, info, json, reset_index, to_datetime, to_numeric, upper, warning |


### 📄 features/token_utils.py

| Aufrufende Funktion | Interne Aufrufe | Externe Aufrufe |

|----------------------|------------------|------------------|

| `exclusion_mask` | – | Series, contains, lower |

| `is_stable_like` | – | bool, search, upper |

| `is_wrapped_like` | – | bool, match, upper |

| `peg_like_mask` | – | bool, search, upper |

| `tag_segment` | – | get, lower |


### 📄 pit_snapshot.py

| Aufrufende Funktion | Interne Aufrufe | Externe Aufrufe |

|----------------------|------------------|------------------|

| `export_excel_snapshot` | – | ExcelWriter, glob, isoformat, read_csv, utcnow, write_meta_sheet, write_sheet |

| `run` | export_excel_snapshot, save_snapshot | DataFrame, Path, date, fetch_mexc_pairs, get_alias_seed, get_cg_categories, getenv, mkdir, strftime, utcnow |

| `save_snapshot` | – | to_csv |


### 📄 pre_universe.py

| Aufrufende Funktion | Interne Aufrufe | Externe Aufrufe |

|----------------------|------------------|------------------|

| `_is_leveraged` | – | endswith, upper |

| `apply_pre_universe_filters` | _is_leveraged | apply, astype, copy, get, head, info, is_stable_like, is_wrapped_like, isin, items, lower, notna, peg_like_mask, to_dict, to_numeric, warning |

| `attach_categories` | – | astype, copy, enrich_categories, fillna, info, tolist |


### 📄 run_snapshot_mode.py

| Aufrufende Funktion | Interne Aufrufe | Externe Aufrufe |

|----------------------|------------------|------------------|

| `run_snapshot` | validate_scores | Path, add_buzz_metrics_for_candidates, apply_pre_universe_filters, backtest_on_snapshot, compute_breakout_for_ids, compute_early_score, compute_feature_block, create_full_excel_export, ensure_schema, error, exists, fetch_cmc_markets, get_alias_seed, info, make_fulldata, map_mexc_pairs, mkdir, notna, score_block, strftime, to_csv, today, tolist, warning |

| `validate_scores` | – | ValueError, dropna, info, isna, to_dict, warning |


### 📄 run_snapshot_mode_patch.py

| Aufrufende Funktion | Interne Aufrufe | Externe Aufrufe |

|----------------------|------------------|------------------|

| `run_with_scoring` | – | compute_early_score, export_to_excel, info, score_block, warning |


### 📄 scores.py

| Aufrufende Funktion | Interne Aufrufe | Externe Aufrufe |

|----------------------|------------------|------------------|

| `_align_bool_mask` | – | Series, astype, equals, fillna, to_numpy |

| `_ensure_series` | – | Series |

| `_mc_bucket` | – | Series, to_numeric |

| `_safe_num` | – | Series, to_numeric |

| `_winsorize` | – | clip, to_numeric |

| `_z` | – | Series, clip, isna, mean, std |

| `_z_by_bucket` | _winsorize | Series, astype, groupby, isfinite, items, mean, std, to_numeric |

| `compute_early_score` | – | clip, copy, fillna, where |

| `compute_scores` | compute_early_score, score_block | exception |

| `score_block` | _z | clip, copy, fillna, minimum, where |


### 📄 utilities.py

| Aufrufende Funktion | Interne Aufrufe | Externe Aufrufe |

|----------------------|------------------|------------------|

| `_cache_key` | – | encode, hexdigest, items, join, sha1 |

| `_resolve_cache_dir` | _is_colab | Path, cwd, getenv |

| `http_get_json` | _cache_key | dumps, error, exists, fromtimestamp, get, json, load, mkdir, now, replace, sleep, stat, time, timedelta, urlparse, warning, write_text |

| `safe_div` | – | isnan |

| `winsor_minmax` | – | clip, fillna, mean, notna, quantile, std, to_numeric |


### 📄 utils/validation.py

| Aufrufende Funktion | Interne Aufrufe | Externe Aufrufe |

|----------------------|------------------|------------------|

| `ensure_schema` | – | ValueError, astype, info, items, warning |

| `validate_nonempty` | – | ValueError |

| `validate_required_columns` | – | ValueError |


---

## 📊 Abhängigkeits-Statistik

| Modul | Interne Aufrufe | Externe Aufrufe | Gesamt |

|--------|------------------|------------------|---------|

| data_sources.py | 16 | 107 | 123 |

| buzz.py | 11 | 68 | 79 |

| exchanges.py | 14 | 61 | 75 |

| category_providers.py | 15 | 46 | 61 |

| breakout.py | 12 | 47 | 59 |

| _legacy/features_legacy.py | 10 | 39 | 49 |

| data_sources_cmc.py | 8 | 38 | 46 |

| scores.py | 4 | 35 | 39 |

| export.py | 5 | 31 | 36 |

| utilities.py | 2 | 33 | 35 |

| run_snapshot_mode.py | 1 | 30 | 31 |

| pre_universe.py | 1 | 24 | 25 |

| cg_cache_patch.py | 2 | 19 | 21 |

| pit_snapshot.py | 2 | 18 | 20 |

| backtest.py | 1 | 14 | 15 |

| features/token_utils.py | 0 | 14 | 14 |

| features/compute_mexc_features.py | 0 | 13 | 13 |

| features/feature_block.py | 0 | 12 | 12 |

| features/fetch_mexc_klines.py | 0 | 11 | 11 |

| utils/validation.py | 0 | 7 | 7 |

| run_snapshot_mode_patch.py | 0 | 5 | 5 |

| export_helpers.py | 1 | 1 | 2 |


🧠 *Hinweis:* Viele **externe Aufrufe** deuten auf hohe Kopplung hin → Kandidaten für Refactoring oder Modularisierung.
