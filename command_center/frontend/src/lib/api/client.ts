/** Typed API client. `paths` is GENERATED from the backend OpenAPI schema (npm run api:gen) —
 *  never hand-edit src/lib/api/schema.d.ts. baseUrl is "" so paths include /api/v1 and the Vite
 *  dev proxy forwards them to FastAPI. */
import createClient from "openapi-fetch";

import type { paths } from "./schema";

export const api = createClient<paths>({ baseUrl: "" });
