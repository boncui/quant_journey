import { useQuery } from "@tanstack/react-query";

import { api } from "@/lib/api/client";
import { type PeriodPreset, periodToStart } from "@/store/selection";

export function usePerformance(tickers: string[], period: PeriodPreset) {
  const start = periodToStart(period);
  const tickersParam = tickers.join(",");
  return useQuery({
    queryKey: ["performance", tickersParam, period],
    enabled: tickers.length > 0,
    queryFn: async () => {
      const { data, error } = await api.GET("/api/v1/performance", {
        params: { query: { tickers: tickersParam, start, base: 100 } },
      });
      if (error || !data) throw error ?? new Error("no performance");
      return data;
    },
  });
}
