import httpx
import asyncio
from collections import defaultdict

async def get_ai_insights(stats):
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
            # Using llama3.2:1b as it is extremely lightweight and should avoid memory issues
            response = await client.post("http://localhost:11434/api/generate", json={
                "model": "llama3.2:1b",
                "prompt": prompt,
                "stream": False
            })
            
            if response.status_code == 200:
                return response.json().get("response", "No insights generated.")
            else:
                return f"AI analysis unavailable (Ollama returned {response.status_code})."
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