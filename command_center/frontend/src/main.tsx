import { QueryClientProvider } from "@tanstack/react-query";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import { App } from "@/App";
import { queryClient } from "@/lib/api/queryClient";
import "@/lib/registry/autoload"; // side effect: registers every panel under src/panels
import { useWorkspace } from "@/store/workspace";
import "@/theme/tokens.css";

// Default workspace: the full Standard-v1 panel set in a dense grid.
const ws = useWorkspace.getState();
ws.openPanel("data.catalog");
ws.openPanel("price.corporate_actions");
ws.openPanel("performance.overlay");
ws.openPanel("returns.distribution");
ws.openPanel("rolling.stats");
ws.openPanel("correlation.matrix");

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </StrictMode>,
);
