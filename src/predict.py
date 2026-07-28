"""Prediction module for Student Marks Prediction.

Provides functions to predict marks from study hours using the trained model.
"""

import os
import joblib
import pandas as pd

MODEL_PATH = "models/marks_model.pkl"


def load_model(filepath=MODEL_PATH):
    """Load the trained model from disk.

    Args:
        filepath (str): Path to the saved model.

    Returns:
        LinearRegression: Loaded model.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Model not found at {filepath}. Please train the model first."
        )
    return joblib.load(filepath)


def predict_marks(study_hours, model=None):
    """Predict marks for given study hours.

    Args:
        study_hours (float): Number of study hours.
        model: Trained model (loaded if None).

    Returns:
        float: Predicted marks.
    """
    if model is None:
        model = load_model()

    prediction = model.predict([[study_hours]])[0]
    return round(prediction, 2)


def predict_from_csv(csv_path, output_path=None):
    """Predict marks for all students in a CSV file.

    The CSV must have a 'Study_Hours' column.

    Args:
        csv_path (str): Path to input CSV.
        output_path (str): Path to save predictions (optional).

    Returns:
        pd.DataFrame: DataFrame with original data and predictions.
    """
    model = load_model()
    df = pd.read_csv(csv_path)

    if "Study_Hours" not in df.columns:
        raise ValueError("Input CSV must contain a 'Study_Hours' column.")

    df["Predicted_Marks"] = model.predict(df[["Study_Hours"]]).round(2)

    if output_path:
        df.to_csv(output_path, index=False)
        print(f"Predictions saved to {output_path}")

    return df


def interactive_predict():
    """Run an interactive prediction session."""
    try:
        model = load_model()
        print("\nEnter Study Hours (or 'q' to quit):")
        while True:
            user_input = input("\n> Enter Study Hours: ").strip()
            if user_input.lower() == "q":
                break
            try:
                hours = float(user_input)
                if hours < 0 or hours > 24:
                    print("Please enter hours between 0 and 24.")
                    continue
                predicted = predict_marks(hours, model)
                print(f"  Predicted Marks: {predicted}")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")
    except FileNotFoundError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    interactive_predict()
