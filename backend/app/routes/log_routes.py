from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import QueryLog, Alert
from app import db
import random
from datetime import datetime

# ✅ Import your real-time AI & hash module
from app.services.realtime_ai_monitor import process_new_query

log_bp = Blueprint("logs", __name__)

# ===========================
# FETCH LATEST LOGS
# ===========================
@log_bp.route("/", methods=["GET"])
@jwt_required(optional=True)
def list_logs():
    logs = QueryLog.query.order_by(QueryLog.executed_at.desc()).limit(100).all()
    return jsonify([
        {
            "id": l.log_id,
            "user_id": l.user_id,
            "query": l.query_text,
            "operation": l.operation_type,
            "time": l.executed_at.isoformat() if l.executed_at else None,
            "hash": l.blockchain_hash,
        } for l in logs
    ])


# ===========================
# ADD A NEW LOG (AI + HASH TRIGGER)
# ===========================
@log_bp.route("/add", methods=["POST"])
@jwt_required(optional=True)
def add_log():
    data = request.get_json()
    log = QueryLog(
        user_id=data.get("user_id"),
        query_text=data.get("query_text"),
        operation_type=data.get("operation_type"),
        client_ip=request.remote_addr,
    )
    db.session.add(log)
    db.session.commit()

    # 🧠 Trigger AI anomaly detection + hash creation immediately
    executed_at = datetime.utcnow()
    try:
        process_new_query(
            log_id=log.log_id,
            query_text=log.query_text,
            operation_type=log.operation_type,
            executed_at=executed_at
        )
    except Exception as e:
        print(f"⚠️ AI/Hash trigger failed for log {log.log_id}: {e}")

    return jsonify({"id": log.log_id, "status": "processed"}), 201


# ===========================
# FETCH ALERTS
# ===========================
@log_bp.route("/alerts", methods=["GET"])
def list_alerts():
    alerts = Alert.query.order_by(Alert.created_at.desc()).limit(100).all()
    results = []
    if not alerts:
        return jsonify([]), 200

    for a in alerts:
        confidence = float(a.confidence or 0)
        level = (
            "High" if confidence > 0.9
            else "Medium" if confidence > 0.75
            else "Info"
        )

        results.append({
            "alert_id": a.alert_id,
            "anomaly_id": a.anomaly_id,
            "alert_type": a.alert_type,
            "confidence": confidence,
            "level": level,
            "status": a.status,
            "created_at": a.created_at.isoformat() if a.created_at else None
        })

    return jsonify(results), 200