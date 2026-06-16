import { registerPanel } from "@/lib/registry/registry";

import { PricePanel } from "./PricePanel";

registerPanel({
  id: "price.corporate_actions",
  title: "Price & Corporate Actions",
  commandCode: "PX",
  description: "candles, volume, adj close, dividend/split markers, log scale",
  category: "price",
  needs: "single",
  defaultConfig: { logScale: false },
  component: PricePanel,
});
