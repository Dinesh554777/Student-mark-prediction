"""Training routes for model retraining."""

import os
import sys
from fastapi import APIRouter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import RetrainResponse, MetricsResponse
from backend.ml_engine import retrain_model

router = APIRouter(prefix="/api/model", tags=["Model"])


@router.post("/retrain", response_model=RetrainResponse)
async def retrain():
    """Retrain the ML model."""
    result = retrain_model()
    old = result.pop("old_metrics", None)
    return RetrainResponse(
        message="Model retrained successfully!",
        old_metrics=MetricsResponse(**old) if old else None,
        new_metrics=MetricsResponse(**result),
    )
