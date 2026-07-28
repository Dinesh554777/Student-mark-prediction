import { useState, useEffect } from "react";
import {
  ScatterChart, Scatter, BarChart, Bar, LineChart, Line,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from "recharts";
import { getMetrics, getRechartsData, getDatasetInfo } from "../api";

export default function DashboardPage() {
  const [metrics, setMetrics] = useState(null);
  const [chartData, setChartData] = useState(null);
  const [dataset, setDataset] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        const [m, c, d] = await Promise.all([
          getMetrics(), getRechartsData(), getDatasetInfo(),
        ]);
        setMetrics(m.data);
        setChartData(c.data);
        setDataset(d.data);
      } catch (err) {
        setError("Failed to load dashboard data");
      } finally {
        setLoading(false);
      }
    };
    load();
  }, []);

  if (loading) {
    return (
      <div>
        <div className="page-header"><div className="page-header-text"><h1>Dashboard</h1></div></div>
        <div className="skeleton skeleton-card"></div>
        <div className="skeleton skeleton-card"></div>
        <div className="skeleton skeleton-chart"></div>
      </div>
    );
  }
  if (error) return <div className="error">{error}</div>;

  return (
    <div>
      <div className="page-header">
        <div className="page-header-text">
          <h1>Dashboard</h1>
          <p>Model metrics, interactive charts, and dataset overview</p>
        </div>
      </div>

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
              <div className="label">R-Score</div>
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
          <p style={{ marginTop: 12, fontSize: "0.85rem", color: "var(--text-muted)", fontStyle: "italic" }}>
            Equation: {metrics.equation}
          </p>
        </div>
      )}

      {chartData && (
        <div className="card">
          <h2>Interactive Charts</h2>
          <div className="charts-grid">
            <div>
              <h3>Study Hours vs Marks</h3>
              <ResponsiveContainer width="100%" height={300}>
                <ScatterChart>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                  <XAxis dataKey="x" name="Study Hours" stroke="var(--text-muted)" fontSize={12} />
                  <YAxis dataKey="y" name="Marks" stroke="var(--text-muted)" fontSize={12} />
                  <Tooltip contentStyle={{ background: "var(--bg-card)", border: "1px solid var(--border)", borderRadius: 8 }} />
                  <Scatter data={chartData.scatter} fill="var(--accent)" opacity={0.6} />
                </ScatterChart>
              </ResponsiveContainer>
            </div>
            <div>
              <h3>Regression Line</h3>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                  <XAxis dataKey="x" name="Study Hours" stroke="var(--text-muted)" fontSize={12} />
                  <YAxis dataKey="y" name="Marks" stroke="var(--text-muted)" fontSize={12} />
                  <Tooltip contentStyle={{ background: "var(--bg-card)", border: "1px solid var(--border)", borderRadius: 8 }} />
                  <Line data={chartData.regression_line} type="monotone" dataKey="y"
                    stroke="#e74c3c" strokeWidth={2} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
            <div>
              <h3>Study Hours Distribution</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={chartData.study_hours_dist}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                  <XAxis dataKey="name" stroke="var(--text-muted)" fontSize={10} angle={-30} textAnchor="end" height={60} />
                  <YAxis stroke="var(--text-muted)" fontSize={12} />
                  <Tooltip contentStyle={{ background: "var(--bg-card)", border: "1px solid var(--border)", borderRadius: 8 }} />
                  <Bar dataKey="value" fill="var(--accent)" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
            <div>
              <h3>Marks Distribution</h3>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={chartData.marks_dist}>
                  <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                  <XAxis dataKey="name" stroke="var(--text-muted)" fontSize={10} angle={-30} textAnchor="end" height={60} />
                  <YAxis stroke="var(--text-muted)" fontSize={12} />
                  <Tooltip contentStyle={{ background: "var(--bg-card)", border: "1px solid var(--border)", borderRadius: 8 }} />
                  <Bar dataKey="value" fill="#e74c3c" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      )}

      {dataset && (
        <div className="card">
          <h2>Dataset ({dataset.rows} rows x {dataset.columns.length} cols)</h2>
          <div style={{ overflowX: "auto" }}>
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
                      <td key={col}>{typeof row[col] === "number" ? row[col].toFixed(1) : row[col]}</td>
                    ))}
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
