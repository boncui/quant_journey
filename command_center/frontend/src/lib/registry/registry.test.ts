import { beforeEach, describe, expect, it } from "vitest";

import { _clearRegistry, allPanels, getPanelByCode, getPanelById, registerPanel } from "./registry";
import type { PanelDefinition } from "./types";

const mk = (id: string, code: string): PanelDefinition => ({
  id,
  title: id,
  commandCode: code,
  description: "",
  category: "data",
  needs: "none",
  component: () => null,
});

describe("panel registry", () => {
  beforeEach(() => _clearRegistry());

  it("registers and looks up by id and (case-insensitive) code", () => {
    registerPanel(mk("a.b", "AB"));
    expect(getPanelById("a.b")?.commandCode).toBe("AB");
    expect(getPanelByCode("ab")?.id).toBe("a.b");
    expect(allPanels()).toHaveLength(1);
  });

  it("rejects a duplicate id", () => {
    registerPanel(mk("dup", "A"));
    expect(() => registerPanel(mk("dup", "B"))).toThrow(/Duplicate panel id/);
  });

  it("rejects a duplicate command code", () => {
    registerPanel(mk("x", "C"));
    expect(() => registerPanel(mk("y", "C"))).toThrow(/Duplicate command code/);
  });
});
