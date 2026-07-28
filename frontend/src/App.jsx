import { BrowserRouter as Router, Routes, Route, NavLink } from "react-router-dom";
import { Home, BarChart3, Upload, History, Settings } from "lucide-react";
import HomePage from "./pages/Home";
import DashboardPage from "./pages/Dashboard";
import BatchUploadPage from "./pages/BatchUpload";
import HistoryPage from "./pages/History";
import SettingsPage from "./pages/Settings";
import "./App.css";

function App() {
  const navItems = [
    { to: "/", label: "Predict", icon: Home },
    { to: "/dashboard", label: "Dashboard", icon: BarChart3 },
    { to: "/batch", label: "Batch Upload", icon: Upload },
    { to: "/history", label: "History", icon: History },
    { to: "/settings", label: "Settings", icon: Settings },
  ];

  return (
    <Router>
      <div className="app">
        <nav className="sidebar">
          <div className="logo">
            <h2>📚 StudentMarks</h2>
            <p>ML Prediction</p>
          </div>
          <ul>
            {navItems.map(({ to, label, icon: Icon }) => (
              <li key={to}>
                <NavLink to={to} className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
                  <Icon size={18} />
                  <span>{label}</span>
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
        <main className="content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/batch" element={<BatchUploadPage />} />
            <Route path="/history" element={<HistoryPage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
