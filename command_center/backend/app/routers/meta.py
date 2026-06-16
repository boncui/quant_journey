"""Service metadata — versions + available data sources (for drift detection & the StatusBar)."""

from __future__ import annotations

import quant_core
from fastapi import APIRouter, Depends
from quant_core.data import DatasetMeta

from .. import __version__ as backend_version
from ..deps import get_catalog
from ..schemas.common import MetaOut

router = APIRouter()


@router.get("/meta", response_model=MetaOut, operation_id="getMeta")
def get_meta(catalog: list[DatasetMeta] = Depends(get_catalog)) -> MetaOut:
    return MetaOut(
        version=backend_version,
        quant_core_version=quant_core.__version__,
        sources=sorted({m.source for m in catalog}),
    )
