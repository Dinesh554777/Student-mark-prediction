import { useState } from "react";
import { retrainModel, clearHistory } from "../api";

export default function SettingsPage() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [toast, setToast] = useState(null);

  const handleRetrain = async () => {
    if (!confirm("Retrain the model? This will overwrite the existing model.")) return;
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

  const handleClearHistory = async () => {
    if (!confirm("Clear ALL prediction history?")) return;
    try {
      await clearHistory();
      setToast("History cleared successfully");
    } catch {
      setToast("Failed to clear history");
    }
    setTimeout(() => setToast(null), 3000);
  };

  return (
    <div>
      <div className="page-header">
        <div className="page-header-text">
          <h1>Settings</h1>
          <p>Manage model and application settings</p>
        </div>
      </div>

      <div className="card">
        <h2>Retrain Model</h2>
        <p style={{ color: "var(--text-secondary)", marginBottom: 16 }}>
          Retrain the Linear Regression model on the current dataset. This will overwrite the existing model.
        </p>
        <button className="btn btn-primary" onClick={handleRetrain} disabled={loading}>
          {loading ? "Retraining..." : "Retrain Model"}
        </button>

        {error && <div className="error" style={{ marginTop: 12 }}>{error}</div>}

        {result && (
          <div className="success" style={{ marginTop: 16 }}>
            <strong>{result.message}</strong>
            <div className="metrics-grid" style={{ marginTop: 12 }}>
              <div className="metric-card">
                <div className="value">{result.new_metrics.r2_score}</div>
                <div className="label">New R-Score</div>
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
                Previous R: {result.old_metrics.r2_score} &rarr; New R: {result.new_metrics.r2_score}
              </p>
            )}
          </div>
        )}
      </div>

      <div className="card">
        <h2>Data Management</h2>
        <p style={{ color: "var(--text-secondary)", marginBottom: 16 }}>
          Clear all stored prediction history from the database.
        </p>
        <button className="btn btn-danger" onClick={handleClearHistory}>
          Clear Prediction History
        </button>
      </div>

      <div className="card">
        <h2>Model Information</h2>
        <table className="data-table">
          <tbody>
            <tr><td><strong>Algorithm</strong></td><td>Linear Regression</td></tr>
            <tr><td><strong>Primary Feature</strong></td><td>Study_Hours</td></tr>
            <tr><td><strong>Optional Features</strong></td><td>Attendance, Sleep_Hours, Previous_Score</td></tr>
            <tr><td><strong>Target</strong></td><td>Marks (0-100)</td></tr>
            <tr><td><strong>Test Split</strong></td><td>80/20</td></tr>
            <tr><td><strong>Storage</strong></td><td>SQLite (predictions.db)</td></tr>
          </tbody>
        </table>
      </div>

      {toast && <div className="toast toast-success">{toast}</div>}
    </div>
  );
}
