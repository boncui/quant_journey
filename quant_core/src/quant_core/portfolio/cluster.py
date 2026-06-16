"""Hierarchical clustering of a correlation matrix — for block-ordered heatmaps & dendrograms.

Uses the López de Prado correlation distance ``d = sqrt(0.5 * (1 - corr))``. Scipy-backed, so it
needs the ``quant-core[stats]`` extra; returns ordering/linkage DATA only (no plotting).
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def _linkage(corr: pd.DataFrame, method: str):
    try:
        from scipy.cluster.hierarchy import linkage
        from scipy.spatial.distance import squareform
    except ModuleNotFoundError as exc:  # pragma: no cover - import guard
        raise ModuleNotFoundError(
            "cluster ordering needs scipy. Install the extra: `uv add 'quant-core[stats]'`."
        ) from exc
    dist = np.sqrt(np.clip(0.5 * (1.0 - corr.to_numpy()), 0.0, None))
    np.fill_diagonal(dist, 0.0)
    condensed = squareform(dist, checks=False)
    return linkage(condensed, method=method)


def cluster_order(corr: pd.DataFrame, *, method: str = "ward") -> list[str]:
    """Leaf order from hierarchical clustering so a reordered heatmap shows correlation blocks."""
    if corr.shape[0] <= 2:
        return [str(c) for c in corr.columns]
    from scipy.cluster.hierarchy import leaves_list

    order = leaves_list(_linkage(corr, method))
    return [str(corr.columns[i]) for i in order]


def linkage_matrix(corr: pd.DataFrame, *, method: str = "ward"):
    """Raw scipy linkage matrix (for an optional dendrogram panel)."""
    return _linkage(corr, method)
