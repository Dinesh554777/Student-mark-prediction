"""SQLite database for prediction history."""

import sqlite3
import os
from typing import List, Dict
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "predictions.db")


def get_connection():
    """Get database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database and create tables."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            study_hours REAL NOT NULL,
            predicted_marks REAL NOT NULL,
            prediction_type TEXT NOT NULL DEFAULT 'single',
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_prediction(study_hours: float, predicted_marks: float, prediction_type: str = "single"):
    """Save a prediction to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO predictions (study_hours, predicted_marks, prediction_type, timestamp) VALUES (?, ?, ?, ?)",
        (study_hours, predicted_marks, prediction_type, datetime.now().isoformat())
    )
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id


def save_batch_predictions(predictions: List[Dict]):
    """Save multiple predictions to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    for pred in predictions:
        cursor.execute(
            "INSERT INTO predictions (study_hours, predicted_marks, prediction_type, timestamp) VALUES (?, ?, ?, ?)",
            (pred["study_hours"], pred["predicted_marks"], "batch", datetime.now().isoformat())
        )
    conn.commit()
    conn.close()


def get_history(limit: int = 50, offset: int = 0) -> List[Dict]:
    """Get prediction history."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM predictions ORDER BY id DESC LIMIT ? OFFSET ?",
        (limit, offset)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_history_count() -> int:
    """Get total number of predictions."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM predictions")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def clear_history():
    """Clear all prediction history."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions")
    conn.commit()
    conn.close()


# Initialize on import
init_db()
