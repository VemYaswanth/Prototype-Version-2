from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import QueryLog, Alert
from app import db
import random

log_bp = Blueprint("logs", __name__)

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
    return jsonify({"id": log.log_id}), 201

# app/routes/log_routes.py
# existing routes like list_logs() stay above...

@log_bp.route("/alerts", methods=["GET"])
def list_alerts():
    alerts = Alert.query.order_by(Alert.created_at.desc()).limit(100).all()
    results = []
    if not alerts:
        return jsonify([]), 200

    for a in alerts:
        confidence = float(a.confidence or 0)
        # derive level dynamically since the column no longer exists
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



