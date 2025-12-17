# 📘 CODE_MAP.md – Modul-, Funktions- und Variablenübersicht
> Repository: `schluchtenscheisser/colabtool`  
> Version: initial full documentation (Dez 2025)

---

## 🧭 Zweck
Dieses Dokument dient als **zentrale technische Übersicht** für das gesamte Tool `colabtool`.  
Es listet alle wichtigen Module, deren Funktionen, Variablen und Abhängigkeiten auf.  
Ziel:  
- Inkonsistente Funktions- oder Variablennamen vermeiden  
- Schnell erkennen, wo welche Daten verarbeitet werden  
- Einheitliche Schnittstellen zwischen Modulen sichern  

---

## 📂 Modulübersicht

| Modul | Hauptaufgabe | Abhängig von |
|--------|---------------|--------------|
| `backtest.py` | Historische Performance-Simulation der Strategien | `utilities`, `data_sources` |
| `breakout.py` | Breakout-Erkennung, Momentum-Signale | `utilities` |
| `buzz.py` | Verarbeitung von News- & RSS-Daten (Buzz-Metrik) | `utilities` |
| `category_providers.py` | Coin-Kategorisierung aus mehreren APIs | `utilities`, `data_sources` |
| `data_sources.py` | CoinGecko-Datenabruf, Caching, Seeds | `utilities`, `category_providers` |
| `data_sources_cmc.py` | CMC-Fallback-Datenquelle | eigenständig |
| `exchanges.py` | MEXC-Daten & Handelspaare | `utilities`, `logger` |
| `features.py` | Technische Feature-Berechnung | `utilities`, `utils.validation` |
| `scores.py` | Score-Berechnung & Ranking | `utilities` |
| `pit_snapshot.py` | Snapshot-Erstellung (Daten → Excel) | `export`, `data_sources`, `exchanges` |
| `pre_universe.py` | Vorverarbeitung, Filterung, Universe-Definition | `utilities`, `features`, `data_sources` |
| `run_snapshot_mode.py` | Zentrale Steuerung der gesamten Pipeline | alle Kernmodule |
| `export.py` | Excel- und CSV-Export | `utilities`, `export_helpers` |
| `utilities.py` | Logging, Caching, HTTP, Rate-Limiting | Grundmodul |
| `utils/validation.py` | Schema-Validierung & Qualitätschecks | eigenständig |

---

## 🧩 Modul-Details

### 📄 backtest.py
- **Funktionen:** `_forward_return_from_chart`, `backtest_on_snapshot`
- **Imports:** `typing`, `.utilities`, `.data_sources`
- **Zweck:** Führt historische Tests auf Momentum-Snapshots durch.  
- **Variablen:** keine globalen Konstanten.

---

### 📄 breakout.py
- **Funktionen:** `_mexc_klines`, `_valid_pair`, `_to_df`, `_pct_change`, `_rolling_max`, `_percentile_rank`, `_zscore`, `_beta`, `_features_from_klines`, `_prep_betas`, `compute_breakout_for_ids`
- **Imports:** `requests`, `pandas`, `numpy`, `.utilities`
- **Variablen:** `_MEXC_BASE`, `_s`
- **Zweck:** Berechnet Breakout-Features auf Basis von Klines-Daten.

---

### 📄 buzz.py
- **Funktionen:** `_is_colab`, `_resolve_seed_dir`, `_env_str`, `_env_float`, `_env_json_dict`, `_parse_entry`, `fetch_rss_all`, `_load_alias_seed`, `_compile_alias_regex`, `_age_weight`, `_pub_weight`, `_match_article`, `_collect_scores_for_ids`, `add_buzz_metrics_for_candidates`
- **Imports:** `feedparser`, `pandas`, `numpy`, `.utilities`
- **Variablen:** `_SEED_DIR`, `HALF_LIFE_H`, `PUB_WEIGHTS`, `_FEEDS`, `__all__`
- **Zweck:** Berechnung von Buzz- und Sentimentmetriken aus RSS-Feeds.

---

