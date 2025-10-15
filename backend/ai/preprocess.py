import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import os

VEC_PATH = os.getenv("VEC_PATH", "backend/ai/vectorizer.pkl")

def clean_sql(query: str) -> str:
    # Remove literals and formatting
    query = re.sub(r"'[^']*'", "?", query)
    query = re.sub(r"[0-9]+", "?", query)
    query = re.sub(r"\\s+", " ", query).strip().lower()
    return query

def fit_vectorizer(queries):
    vectorizer = TfidfVectorizer(max_features=500, analyzer='char', ngram_range=(2,5))
    X = vectorizer.fit_transform(queries)
    joblib.dump(vectorizer, VEC_PATH)
    return vectorizer, X

def load_vectorizer():
    return joblib.load(VEC_PATH)

def transform_queries(queries):
    if not os.path.exists(VEC_PATH):
        raise FileNotFoundError("Vectorizer not found. Train the model first.")
    vectorizer = load_vectorizer()
    return vectorizer.transform([clean_sql(q) for q in queries])
