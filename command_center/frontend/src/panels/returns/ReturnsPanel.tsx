import type { EChartsOption } from "echarts";
import { useMemo } from "react";

import { EChart } from "@/charts/EChart";
import { num } from "@/lib/format";
import { useSelection } from "@/store/selection";
import { tokens } from "@/theme/chartTheme";

import { useDistribution } from "./useDistribution";

function normalPdf(x: number, mu: number, sigma: number): number {
  return (1 / (sigma * Math.sqrt(2 * Math.PI))) * Math.exp(-0.5 * ((x - mu) / sigma) ** 2);
}

export function ReturnsPanel() {
  const { activeTicker, period } = useSelection();
  const { data, isLoading, error } = useDistribution(activeTicker, period);

  const option = useMemo<EChartsOption>(() => {
    if (!data) return {};
    const t = tokens();
    const h = data.histogram;
    const pdf =
      data.normal != null
        ? h.bin_centers.map((x) => normalPdf(x, data.normal!.mu, data.normal!.sigma))
        : [];
    return {
      backgroundColor: "transparent",
      grid: { left: 44, right: 12, top: 28, bottom: 20 },
      tooltip: { trigger: "axis" },
      xAxis: {
        type: "category",
        data: h.bin_centers.map((x) => x.toFixed(3)),
        axisLabel: { color: t.muted, show: false },
        axisLine: { lineStyle: { color: t.border } },
      },
      yAxis: {
        type: "value",
        axisLabel: { color: t.muted, fontSize: 9 },
        splitLine: { lineStyle: { color: t.border } },
      },
      series: [
        { type: "bar", data: h.counts, itemStyle: { color: t.series[0] }, barWidth: "99%", name: "empirical" },
        ...(pdf.length
          ? [{ type: "line" as const, data: pdf, smooth: true, showSymbol: false, lineStyle: { color: t.amber, width: 2 }, name: "normal" }]
          : []),
      ],
    };
  }, [data]);

  if (isLoading) return <div className="cc-empty">loading {activeTicker}…</div>;
  if (error) return <div className="cc-empty">error loading distribution</div>;
  if (!data || data.meta.empty) return <div className="cc-empty">no data for {activeTicker}</div>;

  const m = data.moments;
  return (
    <div style={{ position: "absolute", inset: 0, display: "flex", flexDirection: "column" }}>
      <div style={{ display: "flex", gap: 12, padding: "2px 8px", fontSize: 11 }} className="cc-muted">
        <span>n {m.n}</span>
        <span>skew <b className={Number(m.skew) < 0 ? "cc-down" : "cc-up"}>{num(m.skew)}</b></span>
        <span>kurt <b>{num(m.kurtosis_excess)}</b></span>
        {data.normal && <span>JB p <b>{num(data.normal.jb_pvalue, 3)}</b></span>}
        <span className="cc-muted">log returns vs Normal</span>
      </div>
      <div style={{ position: "relative", flex: 1 }}>
        <EChart option={option} />
      </div>
    </div>
  );
}
