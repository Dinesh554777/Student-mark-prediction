import { useState } from "react";
import { predictSingle } from "../api";

export default function HomePage() {
  const [hours, setHours] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handlePredict = async (e) => {
    e.preventDefault();
    const val = parseFloat(hours);
    if (isNaN(val) || val < 0 || val > 24) {
      setError("Please enter a valid number between 0 and 24");
      return;
    }
    setError("");
    setLoading(true);
    try {
      const res = await predictSingle(val);
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <h1>Predict Marks</h1>
        <p>Enter study hours to predict exam marks using Linear Regression</p>
      </div>

      <div className="card">
        <h2>Enter Study Hours</h2>
        <form onSubmit={handlePredict}>
          <div className="form-group">
            <label>Study Hours (0 - 24)</label>
            <input
              type="number"
              step="0.1"
              min="0"
              max="24"
              value={hours}
              onChange={(e) => setHours(e.target.value)}
              placeholder="e.g. 6.5"
            />
          </div>
          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? "Predicting..." : "Predict Marks"}
          </button>
        </form>

        {error && <div className="error" style={{ marginTop: 12 }}>{error}</div>}

        {result && (
          <div className="result-box">
            <div className="label">Predicted Marks</div>
            <div className="big-number">{result.predicted_marks}</div>
            <div className="equation">{result.equation}</div>
            <div style={{ marginTop: 8, fontSize: "0.85rem", opacity: 0.8 }}>
              Confidence: {result.confidence}%
            </div>
          </div>
        )}
      </div>

      <div className="card">
        <h3>How it works</h3>
        <p style={{ color: "#666", lineHeight: 1.6 }}>
          This model uses <strong>Linear Regression</strong> trained on 100 student records.
          It learns the relationship between study hours and exam marks, then predicts
          your expected score based on the regression equation:
          <code> Marks = slope × Hours + intercept</code>
        </p>
      </div>
    </div>
  );
}
