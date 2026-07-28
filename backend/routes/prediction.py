"""Prediction routes for single and batch predictions."""

import os
import sys
import csv
import io
from fastapi import APIRouter, UploadFile, File, HTTPException

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import (
    PredictionRequest, PredictionResponse,
    BatchPredictionResponse, BatchPredictionResult,
    HistoryEntry
)
from backend.ml_engine import predict, predict_batch
from backend.database import save_prediction, save_batch_predictions, get_history, get_history_count

router = APIRouter(prefix="/api/predict", tags=["Prediction"])


@router.post("/", response_model=PredictionResponse)
async def single_prediction(req: PredictionRequest):
    """Predict marks for a single study hours value."""
    result = predict(req.study_hours)

    # Get confidence from metrics
    from backend.ml_engine import get_metrics
    metrics = get_metrics()

    # Save to history
    save_prediction(req.study_hours, result["predicted_marks"], "single")

    return PredictionResponse(
        study_hours=result["study_hours"],
        predicted_marks=result["predicted_marks"],
        confidence=metrics["confidence"],
        equation=result["equation"],
    )


@router.post("/batch", response_model=BatchPredictionResponse)
async def batch_prediction(file: UploadFile = File(...)):
    """Upload a CSV file for batch predictions."""
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    try:
        content = await file.read()
        text = content.decode("utf-8")
        reader = csv.DictReader(io.StringIO(text))

        if "Study_Hours" not in (reader.fieldnames or []):
            raise HTTPException(
                status_code=400,
                detail="CSV must contain a 'Study_Hours' column"
            )

        hours_list = []
        for row in reader:
            try:
                hours = float(row["Study_Hours"])
                if 0 <= hours <= 24:
                    hours_list.append(hours)
            except (ValueError, KeyError):
                continue

        if not hours_list:
            raise HTTPException(status_code=400, detail="No valid Study_Hours values found")

        results = predict_batch(hours_list)
        avg_marks = sum(r["predicted_marks"] for r in results) / len(results)

        # Save to history
        save_batch_predictions(results)

        return BatchPredictionResponse(
            results=[BatchPredictionResult(**r) for r in results],
            total=len(results),
            average_predicted=round(avg_marks, 2),
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.get("/history", response_model=list[HistoryEntry])
async def prediction_history(limit: int = 50, offset: int = 0):
    """Get prediction history."""
    history = get_history(limit, offset)
    return [
        HistoryEntry(
            id=h["id"],
            study_hours=h["study_hours"],
            predicted_marks=h["predicted_marks"],
            timestamp=h["timestamp"],
            prediction_type=h["prediction_type"],
        )
        for h in history
    ]


@router.get("/history/count")
async def prediction_history_count():
    """Get total number of predictions."""
    return {"total": get_history_count()}
