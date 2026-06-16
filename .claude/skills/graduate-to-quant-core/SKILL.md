---
name: graduate-to-quant-core
description: >-
  Use when logic needs to move INTO quant_core — because a second project (or command_center) now
  needs analytic code currently living in one project, or a stub subpackage
  (stats/metrics/factors/portfolio/backtest) must be filled. Handles choosing the subpackage,
  exporting the public API additively, writing tests, the additive-semver decision (bump or not),
  and re-locking every dependent project. Use whenever you'd otherwise import across projects or
  duplicate analytic code.
---

# graduate-to-quant-core

Move reusable logic into the shared library WITHOUT breaking older projects. Reuse is the whole
point of the monorepo; semver discipline is what keeps 100 projects reproducible.

## Procedure

1. **Confirm it should graduate.** Rule: a project imports only `quant_core` + PyPI, never a
   sibling. If two consumers need it (or `command_center` does), it graduates. One-off glue stays.
2. **Pick the subpackage & public surface.** Place the code in the right stub
   (`stats / metrics / factors / portfolio / backtest`); export it via that subpackage's
   `__init__.py` `__all__` and, if user-facing, the package docstring's public-API list (see
   `quant_core/data/__init__.py` as the pattern).
3. **Keep it additive (semver):**
   - Pure addition (new function, or new param with a default) → stay within `0.1.x`; **no** version
     bump and **no** relock needed for editable source changes.
   - Renamed / removed / changed-signature public API → BREAKING → bump the minor in
     `quant_core/src/quant_core/__init__.py` (`__version__`) and `pyproject.toml` (`0.1 → 0.2`),
     widen each dependent's pin, then `make relock-all`.
   - **New runtime dependency** in `quant_core` (e.g. a new optional extra) → every project must
     `make relock-all` and recommit its `uv.lock` (this is the case that needs a relock even without
     an API change).
4. **Test in `quant_core`** following `quant-analytic` if it's math; mirror the offline-fixture style
   in `quant_core/tests/conftest.py` (inject fakes, no network).
5. **Delete the now-duplicated logic** from the originating project; have it import from core.
6. **Verify:** `make test-core`, then `make test-all` (every project still green under
   `uv sync --locked`), then `make lint`. Commit `quant_core` + any changed `uv.lock`s.

## Done when

Public API is additive (or a clean minor bump + relock), code is tested offline, no project imports
a sibling, `make test-all` is green, and locks are committed.
