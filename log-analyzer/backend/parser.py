import json
import re

def safe_float(val):
    if val is None: return None
    try:
        # Handle "0.142s", "142ms", "142"
        clean = str(val).lower().replace("ms", "").replace("s", "")
        f = float(clean)
        if "ms" in str(val).lower():
            return f
        if "s" in str(val).lower():
            return f * 1000
        return f
    except:
        return None

def parse_line(line):
    line = line.strip()
    if not line:
        return None, "empty"

    # 1. JSON log handling
    if line.startswith("{"):
        try:
            data = json.loads(line)
            return {
                "timestamp": data.get("timestamp"),
                "ip": data.get("ip"),
                "method": data.get("method"),
                "path": data.get("path"),
                "status": data.get("status"),
                "response_time": safe_float(data.get("response_time"))
            }, "json"
        except:
            return None, "malformed"

    # 2. Text log handling
    # Anchor on the IP address to handle space-separated timestamps
    ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    match = re.search(ip_pattern, line)
    
    if not match:
        return None, "malformed"

    ip = match.group(1)
    ip_start = match.start()
    
    # Everything before IP is the timestamp
    timestamp = line[:ip_start].strip()
    
    # Everything after IP
    rest = line[match.end():].strip().split()
    
    if len(rest) < 3: # Need at least Method, Path, Status
        return None, "malformed"

    try:
        method = rest[0]
        path = rest[1]
        status_str = rest[2]
        rt_str = rest[3] if len(rest) > 3 else None

        # Clean status
        status = int(status_str) if status_str.isdigit() else None
        
        return {
            "timestamp": timestamp,
            "ip": ip,
            "method": method,
            "path": path,
            "status": status,
            "response_time": safe_float(rt_str)
        }, "text"

    except:
        return None, "malformed"