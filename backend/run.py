from app import create_app
from app.utils.db_init import init_db
from app.utils.startup_tasks import run_startup_tasks  # ← add this line

app = create_app()

if __name__ == "__main__":
    init_db()
    run_startup_tasks()   # ← run the auto-train + seed steps
    app.run(host="0.0.0.0", port=8000)
