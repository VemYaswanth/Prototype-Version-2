import os
import time
from app import db
from app.models import User, QueryLog
from ai.model_train import train_model
from ai.model_predict import ensure_model, score_query

def auto_train_ai_model():
    """Train or load AI model automatically."""
    try:
        print("🤖 Checking for AI model files...")
        if not os.path.exists("ai/isolation_forest.pkl") or not os.path.exists("ai/vectorizer.pkl"):
            print("⚙️ Training AI model (first run)...")
            sample_logs = [
                "SELECT * FROM users;",
                "INSERT INTO orders (id, amount) VALUES (1,100);",
                "UPDATE employees SET salary=5000 WHERE id=2;",
                "DELETE FROM products WHERE id=3;"
            ]
            train_model(sample_logs)
            print("✅ AI model trained.")
        else:
            print("✅ Existing AI model found.")
    except Exception as e:
        print(f"❌ AI model setup failed: {e}")

def seed_database():
    """Insert a default admin user and example logs if DB is empty."""
    try:
        if not User.query.first():
            print("🌱 Seeding default user and demo logs...")
            admin = User(email="admin@example.com", password_hash="admin123", role="admin")
            db.session.add(admin)
            db.session.commit()

            demo_queries = [
                ("SELECT * FROM employees;", "SELECT"),
                ("UPDATE users SET role='root' WHERE id=1;", "UPDATE"),
                ("DELETE FROM orders WHERE id>100;", "DELETE")
            ]

            for q, op in demo_queries:
                log = QueryLog(user_id=admin.user_id, query_text=q, operation_type=op)
                db.session.add(log)
            db.session.commit()
            print("✅ Demo data inserted.")
        else:
            print("🟡 DB already seeded — skipping.")
    except Exception as e:
        print(f"❌ DB seed failed: {e}")

def run_startup_tasks():
    """Run all startup steps in sequence."""
    print("🚀 Running container startup tasks...")
    # Wait briefly for Postgres to be ready
    time.sleep(3)
    seed_database()
    auto_train_ai_model()
    print("✅ Startup tasks complete.")
