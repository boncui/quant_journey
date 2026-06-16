import type { ComponentType } from "react";

export type PanelCategory = "data" | "price" | "stats" | "risk" | "factor" | "live";

/** What data the panel reads — drives the "needs a ticker / needs a universe" hint. */
export type DataNeed = "none" | "single" | "multi" | "universe";

export interface PanelProps {
  instanceId: string;
  config: Record<string, unknown>;
  setConfig: (patch: Record<string, unknown>) => void;
}

/** The whole contract a new panel implements. A panel is one folder under src/panels/<name>/
 *  whose index.ts calls registerPanel({...}); nothing in core changes. */
export interface PanelDefinition {
  id: string;
  title: string;
  commandCode: string;            // Bloomberg-style mnemonic, e.g. "PX"
  description: string;
  category: PanelCategory;
  needs: DataNeed;
  defaultConfig?: Record<string, unknown>;
  component: ComponentType<PanelProps>;
}
