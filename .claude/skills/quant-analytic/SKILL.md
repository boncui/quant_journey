---
name: quant-analytic
description: >-
  Use when implementing, reviewing, or fixing ANY quantitative analytic for the quant journey —
  returns, volatility, Sharpe/Sortino, drawdown, VaR, correlation/covariance, rolling stats,
  factors, betas, or anything that turns price/return data into a number. Enforces the
  look-ahead-bias / annualization / NaN-min_periods / simple-vs-log checklist and tests against
  known closed-form values. Invoke BEFORE wiring any analytic into an API or chart. Not for plain
  HTTP, plotting, or non-quant code.
---

# quant-analytic

Implement a quantitative analytic so it is **correct and tested** before anything renders it.
Correctness over cleverness; the bug that flatters you is the one you ship.

## Procedure

1. **Locate the home.** Decide the `quant_core` subpackage:
   - returns / distribution / rolling → `stats`
   - Sharpe / Sortino / drawdown / VaR / Calmar / annualization → `metrics`
   - factor / beta / cross-sectional → `factors`
   - weights / optimization / cov matrices → `portfolio`
   - sim / PnL → `backtest`
   If it's reusable, it does **not** belong in `command_center` — hand off placement to
   `graduate-to-quant-core`.
2. **Pin conventions explicitly** in the docstring:
   - Returns: simple `p_t/p_{t-1}-1` vs log `ln(p_t/p_{t-1})` — pick one, keep it end to end.
   - Annualization: factor named and applied once (252 daily, 52 weekly, 12 monthly; vol scales by
     `√factor`, mean/return by `factor`; an annual `rf` is divided by the factor *before*
     subtraction — the classic Sharpe bug).
   - Input: canonical tidy-long frame, or a wide matrix via `to_wide`; tz-aware UTC, float64.
3. **Walk the look-ahead checklist:**
   - Every value at `t` uses only data ≤ `t`. Rolling windows are TRAILING (`.rolling(w)`), never
     `center=True`. Normalization is expanding/trailing, never full-sample on a PIT series.
   - `min_periods` deliberate (default `window`); under-filled windows are NaN, not fabricated.
   - On tidy-long, `groupby("ticker", observed=True)` before any shift/rolling so one ticker's first
     row isn't computed off another's last (no cross-ticker leak).
   - NaN policy explicit and surfaced, never silently filled.
4. **Implement** small and pure: take a DataFrame/Series, return data (Series/DataFrame/float/
   dataclass). No plotting, no I/O, no network (`quant_core` never imports matplotlib — see
   `data/corporate_actions.py`).
5. **Test against KNOWN values** in `quant_core/tests/` (mirror `conftest.py`'s offline fixtures —
   `make_tidy`, `FakeProvider`):
   - One closed-form / hand-computed case (Sharpe of a constant-return series; corr of a series with
     itself == 1; log-returns of a doubling series == `ln 2`; annualized vol == `√252 ×` daily vol).
   - One invariant/property (symmetry, unit diagonal, log-returns additive across concatenation).
   - Edge cases: empty, single row, all-NaN, single ticker, constant series.
6. **Verify:** `make test` (or `uv run --directory quant_core pytest`) + `make lint`.

## Done when

The analytic is in the right subpackage, conventions are documented, the look-ahead checklist
passes, and at least one closed-form + one invariant test pass offline.
