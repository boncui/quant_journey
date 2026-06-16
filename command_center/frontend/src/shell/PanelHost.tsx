import { getPanelById } from "@/lib/registry/registry";
import { useWorkspace } from "@/store/workspace";

export function PanelHost({
  instanceId,
  panelId,
  config,
}: {
  instanceId: string;
  panelId: string;
  config: Record<string, unknown>;
}) {
  const def = getPanelById(panelId);
  const setConfig = useWorkspace((s) => s.setConfig);
  const closePanel = useWorkspace((s) => s.closePanel);

  if (!def) {
    return <div className="cc-empty">Unknown panel: {panelId}</div>;
  }
  const Component = def.component;
  return (
    <div className="cc-panel">
      <div className="cc-panel-head">
        <span>
          <span className="cc-panel-title">{def.title}</span>{" "}
          <span className="cc-panel-code">{def.commandCode}</span>
        </span>
        <span
          className="cc-chip"
          role="button"
          aria-label={`close ${def.title}`}
          onClick={() => closePanel(instanceId)}
        >
          ×
        </span>
      </div>
      <div className="cc-panel-body">
        <Component
          instanceId={instanceId}
          config={config}
          setConfig={(patch) => setConfig(instanceId, patch)}
        />
      </div>
    </div>
  );
}
