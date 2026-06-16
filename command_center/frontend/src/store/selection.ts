/** The cross-panel linking bus. Brushing/selecting in one panel updates this; every panel reads it
 *  so the terminal behaves like Bloomberg (select in one, others follow). */
import { create } from "zustand";

export type PeriodPreset = "1M" | "3M" | "6M" | "1Y" | "5Y" | "MAX";

export interface SelectionState {
  tickers: string[];
  activeTicker: string;
  benchmark: string;
  period: PeriodPreset;
  setActive: (ticker: string) => void;
  toggleTicker: (ticker: string) => void;
  setTickers: (tickers: string[]) => void;
  setBenchmark: (ticker: string) => void;
  setPeriod: (period: PeriodPreset) => void;
}

export const useSelection = create<SelectionState>((set) => ({
  tickers: ["SPY", "KO", "AAPL"],
  activeTicker: "AAPL",
  benchmark: "SPY",
  period: "5Y",
  setActive: (ticker) => set({ activeTicker: ticker }),
  toggleTicker: (ticker) =>
    set((s) => ({
      tickers: s.tickers.includes(ticker)
        ? s.tickers.filter((t) => t !== ticker)
        : [...s.tickers, ticker],
    })),
  setTickers: (tickers) => set({ tickers }),
  setBenchmark: (ticker) => set({ benchmark: ticker }),
  setPeriod: (period) => set({ period }),
}));

/** Period preset -> ISO start date (relative to `end`, default today). Pure + tested. */
export function periodToStart(period: PeriodPreset, end: Date = new Date()): string | undefined {
  const d = new Date(end);
  switch (period) {
    case "1M": d.setMonth(d.getMonth() - 1); break;
    case "3M": d.setMonth(d.getMonth() - 3); break;
    case "6M": d.setMonth(d.getMonth() - 6); break;
    case "1Y": d.setFullYear(d.getFullYear() - 1); break;
    case "5Y": d.setFullYear(d.getFullYear() - 5); break;
    case "MAX": return undefined;
  }
  return d.toISOString().slice(0, 10);
}
