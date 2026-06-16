import { useEffect, useMemo, useRef, useState } from "react";

import { parseCommand } from "@/lib/command";
import { allPanels, commandCodes, getPanelByCode } from "@/lib/registry/registry";
import { useSelection } from "@/store/selection";
import { useWorkspace } from "@/store/workspace";

export function CommandBar() {
  const open = useWorkspace((s) => s.paletteOpen);
  const setOpen = useWorkspace((s) => s.setPaletteOpen);
  const openPanel = useWorkspace((s) => s.openPanel);
  const setTickers = useSelection((s) => s.setTickers);
  const setActive = useSelection((s) => s.setActive);

  const [q, setQ] = useState("");
  const [idx, setIdx] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (open) {
      setQ("");
      setIdx(0);
      setTimeout(() => inputRef.current?.focus(), 0);
    }
  }, [open]);

  const parsed = useMemo(() => parseCommand(q, commandCodes()), [q]);
  const matches = useMemo(() => {
    const text = q.trim().toUpperCase();
    const panels = allPanels();
    if (!text) return panels;
    return panels.filter(
      (p) =>
        (parsed.code && p.commandCode === parsed.code) ||
        p.commandCode.includes(text) ||
        p.title.toUpperCase().includes(text),
    );
  }, [q, parsed.code]);

  if (!open) return null;

  const run = (panelId?: string) => {
    if (parsed.tickers.length) {
      setTickers(parsed.tickers);
      setActive(parsed.tickers[0]);
    }
    const byCode = parsed.code ? getPanelByCode(parsed.code) : undefined;
    const target = panelId
      ? allPanels().find((p) => p.id === panelId)
      : (byCode ?? matches[idx]);
    if (target) openPanel(target.id, target.defaultConfig);
    else setOpen(false);
  };

  return (
    <div className="cc-palette-backdrop" onClick={() => setOpen(false)}>
      <div className="cc-palette" onClick={(e) => e.stopPropagation()}>
        <input
          ref={inputRef}
          value={q}
          placeholder="ticker(s) + code  ·  e.g.  AAPL PX   ·   SPY KO AAPL CORR"
          onChange={(e) => {
            setQ(e.target.value);
            setIdx(0);
          }}
          onKeyDown={(e) => {
            if (e.key === "Escape") setOpen(false);
            else if (e.key === "ArrowDown") setIdx((i) => Math.min(i + 1, matches.length - 1));
            else if (e.key === "ArrowUp") setIdx((i) => Math.max(i - 1, 0));
            else if (e.key === "Enter") run();
          }}
        />
        <div>
          {matches.map((p, i) => (
            <div
              key={p.id}
              className={`cc-palette-item${i === idx ? " active" : ""}`}
              onMouseEnter={() => setIdx(i)}
              onClick={() => run(p.id)}
            >
              <span className="code">{p.commandCode}</span>
              <span>{p.title}</span>
              <span className="cc-muted" style={{ marginLeft: "auto" }}>
                {p.description}
              </span>
            </div>
          ))}
          {matches.length === 0 && <div className="cc-palette-item cc-muted">no matching panel</div>}
        </div>
      </div>
    </div>
  );
}
