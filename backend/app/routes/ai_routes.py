# backend/app/routes/ai_routes.py
from flask import Blueprint, request, jsonify
from app.models import Anomaly, Alert, QueryLog, db
from ai.model_predict import score_query


ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/score", methods=["POST"])
def score():
    """
    Scores a given SQL query log using the AI anomaly detection model.
    Example input: {"log_id": 5}
    """
    data = request.get_json()
    log_id = data.get("log_id")

    ql = QueryLog.query.get(log_id)
    if not ql:
        return jsonify({"error": "Invalid log_id"}), 404

    result = score_query(ql.query_text)

    # Store anomaly result
    anomaly = Anomaly(
        log_id=log_id,
        anomaly_score=result["score"],
        is_anomalous=result["is_anomalous"],
        model_version=result["model_version"]
    )
    db.session.add(anomaly)
    db.session.commit()

    # If anomalous, raise alert
    if result["is_anomalous"]:
        alert = Alert(
            anomaly_id=anomaly.anomaly_id,
            alert_type="Suspicious Query",
            confidence=abs(result["score"]) * 100,
            status="Open"
        )
        db.session.add(alert)
        db.session.commit()

    return jsonify(result), 200
