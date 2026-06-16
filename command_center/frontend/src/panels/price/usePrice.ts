import { useQuery } from "@tanstack/react-query";

import { api } from "@/lib/api/client";
import { type PeriodPreset, periodToStart } from "@/store/selection";

export function usePrice(ticker: string, period: PeriodPreset) {
  const start = periodToStart(period);
  return useQuery({
    queryKey: ["ohlcv", ticker, period],
    queryFn: async () => {
      const ohlcv = await api.GET("/api/v1/ohlcv/{ticker}", {
        params: { path: { ticker }, query: { start } },
      });
      const ca = await api.GET("/api/v1/corporate-actions/{ticker}", {
        params: { path: { ticker }, query: { start } },
      });
      if (ohlcv.error || !ohlcv.data) throw ohlcv.error ?? new Error("no ohlcv");
      if (ca.error || !ca.data) throw ca.error ?? new Error("no corporate actions");
      return { ohlcv: ohlcv.data, ca: ca.data };
    },
  });
}
