import { type LineSeriesData, MultiLineChart } from "@/charts/MultiLineChart";
import { useSelection } from "@/store/selection";
import { tokens } from "@/theme/chartTheme";

import { usePerformance } from "./usePerformance";

export function PerformancePanel() {
  const { tickers, period } = useSelection();
  const { data, isLoading, error } = usePerformance(tickers, period);

  if (!tickers.length) return <div className="cc-empty">select tickers (click chips or use CORR)…</div>;
  if (isLoading) return <div className="cc-empty">loading overlay…</div>;
  if (error) return <div className="cc-empty">error loading performance</div>;
  if (!data || !data.series.length) return <div className="cc-empty">no data</div>;

  const palette = tokens().series;
  const series: LineSeriesData[] = data.series.map((s, i) => ({
    name: s.name,
    color: palette[i % palette.length],
    points: s.points,
  }));

  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <div style={{ position: "absolute", top: 4, left: 6, zIndex: 2, display: "flex", gap: 8 }}>
        {series.map((s) => (
          <span key={s.name} style={{ color: s.color, fontSize: 11 }}>
            ● {s.name}
          </span>
        ))}
        <span className="cc-muted" style={{ fontSize: 10 }}>
          rebased to 100
        </span>
      </div>
      <MultiLineChart series={series} />
    </div>
  );
}
