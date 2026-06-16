# 01 \- Introduction

PROJECT ALPHA → QAIZEN: AI QUANT FIRM

Carlton King & David Cui  
Started 6/09/2026 · last restructured 2026-06-15

THESIS  
Can LLMs and agents replace traditional quant firms?  
That question is the entire point. It is the thing being tested — not assumed. The end-goal is Qaizen, a full AI-integrated quant firm. But we get there in two stages, and stage 2 only begins when the evidence earns it.

THE TWO STAGES  
1\. Learn — build the skills, the tooling, and the rigor through a focused set of projects, and gather honest evidence on whether an agent-driven research process can find real edge.  
2\. Build Qaizen — form the firm, but only when the go/no-go bar comes back YES and we've decided what to actually build (asset class \+ frequency \+ the role agents play).

Honest baseline: Carlton is early-undergrad (NYU CS+Math, grad 2029), strong but not yet a seasoned quant-dev. The plan is paced against that truth, not against a fantasy version. The transferable asset is the process — research that knows the difference between a real edge and an overfit one — whether or not Qaizen ships.

THE VAULT (read in order)  
\- 01 \- Introduction: This page — thesis, stages, index  
\- 02 \- Overview: The knowledge map — five pillars to learn, tagged critical-path vs depth  
\- 03 \- Roadmap: The plan — recalibrated phases, the \~26-project critical path, real pacing  
\- 04 \- Projects: Live status ledger — what's shipped, who owns it, the gate projects  
\- 05 \- Go-No-Go: The pre-registered success bar that decides go/no-go on the thesis  
\- 06 \- Build Stage (Deferred): Firm-formation items, parked until the trigger fires

HOW TO USE THIS  
\- A project isn't done until it produces a number, a chart, or a P\&L. Course → project, or it didn't happen.  
\- Build a reusable core/ library; the compounding across projects is the real point.  
\- Don't skip the rigor projects (cost model, walk-forward, Monte Carlo, purged CV). They are what keep us honest.  
\- Carlton owns the critical path; David contributes in parallel (his startup comes first). Equity is deferred to formation — see 06 \- Build Stage (Deferred).

# 02 \- Overview

OVERVIEW — THE KNOWLEDGE MAP

The five pillars to learn for Qaizen. This isn't a generic quant syllabus — it's tagged to our plan.

Legend: CP \= on the critical path (needed to reach the go/no-go decision). D \= depth pool (pulled in only if the D2 decision points there).

Running thread — Research Rigor. It is not a separate pillar; it cuts across Statistics, ML, and CS. It is the actual edge over a backtest-overfitter, and the heart of 05 \- Go-No-Go: multiple-testing awareness, deflated metrics, out-of-sample discipline, and point-in-time correctness. Wherever you see rigor below, it is load-bearing.

