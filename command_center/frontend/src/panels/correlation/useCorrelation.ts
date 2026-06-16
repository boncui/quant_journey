import { useQuery } from "@tanstack/react-query";

import { api } from "@/lib/api/client";
import { type PeriodPreset, periodToStart } from "@/store/selection";

export function useCorrelation(tickers: string[], period: PeriodPreset) {
  const start = periodToStart(period);
  const tickersParam = tickers.join(",");
  return useQuery({
    queryKey: ["correlation", tickersParam, period],
    enabled: tickers.length >= 2,
    queryFn: async () => {
      const { data, error } = await api.GET("/api/v1/correlation", {
        params: { query: { tickers: tickersParam, start, cluster: true } },
      });
      if (error || !data) throw error ?? new Error("no correlation");
      return data;
    },
  });
}
