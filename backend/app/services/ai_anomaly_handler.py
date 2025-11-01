import os
import psycopg2
import pandas as pd
import hashlib
import json
from datetime import datetime
from sklearn.ensemble import IsolationForest

# Environment configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@db:5432/securitydb").replace("postgresql+psycopg2", "postgresql")

# === Step 1: Connect to database ===
def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

# === Step 2: Train / load AI model ===
def train_ai_model():
    conn = get_db_connection()
    df = pd.read_sql("SELECT query_text, operation_type, executed_at FROM query_logs", conn)
    conn.close()

    if df.empty:
        print("⚠️ No data found for training AI model.")
        return None

    # Convert categorical features to numeric (simple encoding)
    df["operation_code"] = df["operation_type"].astype("category").cat.codes
    df["query_length"] = df["query_text"].apply(len)
    df["hour"] = pd.to_datetime(df["executed_at"]).dt.hour

    X = df[["operation_code", "query_length", "hour"]].values

    model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    model.fit(X)
    print("✅ AI anomaly model trained successfully.")
    return model

# === Step 3: Generate blockchain hash ===
def generate_block_hash(data: dict) -> str:
    encoded = json.dumps(data, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()

# === Step 4: Evaluate new queries and log results ===
def detect_and_log_anomalies(model):
    conn = get_db_connection()
    cur = conn.cursor()

    # Fetch latest unprocessed query logs (no blockchain hash yet)
    cur.execute("SELECT log_id, user_id, query_text, operation_type, executed_at FROM query_logs WHERE blockchain_hash IS NULL;")
    rows = cur.fetchall()

    for log_id, user_id, query_text, op_type, executed_at in rows:
        # Extract features
        op_code = {"SELECT":0, "INSERT":1, "UPDATE":2, "DELETE":3}.get(op_type.upper(), 0)
        features = [[op_code, len(query_text), executed_at.hour]]

        # Run through AI model
        prediction = model.predict(features)[0]
        score = model.decision_function(features)[0]
        is_anomalous = (prediction == -1)
        confidence = round(abs(score), 2)

        # Step 4a: Generate blockchain hash
        block_data = {
            "log_id": log_id,
            "query_text": query_text,
            "operation_type": op_type,
            "executed_at": executed_at.isoformat(),
            "is_anomalous": is_anomalous,
            "score": confidence,
        }
        block_hash = generate_block_hash(block_data)

        # Step 4b: Store hash in query_logs + anomalies + alerts if needed
        cur.execute("UPDATE query_logs SET blockchain_hash=%s WHERE log_id=%s;", (block_hash, log_id))

        if is_anomalous:
            cur.execute(
                "INSERT INTO anomalies (log_id, anomaly_score, is_anomalous, model_version) VALUES (%s, %s, %s, %s) RETURNING anomaly_id;",
                (log_id, confidence, True, 'v1')
            )
            anomaly_id = cur.fetchone()[0]
            cur.execute(
                "INSERT INTO alerts (anomaly_id, alert_type, confidence, status) VALUES (%s, %s, %s, 'Open');",
                (anomaly_id, 'Suspicious SQL Activity', confidence)
            )

        conn.commit()
        print(f"🔍 Processed log {log_id} | Anomaly={is_anomalous} | Hash={block_hash[:12]}...")

    cur.close()
    conn.close()
    print("✅ All pending logs processed successfully.")

if __name__ == "__main__":
    model = train_ai_model()
    if model:
        detect_and_log_anomalies(model)