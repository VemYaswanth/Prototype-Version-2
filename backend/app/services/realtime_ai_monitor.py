import os, hashlib, json, psycopg2
from datetime import datetime
from sklearn.ensemble import IsolationForest
import numpy as np

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db:5432/securitydb").replace("postgresql+psycopg2", "postgresql")

def connect_db():
    return psycopg2.connect(DATABASE_URL)

# === Generate Blockchain Hash ===
def generate_blockchain_hash(data: dict):
    encoded = json.dumps(data, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()

# === Lightweight on-demand model ===
def load_or_train_model():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT query_text, operation_type, executed_at FROM query_logs;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    if len(rows) < 5:
        return None  # not enough data yet

    X = []
    for q, op, t in rows:
        op_code = {"SELECT":0,"INSERT":1,"UPDATE":2,"DELETE":3}.get(op.upper(),0)
        X.append([op_code, len(q), t.hour])

    model = IsolationForest(contamination=0.15, random_state=42)
    model.fit(X)
    return model

# === Main function that triggers automatically ===
def process_new_query(log_id, query_text, operation_type, executed_at):
    model = load_or_train_model()
    conn = connect_db()
    cur = conn.cursor()

    op_code = {"SELECT": 0, "INSERT": 1, "UPDATE": 2, "DELETE": 3}.get(operation_type.upper(), 0)
    features = np.array([[op_code, len(query_text), executed_at.hour]])

    # Default values
    is_anomalous = False
    confidence = 0.5

    if model:
        pred = model.predict(features)[0]
        score = float(abs(model.decision_function(features)[0]))  # ensure Python float
        is_anomalous = bool(pred == -1)                           # ensure Python bool
        confidence = float(round(score, 2))                       # Python float

    # Generate blockchain hash (now fully JSON-serializable)
    payload = {
        "log_id": int(log_id),
        "query_text": str(query_text),
        "operation_type": str(operation_type),
        "executed_at": executed_at.isoformat(),
        "anomaly": is_anomalous,  # plain bool
        "score": confidence       # plain float
    }
    hash_val = generate_blockchain_hash(payload)

    # Update query log with hash
    cur.execute(
        "UPDATE query_logs SET blockchain_hash=%s WHERE log_id=%s;",
        (hash_val, log_id)
    )

    # If anomaly detected, insert alert + anomaly
    if is_anomalous:
        cur.execute(
            """
            INSERT INTO anomalies (log_id, anomaly_score, is_anomalous, model_version)
            VALUES (%s, %s, %s, %s)
            RETURNING anomaly_id;
            """,
            (log_id, confidence, True, "v1")
        )
        anomaly_id = cur.fetchone()[0]

        cur.execute(
            """
            INSERT INTO alerts (anomaly_id, alert_type, confidence, status)
            VALUES (%s, %s, %s, 'Open');
            """,
            (anomaly_id, "Suspicious Query Activity", confidence)
        )

    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Log {log_id} processed | Anomaly={is_anomalous} | Hash={hash_val[:12]}...")
