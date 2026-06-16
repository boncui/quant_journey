/** Command-bar grammar: "<TICKERS> <CODE> [args]".
 *   "AAPL PX"          -> { tickers: [AAPL], code: PX }
 *   "AAPL MSFT CORR"   -> { tickers: [AAPL, MSFT], code: CORR }
 *   "SPY RET 1Y"       -> { tickers: [SPY], code: RET, args: [1Y] }
 *   "CORR"             -> { code: CORR }
 *   "AAPL"             -> { tickers: [AAPL] }
 */
export interface ParsedCommand {
  tickers: string[];
  code?: string;
  args: string[];
}

const TICKER_RE = /^[A-Z0-9.\-]{1,15}$/;

export function isTicker(token: string): boolean {
  return TICKER_RE.test(token);
}

export function parseCommand(input: string, codes: Set<string>): ParsedCommand {
  const toks = input.trim().toUpperCase().split(/\s+/).filter(Boolean);
  let codeIdx = -1;
  for (let i = 0; i < toks.length; i++) {
    if (codes.has(toks[i])) codeIdx = i;
  }
  if (codeIdx === -1) {
    return { tickers: toks.filter(isTicker), args: [] };
  }
  return {
    tickers: toks.slice(0, codeIdx).filter(isTicker),
    code: toks[codeIdx],
    args: toks.slice(codeIdx + 1),
  };
}
