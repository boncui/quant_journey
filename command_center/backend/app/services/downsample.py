"""Server-side downsampling so the wire stays small as series grow toward tick scale.

v1 uses min/max bucketing (preserves visual extremes — wicks, spikes — far better than naive
striding). The same shape serves 252 daily bars and millions of ticks; only the bucket count
changes. (Full LTTB is a later, additive upgrade behind this same function.)
"""

from __future__ import annotations

import numpy as np


def select_indices(values: np.ndarray, max_points: int) -> np.ndarray:
    """Return sorted row indices to keep so the series has <= ``max_points`` points.

    Always keeps the first and last point, plus the argmin and argmax within each bucket so peaks
    and troughs survive. Returns all indices unchanged when the series already fits.
    """
    n = len(values)
    if max_points <= 0 or n <= max_points:
        return np.arange(n)

    n_buckets = max(1, max_points // 2)
    edges = np.linspace(0, n, n_buckets + 1).astype(int)
    keep: set[int] = {0, n - 1}
    finite = np.isfinite(values)
    for i in range(n_buckets):
        lo, hi = int(edges[i]), int(edges[i + 1])
        if hi <= lo:
            continue
        seg_finite = finite[lo:hi]
        if not seg_finite.any():
            keep.add(lo)
            continue
        seg = np.where(seg_finite, values[lo:hi], np.nan)
        keep.add(lo + int(np.nanargmin(seg)))
        keep.add(lo + int(np.nanargmax(seg)))
    return np.array(sorted(keep))
