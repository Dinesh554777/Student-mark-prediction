"""Dashboard routes for metrics and charts."""

import os
import sys
from fastapi import APIRouter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import MetricsResponse, ChartDataResponse, DatasetInfoResponse, RechartsDataResponse
from backend.ml_engine import get_metrics, get_chart_data, get_recharts_data, load_dataset

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])


@router.get("/metrics", response_model=MetricsResponse)
async def model_metrics():
    """Get model evaluation metrics."""
    m = get_metrics()
    return MetricsResponse(**m)


@router.get("/charts", response_model=ChartDataResponse)
async def charts():
    """Get chart images as base64."""
    data = get_chart_data()
    return ChartDataResponse(**data)


@router.get("/recharts")
async def recharts_data():
    """Get chart data formatted for Recharts (JSON)."""
    return get_recharts_data()


@router.get("/dataset", response_model=DatasetInfoResponse)
async def dataset_info():
    """Get dataset information."""
    df = load_dataset()
    stats = df.describe().to_dict()
    stats = {k: {sk: float(sv) for sk, sv in v.items()} for k, v in stats.items()}

    return DatasetInfoResponse(
        rows=len(df),
        columns=list(df.columns),
        shape=list(df.shape),
        null_values=df.isnull().sum().to_dict(),
        statistics=stats,
        sample_data=df.head(10).to_dict(orient="records"),
    )
