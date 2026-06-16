import { registerPanel } from "@/lib/registry/registry";

import { PerformancePanel } from "./PerformancePanel";

registerPanel({
  id: "performance.overlay",
  title: "Performance Overlay",
  commandCode: "PERF",
  description: "multi-ticker cumulative returns rebased to 100",
  category: "stats",
  needs: "multi",
  component: PerformancePanel,
});
