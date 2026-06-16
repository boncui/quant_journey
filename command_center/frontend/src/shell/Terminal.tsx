import { useEffect } from "react";

import { type PeriodPreset, useSelection } from "@/store/selection";
import { useWorkspace } from "@/store/workspace";

import { CommandBar } from "./CommandBar";
import { PanelHost } from "./PanelHost";
import { StatusBar } from "./StatusBar";

const PERIODS: PeriodPreset[] = ["1M", "3M", "6M", "1Y", "5Y", "MAX"];

function isTypingTarget(target: EventTarget | null): boolean {
  const el = target as HTMLElement | null;
  return !!el && (el.tagName === "INPUT" || el.tagName === "TEXTAREA" || el.isContentEditable);
}

function PeriodChips() {
  const { period, setPeriod } = useSelection();
  return (
    <span style={{ display: "flex", gap: 2 }}>
      {PERIODS.map((p) => (
        <span
          key={p}
          className={`cc-chip${p === period ? " on" : ""}`}
          onClick={() => setPeriod(p)}
        >
          {p}
        </span>
      ))}
    </span>
  );
}

function UniverseChips() {
  const { tickers, activeTicker, setActive } = useSelection();
  return (
    <span style={{ display: "flex", gap: 2 }}>
      {tickers.map((t) => (
        <span
          key={t}
          className={`cc-chip${t === activeTicker ? " on" : ""}`}
          onClick={() => setActive(t)}
        >
          {t}
        </span>
      ))}
    </span>
  );
}

export function Terminal() {
  const panels = useWorkspace((s) => s.panels);
  const setPaletteOpen = useWorkspace((s) => s.setPaletteOpen);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (
        (e.key === ":" && !isTypingTarget(e.target)) ||
        ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k")
      ) {
        e.preventDefault();
        setPaletteOpen(true);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [setPaletteOpen]);

  return (
    <div className="cc-terminal">
      <div className="cc-topbar">
        <span className="cc-brand">command_center</span>
        <PeriodChips />
        <UniverseChips />
      </div>
      <div className="cc-grid">
        {panels.map((p) => (
          <PanelHost key={p.instanceId} {...p} />
        ))}
      </div>
      <StatusBar />
      <CommandBar />
    </div>
  );
}
