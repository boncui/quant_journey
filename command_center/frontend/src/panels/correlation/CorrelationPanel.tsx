import type { EChartsOption } from "echarts";
import { useMemo } from "react";

import { EChart } from "@/charts/EChart";
import { useSelection } from "@/store/selection";
import { tokens } from "@/theme/chartTheme";

import { useCorrelation } from "./useCorrelation";

export function CorrelationPanel() {
  const { tickers, period } = useSelection();
  const { data, isLoading, error } = useCorrelation(tickers, period);

  const option = useMemo<EChartsOption>(() => {
    if (!data) return {};
    const t = tokens();
    const tk = data.tickers;
    const cells: [number, number, number | null][] = [];
    data.matrix.forEach((row, i) => row.forEach((v, j) => cells.push([j, i, v])));
    return {
      backgroundColor: "transparent",
      grid: { left: 52, right: 16, top: 12, bottom: 56 },
      tooltip: {
        position: "top",
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        formatter: (p: any) => {
          const v = p.value as [number, number, number | null];
          return `${tk[v[1]]} / ${tk[v[0]]}: ${v[2] == null ? "–" : v[2].toFixed(2)}`;
        },
      },
      xAxis: { type: "category", data: tk, axisLabel: { color: t.muted, fontSize: 9 } },
      yAxis: { type: "category", data: tk, axisLabel: { color: t.muted, fontSize: 9 } },
      visualMap: {
        min: -1,
        max: 1,
        calculable: true,
        orient: "horizontal",
        left: "center",
        bottom: 6,
        textStyle: { color: t.muted },
        inRange: { color: [t.down, t.bg, t.up] },
      },
      series: [
        {
          type: "heatmap",
          data: cells,
          label: {
            show: tk.length <= 12,
            color: t.fg,
            fontSize: 9,
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            formatter: (p: any) => {
              const v = p.value as [number, number, number | null];
              return v[2] == null ? "" : v[2].toFixed(2);
            },
          },
        },
      ],
    };
  }, [data]);

  if (tickers.length < 2) return <div className="cc-empty">pick ≥2 tickers (chips or `A B CORR`)…</div>;
  if (isLoading) return <div className="cc-empty">loading correlation…</div>;
  if (error || !data || !data.matrix.length) return <div className="cc-empty">no correlation data</div>;

  return (
    <div style={{ position: "absolute", inset: 0 }}>
      {data.clustered && (
        <span className="cc-muted" style={{ position: "absolute", top: 2, right: 8, fontSize: 10, zIndex: 2 }}>
          cluster-ordered
        </span>
      )}
      <EChart option={option} />
    </div>
  );
}
