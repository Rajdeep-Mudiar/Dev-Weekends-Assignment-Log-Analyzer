import httpx
import asyncio
from collections import defaultdict
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

async def get_ai_insights(stats):
    if not GROQ_API_KEY:
        return "AI analysis unavailable: GROQ_API_KEY not found in environment. Please add it to your .env file."

    prompt = f"""
    Analyze these server log statistics and provide 3-4 concise, actionable insights.
    Focus on errors, performance bottlenecks, and unusual patterns.
    
    Statistics:
    - Total Logs: {stats['total']}
    - Valid: {stats['valid']}
    - Malformed: {stats['malformed']}
    - Status Code Distribution: {stats['status_counts']}
    - Top Endpoints: {stats['endpoint_hits']}
    - Slowest Endpoints (Avg): {stats['slow_endpoints']}
    
    Format the output as a simple list of bullet points. Keep it professional and technical.
    """
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": "You are a senior site reliability engineer analyzing server logs."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.5,
                    "max_tokens": 500
                }
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                error_detail = response.json().get("error", {}).get("message", "Unknown error")
                return f"AI analysis unavailable (Groq returned {response.status_code}: {error_detail})."
    except Exception as e:
        return f"AI analysis unavailable: {str(e)}"

def analyze(logs):
    total = len(logs)
    valid = 0
    malformed = 0

    status_counts = defaultdict(int)
    endpoint_hits = defaultdict(int)
    ip_counts = defaultdict(int)

    slow_endpoints = defaultdict(list)

    for entry, typ in logs:
        if entry is None:
            malformed += 1
            continue

        valid += 1

        status = entry.get("status")
        path = entry.get("path")
        ip = entry.get("ip")
        rt = entry.get("response_time")

        if status:
            status_counts[status] += 1

        if path:
            endpoint_hits[path] += 1

        if ip:
            ip_counts[ip] += 1

        if path and rt:
            try:
                rt = float(str(rt).replace("ms", "").replace("s", ""))
                slow_endpoints[path].append(rt)
            except:
                pass

    slow_avg = {
        k: sum(v)/len(v)
        for k, v in slow_endpoints.items() if v
    }

    return {
        "total": total,
        "valid": valid,
        "malformed": malformed,
        "status_counts": dict(status_counts),
        "endpoint_hits": dict(endpoint_hits),
        "ip_counts": dict(ip_counts),
        "slow_endpoints": dict(sorted(slow_avg.items(), key=lambda x: -x[1])[:10])
    }