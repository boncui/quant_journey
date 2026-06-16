# command_center

Operating charter for this app: **read [`./METAPROMPT.md`](./METAPROMPT.md) first.**

Repo-wide law (do not re-derive — read the source):

- [`../README.md`](../README.md) — monorepo layout & the reuse boundary.
- [`../quant_core/README.md`](../quant_core/README.md) — canonical OHLCV schema & semver policy.
- [`../roadmap.md`](../roadmap.md) — the 100 projects this terminal visualizes.

The repeatable way to grow this app is the **`add-panel`** skill (at the repo-root
`.claude/skills/`), which composes `quant-analytic`, `graduate-to-quant-core`, `fastapi-endpoint`,
`command-center-design-system`, and `register-data-source`. A new panel should be one folder under
`frontend/src/panels/` plus a tested analytic in `quant_core` and a typed endpoint — no edits to
core files.
