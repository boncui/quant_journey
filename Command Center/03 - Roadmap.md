From first pip install to an autonomous agentic trading system  
Built around your stack — Python, CS + Math fundamentals, ML/AI, and agentic systems (Claude Code overnight loops, the Kaizen research lab). The arc is deliberate: each phase assumes the one before it. Phases 1–3 are genuinely entry-level but you'll move through them fast given your background. Phases 8–10 are where your AI/agentic edge becomes the differentiator that most quants don't have.  
How to use this  
•    Treat each project as ship something runnable, not read about it. A project isn't done until it produces a number, a chart, or a P&L curve.  
•    Re-use code across projects. By Phase 4 you should have your own mini-library (data loader, backtester, metrics module). That compounding is the real point.  
•    Don't skip the "boring" risk/validation projects (17, 19, 73). The single thing separating real quants from backtest-overfitters is rigor about look-ahead bias and out-of-sample testing.  
Core toolkit you'll accumulate: pandas, numpy, scipy, statsmodels, scikit-learn, cvxpy (optimization), arch (GARCH), vectorbt / custom backtester, PyTorch, gymnasium (RL), polars/duckdb (for HF data), plus data sources (yfinance → Polygon/Databento → tick data).  
Reference shelf: Marcos López de Prado, Advances in Financial Machine Learning; Ernie Chan, Quantitative Trading + Algorithmic Trading; Stefan Jansen, ML for Algorithmic Trading; Cartea/Jaimungal/Penalva, Algorithmic and High-Frequency Trading; Hull, Options, Futures and Other Derivatives.

---

