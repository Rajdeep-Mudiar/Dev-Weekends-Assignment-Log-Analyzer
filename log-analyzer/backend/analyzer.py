from collections import defaultdict

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