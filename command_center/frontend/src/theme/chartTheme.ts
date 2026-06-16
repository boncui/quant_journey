/** Read the CSS design tokens once and hand identical colors to the chart library/libraries,
 *  so HTML and canvas charts always match. The single token bridge. */

function cssVar(name: string, fallback: string): string {
  if (typeof window === "undefined") return fallback;
  const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  return v || fallback;
}

export function tokens() {
  return {
    bg: cssVar("--cc-bg", "#0a0a0b"),
    surface: cssVar("--cc-surface", "#121316"),
    border: cssVar("--cc-border", "#23252b"),
    fg: cssVar("--cc-fg", "#d6d7da"),
    muted: cssVar("--cc-fg-muted", "#7a7d85"),
    amber: cssVar("--cc-amber", "#ffb000"),
    up: cssVar("--cc-up", "#26a269"),
    down: cssVar("--cc-down", "#e01b24"),
    series: [1, 2, 3, 4, 5, 6, 7, 8].map((i) => cssVar(`--cc-series-${i}`, "#4fc3f7")),
  };
}

/** Base options shared by every Lightweight-Charts instance. */
export function lwcOptions() {
  const t = tokens();
  return {
    layout: {
      background: { color: t.bg },
      textColor: t.muted,
      fontFamily: "JetBrains Mono, monospace",
      fontSize: 11,
    },
    grid: {
      vertLines: { color: t.border },
      horzLines: { color: t.border },
    },
    rightPriceScale: { borderColor: t.border },
    timeScale: { borderColor: t.border, timeVisible: false },
    crosshair: { mode: 0 },
  };
}