### 📄 category_providers.py
- **Funktionen:** `_now_utc`, `_load_cache`, `_save_cache`, `_cache_get`, `_cache_set`, `_infer_from_tags`, `_norm`, `_cmc_get_map_by_symbols`, `_messari_get_profile`, `_paprika_find_id`, `_paprika_get_coin`, `enrich_categories_hybrid`, `get_cg_categories`
- **Imports:** `requests`, `pandas`, `numpy`, `.utilities`, `.data_sources`
- **Variablen:** `_CACHE_ROOT`, `_PROV_CACHE`, `_CMC_URL`, `_MESSARI_URL`, `_PAPRIKA_SEARCH`, `_PAPRIKA_COIN`, `_PROVIDERS_BUDGET_S`, `_TAG_RULES`
- **Zweck:** Hybridkategorisierung von Coins über mehrere APIs mit Caching.

---

### 📄 data_sources.py
- **Funktionen:** `_env_str`, `_env_bool`, `_env_int`, `_env_float`, `_is_colab`, `_resolve_seed_dir`, `_cg_throttle`, `_on_get`, `_cg_get`, `_make_cache_path`, `_chart_cache_path`, `cg_markets`, `enrich_categories`, `map_tvl`, `update_seen_ids`, `cg_market_chart`, `persist_pit_snapshot`, `get_alias_seed`, `map_mexc_pairs`, `ensure_seed_alias_exists`
- **Imports:** `requests`, `pandas`, `numpy`, `.utilities`, `.category_providers`
- **Variablen:** `_FORCE_FREE`, `_CG_KEY`, `_HAS_PRO`, `_CACHE_DIR`, `_SEED_DIR`
- **Zweck:** Einheitlicher Zugriff auf CoinGecko-Daten, Seeds und lokale Caches.

---

### 📄 data_sources_cmc.py
- **Funktionen:** `_log`, `_on_get`, `fetch_cmc_markets`, `_fetch_mex_pairs`, `map_mex_pairs`, `map_tvl`, `load_or_fetch_markets`, `write_cache`
- **Imports:** `requests`, `pandas`, `numpy`
- **Variablen:** `CMC_API_KEY`, `CMC_BASE_URL`, `MEXC_BASE_URL`, `_CACHE_DIR`
- **Zweck:** CoinMarketCap-Datenabruf mit Caching als Fallback für CoinGecko.

---

### 📄 exchanges.py
- **Funktionen:** `_is_colab`, `_resolve_seed_dir`, `_is_leveraged_symbol`, `_http_json`, `_listing_from_exchange_info`, `_listing_from_ticker24h`, `_load_mexclisting`, `_load_seed_overrides`, `_apply_overrides`, `_choose_preferred_pair`, `_collect_collisions_in_listing`, `apply_mex_filter`, `export_mex_seed_template`, `fetch_mex_pairs`
- **Imports:** `requests`, `pandas`, `numpy`, `.utilities`, `.logger`
- **Variablen:** `_MEXC_BASE`, `_MEXC_EXCHANGE_INFO`, `_MEXC_TICKER_24H`, `_PREFERRED_QUOTES`, `_LEVERAGE_SUFFIXES`, `SEED_DIR`, `SEED_FILE`
- **Zweck:** MEXC-API-Verwaltung, Pair-Filtration und Seed-Verwaltung.

---

### 📄 features.py
- **Funktionen:** `_ensure_series`, `_num_series`, `_lc`, `is_stable_like`, `is_wrapped_like`, `peg_like_mask`, `exclusion_mask`, `fetch_mexc_klines`, `compute_mex_feature`, `compute_feature_block`, `tag_segment`
- **Imports:** `requests`, `pandas`, `numpy`, `.utilities`, `colabtool.utils.validation`
- **Variablen:** `EXCLUDE_IDS`, `_STABLE_HINTS`, `_WRAPPED_HINTS`, `MEXC_KLINES_URL`
- **Zweck:** Erstellung technischer Indikatoren und Segment-Tags.

---

### 📄 scores.py
- **Funktionen:** `_ensure_series`, `_winsorize`, `_mc_bucket`, `_z_by_bucket`, `_safe_num`, `_align_bool_mask`, `score_block`, `compute_early_score`, `compute_scores`
- **Imports:** `pandas`, `numpy`, `.utilities`
- **Zweck:** Aggregation von Features zu quantitativen Scores und Segment-Rankings.

