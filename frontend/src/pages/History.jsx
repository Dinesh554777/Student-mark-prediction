import { useState, useEffect } from "react";
import {
  getHistory, getHistoryCount, deletePrediction,
  clearHistory, exportHistory
} from "../api";

export default function HistoryPage() {
  const [history, setHistory] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(0);
  const [loading, setLoading] = useState(true);
  const [filterType, setFilterType] = useState(null);
  const [toast, setToast] = useState(null);
  const limit = 15;

  useEffect(() => { loadHistory(); }, [page, filterType]);

  const loadHistory = async () => {
    setLoading(true);
    try {
      const [h, c] = await Promise.all([
        getHistory(limit, page * limit, filterType),
        getHistoryCount(filterType),
      ]);
      setHistory(h.data);
      setTotal(c.data.total);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm("Delete this prediction?")) return;
    try {
      await deletePrediction(id);
      setToast({ type: "success", message: "Deleted!" });
      loadHistory();
    } catch {
      setToast({ type: "error", message: "Failed to delete" });
    }
    setTimeout(() => setToast(null), 3000);
  };

  const handleClearAll = async () => {
    if (!confirm("Clear ALL prediction history? This cannot be undone.")) return;
    try {
      await clearHistory();
      setToast({ type: "success", message: "History cleared" });
      setPage(0);
      loadHistory();
    } catch {
      setToast({ type: "error", message: "Failed to clear" });
    }
    setTimeout(() => setToast(null), 3000);
  };

  const handleExport = async () => {
    try {
      const res = await exportHistory();
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const a = document.createElement("a");
      a.href = url;
      a.download = "predictions_export.csv";
      a.click();
      window.URL.revokeObjectURL(url);
      setToast({ type: "success", message: "Exported!" });
    } catch {
      setToast({ type: "error", message: "Export failed" });
    }
    setTimeout(() => setToast(null), 3000);
  };

  const totalPages = Math.ceil(total / limit);

  return (
    <div>
      <div className="page-header">
        <div className="page-header-text">
          <h1>Prediction History</h1>
          <p>{total} total predictions</p>
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          <button className="btn btn-outline btn-sm" onClick={handleExport}>Export CSV</button>
          <button className="btn btn-danger btn-sm" onClick={handleClearAll}>Clear All</button>
        </div>
      </div>

      <div className="filter-bar">
        {[null, "single", "batch"].map(type => (
          <button key={type || "all"}
            className={`filter-btn ${filterType === type ? "active" : ""}`}
            onClick={() => { setFilterType(type); setPage(0); }}>
            {type === null ? "All" : type.charAt(0).toUpperCase() + type.slice(1)}
          </button>
        ))}
      </div>

      <div className="card">
        {loading ? (
          <div className="loading">Loading...</div>
        ) : history.length === 0 ? (
          <p style={{ color: "var(--text-muted)", textAlign: "center", padding: 40 }}>
            No predictions yet.
          </p>
        ) : (
          <>
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Study Hours</th>
                  <th>Predicted Marks</th>
                  <th>Type</th>
                  <th>Timestamp</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {history.map((h) => (
                  <tr key={h.id}>
                    <td>{h.id}</td>
                    <td>{h.study_hours}</td>
                    <td style={{ fontWeight: 600, color: "var(--accent)" }}>
                      {h.predicted_marks}
                    </td>
                    <td>
                      <span className={`badge badge-${h.prediction_type}`}>
                        {h.prediction_type}
                      </span>
                    </td>
                    <td style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>
                      {new Date(h.timestamp).toLocaleString()}
                    </td>
                    <td>
                      <button className="btn btn-danger btn-sm"
                        onClick={() => handleDelete(h.id)}>
                        Delete
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            {totalPages > 1 && (
              <div style={{ display: "flex", justifyContent: "center", gap: 12, marginTop: 16 }}>
                <button className="btn btn-primary btn-sm" disabled={page === 0}
                  onClick={() => setPage(page - 1)}>Previous</button>
                <span style={{ padding: "6px 12px", color: "var(--text-muted)", fontSize: "0.85rem" }}>
                  Page {page + 1} of {totalPages}
                </span>
                <button className="btn btn-primary btn-sm" disabled={page >= totalPages - 1}
                  onClick={() => setPage(page + 1)}>Next</button>
              </div>
            )}
          </>
        )}
      </div>

      {toast && (
        <div className={`toast toast-${toast.type}`}>
          {toast.message}
        </div>
      )}
    </div>
  );
}
