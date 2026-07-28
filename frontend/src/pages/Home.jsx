import { useState, useEffect, useRef, useMemo } from "react";
import {
  ScatterChart, Scatter, LineChart, Line, XAxis, YAxis,
  CartesianGrid, Tooltip, ResponsiveContainer, ReferenceDot
} from "recharts";
import { predictSingle, getRechartsData } from "../api";

export default function HomePage() {
  const [hours, setHours] = useState("");
  const [attendance, setAttendance] = useState("");
  const [sleep, setSleep] = useState("");
  const [prevScore, setPrevScore] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    getRechartsData().then(res => setChartData(res.data)).catch(() => {});
  }, []);

  const hasMulti = attendance || sleep || prevScore;

  const handlePredict = async (e) => {
    e.preventDefault();
    const val = parseFloat(hours);
    if (isNaN(val) || val < 0 || val > 24) {
      setError("Study hours must be between 0 and 24");
      return;
    }
    setError("");
    setLoading(true);
    try {
      const payload = { study_hours: val };
      if (attendance) payload.attendance = parseFloat(attendance);
      if (sleep) payload.sleep_hours = parseFloat(sleep);
      if (prevScore) payload.previous_score = parseFloat(prevScore);
      const res = await predictSingle(payload);
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Prediction failed");
    } finally {
      setLoading(false);
    }
  };

  const livePreview = useMemo(() => {
    if (!chartData || !hours) return null;
    const h = parseFloat(hours);
    if (isNaN(h)) return null;
    const model = chartData.regression_line;
    const closest = model.reduce((prev, curr) =>
      Math.abs(curr.x - h) < Math.abs(prev.x - h) ? curr : prev
    );
    return closest;
  }, [chartData, hours]);

  return (
    <div>
      <div className="page-header">
        <div className="page-header-text">
          <h1>Predict Marks</h1>
          <p>Enter student details to predict exam marks using Machine Learning</p>
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20 }}>
        <div>
          <div className="card">
            <h2>Student Details</h2>
            <form onSubmit={handlePredict}>
              <div className="form-group">
                <label>Study Hours (0 - 24) *</label>
                <input
                  type="number" step="0.1" min="0" max="24"
                  value={hours}
                  onChange={(e) => setHours(e.target.value)}
                  placeholder="e.g. 6.5"
                />
              </div>
              <div className="form-row">
                <div className="form-group">
                  <label>Attendance % (optional)</label>
                  <input type="number" step="0.1" min="0" max="100"
                    value={attendance} onChange={(e) => setAttendance(e.target.value)}
                    placeholder="e.g. 85" />
                </div>
                <div className="form-group">
                  <label>Sleep Hours (optional)</label>
                  <input type="number" step="0.1" min="0" max="24"
                    value={sleep} onChange={(e) => setSleep(e.target.value)}
                    placeholder="e.g. 7.5" />
                </div>
              </div>
              <div className="form-group">
                <label>Previous Score (optional)</label>
                <input type="number" step="0.1" min="0" max="100"
                  value={prevScore} onChange={(e) => setPrevScore(e.target.value)}
                  placeholder="e.g. 72" />
              </div>
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? "Predicting..." : "Predict Marks"}
              </button>
            </form>
            {error && <div className="error" style={{ marginTop: 12 }}>{error}</div>}
          </div>

          {result && (
            <div className="result-box">
              <div className="label">Predicted Marks</div>
              <div className="big-number">{result.predicted_marks}</div>
              <div className="equation">{result.equation}</div>
              <div className="feature-tags" style={{ justifyContent: "center", marginTop: 8 }}>
                {result.features_used?.map(f => (
                  <span key={f} className="feature-tag">{f}</span>
                ))}
              </div>
              <div style={{ marginTop: 8, fontSize: "0.85rem", opacity: 0.8 }}>
                Confidence: {result.confidence}%
              </div>
            </div>
          )}
        </div>

        <div className="card">
          <h2>Live Prediction Chart</h2>
          {chartData ? (
            <ResponsiveContainer width="100%" height={350}>
              <ScatterChart>
                <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
                <XAxis dataKey="x" name="Study Hours" stroke="var(--text-muted)" fontSize={12} />
                <YAxis dataKey="y" name="Marks" stroke="var(--text-muted)" fontSize={12} />
                <Tooltip
                  contentStyle={{ background: "var(--bg-card)", border: "1px solid var(--border)", borderRadius: 8 }}
                  labelStyle={{ color: "var(--text)" }}
                />
                <Scatter data={chartData.scatter} fill="var(--accent)" opacity={0.5} />
                <Scatter data={chartData.regression_line} fill="red" line={{ stroke: "red", strokeWidth: 2 }}
                  shape={() => null} legendType="none" />
                {livePreview && (
                  <ReferenceDot x={livePreview.x} y={livePreview.y}
                    r={8} fill="#ff6b6b" stroke="white" strokeWidth={2} />
                )}
              </ScatterChart>
            </ResponsiveContainer>
          ) : (
            <div className="skeleton skeleton-chart"></div>
          )}
          {livePreview && hours && (
            <p style={{ textAlign: "center", marginTop: 8, color: "var(--text-muted)", fontSize: "0.85rem" }}>
              Preview at {hours}h: ~{livePreview.y} marks
            </p>
          )}
        </div>
      </div>

      <div className="card">
        <h3>How it works</h3>
        <p style={{ color: "var(--text-secondary)", lineHeight: 1.6 }}>
          This model uses <strong>Linear Regression</strong> to learn the relationship between
          study habits and exam marks. Enter study hours for a basic prediction, or add
          attendance, sleep, and previous scores for a more accurate multi-feature prediction.
        </p>
      </div>
    </div>
  );
}
