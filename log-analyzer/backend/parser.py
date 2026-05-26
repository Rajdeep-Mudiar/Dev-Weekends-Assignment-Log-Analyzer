import json

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

    if len(parts) < 6:
        return None, "malformed"

    try:
        timestamp = parts[0]
        ip = parts[1]
        method = parts[2]
        path = parts[3]
        status = parts[4]
        response_time = parts[5]

        if status == "-":
            status = None
        else:
            status = int(status)

        return {
            "timestamp": timestamp,
            "ip": ip,
            "method": method,
            "path": path,
            "status": status,
            "response_time": response_time
        }, "text"

    except:
        return None, "malformed"