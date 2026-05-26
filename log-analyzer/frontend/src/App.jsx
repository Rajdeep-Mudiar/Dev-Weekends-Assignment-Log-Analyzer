import { useState } from "react";
import axios from "axios";
import StatusChart from "./components/StatusChart";
import EndpointChart from "./components/EndpointChart";
import "./App.css";

export default function App() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const uploadFile = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://127.0.0.1:8000/upload", formData);
      setData(res.data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || err.message || "An error occurred during analysis");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Log Analyzer AI</h1>
        <div className="upload-section">
          <input 
            type="file" 
            id="file-upload"
            onChange={(e) => setFile(e.target.files[0])} 
            className="file-input"
          />
          <label htmlFor="file-upload" className="file-label">
            {file ? file.name : "Choose a log file..."}
          </label>
          <button 
            onClick={uploadFile} 
            disabled={!file || loading}
            className="analyze-button"
          >
            {loading ? "Analyzing..." : "Analyze Logs"}
          </button>
        </div>
      </header>

      {error && (
        <div className="error-banner">
          <p><strong>Error:</strong> {error}</p>
        </div>
      )}

      {data && (
        <main className="dashboard-content">
          <section className="summary-grid">
            <div className="stat-card">
              <h3>Total Logs</h3>
              <p className="stat-value">{data.total}</p>
            </div>
            <div className="stat-card">
              <h3>Valid Entries</h3>
              <p className="stat-value green">{data.valid}</p>
            </div>
            <div className="stat-card">
              <h3>Malformed</h3>
              <p className="stat-value red">{data.malformed}</p>
            </div>
          </section>

          <section className="charts-grid">
            <div className="chart-card">
              <StatusChart statusCounts={data.status_counts} />
            </div>
            <div className="chart-card">
              <EndpointChart endpointHits={data.endpoint_hits} />
            </div>
          </section>

          {data.insights && (
            <section className="insights-section">
              <div className={`insight-card ${data.insights.includes('API_KEY not found') ? 'warning' : ''}`}>
                <h3>AI Insights & Recommendations</h3>
                <div className="insight-content">
                  {data.insights.split('\n').map((line, i) => (
                    <p key={i}>{line}</p>
                  ))}
                </div>
                {data.insights.includes('API_KEY not found') && (
                  <div className="setup-instruction">
                    <p>Add your API key to <code>backend/.env</code></p>
                  </div>
                )}
              </div>
            </section>
          )}

          <section className="slow-endpoints">
            <div className="table-card">
              <h3>Slowest Endpoints (Avg Response Time)</h3>
              <table>
                <thead>
                  <tr>
                    <th>Endpoint</th>
                    <th>Avg Time</th>
                  </tr>
                </thead>
                <tbody>
                  {Object.entries(data.slow_endpoints).map(([path, time]) => (
                    <tr key={path}>
                      <td>{path}</td>
                      <td>{time.toFixed(2)}ms</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        </main>
      )}

      {!data && !loading && (
        <div className="welcome-state">
          <img src="/src/assets/hero.png" alt="Hero" className="hero-img" />
          <h2>Upload your server logs to get started</h2>
          <p>Get instant insights, error patterns, and performance analysis.</p>
        </div>
      )}
    </div>
  );
}
