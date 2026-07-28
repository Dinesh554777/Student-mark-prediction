import { useState, useEffect, createContext, useContext } from "react";
import { BrowserRouter as Router, Routes, Route, NavLink } from "react-router-dom";
import { Home, BarChart3, Upload, History, Settings, Sun, Moon, Menu, X } from "lucide-react";
import HomePage from "./pages/Home";
import DashboardPage from "./pages/Dashboard";
import BatchUploadPage from "./pages/BatchUpload";
import HistoryPage from "./pages/History";
import SettingsPage from "./pages/Settings";
import NotFoundPage from "./pages/NotFound";
import "./App.css";

const ThemeContext = createContext();

export function useTheme() {
  return useContext(ThemeContext);
}

function ErrorBoundary({ children }) {
  const [error, setError] = useState(null);
  if (error) {
    return (
      <div className="card" style={{ textAlign: "center", padding: 60 }}>
        <h2 style={{ color: "var(--error-text)", marginBottom: 12 }}>Something went wrong</h2>
        <p style={{ color: "var(--text-muted)" }}>{error.message}</p>
        <button className="btn btn-primary" style={{ marginTop: 16 }} onClick={() => setError(null)}>
          Try Again
        </button>
      </div>
    );
  }
  return <ErrorCatcher onError={setError}>{children}</ErrorCatcher>;
}

class ErrorCatcher extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }
  static getDerivedStateFromError() {
    return { hasError: true };
  }
  componentDidCatch(error) {
    this.props.onError(error);
  }
  render() {
    if (this.state.hasError) return null;
    return this.props.children;
  }
}

import React from "react";

function App() {
  const [theme, setTheme] = useState(() => localStorage.getItem("theme") || "light");
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  const toggleTheme = () => setTheme(t => t === "light" ? "dark" : "light");

  const navItems = [
    { to: "/", label: "Predict", icon: Home },
    { to: "/dashboard", label: "Dashboard", icon: BarChart3 },
    { to: "/batch", label: "Batch Upload", icon: Upload },
    { to: "/history", label: "History", icon: History },
    { to: "/settings", label: "Settings", icon: Settings },
  ];

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      <ErrorBoundary>
        <Router>
          <div className="app">
            <button className="hamburger" onClick={() => setSidebarOpen(!sidebarOpen)}>
              {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
            </button>

            <nav className={`sidebar ${sidebarOpen ? "open" : ""}`}>
              <div className="logo">
                <h2>StudentMarks</h2>
                <p>ML Prediction</p>
              </div>
              <ul>
                {navItems.map(({ to, label, icon: Icon }) => (
                  <li key={to}>
                    <NavLink
                      to={to}
                      className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}
                      onClick={() => setSidebarOpen(false)}
                    >
                      <Icon size={18} />
                      <span>{label}</span>
                    </NavLink>
                  </li>
                ))}
              </ul>
              <div className="sidebar-bottom">
                <button className="theme-toggle" onClick={toggleTheme}>
                  {theme === "light" ? <Moon size={16} /> : <Sun size={16} />}
                  <span>{theme === "light" ? "Dark Mode" : "Light Mode"}</span>
                </button>
              </div>
            </nav>

            <main className="content">
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/dashboard" element={<DashboardPage />} />
                <Route path="/batch" element={<BatchUploadPage />} />
                <Route path="/history" element={<HistoryPage />} />
                <Route path="/settings" element={<SettingsPage />} />
                <Route path="*" element={<NotFoundPage />} />
              </Routes>
            </main>
          </div>
        </Router>
      </ErrorBoundary>
    </ThemeContext.Provider>
  );
}

export default App;
