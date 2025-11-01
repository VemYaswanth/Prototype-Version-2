from app import create_app
from app.utils.db_init import init_db
from app.utils.startup_tasks import run_startup_tasks
from app.services.ai_anomaly_handler import train_ai_model, detect_and_log_anomalies

app = create_app()

if __name__ == "__main__":
    init_db()
    run_startup_tasks()   # ← run the auto-train + seed steps
    app.run(host="0.0.0.0", port=8000)
if __name__ == "__main__":
    model = train_ai_model()
    if model:
        detect_and_log_anomalies(model)
    app.run(host="0.0.0.0", port=8000)
