import { bytes, ymd } from "@/lib/format";
import { useSelection } from "@/store/selection";

import { useCatalog } from "./useCatalog";

export function CatalogPanel() {
  const { data, isLoading, error } = useCatalog();
  const setActive = useSelection((s) => s.setActive);
  const active = useSelection((s) => s.activeTicker);

  if (isLoading) return <div className="cc-empty">loading catalog…</div>;
  if (error) return <div className="cc-empty">catalog error — is the backend running?</div>;
  if (!data || data.empty) {
    return <div className="cc-empty">{data?.hint ?? "No datasets. Run `make cc-seed`."}</div>;
  }

  return (
    <table className="cc-table">
      <thead>
        <tr>
          <th>source</th>
          <th>ticker</th>
          <th className="num">rows</th>
          <th>span</th>
          <th className="num">size</th>
        </tr>
      </thead>
      <tbody>
        {data.items.flatMap((m, i) =>
          m.tickers.map((t) => (
            <tr
              key={`${i}-${t}`}
              className={`cc-row${t === active ? " sel" : ""}`}
              onClick={() => setActive(t)}
            >
              <td className="cc-muted">{m.source}</td>
              <td>{t}</td>
              <td className="num">{m.n_rows.toLocaleString()}</td>
              <td className="cc-muted">
                {ymd(m.start)} → {ymd(m.end)}
              </td>
              <td className="num cc-muted">{bytes(m.n_bytes)}</td>
            </tr>
          )),
        )}
      </tbody>
    </table>
  );
}
