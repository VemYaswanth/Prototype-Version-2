import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError, OperationalError

# Use the same DATABASE_URL as your backend container
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@db:5432/securitydb",
)


def table_exists(conn, table_name: str) -> bool:
    q = text("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = :t
        );
    """)
    return conn.execute(q, {"t": table_name}).scalar()


def column_exists(conn, table_name: str, column_name: str) -> bool:
    q = text("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_name = :t AND column_name = :c
        );
    """)
    return conn.execute(q, {"t": table_name, "c": column_name}).scalar()


def ensure_schema(conn):
    """
    Create all core tables if they don't exist.
    This matches your SQLAlchemy models (User, QueryLog, Anomaly, Alert, BlockchainLog).
    """
    schema_sql = """
    -- USERS (matches app/models/user.py)
    CREATE TABLE IF NOT EXISTS users (
        user_id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role VARCHAR(50) NOT NULL DEFAULT 'user',
        mfa_enabled BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- QUERY LOGS (matches app/models/query_log.py)
    CREATE TABLE IF NOT EXISTS query_logs (
        log_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(user_id),
        query_text TEXT NOT NULL,
        operation_type VARCHAR(50),
        executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        client_ip VARCHAR(100),
        session_id VARCHAR(100),
        blockchain_hash VARCHAR(255)
    );

    -- ANOMALIES (matches app/models/anomaly.py)
    CREATE TABLE IF NOT EXISTS anomalies (
        id SERIAL PRIMARY KEY,
        detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        description TEXT NOT NULL,
        severity VARCHAR(20) DEFAULT 'medium',
        source VARCHAR(100),
        resolved BOOLEAN DEFAULT FALSE
    );

    -- ALERTS (matches app/models/alert.py)
    CREATE TABLE IF NOT EXISTS alerts (
        alert_id SERIAL PRIMARY KEY,
        anomaly_id INTEGER REFERENCES anomalies(id),
        alert_type VARCHAR(100),
        confidence FLOAT,
        status VARCHAR(20),
        created_at TIMESTAMP,
        resolved_at TIMESTAMP
    );

    -- BLOCKCHAIN LOGS (matches app/models/blockchain_log.py)
    CREATE TABLE IF NOT EXISTS blockchain_logs (
        id SERIAL PRIMARY KEY,
        transaction_hash VARCHAR(255) NOT NULL,
        block_number INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status VARCHAR(50) DEFAULT 'pending'
    );
    """
    conn.execute(text(schema_sql))


def ensure_query_logs_columns(conn):
    """
    For existing databases that were created before session_id, etc.,
    add any missing NON-PK columns to query_logs.
    We deliberately do NOT touch log_id (PK).
    """
    if not table_exists(conn, "query_logs"):
        return

    required_querylog_columns = {
        "user_id": "INTEGER",
        "query_text": "TEXT",
        "operation_type": "VARCHAR(50)",
        "executed_at": "TIMESTAMP",
        "client_ip": "VARCHAR(100)",
        "session_id": "VARCHAR(100)",     # <-- this is the one causing 500s now
        "blockchain_hash": "VARCHAR(255)",
    }

    for col, col_type in required_querylog_columns.items():
        if not column_exists(conn, "query_logs", col):
            print(f"🟡 Adding missing column query_logs.{col}")
            try:
                conn.execute(text(f"ALTER TABLE query_logs ADD COLUMN {col} {col_type};"))
                print(f"✅ Added query_logs.{col}")
            except ProgrammingError as e:
                print(f"⚠️ Could not add column {col}: {e}")


def seed_admin(conn):
    """
    Seed a very simple default admin user if it doesn't exist.
    Adjust email/password or hashing later as needed.
    """
    try:
        exists = conn.execute(
            text("SELECT 1 FROM users WHERE email = :email LIMIT 1"),
            {"email": "admin@example.com"},
        ).fetchone()
    except ProgrammingError:
        # If users schema is odd for some reason, just skip seeding.
        print("⚠️ Could not check for admin user (users table mismatch?), skipping.")
        return

    if not exists:
        print("🌱 Inserting default admin user (admin@example.com / admin123)")
        conn.execute(
            text("""
                INSERT INTO users (email, password_hash, role, mfa_enabled)
                VALUES (:email, :pwd, 'admin', FALSE)
            """),
            {"email": "admin@example.com", "pwd": "admin123"},
        )
    else:
        print("✅ Admin user already exists.")


def init_db():
    print("🔄 Initializing database...")
    engine = create_engine(DATABASE_URL, isolation_level="AUTOCOMMIT")

    with engine.connect() as conn:
        try:
            print("📌 Creating schema (IF NOT EXISTS)...")
            ensure_schema(conn)
            print("✅ Schema ensured.")

            print("🔧 Reconciling query_logs columns (session_id, etc.)...")
            ensure_query_logs_columns(conn)
            print("✅ query_logs columns ensured.")

            print("🌱 Seeding default admin user if missing...")
            seed_admin(conn)
            print("✅ Admin user ensured.")

        except (ProgrammingError, OperationalError) as e:
            print(f"❌ Database initialization failed: {e}")
            raise

    print("✅ Database initialization script finished.")


if __name__ == "__main__":
    init_db()