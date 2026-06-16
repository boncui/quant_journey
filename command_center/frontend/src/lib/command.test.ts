import { describe, expect, it } from "vitest";

import { isTicker, parseCommand } from "./command";

const codes = new Set(["PX", "CORR", "RET"]);

describe("parseCommand", () => {
  it("ticker + code", () => {
    expect(parseCommand("AAPL PX", codes)).toEqual({ tickers: ["AAPL"], code: "PX", args: [] });
  });
  it("multi-ticker + code", () => {
    expect(parseCommand("AAPL MSFT CORR", codes)).toEqual({
      tickers: ["AAPL", "MSFT"],
      code: "CORR",
      args: [],
    });
  });
  it("code + args", () => {
    expect(parseCommand("SPY RET 1Y", codes)).toEqual({ tickers: ["SPY"], code: "RET", args: ["1Y"] });
  });
  it("bare code (case-insensitive)", () => {
    expect(parseCommand("corr", codes)).toEqual({ tickers: [], code: "CORR", args: [] });
  });
  it("bare ticker, no code", () => {
    expect(parseCommand("aapl", codes)).toEqual({ tickers: ["AAPL"], args: [] });
  });
});

describe("isTicker", () => {
  it("accepts valid tickers and rejects junk", () => {
    expect(isTicker("AAPL")).toBe(true);
    expect(isTicker("BRK.B")).toBe(true);
    expect(isTicker("A$B")).toBe(false);
  });
});
