import os
import random
import time
from datetime import datetime
from sqlalchemy import create_engine, text

# Get DB URL from environment variable or fallback
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@db:5432/securitydb"
)

engine = create_engine(DATABASE_URL)

# List of users for linking logs
USERS = [
    (1, 'admin@ssems.net'),
    (2, 'analyst@ssems.net'),
    (3, 'auditor@ssems.net'),
    (4, 'developer@ssems.net'),
    (5, 'tester@ssems.net'),
    (6, 'security@ssems.net'),
    (7, 'intern@ssems.net'),
    (8, 'lead@ssems.net'),
    (9, 'manager@ssems.net'),
    (10, 'qa@ssems.net')
]

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

def ensure_users_exist():
    """Ensure all required users exist in the DB."""
    with engine.begin() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM users"))
        count = result.scalar()
        if count == 0:
            print("⚙️ Seeding users table...")
            conn.execute(text("""
                INSERT INTO users (email, password_hash, role, mfa_enabled)
                VALUES
                ('admin@ssems.net', 'admin123', 'admin', false),
                ('analyst@ssems.net', 'analyst123', 'analyst', false),
                ('auditor@ssems.net', 'auditor123', 'auditor', false),
                ('developer@ssems.net', 'developer123', 'developer', false),
                ('tester@ssems.net', 'tester123', 'tester', false),
                ('security@ssems.net', 'security123', 'security', false),
                ('intern@ssems.net', 'intern123', 'intern', false),
                ('lead@ssems.net', 'lead123', 'lead', false),
                ('manager@ssems.net', 'manager123', 'manager', false),
                ('qa@ssems.net', 'qa123', 'qa', false);
            """))
            print("✅ Users seeded successfully.")


def insert_query_log(query, operation_type, user_id, client_ip, suspicious=False):
    """Insert a new query log and, if suspicious, create an alert."""
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO query_logs (user_id, query_text, operation_type, client_ip)
            VALUES (:user_id, :query_text, :operation_type, :client_ip)
        """), {
            "user_id": user_id,
            "query_text": query,
            "operation_type": operation_type,
            "client_ip": client_ip
        })

        if suspicious:
            conn.execute(text("""
                INSERT INTO alerts (alert_type, confidence, message, status, created_at)
                VALUES (:alert_type, :confidence, :message, 'Open', NOW())
            """), {
                "alert_type": "Suspicious SQL Activity",
                "confidence": round(random.uniform(0.8, 0.99), 2),
                "message": query
            })


def run():
    ensure_users_exist()
    print("🚀 Auto Data Generator running...")

    while True:
        query_type = random.choice(["clean", "suspicious"])
        query = random.choice(SUSPICIOUS_QUERIES if query_type == "suspicious" else CLEAN_QUERIES)
        op = query.split()[0].upper()
        user_id = random.randint(1, len(USERS))
        client_ip = f"192.168.1.{random.randint(2, 255)}"

        try:
            insert_query_log(query, op, user_id, client_ip, suspicious=(query_type == "suspicious"))
            print(f"[{datetime.now().isoformat()}] ✅ Inserted {query_type} query log for user {user_id}")
        except Exception as e:
            print(f"[{datetime.now().isoformat()}] ❌ Error inserting query log: {e}")

        time.sleep(random.uniform(2, 4))  # adjustable delay


if __name__ == "__main__":
    run()