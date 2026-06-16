---
name: register-data-source
description: >-
  Use when a new kind of data artifact from the quant_journey monorepo should become visible and
  selectable in command_center's catalog — e.g. a new project's parquet output, the on-disk cache,
  a DuckDB table, a tick store, or a streaming feed. Handles describing the artifact (schema,
  coverage, point-in-time semantics), and registering it as a typed data source the backend can load
  and the catalog panel can list. Use whenever a new project's data needs to appear in the app.
---

# register-data-source

Make a new data artifact type discoverable WITHOUT teaching every panel about it. The catalog is the
front door; data sources are typed, self-describing, and honest about coverage.

## Procedure

1. **Describe the artifact** as a typed descriptor: `id`, human label, `kind` (parquet / cache /
   duckdb / tick-store / stream), location/glob, the canonical schema it conforms to (default:
   `quant_core`'s tidy-long OHLCV; document any superset/variant), coverage (tickers, date span,
   frequency), and **point-in-time semantics** (is it as-of correct? restatement risk?). Coverage
   and PIT honesty are mandatory.
2. **Set a distinct `source` key.** Project slices (`NNN_*/data/{ticker}_{interval}.parquet`, a
   cleaned date-bounded view) and the cache (`~/.cache/quant_journey/ohlcv/`, raw full history) are
   **semantically different artifacts for the same ticker** — they must never be silently merged.
   Key each dataset by `source` (e.g. `project:001`, `cache`) so the catalog and `/ohlcv` keep them
   separate; `/ohlcv` defaults to the cache.
3. **Implement loading behind the uniform data-source interface** (`backend/app/deps.load_ohlcv`)
   so the backend reads any source the same way. Reuse `quant_core.data` loaders/schema; never
   re-invent column names or pivots — conform to the canonical schema or document the deviation.
   Read parquet metadata cheaply (`pyarrow` row-group stats; check `statistics.has_min_max` and fall
   back to reading only the `date`/`ticker` columns) — never load full frames just to enumerate.
4. **Register** the descriptor so the catalog panel lists it and endpoints/panels can reference it by
   `id` + `source`. The catalog is the v1 flagship panel that enumerates the registry, including an
   empty state when no datasets exist.
5. **Respect the boundaries:** `command_center` reads artifacts; it does not import sibling `NNN_*`
   projects (CI forbids it). If transformation logic is needed and reusable, graduate it into
   `quant_core` first.
6. **Test offline** with a synthetic fixture artifact: the descriptor validates, the loader returns
   canonical schema, coverage/PIT metadata is correct, and the source appears in the catalog listing.

## Done when

The source is a typed, self-describing descriptor with a distinct `source` key, conforms to the
canonical schema, loads through the uniform interface, lists in the catalog, surfaces coverage + PIT
honestly, and is tested offline — with no cross-project import.
