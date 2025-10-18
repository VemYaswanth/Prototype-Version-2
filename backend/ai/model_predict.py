import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import joblib,
from ai.model_train import train_model
def ensure_model():
    if not os.path.exists(MODEL_PATH):
        print("⚠️ Model missing, training new one...")
        # Simple fallback training data
        sample_logs = [
            "SELECT * FROM users;",
            "INSERT INTO orders (id, amount) VALUES (1,100);",
            "UPDATE employees SET salary=5000 WHERE id=2;",
            "DELETE FROM products WHERE id=3;"
        ]
        train_model(sample_logs)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from ai.preprocess import transform_queries

MODEL_PATH = os.getenv("MODEL_PATH", "backend/ai/isolation_forest.pkl")

def score_query(query_text: str):
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model not found. Train first.")
    model = joblib.load(MODEL_PATH)
    X = transform_queries([query_text])
    score = model.decision_function(X)[0]
    is_anomalous = model.predict(X)[0] == -1
    return {"score": round(float(score), 4), "is_anomalous": bool(is_anomalous), "model_version": "v1.0"}
