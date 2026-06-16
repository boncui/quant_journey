"""Write the OpenAPI schema to a file (offline, no server) for committed, reviewable type-gen.

`make openapi-dump` -> command_center/backend/openapi.json; the frontend generates TS types from it.
"""

from __future__ import annotations

import json
from pathlib import Path

from .main import create_app


def main() -> int:
    spec = create_app().openapi()
    out = Path(__file__).resolve().parents[1] / "openapi.json"
    out.write_text(json.dumps(spec, indent=2, sort_keys=True))
    print(f"Wrote {out} ({len(spec.get('paths', {}))} paths).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
