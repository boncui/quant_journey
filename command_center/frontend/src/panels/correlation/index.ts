import { registerPanel } from "@/lib/registry/registry";

import { CorrelationPanel } from "./CorrelationPanel";

registerPanel({
  id: "correlation.matrix",
  title: "Correlation & Covariance",
  commandCode: "CORR",
  description: "return-correlation heatmap, hierarchically clustered",
  category: "factor",
  needs: "universe",
  component: CorrelationPanel,
});
