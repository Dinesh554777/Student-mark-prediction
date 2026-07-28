import { useState, useRef } from "react";
import { predictBatch } from "../api";

export default function BatchUploadPage() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [dragOver, setDragOver] = useState(false);
  const fileRef = useRef();

  const handleFile = (f) => {
    if (!f) return;
    if (!f.name.endsWith(".csv")) {
      setError("Please select a CSV file");
      return;
    }
    setFile(f);
    setError("");
    setResult(null);

    // Preview CSV
    const reader = new FileReader();
    reader.onload = (e) => {
      const text = e.target.result;
      const lines = text.split("\n").slice(0, 6);
      setPreview(lines);
    };
    reader.readAsText(f);
  };

  const handleUpload = async () => {
    if (!file) return;
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

  const downloadResults = () => {
    if (!result) return;
    const header = "Study_Hours,Predicted_Marks\n";
    const rows = result.results.map(r => `${r.study_hours},${r.predicted_marks}`).join("\n");
    const blob = new Blob([header + rows], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "predictions.csv";
    a.click();
    window.URL.revokeObjectURL(url);
  };

  return (
    <div>
      <div className="page-header">
        <div className="page-header-text">
          <h1>Batch Prediction</h1>
          <p>Upload a CSV with Study_Hours column for bulk predictions</p>
        </div>
      </div>

      <div className="card">
        <h2>Upload CSV File</h2>
        <div
          className={`file-upload ${dragOver ? "drag-over" : ""}`}
          onDrop={(e) => { e.preventDefault(); setDragOver(false); handleFile(e.dataTransfer.files[0]); }}
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onClick={() => fileRef.current?.click()}
        >
          <input ref={fileRef} type="file" accept=".csv"
            onChange={(e) => handleFile(e.target.files[0])} />
          <p style={{ fontSize: "1.1rem", marginBottom: 8 }}>
            {file ? file.name : "Drag & drop a CSV file or click to browse"}
          </p>
          <p style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>
            CSV must have a "Study_Hours" column
          </p>
        </div>

        {preview && (
          <div style={{ marginTop: 16 }}>
            <h3>Preview (first 5 rows)</h3>
            <pre style={{
              background: "var(--metric-bg)", padding: 12, borderRadius: 8,
              fontSize: "0.8rem", overflow: "auto", color: "var(--text)"
            }}>
              {preview.join("\n")}
            </pre>
          </div>
        )}

        <button className="btn btn-primary" style={{ marginTop: 16 }}
          onClick={handleUpload} disabled={loading || !file}>
          {loading ? "Processing..." : "Upload & Predict"}
        </button>

        {error && <div className="error" style={{ marginTop: 12 }}>{error}</div>}
      </div>

      {result && (
        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <h2>Results</h2>
            <button className="btn btn-outline btn-sm" onClick={downloadResults}>
              Download CSV
            </button>
          </div>
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
          <div style={{ overflowX: "auto" }}>
            <table className="data-table">
              <thead>
                <tr><th>#</th><th>Study Hours</th><th>Predicted Marks</th></tr>
              </thead>
              <tbody>
                {result.results.map((r, i) => (
                  <tr key={i}>
                    <td>{i + 1}</td>
                    <td>{r.study_hours}</td>
                    <td style={{ fontWeight: 600, color: "var(--accent)" }}>{r.predicted_marks}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