Phase 1 — Foundations: Data, Stats & Tooling  
Entry level. The goal is fluency with financial data and the metrics everyone takes for granted.  
1    Market data downloader & cleaner — Pull OHLCV from yfinance/Polygon for a universe of tickers; handle missing data, splits, and dividend adjustments. Learn: data ingestion, corporate actions, why "adjusted close" matters.  
2    Returns & distribution analyzer — Compute simple vs log returns; plot histograms; fit Normal and compare to the fat-tailed reality. Learn: return conventions, skew/kurtosis, why finance breaks Gaussian assumptions.  
3    Rolling statistics dashboard — Rolling mean, volatility, and Sharpe over configurable windows. Learn: rolling windows, annualization, the Sharpe ratio from first principles.  
4    Correlation & covariance explorer — Heatmaps across an asset universe; watch correlations spike in crashes. Learn: covariance vs correlation, instability of estimates.  
5    Moving-average crossover signal generator — Produce buy/sell signals only (no backtest yet). Learn: technical indicators, clean signal generation.  
6    Risk metrics calculator — Max drawdown, Calmar, Sortino, historical VaR. Learn: the metrics that actually get reported to investors.  
7    Tick-data storage pipeline — Load market data into SQLite/DuckDB/Postgres and query it efficiently. Learn: time-series storage, indexing — plays directly to your data-eng strength.  
8    Fundamental + technical stock screener — Filter a universe by P/E, momentum, volatility, etc. Learn: cross-sectional filtering.  
9    Seasonality analyzer — Day-of-week, turn-of-month, month-of-year effects. Learn: calendar anomalies, groupby analysis, multiple-testing skepticism.  
10    Benchmark & beta tool — Regress an asset on SPY for alpha/beta via OLS. Learn: CAPM intuition, your first regression.  
Phase 2 — Backtesting & Basic Strategies  
Where most people lie to themselves. Build the machinery to avoid it.  
11    Vectorized backtester from scratch — Pure pandas, no libraries. Learn: backtest mechanics, and exactly where look-ahead bias sneaks in.  
12    Event-driven backtester — Proper order → fill simulation with an event loop. Learn: realistic execution, decoupling signal from fill.  
13    Transaction cost & slippage model — Add commissions, spread, and slippage to #12. Learn: why a beautiful gross backtest dies net of costs.  
14    Time-series momentum strategy — Trend-following across assets. Learn: the momentum factor, the oldest free lunch.  
15    Mean-reversion strategy — Bollinger/z-score entries and exits. Learn: reversion dynamics, when it works vs blows up.  
16    Basic pairs trade — Test two stocks for cointegration, trade the spread. Learn: Engle-Granger cointegration.  
17    Walk-forward analysis framework — Rolling train/test windows. Learn: out-of-sample discipline — the antidote to overfitting.  
18    Parameter sweep + robustness heatmap — Grid-search params and look for plateaus, not peaks. Learn: parameter sensitivity, fragility detection.  
19    Monte Carlo backtest validation — Bootstrap/shuffle returns to test if your edge beats luck. Learn: statistical significance of a backtest, deflated Sharpe.  
20    Multi-asset rebalancing backtester — Portfolio weights and periodic rebalancing. Learn: portfolio-level (not single-asset) backtesting.  
Phase 3 — Portfolio Construction & Risk  
From "a strategy" to "a portfolio." Optimization meets reality.  
21    Markowitz mean-variance optimizer — Trace the efficient frontier with cvxpy. Learn: MPT, quadratic programming.  
22    Risk parity portfolio — Equalize each asset's risk contribution. Learn: risk budgeting beyond dollar weights.  
23    Black-Litterman model — Blend market equilibrium with your own views. Learn: Bayesian allocation, taming optimizer instability.  
24    Kelly criterion sizing — Growth-optimal bet sizing, plus fractional Kelly. Learn: position sizing, geometric vs arithmetic growth.  
25    CVaR / Expected Shortfall optimizer — Optimize against tail loss, not variance. Learn: coherent risk measures.  
26    Ledoit-Wolf shrinkage covariance — Robustify the noisy covariance matrix. Learn: estimation error, shrinkage.  
27    Hierarchical Risk Parity (HRP) — López de Prado's clustering-based allocation. Learn: ML-meets-portfolio, no matrix inversion needed.  
28    Factor risk decomposition — Attribute portfolio risk to underlying factors. Learn: risk attribution.  
29    Stress testing & scenario engine — Replay 2008/2020 and hypothetical shocks. Learn: scenario analysis, fat-tail planning.  
30    Cost-aware dynamic rebalancing — Solve for the no-trade region. Learn: rebalancing as an optimization, not a calendar.  
Phase 4 — Time Series & Econometrics  
The classical statistical core. Build your own mini-library here.  
31    ARIMA forecaster — Stationarity testing, ACF/PACF, order selection. Learn: the Box-Jenkins workflow, and ARIMA's limits on returns.  
32    GARCH volatility model — Capture volatility clustering and forecast vol. Learn: the GARCH family — vol is far more predictable than returns.  
33    Vector Autoregression (VAR) — Multivariate dynamics + Granger causality. Learn: lead-lag relationships.  
34    Kalman-filtered dynamic hedge ratio — Adaptive beta for pairs trading. Learn: state-space models, online estimation.  
35    Johansen cointegration & VECM — Multi-asset cointegrated baskets. Learn: cointegration beyond two assets.  
36    HMM regime detection — Infer bull/bear/crisis regimes. Learn: hidden Markov models, regime switching.  
37    Ornstein-Uhlenbeck spread model — Fit mean-reversion speed and half-life. Learn: continuous-time stochastic processes.  
38    Fractional differentiation — Make a series stationary while keeping memory. Learn: López de Prado's stationarity-vs-memory tradeoff.  
39    Spectral analysis (Fourier/wavelet) — Hunt for cycles in price series. Learn: frequency-domain thinking (and its overfitting traps).  
40    Change-point detection — Find structural breaks. Learn: CUSUM, Bayesian change-point — regime shifts in real time.  
Phase 5 — Derivatives Pricing & Volatility  
Options force precision. Mispricing here is your edge.  
41    Black-Scholes pricer + Greeks — Price and compute delta/gamma/vega/theta/rho. Learn: BSM, the Greeks as risk sensitivities.  
42    Binomial/trinomial tree pricer — Handle American early exercise. Learn: lattice methods.  
43    Monte Carlo option pricer — Asian/barrier path-dependent payoffs + variance reduction. Learn: MC for derivatives, antithetic/control variates.  
44    Implied volatility solver & surface — Newton-Raphson IV across strikes/expiries. Learn: IV inversion, building a vol surface.  
45    Vol smile/skew analyzer — Risk reversals, butterflies, term structure. Learn: what the smile tells you about market fear.  
46    Local volatility (Dupire) model — Calibrate to the full surface. Learn: local vol calibration.  
47    Heston stochastic volatility model — Price with stochastic vol via characteristic functions. Learn: stochastic vol, semi-analytic pricing.  
48    Delta-hedging simulator — Replicate an option dynamically, track hedging P&L. Learn: dynamic hedging, gamma/theta bleed.  
49    Variance swap & VIX replication — Model-free implied variance. Learn: how VIX is actually constructed.  
50    Exotics & structured-product pricer — Autocallables, knock-outs, etc. Learn: payoff engineering, where banks make margin.  
Phase 6 — Market Microstructure & Execution  
The world below the daily bar. Latency and the order book become the game.  
51    Limit order book reconstructor — Rebuild the LOB from message data. Learn: order types, book mechanics.  
52    Order-book imbalance signal — Predict next-tick direction from book pressure. Learn: your first true microstructure alpha.  
53    VWAP/TWAP execution algos — Schedule child orders against a benchmark. Learn: execution benchmarks.  
54    Almgren-Chriss optimal execution — Trade off market impact vs timing risk. Learn: the canonical execution model.  
55    Market impact model — Estimate temporary vs permanent impact empirically. Learn: impact functions, the square-root law.  
56    Liquidity & spread analytics — Effective spread, Kyle's lambda, depth. Learn: quantifying liquidity.  
57    High-frequency data pipeline — Nanosecond timestamps, GB-scale data with polars/duckdb. Learn: HF data engineering — squarely your strength.  
58    Tick-by-tick backtester — Simulate fills with latency. Learn: HF backtesting, the latency assumption that makes or breaks results.  
59    Queue-position & fill-probability model — Will your resting order fill? Learn: queueing theory in markets.  
60    Order-flow toxicity (VPIN) — Detect adverse selection / informed flow. Learn: VPIN, flow toxicity, flash-crash precursors.  
Phase 7 — Statistical Arbitrage & Factor Investing  
Cross-sectional alpha. Many weak signals, combined well.  
61    Cross-sectional momentum factor — Rank a universe, go long/short the spread. Learn: cross-sectional (not time-series) factors.  
62    Fama-French factor replication — Build value, size, quality, momentum portfolios. Learn: the factor zoo, FF 3/5-factor models.  
63    Multi-factor model with neutralization — Combine factors, neutralize sector/beta exposure. Learn: Barra-style construction, hedging unwanted bets.  
64    PCA statistical arbitrage — Trade residuals off eigenportfolios. Learn: PCA stat arb, the Avellaneda-Lee approach.  
65    Index / ETF-vs-constituents arbitrage — Exploit the basket-vs-parts relationship. Learn: arbitrage relationships, creation/redemption.  
66    Cointegrated basket trading — Multi-leg mean reversion. Learn: scaling pairs trading to baskets.  
67    Alpha combination engine — Blend many weak signals via Information Coefficient weighting. Learn: signal weighting, IC, breadth (the Fundamental Law).  
68    Factor timing model — Decide when to lever which factor. Learn: factor rotation, regime-conditioned exposure.  
69    Cross-asset carry strategy — FX, commodity, and bond carry together. Learn: the carry factor across asset classes.  
70    Meta-portfolio of strategies — Allocate capital across your uncorrelated strats from earlier phases. Learn: strategy-level diversification — the real source of a smooth equity curve.  
Phase 8 — Machine Learning for Alpha  
Where your CS/ML background starts to pull ahead. The danger is leakage — respect it.  
71    Financial ML feature pipeline — Engineer technical/fundamental/alt features with strict point-in-time correctness. Learn: feature engineering, the cardinal sin of look-ahead leakage.  
72    Triple-barrier labeling + meta-labeling — Label by which barrier (profit/stop/time) hits first. Learn: López de Prado's labeling, separating "what" from "when."  
73    Purged & embargoed cross-validation — CV that doesn't leak across overlapping samples. Learn: the single most under-appreciated technique in financial ML.  
74    Gradient-boosted return predictor — XGBoost/LightGBM on your features. Learn: tree ensembles, why they beat deep nets on tabular financial data.  
75    Feature importance with SHAP — MDI/MDA/SHAP attribution + selection. Learn: interpretability, killing spurious features.  
76    Directional classifier with calibration — Predict up/down and trustworthy probabilities. Learn: classification framing, probability calibration, sizing by confidence.  
77    ML regime classifier — Supervised regime detection feeding allocation. Learn: regimes as features, not just labels.  
78    NLP sentiment from news & filings — Score text → signal. Learn: text-as-alpha, the basic sentiment pipeline.  
79    Alternative-data signal — Build a pipeline from satellite/credit-card/web-traffic data to a tradable signal. Learn: alt-data sourcing, signal extraction, decay.  
80    Ensemble & stacking of alpha models — Combine diverse learners robustly. Learn: stacking, out-of-fold predictions, model diversity.  
Phase 9 — Deep Learning & Reinforcement Learning  
Modern architectures applied to the hardest signal-to-noise problem there is.  
81    LSTM/GRU forecaster — Sequence model on returns/vol. Learn: recurrent nets — and a hard lesson in how easily DL overfits noisy markets.  
82    Temporal Convolutional Network (TCN) — Dilated convolutions for long memory. Learn: TCNs as a strong RNN alternative.  
83    Transformer for financial time series — Attention-based forecasting (Informer/Autoformer ideas). Learn: attention for sequences, long-horizon forecasting.  
84    Autoencoder for latent factors & anomalies — Compress the cross-section, flag regime breaks. Learn: representation learning, unsupervised factors.  
85    End-to-end deep portfolio optimization — Differentiable layers that optimize Sharpe directly. Learn: skipping the predict-then-optimize two-step.  
86    DQN trading agent — Single-asset RL with careful reward design. Learn: MDP framing, Q-learning, why naive rewards game themselves.  
87    PPO execution agent — Continuous-control RL for optimal execution. Learn: policy gradients, RL where the objective is genuinely well-posed.  
88    Multi-agent market simulator — Interacting agents producing emergent price dynamics. Learn: agent-based modeling, multi-agent RL.  
89    Generative synthetic market data — GAN/diffusion paths to stress-test and augment backtests. Learn: generative models, escaping the single-history problem.  
90    Deep hedging — Neural hedging under frictions and discrete time (Buehler et al.). Learn: model-free hedging that beats Black-Scholes deltas under real costs.  
Phase 10 — Cutting-Edge: Agentic & Frontier Systems  
Your actual edge. Most quants can't build this; you already run overnight agentic loops and a research lab. This phase turns that into a quant moat.  
91    LLM alpha-research assistant — An agent that reads papers/filings and proposes testable hypotheses for you to vet. Learn: LLM agents as research multipliers — the front of your funnel.  
92    Agentic backtesting loop — An autonomous agent that generates → backtests → critiques → iterates strategies overnight (your Claude Code + tmux setup, pointed at alpha). Learn: closed-loop autonomous research — with hard guardrails against overfitting-by-search.  
93    LLM-powered macro nowcasting — Structured extraction from unstructured releases → real-time macro state. Learn: nowcasting, turning text/data firehoses into features.  
94    Multi-agent "trading firm" simulation — Researcher, PM, risk, and execution agents collaborating with role specialization. Learn: agent orchestration, separation of concerns as a research architecture.  
95    Large-scale document intelligence — LLM analysis of every 10-K/earnings call in a universe: guidance, tone, risk-factor deltas → signal. Learn: document intelligence at scale, longitudinal text signals.  
96    RL execution with realistic market impact — Train against an impact-aware simulator and tackle the sim-to-real gap. Learn: closing the loop between Phases 6 and 9 — the hard part of deployable RL.  
97    Causal inference for alpha — Instrumental variables and causal discovery to separate real drivers from correlation. Learn: causal ML, robustness to regime change — why most ML "alpha" decays.  
98    Online / continual-learning system — A model that adapts to drift in real time without catastrophic forgetting. Learn: concept drift, online learning, non-stationarity head-on.  
99    End-to-end production quant platform — Data → research → backtest → paper-trade → live monitoring, fully automated, with MLOps and risk kill-switches. Learn: production quant engineering — exactly where your full-stack + infra background compounds.  
100    Autonomous agentic hedge fund (capstone) — A self-improving system where agents discover signals, build and risk-manage strategies, execute, and learn from outcomes. The Kaizen research lab, realized in markets. Learn: integrating all 99 prior projects — the genuine frontier of agentic quant.

Pacing & sequencing notes  
•    Phases 1–3 (≈ weeks): With your background, this is review-by-doing. Build the reusable library; don't linger.  
•    Phases 4–7 (≈ months): The real classical-quant curriculum. This is where you'd be competitive for a quant role.  
•    Phases 8–10 (open-ended): Your differentiation. Phase 10 in particular is research, not coursework — projects here can become Kaizen output, blog posts, or the seed of something fundable.  
•    Reality check: No strategy here is assumed to be profitable live. Edges decay, costs are brutal, and markets adapt. The skill being built is the process — rigorous research that knows the difference between a real edge and an overfit one. That discipline is the transferable asset, whether you end up at a fund, building agentic infra, or running Kaizen.