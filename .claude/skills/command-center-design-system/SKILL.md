---
name: command-center-design-system
description: >-
  Use when building or restyling any command_center frontend UI — a panel, chart, table, command
  bar, or theme token. Enforces the Bloomberg-terminal x Tufte aesthetic: dark dense theme,
  consistent chart theming across libraries, monospaced numeric formatting, color that encodes
  meaning, keyboard-first command codes, honest empty/gap states, and high data-ink with zero
  chartjunk. Use for every visual change so panels stay consistent. Not for backend or analytic
  work.
---

# command-center-design-system

Make every panel look like one terminal, not a pile of dashboards. Density is the product; clutter
and decoration are the enemy.

## Theme tokens (single source of truth — never hardcode per component)

Tokens live in `frontend/src/theme/tokens.css` as CSS variables and are bridged to both chart libs
via `frontend/src/theme/chartTheme.ts`. Change a token once → HTML, ECharts, and Lightweight-Charts
all recolor.

- Dark, low-glare background (`--cc-bg`); panel surface (`--cc-surface`); one accent for focus
  (`--cc-amber`). Up = `--cc-up`, down = `--cc-down` (defined once). A single sequential ramp for
  magnitude, a single diverging ramp for signed/centered data (e.g. correlation). **Color always
  encodes meaning — never decoration.** Never encode up/down by color alone — also carry a sign
  glyph / `+/-`.
- Monospaced/tabular numerals everywhere (JetBrains / IBM Plex Mono, `font-variant-numeric:
  tabular-nums`); fixed decimals per quantity; thousands grouping; right-aligned numeric columns.
  Percent vs bps vs price formatted consistently.
- Tight spacing scale (`1 = 2px`) so everything is denser than a normal web app.

## Chart theming (consistent across both libraries)

- Apply the shared theme wrapper (`charts/LightweightChart.tsx`, `charts/EChart.tsx`) to every
  chart — axes, gridlines, fonts, tooltips, colors match regardless of library. No per-chart
  restyling.
- Tufte rules: maximize data-ink; remove chartjunk (no 3D, decorative gradients, gauges, pie charts,
  rainbow colormaps for ordered data). Thin gridlines, direct labels over legends where feasible,
  small multiples over multi-axis cramming.
- **Honesty in pixels:** render NaN / gaps / under-filled rolling windows as greyed/hatched/
  annotated, not interpolated lines. Render the **empty state** explicitly ("no data for {ticker} —
  run `make cc-seed`"). Mark lookback / out-of-sample boundaries when relevant.

## Interaction (keyboard-first)

- Every panel has a short COMMAND CODE (Bloomberg-style mnemonic, e.g. `PX`, `RET`, `CORR`)
  declared in its `PanelDefinition` and reachable from the command bar.
- Core shortcuts are consistent app-wide (open command bar, switch panel, change ticker/date range/
  period preset). Mouse is optional, never required. Icon-only buttons carry `aria-label`s; focus
  rings use the amber token; amber-on-bg meets AAA contrast.

## Procedure

1. Use existing tokens & the shared chart wrapper; extend tokens centrally if something is missing.
2. Build the component dense and legible; audit data-ink (could anything be removed?).
3. Add the command code + keyboard reachability; ensure empty/gap/NaN honesty is visible.
4. Consume ONLY the generated API types (`lib/api/schema.d.ts`) — no `any` on the contract.
5. Verify visual + interaction consistency against an existing panel; add/extend Vitest tests for any
   pure logic (formatters, parsers).

## Done when

The UI uses shared tokens + chart theme, is dense with zero chartjunk, formats numbers consistently,
surfaces empty/gaps honestly, and is fully keyboard-reachable with a command code.
