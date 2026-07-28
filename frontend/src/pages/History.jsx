import { useState, useEffect } from "react";
import { getHistory, getHistoryCount } from "../api";

export default function HistoryPage() {
  const [history, setHistory] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(0);
  const [loading, setLoading] = useState(true);
  const limit = 20;

  useEffect(() => {
    loadHistory();
  }, [page]);

  const loadHistory = async () => {
    setLoading(true);
    try {
      const [h, c] = await Promise.all([
        getHistory(limit, page * limit),
        getHistoryCount(),
      ]);
      setHistory(h.data);
      setTotal(c.data.total);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const totalPages = Math.ceil(total / limit);

  return (
    <div>
      <div className="page-header">
        <h1>Prediction History</h1>
        <p>View all past predictions ({total} total)</p>
      </div>

      <div className="card">
        {loading ? (
          <div className="loading">Loading...</div>
        ) : history.length === 0 ? (
          <p style={{ color: "#888", textAlign: "center", padding: 40 }}>
            No predictions yet. Make some predictions first!
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
                </tr>
              </thead>
              <tbody>
                {history.map((h) => (
                  <tr key={h.id}>
                    <td>{h.id}</td>
                    <td>{h.study_hours}</td>
                    <td style={{ fontWeight: 600, color: "#6c63ff" }}>
                      {h.predicted_marks}
                    </td>
                    <td>
                      <span
                        className={`badge badge-${h.prediction_type}`}
                      >
                        {h.prediction_type}
                      </span>
                    </td>
                    <td style={{ fontSize: "0.8rem", color: "#888" }}>
                      {new Date(h.timestamp).toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>

            <div style={{ display: "flex", justifyContent: "center", gap: 12, marginTop: 16 }}>
              <button
                className="btn btn-primary"
                disabled={page === 0}
                onClick={() => setPage(page - 1)}
              >
                Previous
              </button>
              <span style={{ padding: "10px 16px", color: "#666" }}>
                Page {page + 1} of {totalPages}
              </span>
              <button
                className="btn btn-primary"
                disabled={page >= totalPages - 1}
                onClick={() => setPage(page + 1)}
              >
                Next
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
