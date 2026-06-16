---
name: add-panel
description: >-
  Use to scaffold a NEW research panel in command_center end to end — the repeatable unit of growth.
  Orchestrates the full vertical: (if needed) add a tested analytic to quant_core → (if needed)
  register its data source → add a typed FastAPI endpoint with downsampling + test → regenerate TS
  types → build the themed React panel → register it in the panel registry + command bar → verify.
  Use whenever the user wants to "add a panel / view / chart" for some data or analytic (e.g. the v1
  set: catalog, price/corporate-actions, performance overlay, returns/distribution, rolling stats,
  correlation).
---

# add-panel

The unit of growth: turn one analytic into one honest, dense, typed research panel, keeping every
architecture seam intact. This skill COMPOSES the others — invoke each as you reach it.

## Procedure (compose, in order)

1. **Spec the panel.** Name, command code (e.g. `PX`), which data source(s), which analytic, the
   visualization (chart type / small multiples / table), the controls (ticker(s), date range,
   period preset, window/params), and the performance budget for its main series.
2. **Data source.** If the data artifact isn't already in the catalog → run `register-data-source`.
   Otherwise reference it by `id` + `source`.
3. **Analytic.** If the panel needs a number/series `quant_core` doesn't yet expose → run
   `quant-analytic` to implement + test it, then `graduate-to-quant-core` to place it additively. If
   it already exists, skip. NO quant math lives in the backend or frontend.
4. **API.** Run `fastapi-endpoint`: Pydantic request/response with honest `meta`/`coverage` and an
   empty case, server-side downsampling within budget, a validated ticker, an offline test, and
   regenerated TypeScript types.
5. **Frontend.** Run `command-center-design-system` to build the panel: shared theme + chart wrapper,
   dense/legible, consistent number formatting, empty/gaps/NaN/lookback shown honestly, keyboard-
   reachable with its command code. Consume ONLY the generated API types (no `any`).
6. **Register.** The panel is a self-contained folder under `frontend/src/panels/<name>/` whose
   `index.ts` calls `registerPanel({...})` (id, title, command code, category, dataDeps,
   defaultConfig, lazy component). `import.meta.glob` auto-loads it → it appears in the command bar
   and dock with **zero edits to core files**. Add Vitest coverage for any pure logic it introduces.
7. **Verify end to end:** `quant_core` + backend tests pass offline; the frontend type-checks,
   unit-tests, and builds; the panel opens via its command code, loads data within budget, and
   correctly shows empty/gaps/NaN. Lint clean; `uv.lock` committed; no cross-project imports.

## Done when

A new panel exists end to end — tested analytic in `quant_core`, typed + downsampled endpoint,
generated types, themed honest dense component, registered in the command bar — and the full verify
step is green. This is the loop you repeat for every v1 panel and beyond; it scales unchanged from
daily bars to tick/stream because each seam scales on its own.
