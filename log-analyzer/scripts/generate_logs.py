import random
import json
from datetime import datetime, timedelta

methods = ["GET", "POST", "PUT", "DELETE"]
paths = ["/api/users", "/api/login", "/api/orders", "/api/products"]
status_codes = [200, 201, 400, 401, 404, 500]

def random_time():
    base = datetime.now()
    delta = timedelta(seconds=random.randint(0, 100000))
    return (base - delta).isoformat() + "Z"

def generate_line():
    t = random.choice([0,1,2,3])

    # normal log
    if t == 0:
        return f"{random_time()} 192.168.1.{random.randint(1,255)} {random.choice(methods)} {random.choice(paths)} {random.choice(status_codes)} {random.randint(10,1000)}ms"

    # JSON log
    if t == 1:
        return json.dumps({
            "timestamp": random_time(),
            "ip": f"10.0.0.{random.randint(1,255)}",
            "method": random.choice(methods),
            "path": random.choice(paths),
            "status": random.choice(status_codes),
            "response_time": f"{random.randint(10,1000)}ms"
        })

    # malformed
    if t == 2:
        return "MALFORMED LOG ENTRY ### $$$"

    # missing fields
    return f"{random_time()} 10.0.0.{random.randint(1,255)} GET /api/users - 50ms"

def generate_file(n=1000):
    with open("sample.log", "w") as f:
        for _ in range(n):
            f.write(generate_line() + "\n")

if __name__ == "__main__":
    generate_file(5000)
    print("Log file generated")