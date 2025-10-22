import hashlib, time, random
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@db:5432/securitydb"
engine = create_engine(DATABASE_URL)

def compute_suspicion(query):
    risky = ["DROP", "DELETE", "UPDATE", "GRANT", "ALTER", "INSERT"]
    score = sum(k in query.upper() for k in risky) / len(risky)
    return round(min(1.0, score + random.uniform(0.05, 0.15)), 2)

def generate_hash(prev_hash, query):
    data = f"{prev_hash}{query}{time.time()}"
    return hashlib.sha256(data.encode()).hexdigest()

def process_logs():
    with engine.begin() as conn:
        prev = conn.execute(text("SELECT block_hash FROM blockchain_logs ORDER BY blockchain_id DESC LIMIT 1;")).scalar()
        prev_hash = prev or "GENESIS"

        new_logs = conn.execute(text("SELECT log_id, query_text FROM query_logs WHERE blockchain_hash IS NULL;")).fetchall()
        for log_id, query in new_logs:
            suspicion = compute_suspicion(query)
            block_hash = generate_hash(prev_hash, query)
            conn.execute(text("UPDATE query_logs SET blockchain_hash=:h WHERE log_id=:i"), {"h": block_hash, "i": log_id})
            conn.execute(text("""
                INSERT INTO blockchain_logs (log_id, block_hash, block_index, transaction_id)
                VALUES (:id, :hash, (SELECT COALESCE(MAX(block_index),0)+1 FROM blockchain_logs), :txid)
            """), {"id": log_id, "hash": block_hash, "txid": block_hash[:12]})
            conn.execute(text("""
                INSERT INTO alerts (alert_type, confidence, message, level)
                VALUES ('Blockchain Suspicion', :c, :m,
                CASE WHEN :c > 0.8 THEN 'High' WHEN :c > 0.6 THEN 'Medium' ELSE 'Info' END)
            """), {"c": suspicion, "m": query})
            print(f"[+] Log {log_id} | Suspicion={suspicion} | Hash={block_hash[:10]}...")
            prev_hash = block_hash

if __name__ == "__main__":
    print("🧠 Blockchain Analyzer started.")
    while True:
        try:
            process_logs()
        except Exception as e:
            print(f"⚠️ Error: {e}")
        time.sleep(10)
