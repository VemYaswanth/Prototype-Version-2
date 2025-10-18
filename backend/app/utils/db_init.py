from app import db
from sqlalchemy import inspect
from app.models.user import User
from app.models.query_log import QueryLog

def init_db():
    """Force-create all missing tables, ensuring models are registered."""
    engine = db.get_engine()
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())

    expected_tables = {"users", "query_logs"}
    missing = expected_tables - existing_tables

    if missing:
        print(f"🟢 Missing tables detected: {missing}. Creating them now...")
        db.create_all()
        print("✅ Database schema synchronized.")
    else:
        print("🟡 All required tables exist — no migration needed.")