1 — MATHEMATICS  
\- (CP) Linear Algebra — matrix operations, eigenvalues, PCA, factor models, covariance matrices  
\- (CP) Probability Theory — distributions, expectations, conditional probability, Bayes  
\- (CP) Calculus — derivatives, partial derivatives, chain rule (foundation for optimization/gradients)  
\- (CP) Optimization — convex optimization, quadratic programming, gradient descent  
\- (CP) Information Theory — entropy, mutual information, the Information Coefficient (drives alpha combination \#67)  
\- (D) Stochastic Calculus — Itô's lemma, Brownian motion, martingales (derivatives, Phase 5\)  
\- (D) Numerical methods & matrix conditioning — stability of covariance inversion / optimizers

2 — STATISTICS, ECONOMETRICS & RESEARCH RIGOR  
\- (CP) Statistics — hypothesis testing, p-values, confidence intervals  
\- (CP) Multiple-hypothesis testing & FDR — deflated Sharpe, penalizing for search breadth (the rigor centerpiece — gate \#19)  
\- (CP) Out-of-sample discipline — walk-forward (\#17), purged & embargoed cross-validation (\#73), point-in-time correctness (\#71). The single most under-appreciated skill in financial ML.  
\- (CP) Econometrics — regression, heteroscedasticity, autocorrelation  
\- (CP) Time Series — stationarity testing (CP); ARIMA, GARCH, cointegration (depth beyond stationarity)  
\- (D) Bayesian inference — beyond Bayes' rule: Black-Litterman, regime models  
\- (D) Extreme Value Theory — fat tails, tail risk behind VaR/CVaR

3 — MACHINE LEARNING  
\- (CP) Supervised Learning — regression, classification, tree ensembles / gradient boosting (beat deep nets on tabular financial data, \#74)  
\- (CP) Statistical Learning Theory — bias-variance, overfitting, cross-validation  
\- (CP) Feature Engineering — with strict point-in-time correctness (\#71); the cardinal sin is look-ahead leakage  
\- (CP) Labeling — triple-barrier & meta-labeling (\#72): separating "what" from "when"  
\- (D) Model interpretability — SHAP, MDI/MDA feature importance (\#75), killing spurious features  
\- (D) Probability calibration — trustworthy up/down probabilities for sizing (\#76)  
\- (D) Unsupervised Learning — clustering, dimensionality reduction, PCA (PCA stat-arb \#64)  
\- (D) Ensembling & stacking — out-of-fold predictions, model diversity (\#80)  
\- (D) Deep sequence models — RNN/LSTM, TCN, transformers for time series (Phase 9\)  
\- (D) Reinforcement Learning — Q-learning, policy gradients, bandits (Phase 9 execution/agents)  
\- (D) Causal inference for alpha — IV, causal discovery: separating real drivers from correlation (\#97)

4 — COMPUTER SCIENCE & DATA ENGINEERING  
\- (CP) Programming — Python primary (the whole toolkit is Python); C++/Rust deferred to low-latency only  
\- (CP) Data Structures & Algorithms — arrays, hash maps, trees, heaps; sorting, searching, sliding window, DP  
\- (CP) Data Engineering — columnar storage, DuckDB/Parquet, time-series databases, point-in-time data layout (\#7 — Carlton's strength)  
\- (CP) Software Engineering practice — Git, the monorepo, testing, CI, reproducibility (the protected core/ library lives or dies on this)  
\- (D) Low-Latency Systems — kernel bypass, shared memory, CPU caching (Phase 6, only if going HF)  
\- (D) Networking — UDP multicast, TCP, socket programming  
\- (D) Parallel Computing — multithreading, GPU acceleration, SIMD  
\- (D) MLOps / production — model serving, monitoring, risk kill-switches (\#99, build stage)

5 — AI & AGENTIC SYSTEMS (the differentiator — this is the thesis)  
\- (CP) LLM fundamentals — prompting, context windows, tokenization, embeddings  
\- (CP) Agent architectures — tool use, planning, multi-step generate→test→iterate loops (\#91, \#92)  
\- (CP) Eval harnesses & guardrails — scoring agent output honestly, defending against overfitting-by-search (wires directly into 05 \- Go-No-Go)  
\- (CP) LLM-driven research workflows — autonomous hypothesis generation; the Kaizen overnight loop  
\- (D) Multi-agent orchestration — researcher / PM / risk / execution role specialization (\#94)  
\- (D) RAG & document intelligence — 10-Ks, earnings calls, filings → signal (\#95)  
\- (D) Cost & latency engineering for LLM systems — token budgets, caching, model routing

6 — FINANCE & MARKETS  
\- (CP) Portfolio Theory — mean-variance optimization, Sharpe ratio, Kelly criterion  
\- (CP) Risk Management — VaR, CVaR, stress testing, factor models  
\- (CP) Factor investing & statistical arbitrage — cross-sectional factors, IC, neutralization (Phase 7 core: \#61, \#67)  
\- (CP) Transaction Cost Analysis & execution — spread, slippage, market impact (gate \#13)  
\- (CP) Asset-class landscape — equities / FX / futures / crypto / options / fixed income (needed to choose in the D2 decision; depth per class deferred)  
\- (CP) Market Microstructure basics — order books, bid-ask spread, slippage, liquidity (cost intuition; HF depth is D)  
\- (D) Derivatives Pricing — Black-Scholes, Greeks, volatility surfaces (Phase 5\)  
\- (D) Accounting & Corporate Finance — fundamental data, P\&L, balance sheets  
\- (D) Regulatory & Compliance — RIA/CPO registration, Reg SCI, MiFID II, short-sale rules (relevant at 06 \- Build Stage)

Each pillar maps onto 03 \- Roadmap phases; the CP items are exactly what the \~26 critical-path projects in 04 \- Projects build. Learn D depth only when the decision points there.

# 03 \- Roadmap

ROADMAP

From first pip install to a decision about whether to build Qaizen.

HOW TO READ THIS (start here)  
This is a two-stage project. Stage 1 \= learn. Stage 2 \= build the firm — and Stage 2 does not begin until the evidence in 05 \- Go-No-Go says it can.

Honest baseline (this matters). Carlton is an early-undergrad NYU CS+Math student (grad 2029), strong trajectory and a fast builder, but the demonstrated baseline is early undergrad — not a seasoned quant-dev. So:  
\- Phases 1–3 are genuine first-time learning, not "review-by-doing." Expect weeks-to-months, not days. Do not pace against a version of yourself that doesn't exist yet.  
\- The agentic edge (Phase 10\) is a skill to build and a hypothesis to prove — not an asset you already own. The thesis ("can LLMs/agents do real quant work?") is the thing being tested, not assumed.  
\- Progress is measured against the truth, so the timeline doesn't lie to you.

What the learning stage must output (the whole point of Stage 1):  
1\. Asset class \+ frequency — e.g. equities-daily vs crypto-intraday vs options.  
2\. The role agents/LLMs actually play — research assistant vs full autonomous loop.  
3\. Go/no-go on the thesis, with evidence — see 05 \- Go-No-Go.

The rule that keeps it real: a project is done only when it produces a number, a chart, or a P\&L. A course module is not done until it produces a critical-path project artifact. Course → project, or it didn't happen.

THE CRITICAL PATH (do this) VS THE DEPTH POOL (maybe later)  
The original list below is 100 projects — that's a menu, not a route. Grinding all 100 before deciding anything violates the goal. So the work is cut to a \~26-project critical path — the minimum that reaches the three outputs above. Everything else is demoted to an Optional Depth Pool, pulled in only if the decision points there. The live tracker with owners/status is in 04 \- Projects.

Critical path at a glance:  
\- Phase 0 — Industry & Business Literacy (new; reading, runs in parallel with Phases 1–2)  
\- Phase 1 — Foundation library: 1, 2, 3, 4, 6, 7, 10  
\- Phase 2 — Rigor core: 11, 12, 13, 14, 15, 17, 19, 20  
\- Phase 7 — Thin stat-arb slice: 61, 67  
\- Phase 8 — Thin ML slice (leakage discipline): 71, 72, 73, 74  
\- Phase 10 — The thesis test: 91, 92  
\- Decision instruments: the pre-registered protocol (05 \- Go-No-Go) and the final D2 decision write-up

Gate projects — the four that make the go/no-go bar honest, never skip these: 13 (cost model), 17 (walk-forward), 19 (Monte Carlo / deflated Sharpe), 73 (purged CV).

PHASE 0 — INDUSTRY & BUSINESS LITERACY (new — parallel with Phases 1–2, reading not code)  
The original roadmap jumped straight to a Python data downloader and taught zero about how this industry actually works. But the learning-stage output is partly a business decision, and no amount of code teaches it. Run this as reading alongside Phases 1–2.  
Cover:  
\- Types of firms and how each makes money: prop shop, hedge fund, market maker, asset manager.  
\- Fee / payout structures: 2-and-20, prop splits, high-water marks.  
\- The path of a strategy: idea → capital → risk limits → P\&L.  
\- Org roles: researcher / PM / risk / execution / ops — this maps directly to the multi-agent firm idea (\#94).  
\- What the words mean in practice: AUM, drawdown limit, investor mandate, capacity.  
\- The regulatory floor: who has to register (RIA vs CPO/CTA), and why external money changes everything (see 06 \- Build Stage).  
Sources: Ernie Chan, Quantitative Trading (business-of-it chapters); Narang, Inside the Black Box; firm teardowns (Rentec / Two Sigma / Jane Street profiles).

PACING (grounded in real time budget)  
\- Carlton: \~20 hr/wk in summer, 5–10 hr/wk during semester. Owns the critical path / the core/ library.  
\- David: \~5–10 hr/wk, startup comes first → off the critical path, takes parallel non-blocking enrichment work (mostly drawn from the depth pool from Phase 3 on).  
\- Arc: \~2–3 years. Summers \= deep-build blocks (uninterrupted time for the heavy core). Semesters ride alongside the NYU math you're taking anyway (linear algebra, probability, stochastic calc, econometrics are the Phase 4–5 prerequisites — let coursework do double duty).

Concrete sequence (see 04 \- Projects for the table):  
\- Summer 2026 — Phase 0 (reading) \+ Phase 1 library \+ Phase 2 rigor core. Goal: a strategy can be run end-to-end and judged net-of-cost out-of-sample.  
\- Fall 2026 — Phase 7 thin slice (61, 67\) \+ Phase 8 leakage slice (71, 72, 73). Write the pre-registered 05 \- Go-No-Go protocol at the end of fall, before any agent loop runs.  
\- Winter 2026–27 \+ Spring 2027 — finish 74, then 91 → 92 (the thesis test), scored against the locked bar. End of Spring 2027: write the D2 decision.

Quarterly checkpoint (end-summer / end-fall / end-spring): "closer to go/no-go, or grinding for its own sake?" A critical-path project slipping 2 months gets cut or rescoped, not silently carried.

CORE TOOLKIT YOU'LL ACCUMULATE  
pandas, numpy, scipy, statsmodels, scikit-learn, cvxpy (optimization), arch (GARCH), a custom backtester (built, not vendored), PyTorch, gymnasium (RL), polars/duckdb (HF data). Data sources behind a provider-abstraction layer: LSEG (learning only, non-commercial — see 06 \- Build Stage) with free fallback (yfinance/Stooq/CCXT), local DuckDB/Parquet cache enforcing point-in-time.  
Reference shelf (just-in-time lookup, not front-to-back reads): Marcos López de Prado, Advances in Financial Machine Learning; Ernie Chan, Quantitative Trading \+ Algorithmic Trading; Stefan Jansen, ML for Algorithmic Trading; Cartea/Jaimungal/Penalva, Algorithmic and High-Frequency Trading; Hull, Options, Futures and Other Derivatives.

OPTIONAL DEPTH POOL — THE FULL 100 (pull in only if the decision points there)  
Nothing below is scheduled. Each is a conditional branch with an explicit trigger. If Phase 0 \+ early backtests point at intraday/HF → pull Phase 6\. If options/vol → pull Phase 5\. If cross-sectional equity stat-arb → pull the rest of Phase 7 \+ Phase 4 spread econometrics. Phase 9 deep/RL and the heavy Phase 10 systems (93–100) stay parked until 05 \- Go-No-Go returns YES. Portfolio construction (21–30) waits until there's at least 1 surviving strategy to allocate across. (CP) \= on the critical path.

Phase 1 — Foundations: Data, Stats & Tooling  
1 Market data downloader & cleaner (CP); 2 Returns & distribution analyzer (CP); 3 Rolling statistics dashboard (CP); 4 Correlation & covariance explorer (CP); 5 MA-crossover signal generator; 6 Risk metrics calculator (CP); 7 Tick/bar data storage pipeline (CP); 8 Fundamental+technical screener; 9 Seasonality analyzer; 10 Benchmark & beta tool, CAPM (CP)

Phase 2 — Backtesting & Basic Strategies  
11 Vectorized backtester (CP); 12 Event-driven backtester (CP); 13 Transaction cost & slippage model (CP, gate); 14 Time-series momentum (CP); 15 Mean-reversion (CP); 16 Basic pairs trade; 17 Walk-forward framework (CP, gate); 18 Parameter sweep \+ robustness heatmap; 19 Monte Carlo validation / deflated Sharpe (CP, gate); 20 Multi-asset rebalancing backtester (CP)

Phase 3 — Portfolio Construction & Risk  
21 Markowitz MV optimizer; 22 Risk parity; 23 Black-Litterman; 24 Kelly sizing; 25 CVaR/ES optimizer; 26 Ledoit-Wolf shrinkage; 27 Hierarchical Risk Parity; 28 Factor risk decomposition; 29 Stress testing & scenarios; 30 Cost-aware dynamic rebalancing

Phase 4 — Time Series & Econometrics  
31 ARIMA; 32 GARCH; 33 VAR \+ Granger; 34 Kalman dynamic hedge ratio; 35 Johansen / VECM; 36 HMM regime detection; 37 Ornstein-Uhlenbeck spread; 38 Fractional differentiation; 39 Spectral analysis; 40 Change-point detection

Phase 5 — Derivatives Pricing & Volatility  
41 Black-Scholes \+ Greeks; 42 Binomial/trinomial tree; 43 Monte Carlo option pricer; 44 Implied vol solver & surface; 45 Vol smile/skew; 46 Local vol (Dupire); 47 Heston; 48 Delta-hedging simulator; 49 Variance swap & VIX replication; 50 Exotics & structured products

Phase 6 — Market Microstructure & Execution  
51 LOB reconstructor; 52 Order-book imbalance signal; 53 VWAP/TWAP; 54 Almgren-Chriss; 55 Market impact model; 56 Liquidity & spread analytics; 57 HF data pipeline; 58 Tick-by-tick backtester; 59 Queue-position / fill-probability; 60 Order-flow toxicity (VPIN)

Phase 7 — Statistical Arbitrage & Factor Investing  
61 Cross-sectional momentum factor (CP); 62 Fama-French replication; 63 Multi-factor \+ neutralization; 64 PCA stat-arb; 65 Index/ETF-vs-constituents arb; 66 Cointegrated basket; 67 Alpha combination engine, IC (CP); 68 Factor timing; 69 Cross-asset carry; 70 Meta-portfolio of strategies

Phase 8 — Machine Learning for Alpha  
71 Financial ML feature pipeline, point-in-time (CP); 72 Triple-barrier \+ meta-labeling (CP); 73 Purged & embargoed CV (CP, gate); 74 Gradient-boosted return predictor (CP); 75 SHAP feature importance; 76 Directional classifier \+ calibration; 77 ML regime classifier; 78 NLP sentiment; 79 Alt-data signal; 80 Ensemble & stacking

Phase 9 — Deep Learning & Reinforcement Learning  
81 LSTM/GRU; 82 TCN; 83 Transformer for financial TS; 84 Autoencoder latent factors; 85 End-to-end deep portfolio opt; 86 DQN agent; 87 PPO execution agent; 88 Multi-agent market sim; 89 Generative synthetic data; 90 Deep hedging

Phase 10 — Cutting-Edge: Agentic & Frontier Systems  
91 LLM alpha-research assistant (CP); 92 Agentic backtesting loop (CP); 93 LLM macro nowcasting; 94 Multi-agent "trading firm" sim; 95 Large-scale document intelligence; 96 RL execution w/ market impact; 97 Causal inference for alpha; 98 Online/continual learning; 99 End-to-end production platform; 100 Autonomous agentic hedge fund (capstone — this is build-stage, not learning-stage)

Reality check: no strategy here is assumed profitable live. Edges decay, costs are brutal, markets adapt. The skill being built is the process — rigorous research that knows the difference between a real edge and an overfit one. That discipline is the transferable asset whether Qaizen happens or not.

# 04 \- Projects

\========================================  
QAIZEN — PROJECT SPECS (26 critical-path)  
\========================================  
Legend: CP \= critical path. GATE \= rigor gate, do not rush.  
AI mode: tutor \= you write, I critique. auto \= agent runs it (only \#91/\#92).  
Dates \= suggested targets, adjustable.

\----------------------------------------  
PHASE 0 — INDUSTRY & BUSINESS LITERACY (reading, all summer)  
\----------------------------------------

Project 0: Firm types & how they make money (CP)  
\- Suggested target: 6/30/2026  
\- Purpose: Know what you're even trying to build. You can't choose what kind of firm Qaizen is until you know how each kind earns and survives.  
\- What it is: A research-and-notes project, not code. Read about the four firm archetypes and write up how each makes money.  
\- What you do:  
  \- Read the business chapters of Ernie Chan (Quantitative Trading) \+ Narang (Inside the Black Box).  
  \- For each firm type — prop shop, hedge fund, market maker, asset manager — write how it earns, who its capital comes from, and what kills it.  
  \- Read 2-3 firm teardowns (Renaissance, Two Sigma, Jane Street).  
\- Key questions to resolve:  
  \- How does a prop shop's money differ from a hedge fund's? (own capital vs investor capital)  
  \- What is 2-and-20, a high-water mark, a prop split?  
  \- Which model needs the least outside capital and regulation to start? (matters for Qaizen)  
\- Deliverable: A notes doc \+ a 1-page table "how each firm type earns."  
\- Done when: You can explain, unprompted, how each of the 4 firm types makes money and which fits a 2-person AI-first start.  
\- Skill: Industry literacy. AI mode: tutor (quiz you on it).

Project 0b: Asset-class & frequency landscape (CP)  
\- Suggested target: 7/7/2026  
\- Purpose: The D2 decision is "which asset class, which frequency." This project builds the menu you'll later choose from, bounded by what data you can actually get and afford.  
\- What it is: A comparison study mapping asset classes (equities, futures, FX, crypto, options) against trading frequency (daily, intraday, high-frequency) and data cost/availability.  
\- What you do:  
  \- For each asset class, note: data availability (free vs LSEG vs paid), typical edge sources, capital needed, competition level.  
  \- Map frequency tiers: what daily vs intraday vs HF each require in data and infra.  
  \- Cross-reference with your LSEG access and free sources.  
\- Key questions to resolve:  
  \- Where can a 2-person AI-first team realistically have an edge? (probably not HF market making — needs colocation/capital)  
  \- Which asset class has the cleanest free/academic data for learning? (likely US equities daily)  
  \- What does each frequency demand that you don't have yet?  
\- Deliverable: A comparison table feeding the D2 decision menu.  
\- Done when: You have a ranked shortlist of 2-3 viable asset-class/frequency combos for Qaizen, with reasons.  
\- Skill: Strategic scoping. AI mode: tutor.

\----------------------------------------  
PHASE 1 — FOUNDATION LIBRARY (core/)  
\----------------------------------------

Project 1: Market data downloader & cleaner (CP)  
\- Suggested target: 6/22/2026  
\- Purpose: Familiarize yourself with connecting to market data and get the big picture of how raw price data actually arrives — messy, with gaps, splits, and dividends. This is the foundation every later project imports.  
\- What it is: A reusable core/ module that pulls OHLCV (open/high/low/close/volume) data for a list of tickers, cleans it, and caches it locally.  
\- What you do:  
  \- Build a provider-abstraction layer: one interface, swappable backends (LSEG, yfinance, Stooq). So switching sources later is a config change, not a rewrite.  
  \- Pull a universe (e.g. S\&P 500 daily), handle missing data, stock splits, and dividend adjustments (learn why "adjusted close" exists).  
  \- Cache to DuckDB/Parquet so you never re-hit the API, and the cache is point-in-time correct.  
\- Key questions to resolve:  
  \- What data source? (LSEG for quality, yfinance/Stooq as free fallback — build both behind the abstraction)  
  \- What does "adjusted close" fix, and when must you NOT use it? (look-ahead risk)  
  \- How do you store data so a backtest can only see what was known at each date?  
\- Deliverable: core/ loader \+ one cached universe of clean daily data.  
\- Done when: You can call one function, get clean adjusted data for any ticker/date range, served from cache, with splits/dividends handled.  
\- Skill: Data ingestion, corporate actions, provider abstraction. AI mode: tutor.

Project 2: Returns & distribution analyzer (CP)  
\- Suggested target: 6/25/2026  
\- Purpose: Understand the raw material of all quant work — returns — and confront the single biggest myth in finance: that returns are normally distributed. They aren't (fat tails). Every risk model that assumes Normal underestimates crashes.  
\- What it is: A module that computes returns and visualizes their real distribution vs a Normal fit.  
\- What you do:  
  \- Compute simple returns vs log returns; understand when to use each.  
  \- Plot histograms of returns; overlay a fitted Normal distribution.  
  \- Compute skew and kurtosis; show how fat the tails really are.  
\- Key questions to resolve:  
  \- Simple vs log returns — when does each matter? (log returns add across time, simple across assets)  
  \- How far from Normal are real returns? (kurtosis \>\> 3\)  
  \- Why does this break VaR and option pricing?  
\- Deliverable: A histogram \+ skew/kurtosis numbers vs Normal, for several assets.  
\- Done when: You can show a chart proving returns have fatter tails than Normal, and explain why it matters.  
\- Skill: Return conventions, fat tails. AI mode: tutor.

Project 3: Rolling statistics dashboard (CP)  
\- Suggested target: 6/29/2026  
\- Purpose: The Sharpe ratio is the currency of this whole field and the go/no-go bar. Build it from first principles so you trust it — don't import a black box.  
\- What it is: A module computing rolling mean, volatility, and Sharpe ratio over configurable windows.  
\- What you do:  
  \- Compute rolling mean return and rolling volatility (standard deviation).  
  \- Annualize correctly (multiply by sqrt of periods-per-year — understand why sqrt).  
  \- Compute rolling Sharpe \= annualized excess return / annualized vol.  
\- Key questions to resolve:  
  \- Why do you annualize vol with sqrt(time) but return linearly?  
  \- What window length is honest vs cherry-picked?  
  \- What does a Sharpe of 1.0 actually mean? (this is your gate floor)  
\- Deliverable: A rolling Sharpe/vol chart over time for an asset.  
\- Done when: You can compute and explain a Sharpe ratio from scratch, including annualization.  
\- Skill: Sharpe from first principles, annualization. AI mode: tutor.

Project 4: Correlation & covariance explorer (CP)  
\- Suggested target: 7/2/2026  
\- Purpose: Diversification, portfolios, and stat-arb all rest on correlation. Critically: correlations are unstable — they spike toward 1 in crashes, exactly when you need diversification most.  
\- What it is: A tool computing correlation/covariance across an asset universe, with heatmaps, including during crash periods.  
\- What you do:  
  \- Compute the correlation matrix across a universe; render a heatmap.  
  \- Compare covariance vs correlation (scaled vs unscaled).  
  \- Compute correlations in a calm period vs a crash (2008/2020); show the spike.  
\- Key questions to resolve:  
  \- Covariance vs correlation — what's the difference and when use each?  
  \- Why do correlations break exactly when diversification matters?  
  \- How noisy/unstable are these estimates?  
\- Deliverable: A correlation heatmap \+ a demo of correlations spiking in a crash.  
\- Done when: You can show diversification fails in crashes and explain why.  
\- Skill: Covariance, correlation instability. AI mode: tutor.

Project 6: Risk metrics calculator (CP)  
\- Suggested target: 7/6/2026  
\- Purpose: These are the numbers reported to investors and used to judge every strategy. Build the core/ metrics module once; every later project imports it.  
\- What it is: A module computing max drawdown, Calmar, Sortino, and historical VaR.  
\- What you do:  
  \- Max drawdown: largest peak-to-trough drop in equity.  
  \- Calmar: return / max drawdown. Sortino: like Sharpe but only penalizes downside vol.  
  \- Historical VaR: the loss threshold at a confidence level (e.g. 95%).  
\- Key questions to resolve:  
  \- Why is drawdown what investors actually fear (more than vol)?  
  \- Sortino vs Sharpe — why penalize only downside?  
  \- What does historical VaR miss? (tail beyond the threshold — leads to CVaR later)  
\- Deliverable: A core/ metrics module returning all four for any equity curve.  
\- Done when: Any later project can pass an equity curve and get a full risk report.  
\- Skill: The metrics investors actually see. AI mode: tutor.

Project 7: Tick/bar storage pipeline (CP)  
\- Suggested target: 7/10/2026  
\- Purpose: Your data-eng strength, applied. Fast local storage is what lets you query years of data instantly and enforce point-in-time correctness — the defense against look-ahead bias.  
\- What it is: A pipeline loading market data into DuckDB/Parquet and querying it efficiently.  
\- What you do:  
  \- Design a schema for time-series bars (ticker, date, OHLCV).  
  \- Load your cached data into DuckDB; index by ticker+date.  
  \- Benchmark query speed; confirm you never re-hit the API.  
\- Key questions to resolve:  
  \- Why columnar storage (Parquet/DuckDB) for time series vs a row DB?  
  \- How does the storage layout enforce point-in-time (no future data leaking in)?  
  \- What's the query pattern a backtester needs?  
\- Deliverable: A query benchmark on cached data (e.g. "5 years, 500 tickers, \< 1s").  
\- Done when: You can query any slice of history fast, offline, point-in-time safe.  
\- Skill: Time-series data engineering. AI mode: tutor.

Project 10: Benchmark & beta tool (CP)  
\- Suggested target: 7/13/2026  
\- Purpose: Your first regression, and the baseline every strategy must beat. "Alpha" only means something relative to a benchmark (usually SPY).  
\- What it is: A tool regressing an asset's returns on the market (SPY) to get alpha and beta via OLS.  
\- What you do:  
  \- Run OLS: asset return \= alpha \+ beta \* market return \+ error.  
  \- Interpret beta (market sensitivity) and alpha (excess return).  
  \- Connect to CAPM intuition.  
\- Key questions to resolve:  
  \- What do alpha and beta actually mean?  
  \- Why must a strategy's edge be measured ABOVE the benchmark?  
  \- When is alpha real vs just hidden beta?  
\- Deliverable: Alpha/beta regression output for several assets.  
\- Done when: You can regress any asset on SPY and explain its alpha/beta.  
\- Skill: CAPM, first regression. AI mode: tutor.

\----------------------------------------  
PHASE 2 — RIGOR CORE  
\----------------------------------------

Project 11: Vectorized backtester from scratch (CP)  
\- Suggested target: 7/20/2026  
\- Purpose: The heart of everything. A backtester turns a signal into a P\&L curve. Building it from scratch (pure pandas, no library) is the only way to truly see where look-ahead bias sneaks in.  
\- What it is: A core/ backtester that takes positions and prices and returns an equity curve.  
\- What you do:  
  \- Take a signal (e.g. \+1/-1 positions), shift it forward one bar (you trade on yesterday's signal, not today's — the classic bug), multiply by returns.  
  \- Compound into an equity curve; compute the metrics from \#6.  
  \- Deliberately introduce then fix a look-ahead bug to feel it.  
\- Key questions to resolve:  
  \- Where exactly does look-ahead bias enter? (using same-bar data to trade that bar)  
  \- Why shift signals forward by one period?  
  \- What's gross P\&L vs net (costs come in \#13)?  
\- Deliverable: An equity curve produced from a simple signal.  
\- Done when: You can backtest any signal and you can explain where look-ahead would sneak in.  
\- Skill: Backtest mechanics, look-ahead bias. AI mode: tutor.

Project 12: Event-driven backtester (CP)  
\- Suggested target: 7/27/2026  
\- Purpose: Vectorized backtests cheat — they assume instant perfect fills. An event-driven loop (signal \-\> order \-\> fill) models reality and decouples the decision from the execution.  
\- What it is: A backtester with an event loop: each bar generates orders, orders get filled at the next bar's price.  
\- What you do:  
  \- Build the loop: on each bar, generate an order from the signal, simulate a fill on the next bar.  
  \- Separate the strategy logic from the execution logic.  
  \- Compare results to the vectorized version (\#11) — they should differ.  
\- Key questions to resolve:  
  \- Why is order-\>fill more realistic than instant execution?  
  \- What's the gap between the vectorized and event-driven P\&L, and why?  
  \- How does this set up cost modeling and HF backtesting later?  
\- Deliverable: A fill log \+ P\&L from the event loop.  
\- Done when: You can run a strategy through realistic order-\>fill simulation.  
\- Skill: Realistic execution, decoupling signal from fill. AI mode: tutor.

Project 13: Transaction cost & slippage model (CP, GATE)  
\- Suggested target: 8/1/2026  
\- Purpose: GATE. This is what kills beautiful backtests. Almost every "edge" dies once you subtract commissions, spread, and slippage. Gate 1 of the go/no-go bar is NET of these costs.  
\- What it is: A cost model added to the backtester: every trade pays commission \+ spread \+ slippage.  
\- What you do:  
  \- Add a per-trade cost: commission \+ half-spread \+ a slippage estimate (start 5 bps round-trip for liquid large-caps, per the go/no-go bar).  
  \- Re-run earlier strategies gross vs net; watch edges shrink or vanish.  
  \- Make cost assumptions a frozen config (so you can't quietly relax them to pass).  
\- Key questions to resolve:  
  \- How much of a typical edge survives realistic costs?  
  \- Why does higher trading frequency get punished hardest?  
  \- What cost assumption is honest for your target asset class?  
\- Deliverable: A gross-vs-net P\&L delta showing the cost drag.  
\- Done when: Every backtest reports net-of-cost results by default.  
\- Skill: Why gross backtests lie. AI mode: tutor.

Project 14: Time-series momentum strategy (CP)  
\- Suggested target: 8/6/2026  
\- Purpose: Your first real strategy through the full stack, and a known reference edge (momentum is the oldest documented anomaly) to validate that your backtester and gates work.  
\- What it is: A trend-following strategy: buy what's been going up, sell what's been going down.  
\- What you do:  
  \- Signal: if price \> N-day moving average (or past-N-month return \> 0), go long; else flat/short.  
  \- Run it through the event-driven backtester WITH costs.  
  \- Evaluate net Sharpe, drawdown.  
\- Key questions to resolve:  
  \- Does momentum survive costs in your universe?  
  \- What lookback is robust vs overfit? (don't tune to the best — that's \#18's lesson)  
  \- Is the edge real or a backtest artifact? (you'll test this hard in \#17/\#19)  
\- Deliverable: A net-of-cost P\&L curve for the momentum strategy.  
\- Done when: A complete strategy runs end-to-end, net of costs, with honest metrics.  
\- Skill: The momentum factor, full-stack strategy. AI mode: tutor.

Project 15: Mean-reversion strategy (CP)  
\- Suggested target: 8/10/2026  
\- Purpose: The opposite of momentum — bet that extremes snap back. Gives you a second strategy and a contrast in regime behavior (momentum and reversion thrive in different markets).  
\- What it is: A strategy entering when price deviates far from its mean (z-score / Bollinger bands), exiting on reversion.  
\- What you do:  
  \- Compute a z-score of price vs its rolling mean.  
  \- Enter when |z| is large (bet on reversion), exit when it normalizes.  
  \- Backtest net of costs.  
\- Key questions to resolve:  
  \- When does mean-reversion work vs blow up? (works in chop, dies in trends)  
  \- How is its regime behavior the inverse of momentum?  
  \- Does it survive costs?  
\- Deliverable: A net-of-cost P\&L curve for the reversion strategy.  
\- Done when: You have a working reversion strategy and can articulate when it fails.  
\- Skill: Reversion dynamics. AI mode: tutor.

Project 17: Walk-forward analysis framework (CP, GATE)  
\- Suggested target: 8/17/2026  
\- Purpose: GATE. The antidote to overfitting. You train/tune on one window, test on the NEXT (unseen) window, then roll forward. This is Gate 2 of the go/no-go bar.  
\- What it is: A core/ framework that splits history into rolling train/test windows and evaluates only on out-of-sample test windows.  
\- What you do:  
  \- Split data into rolling windows: fit/tune on window 1, test on window 2, slide forward.  
  \- Aggregate out-of-sample results across all windows.  
  \- Run \#14/\#15 through it; compare in-sample vs out-of-sample performance (OOS is always worse — that's the point).  
\- Key questions to resolve:  
  \- Why is in-sample performance meaningless?  
  \- How many folds is honest? (gate says \~6)  
  \- Does your edge survive on data it was never fit to?  
\- Deliverable: Rolling OOS results across multiple windows/regimes.  
\- Done when: Any strategy can be evaluated purely out-of-sample, rolling.  
\- Skill: Out-of-sample discipline. AI mode: tutor.

Project 19: Monte Carlo validation / deflated Sharpe (CP, GATE)  
\- Suggested target: 8/24/2026  
\- Purpose: GATE. Is your edge real or luck? If you tried 200 strategies, one will look great by chance. This tests significance and deflates for how many you searched. Gate 3 of the go/no-go bar.  
\- What it is: A core/ module that bootstraps/shuffles returns to build a null distribution, and computes a deflated Sharpe penalizing for the number of strategies tried.  
\- What you do:  
  \- Build a null: shuffle/bootstrap returns many times (block bootstrap, \~10k resamples), see what Sharpe luck alone produces.  
  \- Compare your strategy's Sharpe to that null \-\> a p-value.  
  \- Deflate the Sharpe by N (strategies searched) — the more you tried, the higher the bar.  
\- Key questions to resolve:  
  \- How good a Sharpe does pure luck produce when you search 200 strategies?  
  \- What's deflated Sharpe and why does search breadth inflate false positives?  
  \- Does your edge beat the null at p \< 0.05 AFTER deflation?  
\- Deliverable: A p-value vs the shuffled null for a strategy.  
\- Done when: You can statistically test whether an edge beats luck, accounting for search.  
\- Skill: Statistical significance, deflated Sharpe. AI mode: tutor.

Project 20: Multi-asset rebalancing backtester (CP)  
\- Suggested target: 8/29/2026  
\- Purpose: Step from "one strategy on one asset" to "a portfolio across a universe with periodic rebalancing." The agent in \#92 will search across a universe, so the backtester must handle portfolios.  
\- What it is: A backtester holding weighted positions across many assets, rebalancing on a schedule.  
\- What you do:  
  \- Hold target weights across N assets; rebalance (e.g. monthly) back to targets.  
  \- Account for rebalancing trades (and their costs).  
  \- Produce a portfolio-level equity curve.  
\- Key questions to resolve:  
  \- How does portfolio-level backtesting differ from single-asset?  
  \- What does rebalancing cost, and how often is optimal? (foreshadows \#30)  
  \- How do weights interact with the cost model?  
\- Deliverable: A portfolio equity curve with rebalancing.  
\- Done when: You can backtest a weighted multi-asset portfolio net of costs.  
\- Skill: Portfolio-level backtesting. AI mode: tutor.

END-OF-SUMMER GOAL: a strategy can be run end-to-end and judged net-of-cost, out-of-sample. If you hit this, the hard infrastructure is done.

\----------------------------------------  
PHASE 7 — THIN STAT-ARB SLICE (Fall 2026\)  
\----------------------------------------

Project 61: Cross-sectional momentum factor (CP)  
\- Suggested target: late Sept 2026  
\- Purpose: Shift from time-series (one asset over time) to cross-sectional (rank many assets against each other at one time) — the dominant style in modern stat-arb, and the hypothesis space the agent will search.  
\- What it is: A factor that ranks a universe by recent return, goes long the top, short the bottom.  
\- What you do:  
  \- Each period, rank all assets by trailing return.  
  \- Long the top decile, short the bottom decile (dollar-neutral).  
  \- Backtest the long/short spread net of costs.  
\- Key questions to resolve:  
  \- How is cross-sectional momentum different from time-series momentum (\#14)?  
  \- Why does long/short hedge out market beta?  
  \- Does the spread have a real edge net of costs?  
\- Deliverable: A long/short spread return series.  
\- Done when: You can build and test a ranked cross-sectional factor.  
\- Skill: Cross-sectional factors. AI mode: tutor.

Project 67: Alpha combination engine (CP)  
\- Suggested target: mid Oct 2026  
\- Purpose: Real funds don't have one great signal — they blend many weak ones. This teaches how to weight signals by quality (Information Coefficient) and is how the agent's many outputs aggregate into one strategy.  
\- What it is: An engine combining multiple weak signals into one, weighted by each signal's IC (correlation with future returns).  
\- What you do:  
  \- Take 2-3 signals (momentum, reversion, etc.); compute each one's IC.  
  \- Combine them weighted by IC.  
  \- Show the combined signal beats any single one (the Fundamental Law of Active Management: breadth helps).  
\- Key questions to resolve:  
  \- What is the Information Coefficient?  
  \- Why do many weak uncorrelated signals beat one strong one?  
  \- How do you weight without overfitting the weights?  
\- Deliverable: Combined-signal IC vs the individual signals.  
\- Done when: You can blend signals by IC and show the blend wins.  
\- Skill: Signal weighting, breadth. AI mode: tutor.

\----------------------------------------  
PHASE 8 — THIN ML SLICE / LEAKAGE DISCIPLINE (Fall 2026\)  
\----------------------------------------

Project 71: Financial ML feature pipeline (CP)  
\- Suggested target: late Oct 2026  
\- Purpose: ML in finance lives or dies on one thing: look-ahead leakage. This builds features with strict point-in-time correctness — every feature uses only data known at that moment.  
\- What it is: A pipeline turning raw data into ML features (technical, fundamental) with guaranteed no future data.  
\- What you do:  
  \- Engineer features (moving averages, volatility, ratios) using only past data at each timestamp.  
  \- Audit every feature for leakage (e.g. using a full-sample mean \= leak).  
  \- Align features with the point-in-time data store (\#7).  
\- Key questions to resolve:  
  \- What are the subtle ways future data leaks into features?  
  \- How do you prove a feature is point-in-time correct?  
  \- Why is this "the cardinal sin" of financial ML?  
\- Deliverable: A leakage-checked feature set.  
\- Done when: You have features you can defend as having zero look-ahead.  
\- Skill: Feature engineering, leakage prevention. AI mode: tutor.

Project 72: Triple-barrier labeling \+ meta-labeling (CP)  
\- Suggested target: mid Nov 2026  
\- Purpose: To do supervised ML you need labels (what is the model predicting?). Naive labels ("return next day") are weak. Triple-barrier labels by which happens first: profit target, stop loss, or time limit — how a trader actually thinks.  
\- What it is: A labeling scheme (Lopez de Prado): for each entry, label by which of 3 barriers (up/down/time) is hit first. Meta-labeling adds a second model deciding whether to act.  
\- What you do:  
  \- For each potential trade, set a profit barrier, a stop barrier, and a time limit; label by which hits first.  
  \- Add meta-labeling: a model that says "take this signal or not" (sizing/confidence).  
\- Key questions to resolve:  
  \- Why is triple-barrier better than fixed-horizon labeling?  
  \- What does meta-labeling separate? ("what to bet on" vs "how much")  
  \- How does labeling choice change what the model learns?  
\- Deliverable: A labeled dataset.  
\- Done when: You can label data the triple-barrier way and explain meta-labeling.  
\- Skill: Lopez de Prado labeling. AI mode: tutor.

Project 73: Purged & embargoed cross-validation (CP, GATE)  
\- Suggested target: early Dec 2026  
\- Purpose: GATE. Standard cross-validation leaks in finance because samples overlap in time. Purging \+ embargoing removes train samples that overlap test labels. The single most under-appreciated technique in financial ML — supports go/no-go Gate 3\.  
\- What it is: A core/ CV scheme that purges overlapping samples and embargoes a gap around the test set.  
\- What you do:  
  \- Implement k-fold CV but purge training samples whose label windows overlap the test set.  
  \- Add an embargo (a gap) after each test fold.  
  \- Show how much standard CV overstates performance vs purged CV.  
\- Key questions to resolve:  
  \- Why does normal CV leak when labels span time?  
  \- What do purging and embargoing each fix?  
  \- How much does standard CV inflate the score?  
\- Deliverable: CV splits with provably no overlap leakage.  
\- Done when: You can cross-validate a financial ML model without leakage.  
\- Skill: Leak-free validation. AI mode: tutor.

Project 74: Gradient-boosted return predictor (CP)  
\- Suggested target: Dec 2026 break  
\- Purpose: Your first real ML alpha model. Tree ensembles (XGBoost/LightGBM) beat deep nets on tabular financial data. Gives the agent a learned-signal hypothesis class to generate and test.  
\- What it is: A gradient-boosted model predicting returns (or direction) from your \#71 features, validated with \#73.  
\- What you do:  
  \- Train XGBoost/LightGBM on the leakage-checked features, triple-barrier labels.  
  \- Validate with purged CV; measure out-of-sample predictive power.  
  \- Turn predictions into a backtested strategy net of costs.  
\- Key questions to resolve:  
  \- Why do trees beat deep nets on tabular finance data?  
  \- Does the model have real OOS predictive power, or did it memorize?  
  \- How does prediction confidence map to position size?  
\- Deliverable: An OOS predictive score \+ a backtested strategy.  
\- Done when: You have an ML strategy validated leak-free, net of costs.  
\- Skill: Tree ensembles for alpha. AI mode: tutor.

\----------------------------------------  
PHASE 10 — THE THESIS TEST (Winter/Spring 2027\)  
\----------------------------------------

Project 91: LLM alpha-research assistant (CP)  
\- Suggested target: Feb 2027  
\- Purpose: First real test of the thesis. Can an LLM agent read research/filings and propose TESTABLE hypotheses you then vet? This is the front of the research funnel — agent as multiplier.  
\- What it is: An agent that ingests papers/filings/data and outputs structured, testable strategy hypotheses.  
\- What you do:  
  \- Build an agent that reads source material and proposes hypotheses in a structured format (signal, universe, rationale).  
  \- You vet each: is it testable with your stack? Is the rationale sound?  
  \- Log everything (AI mode \= auto, per the go/no-go logging rules).  
\- Key questions to resolve:  
  \- Can the agent generate hypotheses that are actually testable, not vague?  
  \- What fraction are worth testing vs noise?  
  \- Where does it add value vs waste your time?  
\- Deliverable: A set of vettable hypotheses \+ the full log.  
\- Done when: The agent reliably produces hypotheses you can feed to a backtest.  
\- Skill: LLM agents as research multipliers. AI mode: auto.

Project 92: Agentic backtesting loop (CP)  
\- Suggested target: Apr 2027  
\- Purpose: THE thesis test. A closed loop: agent generates a strategy \-\> backtests it \-\> critiques \-\> iterates, autonomously. Scored against the frozen go/no-go bar. This produces the go/no-go evidence and answers the whole project's question.  
\- What it is: An autonomous loop wiring \#91 (hypotheses) into the backtester \+ validation, iterating to find an edge — under hard guardrails against overfitting-by-search.  
\- What you do:  
  \- FIRST: freeze the go/no-go bar (05) and timestamp it. Do not skip this.  
  \- Wire the agent: generate hypothesis \-\> build signal \-\> backtest net of costs \-\> walk-forward \-\> deflated Sharpe \-\> critique \-\> iterate.  
  \- Enforce the search budget (max \~200 strategies) so deflation is honest.  
  \- Score every survivor against all 4 gates. Log which work was agent vs human (Gate 4).  
\- Key questions to resolve:  
  \- Does the loop produce a strategy that clears ALL FOUR gates out-of-sample?  
  \- Did the AGENT do the generative work, or did you hand-hold it? (Gate 4\)  
  \- Is any survivor real, or did search manufacture it? (the deflation must hold)  
\- Deliverable: Strategies scored against the go/no-go bar; a YES or NO on the thesis.  
\- Done when: The loop has run within budget and you have honest go/no-go evidence \-\> feeds the D2 decision \-\> evaluate the build-stage trigger.  
\- Skill: Closed-loop autonomous research. AI mode: auto.

# Phase 0

\----------------------------------------  
PHASE 0 — INDUSTRY & BUSINESS LITERACY (reading, all summer)  
\----------------------------------------

Project 0: Firm types & how they make money (CP)  
\- Suggested target: 6/30/2026  
\- Purpose: Know what you're even trying to build. You can't choose what kind of firm Qaizen is until you know how each kind earns and survives.  
\- What it is: A research-and-notes project, not code. Read about the four firm archetypes and write up how each makes money.  
\- What you do:  
  \- Read the business chapters of Ernie Chan (Quantitative Trading) \+ Narang (Inside the Black Box).  
  \- For each firm type — prop shop, hedge fund, market maker, asset manager — write how it earns, who its capital comes from, and what kills it.  
  \- Read 2-3 firm teardowns (Renaissance, Two Sigma, Jane Street).  
\- Key questions to resolve:  
  \- How does a prop shop's money differ from a hedge fund's? (own capital vs investor capital)  
  \- What is 2-and-20, a high-water mark, a prop split?  
  \- Which model needs the least outside capital and regulation to start? (matters for Qaizen)  
\- Deliverable: A notes doc \+ a 1-page table "how each firm type earns."  
\- Done when: You can explain, unprompted, how each of the 4 firm types makes money and which fits a 2-person AI-first start.  
\- Skill: Industry literacy. AI mode: tutor (quiz you on it).

Project 0b: Asset-class & frequency landscape (CP)  
\- Suggested target: 7/7/2026  
\- Purpose: The D2 decision is "which asset class, which frequency." This project builds the menu you'll later choose from, bounded by what data you can actually get and afford.  
\- What it is: A comparison study mapping asset classes (equities, futures, FX, crypto, options) against trading frequency (daily, intraday, high-frequency) and data cost/availability.  
\- What you do:  
  \- For each asset class, note: data availability (free vs LSEG vs paid), typical edge sources, capital needed, competition level.  
  \- Map frequency tiers: what daily vs intraday vs HF each require in data and infra.  
  \- Cross-reference with your LSEG access and free sources.  
\- Key questions to resolve:  
  \- Where can a 2-person AI-first team realistically have an edge? (probably not HF market making — needs colocation/capital)  
  \- Which asset class has the cleanest free/academic data for learning? (likely US equities daily)  
  \- What does each frequency demand that you don't have yet?  
\- Deliverable: A comparison table feeding the D2 decision menu.  
\- Done when: You have a ranked shortlist of 2-3 viable asset-class/frequency combos for Qaizen, with reasons.  
\- Skill: Strategic scoping. AI mode: tutor.

# Phase 1

\----------------------------------------  
PHASE 1 — FOUNDATION LIBRARY (core/)  
\----------------------------------------

Project 1: Market data downloader & cleaner (CP)  
\- Suggested target: 6/22/2026  
\- Purpose: Familiarize yourself with connecting to market data and get the big picture of how raw price data actually arrives — messy, with gaps, splits, and dividends. This is the foundation every later project imports.  
\- What it is: A reusable core/ module that pulls OHLCV (open/high/low/close/volume) data for a list of tickers, cleans it, and caches it locally.  
\- What you do:  
  \- Build a provider-abstraction layer: one interface, swappable backends (LSEG, yfinance, Stooq). So switching sources later is a config change, not a rewrite.  
  \- Pull a universe (e.g. S\&P 500 daily), handle missing data, stock splits, and dividend adjustments (learn why "adjusted close" exists).  
  \- Cache to DuckDB/Parquet so you never re-hit the API, and the cache is point-in-time correct.  
\- Key questions to resolve:  
  \- What data source? (LSEG for quality, yfinance/Stooq as free fallback — build both behind the abstraction)  
  \- What does "adjusted close" fix, and when must you NOT use it? (look-ahead risk)  
  \- How do you store data so a backtest can only see what was known at each date?  
\- Deliverable: core/ loader \+ one cached universe of clean daily data.  
\- Done when: You can call one function, get clean adjusted data for any ticker/date range, served from cache, with splits/dividends handled.  
\- Skill: Data ingestion, corporate actions, provider abstraction. AI mode: tutor.

Project 2: Returns & distribution analyzer (CP)  
\- Suggested target: 6/25/2026  
\- Purpose: Understand the raw material of all quant work — returns — and confront the single biggest myth in finance: that returns are normally distributed. They aren't (fat tails). Every risk model that assumes Normal underestimates crashes.  
\- What it is: A module that computes returns and visualizes their real distribution vs a Normal fit.  
\- What you do:  
  \- Compute simple returns vs log returns; understand when to use each.  
  \- Plot histograms of returns; overlay a fitted Normal distribution.  
  \- Compute skew and kurtosis; show how fat the tails really are.  
\- Key questions to resolve:  
  \- Simple vs log returns — when does each matter? (log returns add across time, simple across assets)  
  \- How far from Normal are real returns? (kurtosis \>\> 3\)  
  \- Why does this break VaR and option pricing?  
\- Deliverable: A histogram \+ skew/kurtosis numbers vs Normal, for several assets.  
\- Done when: You can show a chart proving returns have fatter tails than Normal, and explain why it matters.  
\- Skill: Return conventions, fat tails. AI mode: tutor.

Project 3: Rolling statistics dashboard (CP)  
\- Suggested target: 6/29/2026  
\- Purpose: The Sharpe ratio is the currency of this whole field and the go/no-go bar. Build it from first principles so you trust it — don't import a black box.  
\- What it is: A module computing rolling mean, volatility, and Sharpe ratio over configurable windows.  
\- What you do:  
  \- Compute rolling mean return and rolling volatility (standard deviation).  
  \- Annualize correctly (multiply by sqrt of periods-per-year — understand why sqrt).  
  \- Compute rolling Sharpe \= annualized excess return / annualized vol.  
\- Key questions to resolve:  
  \- Why do you annualize vol with sqrt(time) but return linearly?  
  \- What window length is honest vs cherry-picked?  
  \- What does a Sharpe of 1.0 actually mean? (this is your gate floor)  
\- Deliverable: A rolling Sharpe/vol chart over time for an asset.  
\- Done when: You can compute and explain a Sharpe ratio from scratch, including annualization.  
\- Skill: Sharpe from first principles, annualization. AI mode: tutor.

Project 4: Correlation & covariance explorer (CP)  
\- Suggested target: 7/2/2026  
\- Purpose: Diversification, portfolios, and stat-arb all rest on correlation. Critically: correlations are unstable — they spike toward 1 in crashes, exactly when you need diversification most.  
\- What it is: A tool computing correlation/covariance across an asset universe, with heatmaps, including during crash periods.  
\- What you do:  
  \- Compute the correlation matrix across a universe; render a heatmap.  
  \- Compare covariance vs correlation (scaled vs unscaled).  
  \- Compute correlations in a calm period vs a crash (2008/2020); show the spike.  
\- Key questions to resolve:  
  \- Covariance vs correlation — what's the difference and when use each?  
  \- Why do correlations break exactly when diversification matters?  
  \- How noisy/unstable are these estimates?  
\- Deliverable: A correlation heatmap \+ a demo of correlations spiking in a crash.  
\- Done when: You can show diversification fails in crashes and explain why.  
\- Skill: Covariance, correlation instability. AI mode: tutor.

Project 6: Risk metrics calculator (CP)  
\- Suggested target: 7/6/2026  
\- Purpose: These are the numbers reported to investors and used to judge every strategy. Build the core/ metrics module once; every later project imports it.  
\- What it is: A module computing max drawdown, Calmar, Sortino, and historical VaR.  
\- What you do:  
  \- Max drawdown: largest peak-to-trough drop in equity.  
  \- Calmar: return / max drawdown. Sortino: like Sharpe but only penalizes downside vol.  
  \- Historical VaR: the loss threshold at a confidence level (e.g. 95%).  
\- Key questions to resolve:  
  \- Why is drawdown what investors actually fear (more than vol)?  
  \- Sortino vs Sharpe — why penalize only downside?  
  \- What does historical VaR miss? (tail beyond the threshold — leads to CVaR later)  
\- Deliverable: A core/ metrics module returning all four for any equity curve.  
\- Done when: Any later project can pass an equity curve and get a full risk report.  
\- Skill: The metrics investors actually see. AI mode: tutor.

Project 7: Tick/bar storage pipeline (CP)  
\- Suggested target: 7/10/2026  
\- Purpose: Your data-eng strength, applied. Fast local storage is what lets you query years of data instantly and enforce point-in-time correctness — the defense against look-ahead bias.  
\- What it is: A pipeline loading market data into DuckDB/Parquet and querying it efficiently.  
\- What you do:  
  \- Design a schema for time-series bars (ticker, date, OHLCV).  
  \- Load your cached data into DuckDB; index by ticker+date.  
  \- Benchmark query speed; confirm you never re-hit the API.  
\- Key questions to resolve:  
  \- Why columnar storage (Parquet/DuckDB) for time series vs a row DB?  
  \- How does the storage layout enforce point-in-time (no future data leaking in)?  
  \- What's the query pattern a backtester needs?  
\- Deliverable: A query benchmark on cached data (e.g. "5 years, 500 tickers, \< 1s").  
\- Done when: You can query any slice of history fast, offline, point-in-time safe.  
\- Skill: Time-series data engineering. AI mode: tutor.

Project 10: Benchmark & beta tool (CP)  
\- Suggested target: 7/13/2026  
\- Purpose: Your first regression, and the baseline every strategy must beat. "Alpha" only means something relative to a benchmark (usually SPY).  
\- What it is: A tool regressing an asset's returns on the market (SPY) to get alpha and beta via OLS.  
\- What you do:  
  \- Run OLS: asset return \= alpha \+ beta \* market return \+ error.  
  \- Interpret beta (market sensitivity) and alpha (excess return).  
  \- Connect to CAPM intuition.  
\- Key questions to resolve:  
  \- What do alpha and beta actually mean?  
  \- Why must a strategy's edge be measured ABOVE the benchmark?  
  \- When is alpha real vs just hidden beta?  
\- Deliverable: Alpha/beta regression output for several assets.  
\- Done when: You can regress any asset on SPY and explain its alpha/beta.  
\- Skill: CAPM, first regression. AI mode: tutor.

# Project 1

Project 1: Market data downloader & cleaner (CP)  
\- Suggested target: 6/22/2026  
\- Purpose: Familiarize yourself with connecting to market data and get the big picture of how raw price data actually arrives — messy, with gaps, splits, and dividends. This is the foundation every later project imports.  
\- What it is: A reusable core/ module that pulls OHLCV (open/high/low/close/volume) data for a list of tickers, cleans it, and caches it locally.  
\- What you do:  
  \- Build a provider-abstraction layer: one interface, swappable backends (LSEG, yfinance, Stooq). So switching sources later is a config change, not a rewrite.  
  \- Pull a universe (e.g. S\&P 500 daily), handle missing data, stock splits, and dividend adjustments (learn why "adjusted close" exists).  
  \- Cache to DuckDB/Parquet so you never re-hit the API, and the cache is point-in-time correct.  
\- Key questions to resolve:  
  \- What data source? (LSEG for quality, yfinance/Stooq as free fallback — build both behind the abstraction)  
  \- What does "adjusted close" fix, and when must you NOT use it? (look-ahead risk)  
  \- How do you store data so a backtest can only see what was known at each date?  
\- Deliverable: core/ loader \+ one cached universe of clean daily data.  
\- Done when: You can call one function, get clean adjusted data for any ticker/date range, served from cache, with splits/dividends handled.  
\- Skill: Data ingestion, corporate actions, provider abstraction. AIt mode: tutor.

# 05 \- Resources

GO-NO-GO — THE PRE-REGISTERED SUCCESS BAR

The pre-registered success bar for the thesis: can an AI-agent process find real edge? This document is the decision instrument. It must be written, frozen, and timestamped before the agentic loop (\#92) runs.

WHY PRE-REGISTRATION  
Set the bar after you see results and every output looks like success — that's storytelling, not research. Setting it before, and refusing to move it, is the one thing that separates a real edge from an overfit one. The deflated-Sharpe gate exists specifically because searching N strategies guarantees a good-looking backtest by luck; if the bar isn't fixed in advance, the agentic loop will simply manufacture false edge — the exact "overfitting-by-search" failure \#92 is built to avoid.  
Changing any threshold below after results are seen invalidates the result. If the bar must change, that is a new pre-registration with a new timestamp, run on fresh unseen data.

THE FOUR MANDATORY GATES  
A candidate strategy counts as "real edge found by the agent process" only if it clears ALL four.  
Note: starting points below are proposed, not frozen. They assume the most likely first target — daily US equities, liquid large/mid-cap universe. If the D2 decision lands elsewhere (crypto-intraday, options), revisit costs/regimes/null before freezing.

Gate 1 — Net-of-cost, out-of-sample, positive  
What: positive return after transaction costs and slippage, on data the agent never saw during search.  
Implemented by: cost model \#13 \+ a held-out OOS split it never trained/searched on.  
Lock before first run:  
\- Minimum net Sharpe (after costs): \>= 1.0 annualized (proposed) — below 1.0 \= not worth capital. Raise to 1.5 if a survivor looks strong; never lower after the fact.  
\- OOS window \+ hold-out: most recent 30% of history held out (proposed), \>= the last 2 years for daily data, true embargo — the agent never reads it during search.  
\- Cost assumptions frozen (proposed): $0 commission \+ 5 bps round-trip all-in (spread \+ slippage) for liquid large-caps; 10 bps for mid-caps. One number, set before any run, never relaxed to make a strategy pass.

Gate 2 — Survives walk-forward across multiple regimes  
What: holds up across rolling out-of-sample windows spanning different market regimes — not one lucky period.  
Implemented by: walk-forward framework \#17.  
Lock before first run:  
\- Number of folds: 6 rolling walk-forward folds (proposed).  
\- Regimes that must be covered (proposed): 2008 GFC, 2020 COVID shock, 2022 rate-hike bear, and a low-vol chop period (2017). If the dataset is too short to span these (e.g. crypto), substitute equivalent stress/calm regimes and document the swap.  
\- Consistency criterion (proposed): positive net Sharpe in \>= 4 of 6 folds, AND no single fold worse than \-0.5 Sharpe (no catastrophic regime blow-up).

Gate 3 — Beats the null, penalized for search breadth  
What: the result beats a Monte Carlo / shuffled-returns null at a pre-set significance, deflated for the number of strategies searched.  
Implemented by: Monte Carlo validation / deflated Sharpe \#19 (supported by purged CV \#73 so the OOS claim isn't leakage-contaminated).  
Lock before first run:  
\- Significance level: deflated-Sharpe p \< 0.05 (proposed).  
\- Search-breadth N to deflate by \= the actual logged count of strategies the agent evaluated this run (counted by core/, not estimated). Bounded by the search budget below.  
\- Null construction (proposed): stationary block bootstrap, \~20-day blocks, 10,000 resamples.

Gate 4 — The agent did the generative work  
What: the hypothesis → test → iterate work was done by the agent, not Carlton hand-feeding it the answer.  
Implemented by: \#91 / \#92, logged per the two-mode rule (see 04 \- Projects).  
Lock before first run:  
\- Definition of "autonomous" (proposed): the agent proposes the hypothesis, writes the feature/signal code, runs the backtest via core/, reads results, and iterates. Allowed human input: initial guardrails (universe, frozen cost model, the gates), infra/bug fixes, killing a clearly broken run. NOT allowed: human picking which signal/feature wins, human tuning params toward the OOS set, human selecting the final survivor.  
\- Logging format (proposed): each iteration → JSON {timestamp, hypothesis, code\_diff, params, in\_sample\_metrics, decision, author: agent|human}. Any human edit to a strategy file flips its tag to human-assisted, which disqualifies it from Gate 4\.

DECISION RULE  
Thesis \= YES if \>= 1 strategy clears all four gates within a fixed search budget.  
Thesis \= NO / partial otherwise → do not advance to 06 \- Build Stage.  
\- Fixed search budget (proposed): max 200 distinct strategies evaluated per run, or 48 h wall-clock, whichever comes first. This bounds the Gate-3 deflation N and stops the loop from brute-forcing a false positive.  
A "no" is a real, valuable result — it answers the thesis honestly and saves you from building a firm on noise.

TO LOCK BEFORE THE FIRST RUN (open numeric placeholders)  
These are the open items Carlton must set. Until every value above is filled and this file is timestamped, \#92 does not run.  
\- Gate 1: net Sharpe floor, OOS window, frozen cost assumptions  
\- Gate 2: fold count, required regimes, consistency criterion  
\- Gate 3: significance level, search-breadth N, null construction  
\- Gate 4: definition of autonomous, logging format  
\- Decision rule: fixed search budget

FREEZE RECORD  
Frozen on: \_\_\_\_-\_\_-\_\_   By: \_\_\_\_  
No threshold above changes after this date without a new pre-registration \+ fresh unseen data.

# Lectures

- [ ] MIT OPEN courseware (Math n Finance)  
      1. [LINK](https://www.youtube.com/watch?v=z4p87TPCnQc&list=PLUl4u3cNGP601Q2jo-J_3raNCMMs6Jves&index=2)  
- [ ] Jim Simons: Quantitative Theorem & Mathematical Genius  
      - [ ] [LINK](https://www.youtube.com/watch?v=VboVwlFvCVs)  
- [ ] William Ackman: Everything You Need to Know About Finance and Investing in Under an Hour  
      - [ ] [LINK](https://www.youtube.com/watch?v=WEDIj9JBTC8)

# Courses

- [ ] [https://www.quantguide.io/](https://www.quantguide.io/)  
- [ ] 

# Projects

# Data

1. [https://www.kaggle.com/](https://www.kaggle.com/)  
2. 

# 06 \- Go-No-Go

BUILD STAGE (DEFERRED)

Everything required to actually form Qaizen. None of it gets work now — it is captured, not solved, so the eventual transition is fast instead of a from-scratch scramble.

TRIGGER — WHEN LEARNING BECOMES BUILDING  
Advance from learning-stage to build-stage only when BOTH are true:  
1\. 05 \- Go-No-Go returns YES — the agent process produced \>= 1 edge surviving all four gates out-of-sample, within the fixed search budget.  
2\. The D2 decision is made — asset class \+ frequency and the agent's role are chosen with evidence (see 03 \- Roadmap).  
Until both hold, nothing below gets cycles — only capture.

Why bind the trigger to evidence? Two opposite failure modes, one rule kills both:  
\- Drift forever — learning with no stopping rule, the firm never starts.  
\- Premature build — getting excited and incorporating around an "edge" that never cleared the bar.  
You build the firm because the evidence earned it, not because you're impatient.

PARKED-BUT-CAPTURED CHECKLIST  
Stubs only. Each becomes a real decision after the trigger fires.  
\- Legal entity \+ registration. RIA vs CPO/CTA thresholds, who must register, jurisdiction (US/state). Note: trading only your own money has a very different bar than managing others'.  
\- Capital source — own money vs prop-firm backing vs external investors. Each is a different regulatory world. External money triggers far more compliance (disclosures, audits, custody). Decide this before anything else legal, because it sets which registration applies.  
\- Exact equity split. Range agreed: 60-40 to 80-20, Carlton majority. Final number \+ vesting / cliff set at formation, not now.  
\- Commercial data licensing. The LSEG academic key CANNOT carry to a commercial firm — it's learning-stage only and dies with enrollment. Budget for real licensing; list candidate vendors (Polygon, Databento, LSEG commercial, exchange direct) once the asset class is known.  
\- Brokerage / execution infra. Broker \+ API choice, order routing, and a hard paper-trading → live gate before any real capital.  
\- David's role formalization. Co-founder vs contributor, and his startup's status at that time. Revisit only when the partnership has proven itself through the learning stage.  
\- Risk kill-switches. Automated drawdown limits and a manual stop before live capital — non-negotiable, designed before go-live.

WHAT YOU'LL ALREADY HAVE BY TRIGGER TIME  
Formation is fast, not from scratch, because the learning stage leaves real assets:  
\- The monorepo \+ protected core/ library (data, backtest, metrics, validation).  
\- A validated research process that knows real edge from overfit.  
\- The go/no-go evidence itself — the strongest possible input to any capital conversation.  
\- Working knowledge of the business \+ regulatory landscape from Phase 0\.  
The hard part — proving the thesis — is done before this document is opened for work.

# 07 \- Build Stage

CHECK-IN LOG

Dated history of qaizen-checkin runs. Newest at top. Maintained by the check-in skill.

2026-06-16 — Baseline  
Phase: Summer 2026 — Foundation \+ Rigor Core (on track — just starting)  
Shipped: 0/26 critical-path  
Since last check-in: vault restructured from the original 100-project roadmap into the 6-doc plan (01–06); critical path cut to \~26; Go-No-Go gate numbers proposed (not frozen); this skill \+ log created.  
Rigor flags:  
\- Go-No-Go gate numbers still proposed — fine for now, must freeze before \#92 (Spring 2027).  
\- David's technical background uncharacterized — his lane (4, 10, 15, 20\) is provisional.  
THE NEXT ACTION: Stand up the GitHub monorepo \+ core/ skeleton, then start project \#1 — the market data downloader behind a provider-abstraction layer (LSEG \+ free fallback, DuckDB/Parquet cache, point-in-time). It's the dependency for everything else.

