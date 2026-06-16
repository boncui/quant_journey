import { useSelection } from "@/store/selection";
import { useWorkspace } from "@/store/workspace";

export function StatusBar() {
  const { activeTicker, benchmark, period, tickers } = useSelection();
  const panelCount = useWorkspace((s) => s.panels.length);
  return (
    <div className="cc-statusbar">
      <span>
        active <b className="cc-up">{activeTicker}</b>
      </span>
      <span>bench {benchmark}</span>
      <span>period {period}</span>
      <span className="cc-muted">universe {tickers.join(" ")}</span>
      <span style={{ marginLeft: "auto" }} className="cc-muted">
        {panelCount} panels · press <b>:</b> for commands
      </span>
    </div>
  );
}
