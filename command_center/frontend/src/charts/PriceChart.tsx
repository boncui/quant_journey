import { createChart, type IChartApi, PriceScaleMode, type UTCTimestamp } from "lightweight-charts";
import { useEffect, useRef } from "react";

import { lwcOptions, tokens } from "@/theme/chartTheme";

export interface Bar {
  t: number;
  o: number | null;
  h: number | null;
  low: number | null;
  c: number | null;
  adj: number | null;
  v: number | null;
}
export interface Marker {
  t: number;
  kind: string;
  value: number;
}

interface Props {
  bars: Bar[];
  dividends?: Marker[];
  splits?: Marker[];
  logScale?: boolean;
  showVolume?: boolean;
  showAdj?: boolean;
}

const sec = (t: number) => (t / 1000) as UTCTimestamp;

export function PriceChart({
  bars,
  dividends = [],
  splits = [],
  logScale = false,
  showVolume = true,
  showAdj = true,
}: Props) {
  const ref = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);

  useEffect(() => {
    if (!ref.current) return;
    const t = tokens();
    const chart = createChart(ref.current, { ...lwcOptions(), autoSize: true });
    chartRef.current = chart;

    const candle = chart.addCandlestickSeries({
      upColor: t.up,
      downColor: t.down,
      borderVisible: false,
      wickUpColor: t.up,
      wickDownColor: t.down,
    });
    candle.setData(
      bars
        .filter((b) => b.c != null && b.o != null && b.h != null && b.low != null)
        .map((b) => ({ time: sec(b.t), open: b.o!, high: b.h!, low: b.low!, close: b.c! })),
    );

    if (showAdj) {
      const adj = chart.addLineSeries({
        color: t.amber,
        lineWidth: 1,
        priceLineVisible: false,
        lastValueVisible: false,
      });
      adj.setData(bars.filter((b) => b.adj != null).map((b) => ({ time: sec(b.t), value: b.adj! })));
    }

    if (showVolume) {
      const vol = chart.addHistogramSeries({
        priceScaleId: "vol",
        priceFormat: { type: "volume" },
        color: t.border,
      });
      chart.priceScale("vol").applyOptions({ scaleMargins: { top: 0.85, bottom: 0 } });
      vol.setData(bars.filter((b) => b.v != null).map((b) => ({ time: sec(b.t), value: b.v! })));
    }

    candle.setMarkers(
      [
        ...dividends.map((d) => ({
          time: sec(d.t),
          position: "belowBar" as const,
          color: t.up,
          shape: "circle" as const,
          text: `D ${d.value}`,
        })),
        ...splits.map((s) => ({
          time: sec(s.t),
          position: "aboveBar" as const,
          color: t.down,
          shape: "arrowDown" as const,
          text: `${s.value}:1`,
        })),
      ].sort((a, b) => (a.time as number) - (b.time as number)),
    );

    chart.applyOptions({
      rightPriceScale: {
        mode: logScale ? PriceScaleMode.Logarithmic : PriceScaleMode.Normal,
        borderColor: t.border,
      },
    });
    chart.timeScale().fitContent();

    return () => {
      chart.remove();
      chartRef.current = null;
    };
  }, [bars, dividends, splits, logScale, showVolume, showAdj]);

  return <div ref={ref} className="cc-chart" />;
}
