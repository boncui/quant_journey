import { useQuery } from "@tanstack/react-query";

import { api } from "@/lib/api/client";
import { type PeriodPreset, periodToStart } from "@/store/selection";

export function useDistribution(ticker: string, period: PeriodPreset) {
  const start = periodToStart(period);
  return useQuery({
    queryKey: ["distribution", ticker, period],
    queryFn: async () => {
      const { data, error } = await api.GET("/api/v1/distribution/{ticker}", {
        params: { path: { ticker }, query: { start, kind: "log" } },
      });
      if (error || !data) throw error ?? new Error("no distribution");
      return data;
    },
  });
}
