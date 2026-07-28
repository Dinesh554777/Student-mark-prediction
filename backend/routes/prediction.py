"""Prediction routes for single and batch predictions."""

import os
import sys
import csv
import io
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import (
    PredictionRequest, PredictionResponse,
    BatchPredictionResponse, BatchPredictionResult,
    HistoryEntry, HistoryStats
)
from backend.ml_engine import predict, predict_multi, predict_batch, get_metrics
from backend.database import (
    save_prediction, save_batch_predictions, get_history,
    get_history_count, get_history_stats, delete_prediction,
    clear_history, export_history_csv
)

router = APIRouter(prefix="/api/predict", tags=["Prediction"])


@router.post("/", response_model=PredictionResponse)
async def single_prediction(req: PredictionRequest):
    """Predict marks for a single student."""
    has_multi = any([req.attendance > 0, req.sleep_hours > 0, req.previous_score > 0])

    if has_multi:
        result = predict_multi(req.study_hours, req.attendance, req.sleep_hours, req.previous_score)
    else:
        result = predict(req.study_hours)
        result["features_used"] = ["Study_Hours"]

    metrics = get_metrics()

    save_prediction(
        req.study_hours, result["predicted_marks"], "single",
        req.attendance, req.sleep_hours, req.previous_score
    )

    return PredictionResponse(
        study_hours=result["study_hours"],
        predicted_marks=result["predicted_marks"],
        confidence=metrics["confidence"],
        equation=result["equation"],
        features_used=result["features_used"],
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
async def prediction_history(limit: int = 50, offset: int = 0, filter_type: str = None):
    """Get prediction history with optional type filter."""
    history = get_history(limit, offset, filter_type)
    return [
        HistoryEntry(
            id=h["id"],
            study_hours=h["study_hours"],
            attendance=h.get("attendance", 0),
            sleep_hours=h.get("sleep_hours", 0),
            previous_score=h.get("previous_score", 0),
            predicted_marks=h["predicted_marks"],
            timestamp=h["timestamp"],
            prediction_type=h["prediction_type"],
        )
        for h in history
    ]


@router.get("/history/count")
async def prediction_history_count(filter_type: str = None):
    """Get total number of predictions."""
    return {"total": get_history_count(filter_type)}


@router.get("/history/stats", response_model=HistoryStats)
async def prediction_history_stats():
    """Get prediction history statistics."""
    stats = get_history_stats()
    return HistoryStats(**stats)


@router.delete("/history/{prediction_id}")
async def delete_prediction_by_id(prediction_id: int):
    """Delete a single prediction."""
    deleted = delete_prediction(prediction_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return {"message": "Prediction deleted", "id": prediction_id}


@router.delete("/history")
async def clear_all_history():
    """Clear all prediction history."""
    clear_history()
    return {"message": "History cleared"}


@router.get("/export")
async def export_history():
    """Export prediction history as CSV."""
    csv_content = export_history_csv()
    return StreamingResponse(
        io.BytesIO(csv_content.encode("utf-8")),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=predictions_export.csv"}
    )
