import { registerPanel } from "@/lib/registry/registry";

import { RollingPanel } from "./RollingPanel";

registerPanel({
  id: "rolling.stats",
  title: "Rolling Statistics",
  commandCode: "ROLL",
  description: "rolling volatility / Sharpe / mean (annualized)",
  category: "stats",
  needs: "single",
  defaultConfig: { stat: "vol", window: 21 },
  component: RollingPanel,
});
