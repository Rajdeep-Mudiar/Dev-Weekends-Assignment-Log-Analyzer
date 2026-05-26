# Log Analyzer AI Dashboard

A robust, AI-powered log analysis tool that handles messy, real-world server logs. It provides a visual dashboard for statistical analysis and integrates with a local LLM to generate intelligent insights and recommendations.

## Features

- **Messy Log Parsing**: Handles mixed formats (Text/JSON), malformed lines, missing fields (`-`), and varying units (`ms`, `s`).
- **Statistical Dashboard**: Visualizes status code distribution and top endpoint hits using Chart.js.
- **AI Insights**: Leverages the **Groq API** (Llama 3.3 70B) to provide actionable recommendations based on log patterns.
- **Performance Tracking**: Identifies and ranks the slowest endpoints by average response time.
- **Robustness**: Degrading gracefully on malformed data, ensuring no crash even with "noisy" log files.

---

## How It Works

### 1. The Parser (`parser.py`)
The tool uses a multi-stage parsing strategy:
- **JSON Detection**: First checks if a line is a valid JSON object.
- **Space-Delimited Parsing**: If not JSON, it splits the line and extracts fields by position.
- **Normalization**: Cleans up status codes (handling `-` as `None`) and response times (converting `ms` and `s` strings to uniform floats).

### 2. The Analysis Engine (`analyzer.py`)
- Aggregates status codes, endpoint hits, and IP addresses using `defaultdict`.
- Calculates moving averages for response times per endpoint.
- Filters the top 10 slowest endpoints for the performance report.

### 3. AI Insights (Groq)
- Sends the aggregated statistics to Groq's Llama 3.3 70B model.
- Uses a system prompt that defines the persona of a Senior SRE to ensure technical and actionable feedback.

---

## Setup & Running

### Prerequisites
- **Python 3.10+**
- **Node.js 18+**
- **Groq API Key** (for AI insights)

### 1. Generate Test Data
Before running, generate a representative sample log file using the included script:
```bash
python scripts/generate_logs.py
```
This creates a `sample.log` in the root with 5,000 mixed-format entries.

### 2. Setup AI (Groq)
1. Get an API key from [Groq Console](https://console.groq.com/).
2. Create a `.env` file in the `backend/` directory.
3. Add your key: `GROQ_API_KEY=your_key_here`.

### 3. Start Backend (FastAPI)
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 4. Start Frontend (React)
Open a new terminal:
```bash
cd frontend
npm install
npm run dev
```
The dashboard will be available at `http://localhost:5173`.

---

## Project Structure
- `/backend`: Python FastAPI server for parsing and analysis.
- `/frontend`: React + Vite + Chart.js dashboard.
- `/scripts`: Log generation utility for testing.
- `ANSWERS.md`: Technical assessment responses.
