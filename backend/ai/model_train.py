import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib
from ai.preprocess import fit_vectorizer, clean_sql

MODEL_PATH = os.getenv("MODEL_PATH", "backend/ai/isolation_forest.pkl")

def train_model(logs):
    clean_logs = [clean_sql(q) for q in logs]
    vectorizer, X = fit_vectorizer(clean_logs)
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
    model.fit(X)
    joblib.dump(model, MODEL_PATH)
    print(f"✅ Model trained and saved at {MODEL_PATH}")

if __name__ == "__main__":
    # Example training set
    df = pd.read_csv("sample_logs.csv")  # e.g. exported pgAudit logs
    train_model(df['query_text'].tolist())