---

### 📄 pit_snapshot.py
- **Funktionen:** `save_snapshot`, `export_excel_snapshot`, `run`
- **Imports:** `.export`, `.data_sources`, `.exchanges`, `.category_providers`
- **Zweck:** Erzeugung und Export von PIT-Snapshots.

---

### 📄 pre_universe.py
- **Funktionen:** `_is_leveraged`, `apply_pre_universe_filters`, `attach_categories`
- **Imports:** `pandas`, `numpy`, `.utilities`, `.features`, `.data_sources`
- **Variablen:** `_LEVERAGE_SUFFIXES`, `_CORE_EXCLUDE_IDS`
- **Zweck:** Filterung und Vorbereitung des zu analysierenden Coin-Universums.

---

### 📄 run_snapshot_mode.py
- **Funktionen:** `validate_scores`, `run_snapshot`
- **Imports:** alle Kernmodule (`data_sources*`, `features`, `scores`, `backtest`, `export`, `buzz`, `breakout`)
- **Zweck:** Orchestrierung der vollständigen Snapshot-Pipeline.

---

### 📄 export.py
- **Funktionen:** `_safe_col_width`, `reorder_columns`, `write_sheet`, `write_meta_sheet`, `create_full_excel_export`, `export_snapshot`
- **Imports:** `pandas`, `numpy`, `.utilities`, `.export_helpers`
- **Variablen:** `_DEF_MIN`, `_DEF_MAX`, `_DEF_FALLBACK`, `EXPORT_PATH`
- **Zweck:** Export aller Ergebnisse in strukturierte Excel-Dateien.

---

### 📄 utilities.py
- **Funktionen:** `_is_colab`, `_resolve_cache_dir`, `safe_div`, `winsor_minmax`, `_cache_key`, `http_get_json`
- **Imports:** `requests`, `pandas`, `numpy`
- **Variablen:** `CACHE_DIR`, `HTTP_MAX_RETRIES`, `HTTP_BACKOFF`, `HOST_MIN_INTERVAL`, `_LAST_CALL`, `CG_KEY`
- **Zweck:** Basis-Utilities für Caching, API-Ratenbegrenzung und Logging.

---

### 📄 utils/validation.py
- **Funktionen:** `ensure_schema`, `validate_required_columns`, `validate_nonempty`
- **Imports:** `pandas`, `logging`
- **Zweck:** Validierung und Typprüfung von DataFrames in der Pipeline.

---

## 🔗 Modulabhängigkeitsmatrix

| Modul | Importiert |
|--------|-------------|
| `backtest` | `utilities`, `data_sources` |
| `breakout` | `utilities` |
| `buzz` | `utilities` |
| `category_providers` | `utilities`, `data_sources` |
| `data_sources` | `utilities`, `category_providers` |
| `data_sources_cmc` | – |
| `exchanges` | `utilities`, `logger` |
| `features` | `utilities`, `utils.validation` |
| `scores` | `utilities` |
| `pit_snapshot` | `export`, `exchanges`, `data_sources`, `category_providers` |
| `pre_universe` | `utilities`, `features`, `data_sources` |
| `run_snapshot_mode` | alle Kernmodule |
| `export` | `utilities`, `export_helpers` |
| `utilities` | – |
| `utils.validation` | – |

---

## 📋 Pflegehinweis

> **Regeln für künftige Änderungen:**
> 1. Vor jeder Codeänderung prüfen, ob Variablen / Funktionen bereits hier existieren.  
> 2. Neue Funktionen und Variablen immer zuerst in dieser Datei dokumentieren.  
> 3. Nach größeren Änderungen `pylint` und `mypy` laufen lassen.  
> 4. Bei neuen Modulen bitte am Ende dieser Datei Abschnitt ergänzen.  

---

✅ **Diese Datei ist ab sofort die „Single Source of Truth“**  
für alle Namenskonventionen und Funktionsdefinitionen im Projekt `colabtool`.

