# ai_training/scripts/train_model.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
import joblib, os, numpy as np

DATA = "../data/query_logs.csv"
MODELS = "../models"
os.makedirs(MODELS, exist_ok=True)

df = pd.read_csv(DATA)
df["query_text"] = df["query_text"].fillna("")

# Vectorize text
vec = TfidfVectorizer(max_features=2000, stop_words="english")
X = vec.fit_transform(df["query_text"])

# Unsupervised to start (labels optional). If you have labels, you can evaluate:
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(X)

# Save artifacts
joblib.dump(vec, f"{MODELS}/vectorizer.pkl")
joblib.dump(model, f"{MODELS}/isolation_forest.pkl")
print("✅ Trained & saved to ai_training/models/")