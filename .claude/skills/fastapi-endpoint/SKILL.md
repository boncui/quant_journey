---
name: fastapi-endpoint
description: >-
  Use when adding or changing a command_center backend HTTP endpoint that exposes quant_core
  analytics or data to the frontend. Produces a typed FastAPI route + Pydantic request/response
  schema, server-side downsampling for large series, an offline test, and regenerated TypeScript
  types from the OpenAPI schema. Use whenever the React app needs a new data feed. Assumes the
  underlying analytic already lives in quant_core (use quant-analytic / graduate-to-quant-core first
  if not).
---

# fastapi-endpoint

Expose a `quant_core` analytic over a typed, budgeted, tested HTTP contract. The Pydantic model IS
the contract; TypeScript is generated from it, never hand-written.

## Procedure

1. **Define the Pydantic schema** (request params + response) in `app/schemas/`. Every route sets an
   explicit `operation_id` (so generated TS names are stable) and a `response_model`. The response
   carries DATA plus an honest `meta`/`coverage` block: row counts, date span, NaN/gap flags,
   `downsampled`, `n_raw`/`n_returned`, `elapsed_ms`, `payload_bytes`. Never omit gaps — surface
   them. Always model the **empty** case.
2. **Write the route thin:** parse → call `quant_core` → serialize. NO quant math in the handler (if
   you're writing `.rolling()` here, stop and graduate it). Require a bounded window (dates and/or
   `limit`); reject unbounded queries. Validate any `{ticker}` path param at the schema boundary with
   `^[A-Z0-9.\-]{1,15}$` and resolve ticker→file only through the in-memory catalog map — **never
   build a filesystem path from user input** (path-traversal guard).
3. **Read data only through `deps.load_ohlcv` / `deps.get_catalog`** (the single swap point). Keep
   project-slice vs cache as distinct `source`-keyed datasets; default to the cache (canonical full
   history). These are `Depends`-injected, never module-level singletons, so tests can override them.
4. **Downsample server-side** when the series exceeds the budget (~5–10k points, payload < ~1 MB):
   min/max-preserving decimation (faithful shape; full LTTB is a later upgrade). The SAME endpoint
   shape must serve 252 daily bars and millions of ticks — parametrize resolution, don't fork the
   route.
5. **Test offline** (`pytest` + `httpx.ASGITransport`, `app.dependency_overrides` → a synthetic
   fixture data dir): a known-value response, the `meta`/`coverage` flags, the downsample path
   (assert the point cap + shape fidelity), and the empty/edge case. No network.
6. **Regenerate TypeScript types** into the frontend (`pnpm --dir command_center/frontend run
   api:gen`, or `make cc-api`). Never hand-edit generated types; commit `schema.d.ts`.
7. **Verify:** backend tests pass; the frontend type-checks against the regenerated contract; the
   latency/payload budget is met (check `meta.elapsed_ms` / `meta.payload_bytes`).

## Done when

The endpoint is typed end to end, honest about coverage/empty, bounded + downsampled within budget,
ticker-validated, tested offline, and the TS types are regenerated and compiling.
