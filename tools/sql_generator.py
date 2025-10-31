# tools/sql_generator.py
import random, time, uuid, requests
from datetime import datetime

API_URL = "http://localhost:8000/api/log_query"   # your Flask API
NUM_SIM_USERS = 8
QPS = 5
ANOMALY_PROB = 0.02
RUN_SECONDS = 600

REGULAR = ["products","orders","customers","inventory","sessions"]
SENSITIVE = ["users","payments","admin_settings","credentials"]

def mk_query():
    if random.random() < ANOMALY_PROB:
        t = random.choice(SENSITIVE + REGULAR)
        return f"UPDATE {t} SET role='admin';", True, "update_no_where"
    # normal-ish
    t = random.choice(REGULAR)
    return f"SELECT * FROM {t} WHERE id = {random.randint(1,9999)};", False, "normal"

def main():
    stop = time.time() + RUN_SECONDS
    while time.time() < stop:
        q, is_anom, reason = mk_query()
        payload = {
            "user_id": random.randint(1, NUM_SIM_USERS),
            "query_text": q,
            "operation_type": q.split()[0].upper(),
            "executed_at": datetime.utcnow().isoformat()+"Z",
            "client_ip": f"10.0.0.{random.randint(2,254)}",
            "session_id": str(uuid.uuid4()),
            "injected_label": int(is_anom),
            "injected_reason": reason
        }
        try:
            requests.post(API_URL, json=payload, timeout=3)
        except Exception as e:
            print("post err:", e)
        time.sleep(max(0.01, random.expovariate(QPS)))
if __name__ == "__main__":
    main()
