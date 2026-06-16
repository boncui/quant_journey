"""quant_core — the shared mini-library for the 100-project quant journey.

Reusable logic graduates into this package; each ``NNN_*`` project folder is a thin
runnable app + report on top of it. Projects depend on a pinned version range
(e.g. ``quant-core>=0.1,<0.2``) so that a breaking change here surfaces loudly
in older projects rather than silently breaking them.

API-evolution policy (semver):
- Within a minor (0.1.x): additive only — never rename or remove public API.
- Breaking changes bump the minor (0.1 -> 0.2); projects opt in by widening their pin.
"""

__version__ = "0.1.1"
