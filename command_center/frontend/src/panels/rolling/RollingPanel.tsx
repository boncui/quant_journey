import type { EChartsOption } from "echarts";
import { useMemo } from "react";

import { EChart } from "@/charts/EChart";
import type { PanelProps } from "@/lib/registry/types";
import { useSelection } from "@/store/selection";
import { tokens } from "@/theme/chartTheme";

import { type RollingStat, useRolling } from "./useRolling";

const STATS: RollingStat[] = ["vol", "sharpe", "mean"];

export function RollingPanel({ config, setConfig }: PanelProps) {
  const { activeTicker, period } = useSelection();
  const stat = (config.stat as RollingStat) ?? "vol";
  const window = (config.window as number) ?? 21;
  const { data, isLoading, error } = useRolling(activeTicker, period, window, stat);

  const option = useMemo<EChartsOption>(() => {
    if (!data) return {};
    const t = tokens();
    return {
      backgroundColor: "transparent",
      grid: { left: 50, right: 12, top: 28, bottom: 22 },
      tooltip: { trigger: "axis" },
      xAxis: { type: "time", axisLabel: { color: t.muted, fontSize: 9 }, axisLine: { lineStyle: { color: t.border } } },
      yAxis: { type: "value", scale: true, axisLabel: { color: t.muted, fontSize: 9 }, splitLine: { lineStyle: { color: t.border } } },
      series: [
        {
          type: "line",
          showSymbol: false,
          connectNulls: false,
          data: data.series.map((p) => [p.t, p.v]),
          lineStyle: { color: t.series[2], width: 1.5 },
        },
      ],
    };
  }, [data]);

  return (
    <div style={{ position: "absolute", inset: 0, display: "flex", flexDirection: "column" }}>
      <div style={{ display: "flex", gap: 4, padding: "2px 8px" }}>
        <span className="cc-chip on">{activeTicker}</span>
        {STATS.map((s) => (
          <span
            key={s}
            className={`cc-chip${s === stat ? " on" : ""}`}
            onClick={() => setConfig({ stat: s })}
          >
            {s}
          </span>
        ))}
        <span className="cc-muted" style={{ fontSize: 10, alignSelf: "center" }}>
          {window}-period{data?.annualized ? " · annualized" : ""}
        </span>
      </div>
      <div style={{ position: "relative", flex: 1 }}>
        {isLoading ? (
          <div className="cc-empty">loading…</div>
        ) : error || !data || data.meta.empty ? (
          <div className="cc-empty">no data for {activeTicker}</div>
        ) : (
          <EChart option={option} />
        )}
      </div>
    </div>
  );
}
