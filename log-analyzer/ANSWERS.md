# Technical Assessment Answers

## 1. How to run
1. **Generate Data**: `python scripts/generate_logs.py` (creates `sample.log`).
2. Setup AI: Get a [Groq API Key](https://console.groq.com/) and add it to `backend/.env` as `GROQ_API_KEY=your_key`.
3. Backend:
   - `cd backend`
   - `pip install -r requirements.txt`
   - `uvicorn main:app --reload --port 8000`
4. Frontend:
   - `cd frontend`
   - `npm install`
   - `npm run dev`
5. Analyze: Open `http://localhost:5173`, click "Choose a log file...", select `sample.log`, and click **Analyze Logs**.

## 2. Stack choice
I chose **FastAPI (Python)** and **React (Vite)** with **Groq API** integration:
- **FastAPI**: Python's `defaultdict` and string processing capabilities are perfect for parsing text-based logs. FastAPI provides high performance and automatic documentation.
- **React + Chart.js**: Provides a modern, interactive way to visualize trends that a CLI might miss (e.g., seeing a spike in 401s visually).
- **Groq API**: Using an external API for LLM analysis completely removes local hardware constraints (like the 8.9 GiB memory limit) while providing lightning-fast inference using Llama 3.3 70B.

**Worse Choice**: A heavy Java Spring Boot or .NET enterprise stack would have been overkill for this "on-call tool" requirement. They add significant boilerplate and memory overhead without providing better parsing logic than Python's native tools.

## 3. One real edge case
**Edge Case**: Missing status codes represented as `-` and mixed response time units.
- **File/Line**: [parser.py:L33-40](file:///d%3A/internship/Dev%20Weekends/log-analyzer/backend/parser.py#L33-40) and [parser.py:L3-7](file:///d%3A/internship/Dev%20Weekends/log-analyzer/backend/parser.py#L3-7).
- **Explanation**: The code checks if the status field is `-` and converts it to `None` instead of crashing on `int("-")`. It also uses `safe_float` to strip `ms` and `s` suffixes from response times, converting them to a common float format.
- **Without this**: The parser would crash on the first "incomplete" log entry or mixed-unit line, rendering the tool useless for the "messy" logs described in the prompt.

## 4. AI usage
- **Tool**: Trae IDE (powered by Gemini-3.5-Flash-Preview).
- **Instances of Usage**:
  1. **Scaffolding**: Asked for a "Log analyzer with FastAPI and React". It provided the project structure and basic file upload logic.
  2. **UI Design**: Asked to "improve the ui" and make it "beautiful and modern". It gave me the `App.css` variables, grid layout, and the "stat-card" component structure.
  3. **Error Resolution**: Provided the "500 Internal Server Error" message regarding memory. Trae analyzed the code, identified that a large local model was being used, and suggested switching to a smaller model or an API.
  4. **Groq Integration**: Asked to "use api key like groq instead of llama3.2:1b". It provided the `httpx` implementation for the Groq chat completion endpoint.

- **Human-in-the-loop Change**: When implementing the Groq integration, the AI initially suggested installing the official `groq` Python library. I manually decided to use direct `httpx` calls instead. **Reason**: This avoids adding another external dependency to the `requirements.txt` and uses the standard OpenAI-compatible REST API, making the backend more lightweight and easier to maintain.

## 5. Honest gap
The **Timestamp Parsing** is currently too rigid. While the prompt mentions variations like "15-Mar-2024" or Unix epochs, the current `parse_line` implementation assumes the timestamp is the first space-separated part and doesn't fully normalize different formats into a single `datetime` object. 

**Fix with another day**: I would implement a more robust normalization layer using `dateutil.parser` or regex to transform all timestamp variations into UTC ISO strings, allowing for time-series charts (e.g., "Errors per Minute") instead of just aggregate counts.
