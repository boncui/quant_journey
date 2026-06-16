"""Return-distribution analytics: histogram, moments, normality, QQ.

Pure-numpy paths (histogram, skew/kurtosis) stay in the base install. Scipy-backed paths
(normality p-values, QQ quantiles) need the ``quant-core[stats]`` extra and raise a clear
ImportError when it is absent (same pattern as the optional providers).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class Histogram:
    counts: list[float]
    bin_edges: list[float]
    bin_centers: list[float]
    density: bool


@dataclass(frozen=True)
class Moments:
    n: int
    mean: float
    std: float            # sample std, ddof=1
    skew: float           # biased (population) skewness — matches scipy.stats.skew default
    kurtosis_excess: float  # excess kurtosis (normal == 0)


@dataclass(frozen=True)
class NormalityFit:
    n: int
    mu: float
    sigma: float
    jb_stat: float
    jb_pvalue: float


@dataclass(frozen=True)
class QQData:
    theoretical: list[float]
    sample: list[float]
    slope: float
    intercept: float


def _clean(returns: pd.Series) -> np.ndarray:
    return pd.Series(returns).dropna().to_numpy(dtype=float)


def histogram(returns: pd.Series, *, bins: int | str = "fd", density: bool = True) -> Histogram:
    """Histogram with Freedman-Diaconis bins by default (robust to fat tails)."""
    x = _clean(returns)
    if x.size == 0:
        return Histogram(counts=[], bin_edges=[], bin_centers=[], density=density)
    counts, edges = np.histogram(x, bins=bins, density=density)
    centers = (edges[:-1] + edges[1:]) / 2.0
    return Histogram(
        counts=counts.tolist(),
        bin_edges=edges.tolist(),
        bin_centers=centers.tolist(),
        density=density,
    )


def moments(returns: pd.Series) -> Moments:
    """Mean, sample std (ddof=1), skewness, and **excess** kurtosis (pure numpy)."""
    x = _clean(returns)
    n = int(x.size)
    if n == 0:
        return Moments(n=0, mean=float("nan"), std=float("nan"), skew=float("nan"), kurtosis_excess=float("nan"))
    mean = float(x.mean())
    std = float(x.std(ddof=1)) if n > 1 else float("nan")
    m2 = float(((x - mean) ** 2).mean())
    if m2 == 0:
        return Moments(n=n, mean=mean, std=std, skew=0.0, kurtosis_excess=-3.0)
    m3 = float(((x - mean) ** 3).mean())
    m4 = float(((x - mean) ** 4).mean())
    skew = m3 / m2**1.5
    kurt_excess = m4 / m2**2 - 3.0
    return Moments(n=n, mean=mean, std=std, skew=skew, kurtosis_excess=kurt_excess)


def normality(returns: pd.Series) -> NormalityFit:
    """Jarque-Bera normality test + fitted Normal params. Needs ``quant-core[stats]`` (scipy)."""
    try:
        from scipy import stats as ss
    except ModuleNotFoundError as exc:  # pragma: no cover - import guard
        raise ModuleNotFoundError(
            "normality() needs scipy. Install the extra: `uv add 'quant-core[stats]'`."
        ) from exc
    x = _clean(returns)
    if x.size < 2:
        return NormalityFit(n=int(x.size), mu=float("nan"), sigma=float("nan"), jb_stat=float("nan"), jb_pvalue=float("nan"))
    jb = ss.jarque_bera(x)
    return NormalityFit(
        n=int(x.size), mu=float(x.mean()), sigma=float(x.std(ddof=1)),
        jb_stat=float(jb.statistic), jb_pvalue=float(jb.pvalue),
    )


def qq_points(returns: pd.Series, dist: str = "norm") -> QQData:
    """Theoretical vs sample quantiles for a QQ plot. Needs ``quant-core[stats]`` (scipy)."""
    try:
        from scipy import stats as ss
    except ModuleNotFoundError as exc:  # pragma: no cover - import guard
        raise ModuleNotFoundError(
            "qq_points() needs scipy. Install the extra: `uv add 'quant-core[stats]'`."
        ) from exc
    x = _clean(returns)
    if x.size < 2:
        return QQData(theoretical=[], sample=[], slope=float("nan"), intercept=float("nan"))
    (osm, osr), (slope, intercept, _r) = ss.probplot(x, dist=dist, fit=True)
    return QQData(theoretical=osm.tolist(), sample=osr.tolist(), slope=float(slope), intercept=float(intercept))
