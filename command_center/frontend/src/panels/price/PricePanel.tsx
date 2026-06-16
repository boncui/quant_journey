import { PriceChart } from "@/charts/PriceChart";
import type { PanelProps } from "@/lib/registry/types";
import { useSelection } from "@/store/selection";

import { usePrice } from "./usePrice";

export function PricePanel({ config, setConfig }: PanelProps) {
  const { activeTicker, period } = useSelection();
  const logScale = Boolean(config.logScale);
  const { data, isLoading, error } = usePrice(activeTicker, period);

  if (isLoading) return <div className="cc-empty">loading {activeTicker}…</div>;
  if (error) return <div className="cc-empty">error loading {activeTicker}</div>;
  if (!data || data.ohlcv.meta.empty) return <div className="cc-empty">no data for {activeTicker}</div>;

  return (
    <div style={{ position: "absolute", inset: 0 }}>
      <div style={{ position: "absolute", top: 4, left: 6, zIndex: 2, display: "flex", gap: 4 }}>
        <span className="cc-chip on">{activeTicker}</span>
        <span
          className={`cc-chip${logScale ? " on" : ""}`}
          onClick={() => setConfig({ logScale: !logScale })}
        >
          log
        </span>
        {data.ohlcv.meta.downsampled && <span className="cc-chip">downsampled</span>}
      </div>
      <PriceChart
        bars={data.ohlcv.bars}
        dividends={data.ca.dividends}
        splits={data.ca.splits}
        logScale={logScale}
      />
    </div>
  );
}
