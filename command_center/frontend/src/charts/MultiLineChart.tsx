import { createChart, type IChartApi, type UTCTimestamp } from "lightweight-charts";
import { useEffect, useRef } from "react";

import { lwcOptions } from "@/theme/chartTheme";

export interface LineSeriesData {
  name: string;
  color: string;
  points: { t: number; v: number | null }[];
}

const sec = (t: number) => (t / 1000) as UTCTimestamp;

export function MultiLineChart({ series }: { series: LineSeriesData[] }) {
  const ref = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);

  useEffect(() => {
    if (!ref.current) return;
    const chart = createChart(ref.current, { ...lwcOptions(), autoSize: true });
    chartRef.current = chart;
    for (const s of series) {
      const line = chart.addLineSeries({ color: s.color, lineWidth: 2, priceLineVisible: false });
      line.setData(
        s.points.filter((p) => p.v != null).map((p) => ({ time: sec(p.t), value: p.v! })),
      );
    }
    chart.timeScale().fitContent();
    return () => {
      chart.remove();
      chartRef.current = null;
    };
  }, [series]);

  return <div ref={ref} className="cc-chart" />;
}
