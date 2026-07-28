import { useState, useEffect } from "react";
import { getMetrics, getCharts, getDatasetInfo } from "../api";

export default function DashboardPage() {
  const [metrics, setMetrics] = useState(null);
  const [charts, setCharts] = useState(null);
  const [dataset, setDataset] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        const [m, c, d] = await Promise.all([
          getMetrics(),
          getCharts(),
          getDatasetInfo(),
        ]);
        setMetrics(m.data);
        setCharts(c.data);
        setDataset(d.data);
      } catch (err) {
        setError("Failed to load dashboard data");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  if (loading) return <div className="loading">Loading dashboard...</div>;
  if (error) return <div className="error">{error}</div>;

  return (
    <div>
      <div className="page-header">
        <h1>Dashboard</h1>
        <p>Model metrics, charts, and dataset overview</p>
      </div>

      {/* Metrics */}
      {metrics && (
        <div className="card">
          <h2>Model Evaluation Metrics</h2>
          <div className="metrics-grid">
            <div className="metric-card">
              <div className="value">{metrics.mae}</div>
              <div className="label">MAE</div>
            </div>
            <div className="metric-card">
              <div className="value">{metrics.rmse}</div>
              <div className="label">RMSE</div>
            </div>
            <div className="metric-card">
              <div className="value">{metrics.r2_score}</div>
              <div className="label">R² Score</div>
            </div>
            <div className="metric-card">
              <div className="value">{metrics.confidence}%</div>
              <div className="label">Confidence</div>
            </div>
            <div className="metric-card">
              <div className="value">{metrics.training_samples}</div>
              <div className="label">Train Samples</div>
            </div>
            <div className="metric-card">
              <div className="value">{metrics.testing_samples}</div>
              <div className="label">Test Samples</div>
            </div>
          </div>
          <p style={{ marginTop: 12, fontSize: "0.85rem", color: "#888", fontStyle: "italic" }}>
            Equation: {metrics.equation}
          </p>
        </div>
      )}

      {/* Charts */}
      {charts && (
        <div className="card">
          <h2>Visualizations</h2>
          <div className="charts-grid">
            {Object.entries(charts).map(([key, chart]) => (
              <div key={key} className="chart-container">
                <h3>{chart.title}</h3>
                <img src={`data:image/png;base64,${chart.image}`} alt={chart.title} />
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Dataset Info */}
      {dataset && (
        <div className="card">
          <h2>Dataset Info</h2>
          <p style={{ marginBottom: 12, color: "#666" }}>
            {dataset.rows} rows × {dataset.columns.length} columns
          </p>
          <table className="data-table">
            <thead>
              <tr>
                {dataset.columns.map((col) => (
                  <th key={col}>{col}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {dataset.sample_data.map((row, i) => (
                <tr key={i}>
                  {dataset.columns.map((col) => (
                    <td key={col}>{row[col]}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
