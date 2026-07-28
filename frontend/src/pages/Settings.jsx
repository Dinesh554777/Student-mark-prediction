import { useState } from "react";
import { retrainModel } from "../api";

export default function SettingsPage() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleRetrain = async () => {
    if (!confirm("Are you sure you want to retrain the model?")) return;
    setLoading(true);
    setError("");
    try {
      const res = await retrainModel();
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Retraining failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <h1>Settings</h1>
        <p>Manage and retrain the ML model</p>
      </div>

      <div className="card">
        <h2>Retrain Model</h2>
        <p style={{ color: "#666", marginBottom: 16 }}>
          Retrain the Linear Regression model on the current dataset.
          This will overwrite the existing model.
        </p>
        <button
          className="btn btn-primary"
          onClick={handleRetrain}
          disabled={loading}
        >
          {loading ? "Retraining..." : "Retrain Model"}
        </button>

        {error && <div className="error" style={{ marginTop: 12 }}>{error}</div>}

        {result && (
          <div className="success" style={{ marginTop: 16 }}>
            <strong>{result.message}</strong>
            <div className="metrics-grid" style={{ marginTop: 12 }}>
              <div className="metric-card">
                <div className="value">{result.new_metrics.r2_score}</div>
                <div className="label">New R² Score</div>
              </div>
              <div className="metric-card">
                <div className="value">{result.new_metrics.mae}</div>
                <div className="label">New MAE</div>
              </div>
              <div className="metric-card">
                <div className="value">{result.new_metrics.confidence}%</div>
                <div className="label">Confidence</div>
              </div>
            </div>
            {result.old_metrics && (
              <p style={{ marginTop: 12, fontSize: "0.85rem" }}>
                Previous R²: {result.old_metrics.r2_score} → New R²: {result.new_metrics.r2_score}
              </p>
            )}
          </div>
        )}
      </div>

      <div className="card">
        <h2>Model Info</h2>
        <table className="data-table">
          <tbody>
            <tr>
              <td><strong>Algorithm</strong></td>
              <td>Linear Regression</td>
            </tr>
            <tr>
              <td><strong>Feature</strong></td>
              <td>Study_Hours</td>
            </tr>
            <tr>
              <td><strong>Target</strong></td>
              <td>Marks</td>
            </tr>
            <tr>
              <td><strong>Test Split</strong></td>
              <td>80/20</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
