import { useQuery } from "@tanstack/react-query";

import { api } from "@/lib/api/client";
import { type PeriodPreset, periodToStart } from "@/store/selection";

export type RollingStat = "vol" | "mean" | "sharpe";

export function useRolling(ticker: string, period: PeriodPreset, window: number, stat: RollingStat) {
  const start = periodToStart(period);
  return useQuery({
    queryKey: ["rolling", ticker, period, window, stat],
    queryFn: async () => {
      const { data, error } = await api.GET("/api/v1/rolling/{ticker}", {
        params: { path: { ticker }, query: { start, window, stat } },
      });
      if (error || !data) throw error ?? new Error("no rolling");
      return data;
    },
  });
}
