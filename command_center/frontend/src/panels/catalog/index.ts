import { registerPanel } from "@/lib/registry/registry";

import { CatalogPanel } from "./CatalogPanel";

registerPanel({
  id: "data.catalog",
  title: "Data Catalog & Health",
  commandCode: "DATA",
  description: "datasets across projects + cache, coverage & freshness",
  category: "data",
  needs: "none",
  component: CatalogPanel,
});
