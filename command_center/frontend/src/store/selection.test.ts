import { beforeEach, describe, expect, it } from "vitest";

import { periodToStart, useSelection } from "./selection";

describe("selection store", () => {
  beforeEach(() => {
    useSelection.setState({ tickers: ["SPY", "KO", "AAPL"], activeTicker: "AAPL", benchmark: "SPY", period: "5Y" });
  });

  it("setActive updates the active ticker", () => {
    useSelection.getState().setActive("KO");
    expect(useSelection.getState().activeTicker).toBe("KO");
  });

  it("toggleTicker removes then re-adds", () => {
    useSelection.getState().toggleTicker("KO");
    expect(useSelection.getState().tickers).not.toContain("KO");
    useSelection.getState().toggleTicker("KO");
    expect(useSelection.getState().tickers).toContain("KO");
  });
});

describe("periodToStart", () => {
  it("MAX -> undefined (no lower bound)", () => {
    expect(periodToStart("MAX")).toBeUndefined();
  });
  it("1Y subtracts one calendar year", () => {
    expect(periodToStart("1Y", new Date("2024-06-14T00:00:00Z"))).toBe("2023-06-14");
  });
});
