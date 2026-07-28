import { useState, useRef } from "react";
import { predictBatch } from "../api";

export default function BatchUploadPage() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const fileRef = useRef();

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a CSV file");
      return;
    }
    setError("");
    setLoading(true);
    try {
      const res = await predictBatch(file);
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Upload failed");
    } finally {
      setLoading(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const f = e.dataTransfer.files[0];
    if (f && f.name.endsWith(".csv")) {
      setFile(f);
    }
  };

  return (
    <div>
      <div className="page-header">
        <h1>Batch Prediction</h1>
        <p>Upload a CSV file with Study_Hours column for bulk predictions</p>
      </div>

      <div className="card">
        <h2>Upload CSV File</h2>
        <div
          className="file-upload"
          onDrop={handleDrop}
          onDragOver={(e) => e.preventDefault()}
          onClick={() => fileRef.current?.click()}
        >
          <input
            ref={fileRef}
            type="file"
            accept=".csv"
            onChange={(e) => setFile(e.target.files[0])}
          />
          <p style={{ fontSize: "1.1rem", marginBottom: 8 }}>
            {file ? file.name : "Drag & drop a CSV file here or click to browse"}
          </p>
          <p style={{ fontSize: "0.8rem", color: "#888" }}>
            CSV must have a "Study_Hours" column
          </p>
        </div>

        <button
          className="btn btn-primary"
          style={{ marginTop: 16 }}
          onClick={handleUpload}
          disabled={loading || !file}
        >
          {loading ? "Processing..." : "Upload & Predict"}
        </button>

        {error && <div className="error" style={{ marginTop: 12 }}>{error}</div>}
      </div>

      {result && (
        <div className="card">
          <h2>Results</h2>
          <div className="metrics-grid" style={{ marginBottom: 16 }}>
            <div className="metric-card">
              <div className="value">{result.total}</div>
              <div className="label">Predictions</div>
            </div>
            <div className="metric-card">
              <div className="value">{result.average_predicted}</div>
              <div className="label">Avg Predicted Marks</div>
            </div>
          </div>
          <table className="data-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Study Hours</th>
                <th>Predicted Marks</th>
              </tr>
            </thead>
            <tbody>
              {result.results.map((r, i) => (
                <tr key={i}>
                  <td>{i + 1}</td>
                  <td>{r.study_hours}</td>
                  <td>{r.predicted_marks}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
