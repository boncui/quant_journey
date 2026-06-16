"""Factor construction & statistical arbitrage (beta/alpha now; cross-sectional later).

Public API (additive within 0.1.x):
    beta, alpha, rolling_beta, capm_fit, CAPMFit
"""

from __future__ import annotations

from .beta import CAPMFit, alpha, beta, capm_fit, rolling_beta

__all__ = ["beta", "alpha", "rolling_beta", "capm_fit", "CAPMFit"]
