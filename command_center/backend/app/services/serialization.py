"""Turn pandas series/frames into compact, JSON-safe wire points (with downsampling)."""

from __future__ import annotations

import math

import numpy as np
import pandas as pd

from ..schemas.common import Point
from .downsample import select_indices


def epoch_ms(ts) -> int:
    return int(pd.Timestamp(ts).timestamp() * 1000)


def jnum(x) -> float | None:
    """JSON-safe number: NaN/inf/None -> None (so gaps serialize as null, not invalid JSON)."""
    if x is None:
        return None
    try:
        xf = float(x)
    except (TypeError, ValueError):
        return None
    return xf if math.isfinite(xf) else None


def series_points(dates, values, *, max_points: int) -> tuple[list[Point], int, int, bool]:
    """Build downsampled ``Point``s. Returns ``(points, n_raw, n_returned, downsampled)``."""
    idx = pd.DatetimeIndex(pd.to_datetime(dates, utc=True))
    vals = np.asarray(values, dtype=float)
    n_raw = len(vals)
    if n_raw == 0:
        return [], 0, 0, False
    keep = select_indices(vals, max_points)
    pts = [Point(t=epoch_ms(idx[i]), v=jnum(vals[i])) for i in keep]
    return pts, n_raw, len(pts), len(pts) < n_raw


def tidy_points(tidy: pd.DataFrame, value_col: str, *, max_points: int) -> tuple[list[Point], int, int, bool]:
    """Points from a single-ticker tidy frame ``[date, ..., value_col]`` (sorted by date)."""
    if tidy.empty:
        return [], 0, 0, False
    t = tidy.sort_values("date")
    return series_points(t["date"], t[value_col], max_points=max_points)
