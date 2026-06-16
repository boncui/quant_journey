import { registerPanel } from "@/lib/registry/registry";

import { ReturnsPanel } from "./ReturnsPanel";

registerPanel({
  id: "returns.distribution",
  title: "Returns & Distribution",
  commandCode: "RET",
  description: "log-return histogram vs Normal, skew/kurtosis, JB test",
  category: "stats",
  needs: "single",
  component: ReturnsPanel,
});
