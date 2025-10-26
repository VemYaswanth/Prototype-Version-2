import random
import psycopg2
from datetime import datetime, timedelta
import uuid

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="securitydb",
    user="postgres",
    password="postgres",
    host="db",
    port="5432"
)
cur = conn.cursor()

operations = ["SELECT", "INSERT", "UPDATE", "DELETE"]

def random_query(op):
    if op == "SELECT":
        table = random.choice(["users", "transactions", "accounts", "logs"])
        return f"SELECT * FROM {table} WHERE id = {random.randint(1,1000)};"
    elif op == "INSERT":
        table = random.choice(["users", "transactions"])
        return f"INSERT INTO {table} VALUES ({random.randint(1,1000)}, 'dummy');"
    elif op == "UPDATE":
        table = random.choice(["users", "admins", "finance"])
        return f"UPDATE {table} SET password='hacked' WHERE id={random.randint(1,100)};"
    else:
        table = random.choice(["users", "logs"])
        return f"DELETE FROM {table} WHERE id={random.randint(1,100)};"

# ensure at least some users exist
for i in range(1, 6):
    cur.execute("""
        INSERT INTO users (email, password_hash, role)
        VALUES (%s, %s, %s)
        ON CONFLICT (email) DO NOTHING;
    """, (f"user{i}@test.com", "hashed_pwd", random.choice(["admin","auditor","viewer"])))

# main data seeding
for i in range(300):
    op = random.choice(operations)
    q = random_query(op)
    is_suspicious = random.random() < 0.25
    anomaly_score = round(random.uniform(0.3, 0.95), 2) if is_suspicious else round(random.uniform(0.0, 0.4), 2)
    session_id = str(uuid.uuid4())  # 🔑 convert to string here
    blockchain_hash = f"hash_{uuid.uuid4().hex[:10]}"

    cur.execute("""
        INSERT INTO query_logs (user_id, query_text, operation_type, executed_at, client_ip, session_id, blockchain_hash)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING log_id;
    """, (
        random.randint(1, 5),
        q,
        op,
        datetime.now() - timedelta(minutes=random.randint(0, 1000)),
        f"192.168.0.{random.randint(2,254)}",
        session_id,
        blockchain_hash
    ))

    log_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO anomalies (log_id, anomaly_score, is_anomalous, model_version)
        VALUES (%s, %s, %s, %s)
        RETURNING anomaly_id;
    """, (log_id, anomaly_score, is_suspicious, "v1.0"))

    anomaly_id = cur.fetchone()[0]

    if is_suspicious:
        cur.execute("""
            INSERT INTO alerts (anomaly_id, alert_type, confidence, status)
            VALUES (%s, %s, %s, %s);
        """, (
            anomaly_id,
            random.choice(["Suspicious UPDATE", "Mass DELETE", "Unusual SELECT", "Unauthorized INSERT"]),
            anomaly_score,
            random.choice(["Open", "Investigating", "Resolved"])
        ))

conn.commit()
cur.close()
conn.close()
print("✅ Seeded 300 mixed SQL logs successfully.")
