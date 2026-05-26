import json

def safe_float(val):
    try:
        return float(val.replace("ms", "").replace("s", ""))
    except:
        return None


def parse_line(line):
    line = line.strip()

    if not line:
        return None, "empty"

    # JSON log
    if line.startswith("{"):
        try:
            return json.loads(line), "json"
        except:
            return None, "malformed"

    parts = line.split()

    if len(parts) < 5:
        return None, "malformed"

    try:
        timestamp = parts[0]
        ip = parts[1]
        method = parts[2]
        path = parts[3]
        status = parts[4] if parts[4] != "-" else None
        rt = parts[5] if len(parts) > 5 else None

        return {
            "timestamp": timestamp,
            "ip": ip,
            "method": method,
            "path": path,
            "status": int(status) if status and status.isdigit() else None,
            "response_time": safe_float(rt)
        }, "text"

    except:
        return None, "malformed"