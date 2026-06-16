import type { EChartsOption } from "echarts";
import * as echarts from "echarts";
import { useEffect, useRef } from "react";

/** Generic ECharts wrapper: lifecycle + resize + dispose. Statistical charts (histogram, QQ,
 *  heatmap, dendrogram) live here; time-series-at-scale uses Lightweight-Charts instead. */
export function EChart({ option }: { option: EChartsOption }) {
  const ref = useRef<HTMLDivElement>(null);
  const chartRef = useRef<echarts.ECharts | null>(null);

  useEffect(() => {
    if (!ref.current) return;
    const chart = echarts.init(ref.current, undefined, { renderer: "canvas" });
    chartRef.current = chart;
    const ro = new ResizeObserver(() => chart.resize());
    ro.observe(ref.current);
    return () => {
      ro.disconnect();
      chart.dispose();
      chartRef.current = null;
    };
  }, []);

  useEffect(() => {
    chartRef.current?.setOption(option, true);
  }, [option]);

  return <div ref={ref} className="cc-chart" />;
}
