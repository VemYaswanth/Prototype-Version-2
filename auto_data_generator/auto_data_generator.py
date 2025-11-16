import os
import random
import time
from datetime import datetime
import requests

# Backend API base URL (inside Docker network)
# Override with BACKEND_URL env if needed, e.g. http://flask_api:8000
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

# Query templates
CLEAN_QUERIES = [
    "SELECT * FROM products WHERE price < 100;",
    "INSERT INTO customers (name, email) VALUES ('Alice','alice@test.com');",
    "UPDATE inventory SET stock = stock - 1 WHERE product_id = 10;",
    "DELETE FROM logs WHERE created_at < NOW() - INTERVAL '30 days';",
]

SUSPICIOUS_QUERIES = [
    "DROP TABLE users;",
    "ALTER TABLE query_logs DISABLE TRIGGER ALL;",
    "GRANT ALL PRIVILEGES ON database securitydb TO hacker;",
    "UPDATE users SET password_hash = 'hacked';",
    "SELECT * FROM users WHERE password_hash IS NOT NULL;",
]


def infer_operation_type(query: str) -> str:
    """Infer SQL operation type from the query text."""
    q_upper = query.strip().upper()
    if q_upper.startswith("SELECT"):
        return "SELECT"
    if q_upper.startswith("INSERT"):
        return "INSERT"
    if q_upper.startswith("UPDATE"):
        return "UPDATE"
    if q_upper.startswith("DELETE"):
        return "DELETE"
    if q_upper.startswith("DROP"):
        return "DROP"
    if q_upper.startswith("ALTER"):
        return "ALTER"
    if q_upper.startswith("GRANT"):
        return "GRANT"
    return "UNKNOWN"


def send_log_to_backend(query: str, operation_type: str, user_id: int, client_ip: str):
    """
    Send a single query log into the Flask backend.

    This hits /logs/add, which will:
      - insert into query_logs
      - run the AI scoring engine (/ai/score)
      - create anomalies / alerts
      - update metrics for /metrics/summary and /alerts/suspicious
    """
    payload = {
        "user_id": user_id,
        "query_text": query,
        "operation_type": operation_type,
        "client_ip": client_ip,
    }

    try:
        resp = requests.post(
            f"{BACKEND_URL}/logs/add",
            json=payload,
            timeout=5,
        )
        if resp.status_code != 200:
            print(
                f"[{datetime.now().isoformat()}] ❌ Backend rejected log "
                f"(status {resp.status_code}): {resp.text}"
            )
        else:
            print(
                f"[{datetime.now().isoformat()}] ⚡ Sent log to backend "
                f"(user={user_id}, op={operation_type})"
            )
    except Exception as e:
        print(f"[{datetime.now().isoformat()}] ❌ Error sending log to backend: {e}")


def run():
    """Main loop for generating synthetic query logs."""
    print("🚀 Auto Data Generator running...")
    print(f"🌐 Using backend URL: {BACKEND_URL}")

    while True:
        try:
            # pick a random user and fake client IP
            # (adjust range if your seeded users are fewer/more)
            user_id = random.randint(1, 10)
            client_ip = f"192.168.1.{random.randint(1, 254)}"

            # random choice: clean vs suspicious
            query_type = random.choice(["clean", "suspicious"])

            if query_type == "clean":
                query = random.choice(CLEAN_QUERIES)
            else:
                query = random.choice(SUSPICIOUS_QUERIES)

            op = infer_operation_type(query)

            send_log_to_backend(
                query=query,
                operation_type=op,
                user_id=user_id,
                client_ip=client_ip,
            )

            print(
                f"[{datetime.now().isoformat()}] ✅ Generated {query_type} "
                f"query (op={op}, user={user_id})"
            )

        except Exception as e:
            print(f"[{datetime.now().isoformat()}] ❌ Unexpected error in generator loop: {e}")
            print("⏳ Waiting before retry...")

        # small delay so we don’t spam too hard
        time.sleep(random.uniform(3, 6))


if __name__ == "__main__":
    run()
