# Scanner Configuration Specification

**Spec Version:** v1.0  
**Audience:** Developers + GPT  
**Purpose:** Defines the deterministic and versioned configuration model used by the scanner.

---

## Overview

The configuration controls:

- pipeline behavior
- thresholds & lookbacks
- penalties & scoring weights
- run modes
- data source usage

Configuration must be:

- explicit
- deterministic
- versioned
- snapshot-captured

Changes **impact backtest compatibility** and must increment version numbers.

---

## Configuration Model

Primary sources:

1. `config.yml` (main config)
2. Environment variables (override)
3. CLI arguments (optional)

Priority:

```
CLI > ENV > config.yml
```

---

## Structure (Recommended)

```
general:
data_sources:
universe_filters:
exclusions:
mapping:
features:
scoring:
backtest:
logging:
```

---

## Sections

### General

```yaml
general:
  run_mode: "standard"   # standard|fast|offline|backtest
  timezone: "UTC"
  shortlist_size: 100
  lookback_days_1d: 120
  lookback_days_4h: 30
```

---

### Data Sources

```yaml
data_sources:
  mexc:
    enabled: true
    max_retries: 3
    retry_backoff_seconds: 3

  market_cap:
    provider: "cmc"
    api_key_env_var: "CMC_API_KEY"
    max_retries: 3
    bulk_limit: 5000
```

Rate limits should be static per provider.

---

### Universe Filters

```yaml
universe_filters:
  market_cap:
    min_usd: 100000000     # 100M
    max_usd: 3000000000    # 3B
  volume:
    min_quote_volume_24h: 1000000
  history:
    min_history_days_1d: 60
  include_only_usdt_pairs: true
```

---

### Exclusions

```yaml
exclusions:
  exclude_stablecoins: true
  exclude_wrapped_tokens: true
  exclude_leveraged_tokens: true
  exclude_synthetic_derivatives: true

  stablecoin_patterns: ["USD", "USDT", "USDC", "EURT"]
  wrapped_patterns: ["WETH", "WBTC", "st", "stk", "w"]
  leveraged_patterns: ["UP", "DOWN", "BULL", "BEAR", "3L", "3S"]
```

---

### Mapping

```yaml
mapping:
  require_high_confidence: false
  overrides_file: "config/mapping_overrides.json"
  collisions_report_file: "reports/mapping_collisions.csv"
  unmapped_behavior: "filter"   # or "warn"
```

---

### Features

```yaml
features:
  timeframes: ["1d", "4h"]
  ema_periods: [20, 50]
  atr_period: 14

  high_low_lookback_days:
    breakout: 30
    reversal: 60

  volume_sma_period: 7
  volume_spike_threshold: 1.5
  drawdown_lookback_days: 365
```

---

### Scoring

**Breakout**

```yaml
scoring:
  breakout:
    enabled: true
    high_lookback_days: 30
    min_volume_spike_factor: 1.5
    max_overextension_ema20_percent: 25
    weights:
      price_break: 0.40
      volume_confirmation: 0.40
      volatility_context: 0.20
```

**Pullback**

```yaml
  pullback:
    enabled: true
    max_pullback_from_high_percent: 25
    min_trend_days: 10
    ema_trend_period_days: 20
    weights:
      trend_quality: 0.40
      pullback_quality: 0.40
      rebound_signal: 0.20
```

**Reversal**

```yaml
  reversal:
    enabled: true
    min_drawdown_from_ath_percent: 40
    max_drawdown_from_ath_percent: 90
    base_lookback_days: 45
    min_base_days_without_new_low: 10
    max_allowed_new_low_percent_vs_base_low: 3
    min_reclaim_above_ema_days: 1
    min_volume_spike_factor: 1.5
    weights:
      base_structure: 0.30
      reclaim_signal: 0.40
      volume_confirmation: 0.30
```

---

### Backtest

```yaml
backtest:
  enabled: true
  forward_return_days: [7, 14, 30]
  max_holding_days: 30
  entry_price: "close"
  exit_price: "close_forward"
  slippage_bps: 10
```

---

### Logging

```yaml
logging:
  level: "INFO"
  file: "logs/scanner.log"
  log_to_file: true
```

---

## Versioning

Configuration changes must bump:

- `config_version`
- `spec_version`

Example:

```yaml
version:
  config: 1.0
  spec: 1.0
```

---

## Anti-Goofs (Important)

Config must not:

- contain fuzzy logic
- depend on ML
- rely on sentiment/news
- implicitly couple scoring modules
- silently change behavior across runs
- mix incompatible parameter domains

---

## Extensibility (v1)

Config must allow adding:

- filters
- penalties
- scores
- timeframes
- data sources

Backward compatibility is desirable but optional for v1.

---
