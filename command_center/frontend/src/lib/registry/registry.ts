import type { PanelDefinition } from "./types";

const byId = new Map<string, PanelDefinition>();
const byCode = new Map<string, PanelDefinition>();

/** Called at import time by each panel's index.ts. Throws on id/commandCode collision. */
export function registerPanel(def: PanelDefinition): void {
  if (byId.has(def.id)) throw new Error(`Duplicate panel id: ${def.id}`);
  const code = def.commandCode.toUpperCase();
  if (byCode.has(code)) throw new Error(`Duplicate command code: ${code}`);
  byId.set(def.id, def);
  byCode.set(code, def);
}

export const getPanelById = (id: string): PanelDefinition | undefined => byId.get(id);
export const getPanelByCode = (code: string): PanelDefinition | undefined =>
  byCode.get(code.toUpperCase());
export const allPanels = (): PanelDefinition[] => [...byId.values()];
export const commandCodes = (): Set<string> => new Set(byCode.keys());

/** Test-only: reset the registry between unit tests. */
export function _clearRegistry(): void {
  byId.clear();
  byCode.clear();
}
