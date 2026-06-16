/** Open panels + command-palette state. v1 uses a fixed grid with one instance per panel type
 *  (instanceId == panelId); dockview/multi-instance is an additive upgrade behind this store. */
import { create } from "zustand";

export interface PanelInstance {
  instanceId: string;
  panelId: string;
  config: Record<string, unknown>;
}

interface WorkspaceState {
  panels: PanelInstance[];
  paletteOpen: boolean;
  focused: string | null;
  openPanel: (panelId: string, defaultConfig?: Record<string, unknown>) => void;
  closePanel: (instanceId: string) => void;
  setConfig: (instanceId: string, patch: Record<string, unknown>) => void;
  focus: (instanceId: string) => void;
  setPaletteOpen: (open: boolean) => void;
}

export const useWorkspace = create<WorkspaceState>((set) => ({
  panels: [],
  paletteOpen: false,
  focused: null,
  openPanel: (panelId, defaultConfig = {}) =>
    set((s) => {
      const existing = s.panels.find((p) => p.panelId === panelId);
      if (existing) return { focused: existing.instanceId, paletteOpen: false };
      const instance: PanelInstance = { instanceId: panelId, panelId, config: { ...defaultConfig } };
      return { panels: [...s.panels, instance], focused: instance.instanceId, paletteOpen: false };
    }),
  closePanel: (instanceId) =>
    set((s) => ({ panels: s.panels.filter((p) => p.instanceId !== instanceId) })),
  setConfig: (instanceId, patch) =>
    set((s) => ({
      panels: s.panels.map((p) =>
        p.instanceId === instanceId ? { ...p, config: { ...p.config, ...patch } } : p,
      ),
    })),
  focus: (instanceId) => set({ focused: instanceId }),
  setPaletteOpen: (open) => set({ paletteOpen: open }),
}));
