# quant_journey

A single monorepo housing all **100 projects** of the [quant roadmap](roadmap.md) — from a
first `pip install` to an autonomous agentic trading system. Each project is a flat,
independently-runnable folder; shared logic compounds into one mini-library, [`quant_core`](quant_core/).

## Layout

```
quant_journey/
├── quant_core/                 # shared, versioned mini-library (data, backtest, metrics, ...)
├── command_center/             # Bloomberg-style research terminal (FastAPI + React) over quant_core
├── 001_market_data_downloader_cleaner/   # ← built
├── 002_.../             # added iteratively, one per roadmap entry
│   ...
├── roadmap.md                  # the 100-project plan (canonical descriptions)
├── Makefile                    # make run N=1 / test N=1 / lint / list / relock / cc (terminal)
└── ruff.toml, .python-version, LICENSE, .env.example
```

## How it works

- **Python 3.12 + [uv](https://docs.astral.sh/uv/).** Each project is its **own uv project with
  its own `.venv`**, depending on `quant_core` through an **editable path source** — so common
  deps live once in `quant_core` and each project only adds its **unique/heavy** deps (torch,
  gymnasium, cvxpy, …). This is deliberately *not* a uv workspace (a workspace forces one shared
  env and one version per package, which breaks down once the deep-learning phases need
  conflicting stacks).
- **Version-pinned core.** Projects pin a compatible range (e.g. `quant-core>=0.1,<0.2`). When
  `quant_core` makes a breaking change it bumps its minor, and an out-of-range project fails its
  `uv sync --locked` *loudly* — keeping older projects reproducible. `uv.lock` is committed
  everywhere.
- **Reuse boundary.** A project imports only `quant_core` + PyPI — never another project. Logic
  that more than one project needs **graduates into `quant_core`**.

## Run any project

```bash
# Prereq: install uv (https://docs.astral.sh/uv/), then from the repo root:
cd 001_market_data_downloader_cleaner
uv sync                 # builds the editable quant_core + this project's deps
uv run python main.py   # run it
uv run pytest           # offline tests
```

Or via the Makefile from the repo root: `make run N=1`, `make test N=1`, `make list`.

## The research terminal (`command_center/`)

A Bloomberg-style, keyboard-driven web terminal to visualize every project's data and find
patterns. It's a **thin viz layer**: a FastAPI backend serves a typed API over `quant_core`
(analytics graduate into the library, never the app), and a React/Vite frontend renders dense,
dark, cross-linked panels. It works offline on a fresh clone via a deterministic **synthetic seed**
(real data via `make cc-seed` is best-effort/local only — never committed).

```bash
make cc-setup     # uv-sync the backend + npm-install the frontend
make cc           # seed synthetic data, build the SPA, serve the whole terminal at :8000
make cc-dev       # dev mode: FastAPI :8000 + Vite :5173 (hot reload)
make cc-test      # backend pytest + frontend typecheck/vitest
```

v1 panels: Data Catalog (`DATA`), Price & Corporate Actions (`PX`), Performance Overlay (`PERF`),
Returns & Distributions (`RET`), Rolling Stats (`ROLL`), Correlation (`CORR`). Press `:` for the
command bar. New panels are one folder under `frontend/src/panels/` — see the `add-panel` skill in
`.claude/skills/`.

## Folder-naming convention

`NNN_<slug>` where `NNN` is the 3-digit roadmap number (sorts correctly through 100) and
`<slug>` is the **bolded roadmap title** lowercased, non-alphanumerics → `_`, no truncation.

---

## The 100 projects

Status: ✅ Built · ⬜ Planned. Descriptions live in [roadmap.md](roadmap.md).

### Phase 1 — Foundations: Data, Stats & Tooling

| # | Project | Folder | Status |
|---|---------|--------|--------|
| 1 | Market data downloader & cleaner | [`001_market_data_downloader_cleaner/`](001_market_data_downloader_cleaner/) | ✅ Built |
| 2 | Returns & distribution analyzer | `002_returns_distribution_analyzer` | ⬜ Planned |
| 3 | Rolling statistics dashboard | `003_rolling_statistics_dashboard` | ⬜ Planned |
| 4 | Correlation & covariance explorer | `004_correlation_covariance_explorer` | ⬜ Planned |
| 5 | Moving-average crossover signal generator | `005_moving_average_crossover_signal_generator` | ⬜ Planned |
| 6 | Risk metrics calculator | `006_risk_metrics_calculator` | ⬜ Planned |
| 7 | Tick-data storage pipeline | `007_tick_data_storage_pipeline` | ⬜ Planned |
| 8 | Fundamental + technical stock screener | `008_fundamental_technical_stock_screener` | ⬜ Planned |
| 9 | Seasonality analyzer | `009_seasonality_analyzer` | ⬜ Planned |
| 10 | Benchmark & beta tool | `010_benchmark_beta_tool` | ⬜ Planned |

### Phase 2 — Backtesting & Basic Strategies

| # | Project | Folder | Status |
|---|---------|--------|--------|
| 11 | Vectorized backtester from scratch | `011_vectorized_backtester_from_scratch` | ⬜ Planned |
| 12 | Event-driven backtester | `012_event_driven_backtester` | ⬜ Planned |
| 13 | Transaction cost & slippage model | `013_transaction_cost_slippage_model` | ⬜ Planned |
| 14 | Time-series momentum strategy | `014_time_series_momentum_strategy` | ⬜ Planned |
| 15 | Mean-reversion strategy | `015_mean_reversion_strategy` | ⬜ Planned |
| 16 | Basic pairs trade | `016_basic_pairs_trade` | ⬜ Planned |
| 17 | Walk-forward analysis framework | `017_walk_forward_analysis_framework` | ⬜ Planned |
| 18 | Parameter sweep + robustness heatmap | `018_parameter_sweep_robustness_heatmap` | ⬜ Planned |
| 19 | Monte Carlo backtest validation | `019_monte_carlo_backtest_validation` | ⬜ Planned |
| 20 | Multi-asset rebalancing backtester | `020_multi_asset_rebalancing_backtester` | ⬜ Planned |

### Phase 3 — Portfolio Construction & Risk

| # | Project | Folder | Status |
|---|---------|--------|--------|
| 21 | Markowitz mean-variance optimizer | `021_markowitz_mean_variance_optimizer` | ⬜ Planned |
| 22 | Risk parity portfolio | `022_risk_parity_portfolio` | ⬜ Planned |
| 23 | Black-Litterman model | `023_black_litterman_model` | ⬜ Planned |
| 24 | Kelly criterion sizing | `024_kelly_criterion_sizing` | ⬜ Planned |
| 25 | CVaR / Expected Shortfall optimizer | `025_cvar_expected_shortfall_optimizer` | ⬜ Planned |
| 26 | Ledoit-Wolf shrinkage covariance | `026_ledoit_wolf_shrinkage_covariance` | ⬜ Planned |
| 27 | Hierarchical Risk Parity (HRP) | `027_hierarchical_risk_parity_hrp` | ⬜ Planned |
| 28 | Factor risk decomposition | `028_factor_risk_decomposition` | ⬜ Planned |
| 29 | Stress testing & scenario engine | `029_stress_testing_scenario_engine` | ⬜ Planned |
| 30 | Cost-aware dynamic rebalancing | `030_cost_aware_dynamic_rebalancing` | ⬜ Planned |

### Phase 4 — Time Series & Econometrics

| # | Project | Folder | Status |
|---|---------|--------|--------|
| 31 | ARIMA forecaster | `031_arima_forecaster` | ⬜ Planned |
| 32 | GARCH volatility model | `032_garch_volatility_model` | ⬜ Planned |
| 33 | Vector Autoregression (VAR) | `033_vector_autoregression_var` | ⬜ Planned |
| 34 | Kalman-filtered dynamic hedge ratio | `034_kalman_filtered_dynamic_hedge_ratio` | ⬜ Planned |
| 35 | Johansen cointegration & VECM | `035_johansen_cointegration_vecm` | ⬜ Planned |
| 36 | HMM regime detection | `036_hmm_regime_detection` | ⬜ Planned |
| 37 | Ornstein-Uhlenbeck spread model | `037_ornstein_uhlenbeck_spread_model` | ⬜ Planned |
| 38 | Fractional differentiation | `038_fractional_differentiation` | ⬜ Planned |
| 39 | Spectral analysis (Fourier/wavelet) | `039_spectral_analysis_fourier_wavelet` | ⬜ Planned |
| 40 | Change-point detection | `040_change_point_detection` | ⬜ Planned |

### Phase 5 — Derivatives Pricing & Volatility

| # | Project | Folder | Status |
|---|---------|--------|--------|
| 41 | Black-Scholes pricer + Greeks | `041_black_scholes_pricer_greeks` | ⬜ Planned |
| 42 | Binomial/trinomial tree pricer | `042_binomial_trinomial_tree_pricer` | ⬜ Planned |
| 43 | Monte Carlo option pricer | `043_monte_carlo_option_pricer` | ⬜ Planned |
| 44 | Implied volatility solver & surface | `044_implied_volatility_solver_surface` | ⬜ Planned |
| 45 | Vol smile/skew analyzer | `045_vol_smile_skew_analyzer` | ⬜ Planned |
| 46 | Local volatility (Dupire) model | `046_local_volatility_dupire_model` | ⬜ Planned |
| 47 | Heston stochastic volatility model | `047_heston_stochastic_volatility_model` | ⬜ Planned |
| 48 | Delta-hedging simulator | `048_delta_hedging_simulator` | ⬜ Planned |
| 49 | Variance swap & VIX replication | `049_variance_swap_vix_replication` | ⬜ Planned |
| 50 | Exotics & structured-product pricer | `050_exotics_structured_product_pricer` | ⬜ Planned |

### Phase 6 — Market Microstructure & Execution

| # | Project | Folder | Status |
|---|---------|--------|--------|
| 51 | Limit order book reconstructor | `051_limit_order_book_reconstructor` | ⬜ Planned |
| 52 | Order-book imbalance signal | `052_order_book_imbalance_signal` | ⬜ Planned |
| 53 | VWAP/TWAP execution algos | `053_vwap_twap_execution_algos` | ⬜ Planned |
| 54 | Almgren-Chriss optimal execution | `054_almgren_chriss_optimal_execution` | ⬜ Planned |
| 55 | Market impact model | `055_market_impact_model` | ⬜ Planned |
| 56 | Liquidity & spread analytics | `056_liquidity_spread_analytics` | ⬜ Planned |
| 57 | High-frequency data pipeline | `057_high_frequency_data_pipeline` | ⬜ Planned |
| 58 | Tick-by-tick backtester | `058_tick_by_tick_backtester` | ⬜ Planned |
| 59 | Queue-position & fill-probability model | `059_queue_position_fill_probability_model` | ⬜ Planned |
| 60 | Order-flow toxicity (VPIN) | `060_order_flow_toxicity_vpin` | ⬜ Planned |

### Phase 7 — Statistical Arbitrage & Factor Investing

| # | Project | Folder | Status |
|---|---------|--------|--------|
| 61 | Cross-sectional momentum factor | `061_cross_sectional_momentum_factor` | ⬜ Planned |
| 62 | Fama-French factor replication | `062_fama_french_factor_replication` | ⬜ Planned |
| 63 | Multi-factor model with neutralization | `063_multi_factor_model_with_neutralization` | ⬜ Planned |
| 64 | PCA statistical arbitrage | `064_pca_statistical_arbitrage` | ⬜ Planned |
| 65 | Index / ETF-vs-constituents arbitrage | `065_index_etf_vs_constituents_arbitrage` | ⬜ Planned |
| 66 | Cointegrated basket trading | `066_cointegrated_basket_trading` | ⬜ Planned |
| 67 | Alpha combination engine | `067_alpha_combination_engine` | ⬜ Planned |
| 68 | Factor timing model | `068_factor_timing_model` | ⬜ Planned |
| 69 | Cross-asset carry strategy | `069_cross_asset_carry_strategy` | ⬜ Planned |
| 70 | Meta-portfolio of strategies | `070_meta_portfolio_of_strategies` | ⬜ Planned |

### Phase 8 — Machine Learning for Alpha

| # | Project | Folder | Status |
|---|---------|--------|--------|
| 71 | Financial ML feature pipeline | `071_financial_ml_feature_pipeline` | ⬜ Planned |
| 72 | Triple-barrier labeling + meta-labeling | `072_triple_barrier_labeling_meta_labeling` | ⬜ Planned |
| 73 | Purged & embargoed cross-validation | `073_purged_embargoed_cross_validation` | ⬜ Planned |
| 74 | Gradient-boosted return predictor | `074_gradient_boosted_return_predictor` | ⬜ Planned |
| 75 | Feature importance with SHAP | `075_feature_importance_with_shap` | ⬜ Planned |
| 76 | Directional classifier with calibration | `076_directional_classifier_with_calibration` | ⬜ Planned |
| 77 | ML regime classifier | `077_ml_regime_classifier` | ⬜ Planned |
| 78 | NLP sentiment from news & filings | `078_nlp_sentiment_from_news_filings` | ⬜ Planned |
| 79 | Alternative-data signal | `079_alternative_data_signal` | ⬜ Planned |
| 80 | Ensemble & stacking of alpha models | `080_ensemble_stacking_of_alpha_models` | ⬜ Planned |

### Phase 9 — Deep Learning & Reinforcement Learning

| # | Project | Folder | Status |
|---|---------|--------|--------|
| 81 | LSTM/GRU forecaster | `081_lstm_gru_forecaster` | ⬜ Planned |
| 82 | Temporal Convolutional Network (TCN) | `082_temporal_convolutional_network_tcn` | ⬜ Planned |
| 83 | Transformer for financial time series | `083_transformer_for_financial_time_series` | ⬜ Planned |
| 84 | Autoencoder for latent factors & anomalies | `084_autoencoder_for_latent_factors_anomalies` | ⬜ Planned |
| 85 | End-to-end deep portfolio optimization | `085_end_to_end_deep_portfolio_optimization` | ⬜ Planned |
| 86 | DQN trading agent | `086_dqn_trading_agent` | ⬜ Planned |
| 87 | PPO execution agent | `087_ppo_execution_agent` | ⬜ Planned |
| 88 | Multi-agent market simulator | `088_multi_agent_market_simulator` | ⬜ Planned |
| 89 | Generative synthetic market data | `089_generative_synthetic_market_data` | ⬜ Planned |
| 90 | Deep hedging | `090_deep_hedging` | ⬜ Planned |

### Phase 10 — Cutting-Edge: Agentic & Frontier Systems

| # | Project | Folder | Status |
|---|---------|--------|--------|
| 91 | LLM alpha-research assistant | `091_llm_alpha_research_assistant` | ⬜ Planned |
| 92 | Agentic backtesting loop | `092_agentic_backtesting_loop` | ⬜ Planned |
| 93 | LLM-powered macro nowcasting | `093_llm_powered_macro_nowcasting` | ⬜ Planned |
| 94 | Multi-agent "trading firm" simulation | `094_multi_agent_trading_firm_simulation` | ⬜ Planned |
| 95 | Large-scale document intelligence | `095_large_scale_document_intelligence` | ⬜ Planned |
| 96 | RL execution with realistic market impact | `096_rl_execution_with_realistic_market_impact` | ⬜ Planned |
| 97 | Causal inference for alpha | `097_causal_inference_for_alpha` | ⬜ Planned |
| 98 | Online / continual-learning system | `098_online_continual_learning_system` | ⬜ Planned |
| 99 | End-to-end production quant platform | `099_end_to_end_production_quant_platform` | ⬜ Planned |
| 100 | Autonomous agentic hedge fund (capstone) | `100_autonomous_agentic_hedge_fund_capstone` | ⬜ Planned |

---

## Adding the next project (iterative)

Until a scaffolding generator is added (deferred until a few projects exist), create the next
project by hand following Project 1 as the template:

1. `mkdir NNN_<slug>` at the repo root (slug from the table above).
2. Copy Project 1's `pyproject.toml` shape: `[tool.uv] package = false`, the
   `quant-core[...]>=0.1,<0.2` pin, and the `[tool.uv.sources]` editable path to `../quant_core`.
   Add only this project's unique deps. For heavy deps that need a custom index (e.g. torch),
   declare `[[tool.uv.index]]` + `[tool.uv.sources]` **in that project** — index config is not
   inherited from `quant_core`.
3. Add `main.py`, `tests/`, `README.md`. Put reusable logic in `quant_core`, not the project.
4. `cd NNN_<slug> && uv sync && uv run pytest`; flip its row to ✅ above.

## License

[MIT](LICENSE).
