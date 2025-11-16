from flask import Blueprint, jsonify
from app import db
from app.models import QueryLog, Anomaly, Alert
from sqlalchemy import func
from datetime import datetime, timedelta

metrics_bp = Blueprint("metrics", __name__)

@metrics_bp.route("/summary", methods=["GET"])
def metrics_summary():

    # Last 24 hours
    since_24h = datetime.utcnow() - timedelta(hours=24)

    # Total logs in 24h
    total_queries = (
        db.session.query(func.count(QueryLog.log_id))
        .filter(QueryLog.executed_at >= since_24h)
        .scalar()
    ) or 0

    # Suspicious = anomalies that are anomalous
    suspicious_queries = (
        db.session.query(func.count(Anomaly.anomaly_id))
        .filter(Anomaly.is_anomalous == True)
        .scalar()
    ) or 0

    # Open alerts = suspicious anomalies (since you have no alerts table yet)
    open_alerts = suspicious_queries

    # Blockchain verified
    verified_logs = (
        db.session.query(func.count(QueryLog.log_id))
        .filter(QueryLog.blockchain_hash.isnot(None))
        .scalar()
    ) or 0

    blockchain_verified = (
        round((verified_logs / total_queries) * 100)
        if total_queries > 0 else 0
    )

    return jsonify({
        "total_queries": total_queries,
        "suspicious_queries": suspicious_queries,
        "open_alerts": open_alerts,
        "blockchain_verified": blockchain_verified
    }), 200