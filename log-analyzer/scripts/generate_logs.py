import random
import json
import time
from datetime import datetime, timedelta

methods = ["GET", "POST", "PUT", "DELETE"]
paths = ["/api/users", "/api/login", "/api/orders", "/api/products", "/api/checkout", "/api/search"]
status_codes = [200, 201, 400, 401, 403, 404, 500]
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "PostmanRuntime/7.26.8",
    "curl/7.64.1"
]

def random_time_variants():
    base = datetime.now() - timedelta(seconds=random.randint(0, 1000000))
    t = random.random()
    if t < 0.4:
        return base.strftime("%Y-%m-%dT%H:%M:%SZ") # ISO
    elif t < 0.6:
        return base.strftime("%Y/%m/%d %H:%M:%S") # Space separated
    elif t < 0.8:
        return base.strftime("%d-%b-%Y %H:%M:%S") # Month name
    else:
        return str(int(time.mktime(base.timetuple()))) # Unix epoch

def random_rt_variants():
    val = random.randint(10, 2000)
    t = random.random()
    if t < 0.6:
        return f"{val}ms"
    elif t < 0.8:
        return f"{val/1000:.3f}s"
    else:
        return str(val) # unitless

def generate_line():
    t = random.random()

    # Normal line (with variations)
    if t < 0.7:
        ts = random_time_variants()
        ip = f"192.168.1.{random.randint(1,255)}"
        method = random.choice(methods)
        path = random.choice(paths)
        status = random.choice(status_codes) if random.random() > 0.05 else "-"
        rt = random_rt_variants()
        
        line = f"{ts} {ip} {method} {path} {status} {rt}"
        
        # Add extra fields sometimes
        if random.random() > 0.7:
            line += f' "{random.choice(user_agents)}" "https://google.com"'
        return line

    # JSON log
    if t < 0.85:
        return json.dumps({
            "timestamp": random_time_variants(),
            "ip": f"10.0.0.{random.randint(1,255)}",
            "method": random.choice(methods),
            "path": random.choice(paths),
            "status": random.choice(status_codes),
            "response_time": random_rt_variants(),
            "extra": "some metadata"
        })

    # Entirely malformed / Stack trace
    if t < 0.95:
        if random.random() > 0.5:
            return "ERROR: java.lang.NullPointerException\n  at com.example.service.User.getId(User.java:42)\n  at com.example.service.Auth.login(Auth.java:12)"
        return "INCOMPLETE_WRITE_###_TRUNCATED"

    # Empty line
    return ""

def generate_file(n=5000):
    with open("sample.log", "w", encoding="utf-8") as f:
        for _ in range(n):
            line = generate_line()
            if line:
                f.write(line + "\n")

if __name__ == "__main__":
    generate_file(5000)
    print("Log file 'sample.log' generated with diverse messy data.")
