"""SQLite database for prediction history."""

import sqlite3
import os
from typing import List, Dict, Optional
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "predictions.db")


def get_connection():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database and create tables."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                study_hours REAL NOT NULL,
                attendance REAL DEFAULT 0,
                sleep_hours REAL DEFAULT 0,
                previous_score REAL DEFAULT 0,
                predicted_marks REAL NOT NULL,
                prediction_type TEXT NOT NULL DEFAULT 'single',
                timestamp TEXT NOT NULL
            )
        """)
        conn.commit()


def save_prediction(study_hours: float, predicted_marks: float,
                    prediction_type: str = "single",
                    attendance: float = 0, sleep_hours: float = 0,
                    previous_score: float = 0) -> int:
    """Save a prediction to the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO predictions
               (study_hours, attendance, sleep_hours, previous_score,
                predicted_marks, prediction_type, timestamp)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (study_hours, attendance, sleep_hours, previous_score,
             predicted_marks, prediction_type, datetime.now().isoformat())
        )
        conn.commit()
        return cursor.lastrowid


def save_batch_predictions(predictions: List[Dict]):
    """Save multiple predictions to the database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        for pred in predictions:
            cursor.execute(
                """INSERT INTO predictions
                   (study_hours, predicted_marks, prediction_type, timestamp)
                   VALUES (?, ?, ?, ?)""",
                (pred["study_hours"], pred["predicted_marks"],
                 "batch", datetime.now().isoformat())
            )
        conn.commit()


def get_history(limit: int = 50, offset: int = 0,
                filter_type: Optional[str] = None) -> List[Dict]:
    """Get prediction history with optional type filter."""
    with get_connection() as conn:
        cursor = conn.cursor()
        if filter_type:
            cursor.execute(
                "SELECT * FROM predictions WHERE prediction_type = ? ORDER BY id DESC LIMIT ? OFFSET ?",
                (filter_type, limit, offset)
            )
        else:
            cursor.execute(
                "SELECT * FROM predictions ORDER BY id DESC LIMIT ? OFFSET ?",
                (limit, offset)
            )
        return [dict(row) for row in cursor.fetchall()]


def get_history_count(filter_type: Optional[str] = None) -> int:
    """Get total number of predictions."""
    with get_connection() as conn:
        cursor = conn.cursor()
        if filter_type:
            cursor.execute(
                "SELECT COUNT(*) FROM predictions WHERE prediction_type = ?",
                (filter_type,)
            )
        else:
            cursor.execute("SELECT COUNT(*) FROM predictions")
        return cursor.fetchone()[0]


def get_history_stats() -> Dict:
    """Get prediction history statistics."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT
                COUNT(*) as total,
                AVG(predicted_marks) as avg_marks,
                MIN(predicted_marks) as min_marks,
                MAX(predicted_marks) as max_marks,
                AVG(study_hours) as avg_hours
            FROM predictions
        """)
        row = cursor.fetchone()
        return dict(row) if row else {}


def delete_prediction(prediction_id: int) -> bool:
    """Delete a single prediction by ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM predictions WHERE id = ?", (prediction_id,))
        conn.commit()
        return cursor.rowcount > 0


def clear_history():
    """Clear all prediction history."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM predictions")
        conn.commit()


def export_history_csv() -> str:
    """Export all predictions as CSV string."""
    import io
    import csv
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, study_hours, attendance, sleep_hours, previous_score, "
            "predicted_marks, prediction_type, timestamp FROM predictions ORDER BY id"
        )
        rows = cursor.fetchall()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "Study_Hours", "Attendance", "Sleep_Hours",
                         "Previous_Score", "Predicted_Marks", "Type", "Timestamp"])
        for row in rows:
            writer.writerow([row["id"], row["study_hours"], row["attendance"],
                           row["sleep_hours"], row["previous_score"],
                           row["predicted_marks"], row["prediction_type"],
                           row["timestamp"]])
        return output.getvalue()


init_db()
